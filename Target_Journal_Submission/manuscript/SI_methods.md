# Supporting Information — Methods

## S1. Data
We used species-level relative-abundance profiles from curatedMetagenomicData (Bioconductor; MetaPhlAn3; release
2021-03-31; LeeKA_2022 from release 2022-04-13; MetaCardis_2020_a from release 2022-10-19), downloaded through ExperimentHub. We kept stool samples from
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
- Note: 30 cohorts are listed for the main analyses; two further cohorts with medication records (VincentC_2016,
  LeeKA_2022) were used only for the development check of the medication addendum.
- Pilot (motivating analysis, before the data lock; it computed source-cut-off specificity at all 11 CRC cohorts,
  including the three later held-out CRC sites, which were therefore not unseen at that stage): fixed LASSO and random forest models across all 11 CRC cohorts
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
3. Prior adjustment (EM; Saerens et al. 2002 [S1]).
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
Pre-specified sensitivity analyses (protocol section 8): alpha in {0.05, 0.20}; misspecified pi_max; one-month follow-up
delay; B in {50, 200}; liberal burn-in at 1 - 3 alpha. Further settings fixed in the frozen analysis code before the
locked run but not listed in the protocol text: kernel-smoothed site populations; 70% colonoscopy attendance; 5% of
cancers missed at colonoscopy; a +0.5 logit shift of all scores from month 7; all combined.

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
carry more oral taxa [S2], receive higher CRC-test scores. Development check (direction only): VincentC_2016, LeeKA_2022,
JieZ_2017. Confirmatory test: MetaCardis_2020_a (1,831 adults; 295 PPI users), CRC-test logit score regressed on PPI,
condition group, sex and other recorded drugs (metformin, statin, aspirin, beta-blocker); age and BMI were not
sufficiently recorded. H5: PPI coefficient > 0 (LASSO primary). H6: PPI raises the oral-taxa component of the score.
Other drugs were secondary with no direction fixed. A post hoc exploratory analysis compared metformin users and
non-users within type 2 diabetes in four cohorts (adjusted for age, BMI and sex where recorded).

## S7. Finite-sample guarantee

**Setting.** A window contains m tested people with scores s_1..s_m; m0 are controls and m1 = m - m0 cases. Person i is
*verified* if referred (score at or above the cut-off in force when tested), attended, and their result is available;
verification reveals the true status. C1 = number of verified cases.

**Assumptions.** (A1) The control scores in the window and the score X of a future control at the same site are
exchangeable (no drift within the window). (A2) The realised number of cases in the window satisfies m1 <= floor(pi_max m)
(a statement about the realised count; with random prevalence pi < pi_max it holds with high probability for large m).
(A3) The reference test never labels a control as a case (cases missed at colonoscopy are allowed).

**Rule.** FP_ub(t) = #{i : s_i >= t and i is not a verified case}; m0_lo = m - max(C1, floor(pi_max m));
k = floor(alpha (m0_lo + 1)) - 1; t* = the smallest t with FP_ub(t) <= k (t* = +inf, i.e. refer nobody, if k < 0).

**Proposition S1.** Under (A1)-(A3), conditional on m0, P(X >= t*) <= alpha, whatever the past referral cut-offs,
attendance and result delays. (If t* = +inf the statement is trivial.)

**Proof.** (i) Every control with s_i >= t* is not a verified case (A3), so FP(t*) := #{controls with s_i >= t*} <= FP_ub(t*) <= k.
(ii) C1 <= m1 <= floor(pi_max m) by (A2), so m0_lo <= m - m1 = m0 and k <= floor(alpha (m0 + 1)) - 1.
(iii) Let S_(1) <= ... <= S_(m0) be the ordered control scores. At most k controls score at or above t*, so t* > S_(m0 - k).
By (A1) the rank of X among the m0 + 1 control scores is uniform (ties broken at random), so
P(X >= t*) <= P(X > S_(m0 - k)) <= (k + 1)/(m0 + 1) <= alpha. Only counts are used, so the bound holds for any
verification pattern, including one that depends on the scores. QED.

**Scope.** The guarantee is marginal (on average over windows), not a bound on the FPR of every month. The
**high-confidence option** replaces k by the largest k with BinomCDF(k; m0_lo, alpha) <= delta; by the same order-statistic
argument and the Beta distribution of F0(S_(m0-k)), P(FPR(t*) > alpha) <= delta conditional on m0 (training-conditional
guarantee). Applying the rule separately within pre-defined patient groups gives the same guarantee within each group.
For the drift alarm, the restart time is chosen from the data, so the guarantee is not formally proven after a restart;
it is supported empirically (Table S2, drift settings). Related label-free threshold adaptation under prevalence shift is described in [S3]. A numerical check in the package test suite (4,000 simulated sites,
random site shifts, 70% attendance, arbitrary prior cut-off) gave a mean FPR of 0.092 for alpha = 0.10.

## S7b. Post hoc analyses (after the locked analysis; reported as exploratory)
P1: comorbidity inside three CRC cohorts (FengQ_2015, ThomasAM_2018a: leave-one-cohort-out scores; YuJ_2015: frozen-run
scores), colonoscopy-negative controls and CRC cases with vs without recorded T2D, hypertension, fatty liver or
hypercholesterolaemia; OLS on logit score and logistic regression on positivity with site fixed effects, age, BMI, sex
(Table S8). P2: MetaCardis condition effects adjusted for sex, country (Denmark, France, Germany) and recorded drugs; age
and BMI (recorded for 72%) in a complete-case sensitivity analysis; species decomposition in the locked cohort (Table S9).
P3b: evaluation without resampling at held-out cohorts with >= 100 controls (Yachida 2019 CRC and adenoma tests;
MetaCardis and Qin 2012 T2D test): controls streamed once in random order (25 per month, 200 random orders), cases
inserted at prevalence 1% or 5%, FPR measured on controls not yet seen; and MetaCardis controls streamed country by
country (T2D test, 5% prevalence, all six orders x 50, both classifiers), FPR on not-yet-seen controls of the current
country (all current-country controls when fewer than 20 remained) (Table S10). P4: downward drift (-0.5 logit from month 7) and the primary endpoint restricted to sites with >= 40 controls,
aggregated per cohort (Table S2c). D10 (development): label-free site-wise standardisation (Table S7). P5: CRC-specific audit of the fixed cut-off at all
11 CRC cohorts (exact Clopper-Pearson CIs, chi-square test against Binomial(n, 0.10), DerSimonian-Laird tau; Table S12).
P6: CRC-only deployment simulation at the 11 CRC cohorts (1% prevalence, 100 streams; Table S13). P7: per-group label-free
recalibration at MetaCardis (Table S11). P8: decomposition of each CRC cohort's control-score shift into species
contributions and Spearman correlation of cohort FPR with shift components and control covariates (Table S14). P9: net
benefit per 1,000 screened, NB = detected cancers - w x false-positive referrals for w = 1/20, 1/50, 1/100 (Table S15).

## S7c. Code changes after the freeze (disclosure)
After the locked analysis, two functions were added to src/calibrate.py: a high-confidence option (argument delta) for
the verified-positive rule and a high-confidence prevalence-bounded quantile (contam_quantile_hc). Existing functions
were not changed in behaviour (delta defaults to None, which reproduces the frozen rule), so all locked results are
unchanged; the file therefore no longer matches its frozen SHA-256 in protocol_freeze_hashes.txt (current SHA-256:
697b946ea734059f0019b94a50bf7c79268dd51cd125ae7b1e851793d9a4fd59). The frozen version is
recoverable from the freeze commit. High-confidence results are post hoc.

## S8. Software and reproducibility
Python 3.13, scikit-learn 1.9.1, NumPy, SciPy, pandas, statsmodels. The proposed rule is released as the open-source Python
package `cutoffguard` (functions for site audits, sequential and per-group recalibration, and a command-line tool). All code, the frozen protocol, the development log and
file hashes are available in the code repository (see Data Availability Statement).


## Supporting Information references
S1. Saerens M, Latinne P, Decaestecker C. Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure. Neural Comput. 2002;14:21–41. https://doi.org/10.1162/089976602753284446
S2. Jackson MA, Goodrich JK, Maxan ME, et al. Proton pump inhibitors alter the composition of the gut microbiota. Gut. 2016;65:749–756. https://doi.org/10.1136/gutjnl-2015-310861
S3. Godau P, et al. Deployment of image analysis algorithms under prevalence shifts. MICCAI 2023, LNCS. https://doi.org/10.1007/978-3-031-43898-1_38
Original cohort publications are given by their PMID in the curatedMetagenomicData sample metadata (column PMID).
