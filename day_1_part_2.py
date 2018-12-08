# coding: utf8

import sys
import itertools
import collections


def main():
    deltas = [int(x) for x in sys.stdin.read().strip().split()]
    # XXX: Simulation is not a good approach here. Shall have tried finding
    # the subarray of which the sum is zero.
    count = collections.defaultdict(int)
    current = 0
    for delta in itertools.cycle(deltas):
        current += delta
        count[current] += 1
        if count[current] == 2:
            print(current)
            break


if __name__ == '__main__':
    main()
