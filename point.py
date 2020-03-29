from wpoint import WeightedPoint


class Point3d(object):
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point3d(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, num: float):
        return Point3d(self.x * num, self.y * num, self.z * num)

    def __str__(self):
        return "Point3d(%s, %s, %s)" % (self.x, self.y, self.z)

    def to_weighted_point(self):
        return WeightedPoint(self.x / self.z, self.y / self.z, self.z)
