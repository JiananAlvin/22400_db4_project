from machine import Pin, PWM
import time
import utime
import constant
import _thread
import random


class FeedingMotor():
    
    period = 0
    duration = 10000 
    feedname = constant.FEEDNAME_FOOD_MOTOR

    def __init__(self):
        self.pinStep = Pin(constant.STEPPER_MOTOR_FOOD_STEP_PIN_NO, Pin.OUT)
        self.pinDir = Pin(constant.STEPPER_MOTOR_FOOD_DIR_PIN_NO, Pin.OUT)
        self.pinDir(1)
        self.pinStep.value(0)
        self.thread = _thread.start_new_thread(self.start, ())



    def read_value(self): # TODO
        """ Returns tuple (duration left, period)"""
        return (self.duration, self.period)

    def update_feeding(self, args): 
        """ Updates the feeding motor with given args:
            args[0] = duration
            args[1] = period
            This method uses a diferent thread every time it is called
        """
        self.duration = duration
        self.period = period

        

    def start(self):
        while(True):
            while(self.duration > 0):
                self.cycle(period)
                self.duration-=1

    def cycle(self, period):
        """Bit-banging for the food dosing pump.
        Represents each cycle
        """
        self.pinStep.value(1)
        utime.sleep_us(period)
        self.pinStep.value(0)
        utime.sleep_us(period)



    
        
    
    

 