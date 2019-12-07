# coding: utf8

import sys


def main():
    edges = [x.strip().split(')') for x in sys.stdin]
    parents = {}
    for parent, child in edges:
        parents[child] = parent
    depth = {}
    dist = None
    for node in ('YOU', 'SAN'):
        curr_depth = 0
        while True:
            if node in depth:
                dist = depth[node] + curr_depth
                break
            depth[node] = curr_depth
            curr_depth += 1
            if node in parents:
                node = parents[node]
            else:
                break
    print(dist - 2)


if __name__ == '__main__':
    main()
