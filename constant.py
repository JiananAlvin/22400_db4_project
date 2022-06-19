# pins for the cooling pump
STEPPER_MOTOR_COOL_DIR_PIN_NO = 27
STEPPER_MOTOR_COOL_STEP_PIN_NO = 33
STEPPER_MOTOR_COOL_UPDATE_PERIOD = 5

# pins for the food dosing pump
STEPPER_MOTOR_FEED_DIR_PIN_NO = 13
STEPPER_MOTOR_FEED_STEP_PIN_NO = 12
STEPPER_MOTOR_FEED_UPDATE_PERIOD = 10*60

# duty cycle for stepper motor int: [0, 1023]
DUTY_CYCLE = int(0.48 * 1023)

# pin for the temperature sensor
TENP_SENS_ADC_PIN_NO = 32

# the desired temperature
SET_POINT = 20

# pins for the OLED screen
OLED_SCL_NO = 22
OLED_SDA_NO = 23

# pin for the LED
LED_PIN_NO = 21 # TODO change to the correct one 
LIGHT_SENSOR_PIN_NO = 39

#Formula contants TODO update
# FLORA
NUMBER_OF_MUSSELS = 5
EXP1 = 1
EXP2 = 1
CON1 = 1
CON2 = 1

# feednames
FEEDNAME_COOL_MOTOR = "Cooling"
FEEDNAME_FOOD_MOTOR = "Feeding"
FEEDNAME_TEMP = "Temperature"
FEEDNAME_LIGHTSENSOR = "Light_Sensor"


# PID
P = 1417.2
I = 566.4
D = 114.2



# AdafruitConstants

WIFI_SSID = "FTTH_AI6519"
WIFI_PASSWORD  = "plyems8drabU"
ADAFRUIT_IO_USERNAME = 's194729'
ADAFRUIT_IO_KEY = 'aio_SImY77ltZfreTukLs1odFTwIvOHb'

