# coding: utf8

import sys


def read_node(nums):
    # returns one node and the residual nums
    num_children, num_meta = nums[:2]
    remaining = nums[2:]
    node = {
        'children': [],
        'meta': [],
    }
    for _ in range(num_children):
        child, remaining = read_node(remaining)
        node['children'].append(child)
    node['meta'] = remaining[:num_meta]
    return node, remaining[num_meta:]


def get_value(node):
    if not node['children']:
        return sum(node['meta'])
    else:
        return sum(
            get_value(node['children'][idx - 1])
            for idx in node['meta']
            if 1 <= idx <= len(node['children'])
        )


def get_meta_sum(node):
    return sum(node['meta']) + sum(get_meta_sum(child) for child in node['children'])


def main():
    nums = [int(x) for x in sys.stdin.read().strip().split()]
    root_node, _ = read_node(nums)
    print(get_value(root_node))


if __name__ == '__main__':
    main()
