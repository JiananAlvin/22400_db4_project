import ssd1306
import tcs34725
import time
from machine import I2C, Pin

# Define I2C
i2c = I2C(scl=Pin(22), sda=Pin(23), freq=100000)

# Define olef
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)

# Define rgb sensor
sensor = tcs34725.TCS34725(i2c)
#sensor.integration_time(10) #value between 2.4 and 614.4.
#sensor.gain(16) #must be a value of 1, 4, 16, 60

def color_rgb_bytes(color_raw):
    """Read the RGB color detected by the sensor.  Returns a 3-tuple of
    red, green, blue component values as bytes (0-255).
    NOTE: These values are normalized against 'clear', remove the division
    by 'clear' if you need the raw values.
    """
    r, g, b, clear = color_raw
    # Avoid divide by zero errors ... if clear = 0 return black
    if clear == 0:
        return (0, 0, 0)
    red   = int(pow((int((r/clear) * 256) / 255), 2.5) * 255)
    green = int(pow((int((g/clear) * 256) / 255), 2.5) * 255)
    blue  = int(pow((int((b/clear) * 256) / 255), 2.5) * 255)
    # Handle possible 8-bit overflow
    if red > 255:
        red = 255
    if green > 255:
        green = 255
    if blue > 255:
        blue = 255
    return (red, green, blue)

while True:
    # Read color sensor
    r,g,b = color_rgb_bytes(sensor.read(True))

    # Show results on OLED
    oled.fill(0)
    oled.text('R: {}'.format(r), 0, 8)
    oled.text('G: {}'.format(g), 0, 16)
    oled.text('B: {}'.format(b), 0, 24)
    oled.show()

    # Print results
    answer = '>r:{} g:{} b:{}<'.format(r, g, b)
    print(answer, end='\n')

    # Wait 1 second before repeating
    time.sleep(1)
