# coding:utf-8

# 导入matplotlib模块并使用Qt5Agg
import matplotlib

matplotlib.use('Qt5Agg')
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib.pyplot as plt
import sys
import numpy as np

#from MainUi import MainUi

from numpy import *

class score_App(QMainWindow):
    def __init__(self,scores, parent=None):
        # 父类初始化方法
        super(score_App, self).__init__(parent)
        self.scores = scores
        self.initUI()

    def initUI(self):
        # self.setWindowTitle()
        # 几个QWidgets
        self.resize(1920, 1200)

        self.main_widget = QWidget()  # 创建窗口主部件 // 기본 위젯 만들기
        self.main_widget.setObjectName("main_widget")   # 위젯 이름
        self.main_layout = QGridLayout()  # 创建主部件的网格布局  메인 화면 그리드 레이아웃 생성

        self.setCentralWidget(self.main_widget)
        self.main_widget.setStyleSheet('''#main_widget{border-image:url(./Ui_images/blackB.jpg);
                                           border-radius:30px}} ''')
        self.score_title = QLabel(self.main_widget)
        self.score_title.setGeometry(800, 50, 500, 200)
        self.score_title.setText("Golf swing Analysis")
        self.score_title.setStyleSheet('font-size: 40px;'
                                           'font-weight: 900;'
                                           'color: white;')
        self.scoreboard = QLabel(self.main_widget)
        self.scoreboard.setGeometry(500, 200, 1000, 700)
        self.scoreboard.setStyleSheet('font-size: 40px;'                                                                                     
                                      'font-weight: 900;'                                                                                    
                                      'color: white;')





        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        layout = QVBoxLayout(self.scoreboard)
        layout.addWidget(self.canvas)

        self.plot_()
        self.show()

    def plot_(self):
        ax = self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        # ax.clear()  # 每次绘制一个函数时清空绘图
        #x = linspace(-3, 3, 6000)
        # 使用了eval函数 점수 표시
        ax.plot([x for x in range(len(self.scores))],self.scores,label = "Score")
        ax.plot([x for x in range(len(self.scores))], [np.mean(self.scores)]*len(self.scores),c = "r",label = "Score mean")
        ax.legend(loc='lower right', fontsize=10)
        ax.set_ylabel('Scores')
        ax.set_xlabel('Frame')

        self.canvas.draw()


"""    def on_MainPage(self):
        the_window = MainUi()
        self.close()
        self.windowList.append(the_window)"""


# 运行程序 프로그램 실행
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = score_App([66,99,33,44,56])

    app.exec()
