# coding: utf8

import sys
import collections


def main():
    lines = [line.strip() for line in sys.stdin]
    canvas = [[' ' for _ in lines[0] + '##']] + [
        [' '] + list(line) + [' ']
        for line in lines
    ] + [[' ' for _ in lines[0] + '##']]
    directions = [
        (x, y)
        for x in [-1, 0, 1]
        for y in [-1, 0, 1]
        if (x, y) != (0, 0)
    ]
    for _ in range(10):
        new_canvas = [x.copy() for x in canvas]
        for x in range(1, len(canvas) - 1):
            for y in range(1, len(canvas[x]) - 1):
                # XXX: No need for a more efficient counting method
                count = collections.defaultdict(int)
                for direction in directions:
                    count[canvas[x + direction[0]][y + direction[1]]] += 1
                if canvas[x][y] == '.':
                    # open
                    if count['|'] >= 3:
                        new_canvas[x][y] = '|'
                elif canvas[x][y] == '|':
                    # tree
                    if count['#'] >= 3:
                        new_canvas[x][y] = '#'
                elif canvas[x][y] == '#':
                    # lumberyard
                    if count['#'] < 1 or count['|'] < 1:
                        new_canvas[x][y] = '.'
        canvas = new_canvas
    tmp = [
        sum(x.count(check) for x in canvas)
        for check in '|#'
    ]
    print(tmp[0] * tmp[1])


if __name__ == '__main__':
    main()
