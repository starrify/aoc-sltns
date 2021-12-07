#!/usr/bin/env bash

awk -F, '
{
    for (i = 1; i <= NF; i++)
        pos[i] = $i;
}

function min(x, y) {
    return x < y ? x : y;
}

END {
    asort(pos);
    pos[0] = pos[1];
    pos[NF + 1] = pos[NF];
    for (i = 1; i <= NF; i++)
        forward[i] = forward[i - 1] + (pos[i] - pos[i - 1]) * (i - 1);
    for (i = NF; i >= 1; i--)
        backward[i] = backward[i + 1] + (pos[i + 1] - pos[i]) * (NF - i);
    ans = -log(0);
    for (i = 1; i <= NF; i++)
        ans = min(ans, forward[i] + backward[i]);
    print(ans);
}
'
