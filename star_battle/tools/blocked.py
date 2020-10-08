
# package
import numpy as np

# internal
from .coordinates import coordinates


def blocked(puzzle: np.array, stars: np.array) -> np.array:
    '''
        Given an input puzzle and star locations grid, return the
        stars grid with blocked locations as -1.
    '''
    def reset_stars(stars: np.array, star_locs: list) -> np.array:
        # replace stars that were overwritten with their saved locations
        stars[tuple(np.transpose(star_locs))] = 1
        return stars

    def block_groups(puzzle: np.array, stars: np.array) -> np.array:
        '''
            Given an input star grid, block every grid space that already has
            a star in the same group.
        '''
        star_locs = coordinates(np.where(stars == 1))
        unique_groups = []
        for star in star_locs:
            group = puzzle[star]
            if group not in unique_groups:
                unique_groups.append(group)

        blocked = []
        for group in unique_groups:
            blocked = blocked + coordinates(np.where(puzzle == group))

        stars[tuple(np.transpose(blocked))] = -1
        return reset_stars(stars, star_locs)

    def block_diagonal(stars: np.array) -> np.array:
        x = stars.shape[0]
        y = stars.shape[1]
        star_locs = coordinates(np.where(stars == 1))

        blocked = []
        for star in star_locs:
            star_row = star[0]
            star_col = star[1]
            # north west
            if (star_row-1 in range(x)) and (star_col-1 in range(y)):
                blocked.append((star_row-1, star_col-1))
            # north east
            if (star_row-1 in range(x)) and (star_col+1 in range(y)):
                blocked.append((star_row-1, star_col+1))
            # south west
            if (star_row+1 in range(x)) and (star_col-1 in range(y)):
                blocked.append((star_row+1, star_col-1))
            # south east
            if (star_row+1 in range(x)) and (star_col+1 in range(y)):
                blocked.append((star_row+1, star_col+1))

        stars[tuple(np.transpose(blocked))] = -1
        return reset_stars(stars, star_locs)

    def block_column(stars: np.array) -> np.array:
        '''
            Given an input star grid, block every grid space that already has
            a star in the same column.
        '''
        rows = stars.shape[0]
        star_locs = coordinates(np.where(stars == 1))
        # block every row in the same col
        for star in star_locs:
            star_col = star[1]
            for row in range(rows):
                stars[row, star_col] = -1

        return reset_stars(stars, star_locs)

    def block_row(stars: np.array) -> np.array:
        '''
            Given an input star grid, block every grid space that already has
            a star in the same row.
        '''
        cols = stars.shape[1]
        star_locs = coordinates(np.where(stars == 1))
        # block every column in the same row
        for star in star_locs:
            star_row = star[0]
            for col in range(cols):
                stars[star_row, col] = -1

        return reset_stars(stars, star_locs)

    if puzzle.shape != stars.shape:
        raise ValueError('puzzle and star grid must have same shape')

    stars = block_groups(puzzle, stars)
    stars = block_diagonal(stars)
    stars = block_column(stars)
    stars = block_row(stars)

    return stars
