# coding: utf8

import sys


def main():
    mem = {}
    for line in sys.stdin:
        cmd = line.split()
        if cmd[0] == 'mask':
            mask = cmd[2]
            assert len(mask) == 36
            mask_1 = int(mask.replace('X', '0'), 2)
            mask_float = int(mask.replace('0', '1').replace('X', '0'), 2)
            float_bits = [1 << (35 - idx) for idx, bit in enumerate(mask) if bit == 'X'][::-1]
            float_iter = [
                sum(bit for idx, bit in enumerate(float_bits) if (i >> idx) & 1)
                for i in range(1 << len(float_bits))
            ]
        else:
            addr = int(cmd[0].split('[')[-1].rstrip(']'))
            addr |= mask_1
            addr &= mask_float
            for float_value in float_iter:
                mem[addr | float_value] = int(cmd[2])
    print(sum(mem.values()))


if __name__ == '__main__':
    main()
