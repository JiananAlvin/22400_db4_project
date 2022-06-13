from webserver.server import Server
import time
from temperature_sensor.read_temp import TemperatureSensor

def main():

    server = Server("jxuiphone", "12345678")
    server.create_MQTT_clientID()
    server.connect_MQTT()

    temperature_sensor = TemperatureSensor()
    temp_sens = temperature_sensor.init_temp_sensor()

    PUBLISH_PERIOD_IN_SEC = 5

    while (True):
        temp = temperature_sensor.read_temp(temp_sens)
        server.publish_feed("temperature", temp)
        time.sleep(PUBLISH_PERIOD_IN_SEC)
    

if __name__=="__main__":
    main()
