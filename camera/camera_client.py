# RasPi.py (Raspberry-Pi File)

# importing modules
from Camera import Camera
import time, datetime, os
import numpy as np

Camera().start('client', host='192.168.0.109') # default port = 4999
