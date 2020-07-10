"""
This file is just checking out all the things you can do with the L298N
motor driver
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

MotorLInput1 = 6
MotorLInput2 = 13

MotorRInput1 = 19
MotorRInput2 = 26

GPIO.setup(MotorLInput1, GPIO.OUT)
GPIO.setup(MotorLInput2, GPIO.OUT)

GPIO.setup(MotorRInput1, GPIO.OUT)
GPIO.setup(MotorRInput2, GPIO.OUT)

LPWM = GPIO.PWM(MotorLInput1, 100)
LPWM.start(50)

RPWM = GPIO.PWM(MotorRInput1, 100)
RPWM.start(50)

time.sleep(5)

LPWM.stop()
RPWM.stop()

GPIO.cleanup()
