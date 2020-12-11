#!/usr/bin/env bash

function do_round() {
    awk -F "" '
        {
            for (i = 1; i <= NF; i++) {
                map[NR][i] = $i;
            }
        }
        END {
            for (i = 1; i <= NR; i++) {
                for (j = 1; j <= NF; j++) {
                    if (map[i][j] != "#") {
                        continue;
                    }
                    for (dx = -1; dx <= 1; dx++) {
                        for (dy = -1; dy <= 1; dy++) {
                            if (dx == 0 && dy == 0) {
                                continue;
                            }
                            for (k = 1; k <= NF; k++) {
                                x = i + dx * k;
                                y = j + dy * k;
                                if (x <= 0 || x > NR || y <= 0 || y > NF) {
                                    break;
                                }
                                if (map[x][y] != ".") {
                                    acc[x][y] += 1;
                                    break;
                                }
                            }
                        }
                    }

                }
            }
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
                        if (acc[i][j] >= 5) {
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

TMP_FILE_1=/tmp/aoc_d11p2_tmp_1
TMP_FILE_2=/tmp/aoc_d11p2_tmp_2

cat > $TMP_FILE_1

while true; do
    cat $TMP_FILE_1 | do_round > $TMP_FILE_2
    if cmp -s $TMP_FILE_1 $TMP_FILE_2; then
        break;
    fi
    cp $TMP_FILE_2 $TMP_FILE_1
done

cat $TMP_FILE_2 | grep -o "#" | wc -l

