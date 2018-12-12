# coding: utf8

import sys


def iterate_state(state, new_tree_states, left_padding, check_size=5):
    tmp_partition = state.partition('#')
    left_padding = left_padding - len(tmp_partition[0]) + 4
    state = '....' + tmp_partition[1] + tmp_partition[2].rstrip('.') + '....'
    return (left_padding - 2, ''.join(
        '#'
        if state[i:i+check_size] in new_tree_states
        else '.'
        for i in range(0, len(state) - check_size + 1)
    ))


def main():
    lines = [x.strip() for x in sys.stdin]
    state = lines[0].split(':')[-1].strip()
    new_tree_states = set(x.split(' => ')[0] for x in lines[2:] if x[-1] == '#')
    left_padding = 0
    target_iteration = 50000000000
    prev_states = {}
    for i in range(target_iteration):
        left_padding, state = iterate_state(state, new_tree_states, left_padding)
        if state in prev_states:
            interval = i - prev_states[state][0]
            remaining = target_iteration - i - 1
            left_padding += (left_padding - prev_states[state][1]) * (remaining // interval)
            for _ in range(remaining % interval):
                left_padding, state = iterate_state(state, new_tree_states, left_padding)
            break
        prev_states[state] = (i, left_padding)
    print(sum(
        idx - left_padding
        for idx, char in enumerate(state)
        if char == '#'
    ))


if __name__ == '__main__':
    main()
