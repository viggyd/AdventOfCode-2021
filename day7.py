import json

def create_parser(reading):

    readings = reading.split(' ')

    num_def = {x: '' for x in range(10)}
    num_read = dict()
    seg_def = dict()

    # Convert each readout into a set of characters
    readings_set = [set([x for x in reading]) for reading in readings]


    # Get the unique segment numbers.
    for reading in readings_set:

        match len(reading):
            case 2:
                num_read[1] = reading
            case 4:
                num_read[4] = reading
            case 3:
                num_read[7] = reading
            case 7:
                num_read[8] = reading
    
    
    # Segment A is the set '7'\'1'.
    seg_def['a'] = num_read[7] - num_read[1]


    # Now, find all 6-segment numbers. The only 6-segment number without all
    # the same segments of '7' is '6'.
    six_seg_numbers = [x for x in readings_set if len(x) == 6]
    num_read[6] = [x for x in six_seg_numbers if len(x - num_read[7]) == 4][0]

    # Segment B is '8'\'6'.
    # Segment C is '1' - 'SegB'
    seg_def['b'] = num_read[8] - num_read[6]
    seg_def['c'] = num_read[1] - seg_def['b']


    # Get all 5-segment numbers. We can use Segments A, B, and C to figure out 
    # which numbers they are.
    five_seg_nums = [x for x in readings_set if len(x) == 5]
    for num in five_seg_nums:

        if num_read[7].issubset(num):
            num_read[3] = num
        
        elif set.union(seg_def['a'], seg_def['b']).issubset(num):
            num_read[2] = num
        
        elif set.union(seg_def['a'], seg_def['c']).issubset(num):
            num_read[5] = num

    # Using 2/3, find segment E.
    seg_def['e'] = (num_read[2] - num_read[7]) - (num_read[3] - num_read[7])


    # We can find 0/9 by finding out which of the 6-segment numbers have '7'
    # as a subset.
    nums_09 = [x for x in six_seg_numbers if num_read[7].issubset(x)]
    
    # Find the index where Segment E is a subset.
    e_idx = 0 if seg_def['e'].issubset(nums_09[0]) else 1
    num_read[0] = nums_09.pop(e_idx)
    num_read[9] = nums_09[0]

    # Segment G is '8'\'0'
    seg_def['g'] = num_read[8] - num_read[0]

    # Using '3' - '7' - 'G', we can get Segment D
    # Using '9' - '3', we can get Segment F. All done!
    seg_def['d'] = num_read[3] - num_read[7] - seg_def['g']
    seg_def['f'] = num_read[9] - num_read[3]

    parse_map = dict()
    for segment, definition in seg_def.items():
        def_letter = list(definition)
        parse_map[def_letter[0]] = segment

    return parse_map


def unscramble_digits(parser, digits):

    num_seg_map = {
        'abcdef': '0',
        'bc': '1',
        'abdeg': '2',
        'abcdg': '3',
        'bcfg': '4',
        'acdfg': '5',
        'acdefg': '6',
        'abc': '7',
        'abcdefg': '8',
        'abcdfg': '9'
    }

    unscambled_digits = list()
    for digit in digits.split(' '):

        unscambled_digits.append(''.join(sorted([parser[x] for x in digit])))
    
    unscambled_digits = [num_seg_map[x] for x in unscambled_digits]
    return unscambled_digits

if __name__ == '__main__':

    with open('data/day7.txt', 'r') as f:
        lines = f.readlines()

    

    parser = create_parser('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab')
    digits = unscramble_digits(parser, 'cdfeb fcadb cdfeb cdbaf')



    num_digits = 0
    digit_sum = 0
    for line in lines:

        [reading, digits_reading] = line.strip().split(' | ')
        parser = create_parser(reading)
        digits = unscramble_digits(parser, digits_reading)

        digit_sum += int(''.join(digits))


        num_digits += digits.count('1')
        num_digits += digits.count('4')
        num_digits += digits.count('7')
        num_digits += digits.count('8')





    print('Number of 1, 4, 7, 8: {0:d}'.format(num_digits))
    print('Sum: {0:d}'.format(digit_sum))
