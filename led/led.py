from machine import Pin
import constant


class LED:

    def __init__(self):
        self.LED = Pin(constant.LED_PIN_NO, Pin.PULL_UP)


    def on(self):
        self.LED.on()
    
    def off(self):
        self.LED.off()