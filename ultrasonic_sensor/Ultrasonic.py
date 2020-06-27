# Ultrasonic.py

# import network wide modules
import socket
import struct
import time
import io
import pickle
import numpy as np
import random

class Ultrasonic:
    def __init__(self, trigger_no, echo_no):
        # initializing constants
        self.significant_figures = 20
        self.gpio_trigger = trigger_no
        self.gpio_echo = echo_no
        self.iteration = 0
        

    def server(self, host, port):
        # server socket
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen(0)

        # make readable file object with connection
        connection = server_socket.accept()[0].makefile('rb')

        try:
            # continuously read from the connection
            while True:
                ultrasonic_stream = io.BytesIO()
                ultrasonic_stream.write(connection.read(self.significant_figures))
                ultrasonic_stream.seek(0)

                distance_value = float(ultrasonic_stream.read().decode('utf-8'))
                print(distance_value)
        finally:
            # close sockets
            connection.close()
            server_socket.close()

    def get_distance_value(self):
        # import client specific modules
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        
        # setup gpio pins
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)

        # trigger sensor
        GPIO.output(self.gpio_trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)

        # measure time taken for return signal
        start = time.time()
        while GPIO.input(self.gpio_echo) == False:
            start = time.time()
        while GPIO.input(self.gpio_echo) == True:
            end = time.time()
        time_taken = end - start

        # calculate distance value
        distance = time_taken / 0.000058
        distance = f"{distance:<{self.significant_figures}}"
        print(distance)
        return distance
    
    def client(self, host, port):
        if self.iteration == 0:
            self.iteration +=1
            # client socket
            client_socket = socket.socket()
            client_socket.connect((host, port))

##            # make writable file object with connection
##            connection = client_socket.makefile('wb')
        
        try:
            # write distance into the connection file
            while True:
                # get value from distance sensor
                distance_value = self.get_distance_value()
##                connection.write(bytes(distance_value, 'utf-8'))
                client_socket.send(bytes(distance_value, 'utf-8'))
        finally:
            # close sockets
            connection.close()
            client_socket.close()

    def start(self, role, host, port=4998):
        # begin socket connection
        if role == 'server':
            self.server(host, port)
        elif role == 'client':
            self.client(host, port)
