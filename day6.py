import json
import collections



if __name__ == '__main__':

    with open('data/day6.json', 'r') as f:
        data = json.load(f)


    # data = [3,4,3,1,2]

    # Get all fish ages and store in dictionary.
    fish_ages = dict()
    for i in range(9):
        fish_ages[str(i)] = data.count(i)


    days = 256

    for i in range(days):
        # Age the fish.
        fish_ages = {
            '0': fish_ages['1'],
            '1': fish_ages['2'],
            '2': fish_ages['3'],
            '3': fish_ages['4'],
            '4': fish_ages['5'],
            '5': fish_ages['6'],
            '6': fish_ages['7'] + fish_ages['0'],
            '7': fish_ages['8'],
            '8': fish_ages['0'],
        }
        # print('{0:03d} Day(s) Complete'.format(i + 1))

    # Count the number of fish.
    print('Fish: {0:d}'.format(sum(list(fish_ages.values()))))

