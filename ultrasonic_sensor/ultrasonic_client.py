# ultrasonic_client.py (Raspberry-Pi File)

# importing modules
from Ultrasonic import Ultrasonic
import time, datetime, os
import numpy as np

Ultrasonic().start('client', host='192.168.0.113')
