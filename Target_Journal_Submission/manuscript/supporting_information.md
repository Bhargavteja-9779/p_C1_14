# Supporting Information

## Methods

### Data
We used species-level relative abundances (MetaPhlAn3) and sample metadata from curatedMetagenomicData [11]: release
2021-03-31 for all cohorts, and release 2022-10-19 for MetaCardis_2020_a. We kept stool samples labelled as case or control.
For cohorts with repeated samples (HMP_2019_ibdmdb, HallAB_2017), we kept the first sample per subject to avoid leakage
between training and test data and pseudo-replication. Diseases and cohorts are listed in Table S1. The adenoma task
re-uses the control samples of five CRC cohorts. Adenoma cases were never used during method development.

### Development and test separation
Before any method was explored, we split the data (file `code/experiments/data_lock.md`, committed before exploration).
Development used only eight CRC cohorts (FengQ_2015, GuptaA_2019, HanniganGD_2017, ThomasAM_2018a, ThomasAM_2018b,
VogtmannE_2016, WirbelJ_2018, ZellerG_2014), with nested leave-one-cohort-out. Two development rounds are logged in
`code/experiments/novelty_escalation_log.md`. A motivating pilot touched all 11 CRC cohorts with fixed standard models
and no method choice. The protocol (`code/experiments/protocol.md`) and the run script were committed before the locked run.
The locked run was executed once. There were no deviations from the protocol.

### Classifiers
Features were log10(relative abundance/100 + 10⁻⁵) for species present in more than 5% of training samples, z-scored
with training means and standard deviations. LASSO logistic regression: L1 penalty, C = 0.1, balanced class weights
(scikit-learn, liblinear). Random forest: 500 trees, minimum leaf size 2, balanced-subsample class weights. Hyper-parameters
were fixed in advance and not tuned. Scores were used on the logit scale. Source scores for threshold setting were
out-of-fold scores from leave-one-cohort-out within the training cohorts.

### Threshold-setting methods (target false-positive rate α)
- **Status quo (`source`)**: the (1 − α) quantile of out-of-fold training-control scores.
- **Cohort-wise standardisation (`cohortstd`)**: each species standardised within each cohort, including the target cohort
  on all its own samples (label-free). Then the model was retrained and the source rule applied. This is a simple
  location–scale batch correction [13, 14].
- **Prevalence EM (`em`)**: the EM prior update of Saerens et al. [15] with kernel density estimates of class-wise source
  scores. The target control CDF was recovered by subtracting the estimated case CDF from the target mixture CDF.
- **Unlabelled-pool quantile (`pool_q`)**: the (1 − α) quantile of all unlabelled target scores [19]. If prevalence is π
  and the pool quantile is taken at level 1 − β, the realised FPR lies between (β − π)/(1 − π) and β/(1 − π). The method is therefore
  only accurate when π is small.
- **Site-shift mixture (`site_shift`)**: our first-round proposal. Target scores were modelled as a + b × (source-equivalent score),
  with class-wise score shapes transported from the source and the mixing weight, a and b fitted by maximum likelihood on unlabelled
  target scores. The threshold was a + b × t_source.
- **Anchor (`anchor_loc`, `anchor_locscale`)**: the source threshold moved by the median (and rescaled by the inter-quartile range)
  of n labelled local controls relative to source controls.
- **Conformal (`conformal`)**: the k-th smallest of n local control scores, k = ⌈(n + 1)(1 − α)⌉. If local controls are
  exchangeable with future controls, E[FPR] ≤ α [17]. If k > n, no finite threshold exists.
- **95%-confidence rule (`tong95`)**: the smallest order statistic k with P(Binomial(n, 1 − α) ≥ k) ≤ 0.05, which gives
  P(FPR > α) ≤ 0.05 [18]. It needs n ≥ 29 for α = 0.10 and n ≥ 59 for α = 0.05.

### Evaluation
For each held-out cohort, controls were split at random into two halves 200 times (20 times for `em` and `site_shift`,
which are slow). The first n controls of the calibration half served as labelled local controls. The evaluation half gave
the realised FPR. All cases of the cohort gave sensitivity. The unlabelled pool for label-free methods was the calibration-half
controls plus all cases (natural prevalence). Local-control methods were evaluated only when the calibration half held at least n controls.

### Endpoints and statistics
All endpoints were pre-registered. P1: the standard deviation across held-out cohorts of cohort-mean FPR, and the
maximum absolute deviation from α. P2: the share of cohort × split cases with FPR > 1.5α. Secondary: mean sensitivity;
the share of splits with FPR ≤ α; over-dispersion of the status-quo FPR against a binomial with all controls of each cohort
(chi-square, df = number of cohorts); harm per 1,000 screened at CRC prevalence p = 0.5% (1% sensitivity analysis),
computed as 1000(1 − p)FPR false positives and 1000p(1 − sensitivity) missed cancers. Uncertainty for the difference in
between-cohort SD (conformal n = 20 minus status quo) used 2,000 cohort-level bootstrap resamples. The pre-stated success
criterion: conformal n = 20 within [0.05, 0.15] in ≥ 90% of feasible cohort × model pairs, with lower between-cohort SD
than the status quo in every disease task; the drift claim needed ≥ 30% of status-quo pairs outside the band. Post-hoc
analyses (Table S4) are labelled as such.

### Software and reproducibility
Python 3.13, scikit-learn, SciPy, pandas, matplotlib. Data download: `code/scripts/fetch_cmd.py`. Locked run:
`code/experiments/final/run_locked.py`. Endpoints: `analyse_locked.py`. Figures: `make_figures.py`. Tables: `make_si_tables.py`.
Post-hoc analyses: `extra_analyses.py`. Per-cohort scores are saved in `code/experiments/final/scores/`. The random seed
is fixed (20261123). Run time is about 30 minutes on 4 CPU cores.

## Supplementary figure

**Figure S1.** As Figure 1, for the random-forest classifier (`figures/FigureS1_fpr_by_cohort_rf.pdf`).

## Supplementary tables
See `si_tables.md` (Tables S1–S5), generated by `make_si_tables.py`.

## Development log summary (development cohorts only)
Round 1: the site-shift mixture failed (mean FPR 0.28–0.38 when the pool was mostly controls). Prevalence EM did not
fix FPR. The local quantile followed the prevalence bound. Round 2: conformal with 10 local controls reduced the
between-cohort SD of cohort-mean FPR from 0.14 to 0.01. Cohort standardisation and anchoring reduced but did not remove
drift. Full details: `code/experiments/novelty_escalation_log.md`.
