# Supporting Information — Methods

## S1. Data
We used species-level relative-abundance profiles from curatedMetagenomicData (Bioconductor; MetaPhlAn3; release
2021-03-31; MetaCardis_2020_a from release 2022-10-19), downloaded through ExperimentHub. We kept stool samples from
adults and, for longitudinal cohorts, the first sample per subject. Table S1 lists all cohorts, sample sizes and roles.

Cohort roles were fixed before any method was developed (data lock, Table S1):
- Development: eight CRC cohorts (FengQ_2015, GuptaA_2019, HanniganGD_2017, ThomasAM_2018a, ThomasAM_2018b,
  VogtmannE_2016, WirbelJ_2018, ZellerG_2014) and eleven non-cancer cohorts used to explore comorbidity effects
  (JieZ_2017, QinN_2014, LiJ_2017, ChengpingW_2017, ZhuF_2020, LoombaR_2017, LiJ_2014, VilaAV_2018, HMP_2019_t2d,
  NagySzakalD_2017, XieH_2016).
- Locked test: CRC sites YachidaS_2019, YuJ_2015, ThomasAM_2019_c; IBD (HMP_2019_ibdmdb, HallAB_2017, IjazUZ_2017,
  NielsenHB_2014); type 2 diabetes (KarlssonFH_2013, MetaCardis_2020_a, QinJ_2012, SankaranarayananK_2015); adenoma
  (FengQ_2015, HanniganGD_2017, ThomasAM_2018a, YachidaS_2019, ZellerG_2014; controls partly shared with CRC
  development). The locked analysis was run once, after the protocol was frozen (commit-time file hashes are provided
  with the code).

## S2. Classifiers
Features: species present in more than 5% of training samples; log10(abundance/100 + 10^-5); z-scored with training
mean and standard deviation. Models: L1-penalised logistic regression (C = 0.1, balanced class weights) and random
forest (500 trees, minimum leaf size 2, balanced subsamples). Model settings were fixed in advance and not tuned.
Scores were used on the logit scale. Out-of-fold source scores were obtained by leave-one-cohort-out cross-validation
within the training cohorts (5-fold stratified when fewer than three cohorts were available).

## S3. Threshold rules
The intended false-positive rate (FPR) is alpha = 0.10 (90% specificity).
1. Source threshold (status quo): the (1 - alpha) quantile of out-of-fold source control scores.
2. Local quantile: the (1 - alpha) quantile of unlabelled scores collected at the new site.
3. Prior adjustment (EM; Saerens et al. 2002).
4. Prevalence-bounded quantile: with an upper bound pi_max on disease prevalence, the unlabelled score distribution
   satisfies F_u = (1 - pi) F_0 + pi F_1, so F_0(t) >= (F_u(t) - pi_max)/(1 - pi_max). The threshold is the
   ceil((m + 1) q)-th order statistic of the m pooled scores with q = (1 - alpha)(1 - pi_max) + pi_max.
5. Labelled local controls: the conformal order statistic of n labelled local controls (expected FPR <= alpha).
6. Proposed — sequential verified-positive recalibration. In screening, every positive test is referred for
   colonoscopy, so the true status of referred people becomes known; the status of test-negative people does not.
   Month 1 uses a liberal threshold (source (1 - 2 alpha) control quantile). At the end of each month, for any
   candidate threshold t we count FP_ub(t) = verified controls with score >= t plus all unverified people with
   score >= t (people who were not referred under the threshold in force when they were tested, did not attend, or
   whose result is pending). Unverified people are thus counted as possible false positives, which keeps the bound
   valid whatever thresholds were used in the past. The number of controls is bounded from below by
   m0 = m - C1 - max(0, floor(pi_max m) - C1), with C1 the number of verified cases. The new threshold is the smallest
   t with (FP_ub(t) + 1)/(m0 + 1) <= alpha. A drift alarm restarts the pool from the most recent month whose verified
   false-positive count exceeds a Binomial(m0, alpha) one-sided test at p < 0.01.
7. Group-conditional version: rule 6 run separately within groups defined by recorded comorbidity.
8. Oracle (reference only): the (1 - alpha) quantile of the site's true control scores.

## S4. Deployment simulation
Each test cohort stands in for the population of a screening site. Each month, B = 100 people (200 in the comorbidity
analysis) are drawn with replacement at disease prevalence pi; thresholds are updated monthly for 12 months (18 with
drift). Because the site population is known, the true FPR and sensitivity of any threshold are computed exactly.
Settings: pi in {0.01, 0.05, 0.10} (adenoma {0.10, 0.30}); pi_max = max(0.05, pi); 200 streams per site and model.
Pre-specified sensitivity analyses: alpha in {0.05, 0.20}; misspecified pi_max; one-month follow-up delay; B in
{50, 200}; liberal burn-in at 1 - 3 alpha; kernel-smoothed site populations; 70% colonoscopy attendance; 5% of cancers
missed at colonoscopy; a +0.5 logit shift of all scores from month 7; all combined.

## S5. Endpoints and statistics
Primary endpoint: share of site-months (months 7-12) with true FPR > alpha + 0.02. Secondary: mean |FPR - alpha|,
sensitivity, unnecessary referrals and missed cases per 1,000 screened, burn-in referral rate. Comparisons are paired
by site and model (one-sided Wilcoxon signed-rank tests; 95% confidence intervals from a cluster bootstrap over sites,
2,000 resamples). Sensitivity non-inferiority to the oracle uses a margin of 0.05.
Comorbidity analysis: CRC models trained on all development CRC cohorts; within each locked cohort, the CRC score of
each condition group is compared with that cohort's own controls by linear regression on the logit score, adjusted for
age, BMI and sex where recorded; one-sided p values are Holm-corrected within model. Positivity ratios have bootstrap
95% confidence intervals (1,000 resamples).

## S6. Software and reproducibility
Python 3.13, scikit-learn, NumPy, SciPy, pandas, statsmodels. All code, the frozen protocol, the development log and
file hashes are available in the code repository (see Data Availability Statement).
