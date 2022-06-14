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
            self.pin_step = Pin(constant.STEPPER_MOTOR_FEED_STEP_PIN_NO, Pin.OUT)
            self.pin_dir = Pin(constant.STEPPER_MOTOR_FEED_DIR_PIN_NO, Pin.OUT)
            self.pin_dir(1)
            self.pin_step.value(0)

        else:
            self.pin_step = PWM(Pin(constant.STEPPER_MOTOR_COOL_STEP_PIN_NO))  # Step
            self.pin_dir = Pin(constant.STEPPER_MOTOR_COOL_DIR_PIN_NO, Pin.OUT)  # Direction
            self.pin_dir(0)
            self.pin_step.freq(0)
            self.pin_step.duty(0)


    #overwrite server method 
    def read_value(self):
        return 10


    def update_cooling(self, args):
        """ Updates the feeding motor with given args:
            args[0] = direction
            args[1] = freq
            args[2] = duty
        """
        # PWM for the cooling pump
        direction, freq, duty = args[0], args[1], args[2]
        self.pin_dir(direction)
        self.pin_step.freq(freq)  # Frequency is the number of times per second that we repeat the on and off cycle -> rotating speed
        self.pin_step.duty(duty)  # Duty cycle refers the amount of time the pulse is ON -> voltage


    def update_feeding(self, args): 
        """ Updates the feeding motor with given args:
            args[0] = direction
            args[1] = duration
            args[2] = period
            This method uses a diferent thread every time it is called
        """
        self.new_request = True
        # bit-banging for the food dosing pump
        direction, duration, period = args[0], args[1], args[2]
        if self.new_request:
            self.new_request = False
            _thread.start_new_thread(update, (direction, duration, period))


    def update(direction, duration, period):
        """ aux function """
        for x in range(0, duration):
            if self.new_request:
                self.new_request = False
                _thread.exit()
            self.pin_dir(direction)
            self.pin_step.value(1)
            utime.sleep_us(period)
            self.pin_step.value(0)
            utime.sleep_us(period) 

    
        
    
    

 