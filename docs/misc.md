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

## Fixing Motor Gear to Drive Gear Tension
`base_center` has the holes that the TT motor holder mounts into. Naturally, where these holes are are very important. I think I got it wrong in the first iteration - there is far too much tension, even possibly damaging the motors internal gears and causing it to malfunction (stall way too early).

I designed a few iterations of the `base_center` part, each one with varying distances:
- `base_center_v1` - what I started with, and what each next one is measured against.
- `base_center_v2` - 1mm more space - **This seems to be right!**

## Controlling the Servo
See [this video](https://www.youtube.com/watch?v=uOQk8SJso6Q) that describes very well how the SG-90 servo can be controlled.

Basically, a duty cycle of 1ms is 0%, 2ms is 100%. So you need to change the duty cycle from 1 to 2 ms to control the rotation, from 0-100%.

At 50 hz (standard for a servo), the full cycle is 20ms. So, using the `PWM.ChangeDutyCycle()` function of the `RPi.GPIO` module, you need to set the duty cycle to between 5% and 10% of the 20ms... that will get you from between 1ms and 2ms!

## Using `screen` to monitor incoming UART messages
Install `screen`: `sudo apt install screen`

Ensure a UART serial is available: `ls /dev/serial*`

Run screen to read the incoming messages on that serial connection: `sudo screen /dev/serial0 9600`

## Setting up a Raspberry Pi to run Ranger
- `sudo apt update` & `sudo apt upgrade`
- Install `pigpio`: `sudo apt install pigpio`
- Install `ffmpeg`: `sudo apt install ffmpeg`
- Install `libjpeg-dev`, a JPEG development library required for Python's `pillow`: `sudo apt-get install libjpeg-dev`
- Create and activate a Python virtual environment to install the following Python packages:
    - Install Python's `requests`: `python3 -m pip install requests`
    - Install Python's `pyserial`: `python3 -m pip install pyserial`
    - Install Python's `RPi.GPIO`: `python3 -m pip install RPi.GPIO` *(this normally comes with the Raspberry Pi, built in, but since we are in a virtual environment, need to install it explicitly)*
    - Install Python's `pigpio`: `python3 -m pip install pigpio`
    - Install Python's `psutil`: `python3 -m pip install psutil`
    - Install Python's `pillow` (`PIL`) library: `python3 -m pip install pillow`

## Other things
- Example grayscale, 160x120 photo captured and transmitted: https://i.imgur.com/Xx46fkX.png