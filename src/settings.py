# TT motor driver pins (not GPIO's, pin #'s)
pin_safety:int = 11 # the "safety" input of the L293D (top left) 
pin_drive1:int = 13 # the first drive pin of the L293D
pin_drive2:int = 15 # the second drive pin of the L293D

# SG-90 Servo for steering
# use GPIO # here, not pin #, because pigpio, what we'll be using to run the steering, using the GPIO #
gpio_steering:int = 23