from webserver.server import Server
import _thread
import utime
# from experiment import Experiment
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.cooling_motor import CoolingMotor
from logger.agent import Logger
from PID.pid import PID
import constant


def main():
    logger = Logger()
    # server = Server("Redmip", "asd12345")
    server = Server("jxuiphone", "12345678")
    # server = Server("a1c3", "nmro9920")
    server.create_MQTT_clientID()
    server.connect_MQTT()

    # Initialize sensors & PID controller
    temperature_sensor = TemperatureSensor(logger)
    cooling_motor = CoolingMotor(logger)
    pid = PID(0, 0, 0)

    while True:
        server.subscribe_feed("p")
        k_p = server.fetch_data("p")
        server.subscribe_feed("i")
        k_i = server.fetch_data("i")
        server.subscribe_feed("d")
        k_d = server.fetch_data("d")
        print('kp = {}, ki = {}, kd = {}'.format(k_p, k_i, k_d))
        pid.reset(k_p, k_i, k_d)

        # Read and publish temperature
        temperature = temperature_sensor.read_value()
        server.publish_feed(temperature_sensor)

        pid.ki_enable(True)
        frequency = pid.update(temperature, constant.SET_POINT)

        # Set and publish frequency
        cooling_motor.update_cooling([1, frequency])
        # server.publish_feed(cooling_motor)

        print("The frequency is " + str(frequency))
        print("================================")
        utime.sleep_ms(5000)


if __name__ == "__main__":
    main()
