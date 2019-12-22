# coding: utf8

import sys


def main():
    deck_size = 10007
    deck = list(range(deck_size))
    for line in sys.stdin.read().splitlines():
        if line == 'deal into new stack':
            deck = deck[::-1]
        elif line.startswith('cut'):
            cut = int(line.split()[-1]) % deck_size
            deck = deck[cut:] + deck[:cut]
        elif line.startswith('deal with increment'):
            increment = int(line.split()[-1])
            new_deck = [None for _ in deck]
            for idx, value in enumerate(deck):
                # as ensured by the input..
                new_deck[idx * increment % deck_size] = value
            deck = new_deck
        else:
            raise ValueError(line)
    print(deck.index(2019))


if __name__ == '__main__':
    main()
