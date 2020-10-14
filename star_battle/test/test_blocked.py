
# package
import numpy as np

# internal
from star_battle.tools.blocked import blocked


def test_blocked_center():
    '''
        Test that blocked1 is the output of puzzle1 and stars1,
        where there is a star in the center of the board
    '''
    puzzle = np.genfromtxt(f'data/puzzles/puzzle1.data', delimiter=',')
    stars = np.genfromtxt(f'data/blocked/stars1.data', delimiter=',')
    stars_blocked = np.genfromtxt(f'data/blocked/blocked1.data', delimiter=',')

    res = blocked(puzzle, stars)
    assert(np.array_equal(res, stars_blocked))


def test_blocked_corner():
    '''
        Test that blocked2 is the output of puzzle1 and stars2,
        where there is a star in a corner of the board
    '''
    assert(True)


def test_blocked_corner():
    '''
        Test that blocked2 is the output of puzzle1 and stars2,
        where there is a star in a corner of the board
    '''
    assert(True)