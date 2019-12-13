# coding: utf8

import sys
import re
import collections
import itertools
import math
import functools

import numpy


def lcm(a, b):
    return a * b // math.gcd(a, b)


def main():
    orig_pos = [
        [int(x) for x in re.findall(r'(-?\d+)', line)]
        for line in sys.stdin
    ]
    axis_period = []
    for axis in range(3):
        pos = numpy.array([x[axis] for x in orig_pos], dtype=int)
        vel = numpy.zeros(len(pos), dtype=int)
        step = 0
        state_steps = collections.defaultdict(int)
        state_steps[tuple(pos) + tuple(vel)] = 0
        while True:
            for idx0, idx1 in itertools.permutations(range(len(pos)), 2):
                if pos[idx0] > pos[idx1]:
                    vel[idx0] -= 1
                elif pos[idx0] < pos[idx1]:
                    vel[idx0] += 1
            pos += vel
            step += 1
            state = tuple(pos) + tuple(vel)
            if state in state_steps:
                axis_period.append(step - state_steps[state])
                break
            else:
                state_steps[state] = step
    print(functools.reduce(lcm, axis_period))


if __name__ == '__main__':
    main()
