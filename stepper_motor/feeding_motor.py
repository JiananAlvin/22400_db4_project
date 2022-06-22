from machine import Pin
import time
import constant
import _thread
import math
import utime
from led.light_sensor import Light_Sensor
from logger.agent import Logger

class FeedingMotor:
    period = 0
    duration = 0
    feedname = constant.FEEDNAME_FOOD_MOTOR
    
    def __init__(self, logger, thread_manager, light_sensor):
        self.pinStep = Pin(constant.STEPPER_MOTOR_FEED_STEP_PIN_NO, Pin.OUT)
        self.pinDir = Pin(constant.STEPPER_MOTOR_FEED_DIR_PIN_NO, Pin.OUT)
        self.pinDir(1)
        self.pinStep.value(0)
        self.start_up_time = time.time()
        self.light_sensor = light_sensor
        self.logger = logger

        thread_manager.run(self.start, ())

    


    # Automation 
    def t(self):
        """ Returns time passed since start up"""
        return time.time() - self.start_up_time

    # TODO change this to the actual content of flora's formula
    def FlorasFormula(self):
        """ needs to be filled """
        light_intensity = self.light_sensor.read_value() 
        light_intensity = light_intensity if light_intensity > 0 else 1
        I0 = 1024
        OD = -math.log10(light_intensity / I0)
        concentration = 6*(10**6)*OD - 27945
        pump_rate = 64800000 / concentration
        return pump_rate

    # TODO change this to the actual content of Jianan's formula
    def JianansFormula(self, pump_rate):
        """ needs to be filled """
        print("\n\n\nPUMP RATE: %d" % pump_rate)
        period = int(60000/(3200* (0.2198 * pump_rate - 0.0592) ))
        period = period if period > 500 else 500
        duration = constant.STEPPER_MOTOR_FEED_UPDATE_PERIOD
        self.update_feeding([period, duration])



    def read_value(self):  # TODO
        """ Returns 0 for now"""
        return self.duration

    def update_feeding(self, args):
        """ Updates the feeding motor with given args:
            args[0] = duration
            args[1] = period
        """
        self.duration = args[1]
        self.period = args[0]
        self.logger.log("Updated feeding <%d,%d>" % (self.duration, self.period), self.feedname)

    def start(self, lock): # TODO i commited after changing this function, so if any exception happens its probably here
        while (True):
            self.JianansFormula(self.FlorasFormula())            # This should be enough with the updated methods below
            final_time = time.time() + 20
            if self.period < 1000:
                while (time.time() < final_time):
                    self.cycle(self.period)

               # self.duration -= 1 # TODO improve this
            #time.sleep(constant.STEPPER_MOTOR_FEED_UPDATE_PERIOD)
            self.logger.log("Finished feeding <%d,%d>" % (self.duration, self.period), self.feedname)

            

    def cycle(self, period):
        """Bit-banging for the food dosing pump.
        Represents each cycle
        """
      #  print("THIS IS A CYCLE %d" % period)
        self.pinStep.value(1)
        time.sleep(period / (10**6))
        self.pinStep.value(0)
        time.sleep(period / (10**6))



