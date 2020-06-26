# Ultrasonic.py

# import network wide modules
import socket
import struct
import time
import io
import pickle
import numpy as np

class Ultrasonic:
    def __init__(self):
        # initializing constants
        self.significant_figures = 5

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

                distance_value = int(ultrasonic_stream.read().decode('utf-8'))
        finally:
            # close sockets
            connection.close()
            client_socket.close()

    def get_distance_value(self):
        return None
    
    def client(self, host, port):
        # client socket
        client_socket = socket.socket()
        client_socket.connect((host, port))

        # make writable file object with connection
        connection = client_socket.makefile('wb')

        try:
            # get value from distance sensor
            distance_value = self.get_distance_value()

            # write into the connection file
            while True:
                connection.write(bytes('2389764378926', 'utf-8'))
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
