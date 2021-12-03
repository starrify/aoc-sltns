#!/usr/bin/env bash

awk '
BEGIN {
    FS = "";
}
{
    for (i = 1; i <= NF; i += 1) {
        cnt[i] -= $i == "0";
        cnt[i] += $i == "1";
    }
}
END {
    for (i = 1; i <= NF; i += 1) {
        gamma = gamma * 2 + (cnt[i] > 0);
        epsilon = epsilon * 2 + (cnt[i] < 0);
    }
    print(gamma * epsilon);
}
'
