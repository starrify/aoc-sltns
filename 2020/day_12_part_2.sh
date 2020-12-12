#!/usr/bin/env bash

sed -E 's/^(.)/\1 /' | awk '
    BEGIN {
        x = 0;
        y = 0;
        dx = 10;
        dy = 1;
    }
    {
        switch ($1) {
        case "N":
            dy += $2;
            break;
        case "S":
            dy -= $2;
            break;
        case "E":
            dx += $2;
            break;
        case "W":
            dx -= $2;
            break;
        case "L":
            for (i = 0; i < $2; i += 90) {
                tmp = -dy
                dy = dx
                dx = tmp
            }
            break;
        case "R":
            for (i = 0; i < $2; i += 90) {
                tmp = dy
                dy = -dx
                dx = tmp
            }
            break;
        case "F":
            x += $2 * dx;
            y += $2 * dy;
            break;
        }
    }
    function abs(x) {
        return x < 0 ? -x : x;
    }
    END {
        print abs(x) + abs(y);
    }
'
