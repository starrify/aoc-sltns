# coding: utf8

import sys
import collections
import itertools
import operator


def new_pos_at_direction(pos, direction):
    return tuple(itertools.starmap(operator.add, zip(pos, direction)))


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
    portals = {}
    for label, pos in labels.items():
        if label in ('AA', 'ZZ'):
            continue
        portals[pos[0]] = pos[1]
        portals[pos[1]] = pos[0]
    min_dist = collections.defaultdict(lambda: float('inf'))
    min_dist[labels['AA'][0]] = 0
    pending = collections.deque([labels['AA'][0]])
    while pending:
        pos = pending.popleft()
        check_positions = [new_pos_at_direction(pos, direction) for direction in directions]
        if pos in portals:
            check_positions.append(portals[pos])
        for new_pos in check_positions:
            if grids[new_pos] == '.':
                dist = min_dist[pos] + 1
                if dist < min_dist[new_pos]:
                    min_dist[new_pos] = dist
                    pending.append(new_pos)
    print(min_dist[labels['ZZ'][0]])


if __name__ == '__main__':
    main()
