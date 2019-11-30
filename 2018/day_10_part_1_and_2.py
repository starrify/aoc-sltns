# coding: utf8

import sys
import re


def main():
    initial_points = [
        # x, y, vx, vy
        [int(x) for x in re.findall(r'[\d-]+', line)]
        for line in sys.stdin
    ]
    points = [dict(zip(('x', 'y', 'vx', 'vy'), point)) for point in sorted(initial_points)]
    canvas_size = 100
    x_span = points[-1]['x'] - points[0]['x']
    vx_both = points[0]['vx'] - points[-1]['vx']
    time_span = ((x_span - canvas_size) / vx_both, (x_span + canvas_size) / vx_both)
    # XXX: Speed up the calculation using numpy if the data range goes larger
    for t in range(int(time_span[0]), int(time_span[1]) + 1):
        tmp_points = [
            (point['x'] + t * point['vx'], point['y'] + t * point['vy'])
            for point in points
        ]
        by_axis = list(zip(*tmp_points))
        bbox = [
            (min(by_axis[axis]), max(by_axis[axis]))
            for axis in range(2)
        ]
        if any(bbox[axis][1] - bbox[axis][0] > canvas_size for axis in range(2)):
            continue
        figure = [
            ['.' for x in range(bbox[0][0], bbox[0][1] + 1)]
            for y in range(bbox[1][0], bbox[1][1] + 1)
        ]
        for point in tmp_points:
            figure[point[1] - bbox[1][0]][point[0] - bbox[0][0]] = '#'
        print(t)
        # This is the part where we could use a human :sweat-smile:
        for line in figure:
            print(''.join(line))


if __name__ == '__main__':
    main()
