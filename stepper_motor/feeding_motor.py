from machine import Pin
import utime
import constant
import _thread


class FeedingMotor:
    period = 0
    duration = 10000
    feedname = constant.FEEDNAME_FOOD_MOTOR
    self.logger = None

    def __init__(self, logger, thread_pool):
        self.pinStep = Pin(12, Pin.OUT)
        self.pinDir = Pin(constant.STEPPER_MOTOR_FEED_DIR_PIN_NO, Pin.OUT)
        self.pinDir(1)
        self.pinStep.value(0)
        self.thread =  _thread.start_new_thread(self.start, ())

    def read_value(self):  # TODO
        """ Returns tuple (duration left, period)"""
        return (self.duration, self.period)

    def update_feeding(self, args):
        """ Updates the feeding motor with given args:
            args[0] = duration
            args[1] = period
            This method uses a different thread every time it is called
        """
        self.duration = args[0]
        self.period = args[1]
        self.logger.log("Updated feeding <%d,%d>" % (self.duration, self.period), self.feedname)

    def start(self):
        while (True):
            while (self.duration > 0):
                self.cycle(self.period)
                self.duration -= 1

    def cycle(self, period):
        """Bit-banging for the food dosing pump.
        Represents each cycle
        """
        self.pinStep.value(1)
        utime.sleep_us(period)
        self.pinStep.value(0)
        utime.sleep_us(period)
