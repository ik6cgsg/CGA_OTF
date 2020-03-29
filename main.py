from nurbs import NURBS
from wpoint import WeightedPoint


if __name__ == "__main__":
    """Example from http://nurbscalculator.in/"""
    degree = 3
    ctrl_points = [
        WeightedPoint(-4, -4, 0.4),
        WeightedPoint(-2, 4, 1),
        WeightedPoint(2, -4, 1),
        WeightedPoint(4, 4, 0.7)]

    knots = [0, 0, 0, 0, 1, 1, 1, 1]
    nurbs = NURBS()
    if nurbs.set_params(degree, ctrl_points, knots):
        u = 0.37
        print("value at %s = %s" % (u, nurbs.value(u)))
