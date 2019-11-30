# coding: utf8

import sys


def main():
    n_recipes = int(sys.stdin.read().strip())
    n_results = 10
    recipes = [3, 7] + [None for _ in range(n_recipes + n_results)]
    n_generated = 2
    cursors = [0, 1]
    while n_generated < n_recipes + n_results:
        newly_generated = [int(x) for x in str(recipes[cursors[0]] + recipes[cursors[1]])]
        recipes[n_generated : n_generated + len(newly_generated)] = newly_generated
        n_generated += len(newly_generated)
        cursors = [
            (x + 1 + recipes[x]) % n_generated
            for x in cursors
        ]
    print(''.join(str(x) for x in recipes[n_recipes:n_recipes+n_results]))


if __name__ == '__main__':
    main()
