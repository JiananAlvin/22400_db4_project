from webserver.server import Server

from temprature_sensor.read_temp import Temperature
import utime

def main():

    server = Server("jxuiphone", "12345678")
    server.create_MQTT_clientID()
    server.connect_MQTT()

    readTemp = Temperature()
    temp_sens = readTemp.init_temp_sensor()

    sample_last_ms = 0
    SAMPLE_INTERVAL = 1000

    while (True):
        if utime.ticks_diff(utime.ticks_ms(), sample_last_ms) >= SAMPLE_INTERVAL:
            temp = readTemp.read_temp(temp_sens)
            print('Thermistor temperature: ' + str(temp))
            sample_last_ms = utime.ticks_ms()
            server.publish_feed("temperature", temp)

    
    

 

if __name__=="__main__":
    main()
