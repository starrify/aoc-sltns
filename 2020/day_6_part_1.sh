#!/usr/bin/env bash

parallel --pipe --recend '\n\n' -N 1 -k "grep -o '\w' | sort | uniq | wc -l" | paste -s -d+ | bc
