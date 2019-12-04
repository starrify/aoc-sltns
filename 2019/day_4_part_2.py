# coding: utf8

import sys
import functools


@functools.lru_cache(maxsize=None)
def count_up_to(target, need_duplicate=True, prev=None, same_prev=0):
    # return number of valid passwords from all zeros to target
    if len(target) == 0:
        if not need_duplicate or same_prev == 2:
            return 1
        else:
            return 0
    if prev is not None and target[0] < prev:
        return 0
    ret = 0
    for initial in range(prev or 0, target[0]):
        ret += count_up_to(
            tuple(9 for _ in target[1:]),
            need_duplicate=need_duplicate and not (initial != prev and same_prev == 2),
            prev=initial,
            same_prev=same_prev + 1 if initial == prev or prev is None else 1
        )
    ret += count_up_to(
        target[1:],
        need_duplicate=need_duplicate and not (target[0] != prev and same_prev == 2),
        prev=target[0],
        same_prev=same_prev + 1 if target[0] == prev or prev is None else 1
    )
    return ret


def main():
    input_range = [tuple(map(int, x)) for x in sys.stdin.read().strip().split('-')]
    print(count_up_to(input_range[1]) - count_up_to(input_range[0]))


if __name__ == '__main__':
    main()
