#!/usr/bin/env bash

tr -s '\n' | sed -E 's/.*: //g;s/-/,/g;s/ or /\n/g' | awk -F, '
    {
        switch ($1) {
        case "your ticket:":
        case "nearby tickets:":
            mode = $1;
            next;
        }
        if (!mode) {
            range[NR][1] = $1;
            range[NR][2] = $2;
        } else if (mode == "nearby tickets:") {
            for (i = 1; i <= NF; i++) {
                maybe_valid = 0;
                for (j in range) {
                    if ($i >= range[j][1] && $i <= range[j][2]) {
                        maybe_valid = 1;
                    }
                }
                if (!maybe_valid) {
                    next;
                }
            }
            valid_tickets[NR] = $0;
        }
    }
    END {
        for (i in valid_tickets) {
            print(valid_tickets[i]);
        }
    }
'
