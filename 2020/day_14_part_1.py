# coding: utf8

import sys


def main():
    mem = {}
    mask = None
    for line in sys.stdin:
        cmd = line.split()
        if cmd[0] == 'mask':
            mask = cmd[2]
        else:
            value = list(bin(int(cmd[2]))[2:])
            value = ['0' for _ in range(36 - len(value))] + value
            for idx, bit in enumerate(mask):
                if bit != 'X':
                    value[idx] = bit
            mem[cmd[0]] = int(''.join(value), 2)
    print(sum(mem.values()))


if __name__ == '__main__':
    main()
