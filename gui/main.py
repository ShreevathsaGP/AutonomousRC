# gui imports
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time, datetime

# socket imports
import socket
import struct
import io
import pickle
import numpy as np
from PIL import Image


class ARC_Companion(QMainWindow):
    def __init__(self):
        super(ARC_Companion, self).__init__()

        # initializing global constants
        self.mode = 'training_mode'
        self.HOST = '192.168.0.104'
        self.CAMERA_PORT = 4999
        self.DISTANCE_PORT = 4998
        self.KEY_PORT = 4997
        self.significant_figures = 20
        self.key_state = [0 for i in range(4)]
    
        # initualizing app
        self.initUI()
        self.initTCPCamera()
        self.initTCPKey()

        # initializing raspberry pi camera feed
        self.camera_timer = QtCore.QTimer()
        self.camera_timer.timeout.connect(self.rpi_camera_feed)
        self.camera_timer.start(10)

        # initializing key press feed
        self.key_timer = QtCore.QTimer()
        self.key_timer.timeout.connect(self.key_feed)
        self.key_timer.start(10)
        
        '''
        # initializing raspberry pi distance feed
        self.initTCPDistance()
        self.distance_timer = QtCore.QTimer()
        self.distance_timer.timeout.connect(self.rpi_distance_feed)
        self.distance_timer.start(10)
        '''

    def rpi_camera_feed(self):
        frame_length = struct.unpack('<L', self.camera_connection.read(struct.calcsize('<L')))[0]
        if not frame_length:
            pass

        try:
            # stream for frames
            image_stream = io.BytesIO()
            image_stream.write(self.camera_connection.read(frame_length))
            image_stream.seek(0)
            frame = np.array(Image.open(image_stream))
            width, height, channels = frame.shape
                                    # np-array    height  width  step=>channels*width     rgb format (888)
            self.frame = QtGui.QImage(frame.data, height, width, frame.strides[0], QtGui.QImage.Format_RGB888)
            self.label.setPixmap(QtGui.QPixmap.fromImage(self.frame))
        except Exception as e:
            # print error
            print(e)

    def key_feed(self):
        # send key state to raspberry pi
        try:
            # 1=True & 0=False --> [W,A,S,D]
            self.key_socket.send(pickle.dumps(self.key_state))
        except Exception as e:
            # print error (if any)
            print(e)

    '''
    def distance_feed(self):
        pass
    '''
            
    def change_mode(self, mode):
        if mode == 'training_mode' and self.mode != 'training_mode':
            # set new mode
            self.mode = 'training_mode'
            
            # select training_mode
            self.icon.addPixmap(QtGui.QPixmap("assets/training_mode_selected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.training_button.setIcon(self.icon)

            # deselect testing_mode
            self.icon1.addPixmap(QtGui.QPixmap("assets/testing_mode.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.testing_button.setIcon(self.icon1)
            
        elif mode == 'testing_mode' and self.mode != 'testing_mode':
            # set new mode
            self.mode = 'testing_mode'
            
            # select testing_mode
            self.icon1.addPixmap(QtGui.QPixmap("assets/testing_mode_selected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.testing_button.setIcon(self.icon1)

            # deselect training_mode
            self.icon.addPixmap(QtGui.QPixmap("assets/training_mode.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.training_button.setIcon(self.icon)

    def initTCPCamera(self):
        self.server_socket = socket.socket()
        self.server_socket.bind((self.HOST, self.CAMERA_PORT))
        self.server_socket.listen(0)

        self.camera_socket, address = self.server_socket.accept()
        print(f"CAM CONNECTION ESTABLISHED WITH :--> {address}")
        self.camera_connection = self.camera_socket.makefile('rb')

    def initTCPKey(self):
        self.server_socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket3.bind((self.HOST, self.KEY_PORT))
        self.server_socket3.listen(0)

        self.key_socket, address = self.server_socket3.accept()
        print(f"KEY CONNECTION ESTABLISHED WITH :--> {address}")
    
    '''
    def initTCPDistance(self):
        self.server_socket2 = socket.socket()
        self.server_socket2.bind((self.HOST, self.DISTANCE_PORT))
        self.server_socket2.listen(0)

        self.client_socket2, address = self.server_socket2.accept()
        self.distance_connection = self.client_socket2.makefile('rb')
    '''
    
    def initUI(self):
        # background
        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.setFixedSize(803, 700)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background: #DCDCDC    ;  border: 0px solid black;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # training mode
        self.training_button = QtWidgets.QPushButton(self.centralwidget)
        self.training_button.setGeometry(QtCore.QRect(0, 0, 411, 61))
        self.training_button.setText("")
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("assets/training_mode_selected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.training_button.setIcon(self.icon)
        self.training_button.setIconSize(QtCore.QSize(400, 55))
        self.training_button.setObjectName("training_button")

        # testing mode
        self.testing_button = QtWidgets.QPushButton(self.centralwidget)
        self.testing_button.setGeometry(QtCore.QRect(400, 0, 401, 61))
        self.testing_button.setText("")
        self.icon1 = QtGui.QIcon()
        self.icon1.addPixmap(QtGui.QPixmap("assets/testing_mode.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.testing_button.setIcon(self.icon1)
        self.testing_button.setIconSize(QtCore.QSize(400, 55))
        self.testing_button.setObjectName("testing_button")

        # design and set raspberry pi camera feed
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(6, 63, 794, 471))
        self.label.setStyleSheet("border: 3px solid black")
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        # forward button
        self.forward = QtWidgets.QPushButton(self.centralwidget)
        self.forward.setGeometry(QtCore.QRect(270, 538, 111, 111))
        self.forward.setStyleSheet("")
        self.forward.setText("")
        self.icon2 = QtGui.QIcon()
        self.icon2.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_up_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.forward.setIcon(self.icon2)
        self.forward.setIconSize(QtCore.QSize(111, 111))
        self.forward.setObjectName("forward")

        # left button
        self.left = QtWidgets.QPushButton(self.centralwidget)
        self.left.setGeometry(QtCore.QRect(550, 538, 111, 111))
        self.left.setStyleSheet("")
        self.left.setText("")
        self.icon3 = QtGui.QIcon()
        self.icon3.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_left_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.left.setIcon(self.icon3)
        self.left.setIconSize(QtCore.QSize(111, 111))
        self.left.setObjectName("left")

        # reverse button
        self.reverse = QtWidgets.QPushButton(self.centralwidget)
        self.reverse.setGeometry(QtCore.QRect(410, 538, 111, 111))
        self.reverse.setStyleSheet("")
        self.reverse.setText("")
        self.icon4 = QtGui.QIcon()
        self.icon4.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_down_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reverse.setIcon(self.icon4)
        self.reverse.setIconSize(QtCore.QSize(111, 111))
        self.reverse.setObjectName("reverse")

        # right button
        self.right = QtWidgets.QPushButton(self.centralwidget)
        self.right.setGeometry(QtCore.QRect(688, 538, 111, 111))
        self.right.setStyleSheet("")
        self.right.setText("")
        self.icon5 = QtGui.QIcon()
        self.icon5.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_right_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.right.setIcon(self.icon5)
        self.right.setIconSize(QtCore.QSize(111, 111))
        self.right.setObjectName("right")

        # design ultrasonic feed
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(6, 538, 241, 111))
        self.font = QtGui.QFont()
        self.font.setFamily("Optima")
        self.font.setPointSize(14)
        self.label_2.setFont(self.font)
        self.label_2.setStyleSheet("background: white; border: 2px solid black;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 550, 131, 50))
        self.font = QtGui.QFont()
        self.font.setFamily("Optima")
        self.font.setPointSize(24)
        self.label_3.setFont(self.font)
        self.label_3.setStyleSheet("background: white;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 590, 131, 40))
        self.font = QtGui.QFont()
        self.font.setFamily("Optima")
        self.font.setPointSize(24)
        self.label_4.setFont(self.font)
        self.label_4.setStyleSheet("background: white;")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(140, 540, 21, 91))
        self.font = QtGui.QFont()
        self.font.setFamily("Optima")
        self.font.setPointSize(64)
        self.label_5.setFont(self.font)
        self.label_5.setStyleSheet("background: white;")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(160, 549, 81, 91))
        self.font = QtGui.QFont()
        self.font.setFamily("Charter")
        self.font.setPointSize(48)
        self.font.setItalic(False)
        self.label_6.setFont(self.font)
        self.label_6.setStyleSheet("background: white;")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")

        # set ultrasonic feed
        self.label_3.setText("Ultrasonic")
        self.label_4.setText("Sensor (cm)")
        self.label_5.setText(":")
        self.label_6.setText("Na")

        # standard stuff
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 22))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # mapping button presses
        self.training_button.clicked.connect(lambda: self.change_mode('training_mode'))
        self.testing_button.clicked.connect(lambda: self.change_mode('testing_mode'))

    def retranslateUi(self):
        # set window title
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "AutonomousRC Companion"))

    def keyPressEvent(self, event):
        # key down with WASD mapping
        if event.text().lower() == 'w':
            self.icon2.addPixmap(QtGui.QPixmap("assets/after/gui_arrow_up_after.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.forward.setIcon(self.icon2)

            self.key_state[0] = 1
            
        elif event.text().lower() == 'a':
            self.icon3.addPixmap(QtGui.QPixmap("assets/after/gui_arrow_left_after.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.left.setIcon(self.icon3)

            self.key_state[1] = 1
            
        elif event.text().lower() == 's':
            self.icon4.addPixmap(QtGui.QPixmap("assets/after/gui_arrow_down_after.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.reverse.setIcon(self.icon4)

            self.key_state[2] = 1
            
        elif event.text().lower() == 'd':
            self.icon5.addPixmap(QtGui.QPixmap("assets/after/gui_arrow_right_after.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.right.setIcon(self.icon5)

            self.key_state[3] = 1

    def keyReleaseEvent(self, event):
        # key up with WASD mapping
        if event.text().lower() == 'w':
            self.icon2.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_up_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.forward.setIcon(self.icon2)

            self.key_state[0] = 0
            
        elif event.text().lower() == 'a':
            self.icon3.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_left_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.left.setIcon(self.icon3)

            self.key_state[1] = 0
            
        elif event.text().lower() == 's':
            self.icon4.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_down_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.reverse.setIcon(self.icon4)

            self.key_state[2] = 0
            
        elif event.text().lower() == 'd':
            self.icon5.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_right_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.right.setIcon(self.icon5)

            self.key_state[3] = 0
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ARC_Companion()
    win.show()
    sys.exit(app.exec_())
