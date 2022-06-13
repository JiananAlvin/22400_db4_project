from machine import Pin, PWM
import time
import utime

pinStep1 = PWM(Pin(33))  # Step
pinDir1 = Pin(27, Pin.OUT)  # Direction
pinStep2 = Pin(12, Pin.OUT)
pinDir2 = Pin(13, Pin.OUT)

pinDir1(1)  # 0: counterclockwise, 1: clockwise
pinDir2(0)

# Initialize two stepper motors
pinStep1.freq(0)
pinStep1.duty(0)
pinStep2.value(0)
time.sleep(5)

# PWM for the cooling pump
pinStep1.freq(800)  # Frequency is the number of times per second that we repeat the on and off cycle -> rotating speed
pinStep1.duty(400)  # Duty cycle refers the amount of time the pulse is ON -> voltage

# bit-banging for the food dosing pump
for x in range(0, 200000):
    pinStep2.value(1)
    utime.sleep_us(500)
    pinStep2.value(0)
    utime.sleep_us(500)