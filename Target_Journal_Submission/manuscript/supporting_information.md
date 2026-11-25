<!-- DRAFT v0.2 (2026-11-25), locked results filled. -->
# Supporting Information

## Methods

### Data
Species-level relative abundances (MetaPhlAn3) and sample metadata were obtained from curatedMetagenomicData [13]
through ExperimentHub (release 2021-03-31; MetaCardis_2020_a from release 2022-10-19). Metadata came from the package's
`sampleMetadata` table. We kept stool samples labelled as the disease of interest or as control. For longitudinal
cohorts (HMP_2019_ibdmdb, HallAB_2017) we kept the first sample per subject, to avoid the same person appearing in the
pool and the evaluation set. Cohorts and sample counts are listed in Table S1.

### Split of cohorts (fixed before method design)
Development: eight CRC cohorts (FengQ_2015, GuptaA_2019, HanniganGD_2017, ThomasAM_2018a, ThomasAM_2018b,
VogtmannE_2016, WirbelJ_2018, ZellerG_2014). All method ideas were tried and chosen on these only (log of all ideas:
`code/experiments/novelty_escalation_log.md`). Locked test: three external CRC cohorts (YachidaS_2019, YuJ_2015,
ThomasAM_2019_c), and all cohorts of IBD (4), T2D (4) and adenoma versus control (5). The analysis protocol was written
and committed before the locked cohorts were scored (`code/experiments/protocol.md`), and each locked analysis was run
once.

### Classifiers
Features were log10(relative abundance + 1e-5) of species present in more than 5% of training samples, z-scored with
training statistics. LASSO: L1 logistic regression, C = 0.1, balanced class weights. Random forest: 500 trees, minimum
leaf size 2, balanced subsample weights. Training scores for setting thresholds were out-of-fold scores from
leave-one-cohort-out inside the training cohorts. Scores were used on the logit scale.

### Threshold rules
Let alpha be the target FPR (0.10 primary; 0.05 secondary). The rule predicts "positive" if score >= t.
- Training cut-off: (1 - alpha) quantile of out-of-fold training control scores.
- Local quantile: (1 - alpha) quantile of the unlabelled pool, assuming it holds only controls.
- Label-shift EM [15]: target prevalence estimated by EM with kernel density estimates of the training class score
  densities; control CDF recovered by subtracting the estimated case component.
- MLLS-BCTS [16]: bias-corrected temperature scaling on training scores, then maximum-likelihood prevalence; same
  deconvolution.
- Unsupervised two-Gaussian calibration [17]: two-component Gaussian mixture fitted by EM to the pool; t = (1 - alpha)
  quantile of the lower component.
- Location-scale mixture fit (ours, development): pool scores modelled as a + b * (training score) with the training
  class shapes and unknown prevalence, fitted by maximum likelihood (|log b| <= 1); t = a + b * (training cut-off).
- Per-site feature standardisation [18]: each training cohort and the target pool standardised with their own means
  and standard deviations; training cut-off applied.
- Ten labelled local controls: split-conformal order statistic, the ceil(11(1 - alpha))-th smallest score [20].
- Rank rule, expected-FPR version (primary): with pool size n and maximum case share pi_max = 0.05, let
  n0 = n - floor(pi_max n) and r = floor((n0 + 1) alpha); t is the r-th largest pool score.
- Rank rule, high-probability version: r is the largest integer with P(Beta(r, n0 - r + 1) > alpha) <= delta
  (delta = 0.10); if no such r exists the rule abstains.

### Note S1. Why the rank rule works
Assume the controls in the pool and future controls are exchangeable (they come from the same laboratory process) and
at most m = floor(pi_max n) pool samples are cases. Take the r-th largest pool score as t. (i) If all cases lie below t,
then t is the r-th largest of n - m controls. For continuous scores, the probability mass of the control distribution
above the r-th largest of n0 exchangeable controls follows Beta(r, n0 - r + 1) [19], with mean r / (n0 + 1). Choosing
r as above bounds the mean, or the upper delta-quantile, of the FPR by alpha. (ii) Each case above t pushes t up by one
control rank, which can only lower the FPR. (iii) Fewer than m cases gives a larger n0 and again a smaller FPR. So the
bound holds for any case share up to pi_max. Ties (frequent with LASSO, which gives equal scores to samples that carry
none of the selected species) make the rule more conservative because positives are called at score >= t. The rule
needs no model of how scores shift between sites. Its cost is that a pool with fewer cases than pi_max gives a slightly
lower FPR than alpha, which reduces sensitivity a little. The sample-size rule (Figure 2C) is the smallest n for
which the high-probability version gives an expected FPR of at least alpha - 0.02 when the pool holds no cases.

### Evaluation design
In each test cohort, controls and cases were split at random into halves, 200 times. Half of the controls, plus cases
at a share pi of 0, 1, 5 or 20%, formed the unlabelled pool. The other half of controls and cases formed the
evaluation set, where we measured the realised FPR and sensitivity. Ten pool controls (with labels) served the
labelled-control rule. Primary endpoint: cohort-RMSE, the root-mean-square over test cohorts and models of (mean
realised FPR - alpha), at pi = 1% and alpha = 0.10. Paired comparisons used the absolute error per cohort and model
(Wilcoxon signed-rank test, cohort-level bootstrap 95% CI, Holm correction across rules). Consequences per 1,000
screened used a CRC prevalence of 0.5% [5].

### Development exploration (not used for claims)
Four rounds on the development cohorts led to the final protocol (log in `code/experiments/novelty_escalation_log.md`).
Ideas that were dropped included the unlabelled location-scale mixture (fails at low prevalence), a hybrid that adds
ten labelled controls to it, and location or location-scale anchoring from ten labelled controls (more sensitive but
less reliable than conformal).

### Software
Python 3.13, scikit-learn, SciPy, pandas, matplotlib. One command reproduces all locked results:
`python code/experiments/final/run_final.py lasso` (and `rf`), then `python code/analysis/analyze_final.py` and
`python code/analysis/make_figures.py`.

## Table S1. Cohorts
Generated by `code/analysis/table_s1.py` -> `results/table_s1_cohorts.csv` (country as recorded in the metadata).
24 cohort-task pairs from 19 studies; 4,051 sample-task entries, 3,626 unique samples (the adenoma task reuses the
controls of five CRC studies). Note: four of the five adenoma cohorts share controls with CRC development cohorts, so
the adenoma task is new for the disease label but not for those controls.

## Table S2. Full results by disease, model, case share and target FPR
Generated by `code/analysis/analyze_final.py` -> `results/main_tables.md` (locked run, LASSO and random forest, R = 200
splits per cohort, 16 cohort-task pairs x 2 models = 32 units). cohort_rmse: root-mean-square over units of (mean realised
FPR - target). Abstention (threshold set to +inf) counts as FPR 0. Methods: source = training cut-off; local_q = plain
quantile of the unlabelled pool; em / mlls = label-shift EM and MLLS-BCTS; gauss2 = two-Gaussian unsupervised
calibration; shift2 = location-scale mixture fit; featstd = per-site feature standardisation; ctrl10 = conformal
threshold from 10 labelled local controls; rpoolmean / rpool = rank rule (expected-FPR / high-probability version).

### alpha = 0.1, case share in pool = 0.0

| method    |   cohort_rmse |   mean_fpr |   max_abs_err |   sens |   p_fpr_over_a_plus_5 |   abstain |   units |
|:----------|--------------:|-----------:|--------------:|-------:|----------------------:|----------:|--------:|
| ctrl10    |         0.027 |      0.086 |         0.1   |  0.24  |                 0.199 |     0.062 |      32 |
| rpoolmean |         0.031 |      0.082 |         0.1   |  0.249 |                 0.143 |     0.062 |      32 |
| local_q   |         0.046 |      0.137 |         0.119 |  0.335 |                 0.327 |     0     |      32 |
| rpool     |         0.08  |      0.025 |         0.1   |  0.076 |                 0.01  |     0.5   |      32 |
| shift2    |         0.153 |      0.221 |         0.372 |  0.434 |                 0.586 |     0     |      32 |
| source    |         0.185 |      0.162 |         0.635 |  0.387 |                 0.392 |     0     |      32 |
| featstd   |         0.203 |      0.23  |         0.51  |  0.412 |                 0.612 |     0     |      32 |
| gauss2    |         0.323 |      0.387 |         0.601 |  0.587 |                 0.792 |     0     |      32 |
| mlls      |         0.339 |      0.318 |         0.875 |  0.53  |                 0.611 |     0     |      32 |
| em        |         0.41  |      0.378 |         0.856 |  0.588 |                 0.64  |     0     |      32 |

### alpha = 0.1, case share in pool = 0.01

| method    |   cohort_rmse |   mean_fpr |   max_abs_err |   sens |   p_fpr_over_a_plus_5 |   abstain |   units |
|:----------|--------------:|-----------:|--------------:|-------:|----------------------:|----------:|--------:|
| ctrl10    |         0.027 |      0.086 |         0.1   |  0.24  |                 0.199 |     0.062 |      32 |
| rpoolmean |         0.031 |      0.082 |         0.1   |  0.249 |                 0.142 |     0.062 |      32 |
| local_q   |         0.046 |      0.137 |         0.119 |  0.334 |                 0.326 |     0     |      32 |
| rpool     |         0.08  |      0.025 |         0.1   |  0.075 |                 0.01  |     0.5   |      32 |
| shift2    |         0.153 |      0.221 |         0.372 |  0.433 |                 0.586 |     0     |      32 |
| source    |         0.185 |      0.162 |         0.635 |  0.387 |                 0.392 |     0     |      32 |
| featstd   |         0.203 |      0.23  |         0.51  |  0.412 |                 0.61  |     0     |      32 |
| gauss2    |         0.323 |      0.386 |         0.601 |  0.586 |                 0.792 |     0     |      32 |
| mlls      |         0.339 |      0.318 |         0.875 |  0.53  |                 0.611 |     0     |      32 |
| em        |         0.41  |      0.378 |         0.856 |  0.589 |                 0.641 |     0     |      32 |

### alpha = 0.1, case share in pool = 0.05

| method    |   cohort_rmse |   mean_fpr |   max_abs_err |   sens |   p_fpr_over_a_plus_5 |   abstain |   units |
|:----------|--------------:|-----------:|--------------:|-------:|----------------------:|----------:|--------:|
| ctrl10    |         0.027 |      0.086 |         0.1   |  0.24  |                 0.199 |     0.062 |      32 |
| rpoolmean |         0.037 |      0.072 |         0.1   |  0.229 |                 0.108 |     0.062 |      32 |
| local_q   |         0.04  |      0.126 |         0.119 |  0.322 |                 0.283 |     0     |      32 |
| rpool     |         0.082 |      0.021 |         0.1   |  0.065 |                 0.005 |     0.5   |      32 |
| shift2    |         0.135 |      0.205 |         0.351 |  0.421 |                 0.546 |     0     |      32 |
| source    |         0.185 |      0.162 |         0.635 |  0.387 |                 0.392 |     0     |      32 |
| featstd   |         0.192 |      0.22  |         0.51  |  0.406 |                 0.593 |     0     |      32 |
| gauss2    |         0.306 |      0.366 |         0.596 |  0.573 |                 0.763 |     0     |      32 |
| mlls      |         0.34  |      0.319 |         0.875 |  0.528 |                 0.61  |     0     |      32 |
| em        |         0.412 |      0.381 |         0.857 |  0.59  |                 0.643 |     0     |      32 |

### alpha = 0.1, case share in pool = 0.2

| method    |   cohort_rmse |   mean_fpr |   max_abs_err |   sens |   p_fpr_over_a_plus_5 |   abstain |   units |
|:----------|--------------:|-----------:|--------------:|-------:|----------------------:|----------:|--------:|
| ctrl10    |         0.027 |      0.086 |         0.1   |  0.24  |                 0.199 |     0.062 |      32 |
| local_q   |         0.043 |      0.092 |         0.096 |  0.26  |                 0.19  |     0     |      32 |
| rpoolmean |         0.059 |      0.049 |         0.1   |  0.161 |                 0.052 |     0.062 |      32 |
| rpool     |         0.084 |      0.019 |         0.1   |  0.077 |                 0.003 |     0.312 |      32 |
| shift2    |         0.1   |      0.168 |         0.25  |  0.386 |                 0.456 |     0     |      32 |
| featstd   |         0.155 |      0.185 |         0.485 |  0.386 |                 0.526 |     0     |      32 |
| source    |         0.185 |      0.162 |         0.635 |  0.387 |                 0.392 |     0     |      32 |
| gauss2    |         0.26  |      0.316 |         0.521 |  0.535 |                 0.687 |     0     |      32 |
| mlls      |         0.357 |      0.328 |         0.875 |  0.516 |                 0.587 |     0     |      32 |
| em        |         0.427 |      0.393 |         0.859 |  0.588 |                 0.633 |     0     |      32 |

### alpha = 0.05, case share in pool = 0.0

| method    |   cohort_rmse |   mean_fpr |   max_abs_err |   sens |   p_fpr_over_a_plus_5 |   abstain |   units |
|:----------|--------------:|-----------:|--------------:|-------:|----------------------:|----------:|--------:|
| rpoolmean |         0.029 |      0.029 |         0.05  |  0.146 |                 0.058 |     0.312 |      32 |
| rpool     |         0.045 |      0.006 |         0.05  |  0.019 |                 0.001 |     0.75  |      32 |
| ctrl10    |         0.05  |      0     |         0.05  |  0     |                 0     |     1     |      32 |
| local_q   |         0.056 |      0.093 |         0.156 |  0.272 |                 0.307 |     0     |      32 |
| shift2    |         0.134 |      0.156 |         0.37  |  0.351 |                 0.528 |     0     |      32 |
| source    |         0.162 |      0.111 |         0.616 |  0.305 |                 0.338 |     0     |      32 |
| featstd   |         0.197 |      0.182 |         0.549 |  0.353 |                 0.619 |     0     |      32 |
| gauss2    |         0.318 |      0.329 |         0.615 |  0.525 |                 0.785 |     0     |      32 |
| mlls      |         0.356 |      0.277 |         0.925 |  0.479 |                 0.588 |     0     |      32 |
| em        |         0.433 |      0.344 |         0.906 |  0.545 |                 0.623 |     0     |      32 |

### alpha = 0.05, case share in pool = 0.01

| method    |   cohort_rmse |   mean_fpr |   max_abs_err |   sens |   p_fpr_over_a_plus_5 |   abstain |   units |
|:----------|--------------:|-----------:|--------------:|-------:|----------------------:|----------:|--------:|
| rpoolmean |         0.029 |      0.029 |         0.05  |  0.145 |                 0.057 |     0.312 |      32 |
| rpool     |         0.045 |      0.006 |         0.05  |  0.019 |                 0.001 |     0.75  |      32 |
| ctrl10    |         0.05  |      0     |         0.05  |  0     |                 0     |     1     |      32 |
| local_q   |         0.056 |      0.093 |         0.156 |  0.271 |                 0.306 |     0     |      32 |
| shift2    |         0.134 |      0.155 |         0.37  |  0.351 |                 0.529 |     0     |      32 |
| source    |         0.162 |      0.111 |         0.616 |  0.305 |                 0.338 |     0     |      32 |
| featstd   |         0.197 |      0.182 |         0.549 |  0.353 |                 0.619 |     0     |      32 |
| gauss2    |         0.317 |      0.329 |         0.615 |  0.525 |                 0.785 |     0     |      32 |
| mlls      |         0.356 |      0.277 |         0.925 |  0.479 |                 0.588 |     0     |      32 |
| em        |         0.433 |      0.344 |         0.906 |  0.545 |                 0.622 |     0     |      32 |

### alpha = 0.05, case share in pool = 0.05

| method    |   cohort_rmse |   mean_fpr |   max_abs_err |   sens |   p_fpr_over_a_plus_5 |   abstain |   units |
|:----------|--------------:|-----------:|--------------:|-------:|----------------------:|----------:|--------:|
| rpoolmean |         0.032 |      0.023 |         0.05  |  0.117 |                 0.031 |     0.312 |      32 |
| rpool     |         0.045 |      0.006 |         0.05  |  0.017 |                 0     |     0.75  |      32 |
| ctrl10    |         0.05  |      0     |         0.05  |  0     |                 0     |     1     |      32 |
| local_q   |         0.05  |      0.083 |         0.156 |  0.253 |                 0.253 |     0     |      32 |
| shift2    |         0.118 |      0.142 |         0.345 |  0.338 |                 0.489 |     0     |      32 |
| source    |         0.162 |      0.111 |         0.616 |  0.305 |                 0.338 |     0     |      32 |
| featstd   |         0.186 |      0.173 |         0.549 |  0.346 |                 0.603 |     0     |      32 |
| gauss2    |         0.3   |      0.31  |         0.61  |  0.511 |                 0.755 |     0     |      32 |
| mlls      |         0.358 |      0.277 |         0.925 |  0.477 |                 0.588 |     0     |      32 |
| em        |         0.435 |      0.346 |         0.907 |  0.545 |                 0.622 |     0     |      32 |

### alpha = 0.05, case share in pool = 0.2

| method    |   cohort_rmse |   mean_fpr |   max_abs_err |   sens |   p_fpr_over_a_plus_5 |   abstain |   units |
|:----------|--------------:|-----------:|--------------:|-------:|----------------------:|----------:|--------:|
| local_q   |         0.037 |      0.056 |         0.111 |  0.175 |                 0.158 |     0     |      32 |
| rpoolmean |         0.039 |      0.014 |         0.05  |  0.068 |                 0.007 |     0.312 |      32 |
| rpool     |         0.046 |      0.005 |         0.05  |  0.014 |                 0     |     0.75  |      32 |
| ctrl10    |         0.05  |      0     |         0.05  |  0     |                 0     |     1     |      32 |
| shift2    |         0.086 |      0.11  |         0.246 |  0.297 |                 0.399 |     0     |      32 |
| featstd   |         0.149 |      0.14  |         0.518 |  0.322 |                 0.536 |     0     |      32 |
| source    |         0.162 |      0.111 |         0.616 |  0.305 |                 0.338 |     0     |      32 |
| gauss2    |         0.256 |      0.261 |         0.524 |  0.47  |                 0.664 |     0     |      32 |
| mlls      |         0.378 |      0.295 |         0.925 |  0.467 |                 0.584 |     0     |      32 |
| em        |         0.451 |      0.361 |         0.909 |  0.54  |                 0.623 |     0     |      32 |

### cohort-RMSE by disease (alpha 0.10, pi 0.01)

| method    |   CRC |   IBD |   T2D |   adenoma |
|:----------|------:|------:|------:|----------:|
| ctrl10    | 0.013 | 0.051 | 0.008 |     0.008 |
| em        | 0.08  | 0.289 | 0.484 |     0.53  |
| featstd   | 0.27  | 0.181 | 0.22  |     0.152 |
| gauss2    | 0.224 | 0.378 | 0.274 |     0.36  |
| local_q   | 0.026 | 0.063 | 0.044 |     0.041 |
| mlls      | 0.126 | 0.249 | 0.513 |     0.313 |
| rpool     | 0.071 | 0.093 | 0.075 |     0.078 |
| rpoolmean | 0.016 | 0.055 | 0.009 |     0.019 |
| shift2    | 0.226 | 0.196 | 0.103 |     0.068 |
| source    | 0.122 | 0.151 | 0.306 |     0.086 |

### Paired comparisons (alpha 0.10, pi 0.01; negative = rpoolmean closer to target)

| comparison          |   n_units |   mean_diff_abs_err |   ci_low |   ci_high |   p_wilcoxon |   p_holm |
|:--------------------|----------:|--------------------:|---------:|----------:|-------------:|---------:|
| rpoolmean - gauss2  |        32 |             -0.2668 |  -0.3143 |   -0.2192 |       0      |   0      |
| rpoolmean - featstd |        32 |             -0.1456 |  -0.1894 |   -0.1075 |       0      |   0      |
| rpoolmean - shift2  |        32 |             -0.1013 |  -0.1345 |   -0.0717 |       0      |   0      |
| rpoolmean - source  |        32 |             -0.1076 |  -0.1595 |   -0.0645 |       0      |   0      |
| rpoolmean - rpool   |        32 |             -0.056  |  -0.0665 |   -0.0454 |       0      |   0      |
| rpoolmean - em      |        32 |             -0.2621 |  -0.3692 |   -0.1625 |       0      |   0      |
| rpoolmean - mlls    |        32 |             -0.1991 |  -0.2942 |   -0.1121 |       0      |   0.0001 |
| rpoolmean - local_q |        32 |             -0.0173 |  -0.0255 |   -0.01   |       0.0001 |   0.0001 |
| rpoolmean - ctrl10  |        32 |              0.0055 |   0.001  |    0.01   |       0.0476 |   0.0476 |

### CRC external cohorts: consequences per 1,000 screened (prevalence 0.5%, target FPR 10%)

| method    |   fpr |   sens |   colonoscopies_per_1000 |   extra_vs_intended |   cancers_detected_per_1000 |
|:----------|------:|-------:|-------------------------:|--------------------:|----------------------------:|
| ctrl10    |  0.09 |   0.44 |                    92.64 |               -9.05 |                        2.19 |
| em        |  0.17 |   0.6  |                   175.34 |               72.85 |                        2.99 |
| featstd   |  0.35 |   0.74 |                   352.31 |              249.08 |                        3.72 |
| gauss2    |  0.3  |   0.7  |                   303.76 |              200.75 |                        3.5  |
| local_q   |  0.12 |   0.53 |                   124.72 |               22.58 |                        2.64 |
| mlls      |  0.21 |   0.65 |                   216.61 |              113.87 |                        3.24 |
| rpool     |  0.03 |   0.19 |                    34.57 |              -65.87 |                        0.94 |
| rpoolmean |  0.09 |   0.48 |                    89.56 |              -12.33 |                        2.4  |
| shift2    |  0.31 |   0.71 |                   307.44 |              204.4  |                        3.54 |
| source    |  0.2  |   0.65 |                   202.26 |               99.52 |                        3.23 |

### Overdispersion of source-threshold FPR across test cohorts (alpha 0.10)

- lasso: chi2 = 291.0, df = 16, p = 1.82e-52; FPR range 0.041-0.597
- rf: chi2 = 461.2, df = 16, p = 4.93e-88; FPR range 0.000-0.735

