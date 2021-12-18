import json

from numpy import product
import bitstruct

OPERATOR_MAP = {
    0: 'sum',
    1: 'prod',
    2: 'min',
    3: 'max',
    5: 'gt',
    6: 'lt',
    7: 'eq'
}


def bin_from_hex(hex_str):

    parts = ['{0:04b}'.format(int(x, base=16)) for x in hex_str]
    return ''.join(parts)


def parse_literal(tx_str, idx=0):

    indicator = 1
    subparts = list()
    while indicator:

        indicator = int(tx_str[idx], base=2)
        subparts.append(tx_str[idx + 1: idx + 5])

        idx += 5

    return int(''.join(subparts), base=2), idx



def parse_n(tx_str, n=1, idx=0):

    item = int(tx_str[idx: idx + n], base=2)
    return item, idx + n


def parse_operator(tx_str, packet=dict(), idx=0):

    len_type, idx =  parse_n(tx_str, 1, idx)
    subpackets = list()
    if len_type:
        packet_num, idx = parse_n(tx_str, 11, idx)
        for _ in range(packet_num):
            sub_pkt = dict()
            sub_pkt, idx = parse_packet(tx_str, idx)
            subpackets.append(sub_pkt)

    else:
        packet_bit_len, idx = parse_n(tx_str, 15, idx)
        sub_str = tx_str[idx:idx + packet_bit_len]
        sub_idx = 0

        while sub_idx < len(sub_str):
            sub_pkt = dict()
            sub_pkt, sub_idx = parse_packet(sub_str, sub_idx)
            subpackets.append(sub_pkt)

        idx += len(sub_str)

    return subpackets, idx

def parse_packet(tx_str, idx=0):

    # Assume string is in binary.
    packet = dict()
    while idx < len(tx_str) and '1' in tx_str[idx:]:
        packet['version'], idx = parse_n(tx_str, 3, idx)
        tx_type, idx =  parse_n(tx_str, 3, idx)

        match tx_type:

            case 4:
                literal, idx = parse_literal(tx_str, idx)
                packet['type'] = 'literal'
                packet['value'] = literal
                return packet, idx
            case _:
                packet['type'] = 'operator'
                packet['operator'] = OPERATOR_MAP[tx_type]

                subpackets, idx = parse_operator(tx_str, packet, idx)
                packet['subpackets'] = [x for x in subpackets]

                return packet, idx



def calculate_version_sum(packet, curr_sum=0):

    curr_sum += packet['version']

    # Base case: No subpackets.
    if 'subpackets' not in packet:
        return curr_sum

    # Else: increment the sum for all subpackets.
    for subpkt in packet['subpackets']:
        curr_sum += calculate_version_sum(subpkt)
    
    return curr_sum


def perform_operations(packet):


    try:
        subpackets = packet['subpackets']
    except KeyError:
        return packet['value']

    # If all subpackets are of the literal type, we can perform the operation and
    # set the value. Otherwise, recurse.
    if not all([x['type'] == 'literal' for x in subpackets]):

        for sub_pkt in subpackets:
            sub_pkt['value'] = perform_operations(sub_pkt)
        

    # If we got here, we have some work to do.
    val_array = [x['value'] for x in subpackets]
    match packet['operator']:

        case 'sum':
            return sum(val_array)
        case 'prod':
            return product(val_array)
        case 'min':
            return min(val_array)
        case 'max':
            return max(val_array)
        case 'gt':
            return int(val_array[0] > val_array[1])
        case 'lt':
            return int(val_array[0] < val_array[1])
        case 'eq':
            return int(val_array[0] == val_array[1])




if __name__ == '__main__':

    with open('data/day16.txt', 'r') as f:
        hex_str = f.readline().strip()

    # tx_str = bin_from_hex('9C0141080250320F1802104A08')
    tx_str = bin_from_hex(hex_str)

    idx = 0
    packet = dict()
    packet, _ = parse_packet(tx_str)
    version_sum = calculate_version_sum(packet)
    op_sum = perform_operations(packet)

    print('Version sum: {0:d}'.format(version_sum))
    print('Operation: {0:d}'.format(op_sum))

