#!/usr/bin/env bash

awk '
{
    rec[NR] = $0;
}

function filter_one(source, most_common, default) {
    asort(source, sorted);
    l = 1;
    r = length(sorted);
    for (i = 1; i <= length(sorted[1]); i += 1) {
        for (j = l; j < r; j += 1) {
            if (substr(sorted[j], i, 1) != substr(sorted[j + 1], i, 1))
                break;
        }
        if (j == r)
            continue;
        balance = (j - l + 1) - (r - j);
        if (balance == 0) {
            l = default == "0" ? l : j + 1;
            r = default == "0" ? j : r;
        } else {
            l = xor(balance < 0, most_common) ? l : j + 1;
            r = xor(balance < 0, most_common) ? j : r;
        }
        if (l == r)
            return sorted[l];
    }
    // unreachable
    exit(1);
}

END {
    printf("%s * %s\n", filter_one(rec, 1, "1"), filter_one(rec, 0, "0"));
}
' | bc <(echo "ibase = 2")
