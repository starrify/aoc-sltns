#!/usr/bin/env bash

sort -n | awk '
    BEGIN {
        cnt[0] = 1;
    }
    {
        for (i = 1; i <= 3; i++) {
            cnt[$1] += cnt[$1 - i];
        }
        last = $1;
    }
    END {
        print cnt[last];
    }
'
