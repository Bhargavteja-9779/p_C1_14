# Response to review round 3 (manuscript v4 -> v5), 2026-11-24
Reports: review_r3_01_statistics_v4.md (7/10 minor), review_r3_02_novelty_v4.md (6/10 major), review_r3_03_editor_v4.md (5/10 major).

| Report # | Concern | Action in v5 |
|---|---|---|
| S1 | A5 "100%" guaranteed by averaging | Post hoc fair comparison on same 8 populations, per draw: local 79% vs country 46% (r3_posthoc.json, Table S12). |
| S2 | 48% mixes cross-site sub-sites into "within-site" | Within-site designs reported separately (57%, 12/13, P=0.0007, post hoc grouping); pre-stated pooled H-NX1 still reported as not supported. |
| S3 | Random-split burn-in error is data-independent | Text now says random splits show how miscalibrated the training cut-off is, not burn-in robustness. |
| S4 | Over-claim vs augmentation | Conclusion conditional; augmentation success with same population stated; different subsets of people noted. |
| S5 | Strict set includes case-control control arms | Stated; Table S1 lists every cohort. |
| S6 | 0-76% headline not size-filtered | Graphical abstract uses LASSO 0-62%; n>=100 ranges in text. |
| S7 | Fold-model check | Per-population max 0.14 reported. |
| S8 | small errors | P < 10^-9; random-effects pooled stated; Holm family rule stated (defined after results); cycle-3 fixes not rerun on dedup data - stated. |
| S9 | Contaminated burn-in narrow | Mis-specified pi_max result (0.082) added; 3 cohorts stated. |
| N1 | SIAMCAT under-described | Introduction states SIAMCAT measured external-control FPR (>2-fold); novelty restated; disagreement on augmentation discussed. |
| N2 | Recalibration literature missing | Leeflang 2013, Janssen 2008, Van Calster 2023, Roschewitz 2023, SACSIM 2026 added (Crossref-verified). |
| N3 | CRC-TrustBench, Poyet 2025 missing | Added (Crossref-verified; Poyet abstract checked). |
| N4 | DEBIAS-M mischaracterised; could run on burn-in | Text corrected (label-free on new batch). NOT RUN: installing its environment (Python 3.11 + torch) was blocked by the session's permission system; listed as untested competitor. Needs the user. |
| N5/N6 | Title/conclusion overreach; ref hygiene | Title "should be recalibrated at the site of use"; ref 12 cited; Bashari cited as arXiv; Wirbel 2019 0.097 pointed to Source Data Fig 3c. |
| E1 | SI stale | supporting_information_v4.md + si_tables_v4.md (S1-S12). |
| E2-E4 | Overstatement; 76%; clinical scope | Fixed; new "WHERE THIS APPLIES" section (screening vs referral). |
| E5 | Reproducibility | README run order; pinned packages; committed sha256-checked metadata; fatal fetch errors; fresh-clone test PASSED (identical outputs). |
| E6 | Declarations, Highlights, graphical abstract | Highlights + graphical abstract image added; author/COI/funding/AI statement remain placeholders for the authors; ethics expanded. |
| E7-E11 | Citations, figure labels, study codes, structure, I2 % | All done (figures_v5). Revision history moved to SI S3. |
