#!/usr/bin/env bash

TMP_FILE=/tmp/aoc_2020_d9p2.tmp
TARGET=$(tee $TMP_FILE | bash ./day_9_part_1.sh);

cat $TMP_FILE | awk '
    {
        for (i = 1; i < NR; i++) {
            sum[i] += $1;
            max[i] = max[i] > $1 ? max[i] : $1;
            min[i] = min[i] < $1 ? min[i] : $1;
            print sum[i], max[i], min[i];
        }
        sum[NR] = $1;
        max[NR] = $1;
        min[NR] = $1;
    }
' | grep '^'$TARGET | sed -E 's/(\S+) (\S+) (\S+)/\2+\3/' | bc
