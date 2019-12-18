# coding: utf8

import sys
import collections
import operator
import itertools
import re


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


def get_new_position(grids, pos, direction):
    offset = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }[direction]
    new_pos = tuple(pos[x] + offset[x] for x in range(2))
    if not (0 <= new_pos[0] < len(grids) and 0 <= new_pos[1] < len(grids[0])):
        return None
    return new_pos


def get_grid_at_offset(grids, pos, direction):
    new_pos = get_new_position(grids, pos, direction)
    if new_pos is None:
        return None
    return grids[new_pos[0]][new_pos[1]]


def main():
    tape = collections.defaultdict(int, enumerate(int(x) for x in sys.stdin.read().strip().split(',')))
    process = TapeProcess(tape.copy())
    [_ for _ in process.run_tape()]
    grids = ''.join(chr(x) for x in process.output_queue).strip().splitlines()
    print('\n'.join(grids))
    # Assumption is the robot turns only when necessary (cannot go forward).
    # This is surely not right but may be enough for some inputs (e.g. mine).
    pos = [
        (i, j)
        for i, row in enumerate(grids)
        for j, grid in enumerate(row)
        if grid in '^v<>'
    ][0]
    direction = grids[pos[0]][pos[1]]
    actions = []
    while True:
        if get_grid_at_offset(grids, pos, direction) == '#':
            # forward
            pos = get_new_position(grids, pos, direction)
            actions.append('F')
        else:
            for turn in 'LR':
                new_dir = {
                    'L': {
                        '^': '<',
                        'v': '>',
                        '<': 'v',
                        '>': '^',
                    },
                    'R': {
                        '^': '>',
                        'v': '<',
                        '<': '^',
                        '>': 'v',
                    },
                }[turn][direction]
                if get_grid_at_offset(grids, pos, new_dir) == '#':
                    pos = get_new_position(grids, pos, new_dir)
                    direction = new_dir
                    actions.append(turn)
                    actions.append('F')
                    break
            else:
                break
    actions = [
        x if x in 'LR' else len(x)
        for x in re.findall('[LR]|F+', ''.join(actions))
    ]
    print(actions)
    # Assumption (WTF) again is split happens no lower on this "actions" level, which is apparently
    # incorrect but still good enough for some inputs (e.g. mine).
    # Well..
    route = {
        'main': 'ABACBACBAC',
        'A': ['L', 6, 'L', 4, 'R', 12],
        'B': ['L', 6, 'R', 12, 'R', 12, 'L', 8],
        'C': ['L', 6, 'L', 10, 'L', 10, 'L', 6],
    }
    formatted = [
        ','.join(str(x) for x in route[key])
        for key in ('main', 'A', 'B', 'C')
    ]
    new_tape = tape.copy()
    new_tape[0] = 2
    process = TapeProcess(new_tape, init_input=[ord(x) for x in '\n'.join(formatted + ['n', ''])])
    [_ for _ in process.run_tape()]
    print(process.output_queue)


if __name__ == '__main__':
    main()
