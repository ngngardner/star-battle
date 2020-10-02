
# packages
import numpy as np

data = np.genfromtxt(f'puzzles/puzzle1.data', delimiter=',')
stars = np.zeros(data.shape)
unique, counts = np.unique(data, return_counts=True)
frequencies = np.asarray((unique, counts)).T
min_count = np.amin(frequencies, axis=0)[1]

# top left most smallest group
smallest_group = np.where(frequencies[:, 1] == min_count)[0][0]
print(smallest_group)
print(stars)

star_loc = np.where(data == smallest_group)[0]

print(star_loc)
