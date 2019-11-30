# coding: utf8

import sys
import re


def simulate(input_groups, boost):
    groups = [x.copy() for x in input_groups]
    for group in groups:
        if group['system'] == 'immune system':
            group['damage'] += boost
            group['effective_power'] = group['n_units'] * group['damage']
    n_round = 0
    while True:
        n_round += 1
        # target locking
        for group in groups:
            group['target'] = None
        selected = set()
        selection_order = sorted([
            (-group['effective_power'], -group['initiative'], group)
            for group in groups
            if group['n_units'] > 0
        ])
        for _, _, group in selection_order:
            targets = sorted([
                (-group['damage_modifier'][tmp_group['id']], -tmp_group['effective_power'], -tmp_group['initiative'], tmp_group)
                for tmp_group in groups
                if tmp_group['n_units'] > 0 and tmp_group['id'] not in selected and tmp_group['system'] != group['system']
            ])
            if targets:
                target = targets[0][-1]
                if group['damage_modifier'][target['id']] > 0:
                    selected.add(target['id'])
                    group['target'] = target['id']
        # attacking
        attacking_order = sorted([
            (-group['initiative'], group)
            for group in groups
            if group['target'] is not None
        ])
        damage_dealt = False
        for _, group in attacking_order:
            if group['n_units'] <= 0:
                continue
            damage = group['damage_modifier'][group['target']] * group['effective_power']
            target = groups[group['target']]
            target['n_units'] -= damage // target['hp']
            if damage // target['hp'] > 0:
                damage_dealt = True
            target['n_units'] = max(0, target['n_units'])
            target['effective_power'] = target['n_units'] * target['damage']
        if len(set(x['system'] for x in groups if x['n_units'] > 0)) <= 1:
            break
        if not attacking_order or not damage_dealt:
            return n_round, 'tie', [x for x in groups if x['n_units'] > 0]
    remaining = [x for x in groups if x['n_units'] > 0]
    return n_round, remaining[0]['system'], sum(x['n_units'] for x in remaining)


def main():
    groups = []
    for _ in range(2):
        system_name = sys.stdin.readline().strip().strip(':').lower()
        while True:
            line = sys.stdin.readline().strip()
            if not line:
                break
            group = {
                'id': len(groups),
                'system': system_name,
            }
            group.update(dict(zip(
                ('n_units', 'hp', 'damage', 'initiative'),
                (int(x) for x in re.findall(r'\d+', line))
            )))
            group['damage_type'] = line.split(' damage ')[0].split()[-1]
            group['effective_power'] = group['n_units'] * group['damage']
            for modifier in ('weak', 'immune'):
                split = modifier + ' to '
                if split in line:
                    group[modifier] = line.split(split)[-1].split(';')[0].split(')')[0].split(', ')
                else:
                    group[modifier] = ()
            groups.append(group)
    for group in groups:
        for group2 in groups:
            if group['system'] == group2['system']:
                continue
            modifier = 1
            if group['damage_type'] in group2['immune']:
                modifier = 0
            elif group['damage_type'] in group2['weak']:
                modifier = 2
            group.setdefault('damage_modifier', {})[group2['id']] = modifier
    check_range = [0, 100]
    assert simulate(groups, check_range[0])[1] == 'infection'
    assert simulate(groups, check_range[1])[1] == 'immune system'
    best_result = None
    while True:
        if check_range[1] - check_range[0] == 1:
            break
        new_check = sum(check_range) // 2
        tmp_result = simulate(groups, new_check)
        print(new_check, tmp_result)
        if tmp_result[1] in ('infection', 'tie'):
            check_range[0] = new_check
        else:
            check_range[1] = new_check
            best_result = (new_check, tmp_result[0], tmp_result[2])
    print(best_result)


if __name__ == '__main__':
    main()
