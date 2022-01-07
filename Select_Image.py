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

from Motion_image_window import Motion_image_window


class Select_Image(QMainWindow):

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

        self.local_button = QPushButton("1. Address", self)
        self.local_button.setGeometry(QRect(60, 400, 180, 360))
        self.local_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                        "QPushButton{background-color:gray}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:10px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.local_button.clicked.connect(self.process_select)

        self.local_button = QPushButton("2. Take Back", self)
        self.local_button.setGeometry(QRect(280, 400, 180, 360))
        self.local_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                        "QPushButton{background-color:gray}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:10px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.local_button.clicked.connect(self.process_select)

        self.local_button = QPushButton("3. Back Swing", self)
        self.local_button.setGeometry(QRect(500, 400, 180, 360))
        self.local_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                        "QPushButton{background-color:gray}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:10px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.local_button.clicked.connect(self.process_select)

        self.local_button = QPushButton("4. Top Position", self)
        self.local_button.setGeometry(QRect(720, 400, 180, 360))
        self.local_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                        "QPushButton{background-color:gray}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:10px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.local_button.clicked.connect(self.process_select)

        self.local_button = QPushButton("5. Down Swing", self)
        self.local_button.setGeometry(QRect(960, 400, 180, 360))
        self.local_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                        "QPushButton{background-color:gray}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:10px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.local_button.clicked.connect(self.process_select)

        self.local_button = QPushButton("6. Impact", self)
        self.local_button.setGeometry(QRect(1180, 400, 180, 360))
        self.local_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                        "QPushButton{background-color:gray}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:10px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.local_button.clicked.connect(self.process_select)

        self.local_button = QPushButton("7. Follow Through", self)
        self.local_button.setGeometry(QRect(1400, 400, 180, 360))
        self.local_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                        "QPushButton{background-color:gray}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:10px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.local_button.clicked.connect(self.process_select)

        self.local_button = QPushButton("8. Finish", self)
        self.local_button.setGeometry(QRect(1620, 400, 180, 360))
        self.local_button.setStyleSheet("QPushButton{color:black;font:bold 20px;}"
                                        "QPushButton{background-color:gray}"
                                        "QPushButton{border:2px}"
                                        "QPushButton{border-radius:10px}"
                                        "QPushButton:pressed{background-color:rgb(180,180,180);border: None;}")
        self.local_button.clicked.connect(self.process_select)
        self.show()

    def process_select(self):
        process_name = QFileDialog.getOpenFileName(self, 'open file', '')
        print(process_name[0])
        self.process_image = process_name[0]
        print(self.target_path)
        the_window = Motion_image_window(self.target_path, self.process_image)
        self.windowList_append(the_window)
        self.close()


def main():
    app = QApplication(sys.argv)
    video_path = r'Video/DustinJohnson/Front/DustinJohnson_Front.mp4'
    gui = Select_Image(video_path)

    gui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()



