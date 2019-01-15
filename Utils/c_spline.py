from Utils.KEDAEZTUNE_types import *

class CSpline(object):
    def __init__(self):
        self.__DataPointsList = []     # 输入点集
        self.__ControlPointsList = []
        self.__SplinePointsList = []   # 输出点集

        self.__dPrecision = 1          # 精度
        self.__bIsXCalibrated = True   # 是否以x为横坐标
        self.__nMaxWidth = 1023
        self.__nMaxHeight = 65535


    def nMaxWidthSet(self, nMaxWidth):
        self.__nMaxWidth = nMaxWidth

    def nMaxHeightSet(self, nMaxHeight):
        self.__nMaxHeight = nMaxHeight

    def dPrecisionSet(self, dPrecision):
        self.__dPrecision = dPrecision

    def dPrecisionGet(self):
        return self.__dPrecision


    def DataPointsListSet(self, DataPointsList):
        self.__DataPointsList = DataPointsList

    def SplinePointsListGet(self):
        self.GetSplinePoints()

        PointTmp = []
        PointTmp.append(self.__DataPointsList[0])
        for i in range(1, len(self.__SplinePointsList)-1):
            PointTmp.append(self.__SplinePointsList[i])

            if PointTmp[i].x < 0:
                PointTmp[i].x = 0
            if PointTmp[i].x > self.__nMaxWidth:
                PointTmp[i].x = self.__nMaxWidth
            if PointTmp[i].y < 0:
                PointTmp[i].y = 0
            if PointTmp[i].y > self.__nMaxHeight:
                PointTmp[i].y = self.__nMaxHeight
        PointTmp.append(self.__DataPointsList[len(self.__DataPointsList)-1])

        return PointTmp


    def GetSplinePoints(self):
        self.__SplinePointsList = []

        if len(self.__DataPointsList) == 1:
            self.__SplinePointsList.append(self.__DataPointsList[0])

        elif len(self.__DataPointsList) == 2:
            n = 1
            if self.__bIsXCalibrated:
                n = (int)((self.__DataPointsList[1].x - self.__DataPointsList[0].x) / self.__dPrecision)
            else:
                n = (int)((self.__DataPointsList[1].y - self.__DataPointsList[0].y) / self.__dPrecision)
            # 边界检测
            if 0 == n:
                n = 1
            if n < 0:
                n = -n
            # 插值
            for i in range(n):
                dRatio = i / n
                self.__SplinePointsList.append((1 - dRatio) * self.__DataPointsList[0] + dRatio * self.__DataPointsList[1])

        elif len(self.__DataPointsList) > 2:
            self.GetControlPoints()

            # Draw bezier curves using Bernstein Polynomials
            for i in range(len(self.__ControlPointsList) - 1):
                b1 = self.__ControlPointsList[i] * 2.0 / 3.0 + self.__ControlPointsList[i+1] / 3.0
                b2 = self.__ControlPointsList[i] / 3.0 + self.__ControlPointsList[i+1] * 2.0 / 3.0

                n = 1
                if self.__bIsXCalibrated:
                    n = (int)((self.__DataPointsList[i+1].x - self.__DataPointsList[i].x) / self.__dPrecision)
                else:
                    n = (int)((self.__DataPointsList[i+1].y - self.__DataPointsList[i].y) / self.__dPrecision)
                # 边界检测
                if 0 == n:
                    n = 1
                if n < 0:
                    n = -n
                # 插值
                for j in range(n):
                    dRatio = j / n
                    PointTmp = (1 - dRatio) * (1 - dRatio) * (1 - dRatio) * self.__DataPointsList[i] +\
                                3 * (1 - dRatio) * (1 - dRatio) * dRatio * b1 +\
                                3 * (1 - dRatio) * dRatio * dRatio * b2 + \
                                dRatio * dRatio * dRatio * self.__DataPointsList[i+1]
                    self.__SplinePointsList.append(PointTmp)


    def GetControlPoints(self):
        if self.__DataPointsList != [] and len(self.__DataPointsList) == 3:
            self.__ControlPointsList = []
            self.__ControlPointsList.append(self.__DataPointsList[0])
            self.__ControlPointsList.append((6 * self.__DataPointsList[1] - self.__DataPointsList[0] - self.__DataPointsList[2]) / 4)
            self.__ControlPointsList.append(self.__DataPointsList[1])

        if self.__DataPointsList != [] and len(self.__DataPointsList) > 3:
            self.__ControlPointsList = []
            diag = []   # tridiagonal matrix a(i , i)
            sub = []    # tridiagonal matrix a(i , i-1)
            sup = []    # tridiagonal matrix a(i , i+1)

            n = len(self.__DataPointsList)
            for i in range(n):
                self.__ControlPointsList.append(self.__DataPointsList[i])
                diag.append(4)
                sub.append(1)
                sup.append(1)

            # 放大6倍
            self.__ControlPointsList[1] = 6 * self.__ControlPointsList[1] - self.__ControlPointsList[0]
            self.__ControlPointsList[n - 2] = 6 * self.__ControlPointsList[n - 2] - self.__ControlPointsList[n - 1]
            for i in range(2, n-2):
                self.__ControlPointsList[i] = 6 * self.__ControlPointsList[i]

            # Gaussian elimination from row 1 to n-2
            for i in range(2, n-1):
                sub[i] = sub[i] / diag[i-1]
                diag[i] = diag[i] - sub[i] * sup[i-1]
                self.__ControlPointsList[i] = self.__ControlPointsList[i] - sub[i] * self.__ControlPointsList[i-1]

            self.__ControlPointsList[n-2] = self.__ControlPointsList[n-2] / diag[n-2]

            for i in range(n-3, 0, -1):
                self.__ControlPointsList[i] = (self.__ControlPointsList[i] - sup[i] * self.__ControlPointsList[i + 1]) / diag[i]



if __name__ == '__main__':
    DataPointsList = [Point(0, 0), Point(50, 50), Point(120, 120), Point(150, 150), Point(255, 255)]
    # DataPointsList = [Point(0, 0), Point(255, 255)]

    cSpline = CSpline()
    cSpline.DataPointsListSet(DataPointsList)
    cSpline.SplinePointsListGet()









