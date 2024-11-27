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

        # internal variables to keep things smooth
        self.__last_steer__:float = None

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
        
    def execute(self, mc:MovementCommand.MovementCommand, stop_at_end:bool = True) -> None:

        # steer, then wait a moment
        time_to_wait:float = 0.3
        if self.__last_steer__ != mc.steer and self.__last_steer__ != None:
            steer_distance:float = abs(mc.steer - self.__last_steer__)
            time_to_wait:float = 0.05 * steer_distance
        self.steer(mc.steer)
        time.sleep(time_to_wait)

        # accelerate up to full power smoothly. It can always be assumed that we are at 0% power (at a standstill) right now, so accelerate up from that.
        accelerate_segments:list[float] = accelerate_in_segments(mc.drive)
        for power in accelerate_segments:
            self.drive(power)
            time.sleep(0.1)

        time.sleep(mc.duration)
        
        # decelerate smoothly
        for x in range(len(accelerate_segments)):
            ta:float = accelerate_segments[len(accelerate_segments) - x - 1]
            self.drive(ta)
            time.sleep(0.1)
        
        if stop_at_end:
            self.drive(0.0) # stop driving



def steer_in_segments(old_steer:float, new_steer:float) -> list[float]:
    steer_distance = abs(new_steer - old_steer)
    min_gapper:float = 0.15
    jumps_needed:int = int(math.floor(steer_distance / min_gapper))
    if jumps_needed > 0:
        true_gapper:float = steer_distance / jumps_needed
        if new_steer < old_steer:
            true_gapper = true_gapper * -1
        ToReturn:list[float] = []
        for x in range(jumps_needed):
            ToReturn.append(old_steer + (true_gapper * x))
        ToReturn.append(new_steer)
        ToReturn.pop(0)
        return ToReturn
    else:
        return [new_steer]


def accelerate_in_segments(power:float) -> list[float]:
    min_gapper:float = 0.1
    jumps_needed:int = int(abs(math.floor(power / min_gapper)))
    print(jumps_needed)
    if jumps_needed > 0:
        true_gapper:float = power / jumps_needed
        ToReturn:list[float] = []
        for x in range(jumps_needed):
            ToReturn.append(true_gapper * x)
        ToReturn.pop(0)
        ToReturn.append(power)
        return ToReturn
    else:
        return [power]