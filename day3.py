import json

if __name__ == '__main__':

    with open('data/day3.json', 'r') as f:
        readings = json.load(f)

    num_readings = len(readings)
    gamma_rate = 0
    bit_width = len(readings[0])

    readings_str = readings
    readings = [int(reading, base=2) for reading in readings]
    common_bits = []

    # Iterate over all bit positions
    for i in range(bit_width):

        # Iterate over all readouts
        # Shift right by i, then mask to get only the last bit.
        sum_bits = sum([(x >> i) & 0x1 for x in readings])
        common_bits.append(sum_bits >= num_readings/2)

        gamma_rate = gamma_rate + ((sum_bits >= num_readings/2) << i)

    eps_rate = ~gamma_rate & 0xFFF

    # print('Gamma rate (bin): {0:s}'.format(''.join(reversed(common_bits))))
    print('Gamma rate: {0:d}'.format(gamma_rate))
    print('Epsilon rate: {0:d}'.format(eps_rate))
    print('Power Output: {0:d}'.format(gamma_rate * eps_rate))

    # oxy_candidate = max([~(reading ^ gamma_rate) for reading in readings])
    # oxy = readings.index(oxy_candidate)

    oxy_candidates = readings
    co2_candidates = readings

    for i in reversed(range(bit_width)):

        # Determine common bit at this position.
        oxy_sum = sum([(x >> i) & 0x1 for x in oxy_candidates])
        oxy_bit = oxy_sum >= len(oxy_candidates)/2

        co2_sum = sum([(x >> i) & 0x1 for x in co2_candidates])
        co2_bit = co2_sum >= len(co2_candidates)/2

        # Update the candidates.
        oxy_candidates = [x for x in oxy_candidates if ((x >> i) & 0x1) == int(oxy_bit)]

        if len(oxy_candidates) == 1:
            oxy = oxy_candidates[0]

        co2_candidates = [x for x in co2_candidates if ((x >> i) & 0x1) != co2_bit]
        if len(co2_candidates) == 1:
            co2 = co2_candidates[0]


    print('Oxygen: {0:d}'.format(oxy))
    print('CO2: {0:d}'.format(co2))
    print('Output: {0:d}'.format(oxy * co2))
