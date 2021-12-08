#!/usr/bin/env bash

tr -d '|' | awk '
BEGIN {
    unique_stokes[2] = 1;
    unique_stokes[4] = 4;
    unique_stokes[3] = 7;
    unique_stokes[7] = 8;
}
{
    for (i = 11; i <= 14; i++) {
        len = split($i, seq, "");
        if (unique_stokes[len] > 0)
            cnt++;
    }
}
END {
    print(cnt);
}
'
