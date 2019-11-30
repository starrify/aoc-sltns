# coding: utf8

import sys


def main():
    coordinates = [
        [int(x) for x in line.split(', ')]
        for line in sys.stdin
    ]
    n_coords = len(coordinates)
    max_dist = 10000
    extra_range = max_dist // n_coords + 1
    coord_by_axis = [sorted(x) for x in list(zip(*coordinates))]
    coord_by_axis_cnt = [{coord: coords.count(coord) for coord in coords} for coords in coord_by_axis]
    cost_by_axis = [
        [None for _ in range(coord_by_axis[axis][-1] + 2 * extra_range)]
        for axis in range(2)
    ]
    for axis in range(2):
        left_cnt = 0
        for pos in range(coord_by_axis[axis][0] - extra_range, coord_by_axis[axis][-1] + extra_range + 1):
            if cost_by_axis[axis][pos - 1] is None:
                cost_by_axis[axis][pos] = sum(coord_by_axis[axis]) - pos * n_coords
            else:
                cost_by_axis[axis][pos] = cost_by_axis[axis][pos - 1] + 2 * left_cnt - n_coords
            left_cnt += coord_by_axis_cnt[axis].get(pos, 0)
    y0 = coord_by_axis[1][0]
    y1 = coord_by_axis[1][-1]
    total_area = 0
    for x in range(coord_by_axis[0][0] - extra_range, coord_by_axis[0][-1] + extra_range + 1):
        cost = cost_by_axis[0][x]
        while cost + cost_by_axis[1][y0] < max_dist:
            y0 -= 1
        while cost + cost_by_axis[1][y0] >= max_dist and cost_by_axis[1][y0 + 1] < cost_by_axis[1][y0]:
            y0 += 1
        while cost + cost_by_axis[1][y1] < max_dist:
            y1 += 1
        while cost + cost_by_axis[1][y1] >= max_dist and cost_by_axis[1][y1 - 1] < cost_by_axis[1][y1]:
            y1 -= 1
        if cost + cost_by_axis[1][y0] >= max_dist:
            continue
        total_area += y1 - y0 + 1
    print(total_area)


if __name__ == '__main__':
    main()
