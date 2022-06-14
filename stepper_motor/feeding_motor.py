from machine import Pin, PWM
import time
import utime
import constant
import _thread
import random

class FeedingMotor:
    
    period = 0
    duration = 0
    feedname = constant.FEEDNAME_FOOD_MOTOR
    new_request = False # Used to kill the current feeding motor thread

    def __init__(self, mode, period):
        self.pinStep = Pin(constant.STEPPER_MOTOR_FOOD_STEP_PIN_NO, Pin.OUT)
        self.pinDir = Pin(constant.STEPPER_MOTOR_FOOD_DIR_PIN_NO, Pin.OUT)
        self.pinDir(1)
        self.pinStep.value(0)
        self.thread = _thread.start_new_thread(self.start, ())




    def read_value(self): # TODO
        """ Returns tuple (duration left, period)"""
        return (duration, period)

    def update(self, args): 
        """ Updates the feeding motor with given args:
            args[0] = duration
            args[1] = period
            This method uses a diferent thread every time it is called
        """
        self.new_request = True
        # bit-banging for the food dosing pump
        duration, period = args[0], args[1]
        if self.new_request:
            self.new_request = False
            _thread.start_new_thread(update , (duration,period))
   


    
    def update(self, duration, period):
        """ aux function, """
        self.duration = duration
        self.period = period
        
    def start(self):
        while(self.duration > 0):
            cycle(self.duration, self.period)
            self.duration-=1

    def cycle(period):
        """Bit-banging for the food dosing pump.
        Represents each cycle
        """
        self.pinStep.value(1)
        utime.sleep_us(period)
        self.pinStep.value(0)
        utime.sleep_us(period)



    
        
    
    

 