#!/usr/bin/env bash

tmp_check () {
    grep -Po '\b(byr|iyr|eyr|hgt|hcl|ecl|pid):\S+' \
    | sed -E '
        s/(hgt:[0-9]+)(cm|in)/\1 \2/;
        s/hcl:#[0-9a-f]{6}/VALID/;
        s/ecl:(amb|blu|brn|gry|grn|hzl|oth)/VALID/;
        s/pid:[0-9]{9}/VALID/;
        s/:/ /;
    ' \
    | awk '{
        if ($1 == "byr" && $2 >= 1920 && $2 <= 2002) {
            print "VALID"
        } else if ($1 == "iyr" && $2 >= 2010 && $2 <= 2020) {
            print "VALID"
        } else if ($1 == "eyr" && $2 >= 2020 && $2 <= 2030) {
            print "VALID"
        } else if ($1 == "hgt") {
            if ($3 == "cm" && $2 >= 150 && $2 <= 193) {
                print "VALID"
            } else if ($3 == "in" && $2 >= 59 && $2 <= 76) {
                print "VALID"
            }
        } else {
            print
        }
    }'
}
export -f tmp_check

parallel --pipe --recend '\n\n' -N 1 -k "tmp_check | grep '^VALID$' -c" | grep 7 -c
