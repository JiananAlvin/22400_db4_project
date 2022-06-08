import _thread
import network
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys

class Server:
    WIFI_SSID = None
    WIFI_PASSWORD = None
    mqtt_client_id = None
    ADAFRUIT_IO_URL = b'io.adafruit.com' 
    ADAFRUIT_USERNAME = b's194729'
    ADAFRUIT_IO_KEY = b'aio_SImY77ltZfreTukLs1odFTwIvOHb'


    def __init__(self, WIFI_SSID, WIFI_PASSWORD):
        self.WIFI_SSID = WIFI_SSID  
        self.WIFI_PASSWORD = WIFI_PASSWORD
        
        # turn off the WiFi Access Point
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        # connect the device to the WiFi network
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)

        # wait until the device is connected to the WiFi network
        MAX_ATTEMPTS = 20
        attempt_count = 0
        while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
            attempt_count += 1
            time.sleep(1)

        if attempt_count == MAX_ATTEMPTS:
            print('could not connect to the WiFi network')
            sys.exit()


    # create a random MQTT clientID 
    def create_MQTT_clientID(self):
        random_num = int.from_bytes(os.urandom(3), 'little')
        self.mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

    # connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
    # 
    # To use a secure connection (encrypted) with TLS: 
    #   set MQTTClient initializer parameter to "ssl=True"
    #   Caveat: a secure connection uses about 9k bytes of the heap
    #         (about 1/4 of the micropython heap on the ESP8266 platform)
    def connect_MQTT(self):

        client = MQTTClient(self.mqtt_client_id, 
                            self.ADAFRUIT_IO_URL, 
                            self.ADAFRUIT_USERNAME, 
                            self.ADAFRUIT_IO_KEY,
                            ssl=False)
        try:            
            client.connect()
        except Exception as e:
            print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
            sys.exit()

    # publish feed statistics to Adafruit IO using MQTT
    #
    # format of feed name:  
    #   "ADAFRUIT_USERNAME/feeds/feed_name"
    def publish_feed(self, feed_name, period):
        ADAFRUIT_IO_FEEDNAME = feed_name.encode()
        mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(self.ADAFRUIT_USERNAME, ADAFRUIT_IO_FEEDNAME), 'utf-8')
        PUBLISH_PERIOD_IN_SEC = period 
        while True:
            try:
                temp = gc.mem_free()
                client.publish(mqtt_feedname, bytes(str(free_heap_in_bytes), 'utf-8'), qos=0)  
                time.sleep(PUBLISH_PERIOD_IN_SEC)
            except KeyboardInterrupt:
                print('Ctrl-C pressed...exiting')
                client.disconnect()
                sys.exit()