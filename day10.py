import statistics

END_CHARS = [')', ']', '}', '>']

MATCHING_CHUNK = {
    '(': ')',
    '{': '}',
    '[': ']',
    '<': '>'
}

SCORE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

INCOMPLETE_SCORE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

def check_syntax(syntax):

    depth_chars = list()

    for char in syntax:

        # Case: We have an opening character for a chunk
        if char in MATCHING_CHUNK:
            depth_chars.append(char)
    
        # Case: End character for a chunk. Check to make sure it closes the 
        #       correct item for what depth we're on.
        elif char in END_CHARS:

            expected_end = MATCHING_CHUNK[depth_chars[-1]]
            if char == expected_end:
                depth_chars.pop()
            else:
                # print('Expected: {0:s}, but found {1:s} instead'.format(expected_end, char))
                return SCORE[char], True
    
    # Calculate incompelte score
    score = 0
    depth_chars = [x for x in depth_chars if x]
    for char in reversed(depth_chars):

        score = score * 5 + INCOMPLETE_SCORE[MATCHING_CHUNK[char]]

    return score, False


if __name__ == '__main__':

    with open('data/day10.txt', 'r') as f:
        lines = f.readlines()

    corrupt_score = 0
    incomplete_scores = list()
    for line in lines:
        score, corrupt = check_syntax(line.strip())

        if corrupt:
            corrupt_score += score
        else:
            incomplete_scores.append(score)


    print('Corrupt Score: {0:d}'.format(corrupt_score))
    print('Incomplete Score: {0:d}'.format(statistics.median(incomplete_scores)))
