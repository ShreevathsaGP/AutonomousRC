import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Motor1A = 23
Motor1B = 24
Motor1E = 25

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

print("Turning motor on)")
GPIO.output(Motor1A, GPIO.HIGH)
GPIO.output(Motor1B, GPIO.LOW)

##GPIO.output(Motor1E, GPIO.HIGH)
##time.sleep(2)
##
##print("Turning motor off")
##GPIO.output(Motor1E, GPIO.LOW)
##
##time.sleep(2)
##
##print("Turning motor back on")
##GPIO.output(Motor1E, GPIO.HIGH)
##time.sleep(2)

# use pwm on 25 (Motor1E) at 100Hz
time.sleep(1)
print("Starting pulse width modulation")
pwm = GPIO.PWM(25, 100)
duty_cycle = 0

for i in range(0,101, 2):
    duty_cycle = i
    pwm.start(duty_cycle)
    time.sleep(0.5)

time.sleep(4)
print("Ending pulse width modulation")
pwm.stop()

GPIO.cleanup()
