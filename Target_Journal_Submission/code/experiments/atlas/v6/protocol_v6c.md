# Analysis plan v6c — does geography-balanced training reduce the per-disease atlas FPR heterogeneity?
Written 2026-11-25 BEFORE running. Generalises the GMWI2 case-mix result (v6b) to the paper's own disease classifiers.

## Question
The atlas (Figure 1) shows population-specific FPR for 14 disease classifiers. v6b showed one cause for a health index
(pooled training over geographically unbalanced studies). Does the same training-time fix reduce the between-population
FPR heterogeneity of the DISEASE classifiers, on held-out healthy populations, without destroying discrimination?

## Classifiers and data (unchanged from the atlas; LASSO only, C=0.1)
The five multi-cohort tests (>= 3 training cohorts): CRC, adenoma, IBD, T2D, IGT (single-cohort tests cannot be
geography-balanced). MetaPhlAn3 species, >5% prevalence, log10 + z-score; cut-off = 90th pct of leave-one-cohort-out
out-of-fold control scores (target FPR 0.10). De-duplicated data (v4).

## Arms
- NAIVE: standard training (as the atlas).
- BALANCED: training-sample weights so that, within each training cohort's country, cases and controls carry equal total
  weight AND each country carries equal total weight (country + label balancing); cut-off re-derived from weighted OOF.
Evaluation: each classifier scored on its unseen healthy atlas populations (strict set, n>=20), exactly as the atlas.

## Hypotheses (falsifiers), Holm over C1-C3
- C1 (heterogeneity reduced): mean over the 5 tests of DerSimonian-Laird tau(logit FPR) across held-out populations is
  lower for BALANCED than NAIVE. FALSIFIED if not lower.
- C2 (calibration improved): mean over tests of the share of held-out populations with FPR outside [0.05,0.15] is lower
  for BALANCED. FALSIFIED if not lower.
- C3 (discrimination kept): mean held-out case-vs-control AUROC (over the training cohorts, leave-one-cohort-out) drops by
  <= 0.03 from NAIVE to BALANCED.
Uncertainty: population-clustered bootstrap (2000) for the tau difference (pooled across tests).
Primary = C1. This is one run; result reported whichever way it goes (the mechanism paper already stands on GMWI2).
