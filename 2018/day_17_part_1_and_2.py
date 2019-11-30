# coding: utf8

import sys
import itertools


def main():
    clays = []
    for line in sys.stdin:
        tmp_range = [
            sorted([int(y) for y in x[1].split('..')])
            for x in sorted([x.split('=') for x in line.strip().split(', ')])
        ][::-1]
        clays.extend(list(itertools.product(*[
            range(tmp_range_axis[0], tmp_range_axis[-1] + 1)
            for tmp_range_axis in tmp_range
        ])))
    by_axis = list(zip(*clays))
    bbox = [(min(x), max(x)) for x in by_axis]
    clays = [
        (x - bbox[0][0] + 1, y - bbox[1][0] + 1)
        for x, y in clays
    ]
    canvas = [
        ['.' for y in range(bbox[1][1] - bbox[1][0] + 3)]
        for x in range(bbox[0][1] - bbox[0][0] + 3)
    ]
    for clay in clays:
        canvas[clay[0]][clay[1]] = '#'
    directions = {
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }
    source = (0, 500 - bbox[1][0] + 1)
    canvas[source[0]][source[1]] = 'w'
    water_grids = {
        # pos: water
        source: {
            'pos': source,
            'freedom': set('v'),
        },
    }
    active = [source]  # pos
    while active:
        new_active = []
        for pos in active:
            water = water_grids[pos]
            if pos[0] + 1 < len(canvas) and canvas[pos[0] + 1][pos[1]] == '.':
                water['freedom'] = set('v')
            for direction in list(water['freedom']):
                step = directions[direction]
                adjacent = tuple(sum(x) for x in zip(pos, step))
                if not 0 <= adjacent[0] < len(canvas):
                    continue
                if not 0 <= adjacent[1] < len(canvas[0]):
                    continue
                if canvas[adjacent[0]][adjacent[1]] == '.':
                    canvas[adjacent[0]][adjacent[1]] = 'w'
                    new_active.append(adjacent)
                    water_grids[adjacent] = {
                        'pos': adjacent,
                        'freedom': set(water['freedom']),
                    }
                elif direction == 'v' and (
                        canvas[adjacent[0]][adjacent[1]] == '#'
                        or adjacent in water_grids and not water_grids[adjacent]['freedom']
                    ):
                    water['freedom'] = set('<>')
                    new_active.append(pos)
                elif (
                        canvas[adjacent[0]][adjacent[1]] == '#'
                        or direction in '<>' and not water_grids[adjacent]['freedom'].intersection([direction, 'v'])
                        or direction == 'v' and not water_grids[adjacent]['freedom']
                    ):
                    water['freedom'].remove(direction)
                    if not water['freedom']:
                        above = (pos[0] - 1, pos[1])
                        if above in water_grids:
                            new_active.append(above)
                    prev = tuple(sum(x) for x in zip(pos, (-x for x in step)))
                    if prev in water_grids:
                        new_active.append(prev)
        active = list(set(new_active))
    print(len([
        pos
        for pos in water_grids
        if 0 < pos[0] < len(canvas) - 1
    ]))
    print(len([
        pos
        for pos, water in water_grids.items()
        if 0 < pos[0] < len(canvas) - 1 and not water['freedom']
    ]))


if __name__ == '__main__':
    main()
