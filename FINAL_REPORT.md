# FINAL REPORT — status 2026-11-28

**Status: submission package v22 ready, pending author-only items.** Branch `claude/bold-clarke-qsp9pf`.
Package: `Target_Journal_Submission/submission_final_v22/` (manuscript and SI as md + docx, 3 figures, 2 supporting
figures, graphical abstract, highlights, cover letter, SUBMISSION_REPORT.md). Earlier reports (v10, v17) are superseded.

## The paper in one paragraph
"Gut-microbiome disease classifiers set for a 10% false-positive rate miss it in most healthy populations" (iMeta,
Letter). We scored 28 classifiers (LASSO and RF, 14 diseases) in 36 groups of healthy adults (6,525 people, 20
countries). In 70% of classifier–population pairs the false-positive rate (FPR) fell outside 5–15%, against about 15%
expected by chance; heterogeneity exceeded sampling noise for all 28 classifiers, and a higher AUROC did not mean a
smaller spread. The heterogeneity survives scoring with the cross-validation models behind the cut-off (65% outside;
28/28), though the most extreme LASSO values shrink. Two released gut-health indices (GMWI2, GMHI; largely shared
training data) labelled a median of 64% and 67% of healthy people in their own East Asian training studies as
non-healthy (12% and 21% elsewhere); retraining GMWI2 linked this to the geographic make-up of its training data. A
known label-free burn-in rule on 100 local people cut the within-site FPR error by 62% (retrospective), failed across
sites and costs sensitivity; it is released as `fprcal`.

## Gates (MASTER_PROMPT Section 7)
| Gate | Status | Evidence |
|---|---|---|
| G1 Journal | partial | iMeta Letter: received→accepted median 33 d, P75 52 d (n = 67, PubMed). JCR quartile from secondary sources only (UNVERIFIED). |
| G2 Prior art | pass | Novelty maps (135 records); r19/r20 novelty reviewers searched independently and found no prior report of the released-index audit. |
| G3 Novelty ≥ 20/25 | not met on the strict self-score | Last self-score 17/25. Blind reviewers rate novelty at or above benchmark P75 (7, 7, 8 in r20). The recalibration rule and spectrum effect are known and credited. |
| G4 Baselines | partial | Training cut-off, pooled/country/neighbour references, ComBat-style alignment, control augmentation, labelled local controls. DEBIAS-M, MMUPHin, ConQuR not run. |
| G5 Main result | partial | Within-site burn-in 28/28 classifiers (pre-specified criterion met), clustered CI 51–70%; earlier pooled hypothesis (≥ 50%) missed (48%). |
| G7 Generalisation | pass, limits stated | 14 diseases × 2 models × 36 (55) populations; two released indices; cross-site failure reported. |
| G8 Leakage | pass | Global de-duplication (119 samples). |
| G9 Reproducibility | pass (partial log) | Fresh-clone rerun of the v4 pipeline 30/30 identical; refit of all 28 atlas classifiers reproduces scores to 9e-16; all 6 submitted figures rebuild pixel-identically (`logs/check_figures_v22.txt`). No single logged end-to-end rerun of v5–v7. |
| G10 Review | pass | Two consecutive blind three-reviewer panels, all minor revision: r19 (7/8/7) and r20 (7.5/8/7). |
| G11 Number audit | pass (lenient) | v22: main text 70/70, SI 428/428, cover letter 13/13, highlights 5/5 numbers match result files. |

**User directive (top-notch = at or above P75 on every scorecard dimension):** met on 9 of 10 dimensions by all r20
reviewers. Clarity: 7, 8, 6 against a P75 of 7.25. v22 cuts main-text numerals from 225 (v17) to 134 and has not been
re-scored.

## This session (2026-11-28)
v17 → v22 over five blind review rounds (r16–r20). Main changes: clarity rewrite (2,400 → ~2,030 words); a post hoc
fold-model check for all 28 classifiers that found part of the LASSO over-flagging comes from scoring with the refitted
model (reported openly; headline moved to a robust number); SIAMCAT credit made explicit; overclaims softened;
robustness checks (Q2 clustered CI, Mongolia sensitivity, H4 at n ≥ 150, binomial power at fixed FPRs); figure fixes;
LICENSE for fprcal. Every step is in `reviews/round_19_triage.md`, `round_20_triage.md`, `journal/ENTRIES/` 19–20 and
`state/decisions.md`.

## What a human must do
1. Fill in author list and affiliations, CRediT contributions, conflicts of interest, funding and acknowledgments.
   Earlier author metadata from a parallel branch (first author P N Bhargav Teja, VIT Vellore; funding none; competing
   interests none) should be confirmed.
2. Write the AI-use statement (Wiley policy), including the simulated editor/reviewer checks named in plans v6 and v7.
3. Make the repository public, archive it on Zenodo, tag the `fprcal` release, and insert URL and DOI.
4. Send the GMWI2 and GMHI audits to their developers for a right of reply; say so in the cover letter.
5. Add suggested reviewers; check the current iMeta Letter limits (words, figures, graphical abstract, heading style).
6. Check Poyet et al. (Cell 2026) for GMHI results in non-industrialised populations.
7. Optional: run DEBIAS-M/MMUPHin (G4), which the sandbox could not install.

## Where everything is
- Package: `Target_Journal_Submission/submission_final_v22/`
- Code: `Target_Journal_Submission/code/` (atlas v4–v7, `tool/` = fprcal); run order in `REPRODUCE.md`
- Reviews and triage: `Target_Journal_Submission/reviews/`
- Diary and decisions: `journal/ENTRIES/`, `state/decisions.md`; resume: `HANDOFF.md`
