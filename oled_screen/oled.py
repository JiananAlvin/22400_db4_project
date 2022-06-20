from machine import I2C, Pin
import constant
from . import ssd1306


class Oled:

    def __init__(self):
        # Define I2C
        i2c = I2C(scl=Pin(constant.OLED_SCL_NO), sda=Pin(constant.OLED_SDA_NO), freq=100000)
#        # Define olef
        self.oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        self.oled.fill(0)
        self.show()

    def write(self, text, line):
        """Writes to text in the indicated line
            line -> [0,1,2,3]
        """

        self.oled.text("Team 09", 2, 0)
        self.oled.text(text, 0, (line+1) * 8)

    def show(self):
        self.oled.show()
