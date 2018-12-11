# coding: utf8

import sys
import re


def main():
    n_player, n_marble = [
        int(x)
        for x in re.findall('\d+', sys.stdin.read().strip())
    ]
    n_marble *= 100
    playground = [
        [0, 0]  # prec (counter-clockwise), succ (clockwise)
    ] + [None for _ in range(n_marble)]
    current = 0
    player_score = [0 for _ in range(n_player + 1)]
    player = 0
    for marble in range(1, n_marble + 1):
        player %= n_player
        player += 1
        if marble % 23:
            current = playground[current][1]
            playground[marble] = [current, playground[current][1]]
            playground[playground[current][1]][0] = marble
            playground[current][1] = marble
            current = marble
        else:
            player_score[player] += marble
            for _ in range(7):
                current = playground[current][0]
            player_score[player] += current
            playground[playground[current][1]][0] = playground[current][0]
            playground[playground[current][0]][1] = playground[current][1]
            current = playground[current][1]
    print(max(player_score))


if __name__ == '__main__':
    main()
