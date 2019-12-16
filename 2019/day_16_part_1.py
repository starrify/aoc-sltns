# coding: utf8

import sys
import itertools
import operator


def main():
    signals = [int(x) for x in sys.stdin.read().strip()]
    base_pattern = [0, 1, 0, -1]
    for phase in range(100):
        new_signals = []
        for idx in range(len(signals)):
            pattern = itertools.cycle(itertools.chain.from_iterable([
                itertools.repeat(x, idx + 1) for x in base_pattern
            ]))
            next(pattern)
            value = abs(sum(itertools.starmap(operator.mul, zip(signals, pattern)))) % 10
            new_signals.append(value)
        signals = new_signals
    print(''.join(str(x) for x in new_signals[:8]))


if __name__ == '__main__':
    main()
