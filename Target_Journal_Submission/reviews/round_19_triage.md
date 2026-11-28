# Round 19 triage (blind panel on v20: statistics 7 minor, novelty 8 minor, editor 7 minor; totals 72 / 77 / 73)

## Statistics (R1)
- M1 refit vs fold-model scoring: NEW ANALYSIS (post hoc) `v5/posthoc_r19_foldmodel.py`, all 28 classifiers. Scores reproduce
  the atlas to 9e-16. Heterogeneity and out-of-band share (70%) unchanged; share > 0.25 drops (LASSO 26% -> 15%); max
  0.87 -> 0.83; I2 >= 0.5 for 26/28. Reported in main text and SI S2.3. Headline moved to the robust out-of-band share.
- M2 overclaims: "AUROC does not warn" -> "did not predict"; "general-population cohorts" -> "groups of healthy adults
  (population cohorts and healthy controls)"; title no longer rests on the 0.87 extreme; highlights add that country size
  and case mix could not be separated.
- Minors 1-12: QC 704 shared samples (S2.2, Fig 2B legend); RF full set 10.2%; S2.1 gross vs net wording; H5 RF secondary
  (S5); 39% gross share 35% stated; unit-level H4 74.6%; unseen EA "suggestive"; Fig 3B hidden point + cohort choice in
  legend; GA overlap fixed; healthy-only burn-in stated in text and limits; N = 50 sentence NOT added (no result file;
  Table S8 holds N = 50 results).
## Novelty (R2)
- M1 SIAMCAT credit: intro now states what SIAMCAT showed and the four extensions. m1 gap re-scoped; m2 shared-training
  caveat in GA summary; m3 "or audit other released indices" in limits; m5 attributions kept.
## Editor (R3)
- GA overlap fixed (v21). Robust headline. Number density: main text 143 numerals (v17: 225). Reproducibility claim narrowed
  to logged runs; LICENSE added to fprcal; environment.yml and REPRODUCE.md updated; "not a diagnostic device" added.
  Methods as a list with a worked k example. SI pointers now say what they hold. Fig 1D, 2C, 2D, 3B legend, S1 title/order.
- REBUTTED: "To the Editor," and ALL-CAPS finding headings are kept; the benchmark of published iMeta Letters
  (journal_selection/benchmark_v2/style_v2.md) shows both.
- NOT DONE (scope): single build entry point / archiving superseded scripts; fail-hard on missing studies; Fig 1A colour
  scale; Fig 3B axis. Listed in HANDOFF.
