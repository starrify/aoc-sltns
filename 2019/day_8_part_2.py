# coding: utf8

import sys


def main():
    img_size = (25, 6)
    layer_size = img_size[0] * img_size[1]
    final_layer = ['2' for _ in range(layer_size)]
    pixels = list(sys.stdin.read().strip())
    for layer_idx in range(0, len(pixels), layer_size):
        layer = pixels[layer_idx:layer_idx + layer_size]
        for pixel_idx, (pixel0, pixel1) in enumerate(zip(final_layer, layer)):
            if pixel0 == '2':
                final_layer[pixel_idx] = pixel1
    for idx in range(0, len(final_layer), img_size[0]):
        print(''.join(final_layer[idx:idx + img_size[0]]))


if __name__ == '__main__':
    main()
