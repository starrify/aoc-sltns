#!/usr/bin/env bash

tail -n +2 | tr , '\n' | awk --bignum '
    BEGIN {
        prod = 1;
    }
    {
        if ($1 != "x") {
            bus[NR] = $1;
            prod *= $1;
        }
    }
    END {
        # assuming all bus IDs are prime (at least for my input)
        for (i in bus) {
            prod_partial = int(prod / bus[i]);
            ans += (bus[i] - i + 1) * prod_partial ** (bus[i] - 1);
        }
        print ans % prod;
    }
'
