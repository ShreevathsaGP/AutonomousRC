import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


Motor1A = 13
Motor1B = 19
Motor1E = 26

Motor2A = 16
Motor2B = 20
Motor2E = 21

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

print("Turning motor FR on)")
GPIO.output(Motor1A, GPIO.HIGH)
GPIO.output(Motor1B, GPIO.LOW)
GPIO.output(Motor1E, True)

print("Turning motor FL on")
GPIO.output(Motor2A, GPIO.HIGH)
GPIO.output(Motor2B, GPIO.LOW)
GPIO.output(Motor2E, GPIO.HIGH)

time.sleep(5)

print("Turning both motors off")
GPIO.output(Motor1E, GPIO.LOW)
GPIO.output(Motor2E, True)

GPIO.cleanup()
