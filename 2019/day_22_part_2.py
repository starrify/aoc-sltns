# coding: utf8

import sys

import numpy


def matpow(base, exp, mod):
    # assuming always handling 2x2 matrices
    ret = numpy.eye(2, dtype=object)
    while exp:
        if exp & 1:
            ret = numpy.matmul(ret, base) % mod
        base = numpy.matmul(base, base) % mod
        exp >>= 1
    return ret


def main():
    deck_size = 119315717514047
    repeat_times = 101741582076661
    transform = numpy.eye(2, dtype=object)
    for line in sys.stdin.read().splitlines():
        if line == 'deal into new stack':
            transform = numpy.matmul(transform, numpy.array(((-1, -1), (0, 1)), dtype=object))
        elif line.startswith('cut'):
            cut = int(line.split()[-1]) % deck_size
            transform = numpy.matmul(transform, numpy.array(((1, cut), (0, 1)), dtype=object))
        elif line.startswith('deal with increment'):
            increment = int(line.split()[-1])
            # assuming the given deck size is always a prime
            modinv = pow(increment, deck_size - 2, deck_size)
            transform = numpy.matmul(transform, numpy.array(((modinv, 0), (0, 1)), dtype=object))
        else:
            raise ValueError(line)
        transform = transform % deck_size
    transform = matpow(transform, repeat_times, deck_size)
    print(numpy.matmul(transform, numpy.array((2020, 1), dtype=object)) % deck_size)


if __name__ == '__main__':
    main()
