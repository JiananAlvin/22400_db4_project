from webserver.server import Server
from PID.pid import PID
import _thread
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.cooling_motor import CoolingMotor
from logger.agent import Logger


class thread_args:
    def __init__(self, sensor, lock):
        self.sensor = sensor
        self.lock = lock


def init_sensors(logger):
    period = 30
    sensor_list = []
    sensor_list.append(TemperatureSensor(period, logger))
    sensor_list.append(CoolingMotor(logger))
    return sensor_list


# Three threads
# [1] publish temperature every 30 seconds
# [2] publish frequency of colling motor every 30 seconds
# [3] tune pid every 500 microseconds
def publish_manager(sensor_list, server, lock):
    for sensor in sensor_list:
        args = (thread_args(sensor, lock),)
        _thread.start_new_thread(server.publish_feed, args)
        print("%s done" % sensor.feedname)
        break


server = Server("jxuiphone", "12345678")
server.create_MQTT_clientID()
server.connect_MQTT()
logger = Logger()
sensor_list = init_sensors(logger)
lock = _thread.allocate_lock()
publish_manager(sensor_list, server, lock)
pid = PID(0, 0, 0)
_thread.start_new_thread(pid.pid_tuning, (lock, server, logger))
