# Borrowed from my "PYPER X" project and customized for Ranger
# Original code: https://raw.githubusercontent.com/TimHanewich/PYPER/refs/heads/master/derivatives/PYPER%20X/src/DrivingSystem.py

import pigpio # but pigpio, with a daemon running in the background, is used for the servo because that needs to be precise. RPi.GPIO is not precise enough (it "twitches")
import RPi.GPIO as GPIO # RPi.GPIO is used for driving (it is easy)
import time
import MovementCommand
import settings
from typing import Union

class DrivingSystem:
    def __init__(self) -> None:

        # setup GPIO's for drive
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(settings.pin_safety, GPIO.OUT)
        GPIO.setup(settings.pin_drive1, GPIO.OUT)
        GPIO.setup(settings.pin_drive2, GPIO.OUT)

        # setup PWM, using RPi.GPIO, for drive
        self.i1 = GPIO.PWM(settings.pin_drive1, 50)
        self.i2 = GPIO.PWM(settings.pin_drive2, 50)
        self.i1.start(0.0) # start at 0% duty cycle (no power)
        self.i2.start(0.0) # start at 0% duty cycle (no power)

        # setup pigpio for front steering (RPi.GPIO is not accurate enough in its timing to be stable: https://ben.akrin.com/raspberry-pi-servo-jitter/)
        self.pwm = pigpio.pi()
        self.pwm.set_mode(settings.gpio_steering, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency(settings.gpio_steering, 50)



    ############## DRIVE #################

    def enable_drive(self) -> None:
        GPIO.output(settings.pin_safety, GPIO.HIGH)

    def disable_drive(self) -> None:
        GPIO.output(settings.pin_safety, GPIO.LOW)
    
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
        s = max(min(steer, 1.0), -1.0) # constrain within absolute bounds
        min_constraint:float = abs(settings.steering_limit) * -1
        max_constraint:float = abs(settings.steering_limit)
        s = min_constraint + ((max_constraint - min_constraint) * ((s +1) / 2.0)) # constrain within steering bounds
        spercent:float = (s + 1) / 2.0
        width:int = int(500 + (spercent * (2500 - 500)))
        self.pwm.set_servo_pulsewidth(settings.gpio_steering, width)



    ######### CLEANUP #############
    def cleanup(self) -> None:
        """Turns off all PWM's and cleans up (releases control)"""
        self.i1.stop()
        self.i2.stop()
        GPIO.cleanup()



    ############## HIGHER LEVEL #############
        
    def execute(self, mc:MovementCommand.MovementCommand, stop_at_end:bool = True, steering_pause:bool = True):
        # steer, then wait a moment
        self.steer(mc.steer)
        if steering_pause:
            time.sleep(0.25)

        # accelerate up to full power smoothly. It can always be assumed that we are at 0% power (at a standstill) right now, so accelerate up from that.
        self.drive(mc.drive)

        # sleep (wait)
        time.sleep(mc.duration)
        
        # stop driving?
        if stop_at_end:
            self.drive(0.0)