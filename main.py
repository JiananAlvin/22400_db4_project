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
import time
import machine




class Thread_manager:
    def __init__(self):
        self.thread_pool = []
        self.lock = _thread.allocate_lock()
        self.button = machine.Pin(constant.BUTTON_PIN_NO, machine.Pin.IN, machine.Pin.PULL_UP)



    def run(self,function, args):
        try:
            args = args + (self.lock,)
            tid = _thread.start_new_thread(function, args)
            #tid =  _thread.get_ident()
            print("starting thread %s with args %s and TID: %s " % (function.__name__, args, tid))

            self.thread_pool.append(tid)
        except:
            print("Exception in thread %s" % function.__name__)

    def kill(self):
        print(self.thread_pool)
        for thread in self.thread_pool[1:]:
            print("Ending thread: %s" % thread)
            thread.exit()

    def manage_threads(self):
        print("Managing threads")
        while self.button.value():
            pass
        print("Button is pressed RIP threads")
        self.kill()




sensor_dict = {}

def init_sensors(logger, thread_manager):
    """ """
    period = 5
    sensor_list = []
    
    temperature_sensor = TemperatureSensor(period, logger, thread_manager, Oled())
    light_sensor = Light_Sensor(logger)
    cooling_motor = CoolingMotor(logger, thread_manager, temperature_sensor)
    feeding_motor = FeedingMotor(logger, thread_manager, light_sensor)
    sensor_list.append(light_sensor)
    sensor_list.append(temperature_sensor)
    sensor_list.append(cooling_motor)
    sensor_list.append(feeding_motor)

    for sensor in sensor_list:
            sensor_dict[sensor.feedname] = sensor

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
        sensor_dict[constant.FEEDNAME_COOL_MOTOR].update_cooling([1, frequency])

        print("The frequency is %d" + frequency)
        print("===========================================")




def PID_experiment(logger, cooling_motor):
    P = 0
    I = 0
    D = 0
    P_range = [300, 306.25, 303.25]
    I_range = [100, 50]
    D_range = [100, 106.25, 103.2]

    for P in P_range:
        print("Experiment for P: %d started" % P)
        i = P
        cooling_motor.pid = PID(P, I, D)

        for name in logger.logfile_names:
            print("here name:%s" % name)
            text = "Updated PID\nP: %d  I: %d  D:  %d"
            logger.log(text % (P,I,D), name)
        input("Press somewhere to start the next experiment")
    P = 303.25
    for I in I_range:
        print("Experiment for I: %d started" % I)
        i = I
        cooling_motor.pid = PID(P, I, D)

        for name in logger.logfile_names:
            print("here name:%s" % name)
            text = "Updated PID\nP: %d  I: %d  D:  %d"
            logger.log(text % (P,I,D), name)
        input("Press somewhere to start the next experiment")
    I = 50
    for D in D_range:
        print("Experiment for D: %d started" % D)
        i = D
        cooling_motor.pid = PID(P, I, D)

        for name in logger.logfile_names:
            print("here name:%s" % name)
            text = "Updated PID\nP: %d  I: %d  D:  %d"
            logger.log(text % (P,I,D), name)
        input("Press somewhere to start the next experiment")
    print("D is %d" % i)
    return 0


def main():
    thread_manager = Thread_manager()
    logger = Logger()
    print("Logger started")
    sensor_list = init_sensors(logger, thread_manager)
    publish_manager(sensor_list[:-2], thread_manager) # no need to publish feeding and cooling motor for now
    #thread_manager.manage_threads()
    PID_experiment(logger, sensor_dict[constant.FEEDNAME_COOL_MOTOR])
    while True:
        # time.sleep(2)
        # sensor_dict[constant.FEEDNAME_LIGHTSENSOR].read_value()
        pass

    return 0


if __name__ == "__main__":
    main()
