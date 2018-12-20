from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets

# 枚举
from enum import Enum
# 路径
import os

# Ui
from Ui.WNRWidget import Ui_WNRWidget
# Log
from Utils.c_log_new import CLogNew
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


log = CLogNew().getlog()
class CWNRForm(QWidget, Ui_WNRWidget):
    def __init__(self):
        super(CWNRForm, self).__init__()
        self.setupUi(self)

        self.__m_tWNR = TWNR()

        self.__m_cAdb = CAdb()


    def PullWNR(self):
        """
        1、adb pull：有可能获取的是空文件，一直获取直到有效
        2、更新控件值：txt--->结构体--->控件
        """
        ret = False

        for i in range(PULL_NUM):
            strLog, ret = self.__m_cAdb.AdbPullDeviceTxt("wnrW")
            if ret == True:
                break

        if ret == True:
            log.info(strLog)   # DebugMK_Log
            log.info("Adb pull wnrW.txt succeed!")   # DebugMK_Log
            self.__UpdataTWNR()
        else:
            log.info(strLog)   # DebugMK_Log
            log.info("Adb pull wnrW.txt succeed!")   # DebugMK_Log


    def PushWNR(self):
        '''
        1、更新txt文件：控件--->结构体--->txt
        2、adb push
        '''
        ret = False

        self.__SetTWNR()

        strLog, ret = self.__m_cAdb.AdbPushDeviceTxt("wnr")

        if ret == True:
            log.info(strLog)   # DebugMK_Log
            log.info("Adb push wnrW.txt succeed!")   # DebugMK_Log
        else:
            log.info(strLog)   # DebugMK_Log
            log.info("Adb push wnrW.txt failed!")   # DebugMK_Log


    def __UpdataTWNR(self):
        '''txt--->结构体--->控件'''
        self.__ReadTWNR()

        for i in range(TWNR_NUMBER.WNR_NUM.value):
            if i <= TWNR_NUMBER.NOISE_PROFILE2.value:
                if i == 0:
                    self.findChild(QtWidgets.QTextBrowser, self.__WNRControlsLineNumber(i)).clear()

                strTmp = ''
                for j in range(WNR_VALUE_NUM):
                    strTmp += (('%.6f' % self.__GetTWNRLineNumber(i)[j]) + "f, ")

                self.findChild(QtWidgets.QTextBrowser, self.__WNRControlsLineNumber(i)).append(strTmp)
            else:
                for j in range(WNR_VALUE_NUM):
                    strTmp = ('%.6f' % self.__GetTWNRLineNumber(i)[j])
                    self.findChild(QtWidgets.QLineEdit, self.__WNRControlsLineNumber(i) + str(j)).setText(strTmp)


    def __SetTWNR(self):
        '''控件--->结构体--->txt'''
        for i in range(TWNR_NUMBER.WNR_NUM.value):
            # NoiseProfile直接以行为单位处理
            if i <= TWNR_NUMBER.NOISE_PROFILE2.value:
                listTmp = self.findChild(QtWidgets.QTextBrowser, self.__WNRControlsLineNumber(i)).toPlainText().\
                    split('\n')[i].split('f, ')
                listTmp = [float(x) for x in listTmp if x != '']

                self.__SetTWNRLineNumber(i, listTmp)
            else:
                for j in range(WNR_VALUE_NUM):
                    floatTmp = float(self.findChild(QtWidgets.QLineEdit, self.__WNRControlsLineNumber(i) + str(j)).text())
                    self.__GetTWNRLineNumber(i)[j] = float(floatTmp)

        self.__WriteTWNR()


    def __ReadTWNR(self):
        # listData以行为元素的列表
        strFilesPath = os.getcwd() + "\\Files\\wnrW.txt"

        listData = Utils.python_txt.txtRead(strFilesPath).split()
        log.info(str(listData))   # DebugMK_Log

        for i in range(TWNR_NUMBER.WNR_NUM.value):
            listTmp = listData[i].split(',')
            listTmp = [float(x) for x in listTmp]
            self.__SetTWNRLineNumber(i, listTmp)


    def __WriteTWNR(self):
        strData = ""
        for i in range(TWNR_NUMBER.WNR_NUM.value):
            for j in range(len(self.__GetTWNRLineNumber(i))):
                strData += str(self.__GetTWNRLineNumber(i)[j])

                if j != (len(self.__GetTWNRLineNumber(i)) - 1):
                    strData += ','

            strData += '\n'
        log.info(strData)   # DebugMK_Log

        strFilesPath = os.getcwd() + "\\Files\\wnr.txt"
        Utils.python_txt.txtWrite(strFilesPath, strData)


    ################################################################################
    def __GetTWNRLineNumber(self, i):
        if i == TWNR_NUMBER.NOISE_PROFILE0.value:
            return self.__m_tWNR.NoiseProfile0
        elif i == TWNR_NUMBER.NOISE_PROFILE1.value:
            return self.__m_tWNR.NoiseProfile1
        elif i == TWNR_NUMBER.NOISE_PROFILE2.value:
            return self.__m_tWNR.NoiseProfile2
        elif i == TWNR_NUMBER.SCALE_Y.value:
            return self.__m_tWNR.Scale_Y
        elif i == TWNR_NUMBER.SCALE_CHROMA.value:
            return self.__m_tWNR.Scale_Chroma
        elif i == TWNR_NUMBER.EDGES_Y.value:
            return self.__m_tWNR.EdgeS_Y
        elif i == TWNR_NUMBER.EDGES_CHROMA.value:
            return self.__m_tWNR.EdgeS_Chroma
        elif i == TWNR_NUMBER.WEIGHT_Y.value:
            return self.__m_tWNR.Weight_Y
        elif i == TWNR_NUMBER.WEIGHT_CHROMA.value:
            return self.__m_tWNR.Weight_Chroma
        else:
            pass

    def __SetTWNRLineNumber(self, i, list):
        if i == TWNR_NUMBER.NOISE_PROFILE0.value:
            self.__m_tWNR.NoiseProfile0 = list
        elif i == TWNR_NUMBER.NOISE_PROFILE1.value:
            self.__m_tWNR.NoiseProfile1 = list
        elif i == TWNR_NUMBER.NOISE_PROFILE2.value:
            self.__m_tWNR.NoiseProfile2 = list
        elif i == TWNR_NUMBER.SCALE_Y.value:
            self.__m_tWNR.Scale_Y = list
        elif i == TWNR_NUMBER.SCALE_CHROMA.value:
            self.__m_tWNR.Scale_Chroma = list
        elif i == TWNR_NUMBER.EDGES_Y.value:
            self.__m_tWNR.EdgeS_Y = list
        elif i == TWNR_NUMBER.EDGES_CHROMA.value:
            self.__m_tWNR.EdgeS_Chroma = list
        elif i == TWNR_NUMBER.WEIGHT_Y.value:
            self.__m_tWNR.Weight_Y = list
        elif i == TWNR_NUMBER.WEIGHT_CHROMA.value:
            self.__m_tWNR.Weight_Chroma = list
        else:
            pass

    def __WNRControlsLineNumber(self, i):
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








