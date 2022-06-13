from webserver.server import Server
import _thread
import time
from temperature_sensor.read_temp import TemperatureSensor

def init_sensors():
    return 0


def main():

    server = Server("jxuiphone", "12345678")
    server.create_MQTT_clientID()
    server.connect_MQTT()

    temperature_sensor = TemperatureSensor(5)

    #server.publish_feed(temperature_sensor)
    _thread.start_new_thread(server.publish_feed(), temperature_sensor)
    print("Thread ok")
    return 0

if __name__=="__main__":
    main()
