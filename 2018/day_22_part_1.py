# coding: utf8

import sys


def main():
    depth = int(sys.stdin.readline().strip().split()[-1])
    target = tuple(int(x) for x in sys.stdin.readline().strip().split()[-1].split(','))
    geologic_index = [
        [None for _ in range(target[1] + 1)]
        for _ in range(target[0] + 1)
    ]
    target_sum = 0
    for x in range(target[0] + 1):
        for y in range(target[1] + 1):
            if x == 0:
                geologic_index[x][y] = y * 48271
            elif y == 0:
                geologic_index[x][y] = x * 16807
            elif (x, y) == target:
                geologic_index[x][y] = 0
            else:
                geologic_index[x][y] = (geologic_index[x - 1][y] + depth) * (geologic_index[x][y - 1] + depth) % 20183
            target_sum += (geologic_index[x][y] + depth) % 20183 % 3
    print(target_sum)


if __name__ == '__main__':
    main()
