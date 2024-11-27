# Ranger 
**PROJECT UNFINISHED**

A prototype, triple-deck, RC car, capable of going anywhere with cellular communications (phone tethered).

![ranger](https://i.imgur.com/isdL1Wh.png)

## What will be onboard ranger?
- Cell phone (for connectivity)
    - 81x170x13 mm
- 4S LiPo battery
    - 137x42x29 mm
- LM2596 DC Voltage step down module
    - 44x22x12 mm
- Raspberry Pi Zero W
    - 69x31x6 mm
- TT Motor
    - *dimensions not needed - already accomodated for in design*
- SG-90 Servo
    - *dimensions not needed - already accomodated for in design*
- Perfboard
    - Dimensions: 40x40x2 mm?
    - Voltage divider (for reading bat voltage)
        - Use a 47,000 ohm R1 resistor, 10,000 ohm R2 resistor, which divides it down to 17.54% of its actual voltage:
        - Fully charged 4S LiPo = 16.8v, divided down to 2.947v (safe to be read on ADC pin)
        - Fully dead 4S LiPo = 12.8v, divided down to 2.246v (safe to be read on ADC pin)
    - L293D motor driver
- Logitech C270 Webcam
- ~~Status lights (WS2812B)~~
- ~~MPU-6050~~
    - 16x21x4 mm

## Design File
Ranger's design file (Blender) can be downloaded [here](https://github.com/TimHanewich/ranger/releases/download/1/ranger7.blend).

## Communication Protocol
Azure Queue Storage will be used for bidirectional communication between the rover and a central command system. Two queues will be used (existing within the same storage account) - one for sending commands from the central command system ("controller" in this relationship) to the car and one for sending messages from the car to the central command system.

The messages exchanged will be in JSON format. Images can be shared from the car to central command by encoding these images in base64.

The minimum resolution that can be captured on the Logitech C270 is 160x120 (160 pixels in width, 120 pixels in height). This is a combined 19,200 pixels. With each pixel having three values (R,G,B), this would mean each image is 57,600 bytes. However, to save on bandwidth, monochrome (black and white) images will be used. This reduces the footprint of each image from 57,600 bytes down to 19,200 bytes, or one byte per pixel. Here is [an example 160x120 image in full color](https://i.imgur.com/pwf6wCL.jpeg) and here is [the monochrome version of that image](https://i.imgur.com/kpKrpUn.png).

The full image capturing and transmitting process will be the following:
1. Image is capture using fswebcam (saved locally to system).
2. Python script uses PIL to loop through each pixel of the image and "average" each pixel into a single monochrome value. See example [here](https://i.imgur.com/dd0vRru.png).
3. These monochrome byte values are added to a `bytearray`, which will total 19,200 bytes.
4. Python converts this `bytearray` into a base64-encoded string using the `base64` module. 
5. This base64-encoded string is posted as a message to Azure Queue Storage, included within a broader JSON object.
6. This queue message is received and the JSON object is deserialized in the central command system (likely .NET-based). See [this example](https://i.imgur.com/3s78G7d.png) on how to receive a Queue message in C#.
7. The base64-encoded string is extracted from the JSON object and converted to `byte[]`.
7. The central command system, written in .NET, uses `System.Drawing` to reconstruct the monochrome image, looping through each byte in the `byte[]` byte array and filling in each pixel one by one. See [this example](https://i.imgur.com/DMnJx8f.png).
8. The resulting image is saved and/or shown to the user of the central command system.

## How to set up a script to run on a Raspberry Pi (linux) on bootup:
Open the crontab editor:
```
crontab -e
```

Add a new cron job:
```
@reboot /usr/bin/python3 /path/to/your_script.py
```

In the above example, `usr/bin/python3/` is typically where Python is installed. Verify that before running this blindly...

Save and exit! Next time you reboot, that script will be run.

## How to capture images through USB web cam
See [this repo](https://github.com/TimHanewich/Raspberry-Pi-Capturing-Images) on how to do that!

## Notable Commits
- `f64b55bba3cd3c5fcbd638805026b2ee7ca7c1e0` - final commit before pivoting to smaller double-18650 battery pack (instead of 4S LiPo).

## Raspbian Lite Flash on Raspberry Pi Zero W on November 25, 2024
Hostname: ranger.local
Username: tim
Password: rolling

```
ssh tim@ranger.local
```

## Fixing Motor Gear to Drive Gear Tension
`base_center` has the holes that the TT motor holder mounts into. Naturally, where these holes are are very important. I think I got it wrong in the first iteration - there is far too much tension, even possibly damaging the motors internal gears and causing it to malfunction (stall way too early).

I designed a few iterations of the `base_center` part, each one with varying distances:
- `base_center_v1` - what I started with, and what each next one is measured against.
- `base_center_v2` - 1mm more space