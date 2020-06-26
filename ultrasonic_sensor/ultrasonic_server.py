# ultrasonic_server.py (Mac File)

# importing modules
from Ultrasonic import Ultrasonic
import time, datetime, os
import numpy as np

Ultrasonic(18,23).start('server', host='192.168.0.104')
