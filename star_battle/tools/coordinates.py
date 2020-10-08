
# package
import numpy as np


def coordinates(points: tuple) -> list:
    '''
        Given an input tuple of size two, with both elements being numpy
        arrays, return a list of coordianates.

        This function is required due to the output of np.where returning
        a an array of x-values and array of y-values.
    '''
    if len(points) != 2:
        return ValueError
    if type(points[0]) != np.ndarray:
        raise TypeError
    if type(points[1]) != np.ndarray:
        raise TypeError

    c = []
    for i, j in zip(points[0], points[1]):
        c.append((i, j))
    return c
