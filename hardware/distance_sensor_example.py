import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIGGER = 4
ECHO = 18

GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIGGER, True)
time.sleep(0.00001)
GPIO.output(TRIGGER, False)

start = time.time()

while GPIO.input(ECHO) == False:
    start = time.time()

while GPIO.input(ECHO) == True:
    end = time.time()

sig_time = end - start

distance = sig_time / 0.000058

print("Distance: {} cm".format(distance))
GPIO.cleanup()
