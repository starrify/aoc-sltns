# coding: utf8

import sys
import re

import numpy


def main():
    max_n = 1001  # large enough for now
    canvas = -numpy.ones((max_n, max_n), dtype=numpy.dtype('int'))
    for line in sys.stdin:
        if not line:
            continue
        x, y, width, height = [int(x) for x in re.split(r'\D+', line.strip())[2:]]
        canvas[x:x+width, y:y+height] += numpy.ones((width, height), dtype=numpy.dtype('int'))
    print(canvas.clip(0, 1).sum())


if __name__ == '__main__':
    main()
