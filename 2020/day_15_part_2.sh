#!/usr/bin/env bash

awk -F, '
    {
        for (i = 1; i <= NF; i++) {
            last_seen[$i] = i;
            prev = $i;
        }
    }
    END {
        for (i = NF + 1; i <= 30000000; i++) {
            if (prev in last_seen) {
                age = i - last_seen[prev] - 1;
            } else {
                age = 0;
            }
            last_seen[prev] = i - 1;
            prev = age;
        }
        print(prev);
    }
'
