# This module creates the Bspline baseline for randomizing mouse movements
# b spline interpolation from https://stackoverflow.com/questions/24612626/b-spline-interpolation-with-python

import numpy as np
import scipy.interpolate as si


def get_bspline():
    # Returns x and y list

    # curve base
    # points = [[-6, 2], [-3, -2],[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 5], [8, 8], [6, 8], [5, 9], [7, 2]];
    points = [[0, 0], [0, 2], [2, 3], [4, 0], [6, 3], [8, 2], [8, 0]]
    points = np.array(points)
    x = points[:,0]
    y = points[:,1]

    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)

    x_tup = si.splrep(t, x, k=3)
    y_tup = si.splrep(t, y, k=3)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)

    return zip(x_i, y_i)


