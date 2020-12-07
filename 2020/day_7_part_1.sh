#!/usr/bin/env bash

sed -E 's/ contain no other bags//; s/ contain\b/,/g; s/, ([0-9]+) /,\1,/g; s/ \bbags?\b//g; s/\.$//' \
| awk -F, '
    {
        for (i = 1; i < NF / 2; i++) {
            holds[$(i * 2 + 1)][$1] = 1;
        }
    }
    END {
        processed_cnt = 0;
        pending[0] = "shiny gold";
        picked["shiny gold"] = 1;
        while (length(pending) > processed_cnt) {
            color = pending[processed_cnt];
            if (length(holds[color]) > 0) {
                for (tmp_color in holds[color]) {
                    if (!picked[tmp_color]) {
                        pending[length(pending)] = tmp_color;
                        picked[tmp_color] = 1;
                    }
                }
            }
            processed_cnt += 1;
        }
        print processed_cnt - 1;
    }
'
