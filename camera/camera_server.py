# camer_server.py (Mac File)

# importing modules
from Camera import Camera
import time, datetime, os
import numpy as np

Camera().start('server', host='192.168.0.105') # default port = 4999
