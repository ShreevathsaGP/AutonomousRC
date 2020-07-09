# Car.py (main file for car control)

import numpy as np
import time, datetime, os
import RPi.GPIO as GPIO

class Car:
    def __init__(self):
        # current states of the car
        self.current_speed = None # percentage value used alongsied PWM (Pulse Width Modulation)
        self.is_going_forward = False
        self.is_going_reverse = False
        self.is_going_right = False
        self.is_going_left = False

##        Function rules:
##            0 --> failed
##            1 --> success

    # forward movement
    def forward(self):
        # if already moving forward then pass
        if is_going_forward:
            return 0

        # if not moving forward log that you now are
        self.is_going_forward = True
        pass

    # reverse movement
    def reverse(self):
        # if already moving reverse then pass
        if is_going_reverse:
            return 0
        
        # if not moving reverse log that you now are
        self.is_going_reverse = True

    # turning right
    def right(self):
        # if already turning right then pass
        if is_going_right:
            return 0
        
        # if not turning right log that you now are
        self.is_turning_right = True

    # turning left
    def left(self):
        if is_going_left:
            return 0
        
        # if not turning left log that you now are
        self.is_turning_left = True
    
