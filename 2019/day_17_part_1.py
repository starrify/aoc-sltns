# coding: utf8

import sys
import collections
import operator
import itertools


class EndExecution(BaseException):
    pass


class TapeProcess:

    def __init__(self, tape, init_input=None, init_output=None, init_run=True):
        self.tape = tape
        self.pc = 0
        self.state = None
        self.process = None
        self.input_queue = collections.deque(init_input or [])
        self.output_queue = collections.deque(init_output or [])
        self.relative_base = 0
        if init_run:
            self.run_tape()

    def get_input(self):
        return self.input_queue.popleft()

    def put_output(self, value):
        self.output_queue.append(value)

    def adjust_relative_base(self, value):
        self.relative_base += value

    def _run_tape(self):
        opcodes = {
            1: ('iio', operator.add),
            2: ('iio', operator.mul),
            3: ('o', self.get_input),
            4: ('i', self.put_output),
            5: ('iip', lambda x, y: y if x else None),
            6: ('iip', lambda x, y: y if not x else None),
            7: ('iio', lambda x, y: 1 if x < y else 0),
            8: ('iio', lambda x, y: 1 if x == y else 0),
            9: ('i', self.adjust_relative_base),
            99: ('', lambda: exec('raise EndExecution')),
        }
        try:
            while True:
                opcode = self.tape[self.pc] % 100
                io_modes, func = opcodes[opcode]
                new_pc = self.pc + 1 + len([x for x in io_modes if x != 'p'])
                io_ref_modes = list(zip(
                    io_modes,
                    itertools.chain(str(self.tape[self.pc] // 100)[::-1], itertools.repeat('0'))
                ))
                operands = []
                for idx, (io_mode, ref_mode) in enumerate(io_ref_modes):
                    if io_mode == 'i':
                        operand = self.tape[self.pc + idx + 1]
                        if ref_mode == '0':
                            # position mode
                            operand = self.tape[operand]
                        elif ref_mode == '1':
                            # immediate mode
                            pass
                        elif ref_mode == '2':
                            # relative mode
                            operand = self.tape[self.relative_base + operand]
                        else:
                            raise ValueError('Invalid ref mode %s at %s' % (ref_mode, self.pc))
                        operands.append(operand)
                outcome = func(*operands)
                if isinstance(outcome, int) or outcome is None:
                    # shortcut for lazy people..
                    outcome = [outcome]
                outcome_idx = 0
                for idx, (io_mode, ref_mode) in enumerate(io_ref_modes):
                    value = outcome[outcome_idx]
                    if io_mode == 'o':
                        output_param = self.tape[self.pc + idx + 1]
                        if ref_mode == '0':
                            # position mode
                            self.tape[output_param] = value
                        elif ref_mode == '2':
                            # relative mode
                            self.tape[self.relative_base + output_param] = value
                        else:
                            raise ValueError('Invalid ref mode %s at %s' % (ref_mode, self.pc))
                    elif io_mode == 'p':
                        if value is not None:
                            new_pc = value
                    else:
                        continue
                    outcome_idx += 1
                self.pc = new_pc
                if opcode == 4:
                    yield
        except EndExecution:
            self.state = 'halted'
            return

    def run_tape(self):
        self.state = 'running'
        self.process = self._run_tape()
        return self.process


def main():
    tape = collections.defaultdict(int, enumerate(int(x) for x in sys.stdin.read().strip().split(',')))
    process = TapeProcess(tape)
    [_ for _ in process.run_tape()]
    grids = ''.join(chr(x) for x in process.output_queue).strip().splitlines()
    print('\n'.join(grids))
    ans = 0
    for i, row in enumerate(grids):
        for j, grid in enumerate(row):
            if grid != '#':
                continue
            is_intersection = True
            for direction in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                pos = (i + direction[0], j + direction[1])
                if not (0 <= pos[0] < len(grids) and 0 <= pos[1] < len(row)):
                    is_intersection = False
                    continue
                if grids[pos[0]][pos[1]] != '#':
                    is_intersection = False
            if is_intersection:
                ans += i * j
    print(ans)


if __name__ == '__main__':
    main()
