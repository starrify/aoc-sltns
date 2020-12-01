# coding: utf8

import sys


def main():
    seen = set()
    twos = {}
    for line in sys.stdin:
        x = int(line)
        if 2020 - x in twos:
            print(x * twos[2020 - x])
            break
        for y in seen:
            twos[x + y] = x * y
        seen.add(x)


if __name__ == '__main__':
    main()
