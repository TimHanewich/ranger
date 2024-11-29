print("Hello, I'm Ranger! Now loading...")
import vision
import settings
import comms
import time

print("Entering infinite loop!")
while True:

    # set up payload
    print("Preparing payload with standard inclusions...")
    payload:dict = comms.prepare() # prepares with standard inclusions

    # capture image?
    if settings.include_image:
        print("Capturing image... ")
        b64:str = vision.capture()
        imgdict:dict = {"base64": b64, "width": 160, "height": 120}
        payload["image"] = imgdict

    # send
    print("Sending payload...")
    comms.send(payload)

    # wait period of time
    for i in range(settings.pulse_frequency_seconds):
        print("Sending next pulse in " + str(settings.pulse_frequency_seconds - i) + "... ")
        time.sleep(1.0)