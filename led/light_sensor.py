import machine
import constant
from logger.agent import Logger
from led.led import LED

class Light_Sensor:

    feedname = constant.FEEDNAME_LIGHTSENSOR

    def __init__(self, logger):
        self.adc = machine.ADC(machine.Pin(constant.LIGHT_SENSOR_PIN_NO))
        self.logger = logger
        self.LED = LED()
        self.LED.on()
        


    def read_value(self):
        """ Returns lightsensor reading"""
        light_intensity = self.adc.read()
        self.logger.log("Light intensity: %f" % light_intensity, self.feedname)
        return light_intensity