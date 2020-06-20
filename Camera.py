
import picamera
import socket
import struct
import time
from system import HOST, PORT

class Camera:
    def __init__(self):
        self.width = 500
        self.height = 480
        self.vflip = True
        self.hflip = False

    def server(self, host, port):
        from PIL import Image
        import matplot.lib.pyplot as plt
        import cv2
        
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen(0)

        connection = server_socket.accept()[0].makefile('rb')

        try:
            frame = None
            while True:
                frame_length = struct.unpack('<L', connection.read(struct.calcsize('L')))[0]
                if not frame_length:
                    break

                image_stream = io.BytesIO()
                image_stream.write(connection.read(frame_length))

                image_stream.seek(0)
                frame = Image.open(image_stream)

                cv2.imshow('RPi-Camera', frame)

                print("Frame is %dx%d" % frame.size())
                frame.verify()
                print("Frame is verified")
        
    
    def client(self, host, port):
        client_socket = socket.socket()
        client_socket.connect((host, port))

        connection = client_socket.makefile('wb')

        try:
            camera = picamera.PiCamera()
            camera.vflip = self.vflip
            camera.hflip = self.hflip

            camera.start_preview()
            time.sleep(1.5)

            start_time = time.time()
            image_stream = io.BytesIO()
            for _ in camera.capture_continuous(image_stream, 'jpeg'):
                connnection.write(struct.pack('<L', image_stream.tell()))
                connection.flush()

                image_stream.seek(0)
                connection.write(stream.read())

                image_stream.seek(0)
                image_stream.truncate()

            connection.write(struct.pack('<L', 0))
        finally:
            connection.cose()
            client_socket.close()

    def start(role):
        if role == 'server':
            server('')
