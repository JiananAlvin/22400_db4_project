from webserver.server import Server
import _thread
import time
#from experiment import Experiment
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.cooling_motor import CoolingMotor
from stepper_motor.feeding_motor import FeedingMotor
from oled_screen.oled import Oled
from logger.agent import Logger


class thread_args:
    def __init__(self, sensor, lock):
        self.sensor = sensor
        self.lock = lock


def init_sensors(logger):
    period = 30
    sensor_list = []
    sensor_list.append(TemperatureSensor(30, logger))
    sensor_list.append(CoolingMotor(logger))
    sensor_list.append(FeedingMotor(logger))
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
    #server = Server("Redmip", "asd12345")
    #server = Server("jxuiphone", "12345678")
    #server.create_MQTT_clientID()
    #server.connect_MQTT()
    # server.publish_feed(temperature_sensor)
    sensor_list = init_sensors(logger)
    #publish_manager(sensor_list, server)

    # sensor_list[1].update_cooling([0, 5000, 1000])
    # sensor_list[2].update_feeding([200000, 500])
    # oled = Oled()
    # oled.write(str(sensor_list[0].read_value()) + "degrees", 1)
    # oled.show()

    now = time.time()
    while (time.time - now < 30 ):
        sensor_list[0].read_value()
        time.sleep(1)
    logger.end()

    return 0


if __name__ == "__main__":
    main()
