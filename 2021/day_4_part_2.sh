#!/usr/bin/env bash

awk '
NR == 1 {
    split($0, seq, ",");
}
NR > 1 && NR % 6 != 2 {
    nboard = int((NR + 3) / 6);
    row = (NR + 4) % 6;
    for (i = 1; i <= 5; i++) {
        boards[nboard, row, i] = $i;
        board_sum[nboard] += $i;
    }
}
END {
    for (taken in seq) {
        for (board = 1; board <= nboard; board++) {
            for (i = 1; i <= 5; i++)
                for (j = 1; j <= 5; j++)
                    if (boards[board, i, j] == seq[taken]) {
                        board_sum[board] -= seq[taken];
                        board_matched_x[board, i] += 1;
                        board_matched_y[board, j] += 1;
                        if (board_matched_x[board, i] == 5 || board_matched_y[board, j] == 5)
                            if (!board_won[board]) {
                                board_won[board] = 1;
                                if (length(board_won) == nboard) {
                                    print(board_sum[board] * seq[taken]);
                                    exit;
                                }
                            }
                    }
        }
    }
}
'
