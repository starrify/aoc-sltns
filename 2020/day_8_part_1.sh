#!/usr/bin/env bash

awk '
    {
        inst[NR][0] = $1
        inst[NR][1] = $2;
    }
    END {
        acc = 0;
        pc = 1;
        delete visited[0];
        while (1) {
            visited[pc] = 1;
            switch (inst[pc][0]) {
            case "nop":
                pc += 1;
                break;
            case "acc":
                acc += inst[pc][1];
                pc += 1;
                break;
            case "jmp":
                pc += inst[pc][1];
                pc = pc < 1 ? 1 : pc;
                break;
            }
            if (pc in visited) {
                print acc;
                break;
            }
        }
    }
'
