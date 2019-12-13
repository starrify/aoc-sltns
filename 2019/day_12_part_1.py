# coding: utf8

import sys
import re
import itertools

import numpy


def main():
    pos = [
        numpy.array([int(x) for x in re.findall(r'(-?\d+)', line)], dtype=int)
        for line in sys.stdin
    ]
    vel = [numpy.zeros(3, dtype=int) for _ in pos]
    for _ in range(1000):
        for idx0, idx1 in itertools.permutations(range(len(pos)), 2):
            for axis in range(3):
                if pos[idx0][axis] > pos[idx1][axis]:
                    vel[idx0][axis] -= 1
                elif pos[idx0][axis] < pos[idx1][axis]:
                    vel[idx0][axis] += 1
        for idx in range(len(pos)):
            pos[idx] += vel[idx]
    print(numpy.multiply(*(numpy.absolute(x).sum(axis=1) for x in (pos, vel))).sum())


if __name__ == '__main__':
    main()
