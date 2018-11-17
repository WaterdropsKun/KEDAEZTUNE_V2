# 枚举
from enum import Enum
# adb
import subprocess
# 路径
import os

# Log
from Utils.c_log import CLog


class ADB_COMMAND(Enum):
    NONE_CMD = 0
    WNR_CMD = 1


class CAdb(object):
    def __init__(self):
        self.__cLog = CLog()


    def AdbConnectDevice(self, strDeviceIP):
        '''
        1、根据adb connect返回值中是否存在"connected"字符串
        2、根据adb devices返回值中是否存在设备ip
        3、1 && 2
        '''
        self.__cLog.LogClear()

        bAdbConnectDeviceFlag = False

        strAdbCmd = "adb connect " + strDeviceIP
        self.__cLog.LogAppend(strAdbCmd)  # DebugMK
        ret = subprocess.Popen(strAdbCmd,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()
        self.__cLog.LogAppend(str(ret))  # DebugMK

        ret = str(ret[0], encoding='utf-8')
        if ret.find("connected") != -1:
            strAdbCmd = "adb devices"
            self.__cLog.LogAppend(strAdbCmd)  # DebugMK
            ret = subprocess.Popen(strAdbCmd,
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE).communicate()
            self.__cLog.LogAppend(str(ret))  # DebugMK

            ret = str(ret[0], encoding='utf-8')
            if ret.find(strDeviceIP) != -1:
                bAdbConnectDeviceFlag = True

        return self.__cLog.GetLog(), bAdbConnectDeviceFlag


    def AdbPullDeviceTxt(self, strFilename):
        '''
        1、根据adb pull返回值中是否存在(b'23 KB/s (336 bytes in 0.014s)\r\n')
        '''
        self.__cLog.LogClear()

        bAdbPullDeviceTxtFlag = False

        strFilesPath = os.getcwd() + "\\Files"
        strAdbCmd = "adb pull /data/effectFile/" + strFilename + ".txt " + strFilesPath
        self.__cLog.LogAppend(strAdbCmd)  # DebugMK
        ret = subprocess.Popen(strAdbCmd,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()
        self.__cLog.LogAppend(str(ret))  # DebugMK

        ret = str(ret[1], encoding='utf-8')
        if ret.find("KB") != -1:
            bAdbPullDeviceTxtFlag = True

        return self.__cLog.GetLog(), bAdbPullDeviceTxtFlag


    def AdbPushDeviceTxt(self, strFilename):
        '''
        1、根据adb push返回值中是否存在(b'23 KB/s (336 bytes in 0.014s)\r\n')
        '''
        self.__cLog.LogClear()

        bAdbPushDeviceTxtFlag = False

        strFilesPath = os.getcwd() + "\\Files"
        strAdbCmd = "adb push " + strFilesPath + "\\" + strFilename + ".txt " + "/data/effectFile"
        self.__cLog.LogAppend(strAdbCmd + '\n')  # DebugMK
        ret = subprocess.Popen(strAdbCmd,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()
        self.__cLog.LogAppend(str(ret))  # DebugMK

        ret = str(ret[1], encoding='utf-8')
        if ret.find("KB") != -1:
            bAdbPushDeviceTxtFlag = True

        return self.__cLog.GetLog(), bAdbPushDeviceTxtFlag


    def AdbCommand(self, enumAdbCommand):
        self.__cLog.LogClear()

        bAdbCommandFlag = False

        strAdbCommand = "adb shell setprop persist.kedaEzTune.enable " + str(enumAdbCommand.value)
        ret = subprocess.Popen(strAdbCommand,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()
        self.__cLog.LogAppend(str(ret))  # DebugMK

        strAdbCommand = "adb shell getprop persist.kedaEzTune.enable"
        ret = subprocess.Popen(strAdbCommand,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE).communicate()
        self.__cLog.LogAppend(str(ret))  # DebugMK

        if ret[0] != b'':
            if int(ret[0]) == enumAdbCommand.value:
                bAdbCommandFlag = True

        return self.__cLog.GetLog(), bAdbCommandFlag

