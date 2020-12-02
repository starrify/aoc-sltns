# coding: utf8

import sys
import re


def main():
    valid_count = 0
    for line in sys.stdin:
        lower, upper, letter, password = re.search(r'(\d+)-(\d+) (\S): (\S+)', line).groups()
        if int(lower) <= password.count(letter) <= int(upper):
            valid_count += 1
    print(valid_count)


if __name__ == '__main__':
    main()
