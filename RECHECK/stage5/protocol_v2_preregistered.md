# Protocol v2 (written 2026-11-23 BEFORE any v2 experiment was run; supersedes first-run data_lock where stated)

## Question
When a gut-microbiome disease classifier is moved to a new site, does its *operating point* (decision threshold chosen for
a target false-positive rate, alpha = 0.10) transfer, and which deployment-time fix restores the target rate?

## Data (curatedMetagenomicData, MetaPhlAn3 species profiles, stool, one sample per subject, case vs control)
- CRC: 10 cohorts (ThomasAM_2019_c REMOVED: its 80 samples duplicate YachidaS_2019 samples - leakage bug of first run).
  Development: 8 cohorts (unchanged). Locked external: YachidaS_2019, YuJ_2015 (models trained on 8 dev cohorts).
- Locked other diseases (never used in development): IBD (4 cohorts), T2D (4), adenoma vs control (5).
  Note: adenoma shares control subjects with CRC cohorts; it is a different case definition, not an independent population.
- Within-cohort near-duplicate profiles (log-profile r > 0.99) removed, keeping the first.

## Classifiers (fixed, standard, no tuning; same as pilot)
LASSO logistic regression (C=0.1, balanced) and random forest (500 trees, min leaf 2, balanced_subsample), on
log10(rel.abundance+1e-5), features with >5% prevalence in training, z-scored with training stats.
Source threshold uses out-of-fold (leave-one-cohort-out inside training) control scores.

## Deployment simulation at each held-out site (unit of analysis = site)
Random split of the held-out site into a deployment POOL (half of controls + cases to give pool prevalence pi) and an
EVALUATION set (the other half of controls and cases). pi in {0, 0.10, 0.30}. 10 seeds x 50 splits = 500 splits per site.
Methods (all choose a threshold; none uses evaluation labels):
 M0 source threshold (status quo)
 M1 local quantile of unlabeled pool (assumes pool = controls)
 M2 EM prior-shift adjustment (Saerens 2002) + mixture subtraction
 M3 known-prevalence mixture subtraction (pi given, e.g. from epidemiology)
 M4 site-shift mixture model (affine score shift, class shapes from source, ML on unlabeled pool)
 M5 split-conformal threshold from n labelled local controls, n in {10, 20} (taken from pool controls)
 Oracle: evaluation-control quantile (reference only).
Feature-level test-time re-standardisation (z-score target features with unlabeled pool statistics) is evaluated as an extra
baseline (M6) because it is a common batch-effect fix.

## Primary endpoint
Mean absolute deviation of realised FPR from alpha, |FPR - 0.10|, averaged over splits, per site; compared between methods
paired by site (Wilcoxon signed-rank, Holm correction over the pre-specified comparisons vs M0), plus site-level
bootstrap 95% CIs. Secondary: P(FPR > 0.15) ("violation rate"), sensitivity, sensitivity loss vs oracle, AUROC,
outcomes per 1,000 screened at prevalence 0.6% (CRC screening) and 5% (FIT-positive referral) - stated as illustrative.
Overdispersion test of realised FPR vs binomial for the status-quo threshold.

## Rules
Method design/selection on development CRC cohorts only. Locked sets run once with the frozen method list.
Every idea tried is logged in RECHECK/novelty_elevation_log.md with the count of ideas tried.
