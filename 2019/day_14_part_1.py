# coding: utf8

import sys
import collections

import regex


def main():
    reactions = {}  # reactions[name] = (amount, [(name, amount), ...])
    for line in sys.stdin:
        captures = regex.search(
            '(?:(?P<src_cnt>\d+) (?P<src_name>\w+)(?:, )?)+ => (?P<dst_cnt>\d+) (?P<dst_name>\w+)',
            line
        ).capturesdict()
        reactions[captures['dst_name'][0]] = (
            int(captures['dst_cnt'][0]),
            list(zip(captures['src_name'], map(int, captures['src_cnt']))),
        )
    needed = collections.defaultdict(int, {'FUEL': 1})
    needed_by = collections.defaultdict(set)
    for dst, (_, src) in reactions.items():
        for src_name, _ in src:
            needed_by[src_name].add(dst)
    pending = collections.deque(['FUEL'])
    while pending:
        dst = pending.popleft()
        dst_cnt = needed.pop(dst)
        n_reactions = (dst_cnt + reactions[dst][0] - 1) // reactions[dst][0]
        for src, src_cnt in reactions[dst][1]:
            needed[src] += n_reactions * src_cnt
            needed_by[src].remove(dst)
            if not needed_by[src] and src != 'ORE':
                pending.append(src)
    print(needed)


if __name__ == '__main__':
    main()
