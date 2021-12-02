#!/usr/bin/env bash

awk '
BEGIN {
    prev = -log(0);
    cnt = 0;
}
{
    cnt += $1 > prev;
    prev = $1;
}
END {
    print(cnt);
}
'
