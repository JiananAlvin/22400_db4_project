import machine
import constant


class LED:

    def __init__(self):
        self.LED = machine.Pin(constant.LED_PIN_NO, machine.Pin.PULL_UP)
        self.LED.on()
        #self.LED.duty(400)


    def on(self):
        self.LED.on()
    
    def off(self):
        self.LED.off()