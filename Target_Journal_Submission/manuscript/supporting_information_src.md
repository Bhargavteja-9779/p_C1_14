<!-- DRAFT v0.3 (2026-11-25). SOURCE FILE: edit this, then run `python build.py`. -->
# Supporting Information

## Methods

### Data
Species-level relative abundances (MetaPhlAn3) and sample metadata were obtained from curatedMetagenomicData [@pasolli2017]
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
Let alpha be the target FPR (0.10 primary; 0.05 secondary). The locked run predicts "positive" if score >= t (see
Note S1 on ties).
- Training cut-off: (1 - alpha) quantile of out-of-fold training control scores.
- Local quantile: (1 - alpha) quantile of the unlabelled pool, assuming it holds only controls.
- Label-shift EM [@saerens2002]: target prevalence estimated by EM with kernel density estimates of the training class score
  densities; control CDF recovered by subtracting the estimated case component.
- MLLS-BCTS [@alexandari2020]: bias-corrected temperature scaling on training scores, then maximum-likelihood prevalence; same
  deconvolution.
- Unsupervised two-Gaussian calibration [@brummer2014]: two-component Gaussian mixture fitted by EM to the pool; t = (1 - alpha)
  quantile of the lower component.
- Location-scale mixture fit (ours, development): pool scores modelled as a + b * (training score) with the training
  class shapes and unknown prevalence, fitted by maximum likelihood (|log b| <= 1); t = a + b * (training cut-off).
- Per-site feature standardisation [@zheng2026]: each training cohort and the target pool standardised with their own means
  and standard deviations; training cut-off applied.
- Ten labelled local controls: split-conformal order statistic, the ceil(11(1 - alpha))-th smallest score [@angelopoulos2023].
- Rank rule, expected-FPR version (primary): with pool size n and maximum case share pi_max = 0.05, let
  n0 = n - floor(pi_max n) and r = floor((n0 + 1) alpha); t is the r-th largest pool score.
- Rank rule, high-probability version: r is the largest integer with P(Beta(r, n0 - r + 1) > alpha) <= delta
  (delta = 0.10); if no such r exists the rule abstains.

### Note S1. Why the rank rule works, and when it does not
The rule is a classical one-sided tolerance limit [@wilks1941] and the order-statistic step of the Neyman-Pearson umbrella
algorithm [@tong2018], applied to an unlabelled pool that may contain a few cases, as in noise-robust Neyman-Pearson
and conformal methods [@yao2023; @bashari2025]. We do not claim the rule as new; we test whether it serves
microbiome laboratories.

Assumption (A): conditional on the number K of cases in the pool, the n - K pool controls and a future control from the
same laboratory are exchangeable, and K does not depend on the control scores. Let t be the r-th largest pool score
and call a sample positive if its score is strictly above t (with ties, break them by a tiny random jitter, as in
conformal prediction; with continuous scores `> t` and `>= t` coincide).

Claim. Whatever the case scores, t is at least the r-th largest of the n - K pool controls, because removing cases can
only lower each order statistic. Under (A) and continuous control scores, the control mass above the r-th largest of
n - K exchangeable controls is Beta(r, n - K - r + 1). If K <= m = floor(pi_max n), then n - K >= n0 = n - m, and
Beta(r, n - K - r + 1) is stochastically no larger than Beta(r, n0 - r + 1). Hence E[FPR] <= r / (n0 + 1) <= alpha for
r = floor((n0 + 1) alpha), and P(FPR > alpha) <= delta for the high-probability choice of r. If K is random (in screening
K is about Binomial(n, prevalence)), both bounds gain the term P(K > m): E[FPR] <= alpha + P(K > m) and
P(FPR > alpha) <= delta + P(K > m). At 0.5% prevalence, pi_max = 5% and n = 360, P(K > 18) < 10^-9.

Ties. The locked run called positives at `>= t`. With a block of tied scores at t this is anti-conservative, not
conservative as an earlier draft stated. In our data ties sat at the lowest LASSO score and at discrete random-forest
votes; re-scoring with `> t` changed the cohort-RMSE by at most less than 0.001 (post-hoc E1, Table S4).

When the guarantee fails. (A) is violated when the pool comes from another study (E3) or another recruiting centre of
the same study (E5), or when the laboratory process drifts after calibration. The rule then has no guarantee, and our
post-hoc tests show FPRs well above the target (Table S4). The pool must be drawn from the population and process the
test will serve.

Sample-size rule (Figure 2C). The smallest n, on a grid of 10 below 1,000 and 100 above, for which the high-probability
version has expected FPR at least alpha - 0.02 when the pool holds no cases. The slack 0.02 is a choice; n = 360 for
pi_max = 0 and for 1%.

### Evaluation design (pre-registered, locked run)
In each test cohort, controls and cases were split at random into halves, 200 times. Half of the controls, plus cases
at a share pi of 0, 1, 5 or 20%, formed the unlabelled pool. The other half of controls and cases formed the
evaluation set, where we measured the realised FPR and sensitivity. Ten pool controls (with labels) served the
labelled-control rule. Primary endpoint: cohort-RMSE, the root-mean-square over test cohorts and models of (mean
realised FPR - alpha), at pi = 1% and alpha = 0.10. Paired comparisons used the absolute error per cohort and model
(Wilcoxon signed-rank test, bootstrap 95% CI, Holm correction across rules). Consequences per 1,000 screened used a CRC
prevalence of 0.5%, close to the 0.7% found in a large average-risk screening study [@imperiale2014].

Deviations and corrections found after the locked run (disclosed in response to review):
1. The number of cases in the pool was round(pi x n0 / (1 - pi)), which is 0 for pools of fewer than about 50
   controls. The pre-registered pi = 1% setting therefore contained no cases in 13 of 16 cohort-task pairs, and
   pi = 5% contained 0-2 cases in most. Robustness to cases in the pool is tested post hoc (E1).
2. The protocol named a cohort-level bootstrap; the analysis script resampled the 32 cohort x model units. The main
   text reports CIs clustered by cohort-task pair and Wilcoxon tests at the cohort-task level (Table S3); the
   unit-level results are kept in Table S2.
3. The random-forest run was interrupted by a container restart after 15 of 16 cohort-task pairs and finished with an
   exact replay of the random-number stream (`code/experiments/final/RUN_NOTES.md`); the replay was verified to
   reproduce the LASSO run exactly.

### Post-hoc experiments (exploratory; designed after the locked results and review round 1)
Code: `code/experiments/posthoc/explore_r1.py`; summaries: `code/analysis/posthoc_r1.py` -> `results/posthoc_r1_tables.md`.
Both classifiers, alpha 0.10 and 0.05, 200 splits unless stated.
- E1, cases in the pool: pools of the same size as in the locked run, of which K ~ Binomial(n, pi) are cases,
  pi in {0, 1, 2, 5, 10, 20%}. Ties scored both as `>= t` and `> t`.
- E2, pool size: in the three locked cohorts with at least 150 controls (YachidaS_2019 for CRC and adenoma, QinJ_2012,
  MetaCardis_2020_a), pools of n in {25, 50, 100, 200, 300, 500} samples (5% or 0% cases); all remaining samples
  evaluate. The share of deployments with FPR above alpha includes evaluation noise from the finite evaluation set.
- E3, pool from another cohort: for every ordered pair (A, B) of test cohorts of the same task, the model (trained
  without A and B) is calibrated on half of the controls of A and evaluated in B (50 splits).
- E5, pool from another centre: MetaCardis_2020_a (one protocol and sequencer; Copenhagen, Leipzig, Paris). Model
  trained on the other T2D cohorts; pool of half the controls of centre A, evaluation on centre B (or on the other
  half of A).

### Development exploration (not used for claims)
Four rounds on the development cohorts led to the final protocol (log in `code/experiments/novelty_escalation_log.md`).
Ideas that were dropped included the unlabelled location-scale mixture (fails at low prevalence), a hybrid that adds
ten labelled controls to it, and location or location-scale anchoring from ten labelled controls (more sensitive but
less reliable than conformal).

### Software
Python 3.13, scikit-learn, SciPy, pandas, matplotlib. One command reproduces all locked results:
`python code/experiments/final/run_final.py lasso` (and `rf`), then `python code/analysis/analyze_final.py` and
`python code/analysis/make_figures.py`. Post-hoc: `python code/experiments/posthoc/explore_r1.py <lasso|rf>
<E1|E2|E3|E5>`, then `python code/analysis/posthoc_r1.py`.

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


## Table S3. Locked run re-analysed: per-deployment error, clustered inference, alpha = 0.05 (post hoc)
Generated by `code/analysis/posthoc_r1.py`. ctrlset clusters CRC and adenoma pairs that share controls.

### E4a. Locked run, per-deployment view (each of 200 splits = one simulated laboratory)

alpha = 0.1, pi = 0 (pi = 0.01 is identical in 13 of 16 cohort-task pairs because the locked design rounded the number of cases to 0; see E1)

| method    |   cohort_rmse |   deploy_rmse |   p_fpr_gt_a_plus_5 |   p_fpr_gt_2a |   abstain |
|:----------|--------------:|--------------:|--------------------:|--------------:|----------:|
| source    |         0.185 |         0.193 |               0.392 |         0.287 |     0     |
| local_q   |         0.046 |         0.119 |               0.327 |         0.199 |     0     |
| em        |         0.41  |         0.44  |               0.64  |         0.526 |     0     |
| mlls      |         0.339 |         0.377 |               0.611 |         0.488 |     0     |
| gauss2    |         0.323 |         0.399 |               0.792 |         0.678 |     0     |
| shift2    |         0.153 |         0.2   |               0.586 |         0.429 |     0     |
| featstd   |         0.203 |         0.229 |               0.612 |         0.501 |     0     |
| ctrl10    |         0.027 |         0.103 |               0.199 |         0.131 |     0.062 |
| rpoolmean |         0.031 |         0.082 |               0.143 |         0.077 |     0.062 |
| rpool     |         0.08  |         0.085 |               0.01  |         0.003 |     0.5   |

alpha = 0.05, pi = 0 (pi = 0.01 is identical in 13 of 16 cohort-task pairs because the locked design rounded the number of cases to 0; see E1)

| method    |   cohort_rmse |   deploy_rmse |   p_fpr_gt_a_plus_5 |   p_fpr_gt_2a |   abstain |
|:----------|--------------:|--------------:|--------------------:|--------------:|----------:|
| source    |         0.162 |         0.169 |               0.338 |         0.338 |     0     |
| local_q   |         0.056 |         0.111 |               0.307 |         0.307 |     0     |
| em        |         0.433 |         0.462 |               0.623 |         0.623 |     0     |
| mlls      |         0.356 |         0.393 |               0.588 |         0.588 |     0     |
| gauss2    |         0.318 |         0.397 |               0.785 |         0.785 |     0     |
| shift2    |         0.134 |         0.178 |               0.528 |         0.528 |     0     |
| featstd   |         0.197 |         0.22  |               0.619 |         0.619 |     0     |
| ctrl10    |         0.05  |         0.05  |               0     |         0     |     1     |
| rpoolmean |         0.029 |         0.048 |               0.058 |         0.058 |     0.312 |
| rpool     |         0.045 |         0.046 |               0.001 |         0.001 |     0.75  |

### E4b. Paired comparisons with clustered bootstrap (alpha 0.10, pi 0.01)

| subset          | comparison          |   mean_diff | ci_cluster_task    | ci_cluster_controls   |   n_tasks |   p_wilcoxon_tasks |   p_holm |
|:----------------|:--------------------|------------:|:-------------------|:----------------------|----------:|-------------------:|---------:|
| all tasks       | rpoolmean - source  |     -0.1076 | -0.1817 to -0.0560 | -0.1800 to -0.0563    |        16 |             0.0001 |   0.0004 |
| all tasks       | rpoolmean - local_q |     -0.0173 | -0.0282 to -0.0081 | -0.0294 to -0.0075    |        16 |             0.0021 |   0.0043 |
| all tasks       | rpoolmean - em      |     -0.2621 | -0.3573 to -0.1697 | -0.3646 to -0.1678    |        16 |             0      |   0.0003 |
| all tasks       | rpoolmean - mlls    |     -0.1991 | -0.3230 to -0.0979 | -0.3188 to -0.0981    |        16 |             0.0006 |   0.0023 |
| all tasks       | rpoolmean - gauss2  |     -0.2668 | -0.3259 to -0.2080 | -0.3348 to -0.2026    |        16 |             0      |   0.0003 |
| all tasks       | rpoolmean - shift2  |     -0.1013 | -0.1421 to -0.0660 | -0.1408 to -0.0676    |        16 |             0.0001 |   0.0004 |
| all tasks       | rpoolmean - featstd |     -0.1456 | -0.1843 to -0.1118 | -0.1858 to -0.1141    |        16 |             0      |   0.0003 |
| all tasks       | rpoolmean - ctrl10  |      0.0055 | -0.0003 to 0.0117  | -0.0006 to 0.0125     |        16 |             0.1771 |   0.1771 |
| all tasks       | rpoolmean - rpool   |     -0.056  | -0.0702 to -0.0413 | -0.0713 to -0.0415    |        16 |             0.0007 |   0.0023 |
| without adenoma | rpoolmean - source  |     -0.1292 | -0.2291 to -0.0575 | -0.2262 to -0.0594    |        11 |             0.002  |   0.0098 |
| without adenoma | rpoolmean - local_q |     -0.0156 | -0.0310 to -0.0034 | -0.0311 to -0.0033    |        11 |             0.042  |   0.084  |
| without adenoma | rpoolmean - em      |     -0.2038 | -0.3150 to -0.1031 | -0.3142 to -0.1024    |        11 |             0.001  |   0.0088 |
| without adenoma | rpoolmean - mlls    |     -0.2013 | -0.3729 to -0.0639 | -0.3675 to -0.0598    |        11 |             0.0186 |   0.0557 |
| without adenoma | rpoolmean - gauss2  |     -0.2545 | -0.3156 to -0.1942 | -0.3160 to -0.1947    |        11 |             0.001  |   0.0088 |
| without adenoma | rpoolmean - shift2  |     -0.1291 | -0.1769 to -0.0849 | -0.1773 to -0.0852    |        11 |             0.001  |   0.0088 |
| without adenoma | rpoolmean - featstd |     -0.1596 | -0.2106 to -0.1170 | -0.2101 to -0.1170    |        11 |             0.001  |   0.0088 |
| without adenoma | rpoolmean - ctrl10  |      0.0045 | -0.0026 to 0.0121  | -0.0026 to 0.0120     |        11 |             0.3594 |   0.3594 |
| without adenoma | rpoolmean - rpool   |     -0.0542 | -0.0750 to -0.0344 | -0.0742 to -0.0342    |        11 |             0.002  |   0.0098 |

TOST rpoolmean vs ctrl10 (absolute FPR error, cohort-task level, margin +/-0.02): mean diff 0.0055, 90% CI -0.0002 to 0.0112, p = 0.0002

### E4c. Locked run, alpha = 0.05 (pre-registered secondary), cohort-RMSE by case share

| method    |   0.0 |   0.01 |   0.05 |   0.2 |
|:----------|------:|-------:|-------:|------:|
| source    | 0.162 |  0.162 |  0.162 | 0.162 |
| local_q   | 0.056 |  0.056 |  0.05  | 0.037 |
| em        | 0.433 |  0.433 |  0.435 | 0.451 |
| mlls      | 0.356 |  0.356 |  0.358 | 0.378 |
| gauss2    | 0.318 |  0.317 |  0.3   | 0.256 |
| shift2    | 0.134 |  0.134 |  0.118 | 0.086 |
| featstd   | 0.197 |  0.197 |  0.186 | 0.149 |
| ctrl10    | 0.05  |  0.05  |  0.05  | 0.05  |
| rpoolmean | 0.029 |  0.029 |  0.032 | 0.039 |
| rpool     | 0.045 |  0.045 |  0.045 | 0.046 |

abstention rate at alpha = 0.05:
| method    |   0.0 |   0.01 |   0.05 |   0.2 |
|:----------|------:|-------:|-------:|------:|
| source    | 0     |  0     |  0     | 0     |
| local_q   | 0     |  0     |  0     | 0     |
| em        | 0     |  0     |  0     | 0     |
| mlls      | 0     |  0     |  0     | 0     |
| gauss2    | 0     |  0     |  0     | 0     |
| shift2    | 0     |  0     |  0     | 0     |
| featstd   | 0     |  0     |  0     | 0     |
| ctrl10    | 1     |  1     |  1     | 1     |
| rpoolmean | 0.312 |  0.312 |  0.312 | 0.312 |
| rpool     | 0.75  |  0.75  |  0.75  | 0.75  |


## Table S4. Post-hoc experiments E1, E2, E3 and E5 (exploratory)

### E1. Cases actually in the pool: K ~ Binomial(n, pi) (both models, alpha 0.10)

models: ['lasso', 'rf']

|                     |   cohort_rmse |   cohort_rmse_strict_ties |   deploy_rmse |   max_cohort_fpr |   sens |   abstain |   mean_cases_in_pool |
|:--------------------|--------------:|--------------------------:|--------------:|-----------------:|-------:|----------:|---------------------:|
| (0.0, 'ctrl10')     |         0.011 |                     0.011 |         0.099 |            0.109 |  0.275 |     0     |                0     |
| (0.0, 'local_q')    |         0.044 |                     0.044 |         0.118 |            0.202 |  0.332 |     0     |                0     |
| (0.0, 'rpool')      |         0.08  |                     0.08  |         0.085 |            0.073 |  0.075 |     0.5   |                0     |
| (0.0, 'rpoolmean')  |         0.03  |                     0.03  |         0.082 |            0.111 |  0.249 |     0.062 |                0     |
| (0.0, 'source')     |         0.184 |                     0.184 |         0.192 |            0.729 |  0.386 |     0     |                0     |
| (0.01, 'ctrl10')    |         0.011 |                     0.011 |         0.099 |            0.109 |  0.275 |     0     |                0.607 |
| (0.01, 'local_q')   |         0.043 |                     0.043 |         0.117 |            0.204 |  0.33  |     0     |                0.541 |
| (0.01, 'rpool')     |         0.08  |                     0.08  |         0.085 |            0.073 |  0.074 |     0.5   |                0.541 |
| (0.01, 'rpoolmean') |         0.031 |                     0.031 |         0.082 |            0.106 |  0.246 |     0.062 |                0.541 |
| (0.01, 'source')    |         0.184 |                     0.184 |         0.192 |            0.729 |  0.386 |     0     |                0.541 |
| (0.02, 'ctrl10')    |         0.011 |                     0.011 |         0.099 |            0.109 |  0.275 |     0     |                1.221 |
| (0.02, 'local_q')   |         0.042 |                     0.042 |         0.116 |            0.207 |  0.328 |     0     |                1.09  |
| (0.02, 'rpool')     |         0.081 |                     0.081 |         0.085 |            0.071 |  0.071 |     0.5   |                1.09  |
| (0.02, 'rpoolmean') |         0.032 |                     0.032 |         0.082 |            0.106 |  0.241 |     0.062 |                1.09  |
| (0.02, 'source')    |         0.184 |                     0.184 |         0.192 |            0.729 |  0.386 |     0     |                1.09  |
| (0.05, 'ctrl10')    |         0.011 |                     0.011 |         0.099 |            0.109 |  0.275 |     0     |                3.072 |
| (0.05, 'local_q')   |         0.038 |                     0.038 |         0.112 |            0.207 |  0.319 |     0     |                2.734 |
| (0.05, 'rpool')     |         0.082 |                     0.082 |         0.085 |            0.068 |  0.068 |     0.5   |                2.734 |
| (0.05, 'rpoolmean') |         0.034 |                     0.034 |         0.082 |            0.105 |  0.23  |     0.062 |                2.734 |
| (0.05, 'source')    |         0.184 |                     0.184 |         0.192 |            0.729 |  0.386 |     0     |                2.734 |
| (0.1, 'ctrl10')     |         0.011 |                     0.011 |         0.099 |            0.109 |  0.275 |     0     |                6.258 |
| (0.1, 'local_q')    |         0.039 |                     0.039 |         0.11  |            0.212 |  0.304 |     0     |                5.567 |
| (0.1, 'rpool')      |         0.083 |                     0.083 |         0.086 |            0.064 |  0.061 |     0.5   |                5.567 |
| (0.1, 'rpoolmean')  |         0.041 |                     0.041 |         0.082 |            0.113 |  0.211 |     0.062 |                5.567 |
| (0.1, 'source')     |         0.184 |                     0.184 |         0.192 |            0.729 |  0.386 |     0     |                5.567 |
| (0.2, 'ctrl10')     |         0.011 |                     0.011 |         0.099 |            0.109 |  0.275 |     0     |               12.408 |
| (0.2, 'local_q')    |         0.048 |                     0.048 |         0.107 |            0.232 |  0.273 |     0     |               11.048 |
| (0.2, 'rpool')      |         0.085 |                     0.085 |         0.087 |            0.058 |  0.052 |     0.5   |               11.048 |
| (0.2, 'rpoolmean')  |         0.052 |                     0.052 |         0.083 |            0.129 |  0.176 |     0.062 |               11.048 |
| (0.2, 'source')     |         0.184 |                     0.184 |         0.192 |            0.729 |  0.386 |     0     |               11.048 |

### E2. Pool size in large cohorts (>= 150 controls; alpha 0.10). Evaluation on the remaining controls, so the share of draws with FPR > alpha includes evaluation noise.

|             |   ('mean_fpr', 'ctrl10') |   ('mean_fpr', 'local_q') |   ('mean_fpr', 'rpool') |   ('mean_fpr', 'rpoolmean') |   ('mean_fpr', 'source') |   ('p_fpr_gt_a', 'ctrl10') |   ('p_fpr_gt_a', 'local_q') |   ('p_fpr_gt_a', 'rpool') |   ('p_fpr_gt_a', 'rpoolmean') |   ('p_fpr_gt_a', 'source') |   ('p_fpr_gt_a_plus_5', 'ctrl10') |   ('p_fpr_gt_a_plus_5', 'local_q') |   ('p_fpr_gt_a_plus_5', 'rpool') |   ('p_fpr_gt_a_plus_5', 'rpoolmean') |   ('p_fpr_gt_a_plus_5', 'source') |   ('sens', 'ctrl10') |   ('sens', 'local_q') |   ('sens', 'rpool') |   ('sens', 'rpoolmean') |   ('sens', 'source') |
|:------------|-------------------------:|--------------------------:|------------------------:|----------------------------:|-------------------------:|---------------------------:|----------------------------:|--------------------------:|------------------------------:|---------------------------:|----------------------------------:|-----------------------------------:|---------------------------------:|-------------------------------------:|----------------------------------:|---------------------:|----------------------:|--------------------:|------------------------:|---------------------:|
| (0.0, 25)   |                    0.089 |                     0.128 |                   0.037 |                       0.076 |                    0.285 |                      0.336 |                       0.634 |                     0.078 |                         0.277 |                      0.667 |                             0.207 |                              0.313 |                            0.018 |                                0.1   |                             0.507 |                0.182 |                 0.257 |               0.094 |                   0.171 |                0.421 |
| (0.0, 50)   |                    0.083 |                     0.113 |                   0.037 |                       0.076 |                    0.285 |                      0.298 |                       0.545 |                     0.034 |                         0.241 |                      0.665 |                             0.167 |                              0.199 |                            0.004 |                                0.055 |                             0.506 |                0.175 |                 0.238 |               0.098 |                   0.177 |                0.421 |
| (0.0, 100)  |                    0.088 |                     0.106 |                   0.058 |                       0.087 |                    0.286 |                      0.339 |                       0.528 |                     0.072 |                         0.307 |                      0.655 |                             0.186 |                              0.125 |                            0.005 |                                0.046 |                             0.528 |                0.183 |                 0.23  |               0.147 |                   0.2   |                0.421 |
| (0.0, 200)  |                    0.087 |                     0.102 |                   0.069 |                       0.093 |                    0.096 |                      0.309 |                       0.461 |                     0.111 |                         0.349 |                      0.401 |                             0.195 |                              0.112 |                            0.019 |                                0.071 |                             0.264 |                0.196 |                 0.24  |               0.179 |                   0.223 |                0.231 |
| (0.0, 300)  |                    0.092 |                     0.104 |                   0.074 |                       0.095 |                    0.037 |                      0.34  |                       0.53  |                     0.12  |                         0.405 |                      0     |                             0.22  |                              0.05  |                            0.002 |                                0.012 |                             0     |                0.191 |                 0.233 |               0.182 |                   0.218 |                0.104 |
| (0.0, 500)  |                    0.09  |                     0.101 |                   0.078 |                       0.094 |                    0.036 |                      0.34  |                       0.47  |                     0.18  |                         0.372 |                      0.002 |                             0.195 |                              0.068 |                            0.008 |                                0.028 |                             0     |                0.191 |                 0.231 |               0.188 |                   0.218 |                0.104 |
| (0.05, 25)  |                    0.089 |                     0.121 |                   0.033 |                       0.071 |                    0.285 |                      0.332 |                       0.563 |                     0.06  |                         0.247 |                      0.667 |                             0.206 |                              0.28  |                            0.01  |                                0.084 |                             0.502 |                0.182 |                 0.245 |               0.084 |                   0.161 |                0.421 |
| (0.05, 50)  |                    0.083 |                     0.106 |                   0.035 |                       0.071 |                    0.285 |                      0.3   |                       0.5   |                     0.028 |                         0.212 |                      0.666 |                             0.167 |                              0.172 |                            0.004 |                                0.046 |                             0.51  |                0.175 |                 0.228 |               0.091 |                   0.167 |                0.421 |
| (0.05, 100) |                    0.088 |                     0.1   |                   0.054 |                       0.082 |                    0.285 |                      0.343 |                       0.472 |                     0.068 |                         0.266 |                      0.659 |                             0.193 |                              0.102 |                            0.002 |                                0.039 |                             0.53  |                0.183 |                 0.22  |               0.138 |                   0.191 |                0.421 |
| (0.05, 200) |                    0.087 |                     0.097 |                   0.063 |                       0.087 |                    0.097 |                      0.322 |                       0.428 |                     0.092 |                         0.311 |                      0.427 |                             0.192 |                              0.066 |                            0.006 |                                0.036 |                             0.251 |                0.196 |                 0.229 |               0.169 |                   0.213 |                0.231 |
| (0.05, 300) |                    0.092 |                     0.098 |                   0.069 |                       0.089 |                    0.037 |                      0.348 |                       0.502 |                     0.075 |                         0.332 |                      0     |                             0.222 |                              0.03  |                            0     |                                0.01  |                             0     |                0.191 |                 0.224 |               0.173 |                   0.209 |                0.104 |
| (0.05, 500) |                    0.091 |                     0.097 |                   0.073 |                       0.089 |                    0.036 |                      0.362 |                       0.438 |                     0.138 |                         0.32  |                      0     |                             0.205 |                              0.04  |                            0     |                                0.015 |                             0     |                0.191 |                 0.221 |               0.181 |                   0.207 |                0.104 |

Per cohort (pi = 0.05, rpool vs rpoolmean vs local_q, share of draws with FPR > 0.15):

|                            |   ctrl10 |   local_q |   rpool |   rpoolmean |   source |
|:---------------------------|---------:|----------:|--------:|------------:|---------:|
| ('MetaCardis_2020_a', 25)  |    0.198 |     0.265 |   0.008 |       0.072 |    0     |
| ('MetaCardis_2020_a', 50)  |    0.175 |     0.175 |   0.002 |       0.045 |    0     |
| ('MetaCardis_2020_a', 100) |    0.19  |     0.072 |   0     |       0.018 |    0     |
| ('MetaCardis_2020_a', 200) |    0.202 |     0.028 |   0     |       0.01  |    0     |
| ('MetaCardis_2020_a', 300) |    0.222 |     0.03  |   0     |       0.01  |    0     |
| ('MetaCardis_2020_a', 500) |    0.205 |     0.04  |   0     |       0.015 |    0     |
| ('QinJ_2012', 25)          |    0.195 |     0.272 |   0.005 |       0.08  |    1     |
| ('QinJ_2012', 50)          |    0.175 |     0.182 |   0.005 |       0.052 |    1     |
| ('QinJ_2012', 100)         |    0.18  |     0.13  |   0.008 |       0.055 |    1     |
| ('YachidaS_2019', 25)      |    0.225 |     0.304 |   0.019 |       0.099 |    0.507 |
| ('YachidaS_2019', 50)      |    0.152 |     0.158 |   0.004 |       0.041 |    0.53  |
| ('YachidaS_2019', 100)     |    0.209 |     0.105 |   0     |       0.044 |    0.591 |
| ('YachidaS_2019', 200)     |    0.182 |     0.105 |   0.012 |       0.062 |    0.502 |

### E3. Pool from ANOTHER cohort of the same task (a different laboratory), alpha 0.10

| method    |   pair_rmse |   median_fpr |   share_pairs_fpr_gt_15 |   max_fpr |
|:----------|------------:|-------------:|------------------------:|----------:|
| local_q   |       0.191 |        0.125 |                    0.48 |     0.754 |
| rpool     |       0.111 |        0     |                    0.11 |     0.43  |
| rpoolmean |       0.158 |        0.068 |                    0.33 |     0.691 |
| source    |       0.173 |        0.128 |                    0.46 |     0.75  |

| disease   |   local_q |   rpool |   rpoolmean |   source |
|:----------|----------:|--------:|------------:|---------:|
| CRC       |     0.086 |   0.073 |       0.068 |    0.12  |
| IBD       |     0.183 |   0.094 |       0.14  |    0.146 |
| T2D       |     0.253 |   0.138 |       0.23  |    0.204 |
| adenoma   |     0.173 |   0.112 |       0.133 |    0.181 |

### E5. Same study, different centre (MetaCardis_2020_a: one protocol and sequencer; Copenhagen, Leipzig, Paris), alpha 0.10

|                                       |   local_q |   rpool |   rpoolmean |   source |
|:--------------------------------------|----------:|--------:|------------:|---------:|
| ('lasso', 'Copenhagen', 'Copenhagen') |     0.105 |   0.061 |       0.089 |    0.01  |
| ('lasso', 'Copenhagen', 'Leipzig')    |     0.262 |   0.17  |       0.236 |    0.088 |
| ('lasso', 'Copenhagen', 'Paris')      |     0.206 |   0.113 |       0.18  |    0.045 |
| ('lasso', 'Leipzig', 'Copenhagen')    |     0.023 |   0.006 |       0.018 |    0.01  |
| ('lasso', 'Leipzig', 'Leipzig')       |     0.106 |   0.067 |       0.094 |    0.088 |
| ('lasso', 'Leipzig', 'Paris')         |     0.058 |   0.036 |       0.051 |    0.045 |
| ('lasso', 'Paris', 'Copenhagen')      |     0.058 |   0.019 |       0.046 |    0.01  |
| ('lasso', 'Paris', 'Leipzig')         |     0.163 |   0.096 |       0.143 |    0.088 |
| ('lasso', 'Paris', 'Paris')           |     0.108 |   0.054 |       0.087 |    0.044 |
| ('rf', 'Copenhagen', 'Copenhagen')    |     0.111 |   0.065 |       0.097 |    0.005 |
| ('rf', 'Copenhagen', 'Leipzig')       |     0.198 |   0.115 |       0.178 |    0.026 |
| ('rf', 'Copenhagen', 'Paris')         |     0.185 |   0.111 |       0.163 |    0.028 |
| ('rf', 'Leipzig', 'Copenhagen')       |     0.055 |   0.033 |       0.052 |    0.005 |
| ('rf', 'Leipzig', 'Leipzig')          |     0.107 |   0.066 |       0.096 |    0.025 |
| ('rf', 'Leipzig', 'Paris')            |     0.107 |   0.072 |       0.1   |    0.028 |
| ('rf', 'Paris', 'Copenhagen')         |     0.057 |   0.021 |       0.045 |    0.005 |
| ('rf', 'Paris', 'Leipzig')            |     0.109 |   0.051 |       0.083 |    0.026 |
| ('rf', 'Paris', 'Paris')              |     0.107 |   0.054 |       0.089 |    0.027 |

| setting                     |   local_q |   rpool |   rpoolmean |   source |
|:----------------------------|----------:|--------:|------------:|---------:|
| pool from another centre    |     0.077 |   0.057 |       0.067 |    0.072 |
| same centre (random halves) |     0.008 |   0.039 |       0.009 |    0.072 |
