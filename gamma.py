from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt

# 路径
import os

from Ui.GammaWidget import Ui_GammaWidget

# types
from Utils.KEDAEZTUNE_types import *
# Log
from Utils.c_log import CLog
# txt
import Utils.python_txt


class CGammaForm(QWidget, Ui_GammaWidget):
    def __init__(self):
        super(CGammaForm, self).__init__()
        self.setupUi(self)

        self.PointsList = []

        self.__cLog = CLog()

        self.ReadTGamma()


    def paintEvent(self, event):
        qPainter = QPainter(self)
        qPainter.begin(self)

        # Draw box
        size = self.size()
        print(size)
        Height = size.height() - 1
        Width = size.width() - 1
        qPen = QPen(Qt.black, 1, Qt.SolidLine)
        qPainter.setPen(qPen)
        qPainter.drawLine(0, 0, 0, Height)
        qPainter.drawLine(0, Height, Width, Height)
        qPainter.drawLine(Width, Height, Width, 0)
        qPainter.drawLine(Width, 0, 0, 0)

        # qPainter.setPen(QColor(168, 34, 3))
        qPainter.setPen(Qt.red)
        qPainter.setBrush(Qt.red)
        nPointNum = len(self.PointsList) - 1
        for i in range(nPointNum):
            qPainter.drawEllipse(self.PointsList[i].x, self.PointsList[i].y, 5, 5)
            qPainter.drawLine(self.PointsList[i].x, self.PointsList[i].y,
                              self.PointsList[i + 1].x, self.PointsList[i + 1].y)

        qPainter.end()


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print("鼠标按下事件_左键")
            x = QMouseEvent.x()
            y = QMouseEvent.y()
            self.PointsList.append(Point(x, y))
            self.update()

        elif QMouseEvent.button() == Qt.RightButton:
            print("鼠标按下事件_右键")

        elif QMouseEvent.button() == Qt.MidButton:
            print("鼠标按下事件_点击滚轮")
            self.PointsList = []
            self.update()


    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print("鼠标释放事件_左键")
        elif QMouseEvent.button() == Qt.RightButton:
            print("鼠标释放事件_右键")
        elif QMouseEvent.button() == Qt.MidButton:
            print("鼠标释放事件_点击滚轮")

    def mouseMoveEvent(self, QMouseEvent):
        print("鼠标移动事件")
        x = QMouseEvent.x()
        y = QMouseEvent.y()
        self.PointsList.append(Point(x, y))
        self.update()


    ############################################################
    def ReadTGamma(self):
        self.__cLog.LogClear()

        strFilesPath = os.getcwd() + "\\Files\\run512GammaW.txt"

        listData = Utils.python_txt.txtRead(strFilesPath).split('|')

        BGamma512 = []
        BGamma512Tmp = listData[0].split('\n')
        for i in range(len(BGamma512Tmp)):
            BGamma512Line = BGamma512Tmp[i].split(',')
            BGamma512Line = [int(x) for x in BGamma512Line if x != '']
            BGamma512.extend(BGamma512Line)

        NGamma512 = []
        NGamma512Tmp = listData[1].split('\n')
        for i in range(len(NGamma512Tmp)):
            NGamma512Line = NGamma512Tmp[i].split(',')
            NGamma512Line = [int(x) for x in NGamma512Line if x != '']
            NGamma512.extend(NGamma512Line)

        LGamma512 = []
        LGamma512Tmp = listData[2].split('\n')
        for i in range(len(LGamma512Tmp)):
            LGamma512Line = LGamma512Tmp[i].split(',')
            LGamma512Line = [int(x) for x in LGamma512Line if x != '']
            LGamma512.extend(LGamma512Line)

        BGamma32 = self.DownSamplePoints(LGamma512)
        print(BGamma32)  ###
        self.PointsList.append(Point(0, 512))
        for i in range(32):
            self.PointsList.append(Point(i * 16, (255 - BGamma32[i]) * 2))
        self.PointsList.append(Point(512, 0))

        return self.__cLog.GetLog()


    def DownSamplePoints(self, PointsList):
        Gamma32 = []

        if 512 == len(PointsList):
            for i in range(32):
                Gamma32.append(PointsList[i*16] >> 6)

        return Gamma32








