import numpy as np

FLASH_THD = 9

if __name__ == '__main__':

    with open('data/day11.txt', 'r') as f:
        lines = f.readlines()
    
    field = np.zeros((10, 10), dtype=int)
    for i, line in enumerate(lines):
        for j, num in enumerate(line.strip()):
            field[(i, j)] = int(num)


    num_flashes = 0

    step = 0

    while True:
        # Step octopuses
        # 1: Add one to energy level of all octopuses
        field += 1

        # 2: Flash all octopuses and propagate.
        flash = field > FLASH_THD

        while(flash.any()):

            # Iterate over all indices that are above the threshold.
            flashing_octopuses = [tuple(x) for x in np.transpose(flash.nonzero())]
            for flasher in flashing_octopuses:
                field[flasher] = 0

            # For all the flashers, increase adjacent energy by 1, as long as it
            # hasn't already flashed this round.
            for flasher in flashing_octopuses:

                for i in range(min(0, flasher[0] - 1), max(9, flasher[0] + 2)):
                    for j in range(min(0, flasher[1] - 1), max(9, flasher[1] + 2)):

                        if field[(i, j)]:
                            field[(i, j)] += 1
            
            flash = field > FLASH_THD

        num_flashes += len(np.transpose((field == 0).nonzero()))
        step += 1

        simul_flash = field == 0
        if simul_flash.all():
            break

    # print('Number of flashes: {0:d}'.format(num_flashes))
    print('Simultaneous flash: {0:d}'.format(step))
