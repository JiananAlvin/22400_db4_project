from machine import Pin, PWM
import constant


class CoolingMotor:
    freq = 0
    duty = 0
    logger = None

    def __init__(self, logger):
        self.feedname = constant.FEEDNAME_COOL_MOTOR
        self.pin_step = PWM(Pin(constant.STEPPER_MOTOR_COOL_STEP_PIN_NO))  # Step
        self.pin_dir = Pin(constant.STEPPER_MOTOR_COOL_DIR_PIN_NO, Pin.OUT)  # Direction
        self.pin_dir(0)
        self.pin_step.freq(1)
        self.pin_step.duty(constant.DUTY_CYCLE)
        self.logger = logger

    # overwrite server method
    def read_value(self):
        """ Returns tuple (freq, duty)"""
        return self.freq

    def update_cooling(self, args):
        """ Updates the feeding motor with given args:
            args[0] = direction
            args[1] = freq
        """
        # PWM for the cooling pump
        self.direction, self.freq = args[0], args[1]
        if self.freq < 1:
            self.freq = 1
        self.pin_dir(self.direction)
        self.pin_step.freq(
            self.freq)  # Frequency is the number of times per second that we repeat the on and off cycle -> rotating speed
        self.logger.log("Updated feeding <%d,%d>" % (self.direction, self.freq))
