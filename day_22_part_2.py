# coding: utf8

import sys


def main():
    depth = int(sys.stdin.readline().strip().split()[-1])
    target = tuple(int(x) for x in sys.stdin.readline().strip().split()[-1].split(','))
    MOD = 20183
    erosion_level_cached = {(0, 0): depth % MOD, target: depth % MOD}
    def _get_erosion_level(pos):
        if pos not in erosion_level_cached:
            x, y = pos
            if x == 0:
                tmp_calculated = (y * 48271 + depth) % MOD
            elif y == 0:
                tmp_calculated = (x * 16807 + depth) % MOD
            else:
                tmp_calculated = (_get_erosion_level((x - 1, y)) * _get_erosion_level((x, y - 1)) % MOD + depth) % MOD
            erosion_level_cached[pos] = tmp_calculated
        return erosion_level_cached[pos]
    def _get_region_type(pos):
        return _get_erosion_level(pos) % 3
    ROCKY, WET, NARROW = 0, 1, 2
    CLIMBING_GEAR, TORCH, NOTHING = 0, 1, 2
    region_equipments = {
        ROCKY: (CLIMBING_GEAR, TORCH),
        WET: (CLIMBING_GEAR, NOTHING),
        NARROW: (TORCH, NOTHING),
    }
    min_cost = {((0, 0), TORCH): 0}  # (pos, equipment)
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    def _calculate_min_cost(active, check_coord_range=True, check_global_optimal=False):
        while active:
            new_active = set()
            for pos, equipment in active:
                for new_equipment in region_equipments[_get_region_type(pos)]:
                    if new_equipment == equipment:
                        continue
                    new_cost = min_cost[(pos, equipment)] + 7
                    if check_global_optimal and new_cost + sum(abs(pos[i] - target[i]) for i in range(2)) >= min_cost[(target, TORCH)]:
                        continue
                    if (pos, new_equipment) not in min_cost or min_cost[(pos, new_equipment)] > new_cost:
                        min_cost[(pos, new_equipment)] = new_cost
                        new_active.add((pos, new_equipment))
                for direction in directions:
                    new_pos = tuple(sum(x) for x in zip(pos, direction))
                    if new_pos[0] < 0 or new_pos[1] < 0:
                        continue
                    if check_coord_range and (new_pos[0] > target[0] or new_pos[1] > target[1]):
                        continue
                    if equipment not in region_equipments[_get_region_type(new_pos)]:
                        continue
                    new_cost = min_cost[(pos, equipment)] + 1
                    if check_global_optimal and new_cost + sum(abs(new_pos[i] - target[i]) for i in range(2)) >= min_cost[(target, TORCH)]:
                        continue
                    if (new_pos, equipment) not in min_cost or min_cost[(new_pos, equipment)] > new_cost:
                        min_cost[(new_pos, equipment)] = new_cost
                        new_active.add((new_pos, equipment))
            active = list(new_active)
    _calculate_min_cost([((0, 0), TORCH)])
    print(min_cost[(target, TORCH)])
    edge_active = [
        (pos, equipment)
        for pos, equipment in min_cost
        if pos[0] == target[0] or pos[1] == target[1]
    ]
    _calculate_min_cost(edge_active, check_coord_range=False, check_global_optimal=True)
    print(min_cost[(target, TORCH)])


if __name__ == '__main__':
    main()
