import numpy as np

class Line(object):
    
    def __init__(self, line) -> None:

        [start, end] = line.strip().split(' -> ')
        self.start = Coordinate(start)
        self.end = Coordinate(end)

        self.straight = self.is_straight()


    def is_straight(self):
        return self.start.x == self.end.x or self.start.y == self.end.y

    def __repr__(self) -> str:
        return '{0:s} -> {1:s}'.format(self.start.__str__(), self.end.__str__())
    
    def __str__(self) -> str:
        return self.__repr__()

class Coordinate(object):

    def __init__(self, coord_str) -> None:
        [self.x, self.y] = coord_str.split(',')
        self.x = int(self.x)
        self.y = int(self.y)

    def __repr__(self) -> str:
        return '({0:d}, {1:d})'.format(self.x, self.y)
    
    def __str__(self) -> str:
        return self.__repr__()

if __name__ == '__main__':

    with open('data/day5.txt') as f:
        readouts = f.readlines()

    lines = list()
    for line in readouts:

        lines.append(Line(line))

    straight_lines = [x for x in lines if x.straight]

    field = np.zeros((1000, 1000), dtype=int)

    for line in lines:

        if line.straight:
            x_dir = 1 if line.start.x <= line.end.x else -1
            y_dir = 1 if line.start.y <= line.end.y else -1

            for i in range(line.start.x, line.end.x + x_dir, x_dir):
                for j in range(line.start.y, line.end.y + y_dir, y_dir):

                    field[(i, j)] += 1

        else:

            x_mag = line.end.x - line.start.x
            y_mag = line.end.y - line.start.y

            x_dir = np.sign(x_mag)
            y_dir = np.sign(y_mag)

            steps = abs(x_mag) + 1
            for i in range(steps):

                x = line.start.x + i * x_dir
                y = line.start.y + i * y_dir

                field[(x, y)] += 1

    danger = field >= 2
    print(danger.sum())
