# coding: utf8

import sys
import re


def intersect_1d(a0, a1, b0, b1):
    return (a0 - b1) * (a1 - b0) < 0


def main():
    claims = [
        # id, x, y, width, height
        [int(x) for x in re.split(r'\D+', line.strip())[1:]]
        for line in sys.stdin
    ]
    for idx, claim in enumerate(claims):
        overlapping = False
        for idx2, claim2 in enumerate(claims):
            if idx2 == idx:
                continue
            if (
                    intersect_1d(claim[1], claim[1] + claim[3], claim2[1], claim2[1] + claim2[3])
                    and
                    intersect_1d(claim[2], claim[2] + claim[4], claim2[2], claim2[2] + claim2[4])
                ):
                overlapping = True
                break
        if not overlapping:
            print(claim[0])


if __name__ == '__main__':
    main()
