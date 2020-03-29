from nurbs import NURBS, NURBSException
from common import WeightedPoint

def example_degree2():
    """Example "heart" from http://nurbscalculator.in/"""
    degree = 2
    ctrl_points = [
        WeightedPoint(5, -5, 1),
        WeightedPoint(-5, 2, 1),
        WeightedPoint(-2, 5, 1),
        WeightedPoint(0, 2, 1),
        WeightedPoint(2, 5, 1),
        WeightedPoint(5, 2, 1),
        WeightedPoint(-5, -5, 1)
    ]

    knots = [0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.6, 0.7, 0.8, 0.9]
    nurbs = NURBS()

    try:
        nurbs.set_params(degree, ctrl_points, knots)
        nurbs.draw_curve(step=0.0005, verbose=False)
        nurbs.draw_curve_and_save_gif(step=0.0005, path_to_save="./results/heart_curve.gif", verbose=True)
    except NURBSException as e:
        print("Exception caught: %s" % str(e))

def example_degree4():
    degree = 4
    ctrl_points = [
        WeightedPoint(-8, 1.2, 0.3),
        WeightedPoint(-7, -4.5, 1),
        WeightedPoint(2, -4, 0.8),
        WeightedPoint(-5, 2, 1),
        WeightedPoint(6, 7, 0.1),
        WeightedPoint(-4, 5, 1),
        WeightedPoint(-10, 4, 0.3)
    ]

    knots = [0, 0, 0, 0, 0, 0.455, 0.545, 1, 1, 1, 1, 1]
    nurbs = NURBS()

    try:
        nurbs.set_params(degree, ctrl_points, knots)
        nurbs.draw_curve(step=0.0005, verbose=False)
        nurbs.draw_curve_and_save_gif(step=0.0005, path_to_save="./results/strange_curve.gif", verbose=True)
    except NURBSException as e:
        print("Exception caught: %s" % str(e))

if __name__ == "__main__":
    example_degree4()
