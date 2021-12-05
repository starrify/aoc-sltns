# coding: utf8

import sys
import collections
import itertools
import operator


def verify_tree_structure(grids, items):
    nodes = collections.defaultdict(dict)
    pending = collections.deque([items['@']])
    visited = set()
    non_tree_nodes = []
    while pending:
        pos = pending.popleft()
        visited.add(pos)
        for direction in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            new_pos = tuple(itertools.starmap(operator.add, zip(pos, direction)))
            if grids[new_pos] == '#':
                continue
            if nodes[pos].get('parent') == new_pos:
                continue
            elif new_pos in visited:
                non_tree_nodes.append(pos)
                continue
            else:
                nodes[pos].setdefault('children', []).append(new_pos)
                nodes[new_pos]['parent'] = pos
                pending.append(new_pos)
    # assuming the graph is indeed a tree (except for the central 3x3 block)
    assert len(set(non_tree_nodes)) == 4


def main():
    grids = {
        (i, j): grid
        for i, row in enumerate(sys.stdin.read().splitlines())
        for j, grid in enumerate(row)
    }
    items = {
        item: pos
        for pos, item in grids.items()
        if item not in '.#'
    }
    verify_tree_structure(grids, items)



    return

    signals = [int(x) for x in sys.stdin.read().strip()]
    base_pattern = [0, 1, 0, -1]
    for phase in range(100):
        new_signals = []
        for idx in range(len(signals)):
            pattern = itertools.cycle(itertools.chain.from_iterable([
                itertools.repeat(x, idx + 1) for x in base_pattern
            ]))
            next(pattern)
            value = abs(sum(itertools.starmap(operator.mul, zip(signals, pattern)))) % 10
            new_signals.append(value)
        signals = new_signals
    print(''.join(str(x) for x in new_signals[:8]))


if __name__ == '__main__':
    main()
