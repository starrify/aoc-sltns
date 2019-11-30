# coding: utf8

import sys


def get_root(parents, node):
    if parents[node] != node:
        parents[node] = get_root(parents, parents[node])
    return parents[node]


def main():
    points = [
        tuple(int(x) for x in line.strip().split(','))
        for line in sys.stdin
    ]
    connectivity = [[] for _ in points]
    for i, point in enumerate(points):
        for j in range(i + 1, len(points)):
            dist = sum(abs(x - y) for x, y in zip(point, points[j]))
            if dist <= 3:
                connectivity[i].append(j)
                connectivity[j].append(i)
    parents = list(range(len(points)))
    for idx in range(len(points)):
        for connected in connectivity[idx]:
            parents[get_root(parents, connected)] = get_root(parents, idx)
    print(len(set(get_root(parents, x) for x in range(len(points)))))


if __name__ == '__main__':
    main()
