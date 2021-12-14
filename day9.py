import numpy as np
from numpy.core.fromnumeric import prod

def get_element(field, coordinate):

    i = coordinate[0]
    j = coordinate[1]

    n_rows, n_cols = field.shape
    if i < 0 or i >= n_rows or j < 0 or j >= n_cols:
        return 9

    return field[i, j]


def get_basin(field, coordinate, basin):

    if get_element(field, coordinate) == 9 or coordinate in basin:
        return
    
    basin.append(coordinate)

    i = coordinate[0]
    j = coordinate[1]

    get_basin(field, (i - 1, j), basin)
    get_basin(field, (i + 1, j), basin)
    get_basin(field, (i, j - 1), basin)
    get_basin(field, (i, j + 1), basin)


if __name__ == '__main__':


    with open('data/day9.txt', 'r') as f:
        lines = f.readlines()



    field = np.zeros((len(lines), len(lines[0]) - 1), dtype=int)

    for i, line in enumerate(lines):

        line = line.strip()
        for j, item in enumerate(line):
            field[(i, j)] = item


    total_risk = 0
    minima = list()
    for i, j in np.ndindex(field.shape):

        north = get_element(field, (i, j - 1))
        south = get_element(field, (i, j + 1))
        east = get_element(field, (i - 1, j))
        west = get_element(field, (i + 1, j))

        center = field[i, j]

        if center < min([north, south, east, west]):
            total_risk += center + 1
            minima.append((i, j))


    basins = list()
    basin_lens = list()
    for i, minimum in enumerate(minima):
        basin = list()
        get_basin(field, minimum, basin)
        basins.append(basin)
        basin_lens.append(len(basin))


    basin_lens = sorted(basin_lens)
    product = basin_lens[-1] * basin_lens[-2] * basin_lens[-3]
    print('Total Risk: {0:d}'.format(total_risk))
    print('Basin size product: {0:d}'.format(product))

