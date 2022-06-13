from machine import Pin, PWM
import time
import utime
import constant
import _thread

class StepperMotor():

    def __init__(self, mode):
        self.mode = mode
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


    def update_threading(self, args):
        # PWM for the cooling pump
        if self.mode == "cooling":
            freq, duty = args[0], args[1] 
            pinStep1.freq(freq)  # Frequency is the number of times per second that we repeat the on and off cycle -> rotating speed
            pinStep1.duty(duty)  # Duty cycle refers the amount of time the pulse is ON -> voltage
        # bit-banging for the food dosing pump
        else: 
            duration, period = args[0], args[1]
            for x in range(0, duration):
                pinStep2.value(1)
                utime.sleep_us(period)
                pinStep2.value(0)
                utime.sleep_us(period)

    def update(self, args):
        _thread.start_new_thread(self.update_threading, args)
    
        
    
    

 