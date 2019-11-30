# coding: utf8

import sys
import re


def main():
    robots = []
    for line in sys.stdin:
        tmp_numbers = [int(x) for x in re.findall('[0-9-]+', line)]
        robots.append({
            'id': len(robots),
            'pos': tuple(tmp_numbers[:3]),
            'r': tmp_numbers[-1],
            'covers': set(),
        })
    for idx, robot in enumerate(robots):
        for j in range(idx, len(robots)):
            dist = sum(abs(x[0] - x[1]) for x in zip(robot['pos'], robots[j]['pos']))
            if dist <= robot['r']:
                robot['covers'].add(j)
            if dist <= robots[j]['r']:
                robots[j]['covers'].add(idx)
    largest = max(robots, key=lambda x: x['r'])
    print(len(largest['covers']))


if __name__ == '__main__':
    main()
