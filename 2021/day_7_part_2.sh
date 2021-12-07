#!/usr/bin/env bash

awk -F, '
{
    for (i = 1; i <= NF; i++) {
        pos[i] = $i;
        guest[$i]++;
    }
}

function min(x, y) {
    return x < y ? x : y;
}

END {
    asort(pos);
    for (i = pos[1]; i <= pos[length(pos)]; i++) {
        forward[i] = forward[i - 1] + f_inc;
        f_nguest += guest[i];
        f_inc += f_nguest;
    }
    for (i = pos[length(pos)]; i >= pos[1]; i--) {
        backward[i] = backward[i + 1] + b_inc;
        b_nguest += guest[i];
        b_inc += b_nguest;
    }
    min_cost = -log(0);
    for (i = pos[1]; i <= pos[length(pos)]; i++)
        min_cost = min(min_cost, forward[i] + backward[i]);
    print(min_cost);
}
'
