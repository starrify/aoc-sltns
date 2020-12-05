#!/usr/bin/env bash

tmp_check () {
    TMP=$(sed 's/[FL]/0/g;s/[BR]/1/g')
    echo "ibase=2;${TMP:0:7}*1000+${TMP:7:3}" | bc
}
export -f tmp_check

parallel --pipe -N 1 tmp_check | sort -nr | head -n 1
