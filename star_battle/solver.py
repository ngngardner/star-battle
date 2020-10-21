
# packages
import numpy as np

# internal
from blocked import blocked
from coordinates import coordinates
from illegal import check_illegal
from tree import Node


def smallest_group(puzzle: np.array,
                   stars: np.array,
                   available_loc: np.array) -> int:
    '''
        Given an input puzzle, return the smallest available group by index
        (e.g. 2)
    '''
    def frequencies(puzzle: np.array) -> np.array:
        '''
            Given an input puzzle, return a 2d array, where column 0 is
            the group index, and column 1 is the count for that group.
        '''
        groups, counts = np.unique(puzzle, return_counts=True)
        return np.asarray((groups, counts)).T

    # top left most smallest group
    f = frequencies(puzzle)
    min_count = np.amin(f, axis=0)[1]
    smallest = np.where(f[:, 1] == min_count)[0][0]

    # find intersection of available locations with group locations
    group_loc = coordinates(np.where(puzzle == smallest))
    common = list(set(group_loc).intersection(available_loc))

    while not common:
        # index of the top left most smallest group
        smallest_loc = np.where(f[:, 0] == smallest)[0]

        if len(f) > 1:
            # delete smallest group by index, since it is blocked
            f = np.delete(f, smallest_loc, axis=0)

            # return group by group index (not array index)
            min_count = np.amin(f, axis=0)[1]
            group = np.where(f[:, 1] == min_count)[0][0]
            smallest = f[group][0]

            # find intersection of available locations with group locations
            group_loc = coordinates(np.where(puzzle == smallest))
            common = list(set(group_loc).intersection(available_loc))
        else:
            # there are no unblocked groups, so return invalid group index
            return -1
    return smallest


def place_star(puzzle: np.array, stars: np.array) -> np.array:
    '''
        Place a star in the smallest top left-most position that is available.
    '''
    def top_left_most(points: list) -> tuple:
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

    temp_stars = np.copy(stars)
    available_loc = coordinates(np.where(temp_stars == 0))
    s = smallest_group(puzzle, temp_stars, available_loc)
    if s != -1:
        group_loc = coordinates(np.where(puzzle == s))
        common = list(set(group_loc).intersection(available_loc))
        if len(common) > 0:
            star_loc = top_left_most(common)
            temp_stars[star_loc] = 1
            temp_stars = blocked(puzzle, temp_stars)
        else:
            print('error, no available locations')
    else:
        print('error, all groups are blocked')
    return temp_stars


def last_placed_star(stars_new: np.array, stars_prev: np.array):
    res = []
    for loc in coordinates(np.where(stars_new == 1)):
        if loc not in coordinates(np.where(stars_prev == 1)):
            return loc
    return None


def solve(puzzle: np.array):
    stars = np.zeros(puzzle.shape)
    node = Node(stars)

    while True:
        if not check_illegal(puzzle, node.data):
            prev_stars = np.copy(node.data)
            stars = place_star(puzzle, prev_stars)

            new_star_loc = last_placed_star(stars, prev_stars)

            node.insert(stars, new_star_loc)

            node = node.children[-1]
            num_stars = len(coordinates(np.where(node.data == 1)))
        else:
            if node.parent is not None:
                bad_loc = node.star_loc
                node = node.parent
                node.delete_children()
                node.data[bad_loc] = -1

        if num_stars == stars.shape[0]:
            print('found solution')
            return stars
            break
