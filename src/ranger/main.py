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
        try:
            b64:str = vision.capture()
            imgdict:dict = {"base64": b64, "width": 160, "height": 120} # keep in mind that the base64 that is transmitted here is NOT the base64 of the JPEG image itself... i.e. you can't just save it as a JPEG. It instead is the base64 of the BYTES behind each pixel's grayscale value. So you have to reconstruct a bitmap, loop through all the pixels and then set the grayscale value. That is why the width and heigh is important here too.
            payload["image"] = imgdict
        except Exception as ex:
            print("Image capture failed! Msg: " + str(ex))

    # send
    print("Sending payload...")
    comms.send(payload)

    # wait period of time
    for i in range(settings.pulse_frequency_seconds):
        print("Sending next pulse in " + str(settings.pulse_frequency_seconds - i) + "... ")
        time.sleep(1.0)