from nurbs import NURBS, NURBSException
from common import WeightedPoint


if __name__ == "__main__":
    """Example from http://nurbscalculator.in/"""
    degree = 2
    ctrl_points = [
        WeightedPoint(5, -5, 1),
        WeightedPoint(-5, 2, 1),
        WeightedPoint(-2, 5, 1),
        WeightedPoint(0, 2, 1),
        WeightedPoint(2, 5, 1),
        WeightedPoint(5, 2, 1),
        WeightedPoint(-5, -5, 1)]

    knots = [0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.6, 0.7, 0.8, 0.9]
    nurbs = NURBS()

    try:
        nurbs.set_params(degree, ctrl_points, knots)
        nurbs.draw_curve(verbose=True)
        nurbs.draw_curve_and_save_gif(path_to_save="./results/heart_curve.gif", verbose=True)
    except NURBSException as e:
        print("Exception caught: %s" % str(e))
