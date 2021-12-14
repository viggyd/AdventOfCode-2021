import json

if __name__ == '__main__':

    horizontal = 0
    depth = 0
    with open('data/day2.txt', 'r') as f:
        lines = f.readlines()

    for command in lines:
        [direction, mag] = command.split(' ')

        if direction == 'up':
            depth -= int(mag)
        elif direction == 'down':
            depth += int(mag)
        elif direction == 'forward':
            horizontal += int(mag)
    
    print('Horizontal: {0:d}'.format(horizontal))
    print('Depth: {0:d}'.format(depth))
    print('Product: {0:d}'.format(horizontal * depth))


    aim = 0
    horizontal = 0
    depth = 0
    for command in lines:
        [direction, mag] = command.split(' ')
        
        match direction:

            case 'up':
                aim -= int(mag)
            case 'down':
                aim += int(mag)
            case 'forward':
                horizontal += int(mag)
                depth += (int(mag) * aim)

    print('Horizontal: {0:d}'.format(horizontal))
    print('Depth: {0:d}'.format(depth))
    print('Product: {0:d}'.format(horizontal * depth))
