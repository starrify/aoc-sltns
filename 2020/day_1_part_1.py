# coding: utf8

import sys


def main():
    seen = set()
    for line in sys.stdin:
        x = int(line)
        if 2020 - x in seen:
            print(x * (2020 - x))
            break
        seen.add(x)


if __name__ == '__main__':
    main()
