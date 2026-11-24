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
- Pilot (motivating analysis, before the data lock): fixed LASSO and random forest models across all 11 CRC cohorts
  (leave-one-cohort-out) with the cut-off at 90% specificity on training out-of-fold controls; realised specificity
  per held-out cohort was compared with Binomial(n0, 0.10) by a chi-square overdispersion test.

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

## S5. Species-level decomposition and specificity-constrained signatures (exploratory; development cohorts)
For the LASSO CRC model trained on all development CRC cohorts, the score difference between a condition group and the
same cohort's controls was decomposed as the sum over species of coefficient x (mean z-scored abundance in the
condition group - mean in controls). Species were grouped as oral-origin taxa with positive coefficients (genera or
species typical of the oral cavity, e.g. Streptococcus, Veillonella, Fusobacterium, Gemella, Peptostreptococcus,
Porphyromonas, Solobacterium, Lactobacillus salivarius, Actinomyces), commensals with negative coefficients
(depleted), and other enriched taxa. Specificity-constrained signatures removed CRC-model species whose standardised
shift had the same sign as their coefficient (|shift| > 0.2) in at least K of the other development conditions
(leave-one-condition-out), and were re-evaluated for CRC AUROC (leave-one-cohort-out) and positivity in the held-out
condition. Control augmentation added the other conditions' samples as negatives during training. This analysis was
performed after the protocol was frozen and is reported as exploratory.

## S6. Endpoints and statistics
Primary endpoint: share of site-months (months 7-12) with true FPR > alpha + 0.02. Secondary: mean |FPR - alpha|,
sensitivity, unnecessary referrals and missed cases per 1,000 screened, burn-in referral rate. Comparisons are paired
by site and model (one-sided Wilcoxon signed-rank tests; 95% confidence intervals from a cluster bootstrap over sites,
2,000 resamples). Sensitivity non-inferiority to the oracle uses a margin of 0.05.
Comorbidity analysis: CRC models trained on all development CRC cohorts; within each locked cohort, the CRC score of
each condition group is compared with that cohort's own controls by linear regression on the logit score, adjusted for
age, BMI and sex where recorded; one-sided p values are Holm-corrected within model. Positivity ratios have bootstrap
95% confidence intervals (1,000 resamples).

## S6b. Medication addendum (pre-specified before analysis; protocol_addendum_drugs.md)
After the locked analysis and the exploratory mechanism analysis, we wrote and committed a second protocol before any
medication-stratified score was computed. Prediction from the mechanism: proton-pump inhibitor (PPI) users, whose guts
carry more oral taxa, receive higher CRC-test scores. Development check (direction only): VincentC_2016, LeeKA_2022,
JieZ_2017. Confirmatory test: MetaCardis_2020_a (1,831 adults; 295 PPI users), CRC-test logit score regressed on PPI,
condition group, sex and other recorded drugs (metformin, statin, aspirin, beta-blocker); age and BMI were not
sufficiently recorded. H5: PPI coefficient > 0 (LASSO primary). H6: PPI raises the oral-taxa component of the score.
Other drugs were secondary with no direction fixed. A post hoc exploratory analysis compared metformin users and
non-users within type 2 diabetes in four cohorts (adjusted for age, BMI and sex where recorded).

## S7. Finite-sample guarantee

**Setting.** A window contains m tested people with scores s_1..s_m; m0 of them are controls and m1 = m - m0 are cases.
Person i is *verified* if they were referred (s_i at or above the cut-off in force when tested), attended, and their
result is available; verification reveals the true status. C1 is the number of verified cases.

**Assumptions.** (A1) The control scores in the window and the score X of a future control at the same site are
exchangeable (no drift within the window). (A2) Prevalence bound: m1 <= floor(pi_max m). (A3) The reference test never
labels a control as a case (missed cancers, i.e. cases labelled as controls, are allowed).

**Rule.** FP_ub(t) = #{i : s_i >= t and i is not a verified case}; m0_lo = m - max(C1, floor(pi_max m));
t* = the smallest t with (FP_ub(t) + 1) / (m0_lo + 1) <= alpha.

**Proposition S1.** Under (A1)-(A3), conditional on m0, P(X >= t*) <= alpha, whatever the past referral cut-offs,
attendance and result delays.

**Proof.** (i) Every control with s_i >= t* is not a verified case (A3), so the number of controls at or above t*,
FP(t*), satisfies FP(t*) <= FP_ub(t*). (ii) C1 <= m1 <= floor(pi_max m) by (A2), so m0_lo = m - max(C1, floor(pi_max m))
<= m - m1 = m0. Hence FP(t*) + 1 <= alpha (m0_lo + 1) <= alpha (m0 + 1), so at most k = floor(alpha (m0 + 1)) - 1 controls
score at or above t*. Let S_(1) <= ... <= S_(m0) be the ordered control scores; then t* > S_(m0 - k). (iii) By (A1), the
rank of X among the m0 + 1 control scores is uniform, so P(X > S_(m0 - k)) <= (k + 1)/(m0 + 1) <= alpha. Since
t* > S_(m0 - k), P(X >= t*) <= P(X > S_(m0 - k)) <= alpha. The argument uses only counts, so it holds for any
verification pattern, including one that depends on the scores. QED.

**Corollaries.** (a) Applied within each recorded patient group, the rule bounds the FPR in every group separately.
(b) With the drift alarm, the guarantee applies within any stationary window after the most recent restart.
(c) Missed cancers at colonoscopy make the rule conservative; a false-positive colonoscopy result (violating A3) is
rare and its effect is bounded by the number of such errors. An independent numerical check (4,000 simulated sites
with random site shifts, 70% attendance and an arbitrary prior cut-off) gave a mean FPR of at most 0.105 (package
test suite, `cutoffguard/tests`).

## S8. Software and reproducibility
Python 3.13, scikit-learn, NumPy, SciPy, pandas, statsmodels. The proposed rule is released as the open-source Python
package `cutoffguard` (functions for site audits, sequential and per-group recalibration, and a command-line tool). All code, the frozen protocol, the development log and
file hashes are available in the code repository (see Data Availability Statement).
