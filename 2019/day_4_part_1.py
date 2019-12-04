# coding: utf8

import sys
import functools


@functools.lru_cache(maxsize=None)
def count_up_to(target, need_duplicate=True, prev=None):
    # return number of valid passwords from all zeros to target
    if prev is not None and target[0] < prev:
        return 0
    if len(target) == 1:
        if need_duplicate:
            if prev is not None and prev <= target[0]:
                return 1
            else:
                return 0
        else:
            return max(target[0] - (prev or 0) + 1, 0)
    ret = 0
    for initial in range(prev or 0, target[0]):
        ret += count_up_to(
            tuple(9 for _ in target[1:]),
            need_duplicate=need_duplicate and initial != prev,
            prev=initial
        )
    ret += count_up_to(
        target[1:],
        need_duplicate=need_duplicate and target[0] != prev,
        prev=target[0]
    )
    return ret


def main():
    input_range = [tuple(map(int, x)) for x in sys.stdin.read().strip().split('-')]
    print(count_up_to(input_range[1]) - count_up_to(input_range[0]))


if __name__ == '__main__':
    main()
