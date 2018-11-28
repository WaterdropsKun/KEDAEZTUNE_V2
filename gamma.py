from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap
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
# 曲线
from Utils.c_spline import CSpline


class CGammaForm(QWidget, Ui_GammaWidget):
    def __init__(self):
        super(CGammaForm, self).__init__()
        self.setupUi(self)

        self.__PointsList = []
        self.__DragPointsList = [Point(0, 512), Point(256, 256), Point(512, 0)]

        self.__bDragFlag = False
        self.__nDragPointIndex = 0

        self.__cLog = CLog()

        self.ReadTGamma()

        ###
        self.__qPixmap = QPixmap(512, 512)
        self.__qPixmap.fill(Qt.white)


    def paintEvent(self, event):
        ###
        self.__qPixmap.fill(Qt.white)

        qPainter = QPainter(self.__qPixmap)
        qPainter.begin(self.__qPixmap)

        # Draw box
        size = self.size()
        Height = size.height() - 1
        Width = size.width() - 1
        qPen = QPen(Qt.black, 1, Qt.SolidLine)
        qPainter.setPen(qPen)
        qPainter.drawLine(0, 0, 0, Height)
        qPainter.drawLine(0, Height, Width, Height)
        qPainter.drawLine(Width, Height, Width, 0)
        qPainter.drawLine(Width, 0, 0, 0)

        cSpline = CSpline()
        # 画Gamma曲线
        qPainter.setPen(Qt.black)   # qPainter.setPen(QColor(168, 34, 3))
        cSpline.DataPointsListSet(self.__PointsList)
        SplinePointsList = cSpline.SplinePointsListGet()
        nPointNum = len(SplinePointsList) - 1
        for i in range(nPointNum):
            qPainter.drawLine(SplinePointsList[i].x, SplinePointsList[i].y,
                              SplinePointsList[i + 1].x, SplinePointsList[i + 1].y)
        # 画拖拽曲线
        qPainter.setPen(Qt.red)
        cSpline.DataPointsListSet(self.__DragPointsList)
        SplinePointsList = cSpline.SplinePointsListGet()
        nPointNum = len(SplinePointsList) - 1
        for i in range(nPointNum):
            qPainter.drawLine(SplinePointsList[i].x, SplinePointsList[i].y,
                              SplinePointsList[i + 1].x, SplinePointsList[i + 1].y)
        # 标记拖拽点
        qPainter.setBrush(Qt.red)
        nPointNum = len(self.__DragPointsList) - 1
        for i in range(nPointNum):
            qPainter.drawEllipse(self.__DragPointsList[i].x, self.__DragPointsList[i].y, 3, 3)

        qPainter.end()

        ###
        self.label.setPixmap(self.__qPixmap)
        self.__qPixmap.save(os.getcwd() + "\\Files\\result.png")


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            print("鼠标按下事件_左键")

            x = QMouseEvent.x()
            y = QMouseEvent.y()

            for i in range(1, len(self.__DragPointsList)):
                if x > self.__DragPointsList[i-1].x + 8 and x < self.__DragPointsList[i].x - 8 and y > 0 and y < self.height():
                    self.__DragPointsList.insert(i, Point(x, y))
                    self.__bDragFlag = True
                    self.__nDragPointIndex = i
                    self.update()
            # 判断点击点16*16范围是否有拖拽点
            for i in range(0, len(self.__DragPointsList)):
                if self.__DragPointsList[i].x > x - 8 and self.__DragPointsList[i].x < x + 8 and self.__DragPointsList[i].y > y - 8 and self.__DragPointsList[i].y < y + 8:
                    self.__bDragFlag = True
                    self.__nDragPointIndex = i


    def mouseReleaseEvent(self, QMouseEvent):
        if self.__bDragFlag:
            self.__bDragFlag = False


    def mouseMoveEvent(self, QMouseEvent):
        print("鼠标移动事件")
        x = QMouseEvent.x()
        y = QMouseEvent.y()

        if self.__bDragFlag and self.__nDragPointIndex > 0 and self.__nDragPointIndex < len(self.__PointsList) - 1:
            if x > self.__DragPointsList[self.__nDragPointIndex - 1].x + 8 and x < self.__DragPointsList[self.__nDragPointIndex + 1].x - 8:
                self.__DragPointsList[self.__nDragPointIndex] = Point(x, y)
            else:
                del self.__DragPointsList[self.__nDragPointIndex]
                self.__bDragFlag = False
                self.update()

        if self.__bDragFlag and self.__nDragPointIndex == 0 and x < self.__PointsList[1].x - 20:
            self.__DragPointsList[0] = Point(x, y)

        if self.__bDragFlag and self.__nDragPointIndex == len(self.__PointsList) - 1 and x > self.__PointsList[len(self.__PointsList) - 2].x + 20:
            self.__DragPointsList[self.__nDragPointIndex] = Point(x, y)

        if self.__bDragFlag:
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


        BGamma32 = self.DownSamplePoints(BGamma512)
        print(BGamma32)   ###
        self.__PointsList.append(Point(0, 512))
        for i in range(32):
            self.__PointsList.append(Point(i * 16, (255 - BGamma32[i]) * 2))
        self.__PointsList.append(Point(512, 0))

        return self.__cLog.GetLog()


    def DownSamplePoints(self, PointsList):
        Gamma32 = []

        if 512 == len(PointsList):
            for i in range(32):
                Gamma32.append(PointsList[i*16] >> 6)

        return Gamma32








