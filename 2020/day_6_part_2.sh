#!/usr/bin/env bash

tmp_check () {
    tr -s '\n' \
    | awk -F "" '
    BEGIN {
        line_count = 0;
    }
    {
        line_count += 1;
        for (i = 1; i <= NF; i++)
            char_count[$i]++;
    }
    END {
        for (char in char_count) {
            if (char_count[char] == line_count)
                print char;
        }
    }
    '
}
export -f tmp_check

parallel --pipe --recend '\n\n' -N 1 -k "tmp_check | wc -l" | paste -s -d+ | bc
