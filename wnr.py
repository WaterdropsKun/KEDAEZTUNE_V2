from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets

# 枚举
from enum import Enum
# 路径
import os

# Ui
from Ui.WNRWidget import Ui_WNRWidget
# Log
from Utils.c_log import CLog
from Utils.c_logger import Logger
# adb
from adb import CAdb, ADB_COMMAND
# txt
import Utils.python_txt


class TWNR_NUMBER(Enum):
    '''枚举：TWNR结构体对应txt文件的行数'''
    NOISE_PROFILE0 = 0
    NOISE_PROFILE1 = 1
    NOISE_PROFILE2 = 2
    SCALE_Y = 3
    SCALE_CHROMA = 4
    EDGES_Y = 5
    EDGES_CHROMA = 6
    WEIGHT_Y = 7
    WEIGHT_CHROMA = 8

    WNR_NUM = 9

class TWNR:
    def __init__(self):
        self.NoiseProfile0 = []
        self.NoiseProfile1 = []
        self.NoiseProfile2 = []
        self.Scale_Y = []
        self.Scale_Chroma = []
        self.EdgeS_Y = []
        self.EdgeS_Chroma = []
        self.Weight_Y = []
        self.Weight_Chroma = []

# adb通讯次数
PULL_NUM = 10
# txt每行参数4个
WNR_VALUE_NUM = 4


log = Logger().getlog()
class CWNRForm(QWidget, Ui_WNRWidget):
    def __init__(self):
        super(CWNRForm, self).__init__()
        self.setupUi(self)

        self.m_tWNR = TWNR()

        self.__cLog = CLog()
        self.__cAdb = CAdb()


    def PullWNR(self):
        '''
        1、adb pull有可能获取的是空文件，一直获取直到有效
        2、更新控件值
        '''
        self.__cLog.LogClear()

        ret = False

        for i in range(PULL_NUM):
            strLog, ret = self.__cAdb.AdbPullDeviceTxt("wnrW")
            if ret == True:
                break

        if ret == True:
            self.__cLog.LogAppend(strLog)   # DebugMK
            self.__cLog.LogAppend("Adb pull wnrW.txt succeed!")  # DebugMK
            self.__UpdataTWNR()
        else:
            self.__cLog.LogAppend(strLog)   # DebugMK
            self.__cLog.LogAppend("Adb pull wnrW.txt failed!")  # DebugMK

        print(self.__cLog.GetLog())   # DebugMK
        log.info(self.__cLog.GetLog())
        return self.__cLog.GetLog()


    def PushWNR(self):
        '''
        1、跟新结构体，写入txt
        2、adb push
        '''
        self.__cLog.LogClear()

        self.__SetTWNR()

        strLog, ret = self.__cAdb.AdbPushDeviceTxt("wnr")

        if ret == True:
            self.__cLog.LogAppend(strLog)  # DebugMK
            self.__cLog.LogAppend("Adb push wnrW.txt succeed!")  # DebugMK
        else:
            self.__cLog.LogAppend(strLog)  # DebugMK
            self.__cLog.LogAppend("Adb push wnrW.txt failed!")  # DebugMK


    def __UpdataTWNR(self):
        '''txt--->结构体--->控件'''
        print(self.__cLog.GetLog())  # DebugMK
        self.__cLog.LogClear()

        strLog = self.__ReadTWNR()
        self.__cLog.LogAppend(strLog)

        for i in range(TWNR_NUMBER.WNR_NUM.value):
            if i <= TWNR_NUMBER.NOISE_PROFILE2.value:
                if i == 0:
                    self.findChild(QtWidgets.QTextBrowser, self.WNRControlsLineNumber(i)).clear()

                strTmp = ''
                for j in range(WNR_VALUE_NUM):
                    strTmp += (('%.6f' % self.GetTWNRLineNumber(i)[j]) + "f, ")

                self.findChild(QtWidgets.QTextBrowser, self.WNRControlsLineNumber(i)).append(strTmp)
            else:
                for j in range(WNR_VALUE_NUM):
                    strTmp = ('%.6f' % self.GetTWNRLineNumber(i)[j])
                    self.findChild(QtWidgets.QLineEdit, self.WNRControlsLineNumber(i)+str(j)).setText(strTmp)

        return self.__cLog.GetLog()


    def __SetTWNR(self):
        '''控件--->结构体--->txt'''
        print(self.__cLog.GetLog())  # DebugMK
        self.__cLog.LogClear()

        for i in range(TWNR_NUMBER.WNR_NUM.value):
            # NoiseProfile直接以行为单位处理
            if i <= TWNR_NUMBER.NOISE_PROFILE2.value:
                listTmp = self.findChild(QtWidgets.QTextBrowser, self.WNRControlsLineNumber(i)).toPlainText().\
                    split('\n')[i].split('f, ')
                listTmp = [float(x) for x in listTmp if x != '']

                self.SetTWNRLineNumber(i, listTmp)
            else:
                for j in range(WNR_VALUE_NUM):
                    floatTmp = float(self.findChild(QtWidgets.QLineEdit, self.WNRControlsLineNumber(i)+str(j)).text())
                    self.GetTWNRLineNumber(i)[j] = float(floatTmp)

        strLog = self.__WriteTWNR()
        self.__cLog.LogAppend(strLog)

        return self.__cLog.GetLog()


    def __ReadTWNR(self):
        print(self.__cLog.GetLog())  # DebugMK
        self.__cLog.LogClear()

        # listData以行为元素的列表
        strFilesPath = os.getcwd() + "\\Files\\wnrW.txt"

        listData = Utils.python_txt.txtRead(strFilesPath).split()
        self.__cLog.LogAppend(str(listData))

        for i in range(TWNR_NUMBER.WNR_NUM.value):
            listTmp = listData[i].split(',')
            listTmp = [float(x) for x in listTmp]
            self.SetTWNRLineNumber(i, listTmp)

        return self.__cLog.GetLog()

    def __WriteTWNR(self):
        print(self.__cLog.GetLog())  # DebugMK
        self.__cLog.LogClear()

        strData = ""
        for i in range(TWNR_NUMBER.WNR_NUM.value):
            for j in range(len(self.GetTWNRLineNumber(i))):
                strData += str(self.GetTWNRLineNumber(i)[j])

                if j != (len(self.GetTWNRLineNumber(i))-1):
                    strData += ','

            strData += '\n'
        self.__cLog.LogAppend(strData)

        strFilesPath = os.getcwd() + "\\Files\\wnr.txt"
        Utils.python_txt.txtWrite(strFilesPath, strData)

        return self.__cLog.GetLog()


    ################################################################################
    def GetTWNRLineNumber(self, i):
        if i == TWNR_NUMBER.NOISE_PROFILE0.value:
            return self.m_tWNR.NoiseProfile0
        elif i == TWNR_NUMBER.NOISE_PROFILE1.value:
            return self.m_tWNR.NoiseProfile1
        elif i == TWNR_NUMBER.NOISE_PROFILE2.value:
            return self.m_tWNR.NoiseProfile2
        elif i == TWNR_NUMBER.SCALE_Y.value:
            return self.m_tWNR.Scale_Y
        elif i == TWNR_NUMBER.SCALE_CHROMA.value:
            return self.m_tWNR.Scale_Chroma
        elif i == TWNR_NUMBER.EDGES_Y.value:
            return self.m_tWNR.EdgeS_Y
        elif i == TWNR_NUMBER.EDGES_CHROMA.value:
            return self.m_tWNR.EdgeS_Chroma
        elif i == TWNR_NUMBER.WEIGHT_Y.value:
            return self.m_tWNR.Weight_Y
        elif i == TWNR_NUMBER.WEIGHT_CHROMA.value:
            return self.m_tWNR.Weight_Chroma
        else:
            pass

    def SetTWNRLineNumber(self, i, list):
        if i == TWNR_NUMBER.NOISE_PROFILE0.value:
            self.m_tWNR.NoiseProfile0 = list
        elif i == TWNR_NUMBER.NOISE_PROFILE1.value:
            self.m_tWNR.NoiseProfile1 = list
        elif i == TWNR_NUMBER.NOISE_PROFILE2.value:
            self.m_tWNR.NoiseProfile2 = list
        elif i == TWNR_NUMBER.SCALE_Y.value:
            self.m_tWNR.Scale_Y = list
        elif i == TWNR_NUMBER.SCALE_CHROMA.value:
            self.m_tWNR.Scale_Chroma = list
        elif i == TWNR_NUMBER.EDGES_Y.value:
            self.m_tWNR.EdgeS_Y = list
        elif i == TWNR_NUMBER.EDGES_CHROMA.value:
            self.m_tWNR.EdgeS_Chroma = list
        elif i == TWNR_NUMBER.WEIGHT_Y.value:
            self.m_tWNR.Weight_Y = list
        elif i == TWNR_NUMBER.WEIGHT_CHROMA.value:
            self.m_tWNR.Weight_Chroma = list
        else:
            pass

    def WNRControlsLineNumber(self, i):
        if i <= TWNR_NUMBER.NOISE_PROFILE2.value:
            return "NoiseProfile"
        elif i == TWNR_NUMBER.SCALE_Y.value:
            return "Scale_Y"
        elif i == TWNR_NUMBER.SCALE_CHROMA.value:
            return "Scale_Chroam"
        elif i == TWNR_NUMBER.EDGES_Y.value:
            return "EdgeS_Y"
        elif i == TWNR_NUMBER.EDGES_CHROMA.value:
            return "EdgeS_Chroma"
        elif i == TWNR_NUMBER.WEIGHT_Y.value:
            return "Weight_Y"
        elif i == TWNR_NUMBER.WEIGHT_CHROMA.value:
            return "Weight_Chroma"
        else:
            pass








