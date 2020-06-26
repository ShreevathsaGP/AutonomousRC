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
        # initializing contants
        self.significant_places = 2

    def server(self, host, port):
        # server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(0)

        try:
            while True:
                distance_value = server_socket.recv(1024).decode('utf-8')
                print(distance_value)
        finally:
            # close sockets
            server_socket.close()

    def client(self, host, port):
        # client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        try:
            while True:
                distance_value = 21
                client_socket.send(bytes(distance_value, 'utf-8'))
        finally:
            # close sockets
            client_socket.close()

    def start(self, role, host, port=4998):
        # begin socket connection
        if role == 'server':
            self.server(host, port)
        elif role == 'client':
            self.client(host, port)
