# 打印函数名
import inspect

class CLog(object):
    def __init__(self):
        self.__strLog = ""


    def LogClear(self):
        self.__strLog = "\n----------Log----------\n"
        self.__strLog += inspect.stack()[1][1] + '\n'        # 文件位置
        self.__strLog += inspect.stack()[1][3] + '\n'        # 函数名
        self.__strLog += str(inspect.stack()[1][2]) + '\n'   # 行号


    def LogAppend(self, strLog):
        # 去除末尾换行符
        strLog = strLog.rstrip()
        self.__strLog += (strLog + "\n")


    def GetLog(self):
        return self.__strLog