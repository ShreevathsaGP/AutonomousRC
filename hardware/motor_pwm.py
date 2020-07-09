import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Motor1A = 23
Motor1B = 24
Motor1E = 25

Motor2A = 13
Motor2B = 19
Motor2E = 26

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)

print("Turning motor FR on)")
PWM1 = GPIO.PWM(Motor1A, 100)
PWM1.start(50)
GPIO.output(Motor1B, GPIO.LOW)
GPIO.output(Motor1E, True)

print("Turning motor FL on")
PWM2 = GPIO.PWM(Motor2A, 100)
PWM2.start(50)
GPIO.output(Motor2B, GPIO.LOW)
GPIO.output(Motor2E, GPIO.HIGH)

time.sleep(5)

print("Turning both motors off")
PWM1.stop()
PWM2.stop()

GPIO.cleanup()
