import json

WINDOW_SIZE = 3

if __name__ == '__main__':

    with open('data/d1p1.json', 'r') as f:
        data = json.load(f)

    num_inc = 0
    prev_meas = data[0]
    for measurement in data[1:]:

        if measurement > prev_meas:
            num_inc += 1
        
        prev_meas = measurement

    print('Number increase: {0:d}'.format(num_inc))

    
    num_inc = 0
    prev_win_sum = sum(data[0:WINDOW_SIZE])
    for i in range(1, len(data) - 2):

        curr_win_sum = sum(data[i:WINDOW_SIZE + i])
        if curr_win_sum > prev_win_sum:
            num_inc += 1
        
        prev_win_sum = curr_win_sum

    print('Window increase: {0:d}'.format(num_inc))
