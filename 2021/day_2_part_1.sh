#!/usr/bin/env bash

awk '
{
    if ($1 == "forward")
        x += $2;
    if ($1 == "down")
        y += $2;
    if ($1 == "up")
        y -= $2;
}
END {
    print(x * y);
}
'
