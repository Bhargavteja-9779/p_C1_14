# 2026-11-25 — DIAGNOSIS (review round 11)
The v6b "case-mix" fix works mostly by changing the geographic make-up of training (equal weight per country x label
group). Label balance within countries alone, keeping country shares, removes only 37% of the East Asian gap (CI includes
0). The v6c disease-classifier weighting had a double-normalisation bug (weights() divided by country size twice) -> v6c
uninterpretable; removed from the main text. Variance decomposition: H2 failed; after removing sampling noise LASSO
pair-specific 48%, RF classifier 46%.
SLIP: importing run_v6c.py (no __main__ guard) re-ran it and overwrote two result files; restored from git. The rerun
differed slightly (unseeded liblinear) -> noted in SI.
v14 written (title tempered; 28 refs, 5 new verified); audit 164/164; fprcal 13 tests pass.
