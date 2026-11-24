# Analysis plan v5 (cycle 5) — 14-test specificity atlas. Written 2026-11-24 BEFORE any v5 atlas result.

Context: v1-v4 studied 3 disease tests (CRC, IBD, T2D). Cycle 5 widens to every disease with a usable case-control
cohort in curatedMetagenomicData, to test whether the population dependence of the false-positive rate (FPR) is
general, whether some populations are over-flagged by many tests at once, and which taxa recur as false-alarm drivers.
DEV-only exploration done so far in cycle 5: geography-stable feature penalisation (failed; dev_gsp.csv). Nothing in
this plan has been run.

## Tests (classifier x disease), all on de-duplicated data (v4 P0), LASSO and RF with the v4 fixed settings
Multi-cohort (leave-one-cohort-out OOF cut-off): CRC (10 cohorts), adenoma (5), IBD (4), T2D (4), IGT (3).
Single-cohort (5-fold stratified OOF cut-off, seed 0): CAD, HF (MetaCardis_2020_a); ACVD (JieZ_2017); cirrhosis
(QinN_2014); hypertension (LiJ_2017); schizophrenia (ZhuF_2020); ME/CFS (NagySzakalD_2017); migraine (XieH_2016);
fatty liver (LoombaR_2017). Rule: cases >= 30 and controls >= 30 adults (one sample per person).
Cut-off: 90th percentile of OOF control scores (target FPR 0.10). AUROC (OOF) is reported for every test.
Healthy populations: v4 strict set (primary) and full set (sensitivity); every cohort used to train a test is excluded
from that test's populations; populations with >= 20 people.

## Pre-stated hypotheses
H1 (generality): the between-population FPR heterogeneity seen for 3 tests holds broadly: I2 >= 0.50 for at least
    20 of the 28 classifier-disease tests (strict set). WRONG if fewer than 14 of 28.
H2 (shared false-alarm propensity): some populations are over-flagged by many tests at once. Crossed random-effects
    model on logit FPR (test and population as crossed random effects; LASSO and RF analysed separately): the
    population variance component is >= 20% of the total between-unit variance. WRONG if < 10%.
H3 (recurrent drivers): in the LASSO decompositions (v4 P8 method), at least 5 taxa are among the top-10 positive
    contributors in the most over-flagged population of >= 4 different tests. WRONG if no taxon recurs in >= 3 tests.
H4 (local fix generalises): within-site non-random burn-in (accession order and covariate halves, N = 100, as v4 P4)
    gives lower mean |FPR - 0.10| than the training cut-off in >= 75% of the 28 tests. WRONG if < 50%.
Secondary/descriptive: FPR vs AUROC across tests (does a better test have a more stable FPR?); FPR vs geography
(world map); per-population "false-alarm index" = mean over tests of logit FPR deviation.
Multiplicity: H1-H4 are the confirmatory family (Holm over their P values where a P value exists).
Every other analysis is labelled exploratory.

## Addendum A (2026-11-24, written AFTER the exploratory explore_v5.py result on the strict set, BEFORE the replication)
Exploratory finding on the 36 strict populations: (i) populations outside Europe/North America (country list EUNA in
explore_v5.py, fixed) have a higher cross-test false-alarm index; (ii) a population's compositional distance from a
test's training controls is positively rank-correlated with its FPR in 12/14 LASSO tests.
Replication set (never used for (i)-(ii)): populations in the FULL de-duplicated set that are NOT in the strict set
(study-level exclusions; all adult controls), n >= 20, each test excluding its training cohorts.
H5: distance-to-training vs FPR Spearman rho > 0 in >= 9 of 14 LASSO tests (one-sided sign test P < 0.05).
    WRONG if <= 7 of 14.
H6: false-alarm index (mean over the 14 LASSO tests of logit-FPR deviation from the test mean, computed on the
    replication populations plus the strict populations as reference) is higher for non-EUNA than EUNA replication
    populations (one-sided Mann-Whitney P < 0.05). WRONG if the median difference is <= 0.
RF results are reported as secondary.
