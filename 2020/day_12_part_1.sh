#!/usr/bin/env bash

sed -E 's/^(.)/\1 /' | awk '
    BEGIN {
        x = 0;
        y = 0;
        dx = 1;
        dy = 0;
    }
    {
        switch ($1) {
        case "N":
            y += $2;
            break;
        case "S":
            y -= $2;
            break;
        case "E":
            x += $2;
            break;
        case "W":
            x -= $2;
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
