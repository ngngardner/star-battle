
# package
import numpy as np


def check_illegal(puzzle: np.array, stars: np.array) -> bool:
    def check_groups(puzzle: np.array, stars: np.array) -> bool:
        # TODO
        return False

    def check_columns(stars: np.array) -> bool:
        rows = stars.shape[0]
        cols = stars.shape[1]
        for col in range(cols):
            blocked = 0
            for row in range(rows):
                if stars[row, col] == -1:
                    blocked += 1
            if blocked >= rows:
                return True
        return False

    def check_rows(stars: np.array) -> bool:
        rows = stars.shape[0]
        cols = stars.shape[1]
        for row in range(rows):
            blocked = 0
            for col in range(cols):
                if stars[row, col] == -1:
                    blocked += 1
            if blocked >= rows:
                return True
        return False

    if check_groups(puzzle, stars):
        return True
    if check_columns(stars):
        return True
    if check_rows(stars):
        return True

    return False
