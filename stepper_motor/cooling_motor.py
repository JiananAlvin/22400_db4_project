from machine import Pin, PWM
import constant
from PID.pid import PID
from temperature_sensor.read_temp import TemperatureSensor
import time

class CoolingMotor:
    freq = 0
    duty = 0
    logger = None
    feedname = constant.FEEDNAME_COOL_MOTOR
    pid = PID(constant.P,constant.I,constant.D)




    def __init__(self, logger, thread_manager, temperature_sensor):
        self.pin_step = PWM(Pin(constant.STEPPER_MOTOR_COOL_STEP_PIN_NO))  # Step
        self.pin_dir = Pin(constant.STEPPER_MOTOR_COOL_DIR_PIN_NO, Pin.OUT)  # Direction
        self.pin_dir(0)
        self.pin_step.freq(1)
        self.pin_step.duty(0)
        self.logger = logger
        thread_manager.run(self.PIDupdater, (5,temperature_sensor))

    # overwrite server method
    def read_value(self):
        """ Returns tuple (freq, duty)"""
        return (self.freq, self.duty)

    def update_cooling(self, args):
        """ Updates the feeding motor with given args:
            args[0] = direction
            args[1] = freq
        """
        # PWM for the cooling pump
        self.direction, self.freq = args[0], args[1]
        self.pin_dir(self.direction)
        self.pin_step.freq(
            self.freq)  # Frequency is the number of times per second that we repeat the on and off cycle -> rotating speed
        self.pin_step.duty(constant.DUTY_CYCLE)  # Duty cycle refers the amount of time the pulse is ON -> voltage
        self.logger.log("Updated cooling <%d,%d>" % (self.direction, self.freq), self.feedname)

    def PIDupdater(self, period, temperature_sensor):
        """
        >>> period: Time between updates
        """ 
        #self.update_cooling([1,3])
        #print("are we here %d" % self.pid.update(temperature_sensor.read_value(), constant.SET_POINT))
        temp = 2#self.pid.update(temperature_sensor.read_temp(), constant.SET_POINT)
        while True:
            time.sleep(1)
            freq = self.pid.update(temperature_sensor.read_value(), constant.SET_POINT)
            self.update_cooling([1, freq])
            #print(self.update_cooling([1,3]))
            #self.update_cooling([1,3])
