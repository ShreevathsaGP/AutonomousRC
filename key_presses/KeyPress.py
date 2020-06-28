# KeyPress.py

# import network wide modules
import socket
import time
import pickle
import numpy as np
import random

class KeyPress:
    def __init__(self):
        # initializing constanta
        pass

    def server(self, host, port):
        # server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.liten(0)

        try:
            # accept connection
            client_socket, address = server_socket.accept()
            print(f"Established connection with {address}")

            # emulate keystates 1=True & 0=False --> [W,A,S,D]
            while True:
                key_state = [random.choice([0,1]) for _ in range(4)]
                print(key_state)

                # real key_state will be done with PyQt5
                client_socket.send(pickle.dumps(key_state))
        finally:
            client_socket.disconnect()
            server_socket.close()

    def client(self, host, port):
        # client socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # get constant state of keyboard from server
        while True:
            key_state = client_socket.recv(1024)
            print(pickle.loads(key_state))

    def start(self, role, host, port=4997):
        # begin socket connection
        if role == 'server':
            self.server(host, port)
        elif role == 'client':
            self.client(host, port)
