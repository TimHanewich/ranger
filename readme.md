## What will be onboard ranger?
- Cell phone (for connectivity)
- 4S LiPo battery
- LM2596 DC Voltage step down module
- MPU-6050
- Raspberry Pi Zero W
- TT Motor
- SG-90 Servo
- Status lights (WS2812B)
- Voltage divider (for reading bat voltage)

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