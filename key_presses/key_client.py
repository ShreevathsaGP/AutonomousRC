# key_client.py (Raspberry-Pi File)

# importing modules
from KeyPress import KeyPress
import time, datetime, os
import numpy as np

KeyPress().start('client', host='192.168.0.104')
