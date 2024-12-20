print("Hello, I'm Ranger!")
print("For more information about me, please visit https://github.com/TimHanewich/ranger")
print("Now loading dependencies...")
import vision
import settings
import time
import threading
import utilities
import AzureQueue
import sensitive
import json
import DrivingSystem
import MovementCommand
import vision
import atexit
import VoltageSensor

# variables we will be tracking and reporting on
program_began:float = time.time()
msgrecv:int = 0 # the number of messages ranger has received so far

# ensure the pigpiod daemon is running - that will be needed to accurately control the steering servo with precision
while utilities.pigpiod_running() == False:
    print("pigpio daemon not running! Attempting to start now...")
    utilities.start_pigpiod()
    time.sleep(1.0)
print("pigpio dameon confirmed to be running!")

# check if webcam is connected if the settings call for imagery capture via webcam
if settings.include_image:
    print("Checking if webcam is connected...")
    if utilities.webcam_connected():
        print("Webcam is connected!")
    else:
        print("Setting 'include_image' is tuned on yet a webcam was not detected! Turning off `include_image`...")
        settings.include_image = False

# if settings call for imagery capture (vision), start ffmpeg stream via vision
vcs:vision.VisionCaptureService = None # declare as None just so the remainder of the program knows the variable exists, even if it is none
if settings.include_image:
    print("Starting FFMPEG background stream...")
    vcs = vision.VisionCaptureService() # tool for streaming via ffmpeg in the background
    vcs.start_streaming() # starts background process
    if vcs.streaming():
        print("FFMPEG background stream now running!")
    else:
        print("FAILURE! FFMPEG background stream didn't seem to work!")

# set up voltage sensor
vs:VoltageSensor.VoltageSensor = VoltageSensor.VoltageSensor()

# set up driving system
ds:DrivingSystem.DrivingSystem = DrivingSystem.DrivingSystem()
ds.enable_drive() # turn on "failsafe" pin
ds.drive(0.0) # start at no power!
ds.steer(0.0) # start at steering in middle

def send_loop() -> None:
    """An infinitely running background process that continuously delivers messages to command via queue storage."""

    # create Queue Storage service
    qs:AzureQueue.QueueService = AzureQueue.QueueService(sensitive.azure_queue_url_send, sensitive.azure_queue_sas)

    print("Entering beginning infinite send loop!")
    while True:

        # set up payload
        print("SEND: Preparing payload with standard inclusions...")
        payload:dict = utilities.prepare_payload() # prepares with standard inclusions

        # add uptime
        payload["uptime"] = int(time.time() - program_began)

        # add msgrev (number of commands that have been received)
        payload["msgrecv"] = msgrecv

        # add battery voltage
        payload["batsoc"] = vs.soc() # battery state of charge (as a percentage between 0.0 and 1.0)

        # capture image?
        if settings.include_image: # if the settings are to include the imag
            if vcs.streaming(): # if we are still currently streaming w/ ffmpeg
                print("SEND: Capturing image... ")
                try:
                    latest_img:bytes = vcs.latest_image() # retrieve the most recent save from the FFMPEG stream, as bytes
                    b64:str = vision.process_image(latest_img) # open the JPG image bytes, open it as an Image, loop through each pixel, convert to grayscale, save those grayscale bytes, and then convert it to base64 (plain string)
                    imgdict:dict = {"base64": b64, "width": 160, "height": 120} # keep in mind that the base64 that is transmitted here is NOT the base64 of the JPEG image itself... i.e. you can't just save it as a JPEG. It instead is the base64 of the BYTES behind each pixel's grayscale value. So you have to reconstruct a bitmap, loop through all the pixels and then set the grayscale value. That is why the width and heigh is important here too.
                    payload["image"] = imgdict
                except Exception as ex:
                    print("SEND: Image capture failed! Msg: " + str(ex))
            else:
                print("SEND: Image capture is on but streaming is off! Perhaps it failed? Not including photo because the photo may be old, out of date.")

        # send
        print("SEND: Sending payload...")
        qs.put(json.dumps(payload)) # send as JSON

        # wait period of time
        for i in range(settings.pulse_frequency_seconds):
            print("SEND: Sending next pulse in " + str(settings.pulse_frequency_seconds - i) + "... ")
            time.sleep(1.0)

def recv_loop() -> None:
    """An infinite loop to receive new commands from command."""

    # global variables (need to declare them as global here to be able to read them from a thread)
    global msgrecv

    # create Queue Storage service
    qs:AzureQueue.QueueService = AzureQueue.QueueService(sensitive.azure_queue_url_recv, sensitive.azure_queue_sas)
    print("RECV: Clearing receive queue of any old messages")
    qs.clear() # clear the queue to begin (we don't want to process any old messages, want to start from a new slate)

    # infinite receive loop
    while True:
        
        # receive command
        print("RECV: Checking for commands...")
        msg:AzureQueue.QueueMessage = qs.receive()
        if msg != None:
            print("RECV: Message of length " + str(len(msg.MessageText)) + " received!")
            msgrecv = msgrecv + 1
            
            # parse message text as json
            command:dict = None
            print("RECV: Parsing message as JSON...")
            try:
                command = json.loads(msg.MessageText)
            except Exception as e:
                print("RECV: JSON Parse failed! Exception msg: " + str(e))
                command = None
            
            # if it was parsed as JSON successfully, proceed with the command
            if command != None:

                # get movement commands? And if there are some, execute
                if "move" in command:
                    movement_commands:list[MovementCommand.MovementCommand] = MovementCommand.MovementCommand.parse(str(json.dumps(command["move"])))
                    print("RECV: " + str(len(movement_commands)) + " movement command(s) received!")
                    on_number:int = 1
                    for mc in movement_commands:
                        print("RECV: executing MC " + str(on_number) + " / " + str(len(movement_commands)) + "... ")
                        ds.execute(mc, False, True)
                        on_number = on_number + 1
                    ds.drive(0.0) # stop at the end of all of them
            
            # delete the message
            print("RECV: Deleting message '" + msg.MessageId + "'...")
            qs.delete(msg.MessageId, msg.PopReceipt)
        
        # wait
        for i in range(settings.recv_frequency_seconds):
            print("RECV: Checking for commands in " + str(settings.recv_frequency_seconds - i) + "... ")
            time.sleep(1.0)

def cleanup() -> None:
    """A cleanup function that will run upon program termination, regardless of HOW the program is terminated"""

    # terminate FFMPEG streaming
    if vcs != None:
        vcs.stop_streaming() # kill the streaming process
        if vcs.streaming() == False:
            print("FFMPEG streaming successfully terminated via cleanup!")
        else:
            print("FFMPEG termination failed! It may be still running!")

    # close serial communication on battery
    vs.close()
    print("Battery monitor via serial communications closed as part of cleanup")

    # turn off driving
    ds.disable_drive() # disable drive (turn off safety)
    print("Drive disabled as part of cleanup")
    ds.pwm.stop() # stop the PWM
    print("Steering PWM stopped as part of cleanup")
atexit.register(cleanup)

# start threads
thread_send_loop = threading.Thread(target=send_loop)
thread_recv_loop = threading.Thread(target=recv_loop)
thread_send_loop.start()
thread_recv_loop.start()

# do nothing, keeping the program alive while allowing the threads to do work
while True:
    time.sleep(1)