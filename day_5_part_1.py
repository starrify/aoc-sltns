# coding: utf8

import sys


def react_units(units_str):
    units = list(units_str)
    tmp_seq = list(range(len(units)))
    prec_idcs = [None] + tmp_seq[:-1]
    succ_idcs = tmp_seq[1:] + [None]
    prev_idx = 0
    curr_idx = 1
    while curr_idx is not None and prev_idx is not None:
        if abs(ord(units[curr_idx]) - ord(units[prev_idx])) == 32:
            units[curr_idx] = ''
            units[prev_idx] = ''
            if prec_idcs[prev_idx] is not None:
                succ_idcs[prec_idcs[prev_idx]] = succ_idcs[curr_idx]
            if succ_idcs[curr_idx] is not None:
                prec_idcs[succ_idcs[curr_idx]] = prec_idcs[prev_idx]
            curr_idx = succ_idcs[curr_idx]
            if curr_idx is not None:
                prev_idx = prec_idcs[curr_idx]
                if prev_idx is None:
                    prev_idx = curr_idx
                    curr_idx = succ_idcs[curr_idx]
        else:
            prev_idx = curr_idx
            curr_idx = succ_idcs[curr_idx]
    return ''.join(units)


def main():
    print(len(react_units(sys.stdin.read().strip())))


if __name__ == '__main__':
    main()
