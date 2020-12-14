#!/usr/bin/env bash

#awk --bignum '
awk '
    {
        if ($1 == "mask") {
            split($3, mask, "");
        } else {
            print("obase=2; " $3) |& "bc";
            "bc" |& getline value;
            value = sprintf("%36s", value);
            gsub(" ", "0", value);
            for (i in mask) {
                if (mask[i] != "X") {
                    value = gensub(".", mask[i], i, value);
                }
            }
            mem[$1] = value;
        }
    }
    END {
        for (i in mem) {
            print(mem[i]);
        }
    }
' | paste -sd '+' | (echo -n "ibase=2;"; cat) | bc
