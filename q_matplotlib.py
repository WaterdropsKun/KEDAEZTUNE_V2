from PyQt5.QtWidgets import QSizePolicy

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

''' 父类调用
# DebugMK matplotlib
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
self.qMatplotlib = QMatplotlib(self, width=5, height=4, dpi=100)
self.qMatplotlibToolBar = NavigationToolbar(self.qMatplotlib, self)
self.verticalLayout.addWidget(self.qMatplotlib)
self.verticalLayout.addWidget(self.qMatplotlibToolBar)
'''


class QMatplotlib(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        # DebugMK
        self.InitPlot()


    def InitPlot(self):
        self.fig.suptitle('Gamma曲线')
        x = [100, 200, 300, 400, 500, 600, 700, 800, 900]
        y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
        self.axes.plot(x, y)
        self.axes.set_ylabel('静态图： Y轴')
        self.axes.set_xlabel('静态图： X轴')
        self.axes.grid(True)





