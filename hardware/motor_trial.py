import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Motor1A = 23
Motor1B = 24
Motor1E = 25

Motor2A = 17
Motor2B = 27
Motor2E = 22

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

print("Turning this garbage on")
GPIO.output(Motor1E, GPIO.HIGH)
GPIO.output(Motor1A, GPIO.HIGH)
GPIO.output(Motor1B, GPIO.LOW)

GPIO.output(Motor2E, GPIO.HIGH)
GPIO.output(Motor2A, GPIO.HIGH)
GPIO.output(Motor2B, GPIO.LOW)

time.sleep(5)

print("Turning this garbage off")
GPIO.output(Motor1E, GPIO.LOW)
GPIO.output(Motor2E, GPIO.LOW)

GPIO.cleanup()
