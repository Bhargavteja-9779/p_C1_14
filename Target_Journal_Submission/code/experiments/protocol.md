# Pre-registered analysis protocol (frozen before any locked-cohort analysis)

Status: DRAFT written 2026-11-23 after development rounds 1-8 (experiments/novelty_escalation_log.md).
Becomes FROZEN at the commit that adds the line "FROZEN: yes" below; the final runner refuses to run otherwise.
FROZEN: no

## 1. Question
When a gut-microbiome disease classifier is deployed at a new site, does its decision threshold keep the intended
false-positive rate (FPR), and can it be re-set at the site without a labelled validation study?

## 2. Data (curatedMetagenomicData, MetaPhlAn3 species relative abundance; stool; one sample per subject)
- CRC external test: train on the 8 DEV cohorts (data_lock.md); test sites YachidaS_2019, YuJ_2015, ThomasAM_2019_c.
- Other diseases, leave-one-cohort-out (LOCO) over all cohorts of the disease:
  IBD (HMP_2019_ibdmdb, HallAB_2017, IjazUZ_2017, NielsenHB_2014); T2D vs control (KarlssonFH_2013, MetaCardis_2020_a,
  QinJ_2012, SankaranarayananK_2015; IGT/CAD/HF excluded); adenoma vs control (FengQ_2015, HanniganGD_2017,
  ThomasAM_2018a, YachidaS_2019, ZellerG_2014; CRC samples excluded).
- Known limitation stated in advance: the adenoma analysis shares CONTROL samples of 4 cohorts with CRC development;
  it is therefore not fully untouched (labelled "partly independent").

## 3. Models (fixed, not tuned on test data)
Preprocessing fit on training cohorts only: species with prevalence > 5%, log10(x/100 + 1e-5), z-score.
LASSO logistic regression (C = 0.1, balanced) and random forest (500 trees, min leaf 2, balanced subsample).
Scores on the logit scale. Source out-of-fold scores by LOCO inside the training cohorts (>= 3 cohorts) else 5-fold.

## 4. Threshold methods (src/calibrate.py at the freezing commit)
1. source: (1 - alpha) quantile of source out-of-fold control scores (status quo).
2. local_q: (1 - alpha) quantile of the site's unlabeled cumulative pool.
3. em: Saerens EM prior adjustment (one-shot analysis only).
4. contam: label-free prevalence-bounded conformal quantile, contam_quantile(pool, alpha, pi_max).
5. conf20: conformal threshold from 20 labelled local controls (one-shot analysis only).
6. **vp (proposed)**: SequentialRecalibrator (src/calibrate.py) = verified_positive_seq with burn-in month at the source
   (1 - 2*alpha) control quantile, then the current threshold; only outcomes of referred and attending samples are
   used; drift alarm restarts the pool when the newest month's verified false positives exceed Binomial(m0, alpha)
   (one-sided p < 0.01); pi_max as below.
7. oracle: (1 - alpha) quantile of the site's true control scores (reference, not deployable).

## 5. Primary simulation (sequential deployment)
Each test cohort = the site's population. 12 monthly batches of B = 100 tests drawn with replacement at prevalence pi;
thresholds updated monthly on the cumulative pool; R = 200 streams per site x model x pi; seed 2026.
alpha = 0.10. pi in {0.01, 0.05, 0.10} (CRC, IBD, T2D) and {0.10, 0.30} (adenoma). pi_max = max(0.05, pi).
True FPR(t) = share of the site's control scores >= t; true sensitivity likewise on its cases.

## 6. Endpoints
- PRIMARY: share of site-months (months 7-12) with true FPR > alpha + 0.02 (= 0.12).
- Secondary: mean |FPR - alpha| (months 7-12); sensitivity; unnecessary referrals and missed cases per 1,000 screened
  (12-month average); burn-in referral rate; one-shot (round-4 style split) results for all 7 methods.

## 7. Hypotheses and statistics
- H1: vp2 has a lower primary endpoint than source and than local_q. Unit = site x model (CRC: 3 sites x 2 models;
  LOCO diseases: all sites x 2 models). Paired one-sided Wilcoxon signed-rank per disease and pooled; 95% CIs of the
  paired difference by cluster bootstrap over sites (2,000 resamples).
- H2 (non-inferiority): mean sensitivity of vp2 (months 7-12) >= oracle sensitivity - 0.05 (cluster-bootstrap lower bound).
- All numbers reported, including failures; no method or setting is dropped after seeing test results.

## 8. Pre-specified sensitivity analyses
(a) alpha in {0.05, 0.20}; (b) pi_max misspecified (pi = 0.10, pi_max = 0.05); (c) one-month follow-up delay
(labels of month k referrals available only after month k+1); (d) batch size B in {50, 200}; (e) burn-in at
(1 - 3*alpha) quantile (vp).

## 8b. Part B - comorbidity confirmation (locked cohorts, data_lock.md addendum)
CRC models (LASSO, RF) trained on all 8 DEV CRC cohorts; threshold = source 90%-specificity (out-of-fold).
Scored: MetaCardis_2020_a (CAD, HF, T2D, IGT, controls), QinJ_2012 and KarlssonFH_2013 (T2D, controls; Karlsson IGT),
IBD cohorts (IBD, controls). One sample per subject, adults.
- H3 (primary for Part B): within each cohort, CRC-test score of each condition group exceeds that cohort's controls
  after adjustment for age, BMI and sex where available (OLS on logit score; condition coefficient > 0, one-sided,
  Holm-corrected across the condition x cohort tests, LASSO model primary, RF secondary).
- Reported: positivity rate per group, ratio to own controls (95% CI by bootstrap), crude and adjusted coefficients.

## 8c. Part C - group-conditional recalibration (locked: MetaCardis_2020_a)
Site = MetaCardis; screened population = its controls + condition groups with shares CAD .10, T2D .15, HF .03, IGT .15
(remaining controls), CRC cases 1% drawn from DEV out-of-fold CRC case scores (sensitivity proxy).
B = 200/month, 18 months, R = 200. Methods: source, pooled SequentialRecalibrator, group-conditional
SequentialRecalibrator (one per group; group known from records).
- H4: P(group FPR > 0.12, months 7-18) is lower for group-conditional than pooled in the worst-off group
  (descriptive with bootstrap CI over streams; also mean FPR per group, overall FPR, sensitivity proxy per group).

## 9. Not allowed after freezing
Changing models, hyper-parameters, methods, burn-in rule, endpoints or cohorts. Any extra analysis is labelled
post hoc.
