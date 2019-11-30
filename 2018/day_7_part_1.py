# coding: utf8

import sys
import re
import queue


def main():
    awaits = {}
    unlocks = {}
    for line in sys.stdin:
        steps = re.findall('Step (.) .* before step (.) ', line)[0]
        unlocks.setdefault(steps[0], []).append(steps[1])
        awaits.setdefault(steps[1], set()).add(steps[0])
    pending = queue.PriorityQueue()
    for step in unlocks.keys():
        if not awaits.get(step):
            pending.put(step)
    solution = []
    while pending.qsize() > 0:
        step = pending.get()
        solution.append(step)
        for unlocked in unlocks.get(step, []):
            awaits[unlocked].remove(step)
            if not awaits[unlocked]:
                pending.put(unlocked)
    print(''.join(solution))


if __name__ == '__main__':
    main()
