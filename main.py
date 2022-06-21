from webserver.server import Server
# from experiment import Experiment
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.cooling_motor import CoolingMotor
from logger.agent import Logger
from PID.pid import PID
import constant
from machine import Pin, PWM
import time


def main():

    led = PWM(Pin(21))
    led.duty(120)
    adc = ADC(Pin(39))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)

    logger = Logger()
    server = Server("jxuiphone", "12345678")
    server.create_MQTT_clientID()
    server.connect_MQTT()

    # temperature_sensor = TemperatureSensor(logger)

    i = 0
    while True:
        light_intensity_record = []
        ADC_data = []
        for j in range(10):
            time.sleep(2)
            ADC_data.append(adc.read())
            # server.mqtt_client.publish("s204698/feeds/light intensity", bytes(str(ADC_data), 'utf-8'), qos=0)
        ADC_value = round(sum(ADC_data)/10, 2)
        light_intensity_record.append(ADC_value)
        # file.write("{}".format(180 * i) + "\t" + "{}".format(ADC) + "\n")

        # Initialize sensors & PID controller
        # Read and publish temperature
        # temperature = temperature_sensor.read_value()
        # server.publish_feed(temperature_sensor)
        cooling_motor = CoolingMotor(logger)
        # pid = PID(303.7, 50, 102.2)
        # frequency = pid.update(temperature, constant.SET_POINT)
        cooling_motor.update_cooling([1, 3300])
        print(ADC_data)
        print("=========================")

        i += 1


if __name__ == "__main__":
    main()
