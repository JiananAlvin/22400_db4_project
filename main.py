from webserver.server import Server
import _thread
import time
from temperature_sensor.read_temp import TemperatureSensor
from stepper_motor import StepperMotor

def init_sensors():
    sensor_list = []
    sensor_list.append(TemperatureSensor(5), StepperMotor("cooling"), StepperMotor("feeding"))
    return sensor_list


def thread_manager(sensor_list):
    for sensor in sensor_list:
        _thread.start_new_thread(server.publish_feed, [sensor])


def main():

    server = Server("jxuiphone", "12345678")
    server.create_MQTT_clientID()
    server.connect_MQTT()

    temperature_sensor = TemperatureSensor(5)

    #server.publish_feed(temperature_sensor)
    thread_manager(init_sensors())
    time.sleep(20)
    return 0

if __name__=="__main__":
    main()
