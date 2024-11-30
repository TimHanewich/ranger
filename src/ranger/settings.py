# PROGRAM SETTINGS
pulse_frequency_seconds:int = 10 # Ranger will send an update every X seconds
recv_frequency_seconds:int = 5 # Ranger will check the receive queue every X seconds for a command from central command
include_image:bool = True # include an image in each pulse (capture using onboard webcam)

# TT motor driver pins (not GPIO's, pin #'s)
pin_safety:int = 11 # the "safety" input of the L293D (top left) 
pin_drive1:int = 15 # the first drive pin of the L293D. Can swap this around with drive2 according to whatever pattern gives the correct forward/backward drive.
pin_drive2:int = 13 # the second drive pin of the L293D. Can swap this around with drive1 according to whatever pattern gives the correct forward/backward drive.

# SG-90 Servo for steering
# use GPIO # here, not pin #, because pigpio, what we'll be using to run the steering, using the GPIO #
gpio_steering:int = 23
steering_limit:float = 0.35 # limits steering to this percent in both directions. i.e. if you set this to 0.5, it would set the max right steering to 0.5 and max left steering to -0.5

# image capture command, using fswebcam
# this is the command that should be used to capture an image
capture_command:str = "fswebcam -d /dev/video0 -r 160x120 --no-banner --skip 15 img.jpg"