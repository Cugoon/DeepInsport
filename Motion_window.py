#실시간 평점

import cv2
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from cv2 import *

from Openpose import Opnenpose

OP = Opnenpose()
from data_preprocessing import *
from score_show import score_App

class VideoThread(QThread): #스레드 구현
    target_pixmap_signal = pyqtSignal(QImage)
    user_pixmap_signal = pyqtSignal(QImage)
    finished = pyqtSignal(str)
    def __init__(self,target_video,user_video,*args, **kwargs):

        super().__init__()
        self.cap_target = VideoCapture(target_video)
        self.cap_user = VideoCapture(user_video)
        self.OP_target = Opnenpose()
        self.OP_user = Opnenpose()
        self.predictior = prediction("SVM.sav") # 사전 학습한 SVM의 prediction을 사용
        self.scores = []
        self.windowList = []


    def run(self):
        #dim = (1000,780)
        while self.cap_target.isOpened() and self.cap_user.isOpened():
            ret_target, frame_target = self.cap_target.read()
            ret_user, frame_user = self.cap_user.read()

            if ret_target and ret_user:
                #frame_target = cv2.resize(frame_target, dim, interpolation=cv2.INTER_AREA)
                #frame_user = cv2.resize(frame_user, dim, interpolation=cv2.INTER_AREA)
                self.OP_target.out_frame(frame_target)
                self.OP_user.out_frame(frame_user)

                frame_target = self.OP_target.datum.cvOutputData
                frame_user = self.OP_user.datum.cvOutputData
                try:
                    if len(self.OP_target.datum.poseKeypoints) <= 1:
                        keypoin_target = self.OP_target.datum.poseKeypoints
                    else:
                        keypoin_target = self.OP_target.datum.poseKeypoints


                    if len(self.OP_user.datum.poseKeypoints) <= 1:
                        keypoin_user = self.OP_user.datum.poseKeypoints
                    else:
                        keypoin_user = self.OP_user.datum.poseKeypoints[0]

                    score = self.predictior.score(np.array(keypoin_target), np.array(keypoin_user))
                    score = (round(score[0][1] * 100))
                except:
                    score = 0


                rgbImage_target = cv2.cvtColor(frame_target, cv2.COLOR_BGR2RGB)
                rgbImage_user = cv2.cvtColor(frame_user, cv2.COLOR_BGR2RGB)

                convertToQtFormat_target = QImage(rgbImage_target.data, rgbImage_target .shape[1],rgbImage_target.shape[0],
                                           QImage.Format_RGB888)
                convertToQtFormat_user = QImage(rgbImage_user.data, rgbImage_user.shape[1],rgbImage_user.shape[0],QImage.Format_RGB888)

                p_target = convertToQtFormat_target.scaled(800, 448, Qt.KeepAspectRatio)
                p_user= convertToQtFormat_user.scaled(800, 448, Qt.KeepAspectRatio)


                self.target_pixmap_signal.emit(p_target)
                self.user_pixmap_signal.emit(p_user)
                self.scores.append(score)
                self.finished.emit(str(score))
            else:
                self.finished.emit("False")
        self.stop()

    def stop(self):
        self.cap_target.release()
        self.cap_user.release()
        # print(self.scores)
        # the_window = score_App(self.scores)
        # self.windowList.append(the_window)
        self.quit()




class Motion_ex_window(QMainWindow):
    def __init__(self,target_video,user_video =0,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_video = target_video
        self.user_video = user_video
        self.OP = Opnenpose()
        self.windowList = []
        self.scores = []
        self.initUI()


    def initUI(self):
        self.resize(1920, 1200)

        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_widget.setObjectName("main_widget")
        self.main_layout = QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  #
        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet('''#main_widget{border-image:url(./Ui_images/blackB.jpg);
                                           border-radius:30px}} ''')

        self.gif = QMovie("./Ui_images/2.gif")
        self.scorelabel = QLabel(self.main_widget)
        self.scorelabel.setGeometry(800, 700, 140, 70)
        self.scorelabel.setMovie(self.gif)
        self.gif.start()

        self.videoframe_target = QLabel(self.main_widget)
        self.videoframe_target.setGeometry(200, 200, 800, 448)

        self.videoframe_user = QLabel(self.main_widget)
        self.videoframe_user.setGeometry(1200, 200, 800, 448)

        self.scoreframe = QLabel(self.main_widget)
        self.scoreframe.setGeometry(965, 712, 150, 50)
        self.scoreframe.setAlignment(Qt.AlignVCenter)

        self.thread = VideoThread(self.target_video,self.user_video)
        self.thread.target_pixmap_signal.connect(self.setImage_target)
        self.thread.user_pixmap_signal.connect(self.setImage_user)
        self.thread.finished.connect(self.setscore)
        self.thread.start()

        self.show()

    def setImage_target(self, image):
        self.videoframe_target.setPixmap(QPixmap.fromImage(image))

    def setImage_user(self, image):
        self.videoframe_user.setPixmap(QPixmap.fromImage(image))

    def setscore(self,text):
        if text == "False":
            self.close()
        self.scoreframe.setStyleSheet("font: bold 50px;color:yellow")
        self.scoreframe.setText(str(text))
        if text != "False":
            self.scores.append(int(text))

    def closeEvent(self, event):
        self.thread.stop()
        the_window = score_App(self.scores)
        self.windowList.append(the_window)
        event.accept()



if __name__ == "__main__":
    mapp = QApplication(sys.argv)
    # mw = Motion_ex_window(r'Video/DustinJohnson/Front/DustinJohnson_Front.mp4',r'Video/CollinMorikawa/Front/CollinMorikawa_Front.mp4')
    mw = Motion_ex_window(r'Video/DustinJohnson/Front/DustinJohnson_Front.mp4', 'rtsp://admin:admin@10.246.67.213:8554/live')
    sys.exit(mapp.exec_())


