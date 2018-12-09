# coding: utf8

import sys
import re

import numpy


def main():
    # assuming the input is well-formed
    lines = sorted(list(sys.stdin))
    guard_sleep = {}
    current_guard = None
    tmp_sleep = None
    for line in lines:
        current_guard = int((re.findall('Guard #(\d+)', line) or [current_guard])[0])
        minute = int(re.findall(r':(\d+)', line)[0])
        if 'falls asleep' in line:
            tmp_sleep = minute
        elif 'wakes up' in line:
            guard_sleep.setdefault(current_guard, []).append([tmp_sleep, minute])
    # find the guard
    sleep_count_guard = [
        (sum(x[1] - x[0] for x in periods), guard)
        for guard, periods in guard_sleep.items()
    ]
    target_guard = sorted(sleep_count_guard)[-1][1]
    # find the minute
    time_span = numpy.zeros((61,))
    for period in guard_sleep[target_guard]:
        time_span[period[0]:period[1]] += numpy.ones((period[1] - period[0],))
    target_minute = time_span.argmax()
    # finally
    print(target_guard * target_minute)


if __name__ == '__main__':
    main()
