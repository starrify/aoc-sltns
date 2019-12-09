# coding: utf8

import sys
import collections
import operator
import itertools


class EndExecution(BaseException):
    pass


def run_tape(tape):
    opcodes = {
        1: ('iio', operator.add),
        2: ('iio', operator.mul),
        3: ('o', lambda: 1),
        4: ('i', print),
        99: ('', lambda: exec('raise EndExecution')),
    }
    pc = 0
    try:
        while True:
            opcode = tape[pc] % 100
            io_modes, func = opcodes[opcode]
            io_ref_modes = list(zip(
                io_modes,
                itertools.chain(str(tape[pc] // 100)[::-1], itertools.repeat('0'))
            ))
            operands = []
            for idx, (io_mode, ref_mode) in enumerate(io_ref_modes):
                if io_mode == 'i':
                    operand = tape[pc + idx + 1]
                    if ref_mode == '0':
                        # position mode
                        operand = tape[operand]
                    elif ref_mode == '1':
                        # immediate mode
                        pass
                    else:
                        raise ValueError('Invalid ref mode %s at %s' % (ref_mode, pc))
                    operands.append(operand)
            outcome = func(*operands)
            if isinstance(outcome, int):
                # shortcut for lazy people..
                outcome = [outcome]
            outcome_idx = 0
            for idx, (io_mode, ref_mode) in enumerate(io_ref_modes):
                if io_mode == 'o':
                    # position mode
                    assert ref_mode == '0'
                    tape[tape[pc + idx + 1]] = outcome[outcome_idx]
                    outcome_idx += 1
            pc += 1 + len(io_modes)
    except EndExecution:
        pass
    return tape


def main():
    tape = collections.defaultdict(int, enumerate(int(x) for x in sys.stdin.read().strip().split(',')))
    run_tape(tape)


if __name__ == '__main__':
    main()
