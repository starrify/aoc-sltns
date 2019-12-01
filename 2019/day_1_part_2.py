# coding: utf8

import sys


def fuel_for_mass(n):
    return max(n // 3 - 2, 0)


def fuel_for_mass_recursively(n):
    ret = 0
    while n > 0:
        n = fuel_for_mass(n)
        ret += n
    return ret


def main():
    modules = [int(x) for x in sys.stdin.read().strip().split()]
    print(sum(fuel_for_mass_recursively(x) for x in modules))


if __name__ == '__main__':
    main()
