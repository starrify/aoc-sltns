# coding: utf8

import sys
import collections
import itertools
import operator


def new_pos_at_direction(pos, direction):
    return tuple(itertools.starmap(operator.add, zip(pos, direction)))


def dist_to_center(center, pos):
    # assuming the playground is nested squares (than arbitrary rectangles)
    return max(abs(center[x] - pos[x]) for x in range(2))


def main():
    grids = {
        (i, j): grid
        for i, row in enumerate(sys.stdin.read().splitlines())
        for j, grid in enumerate(row)
    }
    directions = (
        (-1, 0),
        (0, -1),
        (0, 1),
        (1, 0),
    )
    labels = {}
    for pos, grid in grids.items():
        if grid != '.':
            continue
        for direction in directions:
            new_pos = new_pos_at_direction(pos, direction)
            if 'A' <= grids[new_pos] <= 'Z':
                label = [grids[x] for x in (new_pos, new_pos_at_direction(new_pos, direction))]
                if direction in ((-1, 0), (0, -1)):
                    label = label[::-1]
                labels.setdefault(''.join(label), []).append(pos)
                break
    center = tuple(max(pos[x] for pos in grids) // 2 for x in range(2))
    portals = {}
    for label, pos in labels.items():
        if label in ('AA', 'ZZ'):
            continue
        if dist_to_center(center, pos[0]) > dist_to_center(center, pos[1]):
            # ensure pos[0] is the inner one
            pos = pos[::-1]
        portals[pos[0]] = (pos[1], 1)
        portals[pos[1]] = (pos[0], -1)
    min_dist = collections.defaultdict(lambda: float('inf'))
    pending = collections.deque([(labels['AA'][0], 0)])
    min_dist[pending[0]] = 0
    target_found = False
    while pending and not target_found:
        pos, level = pending.popleft()
        check_positions = [
            (new_pos_at_direction(pos, direction), level)
            for direction in directions
        ]
        if pos in portals:
            new_level = level + portals[pos][1]
            if new_level >= 0:
                check_positions.append((portals[pos][0], new_level))
        for new_pos_level in check_positions:
            if grids[new_pos_level[0]] == '.':
                dist = min_dist[(pos, level)] + 1
                if dist < min_dist[new_pos_level]:
                    min_dist[new_pos_level] = dist
                    pending.append(new_pos_level)
                    if new_pos_level == (labels['ZZ'][0], 0):
                        target_found = True
    print(min_dist[(labels['ZZ'][0], 0)])


if __name__ == '__main__':
    main()
