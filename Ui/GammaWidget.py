# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GammaWidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GammaWidget(object):
    def setupUi(self, GammaWidget):
        GammaWidget.setObjectName("GammaWidget")
        GammaWidget.resize(512, 512)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GammaWidget.sizePolicy().hasHeightForWidth())
        GammaWidget.setSizePolicy(sizePolicy)
        GammaWidget.setMinimumSize(QtCore.QSize(512, 512))
        GammaWidget.setMaximumSize(QtCore.QSize(512, 512))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(GammaWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(GammaWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)

        self.retranslateUi(GammaWidget)
        QtCore.QMetaObject.connectSlotsByName(GammaWidget)

    def retranslateUi(self, GammaWidget):
        _translate = QtCore.QCoreApplication.translate
        GammaWidget.setWindowTitle(_translate("GammaWidget", "Form"))

