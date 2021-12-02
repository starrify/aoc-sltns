#!/usr/bin/env bash

awk '
{
    if (NR > 2)
        print(prev2 + prev1 + $1);
    prev3 = prev2;
    prev2 = prev1;
    prev1 = $1;
}
' | bash day_1_part_1.sh
