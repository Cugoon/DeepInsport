from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
import time
import cv2
import os
from PyQt5.QtMultimediaWidgets import QVideoWidget



import qtawesome
import functools
import sys
from PyQt5 import QtCore
from Motion_window import *


class Select_Video(QMainWindow):

    def __init__(self, video_path):
        super().__init__()
        self.windowList = []
        self.target_path = video_path
        self.user_video = None
        self.windowList = []
        self.init_UI()

    def init_UI(self):
        self.resize(1920, 1240)
        self.main_widget = QWidget()
        self.main_widget.setObjectName("main_widget")
        self.main_layout = QGridLayout()
        self.main_widget.setLayout(self.main_layout)  #
        self.setCentralWidget(self.main_widget)

        self.main_widget.setStyleSheet('''
         #main_widget{

        border-image:url(./Ui_images/Choose_Video.jpg);

        border-radius:30px
        }

        }
        ''')

        self.local_button = QPushButton("Local Video", self)
        self.local_button.setGeometry(QRect(800, 400, 200, 50))
        self.local_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                        "QPushButton{background-color:gray}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:10px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.local_button.clicked.connect(self.onchick_select_local)

        self.camera_button = QPushButton("Open Camera", self)
        self.camera_button.setGeometry(QRect(800, 500, 200, 50))
        self.camera_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                         "QPushButton{background-color:gray}"
                                         "QPushButton{border:2px}"
                                         "QPushButton{border-radius:10px}"
                                         "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.camera_button.clicked.connect(self.onchick_select_camera)
        self.show()

    def onchick_select_local(self):
        openfile_name = QFileDialog.getOpenFileName(self, 'open file', '', 'Excel files(*.mp4 , *.avi)')
        print(openfile_name[0])
        self.user_video = openfile_name[0]
        print(self.target_path)
        the_window = Motion_ex_window(self.target_path,self.user_video)
        self.windowList.append(the_window)
        self.close()

    def onchick_select_camera(self):
        self.user_video = 0
        the_window = Motion_ex_window(self.target_path,self.user_video)
        self.windowList.append(the_window)
        self.close()


def main():
    app = QApplication(sys.argv)
    video_path = r'Video/DustinJohnson/Front/DustinJohnson_Front.mp4'
    gui = Select_Video(video_path)


    gui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


    
