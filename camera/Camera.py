# Camera.py

# import network wide modules
import socket
import struct
import time
import io
import pickle
import numpy as np

class Camera:
    def __init__(self):
        # initializing contants
        self.width = 320
        self.height = 240
        self.vflip = True

    def server(self, host, port):
        # importing server spcific modules
        from PIL import Image
        import matplotlib.pyplot as plt
        import cv2

        # server socket
        server_socket = socket.socket()
        server_socket.bind((host, port))
        server_socket.listen(0)

        # make readable file object with connection
        connection = server_socket.accept()[0].makefile('rb')

        try:
            frm = None
            while True:
                # find length of frame
                frame_length = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not frame_length:
                    break

                # open anf convert frame into array
                image_stream = io.BytesIO()
                image_stream.write(connection.read(frame_length))
                image_stream.seek(0)
                frame = Image.open(image_stream)

                # display (colour converted) frame
                cv2.imshow('RasPi-Feed', cv2.cvtColor(np.array(frame), cv2.COLOR_BGR2RGB))
                if cv2.waitKey(25) & 0xff == ord('q'):
                    cv2.destroyAllWindows()
                    break

        finally:
            # close sockets
            connection.close()
            server_socket.close()
        
    def client(self, host, port):
        # importing client specific modules
        import picamera

        # client socket
        client_socket = socket.socket()
        client_socket.connect((host, port))

        connection = client_socket.makefile('wb')
        # make writable file object with connection

        try:
            # configure camera
            camera = picamera.PiCamera()
            camera.vflip = self.vflip
            camera.resolution = (self.width, self.height)
            camera.framerate = 30

            # start and warm up camera => 1 second
            camera.start_preview()
            time.sleep(1)

            start_time = time.time()
            image_stream = io.BytesIO()
            for _ in camera.capture_continuous(image_stream, 'jpeg', use_video_port=True):
                # write current position of file into connection
                connection.write(struct.pack('<L', image_stream.tell()))
                # clean internal buffer
                connection.flush()

                # write frame into connection
                image_stream.seek(0)
                connection.write(image_stream.read())

                image_stream.seek(0)
                image_stream.truncate()

            # signal end of stream
            connection.write(struct.pack('<L', 0))
        finally:
            # close sockets
            connection.close()
            client_socket.close()

    def start(self, role, host, port=4999):
        # begin socket connection
        if role == 'server':
            self.server(host, port)
        elif role == 'client':
            self.client(host, port)
