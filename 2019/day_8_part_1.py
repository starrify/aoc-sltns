# coding: utf8

import sys


def main():
    img_size = (25, 6)
    layer_size = img_size[0] * img_size[1]
    pixels = list(sys.stdin.read().strip())
    min_zero_cnt = float('inf')
    ans = None
    for idx in range(0, len(pixels), layer_size):
        layer = pixels[idx:idx + layer_size]
        zero_cnt = layer.count('0')
        if zero_cnt < min_zero_cnt:
            min_zero_cnt = zero_cnt
            ans = layer.count('1') * layer.count('2')
    print(ans)


if __name__ == '__main__':
    main()
