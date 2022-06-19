from webserver.server import Server
import _thread
import utime
# from experiment import Experiment
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.cooling_motor import CoolingMotor
from stepper_motor.feeding_motor import FeedingMotor
from logger.agent import Logger
from oled_screen.oled import Oled
from PID.pid import PID
from led.light_sensor import Light_Sensor
import constant





class Thread_manager:
    def __init__(self):
        self.thread_pool = []
        self.lock = _thread.allocate_lock()

    def run(self,function, args):
        try:
            print("starting thread %s with args %s " % (function.__name__, args))
            args = args + (self.lock,)
            self.thread_pool.append(_thread.start_new_thread(function, args))
        except:
            print("Exception in thread %s" % function.__name__)

    def kill(self):
        for thread in self.thread_pool:
            thread.exit()






def init_sensors(logger, thread_manager):
    """ """
    period = 5
    sensor_list = []

    temperature_sensor = TemperatureSensor(period, logger, thread_manager, None)
   # TODO uncomment after oled screen is fixed and delete line above
   # temperature_sensor = TemperatureSensor(period, logger, thread_manager, Oled())
    light_sensor = Light_Sensor(logger)
    sensor_list.append(light_sensor)
    sensor_list.append(temperature_sensor)
    sensor_list.append(CoolingMotor(logger, thread_manager, temperature_sensor))

    sensor_list.append(FeedingMotor(logger, thread_manager, light_sensor))
        
    print("Sensors inited")
    return sensor_list


def publish_manager(sensor_list, thread_manager):
    server = Server()
    server.create_MQTT_clientID()
    server.connect_MQTT()
    print(sensor_list)
    for sensor in sensor_list:
        args = (sensor,)
        thread_manager.run(server.publish_feed, args)
        print("Start publishing thread for %s" % sensor.feedname)
        
 
def subcriber():
    """ Call this function on main to run the adafruit PID experiment """
    while True:
        k_p = server.subscribe_feed("P")
        k_i = server.subscribe_feed("I")
        k_d = server.subscribe_feed("D")
        # k_p = 900
        # k_i = 0
        # k_d = 0
        pid.reset(k_p, k_i, k_d)
        temperature = sensor_list[0].read_value()
        frequency = pid.update(temperature, constant.SET_POINT)
        sensor_list[1].update_cooling([1, frequency])
        print("The frequency is " + str(frequency))
        print("===========================================")


def main():
    thread_manager = Thread_manager()
    logger = Logger()
    print("Logger started")
    sensor_list = init_sensors(logger, thread_manager)
    publish_manager(sensor_list[:-2], thread_manager) # no need to publish feeding and cooling motor for now


    while True:
        pass
    thread_manager.kill()
    return 0


if __name__ == "__main__":
    main()
