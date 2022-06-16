from webserver.server import Server
import _thread
import utime
# from experiment import Experiment
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.cooling_motor import CoolingMotor
from logger.agent import Logger
from PID.pid import PID
import constant


class thread_args:
    def __init__(self, sensor, lock):
        self.sensor = sensor
        self.lock = lock


def init_sensors(logger):
    period = 5
    sensor_list = []
    sensor_list.append(TemperatureSensor(period, logger))
    sensor_list.append(CoolingMotor(logger))
    # sensor_list.append(FeedingMotor(logger))
    return sensor_list


def publish_manager(sensor_list, server):
    lock = _thread.allocate_lock()
    for sensor in sensor_list:
        args = (thread_args(sensor, lock),)
        _thread.start_new_thread(server.publish_feed, args)
        print("%s done" % sensor.feedname)
        break


def main():
    logger = Logger()
    # server = Server("Redmip", "asd12345")
    server = Server("jxuiphone", "12345678")
    server.create_MQTT_clientID()
    server.connect_MQTT()
    # server.publish_feed(temperature_sensor)
    sensor_list = init_sensors(logger)
    publish_manager(sensor_list, server)

    # sensor_list[1].update_cooling([0, 5000, 1000])
    # sensor_list[2].update_feeding([200000, 500])
    # oled = Oled()
    # oled.write(str(sensor_list[0].read_value()) + "degrees", 1)
    # oled.show()

    # now = time.time()
    # while (time.time - now < 30 ):
    #     sensor_list[0].read_value()
    #     time.sleep(1)
    # logger.end()
    pid = PID(0, 0, 0)
    print("check 2")
    while True:
        # k_p = server.subscribe_feed("P")
        # k_i = server.subscribe_feed("I")
        # k_d = server.subscribe_feed("D")
        k_p = 900
        k_i = 0
        k_d = 0
        pid.reset(k_p, k_i, k_d)
        temperature = sensor_list[0].read_value()
        frequency = pid.update(temperature, constant.SET_POINT)
        sensor_list[1].update_cooling([1, frequency])
        print("The frequency is " + str(frequency))
        print("===========================================")
        utime.sleep_ms(500)
    return 0


if __name__ == "__main__":
    main()
