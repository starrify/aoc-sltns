# coding: utf8

import sys


def get_common_sub(str1, str2):
    return ''.join(
        x[0]
        for x in zip(str1, str2)
        if x[0] == x[1]
    )


def main():
    box_ids = sys.stdin.read().splitlines()
    assert all(len(x) == len(box_ids[0]) for x in box_ids)
    for ordering in (
            # shall satisfy `ordering(ordering(x)) == x`
            lambda x: x,
            lambda x: x[::-1],
        ):
        tmp_ids = sorted([ordering(x) for x in box_ids])
        for idx in range(len(tmp_ids) - 1):
            common_sub = get_common_sub(tmp_ids[idx], tmp_ids[idx + 1])
            if len(common_sub) == len(tmp_ids[idx]) - 1:
                print(get_common_sub(ordering(tmp_ids[idx]), ordering(tmp_ids[idx + 1])))


if __name__ == '__main__':
    main()
