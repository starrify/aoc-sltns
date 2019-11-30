# coding: utf8

import sys


def apply_operation(registers, instruction, operation):
    operands = [
        operand if operand_type == 'i' else registers[operand]
        for operand, operand_type in zip(instruction[1:3], operation[:2])
    ]
    tmp_registers = registers[:]
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
    registers = [0] + [0 for _ in range(5)]
    last = None
    seen = set()
    # simulation. takes minutes to finish
    while 0 <= registers[ip_reg] < len(instructions):
        instruction = instructions[registers[ip_reg]]
        if instruction == ['eqrr', 3, 0, 4]:
            # as per the input program
            if registers[3] not in seen:
                seen.add(registers[3])
                last = registers[3]
                print(last)
            else:
                print(last)
                break
        registers = apply_operation(
            registers,
            instruction,
            opcodes[instruction[0]]
        )
        registers[ip_reg] += 1


def main2():
    r1, r3, r4 = 0, 0, 0
    last = None
    seen = set()
    found = False
    while True:
        r1 = r3 | 65536
        r3 = 9450265
        while True:
            r4 = r1 & 255
            r3 += r4
            r3 = ((r3 & 16777215) * 65899) & 16777215
            if r1 < 256:
                if r3 not in seen:
                    seen.add(r3)
                    last = r3
                else:
                    found = True
                    print(last)
                break
            r1 /= 256
        if found:
            break


if __name__ == '__main__':
    # brute-force simulation. takes minutes to finish
    #main()
    # reimplementing the original program in Python. takes less than 1 second
    main2()
