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
- MPU-6050
    - 16x21x4 mm
- Raspberry Pi Zero W
    - 69x31x6 mm
- TT Motor
    - *dimensions not needed - already accomodated for in design*
- SG-90 Servo
    - *dimensions not needed - already accomodated for in design*
- Status lights (WS2812B)
- Perfboard
    - Dimensions: 40x40x2 mm?
    - Voltage divider (for reading bat voltage)
        - Use a 47,000 ohm R1 resistor, 10,000 ohm R2 resistor, which divides it down to 17.54% of its actual voltage:
        - Fully charged 4S LiPo = 16.8v, divided down to 2.947v (safe to be read on ADC pin)
        - Fully dead 4S LiPo = 12.8v, divided down to 2.246v (safe to be read on ADC pin)
    - L293D motor driver

## Design File
Ranger's design file (Blender) can be downloaded [here](https://github.com/TimHanewich/ranger/releases/download/1/ranger7.blend).

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