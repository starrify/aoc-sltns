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
    freq_guard_minute = None
    for guard, periods in guard_sleep.items():
        time_span = numpy.zeros((61,))
        for period in periods:
            time_span[period[0]:period[1]] += numpy.ones((period[1] - period[0],))
        target_minute = time_span.argmax()
        tmp_result = (time_span[target_minute], guard, target_minute)
        if freq_guard_minute is None or tmp_result > freq_guard_minute:
            freq_guard_minute = tmp_result
    print(freq_guard_minute[1] * freq_guard_minute[2])


if __name__ == '__main__':
    main()
