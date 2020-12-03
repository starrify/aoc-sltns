# coding: utf8

import sys


def main():
    grids = sys.stdin.read().splitlines()
    ans = 0
    for idx, line in enumerate(grids):
        if line[3 * idx % len(line)] == '#':
            ans += 1
    print(ans)


if __name__ == '__main__':
    main()
