# coding: utf8

import sys
import collections
import math

import numpy


def vector_from_nodes(node0, node1):
    return tuple(node1[x] - node0[x] for x in range(2))


def vector_length(vector):
    return sum(x ** 2 for x in vector) ** 0.5


def normalize_vector_int(vector):
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
    vec = vector_from_nodes(node0, node1)
    int_normalized = normalize_vector_int(vec)
    detections[node0][int_normalized].append((vector_length(vec), node1))


def direction_for_sorting(vector):
    vec = numpy.array(vector)
    vec /= numpy.linalg.norm(vec)
    if vector[1] >= 0:
        return (0, numpy.cross(numpy.array([0, -1]), vec))
    else:
        return (1, numpy.cross(numpy.array([0, 1]), vec))


def main():
    region_map = sys.stdin.read().splitlines()
    asteroids = [
        (i, j)
        for i, row in enumerate(region_map)
        for j, cell in enumerate(row)
        if cell == '#'
    ]
    detections = collections.defaultdict(lambda: collections.defaultdict(list))
    for i in range(len(asteroids)):
        for j in range(i + 1, len(asteroids)):
            check_detection(detections, asteroids[i], asteroids[j])
            check_detection(detections, asteroids[j], asteroids[i])
    max_detected = []
    for asteroid, detected in detections.items():
        if len(detected) > len(max_detected):
            max_detected = detected
    sorted_dirs = sorted([
        (direction_for_sorting(direction), sorted(nodes)[::-1])
        for direction, nodes in max_detected.items()
    ])
    picked_nodes = []
    while sorted_dirs:
        for _, nodes in sorted_dirs:
            picked_nodes.append(nodes.pop()[1])
        sorted_dirs = [x for x in sorted_dirs if x[1]]
    print(picked_nodes[199][1] * 100 + picked_nodes[199][0])
    

if __name__ == '__main__':
    main()
