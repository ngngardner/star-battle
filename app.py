
# packages
import numpy as np


def coordinates(points: tuple):
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


def blocked(puzzle: np.array, stars: np.array):
    '''
        Given an input puzzle and star locations grid, return the
        stars grid with blocked locations as -1.
    '''
    def reset_stars(stars: np.array, star_locs: list):
        # replace stars that were overwritten with their saved locations
        stars[tuple(np.transpose(star_locs))] = 1
        return stars

    def block_groups(puzzle: np.array, stars: np.array):
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

    def block_diagonal(stars: np.array):
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

    def block_column(stars: np.array):
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

    def block_row(stars: np.array):
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


def smallest_group(puzzle: np.array, stars: np.array, available_loc: np.array):
    '''
        Given an input puzzle, return the smallest available group by index
        (e.g. 2)
    '''
    def frequencies(puzzle: np.array):
        '''
            Given an input puzzle, return a 2d array, where column 0 is
            the group index, and column 1 is the count for that group.
        '''
        groups, counts = np.unique(puzzle, return_counts=True)
        return np.asarray((groups, counts)).T

    f = frequencies(puzzle)
    min_count = np.amin(f, axis=0)[1]

    # top left most smallest group
    smallest = np.where(f[:, 1] == min_count)[0][0]
    group_loc = coordinates(np.where(puzzle == smallest))
    common = list(set(group_loc).intersection(available_loc))

    while not common:
        test = np.where(f[:, 0] == smallest)
        smallest_loc = np.where(f[:, 0] == smallest)[0]
        f = np.delete(f, smallest_loc, axis=0)
        min_count = np.amin(f, axis=0)[1]
        group = np.where(f[:, 1] == min_count)[0][0]
        smallest = f[group][0]
        group_loc = coordinates(np.where(puzzle == smallest))
        common = list(set(group_loc).intersection(available_loc))
    return smallest


def place_star(puzzle: np.array, stars: np.array):
    '''
        Place a star in the smallest top left-most position that is available.
    '''
    def top_left_most(points: list):
        '''
            Given a list of tuples which are 2d coordinates, return the
            x, y coordinate pair that is top left most.
        '''
        if len(points) < 1:
            raise ValueError
        if len(points[0]) != 2:
            raise ValueError

        p_x = points[0][0]
        p_y = points[0][1]
        min_total = p_x + p_y
        tpm_point = points[0]

        for point in points:
            p_x = point[0]
            p_y = point[1]
            total = p_x + p_y
            if total < min_total:
                min_total = total
                tpm_point = point

        return tpm_point

    available_loc = coordinates(np.where(stars == 0))
    s = smallest_group(puzzle, stars, available_loc)
    group_loc = coordinates(np.where(puzzle == s))
    common = list(set(group_loc).intersection(available_loc))
    if len(common) > 0:
        star_loc = top_left_most(common)
        stars[star_loc] = 1
        stars = blocked(puzzle, stars)
    else:
        print('error, no available locations')
    return stars


if __name__ == "__main__":
    puzzle = np.genfromtxt(f'puzzles/puzzle1.data', delimiter=',')
    stars = np.zeros(puzzle.shape)

    print('Puzzle:')
    print(puzzle)

    print('Star 1')
    stars = place_star(puzzle, stars)
    print(stars)

    print('Star 2')
    stars = place_star(puzzle, stars)
    print(stars)
