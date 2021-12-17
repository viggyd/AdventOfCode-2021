import numpy as np

if __name__ == '__main__':

    with open('data/day15.txt', 'r') as f:
        lines = f.readlines()

    orig_field = np.zeros((len(lines), len(lines[0]) - 1), dtype=int)
    field = orig_field

    for i, line in enumerate(lines):
        for j, risk in enumerate(line.strip()):
            field[i, j] = risk

    new_field = orig_field 
    for i in range(4):
        field = np.concatenate((field, new_field + i + 1), axis=1)

    new_field = field
    for i in range(4):
        field = np.concatenate((field, new_field + i + 1), axis=0)

    fix_coords = np.transpose((field > 9).nonzero())
    for coord in fix_coords:
        coord = tuple(coord)
        field[coord] = field[coord] % 9


    visit = np.zeros(field.shape, dtype=int)
    dist = np.ones(field.shape, dtype=int) * 99999

    entry = (0, 0)
    exit = (field.shape[0] - 1, field.shape[1] - 1)

    dist[entry] = 0
    visit[entry] = 1

    shortest_path_set = {entry}
    visited_nodes = {entry}

    spot = entry
    perc_done = 0

    while exit not in visited_nodes:

        # Determine adjacent neighbors
        neighbors = [
            (spot[0] - 1, spot[1]),
            (spot[0] + 1, spot[1]),
            (spot[0], spot[1] - 1),
            (spot[0], spot[1] + 1)
        ]

        # Update distances of all adjacent neighbors.
        for neighbor in neighbors:
            
            if  0 <= neighbor[0] < field.shape[0] \
            and 0 <= neighbor[1] < field.shape[1]:
                dist[neighbor] = min(dist[neighbor], dist[spot] + field[neighbor])
                visited_nodes.add(neighbor)
                visit[neighbor] = 1


        # Now, pick the node that has minimum distance, but is also not in
        # the shortest path set. In the case of ties, just pick the first one.
        candidates = visited_nodes - shortest_path_set
        cand_costs = {x: dist[x] for x in candidates}
        spot = min(cand_costs, key=cand_costs.get)
        shortest_path_set.add(spot)

    print('Minimum risk: {0:d}'.format(dist[exit]))
