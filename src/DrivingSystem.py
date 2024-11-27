# Borrowed from my "PYPER X" project and customized for Ranger
# Original code: https://raw.githubusercontent.com/TimHanewich/PYPER/refs/heads/master/derivatives/PYPER%20X/src/DrivingSystem.py

import pigpio # but pigpio, with a daemon running in the background, is used for the servo because that needs to be precise. RPi.GPIO is not precise enough (it "twitches")
import RPi.GPIO as GPIO # RPi.GPIO is used for driving (it is easy)
import time
import MovementCommand
import settings
import math

class DrivingSystem:

    def __init__(self) -> None:

        # setup GPIO's for drive
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(settings.pin_safety, GPIO.OUT)
        GPIO.setup(settings.pin_drive1, GPIO.OUT)
        GPIO.setup(settings.pin_drive1, GPIO.OUT)

        # setup PWM, using RPi.GPIO, for drive
        self.i1 = GPIO.PWM(settings.gpio_drive_i1, 50)
        self.i2 = GPIO.PWM(settings.gpio_drive_i2, 50)
        self.i1.start(0.0) # start at 0% duty cycle (no power)
        self.i2.start(0.0) # start at 0% duty cycle (no power)

        # setup pigpio for front steering (RPi.GPIO is not accurate enough in its timing to be stable: https://ben.akrin.com/raspberry-pi-servo-jitter/)
        self.pwm = pigpio.pi()
        self.pwm.set_mode(settings.pin_steering, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(settings.pin_steering, 50)



    ############## DRIVE #################

    def enable_drive(self) -> None:
        GPIO.output(settings.gpio_drive_safety, GPIO.HIGH)

    def disable_drive(self) -> None:
        GPIO.output(settings.gpio_drive_safety, GPIO.LOW)
    
    # provide power as float between -1.0 and 1.0
    def drive(self, power:float) -> None:
        power = max(min(power, 1.0), -1.0) # constrain within bounds
        if power >= 0.0:
            self.i1.ChangeDutyCycle(power * 100)
            self.i2.ChangeDutyCycle(0.0)
        else:
            self.i1.ChangeDutyCycle(0.0)
            self.i2.ChangeDutyCycle(power * -100)


    
    ############ STEER ##################
    def steer(self, steer:float) -> None:
        s = max(min(steer, 1.0), -1.0) # constrain within bounds
        spercent:float = (s + 1) / 2.0
        width:int = int(500 + (spercent * (2500 - 500)))
        self.pwm.set_servo_pulsewidth(settings.pin_steering, width)



    ############## HIGHER LEVEL #############
        
    def execute(self, mc:MovementCommand.MovementCommand) -> None:

        # steer, then wait a moment
        self.steer(mc.steer)
        time.sleep(0.25)

        # accelerate up to full power smoothly. It can always be assumed that we are at 0% power (at a standstill) right now, so accelerate up from that.
        self.drive(mc.drive)

        # sleep (wait)
        time.sleep(mc.duration)
        
        # stop driving
        self.drive(0.0)