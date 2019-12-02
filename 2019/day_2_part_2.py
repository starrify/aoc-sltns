# coding: utf8

import sys
import collections
import operator
import itertools


def run_tape(tape):
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
    return tape


def main():
    orig_tape = collections.defaultdict(int, enumerate(int(x) for x in sys.stdin.read().strip().split(',')))
    for noun, verb in itertools.product(range(100), repeat=2):
        tape = orig_tape.copy()
        tape[1], tape[2] = noun, verb
        if run_tape(tape)[0] == 19690720:
            print(100 * noun + verb)


if __name__ == '__main__':
    main()
