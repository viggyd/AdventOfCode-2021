import json
import sys
import collections
import numpy as np

class Board(object):

    def __init__(self, lines) -> None:
        
        self.board = dict()
        self.bingo = False
        self.marked_coords = np.zeros((5,5), dtype=int)
        
        for row, line in enumerate(lines):
            numbers = line.split(' ')
            numbers = [int(x) for x in numbers if x]
            for i, number in enumerate(numbers):
                self.board[number] = {
                    'coordinate': (row, i),
                    'marked': False
                }

    def set_win_num(self, win_num):
        self.win_num = win_num

    def call_number(self, number):

        try:
            self.board[number]['marked'] = True
            self.marked_coords[self.board[number]['coordinate']] = 1
        except KeyError:
            return False, 0

        bingo = self.check_bingo()
        if bingo:
            self.bingo = True
            return True, self.get_score()
        else:
            return False, 0

    def check_bingo(self):
        
        rows = self.marked_coords.sum(axis=0)
        cols = self.marked_coords.sum(axis=1)
        
        return any([x == 5 for x in rows]) or any([x == 5 for x in cols])
    

    def get_score(self):

        nums = [num for num, data in self.board.items() if not data['marked']]
        return sum(nums)

if __name__ == '__main__':
    

    boards = []
    with open('data/day4.txt', 'r') as f:
        lines = f.readlines()
    
    numbers = lines[0]
    numbers = [int(x) for x in numbers.split(',')]
    print(len(lines[1:]))
    
    for i in range(int(len(lines[1:])/6)):

        s_idx = (i * 6) + 2
        e_idx = (i + 1) * 6 + 1

        boards.append(Board(lines[s_idx:e_idx]))



    bingo = False
    score = 0
    round = 1
    for call in numbers:
        for i, board in enumerate(boards):
            bingo, score = board.call_number(call)

            if bingo:
                print('Score: {0:d}'.format(score))
                print('Final score: {0:d}\n'.format(score * call))

        boards = [board for board in boards if not board.bingo]
        print('Round: {1:d}: {0:d} Boards remaining.'.format(len(boards), round))
        if not len(boards):
            break
        
        round += 1
