# coding: utf8

import sys
import itertools
import functools


def parse_wires(input_wire):
    directions = {
        'R': (1, 0),
        'L': (-1, 0),
        'U': (0, 1),
        'D': (0, -1),
    }
    curr_node = (0, 0)
    segments = []
    for move in input_wire:
        step = int(move[1:])
        new_node = tuple(
            curr_node[x] + step * directions[move[0]][x]
            for x in range(2)
        )
        segments.append((curr_node, new_node))
        curr_node = new_node
    return segments


def point_on_segment(point, segment):
    return any(
        point[x] == segment[0][x] == segment[1][x]
        and (segment[0][x ^ 1] - point[x ^ 1]) * (segment[1][x ^ 1] - point[x ^ 1]) <= 0
        for x in range(2)
    )


def segment_intersection(seg0, seg1):
    """
    Returns:
    - No point if no intersection
    - Or the one point of intersection
    - Or the two ending points of intersection if overlapping
    """
    overlapping = set(
        x
        for x in seg0 + seg1
        if all(point_on_segment(x, seg) for seg in (seg0, seg1))
    )
    if overlapping:
        # may contain 0, 1, or 2 points
        yield from overlapping
        return
    for axis in range(2):
        if seg0[0][axis] == seg0[1][axis] and seg1[0][axis ^ 1] == seg1[1][axis ^ 1]:
            crossing = (seg0[0][axis], seg1[0][axis ^ 1])
            if axis == 1:
                crossing = crossing[::-1]
            if all(point_on_segment(crossing, seg) for seg in (seg0, seg1)):
                yield crossing


def steps_between_points(point0, point1):
    return sum(abs(point0[x] - point1[x]) for x in range(2))


@functools.lru_cache(maxsize=None)
def steps_up_to_index(wire, index):
    if index > 0:
        prev = steps_up_to_index(wire, index - 1)
    else:
        prev = 0
    return prev + steps_between_points(*wire[index])


def main():
    wires = tuple(
        tuple(parse_wires(x.split(',')))
        for x in sys.stdin.read().splitlines()
    )
    min_steps = float('inf')
    for (idx0, seg0), (idx1, seg1) in itertools.product(*map(enumerate, wires)):
        for point in segment_intersection(seg0, seg1):
            if point == (0, 0):
                continue
            steps = sum(
                steps_up_to_index(wires[x], (idx0, idx1)[x] - 1)
                + steps_between_points((seg0, seg1)[x][0],  point)
                for x in range(2)
            )
            min_steps = min(min_steps, steps)
    print(min_steps)


if __name__ == '__main__':
    main()
