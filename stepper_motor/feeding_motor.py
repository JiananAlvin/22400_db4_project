from machine import Pin, PWM
import time
import utime
import constant
import _thread
import random

class FeedingMotor:
    
    period = 30
    feedname = FeedingMotor
    new_request = False # Used to kill the current feeding motor thread

    def __init__(self, mode, period):
        self.mode = mode
        self.feedname = mode
        self.pinStep = Pin(constant.STEPPER_MOTOR_FOOD_STEP_PIN_NO, Pin.OUT)
        self.pinDir = Pin(constant.STEPPER_MOTOR_FOOD_DIR_PIN_NO, Pin.OUT)
        self.pinDir(1)
        self.pinStep.value(0)



    def read_value(self): # TODO
        """ Needs to be updated with proper values"""
        return 10

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
   

    def cycle(duration, period):
        if self.new_request:
                self.new_request = False
                _thread.exit()
        self.pinStep.value(1)
        utime.sleep_us(period)
        self.pinStep.value(0)
        utime.sleep_us(period)
    
    def update(duration, period):
        """ aux function, """

        for x in range(0, duration):
            if self.new_request:
                self.new_request = False
                _thread.exit()
            self.pinStep.value(1)
            utime.sleep_us(period)
            self.pinStep.value(0)
            utime.sleep_us(period) 

    
        
    
    

 