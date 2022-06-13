import tcs34725




class rgbsensor:
    
    def __init__(self):
        # Define rgb sensor
        self.sensor = tcs34725.TCS34725(i2c)
        #sensor.integration_time(10) #value between 2.4 and 614.4.
        #sensor.gain(16) #must be a value of 1, 4, 16, 60

    def read_value(self):
        return self.sensor.read(True)
        
    def color_rgb_bytes(self):
        """Read the RGB color detected by the sensor.  Returns a 3-tuple of
        red, green, blue component values as bytes (0-255).
        NOTE: These values are normalized against 'clear', remove the division
        by 'clear' if you need the raw values.
        """
        r, g, b, clear = self.read_value()
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

