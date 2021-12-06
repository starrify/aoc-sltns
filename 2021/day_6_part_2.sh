#!/usr/bin/env bash

awk -F, '
{
    for (i = 1; i <= NF; i++)
        cnt[$i] += 1;
}

END {
    for (i = 1; i <= 256; i++) {
        delete tmp;
        tmp[8] = cnt[0];
        tmp[6] = cnt[0];
        for (j = 1; j <= 8; j++)
            tmp[j - 1] += cnt[j];
        delete cnt;
        for (j in tmp)
            cnt[j] = tmp[j];
    }
    for (i = 0; i <= 8; i++)
        ans += cnt[i];
    print(ans);
}
'
