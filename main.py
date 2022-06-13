from webserver.server import Server
import time
from temperature_sensor.read_temp import TemperatureSensor

def main():

    server = Server("jxuiphone", "12345678")
    server.create_MQTT_clientID()
    server.connect_MQTT()

    temperature_sensor = TemperatureSensor(5)

    while (True):
        server.publish_feed(temperature_sensor)
        time.sleep(PUBLISH_PERIOD_IN_SEC)
    

if __name__=="__main__":
    main()
