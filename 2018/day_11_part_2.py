# coding: utf8

import sys


def main():
    grid_serial = int(sys.stdin.read().strip())
    grid_size = 300
    max_step = 300
    grid_power = [
        [
            ((i + 11) * (j + 1) + grid_serial) * (i + 11) % 1000 // 100 - 5
            if i < grid_size and j < grid_size
            else 0
            for j in range(grid_size + max_step)
        ]
        for i in range(grid_size + max_step)
    ]
    accumulated = [[[0 for _ in range(max_step + 1)] for _ in range(grid_size + 1)] for _ in range(grid_size + 1)]
    max_power = (float('-inf'), None)
    for step in range(1, max_step + 1):
        for i in range(grid_size):
            for j in range(grid_size):
                accumulated[i][j][step] = (
                    accumulated[i - 1][j][step] + accumulated[i][j - 1][step] - accumulated[i - 1][j - 1][step]
                    + grid_power[i - step][j - step] + grid_power[i][j]
                    - grid_power[i][j - step] - grid_power[i - step][j]
                )
                max_power = max(max_power, (accumulated[i][j][step], i - step + 2, j - step + 2, step))
    print(*max_power[1:], sep=',')


if __name__ == '__main__':
    main()
