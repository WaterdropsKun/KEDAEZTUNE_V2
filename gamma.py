from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QPixmap
from PyQt5.QtCore import Qt

import cv2

# 路径
import os

# Ui
from Ui.GammaWidget import Ui_GammaWidget
# types
from Utils.KEDAEZTUNE_types import *
# Log
from Utils.c_log_new import CLogNew
# adb
from adb import CAdb, ADB_COMMAND
# txt
import Utils.python_txt
# 曲线
from Utils.c_spline import CSpline


class TGAMMA:
    def __init__(self):
        self.BGamma32 = []
        self.NGamma32 = []
        self.LGamma32 = []
        self.Gamma32 = []
        self.Gamma64 = []


log = CLogNew().getlog()
class CGammaForm(QWidget, Ui_GammaWidget):
    def __init__(self):
        super(CGammaForm, self).__init__()
        self.setupUi(self)

        self.__PointsList = []                                                    # 存放读取的Gamma曲线（下采样32点+首尾2点）
        self.__DragPointsList = [Point(0, 512), Point(256, 256), Point(512, 0)]   # 存放拖拽的Gamma曲线

        self.__bPaintFlag = True     # 左键按下开始绘制，弹起结束绘制，减少绘制次数
        self.__bDragFlag = False     # 拖拽曲线标志位
        self.__nDragPointIndex = 0   # 实时拖拽点在点集中的序号

        self.__qPixmap = QPixmap(512, 512)   # 画布

        self.__cSpline = CSpline()

        self.__m_tGAMMA = TGAMMA()

        self.__m_cAdb = CAdb()

        self.Init()


    def paintEvent(self, event):
        if self.__bPaintFlag:
            ###
            self.__qPixmap.fill(Qt.white)

            qPainter = QPainter(self.__qPixmap)
            qPainter.begin(self.__qPixmap)

            # Draw box
            size = self.label.size()
            Height = size.height() - 1
            Width = size.width() - 1
            qPen = QPen(Qt.black, 1, Qt.SolidLine)
            qPainter.setPen(qPen)
            qPainter.drawLine(0, 0, 0, Height)
            qPainter.drawLine(0, Height, Width, Height)
            qPainter.drawLine(Width, Height, Width, 0)
            qPainter.drawLine(Width, 0, 0, 0)

            # 画Gamma曲线
            qPainter.setPen(Qt.black)   # qPainter.setPen(QColor(168, 34, 3))
            self.__cSpline.DataPointsListSet(self.__PointsList)
            SplinePointsList = self.__cSpline.SplinePointsListGet()
            nPointNum = len(SplinePointsList) - 1
            for i in range(nPointNum):
                qPainter.drawLine(SplinePointsList[i].x, SplinePointsList[i].y,
                                  SplinePointsList[i + 1].x, SplinePointsList[i + 1].y)
            # 画拖拽曲线
            qPainter.setPen(Qt.red)
            self.__cSpline.DataPointsListSet(self.__DragPointsList)
            SplinePointsList = self.__cSpline.SplinePointsListGet()
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

            # 画布保存成图片
            self.label.setPixmap(self.__qPixmap)
            self.__qPixmap.save(os.getcwd() + "\\Files\\result.png")


    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            x = QMouseEvent.x()
            y = QMouseEvent.y()

            # 判断拖拽点横坐标16*16范围是否有点击点，如没有，以插入点为拖拽点
            for i in range(1, len(self.__DragPointsList)):
                if x > self.__DragPointsList[i-1].x + 8 and x < self.__DragPointsList[i].x - 8 and y > 0 and y < self.height():
                    self.__DragPointsList.insert(i, Point(x, y))
                    self.__bDragFlag = True
                    self.__nDragPointIndex = i
                    self.update()
            # 判断点击点16*16范围是否有拖拽点，如有，以原来点作为拖拽点
            for i in range(0, len(self.__DragPointsList)):
                if self.__DragPointsList[i].x > x - 8 and self.__DragPointsList[i].x < x + 8 and self.__DragPointsList[i].y > y - 8 and self.__DragPointsList[i].y < y + 8:
                    self.__bDragFlag = True
                    self.__nDragPointIndex = i

            self.__bPaintFlag = True


    def mouseReleaseEvent(self, QMouseEvent):
        if self.__bDragFlag:
            self.__bDragFlag = False

        if self.__bPaintFlag:
            self.__bPaintFlag = False


    def mouseMoveEvent(self, QMouseEvent):
        x = QMouseEvent.x()
        y = QMouseEvent.y()

        # 实时更新拖拽点或合并拖拽点
        if self.__bDragFlag and self.__nDragPointIndex > 0 and self.__nDragPointIndex < len(self.__PointsList) - 1:
            if x > self.__DragPointsList[self.__nDragPointIndex - 1].x + 8 and x < self.__DragPointsList[self.__nDragPointIndex + 1].x - 8:
                self.__DragPointsList[self.__nDragPointIndex] = Point(x, y)
            else:
                del self.__DragPointsList[self.__nDragPointIndex]
                self.__bDragFlag = False
                self.update()
        # 首尾拖拽点更新
        if self.__bDragFlag and self.__nDragPointIndex == 0 and x < self.__PointsList[1].x - 20:
            self.__DragPointsList[0] = Point(x, y)
        if self.__bDragFlag and self.__nDragPointIndex == len(self.__PointsList) - 1 and x > self.__PointsList[len(self.__PointsList) - 2].x + 20:
            self.__DragPointsList[self.__nDragPointIndex] = Point(x, y)

        if self.__bDragFlag:
            self.update()


    ############################################################
    def Init(self):
        self.PullGAMMA()


    def BrightClicked(self):
        self.UpdataTGAMMA()

    def NormalClicked(self):
        self.UpdataTGAMMA()

    def LowClicked(self):
        self.UpdataTGAMMA()


    def PullGAMMA(self):
        """
        1、adb pull：有可能获取的是空文件，一直获取直到有效
        2、更新控件值：txt--->结构体--->控件
        """
        ret = False

        for i in range(PULL_NUM):
            if self.rbCamera0.isChecked():
                strLog, ret = self.__m_cAdb.AdbPullDeviceTxt("run512GammaW")
            elif self.rbCamera1.isChecked():
                strLog, ret = self.__m_cAdb.AdbPullDeviceTxt("run512GammaW_2")
            if ret == True:
                break

        if ret == True:
            log.info(strLog)   # DebugMK_Log
            log.info("Adb pull wnrW.txt succeed!")   # DebugMK_Log
            self.UpdataTGAMMA()
        else:
            log.info(strLog)   # DebugMK_Log
            log.info("Adb pull wnrW.txt failed!")   # DebugMK_Log


    def PushGAMMA(self):
        '''
        1、更新txt文件：Gamma曲线图片--->结构体--->txt
        2、adb push
        '''
        ret = False

        self.SetTGAMMA()

        strLog, ret = self.__m_cAdb.AdbPushDeviceTxt("runGamma")

        if ret == True:
            log.info(strLog)   # DebugMK_Log
            log.info("Adb push runGamma.txt succeed!")   # DebugMK_Log
        else:
            log.info(strLog)   # DebugMK_Log
            log.info("Adb push runGamma.txt failed!")   # DebugMK_Log


    def UpdataTGAMMA(self):
        '''txt--->结构体--->控件'''
        self.ReadTGAMMA()

        # Choose Gamma curve
        if self.rbBright.isChecked():
            self.__m_tGAMMA.Gamma32 = self.__m_tGAMMA.BGamma32
        elif self.rbNormal.isChecked():
            self.__m_tGAMMA.Gamma32 = self.__m_tGAMMA.NGamma32
        elif self.rbLow.isChecked():
            self.__m_tGAMMA.Gamma32 = self.__m_tGAMMA.LGamma32

        self.__PointsList = []
        self.__PointsList.append(Point(0, 512))
        for i in range(32):
            self.__PointsList.append(Point(i * 16, (255 - self.__m_tGAMMA.Gamma32[i]) * 2))
        self.__PointsList.append(Point(512, 0))

        self.__bPaintFlag = True   # 更新即绘图


    def SetTGAMMA(self):
        '''Gamma曲线图片--->结构体--->txt'''
        self.__bPaintFlag = False   # 关闭绘制和保存Gamma曲线
        matImg = cv2.imread(os.getcwd() + "\\Files\\result.png")
        nImgHeight = matImg.shape[0]
        nImgWidth = matImg.shape[1]
        nChannels = matImg.shape[2]

        self.__m_tGAMMA.Gamma64 = []
        self.__m_tGAMMA.Gamma64.append(0)   # 第0列可能出现检测不到红色
        for i in range(1, 64):
            x = i * 8
            for y in range(nImgHeight):
                (b, g, r) = matImg[y, x]
                if b == 0 and g == 0 and r == 255:
                    self.__m_tGAMMA.Gamma64.append((int)((511 - y) / 2))
                    print(x, self.__m_tGAMMA.Gamma64[i])  ###
                    break

        self.WriteTGAMMA()
        # 显示Gamma曲线
        # cv2.imshow("Gamma", matImg)


    def ReadTGAMMA(self):
        if self.rbCamera0.isChecked():
            strFilesPath = os.getcwd() + "\\Files\\run512GammaW.txt"
        elif self.rbCamera1.isChecked():
            strFilesPath = os.getcwd() + "\\Files\\run512GammaW_2.txt"

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

        self.__m_tGAMMA.BGamma32 = self.DownSamplePoints(BGamma512)
        self.__m_tGAMMA.NGamma32 = self.DownSamplePoints(NGamma512)
        self.__m_tGAMMA.LGamma32 = self.DownSamplePoints(LGamma512)


    def WriteTGAMMA(self):
        strData = ""
        for i in range(8):
            for j in range(8):
                strData += str(self.__m_tGAMMA.Gamma64[i * 8 + j])
                if j != 7:
                    strData += ','
            strData += '\n'

        strFilesPath = os.getcwd() + "\\Files\\runGamma.txt"
        Utils.python_txt.txtWrite(strFilesPath, strData)


    def DownSamplePoints(self, PointsList):
        Gamma32 = []
        if 512 == len(PointsList):
            for i in range(32):
                Gamma32.append(PointsList[i*16] >> 6)

        return Gamma32








