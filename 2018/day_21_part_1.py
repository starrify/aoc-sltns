# coding: utf8

import sys


def apply_operation(registers, instruction, operation):
    operands = [
        operand if operand_type == 'i' else registers[operand]
        for operand, operand_type in zip(instruction[1:3], operation[:2])
    ]
    tmp_registers = registers.copy()
    tmp_registers[instruction[3]] = operation[2](*operands)
    return tmp_registers


def main():
    ip_reg = int(next(sys.stdin).strip().split('#ip ')[-1])
    instructions = [
        [
            int(x) if x.isdigit() else x
            for x in line.strip().split()
        ]
        for line in sys.stdin
    ]
    opcodes = {
        'addr': ['r', 'r', lambda x, y: x + y],
        'addi': ['r', 'i', lambda x, y: x + y],
        'mulr': ['r', 'r', lambda x, y: x * y],
        'muli': ['r', 'i', lambda x, y: x * y],
        'banr': ['r', 'r', lambda x, y: x & y],
        'bani': ['r', 'i', lambda x, y: x & y],
        'borr': ['r', 'r', lambda x, y: x | y],
        'bori': ['r', 'i', lambda x, y: x | y],
        'setr': ['r', 'i', lambda x, y: x],
        'seti': ['i', 'i', lambda x, y: x],
        'gtir': ['i', 'r', lambda x, y: 1 if x > y else 0],
        'gtri': ['r', 'i', lambda x, y: 1 if x > y else 0],
        'gtrr': ['r', 'r', lambda x, y: 1 if x > y else 0],
        'eqir': ['i', 'r', lambda x, y: 1 if x == y else 0],
        'eqri': ['r', 'i', lambda x, y: 1 if x == y else 0],
        'eqrr': ['r', 'r', lambda x, y: 1 if x == y else 0],
    }
    registers = [1] + [0 for _ in range(5)]
    while 0 <= registers[ip_reg] < len(instructions):
        instruction = instructions[registers[ip_reg]]
        if instruction == ['eqrr', 3, 0, 4]:
            # as per the input program
            print(registers[3])
            break
        registers = apply_operation(
            registers,
            instruction,
            opcodes[instruction[0]]
        )
        registers[ip_reg] += 1


if __name__ == '__main__':
    main()
