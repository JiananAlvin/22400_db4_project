from webserver.server import Server
from PID.pid import PID
import _thread
import utime
# from experiment import Experiment
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.cooling_motor import CoolingMotor
from logger.agent import Logger
import constant


class thread_args:
    def __init__(self, sensor, lock):
        self.sensor = sensor
        self.lock = lock


def init_sensors(logger):
    period = 30
    sensor_list = []
    sensor_list.append(TemperatureSensor(period, logger))
    sensor_list.append(CoolingMotor(logger))
    sensor_list.append(PID(0, 0, 0))
    return sensor_list


# Three threads
# [1] publish temperature every 30 seconds
# [2] publish frequency of colling motor every 30 seconds
# [3] tune pid every 500 microseconds
def publish_manager(sensor_list, server):
    lock = _thread.allocate_lock()
    for sensor in sensor_list:
        args = (thread_args(sensor, lock),)
        _thread.start_new_thread(server.publish_feed, args)
        print("%s done" % sensor.feedname)
        break



