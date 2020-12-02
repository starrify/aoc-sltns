# coding: utf8

import sys
import re


def main():
    valid_count = 0
    for line in sys.stdin:
        lower, upper, letter, password = re.search(r'(\d+)-(\d+) (\S): (\S+)', line).groups()
        if list(password[int(x) - 1] for x in (upper, lower)).count(letter) == 1:
            valid_count += 1
    print(valid_count)


if __name__ == '__main__':
    main()
