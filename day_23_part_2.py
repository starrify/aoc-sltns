# coding: utf8

import sys
import re
import heapq
import itertools
import fractions


def main():
    robots = []
    for line in sys.stdin:
        tmp_numbers = [int(x) for x in re.findall('[0-9-]+', line)]
        robots.append({
            'pos': tuple(tmp_numbers[:3]),
            'r': tmp_numbers[-1],
        })
    min_coord = tuple(
        min(
            robot['pos'][axis] - robot['r']
            for robot in robots
        )
        for axis in range(3)
    )
    max_size = max(
        robot['pos'][axis] + robot['r'] - min_coord[axis]
        for robot in robots
        for axis in range(3)
    )
    max_size = 1 << len(bin(max_size)[2:])  # next power-of-2 of max_size
    n_max_coverage = 1  # number of maximum coverage
    optimal_dist = float('inf')  # minimum distance at maximum coverage
    active = [
        # (negative) maximum possible number of robots coverage, minimum possible distance to origin, pos, size, set of robots (partially?) covered
        (-len(robots), float('inf'), min_coord, max_size, list(range(len(robots))))
    ]
    while active:
        n_covered, min_dist, pos, size, covered_robots = heapq.heappop(active)
        n_covered = -n_covered
        if n_covered < n_max_coverage:
            continue
        if n_covered == n_max_coverage and min_dist >= optimal_dist:
            continue
        new_size = size // 2
        for direction in itertools.product((0, 1), repeat=3):
            new_pos = tuple(
                coord + axis * new_size
                for coord, axis in zip(pos, direction)
            )
            new_center = tuple(
                x + fractions.Fraction(new_size - 1, 2)
                for x in new_pos
            )
            target_r = fractions.Fraction(new_size - 1, 2) * 3
            new_covered = [
                r_id
                for r_id in covered_robots
                if sum(abs(x[0] - x[1]) for x in zip(robots[r_id]['pos'], new_center)) <= robots[r_id]['r'] + target_r
            ]
            new_min_dist = sum(
                0
                if x <= 0 <= x + new_size
                else min(abs(x), abs(x + new_size))
                for x in new_pos
            )
            if new_size == 1:
                if len(new_covered) > n_max_coverage:
                    n_max_coverage = len(new_covered)
                    optimal_dist = new_min_dist
                elif len(new_covered) == n_max_coverage and optimal_dist > new_min_dist:
                    optimal_dist = new_min_dist
            else:
                if len(new_covered) < n_max_coverage:
                    continue
                elif len(new_covered) == n_max_coverage and optimal_dist >= new_min_dist:
                    continue
                heapq.heappush(active, (-len(new_covered), new_min_dist, new_pos, new_size, new_covered))
    print(n_max_coverage, optimal_dist)


if __name__ == '__main__':
    main()
