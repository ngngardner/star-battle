
# package
import numpy as np

# internal
from star_battle.tools.illegal import check_illegal


def test_illegal_row():
    assert(True)


def test_illegal_column():
    assert(True)


def test_illegal_group():
    assert(True)


def test_illegal_none():
    '''
        Test that blocked1 is a legal placement of a star in puzzle1
    '''
    puzzle = np.genfromtxt(f'data/puzzles/puzzle1.data', delimiter=',')
    stars = np.genfromtxt(f'data/blocked/blocked1.data', delimiter=',')

    res = check_illegal(puzzle, stars)
    assert(not res)
