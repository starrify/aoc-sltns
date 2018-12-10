# coding: utf8

import sys
import re
import queue


def get_min_cost(step, steps):
    if 'min_cost' not in step:
        step['min_cost'] = step['cost'] + max(
            (get_min_cost(steps[x], steps) for x in step['unlocks']),
            default=0
        )
    return step['min_cost']


def main():
    n_worker = 5
    input_steps = [
        re.findall('Step (.) .* before step (.) ', line)[0]
        for line in sys.stdin
    ]
    steps = {
        step: {
            'name': step,
            'unlocks': [],
            'awaits': set(),
            'cost': 61 + ord(step) - ord('A'),
        }
        for step in set(y for x in input_steps for y in x)
    }
    for input_step in input_steps:
        steps[input_step[0]]['unlocks'].append(input_step[1])
        steps[input_step[1]]['awaits'].add(input_step[0])
    pending = queue.PriorityQueue()  # (-min_cost, curr_time, something_arbitrary (for helping the sort), step)
    for step in steps.values():
        if not step['awaits']:
            pending.put((-get_min_cost(step, steps), 0, step['name'], step))
    in_progress = queue.PriorityQueue()  # (finish_time, step)
    curr_time = 0
    while pending.qsize() > 0 or in_progress.qsize() > 0:
        while in_progress.qsize() < n_worker and pending.qsize() > 0:
            _, _, _, step_next = pending.get()
            in_progress.put((curr_time + step_next['cost'], step_next))
        if in_progress.qsize() > 0:
            curr_time, step_finished = in_progress.get()
            for unlocked in step_finished['unlocks']:
                steps[unlocked]['awaits'].remove(step_finished['name'])
                if not steps[unlocked]['awaits']:
                    pending.put((-get_min_cost(steps[unlocked], steps), curr_time, steps[unlocked]['name'], steps[unlocked]))
    print(curr_time)


if __name__ == '__main__':
    main()
