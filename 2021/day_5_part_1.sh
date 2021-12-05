#!/usr/bin/env bash

sed 's/[^0-9]/ /g' | awk '
function min(x1, x2) {
    return x1 < x2 ? x1 : x2;
}

function max(x1, x2) {
    return x1 > x2 ? x1 : x2;
}

{
    if ($1 == $3)
        for (i = min($2, $4); i <= max($2, $4); i++)
            point[$1, i] += 1;
    else if ($2 == $4)
        for (i = min($1, $3); i <= max($1, $3); i++)
            point[i, $2] += 1;
}

END {
    for (key in point)
        if (point[key] > 1)
            count += 1;
    print(count);
}
'
