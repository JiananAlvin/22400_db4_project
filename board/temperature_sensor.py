from machine import Pin
from machine import ADC
from time import sleep

def init_temp_sensor(pin_nr):
    thermistor_adc = ADC(Pin(pin_nr))
    thermistor_adc.atten(ADC.ATTN_11DB)
    thermistor_adc.width(ADC.WIDTH_10BIT)
    while True:
        thermistor_value = thermistor_adc.read()
        print(thermistor_value)
        sleep(0.5)



def main():
    init_temp_sensor(32)
    return 0

main()




