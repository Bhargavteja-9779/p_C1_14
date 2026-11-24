<!-- DRAFT v0.1 (2026-11-24). [[...]] filled after the locked run. -->
# Supporting Information

## Methods

### Data
Species-level relative abundances (MetaPhlAn3) and sample metadata were obtained from curatedMetagenomicData [7]
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
- Label-shift EM [9]: target prevalence estimated by EM with kernel density estimates of the training class score
  densities; control CDF recovered by subtracting the estimated case component.
- MLLS-BCTS [10]: bias-corrected temperature scaling on training scores, then maximum-likelihood prevalence; same
  deconvolution.
- Unsupervised two-Gaussian calibration [11]: two-component Gaussian mixture fitted by EM to the pool; t = (1 - alpha)
  quantile of the lower component.
- Location-scale mixture fit (ours, development): pool scores modelled as a + b * (training score) with the training
  class shapes and unknown prevalence, fitted by maximum likelihood (|log b| <= 1); t = a + b * (training cut-off).
- Per-site feature standardisation [12]: each training cohort and the target pool standardised with their own means
  and standard deviations; training cut-off applied.
- Ten labelled local controls: split-conformal order statistic, the ceil(11(1 - alpha))-th smallest score [14].
- Rank rule, expected-FPR version (primary): with pool size n and maximum case share pi_max = 0.05, let
  n0 = n - floor(pi_max n) and r = floor((n0 + 1) alpha); t is the r-th largest pool score.
- Rank rule, high-probability version: r is the largest integer with P(Beta(r, n0 - r + 1) > alpha) <= delta
  (delta = 0.10); if no such r exists the rule abstains.

### Note S1. Why the rank rule works
Assume the controls in the pool and future controls are exchangeable (they come from the same laboratory process) and
at most m = floor(pi_max n) pool samples are cases. Take the r-th largest pool score as t. (i) If all cases lie below t,
then t is the r-th largest of n - m controls. For continuous scores, the probability mass of the control distribution
above the r-th largest of n0 exchangeable controls follows Beta(r, n0 - r + 1) [13], with mean r / (n0 + 1). Choosing
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
screened used a CRC prevalence of 0.5% [18].

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
[[generated from data: cohort, disease, country, n controls, n cases, role]]

## Table S2. Full results by disease, model, case share and target FPR
[[from results/main_tables.md]]
