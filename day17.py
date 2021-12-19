import math
import collections
import json

def calculate_max_k_x(dest_x):
    return math.ceil(math.sqrt(2*dest_x))


def calc_vel_from_dest_step(dest, step):
    return ((2 * dest)/float(step) + step - 1)/2.0

def calc_pos_from_vel_k(init_vel, step):
    return -1/2.0 * step * (step - 2 * init_vel - 1)

if __name__ == '__main__':
    
    target = {
        'x': (32, 65),
        'y': (-225, -177)
    }

    candidates = list()
    for x in range(target['x'][0], target['x'][1] + 1):

        max_k = calculate_max_k_x(x)

        x_vel_candidates = list()
        for k in range(1, max_k + 1):

            vel_x = calc_vel_from_dest_step(x, k)
            if vel_x.is_integer() and k <= vel_x:
                candidates.append({'vel': int(vel_x), 'k': k})



    k_y_vel = collections.defaultdict(list)
    for y_vel in range(target['y'][0], -target['y'][0]):
        
        k = 1
        pos = target['y'][0] + 1

        while pos > target['y'][0]:
            
            pos = calc_pos_from_vel_k(y_vel, k)
            if target['y'][0] <= pos <= target['y'][1]:
                k_y_vel[k].append(y_vel)

            k += 1




    count = 0
    candidates_sort = sorted(candidates, key=lambda d: d['vel'])
    valid_vels = set()

    for candidate in candidates_sort:

        if candidate['k'] >= candidate['vel']:
            k_candidates = [k for k in k_y_vel.keys() if k >= candidate['vel']]
        else:
            k_candidates = [candidate['k']]


        for k in k_candidates:

            for y_vel in k_y_vel[k]:
                valid_vels.add((candidate['vel'], y_vel))


    print('Combinations: {0:d}'.format(len(valid_vels)))


