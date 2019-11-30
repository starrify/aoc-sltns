# coding: utf8

import sys
import re


def main():
    n_player, n_marble = [
        int(x)
        for x in re.findall('\d+', sys.stdin.read().strip())
    ]
    playground = {
        0: {
            'id': 0,
            'prec': 0,  # counter-clockwise
            'succ': 0,  # clockwise
        }
    }
    current = 0
    player_score = [0 for _ in range(n_player + 1)]
    player = 0
    for marble in range(1, n_marble + 1):
        player %= n_player
        player += 1
        if marble % 23:
            current = playground[current]['succ']
            playground[marble] = {
                'id': marble,
                'prec': current,
                'succ': playground[current]['succ'],
            }
            playground[playground[current]['succ']]['prec'] = marble
            playground[current]['succ'] = marble
            current = marble
        else:
            player_score[player] += marble
            for _ in range(7):
                current = playground[current]['prec']
            player_score[player] += current
            playground[playground[current]['succ']]['prec'] = playground[current]['prec']
            playground[playground[current]['prec']]['succ'] = playground[current]['succ']
            current = playground[current]['succ']
    print(max(player_score))


if __name__ == '__main__':
    main()
