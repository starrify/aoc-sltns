# coding: utf8

import sys
import collections
import operator


def main():
    tape = collections.defaultdict(int, enumerate(int(x) for x in sys.stdin.read().strip().split(',')))
    tape[1], tape[2] = 12, 2
    pc = 0
    while True:
        op_func = {
            1: operator.add,
            2: operator.mul,
        }
        if tape[pc] == 99:
            break
        elif tape[pc] in op_func:
            tape[tape[pc + 3]] = op_func[tape[pc]](tape[tape[pc + 1]], tape[tape[pc + 2]])
        pc += 4
    print(tape[0])


if __name__ == '__main__':
    main()
