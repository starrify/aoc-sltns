#!/usr/bin/env bash

awk '
{
    if ($1 == "forward") {
        x += $2;
        y += $2 * aim;
    }
    if ($1 == "down")
        aim += $2;
    if ($1 == "up")
        aim -= $2;
}
END {
    print(x * y);
}
'
