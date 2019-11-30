# coding: utf8

import sys
import queue


def main():
    # Transposed coordinate system. E.g., the "7,3" example shall be "3,7" here.
    grids = [
        list(line.strip('\n')) + [' ']
        for line in sys.stdin
    ]
    grids.append([' ' for _ in grids[0]])
    # Important: "On your initial map, the track under each cart is a straight path matching the direction the cart is facing."
    # 
    # Edge cases:
    # 
    # (invalid as per the description)
    # /\/\/\
    # \/\/\/
    # /\/</\
    # \/\/\/
    #
    # (invalid as per the description)
    # v<
    # >^
    #
    # (good thing is that the given input is rather trivial and does not contain such edge cases)
    #  /
    # ->-
    #  \
    #
    # -->>-- (crash)
    # --<<-- (no crash)
    #
    direction_rev = {
        '^': 'v',
        '>': '<',
        '<': '>',
        'v': '^',
    }
    direction_offset = {
        '^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1),
    }
    horizontal = set('<>')
    vertical = set('^v')
    all_4_dir = horizontal.union(vertical)
    symbol_connectivity = {
        # symbol: directions (possibly) connected
        '-': horizontal,
        '|': vertical,
        '+': all_4_dir,
        '\\': all_4_dir,
        '/': all_4_dir,
    }
    turn_direction = {
        '/': {
            '^': '>',
            '>': '^',
            'v': '<',
            '<': 'v',
        },
        '\\': {
            '^': '<',
            '<': '^',
            'v': '>',
            '>': 'v',
        },
    }
    # turn order: left, straight, right = 0, 1, 2
    turn_direction_relative = {
        '^': ['<', '^', '>'],
        '>': ['^', '>', 'v'],
        'v': ['>', 'v', '<'],
        '<': ['v', '<', '^'],
    }
    carts = queue.PriorityQueue()  # (pos, dir, turn)
    cart_locs = set()
    for x, row in enumerate(grids):
        for y, symbol in enumerate(row):
            if symbol in ['<', '>', '^', 'v']:
                # rebuild the original grid
                connectivity = set()
                for direction, offset in direction_offset.items():
                    tmp_x = x + offset[0]
                    tmp_y = y + offset[1]
                    if direction_rev[direction] in symbol_connectivity.get(grids[tmp_x][tmp_y], []):
                        connectivity.add(direction)
                if connectivity == horizontal:
                    grids[x][y] = '-'
                elif connectivity == vertical:
                    grids[x][y] = '|'
                elif connectivity == all_4_dir:
                    grids[x][y] = '+'
                else:
                    raise ValueError('Connectivity %s found at %s %s' % (connectivity, x, y))
                carts.put(((x, y), symbol, 0))
                cart_locs.add((x, y))
    collision_loc = None
    while not collision_loc:
        tmp_carts = queue.PriorityQueue()
        while carts.qsize():
            pos, direction, turn_order = carts.get()
            new_pos = tuple(
                pos[i] + direction_offset[direction][i]
                for i in range(2)
            )
            if new_pos in cart_locs:
                collision_loc = new_pos
                break
            else:
                cart_locs.add(new_pos)
                cart_locs.remove(pos)
            new_grid = grids[new_pos[0]][new_pos[1]]
            if new_grid in '-|':
                assert direction in symbol_connectivity[new_grid]
            elif new_grid in '\\/':
                direction = turn_direction[new_grid][direction]
            elif new_grid == '+':
                direction = turn_direction_relative[direction][turn_order]
                turn_order += 1
                turn_order %= 3
            else:
                raise ValueError
            tmp_carts.put((new_pos, direction, turn_order))
        carts = tmp_carts
        if False:
            tmp_carts = queue.PriorityQueue()
            tmp_grids = [x.copy() for x in grids]
            while carts.qsize():
                cart = carts.get()
                tmp_grids[cart[0][0]][cart[0][1]] = cart[1]
                tmp_carts.put(cart)
            for tmp_row in tmp_grids:
                print(''.join(tmp_row))
            carts = tmp_carts
    print(*collision_loc[::-1], sep=',')


if __name__ == '__main__':
    main()
