#!/usr/bin/env bash

awk '
    {
        inst[NR][0] = $1
        inst[NR][1] = $2;
    }
    function run_code(ret, inst) {
        acc = 0;
        pc = 1;
        delete visited;
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
            if (pc in visited || pc > length(inst)) {
                break;
            }
        }
        ret["acc"] = acc;
        ret["pc"] = pc;
    }
    function check_replace(inst, idx, new_op) {
        old_op = inst[idx][0];
        inst[idx][0] = new_op;
        delete ret[0];
        run_code(ret, inst);
        if (ret["pc"] > length(inst)) {
            print ret["acc"];
        }
        inst[idx][0] = old_op;
    }
    END {
        for (i = 1; i <= length(inst); i++) {
            switch (inst[i][0]) {
            case "jmp":
                check_replace(inst, i, "nop");
                break;
            case "nop":
                check_replace(inst, i, "jmp");
                break;
            default:
                break;
            }
        }
    }
'
