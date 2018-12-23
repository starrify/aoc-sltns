# coding: utf8

import sys
import re


def main():
    input_route = sys.stdin.read().strip().strip('^$')
    # "ValueError: split() requires a non-empty pattern match." before 3.7
    #segments = [x for x in re.split(r'\b|(?<=\W)\B', input_route.strip('^$')) if x]
    segments = [x for x in re.sub(r'\b|(?<=\W)\B', 'wtf', input_route).strip('^$').split('wtf') if x]
    end_of_closure = [None for _ in segments]  # idx of nearest rigth parenthesis
    list_of_alternatives = [None for _ in segments]  # indices of vertical bars in the same closure
    tmp_closure = []
    tmp_pending = []
    for idx in reversed(range(len(segments))):
        if segments[idx] == ')':
            end_of_closure[idx] = idx
            tmp_closure.append(idx)
        elif segments[idx] == '(':
            end_of_closure[idx] = tmp_closure[-1]
            tmp_closure.pop()
        elif tmp_closure:
            end_of_closure[idx] = tmp_closure[-1]
        if segments[idx] == ')':
            tmp_pending.append([])
        elif segments[idx] == '|':
            tmp_pending[-1].append(idx)
        elif segments[idx] == '(':
            list_of_alternatives[idx] = tmp_pending.pop()
    rooms = {
        (0, 0): {
            'coord': (0, 0),
            'connectivity': set(),
        }
    }
    directions = {
        'N': (-1, 0),
        'W': (0, -1),
        'E': (0, 1),
        'S': (1, 0),
    }
    rev_dirs = {
        'N': 'S',
        'W': 'E',
        'E': 'W',
        'S': 'N',
    }
    active = [((0, 0), 0)]  # (pos, next_index)
    queued = set(active)
    while active:
        new_active = set()
        for pos, idx in active:
            segment = segments[idx]
            if segment == '(':
                for next_idx in [idx] + list_of_alternatives[idx]:
                    new_active.add((pos, next_idx + 1))
            elif segment in '|)':
                new_active.add((pos, end_of_closure[idx] + 1))
            elif segment[0] in 'NEWS':
                for char in segment:
                    new_pos = tuple(sum(x) for x in zip(pos, directions[char]))
                    new_room = rooms.setdefault(new_pos, {
                        'coord': new_pos,
                        'connectivity': set(),
                    })
                    new_room['connectivity'].add(rev_dirs[char])
                    rooms[pos]['connectivity'].add(char)
                    pos = new_pos
                new_active.add((new_pos, idx + 1))
            else:
                raise ValueError
        active = [x for x in new_active - queued if x[1] < len(segments)]
        queued.update(active)
    active = [((0, 0), 0)]  # (pos, dist)
    min_dist = {(0, 0): 0}
    while active:
        new_active = set()
        for pos, dist in active:
            for direction in rooms[pos]['connectivity']:
                new_pos = tuple(sum(x) for x in zip(pos, directions[direction]))
                if new_pos not in min_dist or min_dist[new_pos] > dist + 1:
                    min_dist[new_pos] = dist + 1
                    new_active.add((new_pos, dist + 1))
        active = new_active
    print(max(min_dist.values()))
    print(len([x for x in min_dist.values() if x >= 1000]))


if __name__ == '__main__':
    main()
