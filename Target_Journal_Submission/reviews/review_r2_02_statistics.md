# Review R2-02: Statistical review (round 2)

Manuscript: "The decision threshold of a stool-metagenome classifier must be set at each site, on that site's own
samples" (iMeta Letter, draft v0.3). Files reviewed: manuscript/manuscript.md, manuscript/supporting_information.md,
code/experiments/protocol.md, code/experiments/final/{run_final.py, RUN_NOTES.md}, code/src/calibrate.py,
code/experiments/posthoc/explore_r1.py, code/analysis/{analyze_final.py, posthoc_r1.py, make_figures.py},
results/{main_tables.md, posthoc_r1_tables.md}. I recomputed the key numbers from final_{lasso,rf}.csv.gz
(512,000 rows) and E{1,2,3,5}_{lasso,rf}.csv.gz. My scripts are in the reviewer scratchpad, not in the repository.

## Summary

The revision deals with most round-1 points. Note S1 is now correct in substance. Post-hoc work is in a separate
paragraph and a separate section. Inference is at the cohort-task level, and the sensitivity analysis without adenoma
has been added. Every main-text number I checked matches the tables and the raw data (list at the end). The protocol
commit (73f827d, 21:51 UTC) and the analysis script (cc66a43/7fe8ca7, 22:02 UTC) both come before the locked launch
(22:52 UTC). The RF resume is documented and was verified.

Four problems remain, and they are about interpretation and labelling, not arithmetic:

1. Under the locked design, the rank rule's cohort-RMSE is almost entirely determined by the closed-form value
   r/(n+1). The formula alone gives 0.030, against an observed 0.031. Most of it, 0.025, comes from one cohort where
   the rule abstains. The P-values and the TOST "equivalence" built on this result look like empirical evidence but are
   in fact a check that a theorem holds.
2. The main text presents post-hoc inference (clustered CIs, cohort-level Wilcoxon/Holm, TOST, the no-adenoma
   analysis) inside the "locked" paragraph without a label. It also leaves out the pre-registered result that contradicts
   the equivalence claim (ctrl10 closer to target, Holm P = 0.048).
3. Figure 2C and the E2 sentence mix two things. The cohorts in the comparison change with pool size, and the
   evaluation sets shrink as the pool grows. At n = 200 in YachidaS_2019, evaluation noise alone would give about 7%
   of draws above 15%.
4. E5 rests on three centres, and the whole effect comes from one of them (Copenhagen). The cross-centre pool is no
   better than the training cut-off (RMSE 0.067 vs 0.072; 33% vs 0% of deployments above 15%). Yet the Highlights,
   the Conclusion and the section title state the E5 result as a general rule, without a post-hoc label.

**Recommendation: MAJOR REVISION.** No new data are needed. The work is re-analysis of existing outputs (E2
stratification, E3 within-pair reference, E5 uncertainty) and rewording.

---

## MAJOR issues

### M1. The locked rank-rule result is fixed by the formula; present it as a check, not as inferential evidence
**Location:** manuscript.md lines 82-87 ("At the locked cohorts, pools were random halves ... equivalence P = 0.0002");
Table S3 E4b; TOST in posthoc_r1.py.

Pools and evaluation sets are random halves of the same cohort, so by exchangeability E[FPR] = r/(n_c + 1) exactly.
Recomputed per unit (alpha 0.10, pi 0):

- Theory alone gives cohort-RMSE **0.030**; observed **0.031**. Observed minus theory is within ±0.009 in 31 of 32
  units (max 0.015, ZellerG_2014 RF, which is Monte-Carlo noise with R = 200).
- The two HallAB_2017 units (6 pool controls, abstain, error 0.10 each) contribute sqrt(2 × 0.01/32) = 0.025 of the
  0.031. Without HallAB the RMSE is 0.018 (ctrl10 0.010; training cut-off 0.185).
- So the "difference vs local quantile" (-0.017) is the gap between floor((n0+1)alpha)/(n+1) and the interpolated
  quantile. The ctrl10 "equivalence" compares two conformal order statistics that both have known expectations. Both
  follow from the formulas.

The authors now say that exchangeability "held by design" (line 81), which is right. But the Wilcoxon/Holm P-values,
the bootstrap CIs and the TOST P = 0.0002 still read as empirical evidence that the rule works. They test only that
sampling noise is small.

**Fix:**
(a) Add one sentence and a supplementary column giving the theoretical E[FPR] = r/(n+1) for each cohort next to the
observed mean. State that the locked test confirms the formula to within ±0.015 per unit.
(b) Keep the paired tests only for the comparators whose behaviour is not fixed by design (training cut-off, the
label-free methods). For rank rule vs ctrl10 and vs local_q, report the theoretical difference, or label the test as a
Monte-Carlo check.
(c) Report the RMSE with and without the abstaining cohort, or report abstention separately from the FPR error. One
cohort of six controls should not decide the headline number.

### M2. Locked and post-hoc inference are mixed in the main text, and a pre-registered result is left out
**Location:** manuscript.md lines 83-89; SI "Deviations" item 2; response_r1.md (M4 row: "The unit-level P = 0.048
is no longer cited").

- The clustered CI (-0.182 to -0.056), the cohort-level Wilcoxon with Holm (P = 0.0004), the TOST (margin ±0.02,
  P = 0.0002) and the "without the adenoma task" analysis all come from posthoc_r1.py (Table S3, headed "post hoc").
  The main text gives them in the locked paragraph with no label.
- The TOST and its ±0.02 margin are not in protocol.md. The margin was chosen after the results were seen, and it is
  two-thirds of the rank rule's own RMSE (0.031). That is a lenient margin.
- The pre-registered analysis script (analyze_final.py) was committed before the locked run. Its result is ctrl10 closer
  to target than rpoolmean: difference +0.0055, CI 0.001 to 0.010, Holm P = 0.048 (Table S2). Deviation 2 can justify
  re-analysing at the cohort level, because the protocol text says "cohort-level bootstrap". It does not justify
  leaving the pre-registered result out of the main text while claiming equivalence. At the task level, 4 of 16 tasks
  have a difference above 0.019, close to the margin.

**Fix:** Label the inferential statistics in lines 83-89 as "post-hoc re-analysis (Table S3)". Add one clause: "the
pre-registered unit-level analysis found ten labelled controls slightly closer to target (difference 0.006, Holm
P = 0.048)". Either justify the ±0.02 margin independently of the data (for example clinically: 2 colonoscopies per
100 screened) or drop the word "equivalent". Given M1, "both were within 0.01 of their theoretical expectation" is
more accurate.

### M3. E2 / Figure 2C: the pool-size curve mixes changing cohort composition with shrinking evaluation sets
**Location:** manuscript.md lines 96-98; Figure 2C legend (line 147-148); SI E2 description; posthoc_r1.py E2 block;
make_figures.py Figure 2C block; explore_r1.py E2 branch.

- **Composition.** The available pool sizes differ by cohort. YachidaS_2019 goes up to 200, QinJ_2012 up to 100, and
  MetaCardis up to 500 (rule n <= n_controls - 50). Figure 2C and Table S4 average over whichever cohorts exist at
  each n, so n = 200 has no QinJ and n >= 300 is MetaCardis alone. The training cut-off's P(FPR > 15%) "falls" from
  0.50 to 0 with n. That is the clearest sign that the curve tracks composition, not pool size.
- **Merged tasks.** posthoc_r1.py and make_figures.py group by `cohort` without `disease`. As a result, YachidaS_2019
  CRC and YachidaS_2019 adenoma (different models, different cases) are pooled into one "cohort". At n = 200 the two
  give 4.8% and 7.8% for the rank rule, against the reported aggregate of about 4%.
- **Evaluation noise.** The evaluation set is "all remaining controls", so it shrinks as the pool grows: 51 controls
  in Yachida at n = 200, about 75 in QinJ at n = 100. With a true FPR of 0.087, Binomial(51) noise alone gives
  P(FPR_hat > 0.15) = 0.072, and Binomial(75) gives 0.028. At these sizes the reported 4-8% for the rank rule is mostly
  evaluation noise, and the noise grows with n. That works against large pools, which is the opposite of the
  conclusion drawn. The SI mentions the noise but the main text does not, and the text then compares the methods'
  exceedance rates as if they were deployment risks.

**Fix:** (i) Group by (disease, cohort). (ii) Plot each task separately, or restrict to the n range common to all
tasks (25-100), and show MetaCardis alone for 200-500. (iii) Use a fixed held-out evaluation set (for example 50
controls set aside before drawing pools of every size), or report the "population" FPR, estimated as the tail mass of
the threshold in all non-pool controls, together with its binomial noise floor. (iv) Rewrite lines 96-98 to give
per-cohort ranges and state the noise floor.

### M4. Per-deployment exceedance in the locked run is dominated by evaluation granularity in small cohorts
**Location:** manuscript.md lines 87-88 ("FPR exceeded 15% in 14% ... 20% ... 33% ... 39%"); Figure 2A.

12 of 16 cohorts have 6-30 evaluation controls. With 6-13 controls, one or two false positives already exceed 15%.
The per-deployment metric therefore mixes pool sampling with evaluation granularity, and the evaluation granularity
does not reflect a laboratory's long-run FPR. In the four tasks with at least 80 pool controls (QinJ, Yachida ×2,
MetaCardis), exceedance is 6.5% for the rank rule, 21% for ctrl10, 13% for local_q and 55% for the training cut-off.
The ranking changes: local_q beats ctrl10 there.

**Fix:** Report the exceedance shares separately for large cohorts, or replace the empirical evaluation FPR with the
tail mass in the full held-out control set. Add the caveat to the Figure 2A legend.

### M5. E5 (three centres, one study) cannot carry the weight put on it in the Highlights, Conclusion and section title
**Location:** Highlights bullet 3 (line 17-18); graphical abstract; section title "THE SAMPLES MUST COME FROM THE SAME
SITE" (lines 102-109); Conclusion lines 123-124 ("or even from another centre of the same study, does not"); Table S4 E5.

- There are 3 centres, giving 6 ordered cross-centre pairs × 2 models = 12 non-independent units, with no CI. The
  failure comes entirely from Copenhagen. A Copenhagen pool applied elsewhere is too high (0.16-0.24), and a pool from
  elsewhere applied in Copenhagen is too low (0.02-0.05). Between Leipzig and Paris the rank rule's RMSE is **0.034**
  (training cut-off 0.059). This is one centre that differs, not a general centre effect.
- The comparator is left out. In E5 the cross-centre pool (RMSE 0.067) is no better than the training cut-off
  (0.072). Across deployments, 33% of cross-centre rank-rule deployments exceed 15% FPR, against **0%** for the training
  cut-off, whose FPR in MetaCardis is 0.005-0.088. The text gives the same comparison for E3 but not for E5.
- The centres are also the countries (DK, DE, FR), and control recruitment differed by centre. E5 cannot separate
  centre from country, so "not to the study or the country" (line 108-109) is not supported for "country". The claim
  of "one protocol and sequencer" needs a citation to the MetaCardis methods.
- "Within 0.01 of the target" (line 104): the largest same-centre deviation is 0.0125 (Copenhagen RF 0.097, Paris
  LASSO 0.087). Say "within 0.013", or use the RMSE alone.

**Fix:** Label E5 as post hoc in the Highlights, the graphical abstract text and the Conclusion, or remove it from
them. Report the training-cut-off comparison and the Leipzig-Paris result. Give a cluster bootstrap over centres, or
state that with three centres no uncertainty can be estimated. Replace "not to the study or the country" with "a pool
from another centre of the same study failed in one of three centres".

### M6. E3: no within-pair reference, dependent pair units, and the abstention/conservatism behind the summary
**Location:** manuscript.md lines 106-107; Table S4 E3; explore_r1.py E3 branch.

- For IBD and T2D (4 cohorts each) the E3 model is trained on only 2 cohorts, and for adenoma on 3. Each unordered
  pair has its own model, which differs from the locked model, and the same-site comparison (locked RMSE 0.031) uses a
  different model and pool. The cross-cohort penalty is therefore not isolated. Within E3, the same model and the same
  pool size are available for B's own half, which gives a clean contrast.
- The 100 pair×model units are summarised as if independent, although each cohort appears in up to 8 ordered pairs.
  "A third of cohort pairs exceeded 15%" and "no better than the training cut-off (0.173)" have no uncertainty. Paired
  per unit, the rank rule beats the training cut-off in 48% of units (mean |error| difference -0.015).
- E3 errors go in both directions: 45% of rank-rule units have FPR < 0.05, and 6% abstain. The strict rule's "best"
  RMSE (0.111) comes from 50% abstention and a median FPR of 0. If Figure 2B or any text uses it, say so.

**Fix:** Add a same-model within-cohort reference (pool and evaluation from B's own halves) to E3, and report the
difference cross minus within per pair with a bootstrap clustered by cohort. Say that E3 models are trained on 2-3
cohorts.

### M7. Highlights and Figure 1C overclaims about the label-free methods
**Location:** Highlights bullet 2 (line 15); manuscript.md lines 58-62; SI threshold-rule list.

- "Five **published** label-free adaptation methods": the location-scale mixture fit is described in the SI as
  "(ours, development)". Only four are published, and the one that "did better than doing nothing" is the authors' own.
- "Four made it worse": this holds only when the classifiers are pooled. Per classifier, feature standardisation
  **improved** on the training cut-off for random forest (cohort-RMSE 0.125 vs 0.199) and was worse for LASSO
  (0.258 vs 0.170). The pooled difference (0.203 vs 0.185) is small and untested. No method-vs-source comparison is
  tested at all (all tests are rank rule vs X).
- These are the authors' re-implementations: KDE-based EM, MLLS-BCTS via Nelder-Mead, and their own two-Gaussian
  initialisation. Say so; failures can partly reflect implementation choices.

**Fix:** Write "Four published label-free methods and one mixture fit of our own ...". Replace "four made it worse"
with the per-classifier statement. Add paired tests of each method against the training cut-off, or describe the
comparison as descriptive.

---

## MINOR issues

1. **Note S1, distributional claim (SI lines 54-63).** The proof's logic is correct. Removing cases lowers order
   statistics, the Beta is stochastically ordered in n - K, and both the bound E[FPR] <= alpha + P(K > m) and the
   numeric P(K > 18) = 7e-14 at n = 360, prevalence 0.5% are right. Monte-Carlo check with K = floor(0.05n) cases
   placed below all controls, n = 40: E[FPR] = 0.0770 = 3/39 = r/(n0+1). However, "the control mass above the r-th
   largest ... is Beta(r, n - K - r + 1)" requires the pool controls and future controls to be i.i.d. from a
   continuous F0 given K. Finite exchangeability alone gives only the marginal statement P(future control >= t) <=
   r/(n0+1), which is enough for the expected-FPR version but not for the high-probability version. State
   "conditionally i.i.d." for the strict version. Code matches the Note: `robust_pool_mean` uses r = floor((n0+1)alpha)
   and `robust_pool_rank` uses `beta.sf(alpha, k, n0-k+1) <= delta`, and is monotone, so the `break` is valid.
2. **Random K in practice (Note S1; lines 77-78, 95).** "If at most 5% of the pool are patients" is a fixed cap. With
   K ~ Binomial(n, 0.05), the cap is exceeded in 41% of E1 pools, so at the design share the bound alpha + P(K > m) is
   close to vacuous. E1 shows the failure mode the Note predicts. In SankaranarayananK_2015 (9 pool controls, AUROC
   0.58) the mean FPR rises from 0.099 to 0.124 (LASSO) and 0.129 (RF) at pi = 0.2, above target. That is why the E1
   max cohort FPR rises from 0.111 to 0.129. The "RMSE 0.030-0.052" (line 95) hides two things: target exceedance in
   weak-classifier, small-pool cohorts, and growing conservatism elsewhere (sensitivity 0.249 to 0.176). Mention both.
3. **E1 design differs from the locked design.** E1 keeps the pool size fixed, so cases replace controls, whereas the
   locked run added cases. ctrl10 in E1 is skipped (NaN) rather than abstaining in HallAB_2017, so the E1 ctrl10 RMSE
   (0.011) is not comparable to the rank rule (0.030) or to the locked ctrl10 (0.027). Note this under Table S4.
4. **Ties (line 98; SI line 69).** In E1, `>=` and `>` gave identical FPRs in every one of the 374,400 rows (difference
   exactly 0). So "changed no result at the third decimal" is true but checked only on E1, not on the locked run,
   whose scores were not saved. "By at most less than 0.001" (SI line 69) is awkward; write "did not change any FPR in
   E1". Save the scores in future runs.
5. **"Holm-adjusted P = 0.0004 over 16 cohort-task pairs" (line 84).** The Holm family is 9 comparisons, and n = 16 is
   the Wilcoxon sample size. Write "Wilcoxon signed-rank over 16 cohort-task pairs, Holm-adjusted for 9 comparisons".
   The P values shown as "0" in Table S2/S3 should be "<0.0001". The exact minimum two-sided P for n = 16 is 3.1e-5.
6. **"Results held ... without the adenoma task" (lines 88-89).** Without adenoma, rpoolmean vs local_q has Holm
   P = 0.084 and vs MLLS P = 0.056 (Table S3). The direction holds; significance does not. Say "the direction of every
   comparison held". Per-classifier Wilcoxon P values (my recomputation, not in the SI) also support "both
   classifiers"; add a per-model column to Table S3.
7. **Clustered bootstrap with 16 (11) clusters.** Percentile cluster bootstraps under-cover with few clusters. A t
   interval on the 16 cohort-task mean differences, which the TOST already uses, is simpler and consistent. Report that
   instead, or use BCa. Also, the CI is for the mean absolute error difference while the headline is the RMSE. Give a
   cluster CI for the RMSE itself (also round-1 minor 12, still open).
8. **"Overdispersion" test (lines 48-49; analyze_final.py lines 53-59).** The statistic tests H0 that every cohort has
   FPR = 0.10 (df = 16). It is a calibration test, not a test of overdispersion around a common mean. The binomial n is
   the pool size, but the 200-split mean approximates the FPR in the full cohort (about 2n controls), so the variance
   is overstated about twofold and the test is conservative. YachidaS_2019 controls enter twice. Call it "a test that
   every cohort meets the 10% target", and report P < 10^-30 rather than 2 × 10^-52, a precision the binomial model
   cannot support.
9. **"AUROC did not predict which cohorts failed" (Highlights; line 52-53).** Quantify it: Spearman rho between AUROC
   and |FPR - 0.10| across the 32 units is -0.18 (P = 0.34, units not independent). One sentence with this number is
   stronger than "cannot reveal".
10. **Sample-size rule contradicts line 116.** With the absolute slack 0.02, `needed_pool_size` gives n = 160 at
    alpha = 0.05 (pi_max 1%) against 360 at alpha = 0.10. The rule says a 5% target needs **smaller** pools, the
    opposite of "need correspondingly larger pools". Use a relative slack (for example expected FPR >= 0.8 alpha), or
    give the alpha = 0.05 numbers. Also say that "needs about 360" (line 114) is a sensitivity-efficiency criterion,
    because the guarantee holds at any n with r >= 1. SI line 76 points the sample-size rule to Figure 2C, but
    Figure 2C shows E2 and not this rule; fix the cross-reference.
11. **Consequences per 1,000 (lines 111-114).** The numbers are correct (199 and 87 healthy per 1,000; recomputed
    1000 × 0.995 × FPR). They average 3 cohorts × 2 models with no range, and sensitivities are compared at different
    realised FPRs. Round-1 minors 5 and 6 are still open: give per-unit ranges, and give sensitivity at matched FPR or
    relative to an oracle cut-off.
12. **E3 / E5 / Figure 2B grouping.** make_figures.py groups E3 by (model, pool_from, cohort) without disease. No
    duplicate pair arises in the current data, but add `disease` for safety, matching posthoc_r1.py.
13. **ctrl10 vs rank rule are not given the same information.** ctrl10 uses 10 labelled controls, while the rank rule
    uses the whole pool (6-321). The fair labelled comparator at equal n is the conformal quantile of the labelled
    pool. One sentence would stop "equivalent to ten labelled controls" from being read as "labels are worthless".

---

## Number check (main text vs tables vs raw data)

| Claim (manuscript.md line) | Recomputed | Status |
|---|---|---|
| Training cut-off FPR 0.00-0.74, median 0.10 (47) | 0.000-0.735, median 0.104 | OK |
| Overdispersion P 2e-52 / 5e-88 (48) | 1.82e-52 / 4.93e-88 | OK (see minor 8) |
| T2D/adenoma AUROC 0.54-0.69 (50) | 0.535-0.692 | OK |
| 10 pairs AUROC >= 0.70: FPR 0.02-0.39 (51) | 10 pairs, 0.025-0.391 | OK |
| External CRC AUROC 0.70-0.86, FPR 0.11-0.30 (52) | AUROC 0.696-0.859, FPR 0.114-0.303 | OK (0.696 rounds to 0.70) |
| Label-free RMSE 0.41/0.34/0.32/0.20/0.15 vs 0.19 (pi 0) (58-60) | 0.410/0.339/0.323/0.203/0.153 vs 0.185 | OK |
| Mixture fit 0.10 at pi 0.2 (61) | 0.100 | OK |
| 6-30 controls in 12 of 16 (82) | 12 of 16 | OK |
| RMSE 0.031 vs 0.185; diff -0.108, CI -0.182 to -0.056, Holm P 0.0004 (83-84) | Table S3 E4b; Wilcoxon exact P 6.1e-5, Holm rank 4 of 9 (×6) = 0.0004 (my recomputation) | OK (label: post hoc) |
| vs local_q -0.017 (-0.028 to -0.008) (85) | -0.0173 (-0.0282 to -0.0081) | OK |
| vs ctrl10 0.006, 90% CI -0.000 to 0.011, P 0.0002 (86-87) | 0.0055 (-0.0002 to 0.0112), 0.0002 | OK (see M2) |
| Exceedance 14/20/33/39% (87-88) | 14.3/19.9/32.7/39.2% | OK (see M4) |
| Strict abstains in half (90-91) | 0.50 | OK |
| E1 RMSE 0.030-0.052 (95) | 0.030-0.052 | OK (see minor 2) |
| E2 n 100-200, 5% cases: 4% / 7-10% / 19% / <1% (96-98) | 3.6-3.9% / 6.6-10.2% / 19.2-19.3% / 0.2-0.6% | OK (see M3) |
| E5 same-centre RMSE 0.009; other centre 0.067; max 0.24 (104-106) | 0.009; 0.067; 0.236 | OK; "within 0.01" should be 0.013 |
| E3 RMSE 0.158, 1/3 > 15%, source 0.173 (106-107) | 0.158, 0.33, 0.173 | OK (see M6) |
| CRC 199 vs 87 per 1,000; sens 0.48 vs 0.65 (111-113) | 199.0 vs 87.2; 0.480 vs 0.647 | OK |
| Strict n = 360 / 610 / 1,500 (114-115) | 360 / 610 / 1500 | OK (see minor 10) |
| Rank rule abstains 31% at alpha 0.05 (117) | 0.312 | OK |
| P(K > 18), n = 360, prev 0.5% < 1e-9 (SI) | 7.1e-14 | OK |
