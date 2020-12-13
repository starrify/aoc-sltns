#!/usr/bin/env bash

awk -F, '
    {
        if (NR == 1) {
            start = $1;
        } else if (NR == 2) {
            min_wait = -1;
            for (i = 1; i <= NF; i++) {
                if ($i != "x") {
                    wait = $i - (start - 1) % $i - 1;
                    if (min_wait == -1 || min_wait > wait) {
                        min_wait = wait;
                        ans = wait * $i;
                    }
                }
            }
            print ans;
        }
    }
'
