import _thread
import network
import time
from umqtt.robust import MQTTClient
import os
import sys
import constant

class Server:
    WIFI_SSID = None
    WIFI_PASSWORD = None
    mqtt_client_id = None
    mqtt_client = None
    ADAFRUIT_IO_URL = 'io.adafruit.com'
    ADAFRUIT_IO_USERNAME = constant.ADAFRUIT_IO_USERNAME
    ADAFRUIT_IO_KEY = constant.ADAFRUIT_IO_KEY

    def __init__(self):
        self.WIFI_SSID = constant.WIFI_SSID
        self.WIFI_PASSWORD = constant.WIFI_PASSWORD

        # turn off the WiFi Access Point
        ap_if = network.WLAN(network.AP_IF)
        ap_if.active(False)

        # connect the device to the WiFi network
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(self.WIFI_SSID,self.WIFI_PASSWORD)

        # wait until the device is connected to the WiFi network
        MAX_ATTEMPTS = 2**32-1
        attempt_count = 0
        while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
            attempt_count += 1
            time.sleep(1)
            print("Trying to connect %d" % attempt_count)

        if attempt_count == MAX_ATTEMPTS:
            print('could not connect to the WiFi network')
            sys.exit()
        print("Connected")

    # create a random MQTT clientID 
    def create_MQTT_clientID(self):
        random_num = int.from_bytes(os.urandom(3), 'little')
        self.mqtt_client_id = bytes('client_' + str(random_num), 'utf-8')

    # connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
    # 
    # To use a secure connection (encrypted) with TLS: 
    #   set MQTTClient initializer parameter to "ssl=True"
    #   Caveat: a secure connection uses about 9k bytes of the heap
    #         (about 1/4 of the micropython heap on the ESP8266 platform)
    def connect_MQTT(self):
        self.mqtt_client = MQTTClient(client_id=self.mqtt_client_id,
                                      server=self.ADAFRUIT_IO_URL,
                                      user=self.ADAFRUIT_IO_USERNAME,
                                      password=self.ADAFRUIT_IO_KEY,
                                      ssl=False)
        try:
            self.mqtt_client.connect()
            print("Connected to MQTT server")
        except Exception as e:
            print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
            sys.exit()

    # publish feed statistics to Adafruit IO using MQTT
    #
    # format of feed name:  
    #   "ADAFRUIT_USERNAME/feeds/feed_name"
    def publish_feed(self, sensor, lock):
        print(sensor)
        print("publishing %s" % sensor.feedname)
        mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(self.ADAFRUIT_IO_USERNAME, sensor.feedname), 'utf-8')
        while True:
            lock.acquire()
            feed_data = sensor.read_value()
            #print("value %s" % str(feed_data))

            try:
                self.mqtt_client.publish(mqtt_feedname, bytes(str(feed_data), 'utf-8'), qos=0)
                lock.release()
                time.sleep(10)
            except KeyboardInterrupt:
                print('Ctrl-C pressed...exiting')
                self.mqtt_client.disconnect()
                sys.exit()

    def cb(self, topic, msg):
        print('Received data: Topic = {}, Msg = {}'.format(topic, msg))

    def subscribe_feed(self, args):
        """ Subscribes to a feed to receive data from Adafruit IO broker:
            args[0] = feedname
        """
        feedname = args[0]
        mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(self.ADAFRUIT_IO_USERNAME, feedname), 'utf-8')
        self.mqtt_client.set_callback(Server.cb)
        self.mqtt_client.subscribe(mqtt_feedname)
