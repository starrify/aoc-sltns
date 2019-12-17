# coding: utf8

import sys


def main():
    input_str = sys.stdin.read().strip()
    offset = int(input_str[:7])
    signals = [int(x) for x in input_str] * 10000
    assert offset >= len(signals) // 2
    for _ in range(100):
        for i in range(len(signals) - 2, max(len(signals) // 2, offset) - 1, -1):
            signals[i] += signals[i + 1]
            signals[i] %= 10
    print(''.join(str(x) for x in signals[offset:offset + 8]))


if __name__ == '__main__':
    main()
