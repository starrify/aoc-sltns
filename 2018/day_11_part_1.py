# coding: utf8

import sys


def main():
    grid_serial = int(sys.stdin.read().strip())
    grid_size = 300
    accumulate_step = 3
    grid_power = [
        [
            ((i + 11) * (j + 1) + grid_serial) * (i + 11) % 1000 // 100 - 5
            if i < grid_size and j < grid_size
            else 0
            for j in range(grid_size + accumulate_step)
        ]
        for i in range(grid_size + accumulate_step)
    ]
    accumulated = [[0 for _ in range(grid_size + 1)] for _ in range(grid_size + 1)]
    for i in range(grid_size):
        for j in range(grid_size):
            accumulated[i][j] = (
                accumulated[i - 1][j] + accumulated[i][j - 1] - accumulated[i - 1][j - 1]
                + grid_power[i - accumulate_step][j - accumulate_step] + grid_power[i][j]
                - grid_power[i][j - accumulate_step] - grid_power[i - accumulate_step][j]
            )
    max_power = max(accumulated[i][j] for i in range(2, grid_size) for j in range(2, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            if max_power == accumulated[i][j]:
                print(i - accumulate_step + 2, j - accumulate_step + 2, sep=',')


if __name__ == '__main__':
    main()
