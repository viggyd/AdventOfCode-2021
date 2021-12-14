import json
import numpy as np

FOLDS = [
    ('x', 655),
    ('y', 447),
    ('x', 327),
    ('y', 223),
    ('x', 163),
    ('y', 111),
    ('x', 81),
    ('y', 55),
    ('x', 40),
    ('y', 27),
    ('y', 13),
    ('y', 6)
]

# FOLDS = [
#     ('y', 7),
#     ('x', 5)
# ]
AXIS = {'x': 1, 'y': 0}


class Dot(object):

    def __init__(self, dot) -> None:
        self.x = dot[0]
        self.y = dot[1]
    
    def __repr__(self) -> str:
        return '({0:d}, {1:d})'.format(self.x, self.y)


    

class DotField(object):

    def __init__(self, x, y) -> None:
        self.field = np.zeros((y, x), dtype=int)

    def add_dot(self, dot):
        self.field[(dot.y, dot.x)] = 1

    
    def fold(self, idx, axis):

        np_axis = AXIS[axis]  # Convert from x/y to 0/1 for numpy axes

        # Split the field.
        split_idx = [idx]
        if self.field.shape[np_axis] % 2 != 0:
            split_idx = [idx, idx + 1]

        folded_field = np.split(self.field, split_idx, axis=np_axis)
        base = folded_field[0]
        foldee = folded_field[-1]


        # Reverse the field to be folded into the base, reverse along the
        # same axis.
        base_rev = np.flip(base, axis=np_axis)
        self.field = np.flip(base_rev | foldee, axis=np_axis)

        return


    def __repr__(self) -> str:
        return self.field.__repr__()

    def __str__(self) -> str:

        print_str = ''
        for row in field.field:
            row = list(row)
            print_str += ''.join(['▪' if x == 1 else ' ' for x in row ]) + '\n'
        
        return print_str

if __name__ == '__main__':

    with open('data/day13.json', 'r') as f:
        dots = json.load(f)
    
    dots = [Dot(x) for x in dots]

    max_x = max([x.x for x in dots]) + 1
    max_y = max([x.y for x in dots]) + 1

    max_x += max_x % 2 == 0
    max_y += max_y % 2 == 0

    field = DotField(max_x, max_y)

    for dot in dots:
        field.add_dot(dot)

    for fold in FOLDS:
        field.fold(fold[1], fold[0])

    print(field)

    

