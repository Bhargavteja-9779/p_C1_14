# Response to review round 10 (manuscript v12 -> v13)

## Statistics (6/10, major)
1. v6c "pre-specified": ACCEPTED. protocol_v6c.md was committed together with its results; v6c is now labelled post hoc in
   the text and SI S6.5; the introduction says one plan was committed only with its results.
2. v6c does not support "confirming": ACCEPTED and extended. Corrected cluster bootstrap (corrected_boot_v13.py):
   CI −0.22 to −0.01. Level-free check: median absolute deviation of FPR lower in only 2/5 tests (mean 0.093 → 0.110);
   mean |FPR − 0.10| rose 0.150 → 0.249. Text now says balancing did not carry over cleanly; C2 and C3 failed; no
   generalisation claim. (Re-thresholding to a pooled FPR of 0.10 was not possible: v6c_rows stores counts only.)
3. v6b bootstrap: ACCEPTED. Corrected CI 41–149% (6% of draws below 50%); text says the CI includes values below the criterion.
4. G3: ACCEPTED. Main text states the in-sample-optimism hypothesis was falsified; Holm-adjusted P values reported
   (holm_v6_v13.py: G2 1.8e-12, G4 < 0.001, G3 0.72).
5. Unseen East Asian comparison: labelled post hoc.
6. Graphical abstract: "because" -> "consistent with"; 88% attributed to the retraining experiment; 62% and 79% separated;
   sensitivity cost mentioned.
7. GMWI2 stated FPR: defined in text as the share among 5,514 healthy people in 44 studies with ≥ 20 healthy people.
8. Different weighting schemes: stated in text and SI.

## Novelty (8/10, minor)
1. Ref 9 not resolving: REBUTTED. Crossref returns 10.3389/fmicb.2026.1971707 (Front Microbiol 2026; Europe PMC indexes
   it); a published correction (10.3389/fmicb.2026.2021752) is now cited alongside.
2. SIAMCAT country confounding: ACCEPTED. One sentence credits [8]; our contribution is framed as the consequence for a
   published index's FPR, its size and a retraining test.
3. Poyet 2026 wording: kept ("lose accuracy"), pending re-check of the final text (open item).
4. "confirming": removed (see statistics 2). 5. Optional: not added.

## Editor (8/10, minor)
1. 62–79% conflation: separated. 2. Fig 3C: H0 stated in text with n = 100. 3. References renumbered in order of first
citation. 4. Retrospective, within-cohort evaluation stated; prospective validation named as next step. 5. Sensitivity
cost already in main text (kept). 6. Kept. 7. I²: pointer to Table S2 (Q, PI). 8. Figure annotation: not changed in this
revision (figure files unchanged). Line-level: units harmonised in summary; GMWI2 training FPR clarified.
