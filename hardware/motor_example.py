import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# setting up motor 1
Motor1A = 16
Motor1B = 18
Motor1E = 22

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

# turning motor forward
print("Turning motor forward")
GPIO.output(Motor1A, GPIO.HIGH)
GPIO.output(Motor1B, GPIO.LOW)
GPIO.output(Motor1E, GPIO.HIGH)

time.sleep(2)

# turning motor in reverse
print("Turning motor backward")
GPIO.output(Motor1A, GPIO.LOW)
GPIO.output(Motor1B, GPIO.HIGH)
GPIO.output(Motor1E, GPIO.HIGH)

time.sleep(2)

# turning motor off
print("Turning motor off")
GPIO.output(Motor1E, GPIO.LOW)

# ending GPIOs
GPIO.cleanup()

