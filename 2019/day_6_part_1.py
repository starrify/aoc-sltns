# coding: utf8

import sys


def get_depth(parents, depth, node):
    if node not in depth:
        if node in parents:
            depth[node] = get_depth(parents, depth, parents[node]) + 1
        else:
            # root
            depth[node] = 0
    return depth[node]


def main():
    edges = [x.strip().split(')') for x in sys.stdin]
    parents = {}
    for parent, child in edges:
        parents[child] = parent
    depth = {}
    print(sum(get_depth(parents, depth, x) for x in parents))


if __name__ == '__main__':
    main()
