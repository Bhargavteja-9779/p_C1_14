# Frozen protocol (pre-registration) - written 2026-11-24 after D6 round 4, BEFORE touching locked data

## Question
Can a stool-metagenome disease classifier keep its intended false-positive rate (FPR) at a new laboratory, and which
threshold-setting rules achieve this without labels at screening prevalence?

## Classifiers (fixed, not tuned on locked data)
LASSO logistic regression (C=0.1, L1, balanced) and random forest (500 trees, min_samples_leaf=2), log10 relative
abundance, 5% prevalence filter, z-scored on training data (src/models.py). Source out-of-fold scores via
leave-one-cohort-out inside the training cohorts.

## Threshold rules compared (src/calibrate.py; all frozen)
source (training-control quantile), local_q (quantile of unlabelled pool), em (Saerens 2002), mlls (MLLS-BCTS,
Alexandari 2020), gauss2 (unsupervised 2-Gaussian calibration), shift2 (site-shift mixture, bounded), featstd (per-site
feature standardisation with pool statistics), ctrl10 (conformal, 10 labelled local controls), rpoolmean
(contamination-robust rank rule, E[FPR] <= alpha for case share <= pi_max = 0.05), rpool (same, P(FPR > alpha) <= delta = 0.10).
Primary method: rpoolmean (label-free). rpool reported with its abstention rate.

## Locked evaluation (each run once)
1. CRC external: train on the 8 development cohorts; test on YachidaS_2019, YuJ_2015, ThomasAM_2019_c.
2. IBD, T2D, adenoma-vs-control: leave-one-cohort-out over their cohorts (src/data.py DISEASES).
Within each test cohort, R = 200 random splits: half of controls (+ cases at share pi in {0, 0.01, 0.05, 0.2}) form the
unlabelled pool; the other half of controls and cases form the evaluation set. ctrl10 uses 10 pool controls with labels.
alpha = 0.10 (primary), 0.05 (secondary).

## Endpoints
Primary: per-cohort mean realised FPR minus alpha, summarised as cohort-RMSE (systematic miscalibration), at pi = 0.01.
Secondary: mean FPR, sensitivity, P(realised FPR > alpha + 0.05), abstention; consequences per 1,000 screened at
prevalence 0.5% (CRC): extra colonoscopies = 1000 * 0.995 * (FPR - alpha) and cancers detected = 1000 * 0.005 * sens.
Statistics: paired comparison rpoolmean vs each rule on |cohort-mean FPR - alpha| across test cohorts (all diseases,
both models): Wilcoxon signed-rank + cohort-level bootstrap 95% CI of the mean difference; Holm correction over rules.
Motivating analysis: overdispersion of realised FPR of the source threshold across cohorts (chi-square vs binomial).

## Known limitations fixed in advance
Random within-cohort splits make pool and evaluation exchangeable by design; the cross-study stress test (dev round 4B)
is the evidence about non-exchangeable pools. Locked pools are mostly below the ~360 samples the rpool guarantee needs.
