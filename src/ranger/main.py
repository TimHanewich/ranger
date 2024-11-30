print("Hello, I'm Ranger!")
print("For more information about me, please visit https://github.com/TimHanewich/ranger")
print("Now loading dependencies...")
import vision
import settings
import comms
import time

def send_loop() -> None:
    """An infinitely running background process that continuously delivers messages to command via queue storage."""
    print("Entering beginning infinite send loop!")
    while True:

        # set up payload
        print("SEND: Preparing payload with standard inclusions...")
        payload:dict = comms.prepare() # prepares with standard inclusions

        # capture image?
        if settings.include_image:
            print("SEND: Capturing image... ")
            try:
                b64:str = vision.capture()
                imgdict:dict = {"base64": b64, "width": 160, "height": 120} # keep in mind that the base64 that is transmitted here is NOT the base64 of the JPEG image itself... i.e. you can't just save it as a JPEG. It instead is the base64 of the BYTES behind each pixel's grayscale value. So you have to reconstruct a bitmap, loop through all the pixels and then set the grayscale value. That is why the width and heigh is important here too.
                payload["image"] = imgdict
            except Exception as ex:
                print("SEND: Image capture failed! Msg: " + str(ex))

        # send
        print("SEND: Sending payload...")
        comms.send(payload)

        # wait period of time
        for i in range(settings.pulse_frequency_seconds):
            print("SEND: Sending next pulse in " + str(settings.pulse_frequency_seconds - i) + "... ")
            time.sleep(1.0)