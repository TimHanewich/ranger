from PIL import Image

img = Image.open("../../sample160x120.jpg")
width, height = img.size

ba:bytearray = bytearray()
for y in range(0, height):
    for x in range(0, width):
        r,g,b = img.getpixel((x, y))
        avg:int = int((r + g + b) / 3)
        ba.append(avg)

print("Complete!")
print("Bytearray length of monochrome: " + str(len(ba)))