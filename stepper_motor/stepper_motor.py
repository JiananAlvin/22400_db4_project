
from machine import Pin, PWM

pin = PWM(Pin(33))  # Step
pinDir = Pin(27, Pin.OUT)  # Direction

pinDir(0)  # 0: counterclockwise, 1: clockwise

pin.freq(400)  # Frequency is the number of times per second that we repeat the on and off cycle -> rotating speed
pin.duty(100)  # Duty cycle refers the amount of time the pulse is ON -> voltage

