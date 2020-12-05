#!/usr/bin/env bash
parallel --pipe --recend '\n\n' -N 1 "grep -Po '\b(byr|iyr|eyr|hgt|hcl|ecl|pid)(?=:\S+)' | wc -l" | grep 7 -c
