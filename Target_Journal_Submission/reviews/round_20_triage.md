# Round 20 triage (blind panel on v21: statistics 7.5 minor [rerun after the first statistics agent stopped before
# writing], novelty 8 minor, editor 7 minor; totals 75 / 78 / 74). Second consecutive all-minor panel (G10).

## Statistics
- M1 fold-model comparator: NEW post hoc `v5/posthoc_r20_perfold.py` (per-fold flags averaged; closer comparator).
  Heterogeneity 28/28 (I2 median 0.91); 65% outside 0.05-0.15; extremes shrink for LASSO; AUROC-tau rho = 0.41
  (P = 0.032). SI S2.3 now a three-column table (refit, per-fold, mean-logit). Main text, highlights, cover letter and
  conclusion reworded: "a higher AUROC did not mean a smaller spread" (true under every scoring). S2.1 bullet reconciled.
- M2 AUROC wording: see M1.
- m1 qualified ("if each cut-off were exactly calibrated"); m2 65% for AUROC >= 0.65 (posthoc_r20_numbers.py; the
  reviewer's 62% was not reproduced, file value used); m3 clustered CI cited, 75% of splits improved; m4 sensitivity
  about 0.25, three cohorts, no interval; m5 eight below / four above; m6 RF in-sample note; m7 kept; m8 "net".
## Novelty
- m1 benchmarks [13, 15, 16] report discrimination, not FPR at a fixed cut-off; m2 Poyet [12] lacks a per-population
  FPR; m3/m4 partly (AUROC finding now stated in its own sentence).
## Editor
- Number density: main text 134 numerals (v17 225); GMHI gate history, P = 0.10, 37%, 27 vs 36% moved to SI.
- Pixel-identical rebuild of all six submitted figures: scripts/check_figures_v22.py, 6/6 identical.
- Minors: LASSO 0-0.77 vs RF 0-0.87; cMD defined; "patients" in Fig 3B; S1 rule names and saw-tooth explained; Fig 1D CI
  in legend; Fig 2D rounding; one-claim highlights; drafting language removed from SI; checksum note in REPRODUCE.md.
- Author-only (unchanged): URL/DOI, author statements, AI-use statement (must mention the simulated review rounds named
  in plans v6/v7), right of reply to GMWI2/GMHI developers.
- Not done: Fig 1A marker overlap; single build entry point; fail-hard on missing studies.
