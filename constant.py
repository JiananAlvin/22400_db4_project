# pins for the cooling pump
STEPPER_MOTOR_COOL_DIR_PIN_NO = 27
STEPPER_MOTOR_COOL_STEP_PIN_NO = 33

# pins for the food dosing pump
STEPPER_MOTOR_FEED_DIR_PIN_NO = 13
STEPPER_MOTOR_FEED_STEP_PIN_NO = 12

# duty cycle for stepper motor int: [0, 1023]
DUTY_CYCLE = int(0.48 * 1023)

# pin for the temperature sensor
TENP_SENS_ADC_PIN_NO = 32

# the desired temperature
SET_POINT = 20

# pins for the OLED screen
OLED_SCL_NO = 22
OLED_SDA_NO = 23

# feednames
FEEDNAME_COOL_MOTOR = "Cooling"
FEEDNAME_FOOD_MOTOR = "Feeding"
