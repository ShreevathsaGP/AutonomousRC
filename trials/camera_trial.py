import picamera
import time, datetime, os

camera = picamera.PiCamera()
camera.vflip = True

camera.start_recording("sample_files/example_video.h264")
time.sleep(5)
camera.stop_recording()
