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
        if init_run:
            self.run_tape()

    def get_input(self):
        return self.input_queue.popleft()

    def put_output(self, value):
        self.output_queue.append(value)

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
            99: ('', lambda: exec('raise EndExecution')),
        }
        try:
            while True:
                opcode = self.tape[self.pc] % 100
                io_modes, func = opcodes[opcode]
                new_pc = self.pc + 1 + len([x for x in io_modes if x != 'p'])
                ref_modes = itertools.chain(str(self.tape[self.pc] // 100)[::-1], itertools.repeat('0'))
                operands = []
                for idx, (io_mode, ref_mode) in enumerate(zip(io_modes, ref_modes)):
                    if io_mode == 'i':
                        operand = self.tape[self.pc + idx + 1]
                        if ref_mode == '0':
                            # position mode
                            operand = self.tape[operand]
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
                        self.tape[self.tape[self.pc + idx + 1]] = value
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
    orig_tape = collections.defaultdict(int, enumerate(int(x) for x in sys.stdin.read().strip().split(',')))
    max_output = float('-inf')
    max_output_signals = None
    for signals in itertools.permutations(range(5, 10)):
        process = []
        curr_tape = 0
        last_output = 0
        pending_signals = collections.deque(signals)
        while True:
            try:
                if len(process) <= curr_tape:
                    process.append(TapeProcess(orig_tape.copy()))
                    process[curr_tape].input_queue.append(pending_signals.popleft())
                if process[curr_tape].state == 'halted':
                    break
                process[curr_tape].input_queue.append(last_output)
                process[curr_tape].process.send(None)
            except StopIteration:
                pass
            last_output = process[curr_tape].output_queue[-1]
            curr_tape += 1
            curr_tape %= len(signals)
        if last_output > max_output:
            max_output = last_output
            max_output_signals = signals
    print(max_output, max_output_signals)


if __name__ == '__main__':
    main()
