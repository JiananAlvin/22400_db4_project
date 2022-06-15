from machine import Pin, PWM
import constant


class CoolingMotor:

    def __init__(self):
        self.feedname = constant.FEEDNAME_COOL_MOTOR
        self.pin_step = PWM(Pin(constant.STEPPER_MOTOR_COOL_STEP_PIN_NO))  # Step
        self.pin_dir = Pin(constant.STEPPER_MOTOR_COOL_DIR_PIN_NO, Pin.OUT)  # Direction
        self.pin_dir(0)
        self.pin_step.freq(0)
        self.pin_step.duty(0)


    # overwrite server method
    def read_value(self):
        """ Returns tuple (freq, duty)"""
        return (self.freq, self.duty)


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

    
