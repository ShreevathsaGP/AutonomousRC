# Car.py (Raspberry-Pi File)

# camera multiprocessing imports
from camera.Camera import Camera
import multiprocessing

# import car wide modules
import time, datetime, os
import RPi.GPIO as GPIO
import socket
import pickle
import numpy as np

# BroadCom mode
GPIO.setmode(GPIO.BCM)

class Car:
    def __init__(self, speed_mode, usage_mode):
        # Car modes
        self.speed_mode = speed_mode
        self.usage_mode = usage_mode
        
        # Motor GPIO pins (LOW by default)
        self.left_forward = 6 # Left side motors (Input 1)
        self.left_backward = 13 # Left side motors (Input 2)
        GPIO.setup(self.left_forward, GPIO.OUT)
        GPIO.setup(self.left_backward, GPIO.OUT)
        self.right_forward = 19 # Right side motors (Input 3)
        self.right_backward = 26 # Right side motors (Input 4)
        GPIO.setup(self.right_forward, GPIO.OUT)
        GPIO.setup(self.right_backward, GPIO.OUT)

        # PWM (Pulse Width Modulation) constants
        self.frequency = 100 # Hertz
        self.duty_cycle = 70

        # Recording state of the car
        self.already_reset = False

        # Initializing PWMs
        self.lfPWM = GPIO.PWM(self.left_backward, self.frequency)
        self.lbPWM = GPIO.PWM(self.left_forward, self.frequency)
        self.rfPWM = GPIO.PWM(self.right_backward, self.frequency)
        self.rbPWM = GPIO.PWM(self.right_forward, self.frequency)
        
        # Configuring TCP Server
        self.host = '192.168.0.104'
        self.port = 4997
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Attempting TCP Connection with: {} at {}".format(self.host, self.port))
        self.client_socket.connect((self.host, self.port))
        print("Established TCP Connection with: {} at {}".format(self.host, self.port))
        
    def reset(self):
        self.already_reset = True

        if self.speed_mode == 'chill':
            # Stop all PWM processes
            self.lfPWM.stop()
            self.lbPWM.stop()
            self.rfPWM.stop()
            self.rbPWM.stop()
        elif self.speed_mode == 'ludicrous':
            # Set everything to low
            GPIO.output(self.left_forward, GPIO.LOW)
            GPIO.output(self.left_backward, GPIO.LOW)
            GPIO.output(self.right_forward, GPIO.LOW)
            GPIO.output(self.right_backward, GPIO.LOW)

    def forward(self):
        self.already_reset = False
        
##        print("forward")
        if self.speed_mode == 'chill':
            self.lfPWM.start(self.duty_cycle)
            self.rfPWM.start(self.duty_cycle)
        elif self.speed_mode == 'ludicrous':
            GPIO.output(self.right_forward, GPIO.HIGH)
            GPIO.output(self.left_forward, GPIO.HIGH)

    def reverse(self):
        self.already_reset = False
        
##        print("reverse")
        if self.speed_mode == 'chill':
            self.lbPWM.start(self.duty_cycle)
            self.rbPWM.start(self.duty_cycle)
        elif slef.speed_mode == 'ludicrous':
            GPIO.output(self.right_backward, GPIO.HIGH)
            GPIO.output(self.left_backward, GPIO.HIGH)

    def forward_right(self):
        self.already_reset = False
        
##        print("forward right")
        if self.speed_mode == 'chill':
            self.rfPWM.start(90)
        elif self.speed_mode == 'ludicrous':
            GPIO.output(self.right_backward, GPIO.HIGH)

    def backward_right(self):
        self.already_reset = False

##        print("backward right")
        if self.speed_mode == 'chill':
            self.rbPWM.start(90)
        elif self.speed_mode == 'ludicrous':
            GPIO.output(self.right_forward, GPIO.HIGH)

    def forward_left(self):
        self.already_reset = False
        
##        print("forward left")
        if self.speed_mode == 'chill':
            self.lfPWM.start(90)
        elif self.speed_mode == 'ludicrous':
            GPIO.output(self.left_backward, GPIO.HIGH)

    def backward_left(self):
        self.already_reset = False

##        print("backward left")
        if self.speed_mode == 'chill':
            self.lbPWM.start(90)
        elif self.speed_mode == 'ludicrous':
            GPIO.output(self.left_forward, GPIO.HIGH)
    
    def listen(self):
        """ Input Format: [W,A,S,D] --> 1 = Pressed & 0 = NotPressed """
        while True:
            instruction = None
            try:
                key_state = pickle.loads(self.client_socket.recv(1024))
                print(key_state)
                
                if key_state[0] == 1:
                    if key_state[1] == 1: # straight & left
                        if not self.already_reset:
                            self.reset()
                        self.forward_left()

                    elif key_state[-1] == 1: # straight & right
                        if not self.already_reset:
                            self.reset()
                        self.forward_right()
                        
                    else: # straight only
                        if not self.already_reset:
                            self.reset()
                        self.forward()
                        
                elif key_state[2] == 1:
                    if key_state[1] == 1: # reverse & left
                        pass
                        if not self.already_reset:
                            self.reset()
                        self.backward_left()

                    elif key_state[-1] == 1: # reverse & right
                        pass
                        if not self.already_reset:
                            self.reset()
                        self.backward_right()
                        
                    else: # reverse only
                        if not self.already_reset:
                            self.reset()
                        self.reverse()

                # if no instructions => [0,0,0,0]
                else:
                    if not self.already_reset:
                        self.reset()

            except Exception as e:
                print(e)
                pass

def camera_target():
    # Define camera object and run()
    Camera().start('client', '192.168.0.104')
##    print("camera starting")

def car_target():
    # Define car object and run()
    AutonomousRC = Car('chill', 'ludicrous')
    AutonomousRC.listen()
##    print("car booting")

camera_process = multiprocessing.Process(target=camera_target)
car_process = multiprocessing.Process(target=car_target)

camera_process.start()
car_process.start()
