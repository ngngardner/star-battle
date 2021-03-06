
# packages
import numpy as np

# internal
from solver import solve

if __name__ == "__main__":
    puzzle = np.genfromtxt(f'data/puzzles/puzzle2.data', delimiter=',')
    stars = np.zeros(puzzle.shape)

    print('Puzzle:')
    print(puzzle)

    stars = solve(puzzle)
    print(stars)
