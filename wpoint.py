from point import Point3d


class WeightedPoint(object):
    def __init__(self, x: float, y: float, w: float):
        self.x = x
        self.y = y
        self.w = w

    def to3d(self) -> Point3d:
        return Point3d(self.x * self.w, self.y * self.w, self.w)

    def __str__(self):
        return "WeightedPoint(%s, %s) with weight = %s)" % (self.x, self.y, self.w)
