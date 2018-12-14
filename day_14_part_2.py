# coding: utf8

import sys


def main():
    target_seq = [int(x) for x in sys.stdin.read().strip()]
    n_recipes = 2
    recipes = [3, 7]
    n_generated = 2
    cursors = [0, 1]
    target_found = False
    while not target_found:
        newly_generated = [int(x) for x in str(recipes[cursors[0]] + recipes[cursors[1]])]
        while n_generated + len(newly_generated) > n_recipes:
            recipes.extend([None for _ in range(n_recipes)])
            n_recipes *= 2
        recipes[n_generated : n_generated + len(newly_generated)] = newly_generated
        n_generated += len(newly_generated)
        cursors = [
            (x + 1 + recipes[x]) % n_generated
            for x in cursors
        ]
        # XXX: An KMP-like idea would make the comparision cost O(n + m) (currently O(n * m))
        for i in range(len(newly_generated)):
            if recipes[n_generated - i - len(target_seq) : n_generated - i] == target_seq:
                print(n_generated - i - len(target_seq))
                target_found = True
                break


if __name__ == '__main__':
    main()
