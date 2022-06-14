from machine import Pin, PWM
import time
import utime
import constant
import _thread
import random

class StepperMotor:
    
    period = 30
    new_request = False # Used to kill the current feeding motor thread

    def __init__(self, mode, period):
        self.mode = mode
        self.feedname = mode
        if mode == "feeding":
            self.pinStep = Pin(constant.STEPPER_MOTOR_FOOD_STEP_PIN_NO, Pin.OUT)
            self.pinDir = Pin(constant.STEPPER_MOTOR_FOOD_DIR_PIN_NO, Pin.OUT)
            self.pinDir(1)
            self.pinStep.value(0)

        else:
            self.pinStep = PWM(Pin(constant.STEPPER_MOTOR_COOL_STEP_PIN_NO))  # Step
            self.pinDir = Pin(constant.STEPPER_MOTOR_COOL_DIR_PIN_NO, Pin.OUT)  # Direction
            self.pinDir(0)
            self.pinStep.freq(0)
            self.pinStep.duty(0)


    #overwrite server method 
    def read_value(self):
        return 10

    def update_cooling(self, args):
        """ Updates the feeding motor with given args:
            args[0] = freq
            args[1] = duty
        """
        # PWM for the cooling pump
        freq, duty = args[0], args[1] 
        self.pinStep.freq(freq)  # Frequency is the number of times per second that we repeat the on and off cycle -> rotating speed
        self.pinStep.duty(duty)  # Duty cycle refers the amount of time the pulse is ON -> voltage
    
    
    def update_feeding(self, args): 
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
   

    def update(duration, period):
        """ aux function """
        for x in range(0, duration):
            if self.new_request:
                self.new_request = False
                _thread.exit()
            self.pinStep.value(1)
            utime.sleep_us(period)
            self.pinStep.value(0)
            utime.sleep_us(period) 

    
        
    
    

 