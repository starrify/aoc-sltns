# coding: utf8

import sys


def main():
    coordinates = [
        [int(x) for x in line.split(', ')]
        for line in sys.stdin
    ]
    by_axis = list(zip(*coordinates))
    bbox = [
        min(by_axis[0]), min(by_axis[1]), max(by_axis[0]), max(by_axis[1])
    ]
    locations = [[{'x': i, 'y': j} for j in range(bbox[3] + 1)] for i in range(bbox[2] + 1)]
    active_set = []
    for idx, coord in enumerate(coordinates):
        loc = locations[coord[0]][coord[1]]
        loc['nearest'] = [idx]
        loc['shortest'] = 0
        active_set.append(loc)
    def _within_range(x, y):
        return bbox[0] <= x <= bbox[2] and bbox[1] <= y <= bbox[3]
    while active_set:
        current_loc = active_set[0]
        active_set = active_set[1:]
        if len(current_loc['nearest']) > 1:
            continue
        for direction in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            x = current_loc['x'] + direction[0]
            y = current_loc['y'] + direction[1]
            if not _within_range(x, y):
                continue
            loc = locations[x][y]
            dist = current_loc['shortest'] + 1
            if 'shortest' not in loc or dist < loc['shortest']:
                loc['shortest'] = dist
                loc['nearest'] = current_loc['nearest'].copy()
                active_set.append(loc)
            elif loc['shortest'] == dist and current_loc['nearest'][0] not in loc['nearest']:
                loc['nearest'].append(current_loc['nearest'][0])
            elif loc['shortest'] > dist:
                raise Exception('unexpected')
    idx_area = {idx: 0 for idx in range(len(coordinates))}
    on_edge = set()
    for i in range(bbox[0], bbox[2] + 1):
        for j in range(bbox[1], bbox[3] + 1):
            loc = locations[i][j]
            if len(loc['nearest']) == 1:
                idx_area[loc['nearest'][0]] += 1
            if i in (bbox[0], bbox[2]) or j in (bbox[1], bbox[3]):
                on_edge.update(loc['nearest'])
    print(sorted([area for idx, area in idx_area.items() if idx not in on_edge])[-1])


if __name__ == '__main__':
    main()
