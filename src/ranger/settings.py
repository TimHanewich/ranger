# TT motor driver pins (not GPIO's, pin #'s)
pin_safety:int = 11 # the "safety" input of the L293D (top left) 
pin_drive1:int = 15 # the first drive pin of the L293D. Can swap this around with drive2 according to whatever pattern gives the correct forward/backward drive.
pin_drive2:int = 13 # the second drive pin of the L293D. Can swap this around with drive1 according to whatever pattern gives the correct forward/backward drive.

# SG-90 Servo for steering
# use GPIO # here, not pin #, because pigpio, what we'll be using to run the steering, using the GPIO #
gpio_steering:int = 23

# SAS URL to Azure Storage Queue that will be used to send messages to
azure_sas_url:str = ""