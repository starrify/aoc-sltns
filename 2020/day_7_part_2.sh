#!/usr/bin/env bash

sed -E 's/ contain no other bags//; s/ contain\b/,/g; s/, ([0-9]+) /,\1,/g; s/ \bbags?\b//g; s/\.$//' \
| awk -F, '
    {
        for (i = 1; i < NF / 2; i++) {
            holds[$1][$(i * 2 + 1)] = $(i * 2);
        }
    }
    function bags_count(color, count_cache, holds) {
        if (!(color in count_cache)) {
            count_cache[color] = 1;
            if (length(holds[color]) > 0) {
                for (tmp_color in holds[color]) {
                    count_cache[color] += holds[color][tmp_color] * bags_count(tmp_color, count_cache, holds);
                }
            }
        }
        return count_cache[color];
    }
    END {
        delete count_cache[0];
        print bags_count("shiny gold", count_cache, holds) - 1;
    }
'
