#!/usr/bin/env bash

sort -n | awk '
    BEGIN {
        prev = 0;
    }
    {
        acc[$1 - prev] += 1;
        prev = $1;
    }
    END {
        acc[3] += 1;
        print acc[1] * acc[3];
    }
'
