# coding: utf8

import sys
import functools
import operator


def main():
    grids = sys.stdin.read().splitlines()
    counts = []
    for right, down in (
            (1, 1),
            (3, 1),
            (5, 1),
            (7, 1),
            (1, 2),
        ):
        count = 0
        for i in range(0, len(grids), down):
            if grids[i][right * i // down % len(grids[i])] == '#':
                count += 1
        counts.append(count)
    print(functools.reduce(operator.mul, counts, 1))


if __name__ == '__main__':
    main()
