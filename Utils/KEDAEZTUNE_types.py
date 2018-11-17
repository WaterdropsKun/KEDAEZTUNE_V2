class Point:
    def __init__(self, xParam = 0.0, yParam = 0.0):
        self.x = xParam
        self.y = yParam

    def __str__(self):
        return "(%.2f, %.2f)" % (self.x, self.y)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)
    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)



