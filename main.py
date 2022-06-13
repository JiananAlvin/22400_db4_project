from webserver.server import Server
import _thread
import time
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor.stepper_motor import StepperMotor

def init_sensors():
    sensor_list = []
    sensor_list.append(TemperatureSensor(5))
    # sensor_list.append(StepperMotor("cooling"))
    # sensor_list.append(StepperMotor("feeding"))
    return sensor_list


def thread_manager(sensor_list, server):
    for sensor in sensor_list:
        server.publish_feed(sensor)
        # _thread.start_new_thread(server.publish_feed, [sensor])


def main():

    server = Server("Redmip", "asd12345")
    server.create_MQTT_clientID()
    server.connect_MQTT()

    #server.publish_feed(temperature_sensor)
    sensor_list = init_sensors()
    thread_manager(sensor_list, server)
    # sensor_list[1].update([800,400])
    # sensor_list[2].update([200000, 500])
    
    time.sleep(20)


    return 0

if __name__=="__main__":
    main()
