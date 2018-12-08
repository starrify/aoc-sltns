# coding: utf8

import sys
import collections


def main():
    count = {
        2: 0,
        3: 0,
    }
    for line in sys.stdin.read().splitlines():
        tmp_count = collections.defaultdict(int)
        for letter in line:
            tmp_count[letter] += 1
        count_set = set(tmp_count.values())
        for check in (2, 3):
            if check in count_set:
                count[check] += 1
    print(count)
    print(count[2] * count[3])


if __name__ == '__main__':
    main()
