# TT motor driver pins (not GPIO's, pin #'s)
pin_safety:int = 11 # the "safety" input of the L293D (top left) 
pin_drive1:int = 15 # the first drive pin of the L293D. Can swap this around with drive2 according to whatever pattern gives the correct forward/backward drive.
pin_drive2:int = 13 # the second drive pin of the L293D. Can swap this around with drive1 according to whatever pattern gives the correct forward/backward drive.

# SG-90 Servo for steering
# use GPIO # here, not pin #, because pigpio, what we'll be using to run the steering, using the GPIO #
gpio_steering:int = 23

# image capture command, using fswebcam
# this is the command that should be used to capture an image
capture_command:str = "fswebcam -d /dev/video0 -r 160x120 --skip 15 img.jpg"

# SAS URL to Azure Storage Queue that will be used to send messages to
# insert here the normal SAS URL. Not with any specified queue name, those will be added programatically
# when creating the SAS, you will be given a range of URL's for different services... blob, table, file, queue... make sure you copy and paste the **queue** URL, just as it is!
# the specific URL for the "r2c" and "c2r" queues will be inferred (inserted into URL) later.
# example: https://rangercomms.queue.core.windows.net/?sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-11-29T06:13:43Z&st=2024-11-28T22:13:43Z&spr=https,http&sig=UPVdKL03ESjtDDoL6%2Bc61dfr4opELJ2CKZc0KzqrrY%3D
azure_queue_sas_url:str = ""