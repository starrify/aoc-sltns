# coding: utf8

import sys
import re


def apply_operation(registers, instruction, operation):
    operands = [
        operand if operand_type == 'i' else registers[operand]
        for operand, operand_type in zip(instruction[1:3], operation[:2])
    ]
    tmp_registers = registers.copy()
    tmp_registers[instruction[3]] = operation[2](*operands)
    return tmp_registers


def main():
    lines = [x.strip() for x in sys.stdin]
    cursor = 0
    executions = []
    instructions = []
    while cursor < len(lines):
        if 'before' in lines[cursor].lower():
            executions.append(dict(zip(
                ['before', 'instruction', 'after'],
                [
                    [
                        int(x)
                        for x in re.findall(r'\d+', lines[cursor + i])
                    ]
                    for i in range(3)
                ]
            )))
            cursor += 4
        else:
            instructions = [x for x in lines[cursor:] if x]
            break
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
    opcode_id_mapping = {}
    id_opcode_mapping = {}
    total_matched = 0
    for execution in executions:
        matched = 0
        for opcode, operation in opcodes.items():
            check_after = apply_operation(execution['before'], execution['instruction'], operation)
            if check_after == execution['after']:
                matched += 1
                opcode_id_mapping.setdefault(opcode, set()).add(operation[0])
                id_opcode_mapping.setdefault(operation[0], set()).add(opcode)
        if matched >= 3:
            total_matched += 1
    print(total_matched)


if __name__ == '__main__':
    main()
