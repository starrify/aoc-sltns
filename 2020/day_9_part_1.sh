#!/usr/bin/env bash

awk '
    function check_valid(numbers, idx, check_size) {
        for (i = 1; i <= check_size; i++) {
            for (j = 1; j <= check_size; j++) {
                if (i == j) {
                    continue;
                }
                if (numbers[idx - i] + numbers[idx - j] == numbers[idx]) {
                    return 1;
                }
            }
        }
        return 0;
    }
    {
        check_size = 25;
        numbers[NR] = $1;
        if (NR > check_size) {
            if (!check_valid(numbers, NR, check_size)) {
                print $1;
                exit;
            }
        }
    }
'
