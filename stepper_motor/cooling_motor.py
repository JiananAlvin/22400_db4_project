from machine import Pin, PWM
import constant
from PID.pid import PID
from temperature_sensor.read_temp import TemperatureSensor
import time

class CoolingMotor:
    freq = 100
    duty = 1
    logger = None
    feedname = constant.FEEDNAME_COOL_MOTOR
    pid = PID(constant.P,constant.I,constant.D)




    def __init__(self, logger, thread_manager, temperature_sensor):
        print("Cooling motor started")

        self.pin_step = PWM(Pin(constant.STEPPER_MOTOR_COOL_STEP_PIN_NO))  # Step
        self.pin_dir = Pin(constant.STEPPER_MOTOR_COOL_DIR_PIN_NO, Pin.OUT)  # Direction
        self.pin_dir(0)
        self.pin_step.freq(1)
        self.pin_step.duty(0)
        self.logger = logger
        thread_manager.run(self.PIDupdater, (constant.STEPPER_MOTOR_COOL_UPDATE_PERIOD ,temperature_sensor))

    # overwrite server method
    def read_value(self):
        """ Returns freq"""
        return self.freq

    def update_cooling(self):
        """ Updates the feeding motor with given args:
            args[0] = direction
            args[1] = freq
        """
        # PWM for the cooling pump
        self.direction = 1
        self.pin_dir(self.direction)
        if self.freq < 1:
            self.freq = 1 
        if self.freq > 15000:
            self.freq  = 15000
        self.pin_step.freq(self.freq)  # Frequency is the number of times per second that we repeat the on and off cycle -> rotating speed
        self.pin_step.duty(constant.DUTY_CYCLE)  # Duty cycle refers the amount of time the pulse is ON -> voltage
        self.logger.log("Updated cooling <%d,%d>" % (self.direction, self.freq), self.feedname)

    def PIDupdater(self, period, temperature_sensor, lock):
        """
        >>> period: Time between updates
        """ 
        while True:
            time.sleep(period)
            self.freq = self.pid.update(temperature_sensor.read_value(log1=True), constant.SET_POINT)
            print("Updating freq on coooling motor: %f" % self.freq)
            self.freq = 8000
            self.update_cooling()
