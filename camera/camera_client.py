# camera_client.py (Raspberry-Pi File)

# importing modules
from Camera import Camera
import time, datetime, os
import numpy as np

Camera().start('client', host='192.168.0.104') # default port = 4999
