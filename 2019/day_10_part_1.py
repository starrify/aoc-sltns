# coding: utf8

import sys
import collections
import math


def normalize_vector(vector):
    if vector[0] == vector[1] == 0:
        pass
    elif vector[0] == 0:
        vector = (0, vector[1] / abs(vector[1]))
    elif vector[1] == 0:
        vector = (vector[0] / abs(vector[0]), 0)
    else:
        divisor = math.gcd(*vector)  # always non-negative
        vector = tuple(x / divisor for x in vector)
    return vector


def check_detection(detections, node0, node1):
    diff_vec = tuple(node1[x] - node0[x] for x in range(2))
    normalized = normalize_vector(diff_vec)
    detections[node0].add(normalized)


def main():
    region_map = sys.stdin.read().splitlines()
    asteroids = [
        (i, j)
        for i, row in enumerate(region_map)
        for j, cell in enumerate(row)
        if cell == '#'
    ]
    detections = collections.defaultdict(set)
    for i in range(len(asteroids)):
        for j in range(i + 1, len(asteroids)):
            check_detection(detections, asteroids[i], asteroids[j])
            check_detection(detections, asteroids[j], asteroids[i])
    print(max(len(x) for x in detections.values()))
    

if __name__ == '__main__':
    main()
