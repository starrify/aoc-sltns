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
        3: ('o', lambda: 5),
        4: ('i', print),
        5: ('iip', lambda x, y: y if x else None),
        6: ('iip', lambda x, y: y if not x else None),
        7: ('iio', lambda x, y: 1 if x < y else 0),
        8: ('iio', lambda x, y: 1 if x == y else 0),
        99: ('', lambda: exec('raise EndExecution')),
    }
    pc = 0
    try:
        while True:
            opcode = tape[pc] % 100
            io_modes, func = opcodes[opcode]
            new_pc = pc + 1 + len([x for x in io_modes if x != 'p'])
            ref_modes = itertools.chain(str(tape[pc] // 100)[::-1], itertools.repeat('0'))
            operands = []
            for idx, (io_mode, ref_mode) in enumerate(zip(io_modes, ref_modes)):
                if io_mode == 'i':
                    operand = tape[pc + idx + 1]
                    if ref_mode == '0':
                        # position mode
                        operand = tape[operand]
                    elif ref_mode == '1':
                        # immediate mode
                        pass
                    else:
                        raise ValueError('Invalid ref mode %s at %s' % (ref_mode))
                    operands.append(operand)
            outcome = func(*operands)
            if isinstance(outcome, int) or outcome is None:
                # shortcut for lazy people..
                outcome = [outcome]
            outcome_idx = 0
            for idx, (io_mode, ref_mode) in enumerate(zip(io_modes, ref_modes)):
                value = outcome[outcome_idx]
                if io_mode == 'o':
                    # position mode
                    assert ref_mode == '0'
                    tape[tape[pc + idx + 1]] = value
                elif io_mode == 'p':
                    if value is not None:
                        new_pc = value
                else:
                    continue
                outcome_idx += 1
            pc = new_pc
    except EndExecution:
        pass
    return tape


def main():
    tape = collections.defaultdict(int, enumerate(int(x) for x in sys.stdin.read().strip().split(',')))
    run_tape(tape)


if __name__ == '__main__':
    main()
