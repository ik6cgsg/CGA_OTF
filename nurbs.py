from typing import List
from point import Point3d
from wpoint import WeightedPoint

class NURBS(object):
    def __init__(self):
        self.degree: int = 0
        self.controlPoints3d: List[Point3d] = []
        self.knots: List[float] = []
        pass

    def setParams(self, degree: int, controlPoints: List[WeightedPoint], knots: List[float]) -> bool:
        if len(knots) != len(controlPoints) + degree + 1:
            print("wrong params!")
            return False
        self.degree = degree
        self.controlPoints3d = NURBS.__get3dControlPoints(controlPoints)
        self.knots = knots
        return True

    def value(self, u: float) -> WeightedPoint:
        """de Boor algorithm
        Params:
        u: float - value of knot in [0, 1]

        Returns:
        value of NURBS at this knot
        """
        index, multiplicity = self.__findKnotIndex(u)
        print("index = %s, multiplicity = %s" % (index, multiplicity))
        insertTimes = self.degree - multiplicity                        # +1 in case of "inclusive"
        currentControlPoints = self.controlPoints3d[index - self.degree : index - multiplicity + 1]
        for r in range(1, insertTimes + 1):
            newControlPoints: List[Point3d] = []
            start = index - self.degree + r
            for i in range(start, index - multiplicity + 1):
                a_ir = (u - self.knots[i]) / (self.knots[i + self.degree - r + 1] - self.knots[i])
                p_ir = currentControlPoints[i - start] * (1 - a_ir) + currentControlPoints[i - start + 1] * a_ir
                newControlPoints.append(p_ir)
            currentControlPoints = list(newControlPoints)
            NURBS.__draw(currentControlPoints)
        return currentControlPoints[0].toWPoint()

    def __findKnotIndex(self, u: float) -> (int, int):
        """
        Returns:
        -- knotIntervalIndex: int - such index as u is in [u_k, u_(k+1))
        -- multiplicity: int - knot's multiplicity - 1
        """
        knotIntervalIndex = 0
        multiplicity = 0
        for i in range(len(self.knots)):
            if self.knots[i] > u:
                knotIntervalIndex = i - 1
                break
            if self.knots[i] == u:
                multiplicity += 1
        if multiplicity > 0:  # we need multiplicity - 1
            multiplicity -= 1
            if knotIntervalIndex == 0:
                knotIntervalIndex = len(self.knots) - 2
        return knotIntervalIndex, multiplicity

    @staticmethod
    def __get3dControlPoints(currentControlPoints: List[WeightedPoint]) -> List[Point3d]:
        listPoint3d: List[Point3d] = []
        for wpoint in currentControlPoints:
            listPoint3d.append(wpoint.to3d())
        return listPoint3d

    @staticmethod
    def __draw(currentControlPoints: List[Point3d]):
        for p in currentControlPoints:
            print(p)
        print("--------------------------------------")
