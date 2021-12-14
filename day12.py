import networkx as nx
import collections

from networkx.generators import small

def generate_node(node):

    node_dict = {
        'name': node,
        'start': False,
        'end': False,
        'cave': '',
        'visited': False
    }

    if node == 'start':
        node_dict['start'] = True
    elif node == 'end':
        node_dict['end'] = True
    elif node.islower():
        node_dict['cave'] = 'small'
    else:
        node_dict['cave'] = 'big'

    return node_dict

def determine_small_visit_twice(curr_path):
    
    small_caves = [x for x in curr_path if x.islower()]
    counts = collections.Counter(small_caves)

    count_vals = [x > 1 for x in counts.values()]
    return any(count_vals)


def traverse_system(cave_system, current_node, curr_path=list(), valid_paths=list()):


    # Base Case 1: Current node is the end node.
    # This is a valid path. Increment the number of valid paths.
    if current_node['end']:
        valid_paths.append([x for x in curr_path + ['end']])
        return
    
    # Base Case 2: The current node is the start node or a previously visited
    # small cave. These types are invalid, don't increment the valid paths, but return.
    if current_node['visited'] and current_node['start']:
        return

    # Get all lowercase caves in current path.

    if current_node['cave'] == 'small':
        if current_node['name'] in curr_path:
            if determine_small_visit_twice(curr_path):
                return


    curr_path.append(current_node['name'])

    # Otherwise, make sure to mark this node as visited.
    current_node['visited'] = True

    # Get neighbors of the current node.
    for neighbor in cave_system.neighbors(current_node['name']):
        traverse_system(cave_system, cave_system.nodes[neighbor], curr_path, valid_paths)

    # return valid_paths
    curr_path.pop()



if __name__ == '__main__':

    with open('data/day12.txt', 'r') as f:
        lines = f.readlines()
    
    cave_system = nx.Graph()

    known_nodes = list()
    for line in lines:
        [start, end] = line.strip().split('-')

        if start not in known_nodes:
            cave_system.add_nodes_from([(start, generate_node(start))])
            known_nodes.append(start)

        if end not in known_nodes:
            cave_system.add_nodes_from([(end, generate_node(end))])
            known_nodes.append(end)

        cave_system.add_edge(start, end)

    start = cave_system.nodes['start']
    valid_paths = list()
    curr_path = list()
    traverse_system(cave_system, start, curr_path, valid_paths)

    print('Number of valid paths: {0:d}'.format(len(valid_paths)))
    # print('Valid paths: {0:d}'.format(paths))
