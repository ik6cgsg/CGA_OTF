import os

import numpy as np
import matplotlib.pyplot as plt

from typing import List
from celluloid import Camera

from common import Point3d, WeightedPoint
from common import convert_point3d_list_to_weighted_point_list, convert_weighted_point_list_to_point3d_list


class NURBSException(Exception):
    pass


class NURBS(object):
    def __init__(self):
        self.degree: int = 0
        self.control_points3d: List[Point3d] = []
        self.knots: List[float] = []

        self.control_points_by_levels: List[List[WeightedPoint]] = []

    def set_params(self, degree: int, control_points: List[WeightedPoint], knots: List[float]):
        if len(knots) != len(control_points) + degree + 1:
            raise NURBSException("wrong params!")

        self.degree = degree
        self.control_points3d = convert_weighted_point_list_to_point3d_list(control_points)
        self.knots = knots

    def value(self, u: float) -> WeightedPoint:
        """
        De Boor algorithm implementation
        :param u: value of knot in [0, 1]
        :type u: float

        :return: value of NURBS at this knot
        """
        self.control_points_by_levels = [convert_point3d_list_to_weighted_point_list(self.control_points3d)]

        index, multiplicity = self._find_knot_index(u)
        insert_times = self.degree - multiplicity                        # +1 in case of "inclusive"

        cur_control_points = self.control_points3d[index - self.degree: index - multiplicity + 1]
        for r in range(1, insert_times + 1):
            new_control_points: List[Point3d] = []
            start = index - self.degree + r
            for i in range(start, index - multiplicity + 1):
                a_ir = (u - self.knots[i]) / (self.knots[i + self.degree - r + 1] - self.knots[i])
                p_ir = cur_control_points[i - start] * (1 - a_ir) + cur_control_points[i - start + 1] * a_ir
                new_control_points.append(p_ir)
            cur_control_points = new_control_points
            self.control_points_by_levels.append(convert_point3d_list_to_weighted_point_list(cur_control_points))

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

    def _value_generator(self, step=0.001, verbose=False):
        """
        Special generator for yielding curve point in certain position.
        """
        start_u = self.knots[self.degree]
        end_u = self.knots[len(self.knots) - 1 - self.degree]
        for u in np.arange(start_u, end_u, step):
            if verbose:
                print("u: %f" % u)
            yield self.value(u)

    def _get_control_points_coords(self):
        control_points_x = []
        control_points_y = []
        for point in convert_point3d_list_to_weighted_point_list(self.control_points3d):
            control_points_x.append(point.x)
            control_points_y.append(point.y)

        return control_points_x, control_points_y

    def draw_curve(self, step=0.001, verbose=False):
        if not self.control_points3d:
            raise NURBSException("The curve isn't initialized."
                                 " Please call `set_params` method before trying to draw the curve.")

        curve_points_x = []  # list of curve's points' x coordinate
        curve_points_y = []  # list of curve's points' y coordinate

        if verbose:
            print("Calculating curve with step %f..." % step)

        value_generator = self._value_generator(step, verbose)
        for curve_point in value_generator:
            curve_points_x.append(curve_point.x)
            curve_points_y.append(curve_point.y)

        control_points_x, control_points_y = self._get_control_points_coords()

        plt.figure(figsize=(8, 8))
        plt.plot(control_points_x, control_points_y, c='g')
        plt.scatter(x=curve_points_x, y=curve_points_y, c='r', marker='.')
        plt.scatter(x=control_points_x, y=control_points_y, c='g', marker='s')
        plt.title("Calculated NURBS Curve\nSTEP: %f" % step)
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.show()

        if verbose:
            print("Done.")

    def draw_curve_and_save_gif(self, path_to_save, step=0.0011, verbose=False):
        if not self.control_points3d:
            raise NURBSException("The curve isn't initialized."
                                 " Please call `set_params` method before trying to draw the curve.")

        dir_to_save = os.path.dirname(path_to_save)
        if not os.path.exists(dir_to_save):
            os.makedirs(dir_to_save)

        fig = plt.figure(figsize=(8, 8))
        camera = Camera(fig)

        colors = ['b', 'g', 'y', 'c', 'm', 'o', 'p']
        control_points_x, control_points_y = self._get_control_points_coords()
        curve_points_x = []  # list of curve's points' x coordinate
        curve_points_y = []  # list of curve's points' y coordinate

        if verbose:
            print("Calculating curve and make animation with step %f..." % step)

        for curve_point in self._value_generator(step, verbose):
            plt.title("Calculated NURBS Curve Animation\n STEP: %f" % step)
            plt.xlabel("X")
            plt.ylabel("Y")

            # plot original control points
            plt.plot(control_points_x, control_points_y, c='g')
            plt.scatter(x=control_points_x, y=control_points_y, c='g', marker='s')

            # plot auxiliary control points
            for ind, cur_points_level in enumerate(self.control_points_by_levels[:-1]):
                x_coords = []
                y_coords = []
                for point in cur_points_level:
                    x_coords.append(point.x)
                    y_coords.append(point.y)

                plt.plot(x_coords, y_coords, c=colors[ind])
                plt.scatter(x=x_coords, y=y_coords, marker='s', c=colors[ind])

            # plot the curve points
            curve_points_x.append(curve_point.x)
            curve_points_y.append(curve_point.y)
            plt.scatter(x=curve_points_x, y=curve_points_y, c='r', marker='.')

            camera.snap()

        if verbose:
            print("Done.")

        if verbose:
            print("Saving animation...")
        animation = camera.animate()
        animation.save(path_to_save, writer="imagemagick", fps=40)
        if verbose:
            print("Done.")
