from machine import Pin
import time
import constant
import _thread
import math
import utime


class FeedingMotor:
    period = 0
    duration = 0
    feedname = constant.FEEDNAME_FOOD_MOTOR
    
    def __init__(self, logger, thread_manager, light_sensor):
        self.pinStep = Pin(12, Pin.OUT)
        self.pinDir = Pin(constant.STEPPER_MOTOR_FEED_DIR_PIN_NO, Pin.OUT)
        self.pinDir(1)
        self.pinStep.value(0)
        thread_manager.run(self.start, ())
        self.start_up_time = time.time()
        self.light_sensor = light_sensor
        self.logger = logger


    def read_value(self):  # TODO
        """ Returns 0 for now"""
        return 0

    def update_feeding(self, args):
        """ Updates the feeding motor with given args:
            args[0] = duration
            args[1] = period
        """
        self.duration = args[0]
        self.period = args[1]
        self.logger.log("Updated feeding <%d,%d>" % (self.duration, self.period), self.feedname)

    def start(self, lock): # TODO i commited after changing this function, so if any exception happens its probably here
        while (True):
            self.JianansFormula(self.FlorasFormula())            # This should be enough with the updated methods below
            final_time = self.t() + self.duration
            while (time.time() < final_time):
                self.cycle(self.period)
               # self.duration -= 1 # TODO improve this
            time.sleep(constant.STEPPER_MOTOR_FEED_UPDATE_PERIOD)
        self.logger.log("Finished feeding <%d,%d>" % (self.duration, self.period), self.feedname)

            

    def cycle(self, period):
        """Bit-banging for the food dosing pump.
        Represents each cycle
        """
        self.pinStep.value(1)
        utime.sleep_us(period)
        self.pinStep.value(0)
        utime.sleep_us(period)




    # Automation 
    def t(self):
        """ Returns time passed since start up"""
        return time.time() - self.start_up_time

    # TODO change this to the actual content of flora's formula
    def FlorasFormula(self):
        """ needs to be filled """
        light_intensity = self.light_sensor.read_value()
        t = self.t()
        pump_rate = 0
        return pump_rate

    # TODO change this to the actual content of Jianan's formula
    def JianansFormula(self, pump_rate):
        """ needs to be filled """
        
        period = 10
        duration = 100
        self.update_feeding([period, duration])
