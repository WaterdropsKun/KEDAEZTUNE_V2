from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

import sys


# Ui
from Ui.MainWindow import Ui_MainWindow
# adb
from adb import CAdb, ADB_COMMAND
# WNR
from wnr import CWNRForm
# ASF
from asf import CASFForm
# GAMMA
from gamma import CGammaForm


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # signal slot
        # 菜单栏信号槽函数关联
        self.TestAction.triggered.connect(self.Test)

        # 初始化子窗口
        self.cWNRForm = CWNRForm()
        self.cASFForm = CASFForm()
        self.cGammaForm = CGammaForm()

        # 工具类初始化
        self.cAdb = CAdb()

        # 初始化操作（adb连接 + 发送命令）
        self.AdbConnect()
        self.SendAdbCommand(ADB_COMMAND.NONE_CMD)


    def Test(self):
        print("Test")   # DebugMK
        self.SendAdbCommand(ADB_COMMAND.WNR_CMD)

        #DebugMK 添加子窗口
        self.ChildrenForm.addWidget(self.cWNRForm)
        self.ChildrenForm.addWidget(self.cASFForm)
        self.ChildrenForm.addWidget(self.cGammaForm)
        self.cASFForm.hide()
        self.cWNRForm.hide()
        self.cGammaForm.hide()

        self.cWNRForm.show()


    def AdbConnect(self):
        strDeviceIP = self.lineEdit.text()

        strLog, ret = self.cAdb.AdbConnectDevice(strDeviceIP)
        self.Log.append(strLog)  # DebugMK
        if ret == True:
            self.Log.append("Adb connect succeed!")
        else:
            self.Log.append("Adb connect failed!")


    def SendAdbCommand(self, enumAdbCommand):
        strLog, ret = self.cAdb.AdbCommand(enumAdbCommand)
        self.Log.append(strLog)  # DebugMK
        if ret == True:
            self.Log.append("Adb command " + str(enumAdbCommand) + " succeed!")
        else:
            self.Log.append("Adb command " + str(enumAdbCommand) + " failed!")


    def LogClear(self):
        self.Log.clear()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    ui = MainWindow()
    ui.show()

    sys.exit(app.exec_())
