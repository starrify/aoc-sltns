# coding: utf8

import sys
import collections
import operator
import itertools


TILE_PADDLE = 3
TILE_BALL = 4


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
        self.tiles = {}
        self.last_positions = {}
        self.score = None
        if init_run:
            self.run_tape()

    def get_input(self):
        if not all(x in self.last_positions for x in (TILE_PADDLE, TILE_BALL)):
            # no move
            return 0
        if self.last_positions[TILE_PADDLE][0] < self.last_positions[TILE_BALL][0]:
            # right
            return 1
        elif self.last_positions[TILE_PADDLE][0] > self.last_positions[TILE_BALL][0]:
            # left
            return -1
        else:
            # no move
            return 0

    def put_output(self, value):
        self.output_queue.append(value)
        if len(self.output_queue) == 3:
            pos = (self.output_queue[0], self.output_queue[1])
            tile = self.output_queue[2]
            if pos == (-1, 0):
                # special score output
                self.score = tile
            else:
                self.tiles[pos] = tile
                if tile in (TILE_PADDLE, TILE_BALL):
                    # assuming only one instance
                    self.last_positions[tile] = pos
            self.output_queue.clear()

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
    tape[0] = 2
    process = TapeProcess(tape, init_input=[1])
    [_ for _ in process.run_tape()]
    print(process.score)


if __name__ == '__main__':
    main()
