import json
import collections

if __name__ == '__main__':

    # File input.
    with open('data/day14.json', 'r') as f:
        data = json.load(f)

    polymer = data['polymer']
    rules = data['rules']

    # Initialize the pairs data structure based on the initial string.
    pairs = collections.defaultdict(int)
    for i in range(len(polymer) - 1):
        pairs[polymer[i:i+2]] += 1


    # Perform the polymerization.
    new_poly = polymer
    for step in range(40):

        # Iterate over all pairs that currently exist.
        new_pairs = collections.defaultdict(int)
        for pair, num in pairs.items():

            # Check their polymerization rule.
            new_item = rules[pair]

            # Create new pairs based on the polymerization rule.
            new_pairs[pair[0] + new_item] += num
            new_pairs[new_item + pair[1]] += num

        # Perform a deep copy to repeat this step on the new set of pairs.
        pairs = {k: v for k, v in new_pairs.items()}

    # Count up all the letter frequencies (each pair has a letter appearing twice)
    counts = collections.defaultdict(int)
    for pair, count in pairs.items():
        counts[pair[0]] += count/2
        counts[pair[1]] += count/2

    # Add 1/2 for the beginning/end letters since they only ever appear once.
    counts[polymer[0]] += 0.5
    counts[polymer[-1]] += 0.5

    # Print result.
    diff = max(counts.values()) - min(counts.values())
    print('Difference: {0:d}'.format(int(diff)))
