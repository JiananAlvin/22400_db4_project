from webserver.server import Server
import _thread
import time
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.stepper_motor import StepperMotor

def init_sensors():
    period = 30
    sensor_list = []
    sensor_list.append(TemperatureSensor(30))
    #sensor_list.append(StepperMotor("cooling", period))
    #sensor_list.append(StepperMotor("feeding", period))
    return sensor_list


def thread_manager(sensor_list, server):
    lock = _thread.allocate_lock()
    publish = publish_feed
    for sensor in sensor_list:
        print(sensor.feedname)
        #server.publish_feed(sensor)
        _thread.start_new_thread(publish,(sensor,lock))
        print("%s done" % sensor.feedname)


def main():
    server = Server("Redmip", "asd12345")
    server.create_MQTT_clientID()
    server.connect_MQTT()
    #server.publish_feed(temperature_sensor)
    sensor_list = init_sensors()
    thread_manager(sensor_list, server)
    # sensor_list[1].update([800,400])
    # sensor_list[2].update([200000, 500])
    
    while True:
        0

    return 0

if __name__=="__main__":
    main()
