import subprocess
import os
import settings
from PIL import Image
import base64
import time

def capture() -> str:
    """Makes a command line command to capture an image using fswebcam, converts it to grayscale, and returns the bytes of the image as base64"""

    # run command
    subprocess.run(settings.capture_command, shell=True, capture_output=True, text=True) # run the command
    time.sleep(0.25)

    # check if file exists
    if os.path.exists("./img.jpg") == False:
        raise Exception("File 'img.jpg' not found! Image capture must not have worked!")

    # open as image
    img = Image.open("./img.jpg")
    os.remove("./img.jpg") # delete the image
    width, height = img.size

    # get bytes
    ba:bytearray = bytearray()
    for y in range(0, height):
        for x in range(0, width):
            r,g,b = img.getpixel((x, y))
            avg:int = int((r + g + b) / 3)
            ba.append(avg)
    
    # return as base64
    b64:str = base64.b64encode(bytes(ba)).decode("utf-8")
    return b64