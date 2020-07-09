"""
Observations:
1) Firstly, there is a probllem wherein one of the motors randomly starts spinning
   full speed even befor ethe Raspberry Pi is turned on, which is definetely a
   problem, however that might be something to do with my wiring.

2) I tried moving this under load, and it is definetely powerful enough to run the
   car on the ground, which means I will be disposing the useless L293D's and
   using this powerful device instead, and as I anticipated it was the 600Ma
   current max on the L293D which restricted the motor's torque and because this
   has 1400mA more than the L293D this was able to give the motor all the current
   it needed and let it run at capacity or more.
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

print("Turning motors forward.")
""" Left side motors """
GPIO.output(MotorLInput1, GPIO.HIGH)
GPIO.output(MotorLInput2, GPIO.LOW)

""" Right side motors """
GPIO.output(MotorRInput1, GPIO.HIGH)
GPIO.output(MotorRInput2, GPIO.LOW)

time.sleep(3)

print("Turning motors backward.")
""" Left side motors """
GPIO.output(MotorLInput1, GPIO.LOW)
GPIO.output(MotorLInput2, GPIO.HIGH)

""" Right side motors """
GPIO.output(MotorRInput1, GPIO.LOW)
GPIO.output(MotorRInput2, GPIO.HIGH)

time.sleep(3)

print("Trying pulse width modulation")
GPIO.output(MotorLInput1, GPIO.LOW)
GPIO.output(MotorLInput2, GPIO.LOW)
GPIO.output(MotorRInput1, GPIO.LOW)
GPIO.output(MotorRInput2, GPIO.LOW)

LPWM = GPIO.PWM(MotorLInput2, 100)
LPWM.start(70)

RPWM = GPIO.PWM(MotorRInput2, 100)
RPWM.start(70)

time.sleep(4)

LPWM.stop()
RPWM.stop()

print("Turning motors off.")
GPIO.output(MotorLInput1, GPIO.LOW)
GPIO.output(MotorLInput2, GPIO.LOW)
GPIO.output(MotorRInput1, GPIO.LOW)
GPIO.output(MotorRInput2, GPIO.LOW)

time.sleep(2)

GPIO.cleanup()
