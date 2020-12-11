#!/usr/bin/env bash

function do_round() {
    awk -F "" '
        {
            for (i = 1; i <= NF; i++) {
                map[NR][i] = $i;
                if ($i != "#") {
                    continue;
                }
                for (j = -1; j <= 1; j++) {
                    for (k = -1; k <= 1; k++) {
                        if (j == 0 && k == 0) {
                            continue;
                        }
                        acc[NR - j][i - k] += 1;
                    }
                }
            }
        }
        END {
            for (i = 1; i <= NR; i++) {
                for (j = 1; j <= NF; j++) {
                    switch (map[i][j]) {
                    case ".":
                        break;
                    case "L":
                        if (acc[i][j] == 0) {
                            map[i][j] = "#";
                        }
                        break;
                    case "#":
                        if (acc[i][j] >= 4) {
                            map[i][j] = "L";
                        }
                        break;
                    }
                    printf map[i][j];
                }
                print "";
            }
        }
    '
}

TMP_FILE_1=/tmp/aoc_d11p1_tmp_1
TMP_FILE_2=/tmp/aoc_d11p1_tmp_2

cat > $TMP_FILE_1

while true; do
    cat $TMP_FILE_1 | do_round > $TMP_FILE_2
    if cmp -s $TMP_FILE_1 $TMP_FILE_2; then
        break;
    fi
    cp $TMP_FILE_2 $TMP_FILE_1
done

cat $TMP_FILE_2 | grep -o "#" | wc -l

