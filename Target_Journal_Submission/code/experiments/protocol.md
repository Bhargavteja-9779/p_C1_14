# Pre-registered protocol (frozen 2026-11-23, committed BEFORE any locked-cohort result is computed)

Development results that motivated every choice below: `novelty_escalation_log.md` (rounds 1-2, 8 dev CRC cohorts only).
Code that implements this protocol: `experiments/final/run_locked.py` (committed together with this file).
Nothing in this file may be changed after the locked run. Deviations go in a dated "Deviations" section at the end.

## Question
When a gut-metagenome disease classifier is moved to a new site, does a decision threshold chosen for a target
false-positive rate (FPR) keep that FPR, and which deployment step restores it?

## Data (curatedMetagenomicData 2021-03-31 MetaPhlAn3 species profiles; MetaCardis 2022-10-19 release)
Stool, case vs control, first sample per subject. Cohort sizes (controls/cases):
- CRC external (train on the 8 dev cohorts, test once): YachidaS_2019 251/258, YuJ_2015 54/74, ThomasAM_2019_c 40/40.
- IBD LOSO: HMP_2019_ibdmdb 27/103, HallAB_2017 12/20, IjazUZ_2017 38/12, NielsenHB_2014 59/82.
- T2D LOSO: KarlssonFH_2013 43/53, MetaCardis_2020_a 642/550, QinJ_2012 174/170, SankaranarayananK_2015 18/19.
- Adenoma vs control LOSO: FengQ_2015 61/47, HanniganGD_2017 28/26, ThomasAM_2018a 24/27, YachidaS_2019 251/67, ZellerG_2014 61/42.
(The adenoma task reuses controls of dev CRC cohorts; adenoma cases were never used in development. This is disclosed.)

## Models (fixed, no tuning on locked data)
LASSO logistic regression (C=0.1, balanced) and random forest (500 trees, min leaf 2, balanced), on log10 relative
abundance of species with >5% prevalence in training data, z-scored on training data. Source scores for threshold
setting are leave-one-cohort-out out-of-fold scores within the training cohorts.

## Target FPR
Primary alpha = 0.10 (90% specificity). Secondary alpha = 0.05.

## Evaluation split inside each held-out cohort
R = 200 random splits. Target controls are split in half: a calibration half (the first n are "local controls")
and an evaluation half. Evaluation = evaluation-half controls (FPR) and all cases (sensitivity).
The unlabeled pool for label-free methods = calibration-half controls + all cases (natural prevalence) — label-free
methods never see labels. Local-control methods with n controls are evaluated only where the calibration half has
>= n controls; otherwise reported as "not feasible".

## Methods compared
1. `source` — (1-alpha) quantile of source out-of-fold control scores (status quo).
2. `cohortstd` — batch-correction baseline: features standardised within each cohort (target on its own samples), then source threshold.
3. `em` — prevalence (label-shift) EM, then threshold from implied target control CDF.
4. `pool_q` — (1-alpha) quantile of the unlabeled pool (label-free; valid only at low prevalence).
5. `site_shift` — location-scale mixture on unlabeled scores (our v1; failed in development, reported as negative result).
6. `anchor_loc`, `anchor_locscale` — source threshold moved by median (and IQR) of n local controls.
7. `conformal` — order statistic ceil((n+1)(1-alpha)) of n local controls (E[FPR] <= alpha). n in {10, 20, 30}.
8. `tong95` — order statistic with P(FPR > alpha) <= 0.05 (Tong, Feng & Li 2018). n in {30, 50}.
Recommended protocol = `conformal` with n = 20 (primary); `tong95` when >= 29-30 controls are available.

## Endpoints
Primary (per method, per disease task, per model):
- P1: between-site dispersion = SD across held-out cohorts of the cohort-mean realised FPR; and max |cohort-mean FPR - alpha|.
- P2: share of (cohort x split) with realised FPR > 1.5 alpha.
Secondary: mean sensitivity; for tong95 the share of splits with FPR <= alpha (target >= 0.95);
overdispersion of `source` realised FPR vs binomial (chi-square over cohorts, using full-cohort counts);
harm per 1,000 screened at assumed prevalence p (CRC p = 0.005 primary, 0.01 sensitivity analysis):
false positives = 1000 (1-p) FPR, missed cases = 1000 p (1 - sens).
Uncertainty: 95% intervals by cohort-level bootstrap (2,000 resamples) for P1 differences conformal(n=20) - source.

## Pre-stated success criterion
The recommended protocol (conformal, n=20) succeeds if, pooled over all feasible cohort x model pairs at alpha=0.10,
>= 90% have cohort-mean FPR within [0.05, 0.15], AND the SD of cohort-mean FPR is smaller than for `source`
in every disease task. The drift claim holds if `source` has cohort-mean FPR outside [0.05, 0.15] in >= 30% of pairs.
Both outcomes are reported whatever they are.

## Deviations
(none yet)
