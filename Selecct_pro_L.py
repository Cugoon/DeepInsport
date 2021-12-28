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
from Select_angle import Select_Angle
from Select_Pro import Select_Pro

class Select_Pro_L(QMainWindow):

    def __init__(self):
        super().__init__()
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

        border-image:url(./Ui_images/golf_select.jpg);

        border-radius:30px
        }

        }
        ''')
        self.back_button = QPushButton("Back", self)    # 마우스 올릴 떄 툴팁
        """方法setToolTip在用户将鼠标停留在按钮上时显示的消息"""
        self.back_button.setToolTip("This is an example button")

        """按钮坐标x = 100, y = 70"""   #버튼 좌표
        # self.start_button.move(100,240)
        self.back_button.setGeometry(QRect(100, 240, 120, 28))

        # self.start_button.setStyleSheet("QPushButton{border-image: url(UI_images/CollinMorikawa.png)}")
        self.back_button.setStyleSheet(
            'background-color:rgb(192,192,190);border-radius: 10px; border: 5px groove gray;border-style: outset;')
        """按钮与鼠标点击事件相关联"""  # 마우스 클릭 이벤트
        self.back_button.clicked.connect(self.oncick_Back)
        self.Pro1_button = QPushButton(self)
        self.Pro1_button.setGeometry(QRect(250, 400, 180, 360))
        self.Pro1_button.setStyleSheet("QPushButton{background-image:url(UI_images/icons/YealimiNoh_.png);}")
        self.Pro1_button.clicked.connect(self.onchick_select_pro1)

        self.Pro2_button = QPushButton(self)
        self.Pro2_button.setGeometry(QRect(650, 400, 180, 360))
        self.Pro2_button.setStyleSheet("QPushButton{background-image:url(UI_images/icons/YOOHyunJu.png);}")
        self.Pro2_button.clicked.connect(self.onchick_select_pro2)

        self.Pro3_button = QPushButton(self)
        self.Pro3_button.setGeometry(QRect(1050, 400, 180, 360))
        self.Pro3_button.setStyleSheet("QPushButton{background-image:url(UI_images/icons/LeeHanSol.png);}")
        self.Pro3_button.clicked.connect(self.onchick_select_pro3)

        self.Pro4_button = QPushButton(self)
        self.Pro4_button.setGeometry(QRect(1450, 400, 180, 351))
        path = r"UI_images/icons/TigerWoods.png"
        self.Pro4_button.setStyleSheet("QPushButton{background-image:url(UI_images/icons/MichelleSungWie.png);}")
        self.Pro4_button.clicked.connect(self.onchick_select_pro4)

        self.show()

    def onchick_select_pro1(self):
        video_path = r"Video/YealimiNoh/"
        front_image = "QPushButton{background-image:url(UI_images/icons/YealimiNoh_front.png);}"
        side_image = "QPushButton{background-image:url(UI_images/icons/YealimiNoh_side.png);}"
        the_window = Select_Angle(video_path, front_image, side_image)
        self.close()
        self.windowList.append(the_window)

    def onchick_select_pro2(self):
        video_path = r"Video/YOOHyunJu/"
        front_image = "QPushButton{background-image:url(UI_images/icons/YOOHyunJu_front.png);}"
        side_image = "QPushButton{background-image:url(UI_images/icons/YOOHyunJu_Side.png);}"
        the_window = Select_Angle(video_path, front_image, side_image)
        self.close()
        self.windowList.append(the_window)

    def onchick_select_pro3(self):
        video_path = r"Video/LeeHanSol/"
        front_image = "QPushButton{background-image:url(UI_images/icons/LeeHanSol_front.png);}"
        side_image = "QPushButton{background-image:url(UI_images/icons/LeeHanSol_side.png);}"
        the_window = Select_Angle(video_path, front_image, side_image)
        self.close()
        self.windowList.append(the_window)

    def onchick_select_pro4(self):
        video_path = r"Video/TigerWoods/"
        front_image = "QPushButton{background-image:url(UI_images/icons/TigerWoods_front.png);}"
        side_image = "QPushButton{background-image:url(UI_images/icons/TigerWoods_side.png);}"
        the_window = Select_Angle(video_path, front_image, side_image)
        self.close()
        self.windowList.append(the_window)

    def oncick_Back(self):
        the_window = Select_Pro()
        self.close()
        self.windowList.append(the_window)
def main():
    app = QApplication(sys.argv)

    gui = Select_Pro_L()

    gui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
