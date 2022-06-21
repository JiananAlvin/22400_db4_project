import machine
import constant
from logger.agent import Logger
from led.led import LED
import time

class Light_Sensor:

    feedname = constant.FEEDNAME_LIGHTSENSOR

    def __init__(self, logger):
        self.adc = machine.ADC(machine.Pin(constant.LIGHT_SENSOR_PIN_NO))
        self.logger = logger
        self.LED = LED()
        self.LED.on()
        self.adc.atten(machine.ADC.ATTN_11DB)
        self.adc.width(machine.ADC.WIDTH_10BIT)  # was 10


        


    def read_value(self):
        """ Returns lightsensor reading"""

        light_intensity = self.adc.read()
        self.logger.log("Light intensity: %d" % light_intensity, self.feedname)
        print("\nLight intensity = %d\n\n" % light_intensity)
        
        return light_intensity

    def adjuster(self):
        light_intensity = 0
        return light_intensity