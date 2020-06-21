from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def initUI(self):
        # background
        self.setObjectName("MainWindow")
        self.setEnabled(True)
        self.resize(803, 700)
        self.setAutoFillBackground(False)
        self.setStyleSheet("background: #DCDCDC    ;  border: 0px solid black;")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        # training_mode
        self.training_button = QtWidgets.QPushButton(self.centralwidget)
        self.training_button.setGeometry(QtCore.QRect(0, 0, 411, 61))
        self.training_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/training_mode.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.training_button.setIcon(icon)
        self.training_button.setIconSize(QtCore.QSize(400, 55))
        self.training_button.setObjectName("training_button")

        # testing_mode
        self.testing_button = QtWidgets.QPushButton(self.centralwidget)
        self.testing_button.setGeometry(QtCore.QRect(400, 0, 401, 61))
        self.testing_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/testing_mode.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.testing_button.setIcon(icon1)
        self.testing_button.setIconSize(QtCore.QSize(400, 55))
        self.testing_button.setObjectName("testing_button")
        self.label = QtWidgets.QLabel(self.centralwidget)

        # raspberry pi feed
        self.label.setGeometry(QtCore.QRect(6, 63, 794, 471))
        self.label.setStyleSheet("background: white; border: 3px solid black")
        self.label.setText("")
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

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "AutonomousRC Companion"))

    def keyPressEvent(self, event):
        if event.text().lower() == 'w':
            self.icon2.addPixmap(QtGui.QPixmap("assets/after/gui_arrow_up_after.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.forward.setIcon(self.icon2)
        elif event.text().lower() == 'a':
            self.icon3.addPixmap(QtGui.QPixmap("assets/after/gui_arrow_left_after.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.left.setIcon(self.icon3)
        elif event.text().lower() == 's':
            self.icon4.addPixmap(QtGui.QPixmap("assets/after/gui_arrow_down_after.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.reverse.setIcon(self.icon4)
        elif event.text().lower() == 'd':
            self.icon5.addPixmap(QtGui.QPixmap("assets/after/gui_arrow_right_after.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.right.setIcon(self.icon5)

    def keyReleaseEvent(self, event):
        if event.text().lower() == 'w':
            self.icon2.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_up_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.forward.setIcon(self.icon2)
        elif event.text().lower() == 'a':
            self.icon3.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_left_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.left.setIcon(self.icon3)
        elif event.text().lower() == 's':
            self.icon4.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_down_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.reverse.setIcon(self.icon4)
        elif event.text().lower() == 'd':
            self.icon5.addPixmap(QtGui.QPixmap("assets/before/gui_arrow_right_before.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.right.setIcon(self.icon5)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())
