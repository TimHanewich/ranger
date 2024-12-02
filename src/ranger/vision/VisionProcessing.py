from PIL import Image
import base64
import io

def process_image(img:bytes) -> str:
    """Takes a JPG image, represented as bytes, turns each pixel to grayscale, and encodes the RGB pixel values as base64 and returns that."""

    # open image with PIL
    img = Image.open(io.BytesIO(img))
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