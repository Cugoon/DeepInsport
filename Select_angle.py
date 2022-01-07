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
from Select_Video import Select_Video


class Select_Angle(QMainWindow):

    def __init__(self, video_path, front_image, side_image):
        super().__init__()
        self.windowList = []
        self.video_path = video_path
        self.front_image = front_image
        self.side_image = side_image
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

        border-image:url(./Ui_images/Choose_angle.jpg);

        border-radius:30px
        }

        }
        ''')

        self.front_button = QPushButton(self)
        self.front_button.setGeometry(QRect(600, 400, 250, 500))
        self.front_button.setStyleSheet(self.front_image)
        self.front_button.clicked.connect(self.onchick_select_front)

        self.side_button = QPushButton(self)
        self.side_button.setGeometry(QRect(1200, 400, 250, 500))
        self.side_button.setStyleSheet(self.side_image)
        self.side_button.clicked.connect(self.onchick_select_side)
        self.show()

    def onchick_select_front(self):
        name = self.video_path[6:-1]
        video_path = self.video_path + "Front/" + name + "_Front.mp4"
        print(video_path)
        self.close()
        the_window = Select_Video(video_path)
        self.windowList.append(the_window)

    def onchick_select_side(self):
        name = self.video_path[6:-1]
        video_path = self.video_path + "Side/" + name + "_Side.mp4"
        self.close()
        the_window = Select_Video(video_path)
        self.windowList.append(the_window)


def main():
    app = QApplication(sys.argv)
    video_path = r"Video/CollinMorikawa/"
    front_image = "QPushButton{background-image:url(UI_images/icons/CollinMorikawa_front.png);}"
    side_image = "QPushButton{background-image:url(UI_images/icons/CollinMorikawa_side.png);}"
    gui = Select_Angle(video_path, front_image, side_image)

    gui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()