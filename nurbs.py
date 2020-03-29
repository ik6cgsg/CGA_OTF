from typing import List

from point import Point3d
from wpoint import WeightedPoint


class NURBS(object):
    def __init__(self):
        self.degree: int = 0
        self.control_points3d: List[Point3d] = []
        self.knots: List[float] = []

    def set_params(self, degree: int, control_points: List[WeightedPoint], knots: List[float]) -> bool:
        if len(knots) != len(control_points) + degree + 1:
            print("wrong params!")
            return False

        self.degree = degree
        self.control_points3d = NURBS._get_control_points3d(control_points)
        self.knots = knots
        return True

    def value(self, u: float) -> WeightedPoint:
        """
        De Boor algorithm implementation
        :param u: value of knot in [0, 1]
        :type u: float

        :return: value of NURBS at this knot
        """
        index, multiplicity = self._find_knot_index(u)
        print("index = %s, multiplicity = %s" % (index, multiplicity))
        insert_times = self.degree - multiplicity                        # +1 in case of "inclusive"

        cur_control_points = self.control_points3d[index - self.degree: index - multiplicity + 1]
        for r in range(1, insert_times + 1):
            new_control_points: List[Point3d] = []
            start = index - self.degree + r
            for i in range(start, index - multiplicity + 1):
                a_ir = (u - self.knots[i]) / (self.knots[i + self.degree - r + 1] - self.knots[i])
                p_ir = cur_control_points[i - start] * (1 - a_ir) + cur_control_points[i - start + 1] * a_ir
                new_control_points.append(p_ir)
            cur_control_points = list(new_control_points)
            NURBS._draw(cur_control_points)
        return cur_control_points[0].to_weighted_point()

    def _find_knot_index(self, u: float) -> (int, int):
        """
        :param u: value of knot in [0, 1]
        :type u: float

        :return: (knot_interval_index, multiplicity), where knot_interval_index - such index as u is in [u_k, u_(k+1)),
                 multiplicity - knot's multiplicity - 1
        """
        knot_interval_index = 0
        multiplicity = 0
        for i in range(len(self.knots)):
            if self.knots[i] > u:
                knot_interval_index = i - 1
                break

            if self.knots[i] == u:
                multiplicity += 1

        if multiplicity > 0:  # we need multiplicity - 1
            multiplicity -= 1
            if knot_interval_index == 0:
                knot_interval_index = len(self.knots) - 2

        return knot_interval_index, multiplicity

    @staticmethod
    def _get_control_points3d(cur_control_points: List[WeightedPoint]) -> List[Point3d]:
        list_point3d: List[Point3d] = []
        for wpoint in cur_control_points:
            list_point3d.append(wpoint.to3d())

        return list_point3d

    @staticmethod
    def _draw(cur_control_points: List[Point3d]):
        for p in cur_control_points:
            print(p)
        print("--------------------------------------")
