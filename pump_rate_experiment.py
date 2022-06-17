
from machine import Pin, PWM
import utime
import constant

# pin_feed_step = Pin(constant.STEPPER_MOTOR_FEED_STEP_PIN_NO, Pin.OUT)
# pin_feed_dir = Pin(constant.STEPPER_MOTOR_FEED_DIR_PIN_NO, Pin.OUT)

pin_feed_step = Pin(constant.STEPPER_MOTOR_COOL_STEP_PIN_NO, Pin.OUT)
pin_feed_dir = Pin(constant.STEPPER_MOTOR_COOL_DIR_PIN_NO, Pin.OUT)


pin_feed_dir(1)
pin_feed_step.value(0)

# bit-banging for the food dosing pump
while True:
    pin_feed_step.value(1)
    utime.sleep_us(25)
    pin_feed_step.value(0)
    utime.sleep_us(25)
from machine import Pin, PWM
import utime
import constant

# pin_feed_step = Pin(constant.STEPPER_MOTOR_FEED_STEP_PIN_NO, Pin.OUT)
# pin_feed_dir = Pin(constant.STEPPER_MOTOR_FEED_DIR_PIN_NO, Pin.OUT)

pin_feed_step = Pin(constant.STEPPER_MOTOR_COOL_STEP_PIN_NO, Pin.OUT)
pin_feed_dir = Pin(constant.STEPPER_MOTOR_COOL_DIR_PIN_NO, Pin.OUT)


pin_feed_dir(1)
pin_feed_step.value(0)

# bit-banging for the food dosing pump
while True:
    pin_feed_step.value(1)
    utime.sleep_us(10)
    pin_feed_step.value(0)
    utime.sleep_us(10)