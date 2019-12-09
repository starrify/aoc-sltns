# coding: utf8

import sys
import collections
import operator
import itertools


class EndExecution(BaseException):
    pass


class TapeIO:

    def __init__(self, init_input=None, init_output=None):
        self.input_queue = collections.deque(init_input or [])
        self.output_queue = collections.deque(init_output or [])

    def get_input(self):
        return self.input_queue.popleft()

    def put_output(self, value):
        self.output_queue.append(value)


def run_tape(tape, tape_io=None):
    if tape_io is None:
        tape_io = TapeIO()
    opcodes = {
        1: ('iio', operator.add),
        2: ('iio', operator.mul),
        3: ('o', tape_io.get_input),
        4: ('i', tape_io.put_output),
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
            if isinstance(outcome, int) or outcome is None:
                # shortcut for lazy people..
                outcome = [outcome]
            outcome_idx = 0
            for idx, (io_mode, ref_mode) in enumerate(io_ref_modes):
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
    return tape, tape_io


def main():
    orig_tape = collections.defaultdict(int, enumerate(int(x) for x in sys.stdin.read().strip().split(',')))
    max_output = float('-inf')
    max_output_signals = None
    for signals in itertools.permutations(range(5)):
        tape = orig_tape.copy()
        previous_output = 0
        for curr_signal in signals:
            tape_io = TapeIO(init_input=[curr_signal, previous_output])
            tape, tape_io = run_tape(tape, tape_io)
            previous_output = tape_io.output_queue[0]
        if previous_output > max_output:
            max_output = previous_output
            max_output_signals = signals
    print(max_output, max_output_signals)


if __name__ == '__main__':
    main()
