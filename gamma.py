from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QPen
from PyQt5.QtCore import Qt

# DebugMK
import math

from GammaWidget import Ui_GammaWidget


class CGammaForm(QWidget, Ui_GammaWidget):
    def __init__(self):
        super(CGammaForm, self).__init__()
        self.setupUi(self)


    def paintEvent(self, event):
        qPainter = QPainter(self)
        qPainter.begin(self)

        qPainter.setPen(QColor(168, 34, 3))
        qPainter.setFont(QFont('SimSum', 20))
        qPainter.drawText(event.rect(), Qt.AlignCenter, "实时调试工具")

        qPainter.setPen(Qt.red)
        size = self.size()
        for i in range(1000):
            x = 100 * (-1 + 2.0 * i / 1000) + size.width() / 2.0
            y = -50 * math.sin((x - size.width() / 2.0) * math.pi / 50) + size.height() / 2.0
            qPainter.drawPoint(x, y)

        print(size)
        Height = size.height() - 1
        Width = size.width() - 1
        qPen = QPen(Qt.black, 1, Qt.SolidLine)
        qPainter.setPen(qPen)
        qPainter.drawLine(0, 0, 0, Height)
        qPainter.drawLine(0, Height, Width, Height)
        qPainter.drawLine(Width, Height, Width, 0)
        qPainter.drawLine(Width, 0, 0, 0)

        qPainter.end()


    def mousePressEvent(self, QMouseEvent):
        print("鼠标按下事件")

    def mouseReleaseEvent(self, QMouseEvent):
        print("鼠标释放事件")
        if QMouseEvent.button() == Qt.LeftButton:
            print("左键")
        elif QMouseEvent.button() == Qt.RightButton:
            print("右键")
        elif QMouseEvent.button() == Qt.MidButton:
            print("点击滚轮")

    def mouseMoveEvent(self, QMouseEvent):
        print("鼠标移动事件")




