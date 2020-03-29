from typing import List


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


class WeightedPoint(object):
    def __init__(self, x: float, y: float, w: float):
        self.x = x
        self.y = y
        self.w = w

    def to_point3d(self) -> Point3d:
        return Point3d(self.x * self.w, self.y * self.w, self.w)

    def __str__(self):
        return "WeightedPoint(%s, %s) with weight = %s)" % (self.x, self.y, self.w)


def convert_point3d_list_to_weighted_point_list(points3d_list: List[Point3d]) -> List[WeightedPoint]:
    return [point.to_weighted_point() for point in points3d_list]


def convert_weighted_point_list_to_point3d_list(weighted_points_list: List[WeightedPoint]) -> List[Point3d]:
    return [point.to_point3d() for point in weighted_points_list]
