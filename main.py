from webserver.server import Server
import _thread
import time
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.cooling_motor import CoolingMotor


class thread_args:
    def __init__(self, sensor, lock):
        self.sensor = sensor
        self.lock = lock


def init_sensors():
    period = 30
    sensor_list = []
    sensor_list.append(TemperatureSensor(30))
    sensor_list.append(CoolingMotor(period))
    # sensor_list.append(FeedingMotor(period))
    return sensor_list


def thread_manager(sensor_list, server):
    lock = _thread.allocate_lock()
    for sensor in sensor_list:
        args = (thread_args(sensor, lock),)
        # print(args)
        # print(type(args))
        _thread.start_new_thread(server.publish_feed, args)
        print("%s done" % sensor.feedname)


def main():
    # server = Server("Redmip", "asd12345")
    server = Server("jxuiphone", "12345678")
    server.create_MQTT_clientID()
    server.connect_MQTT()
    # server.publish_feed(temperature_sensor)
    sensor_list = init_sensors()
    thread_manager(sensor_list, server)
    sensor_list[1].update_cooling([0, 5000, 1000])
    # sensor_list[2].update([0, 200000, 500])
    
    while True:
        0

    return 0


if __name__=="__main__":
    main()
