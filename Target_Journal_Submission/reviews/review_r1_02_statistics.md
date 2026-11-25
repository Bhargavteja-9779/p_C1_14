# Review R1-02: Statistical review

**Manuscript:** "Stool-metagenome classifiers miss their intended false-positive rate in new laboratories, and a label-free rank rule fixes it" (iMeta Letter, draft v0.2)
**Reviewer role:** statistics / methods
**Material checked:** manuscript.md, supporting_information.md, protocol.md, run_final.py, RUN_NOTES.md, calibrate.py, models.py, analyze_final.py, main_tables.md, data_lock.md, novelty_escalation_log.md, git history, and the raw locked outputs final_lasso.csv.gz / final_rf.csv.gz (512,000 rows). I re-ran checks independently in scratch scripts. I did not modify any repository file except this review.

## Summary

The Letter makes three claims. (1) A cut-off fixed on training cohorts gives very different realised FPRs at new cohorts, and AUROC does not show this. (2) Published label-free adaptation methods fail at screening prevalence. (3) An order-statistic ("rank") threshold on the laboratory's own unlabelled pool keeps the intended FPR, with a finite-sample guarantee that holds when some of the pool are cases.

Reproducibility and bookkeeping are good. The manuscript numbers match `results/main_tables.md`, and I could reproduce every table value from the raw CSVs. The per-model RMSEs quoted in the text are not in the tables, but they also reproduce: LASSO 0.031 vs 0.170 and RF 0.031 vs 0.199. The sample-size numbers (360/610/1,500) reproduce from `needed_pool_size`. The expected-FPR version of the rule really does keep the mean FPR at or below alpha in every locked unit. The largest unit mean is 0.112 (ZellerG_2014 adenoma, RF), which is within Monte Carlo error (z = 2.0 of 32 units).

However, the evaluation cannot test the claims that make the contribution new, and some statistical statements are wrong or overreach:

- The within-cohort random-split design makes the pool exchangeable with the evaluation set. Under that design the guarantee holds by construction.
- The "1% case share" pools contain **zero** cases in 13 of 16 cohort-task pairs, so the robustness to cases in the pool was barely tested.
- The authors' own development stress test shows the rank rule failing when the pool is not exchangeable (FPR 0.65). This result is not reported.
- The handling of ties in Note S1 goes in the wrong direction.
- Inference treats 32 dependent units as independent, and the bootstrap is not the pre-registered cohort-level bootstrap.
- Several pre-registered secondary results that are unfavourable are left out of the main text.

**Recommendation: MAJOR REVISION.**

---

## MAJOR issues

### M1. Under the evaluation design the headline result holds by construction, and the one non-exchangeable test (which the rule fails) is not reported
**Location:** Main text lines 65-81 and 95-97; SI "Evaluation design" (lines 60-67); protocol.md line 35; novelty_escalation_log.md Round 4(B).

Pool and evaluation set are random halves of the same cohort (run_final.py lines 26-29). Note S1 proves E[FPR] <= alpha under exactly this exchangeability, so the locked test cannot fail apart from abstention and Monte Carlo noise. The "keeps the promise" result (cohort-RMSE 0.031) therefore checks the arithmetic. It is not evidence that the rule works in a laboratory. The real risk in deployment is that the first n samples differ from later ones (batch, kit, season, change in referral population). The protocol names the cross-study stress test (dev round 4B) as "the evidence about non-exchangeable pools". In that test the rank rule gave realised FPRs of **0.13, 0.65, 0.23 and 0.10** at target 0.10 (Hannigan to Vogtmann: 0.65). For comparison, the training cut-off gave 0.21, 0.19, 0.25 and 0.63.

The manuscript (lines 42-45) quotes only the local-quantile results from this test (0.33, 0.87). It describes them as "a cut-off set on the controls of one study", without saying that the rank rule failed in the same test. In two of the four pairs the training cut-off did better than any pool-based rule.

**Fix:**
- (a) Report the full round-4(B) table (all rules, both models if available) in the main text or Figure 1C, and say plainly that the guarantee does not hold when the pool comes from another study or pipeline.
- (b) Add an evaluation in which the pool and evaluation samples are not exchangeable by design. For example, split by recorded centre or sequencing batch within MetaCardis_2020_a or YachidaS_2019, or by collection date where metadata allow. Label it post hoc.
- (c) Rewrite the title and lines 25-27, 92-93 accordingly. "Fixes it" and "restores the intended false-positive rate with a guarantee" should become "restores it when the calibration pool comes from the same process as later samples".

### M2. The "1% case share" primary setting is effectively case-free, so contamination robustness is untested and the gain over the naive pool quantile comes from a small-sample correction
**Location:** run_final.py line 29; main text lines 56, 74, 71-72 ("Patients in the pool can only make the rule more cautious"); SI line 62; main_tables.md (pi = 0 and pi = 0.01 tables are nearly identical).

`n1 = min(len(c1), round(pi * len(c0) / (1 - pi)))` rounds to 0 whenever the pool has fewer than about 50 controls. Realised case counts in the pool at pi = 0.01, recomputed from n_pool:

| cohort-task pairs | cases in pool at "1%" |
|---|---|
| 13 of 16 (ThomasAM_2019_c, YuJ_2015, all IBD, KarlssonFH, SankaranarayananK, adenoma FengQ/Hannigan/ThomasAM_2018a/Zeller) | **0** |
| YachidaS_2019 (CRC and adenoma), QinJ_2012 | 1 |
| MetaCardis_2020_a | 3 |

Even at the nominal 5%, HallAB_2017 and SankaranarayananK_2015 have no cases. The primary endpoint therefore mostly tests a case-free pool. The contamination-robust part of the rule (n0 = n - floor(pi_max n)), which is presented as the new contribution, is barely tested.

The 4 cohort-task pairs with pools of at least 50 (8 units) show this. There the naive pool quantile `local_q` does as well as `rpoolmean` (cohort-RMSE 0.006 vs 0.008). The overall advantage of rpoolmean over local_q (-0.017) comes from small pools (6-30 samples). In those pools `np.quantile` with linear interpolation is biased upward (local_q mean FPR 0.137 with no cases at all). That is a finite-sample order-statistic effect, not robustness to contamination.

**Fix:**
- Report the realised number of cases in each pool (a column in Table S1/S2).
- Add a post-hoc analysis in which cases are actually present. Options: draw the case count as Binomial(n, pi) with probability-proportional rounding, or fix the case count at ceil(pi n). Also sweep pi above and below pi_max = 0.05.
- In the text, separate the two ingredients (the finite-sample order statistic and the contamination margin) and say which one drives the gain.

### M3. Note S1: the tie argument goes in the wrong direction, the case-count assumption is not stated precisely, and the proof is loose
**Location:** SI lines 47-58 (Note S1); calibrate.py lines 172-182; main text lines 68-72.

**(a) Ties.** Note S1 says ties "make the rule more conservative because positives are called at score >= t". The reverse is true. The order-statistic result P(X >= X_(r)) has mean r/(n0+1) only for continuous scores. If there is a block of tied scores at t, calling positives at `>= t` counts every future control at that tied value as positive, so the realised FPR can be far above r/(n0+1). For example, if more than 90% of controls share the LASSO floor score and r falls in that block, FPR is close to 1. Calling positives only at a strict `> t` is conservative under ties. In this data the ties sit at the low end, so the locked results are probably not affected (the largest LASSO unit mean is 0.101). But the statement in the proof is wrong.
*Fix:* call positives at strict `> t`, or break ties at random (add a tiny uniform jitter, the standard conformal device), and correct the text.

**(b) Case count.** The guarantee needs the number of cases K <= m = floor(pi_max n) with certainty, and K must not depend on the control scores. In screening, K is random, roughly Binomial(n, prevalence). The guarantee should then read P(FPR > alpha) <= delta + P(K > m). For the expected-FPR version, E[FPR] <= alpha + P(K > m) is the simple bound, since FPR <= 1 on the event K > m. Main-text line 68 ("If at most a share pi_max ... are patients") should state this as a deterministic assumption, or the bound should include the binomial term. With prevalence 0.5%, pi_max = 5% and n = 360, P(K > 18) is tiny, so this costs nothing and makes the result correct.

**(c) Proof structure.** Step (i), "If all cases lie below t, then t is the r-th largest of n - m controls", holds only when exactly m cases are present. Steps (i)-(iii) are a case-by-case argument where one line would do. Whatever the case scores (even adversarial), t is at least the r-th largest of the n - K pool controls. Its tail mass is therefore at most Beta(r, n - K - r + 1), which is stochastically no larger than Beta(r, n0 - r + 1) because n - K >= n0. Please replace (i)-(iii) with this argument and state exchangeability explicitly: pool controls and a future control are exchangeable, conditional on K.

**(d) Sample-size rule.** The rule (SI line 57; `needed_pool_size`) is defined by an arbitrary slack (expected FPR >= alpha - 0.02 when the pool has no cases). It is evaluated on a grid with steps of 10 below 1,000 and 100 above, so "1,500" is a grid value. Also, n = 360 is the answer for pi_max = 0 as well as 1%. Please state these choices in the main text next to Figure 2C.

### M4. Inference treats 32 dependent units as independent; the bootstrap is not the pre-registered cohort-level bootstrap; the ctrl10 comparison does not hold up under clustering
**Location:** analyze_final.py lines 29-42; SI line 66; protocol.md line 31; main text lines 75-77.

The protocol specifies a "cohort-level bootstrap 95% CI". The code resamples the 32 cohort x model differences independently (`rng.choice(diff, len(diff))`), which is a deviation from the protocol. The units are not independent:

- LASSO and RF are scored on identical splits of the same cohort. The between-model correlation of the source absolute error is 0.78.
- YachidaS_2019 controls appear in both the CRC and adenoma tasks, so 4 units share one control set. FPR depends only on controls.

I re-ran the paired tests with (i) 16 cohort-task clusters and (ii) 15 control-set clusters. In each case I used a Wilcoxon test on cluster means, a cluster bootstrap, and Holm correction over 9 comparisons:

| comparison | reported (32 units) | 16 cohort-task clusters | 15 control-set clusters |
|---|---|---|---|
| rpoolmean - source | -0.108 [-0.160, -0.065], P_holm < 1e-4 | [-0.177, -0.056], P_holm = 4e-4 | [-0.179, -0.057], P_holm = 7e-4 |
| rpoolmean - local_q | -0.017 [-0.026, -0.010], P_holm = 1e-4 | [-0.029, -0.008], P_holm = 0.004 | P_holm = 0.005 |
| rpoolmean - ctrl10 | +0.006 [0.001, 0.010], P = 0.048 | [-0.001, 0.012], **P_holm = 0.18** | [-0.000, 0.012], **P_holm = 0.13** |

The main conclusions hold under clustering. The ctrl10 comparison does not. Also, the manuscript reports P = 0.048 (rpoolmean significantly *worse*) while saying the rule "came close to" ctrl10. A significance test cannot support "close"; that needs an equivalence or non-inferiority margin. Finally, the Wilcoxon signed-rank test drops zero differences (HallAB_2017 for ctrl10), and it tests a shift in location while the CI is for the mean. Please say so.

**Fix:**
- Re-run the paired analysis with cohort-task (or control-set) clusters, as pre-registered: cluster bootstrap and either Wilcoxon on cluster means or a mixed model with a random cohort effect.
- Report the change from 32 units as a correction of a protocol deviation.
- For ctrl10, report a mean difference with a cluster CI and an equivalence margin set in advance (for example +/-0.02 FPR), or drop the P-value.

### M5. The primary metric hides how much one laboratory's FPR varies, and abstention counted as FPR 0 changes the ranking
**Location:** SI lines 63-65 and 88-89; main text lines 74-81; analyze_final.py lines 8-19.

Cohort-RMSE is computed on the mean FPR over 200 splits. It measures bias across cohorts, not what happens to a single laboratory. A laboratory deploys once. Per-deployment RMSE at alpha = 0.10, pi = 0.01, which I computed from the raw rows, is:

| rule | per-deployment RMSE | cohort-RMSE |
|---|---|---|
| rpoolmean | 0.082 | 0.031 |
| ctrl10 | 0.103 | 0.027 |
| source | 0.193 | 0.185 |

The pre-registered secondary endpoint P(FPR > alpha + 0.05) is **0.142** for rpoolmean, so one deployment in seven exceeds 15% FPR. The main text does not report this. Some of this spread is noise from the small evaluation halves, which the development log puts at a floor of about 0.04. That is a reason to report it with the noise separated out, not to leave it out.

Abstention is coded as FPR 0 and so as an absolute error of alpha. rpoolmean's RMSE of 0.031 comes mostly from the HallAB_2017 abstention (2 of 32 units each contribute 0.10). Without that cohort the RMSE is 0.019, and ctrl10's is 0.010. A symmetric RMSE also scores conservative error (the guaranteed direction) the same as anti-conservative error.

**Fix:**
- Report the distribution of realised FPR per deployment (quantiles, or P(FPR > alpha + 0.05)) next to cohort-RMSE in Figure 2A and the text.
- Report abstention as its own outcome and compute error metrics on non-abstaining deployments, in addition to the current coding.
- Add a one-sided exceedance metric that matches the one-sided guarantee.
- Change "keeps the promise" to "keeps the *expected* FPR at or below the target".

### M6. Claims go beyond the data, and unfavourable pre-registered results are left out
**Location:** lines 4 (title), 23-24, 38, 62-63, 85-86, 92-93; protocol.md lines 17, 24, 28.

- **"Although the AUROC stays acceptable" (line 24) and "The AUROC did not warn about this" (line 38).** Locked AUROCs range from 0.54 to 0.86. Adenoma is 0.54-0.65, T2D is 0.58-0.69, and the most extreme FPR (0.73 for QinJ_2012 RF) comes with AUROC 0.58. Several classifiers barely beat chance, so the claim "AUROC hides the problem" rests mainly on CRC (3 cohorts). *Fix:* report AUROC per cohort in Table S1, restrict the AUROC-versus-FPR statement to cohorts with AUROC >= 0.7, or quantify it (for example, the rank correlation between AUROC and |FPR - alpha|).
- **"These methods only worked when about half of the pool were patients" (lines 62-63).** The locked data go up to pi = 0.2 only, and at pi = 0.2 every one of these methods is still worse than rpoolmean and local_q. In development, EM and MLLS failed at about 50% as well (cohort-RMSE 0.325 and 0.361). *Fix:* limit the statement to the mixture methods, cite it as a development result, or remove it.
- **"A rank rule on a few hundred of the laboratory's own unlabelled samples restores ... with a guarantee" (lines 92-93) and lines 85-86.** The locked pools held 6-321 controls (median about 24). The high-probability version abstained completely in 8 of 16 cohort-task pairs (abstention 0.50 of units). Where it did not abstain, its mean FPR was 0.025 and sensitivity 0.075. At about the recommended pool size it was tested only on MetaCardis_2020_a (n = 321). The protocol (line 17) requires rpool to be "reported with its abstention rate". The main text does not report rpool's locked results at all. *Fix:* report rpool's locked FPR, sensitivity and abstention in the main text.
- **Secondary alpha = 0.05 results are missing from the main text.** At alpha = 0.05, ctrl10 abstains in 100% of units (it needs at least 19 controls) and rpoolmean in 31%. These are pre-registered secondary results and should be summarised in one sentence.
- **Title "...fixes it".** This should be qualified as in M1.

### M7. Some "locked" FPR endpoints use control samples seen during development, and one control set is counted four times
**Location:** SI lines 82-84 (Table S1 note); data_lock.md; main text lines 33-34 ("locked 16 test cohorts before any method was designed").

The realised FPR depends only on the controls. Four of the five adenoma cohort-task pairs (FengQ_2015, HanniganGD_2017, ThomasAM_2018a, ZellerG_2014) use the same controls as the CRC development cohorts. Those controls were used to choose the method. So 8 of 32 primary units measure FPR on development controls, and the SI note understates this. YachidaS_2019 controls are counted in 4 units. data_lock.md also says the pilot "has touched all CRC cohorts", including the three locked CRC cohorts.

I ran a sensitivity analysis excluding the adenoma task. The conclusions hold (cohort-RMSE rpoolmean 0.035, ctrl10 0.032, source 0.216). The issue therefore needs disclosure and a sensitivity analysis rather than a change of conclusion.

**Fix:**
- Report the primary endpoint excluding the four adenoma pairs that reuse development controls (or the whole adenoma task).
- Count YachidaS once in inference (see M4).
- Change line 33 to say that the pilot had already seen the three locked CRC cohorts.

---

## MINOR issues

1. **"Binomial test of overdispersion" (main text lines 37-38; analyze_final.py lines 53-59).** The statistic is sum (FPR_c - 0.1)^2 / (0.09 / n_pool,c). It tests whether every cohort has FPR exactly 0.10, which is calibration to a fixed value, not overdispersion around a common mean. It also has several problems:
   - It ignores the uncertainty of the source threshold itself. That threshold is estimated from training out-of-fold controls and is shared by all cohorts of a task, so the cohorts are correlated.
   - It uses n_pool as a stand-in for the evaluation size.
   - LASSO and RF are tested separately although they are not independent.
   - P = 5 x 10^-88 is false precision.

   *Fix:* call it a chi-square goodness-of-fit test against FPR = 0.10. Better, report a heterogeneity estimate (for example, the between-cohort SD of FPR from a beta-binomial or random-effects model, with CI). Report P as "< 10^-10".
2. **Inconsistent rounding:** the training cut-off is "0.19" at line 58 and "0.185" at line 75. Use one value.
3. **Development numbers presented next to locked numbers (lines 39-40 and 42-44).** The RF mean FPR of 0.092 and RMSE of 0.125 come from development round 3 (R = 30). The values 0.33 and 0.87 come from round 4(B), LASSO, local quantile, pi = 0. None of these are in main_tables.md. Label them as development results, name the rule (local quantile) and the model, and point to their source (novelty_escalation_log.md / a supplementary table).
4. **Training description (lines 31-33).** "We trained ... on eight development CRC cohorts" applies only to the CRC task. IBD, T2D and adenoma models were trained leave-one-cohort-out on the other 3-4 cohorts of the same disease. Those training sets are small, and for 3 or more training cohorts the out-of-fold scores come from GroupKFold. State this, because it affects how variable the source threshold is.
5. **Consequences per 1,000 (lines 83-85; main_tables CRC table).** These figures average 3 CRC cohorts x 2 models (6 units), give no uncertainty, and use pools with a 1% case share while assuming 0.5% prevalence. Per-unit healthy referrals per 1,000 range from 113 to 301 for the training cut-off and 73 to 98 for the rank rule. Report this range, or a cluster CI, instead of single values.
6. **Sensitivity comparison (lines 79-81).** Sensitivities compared at different realised FPRs (0.48 at about 0.09 vs 0.65 at about 0.20) mix the effect of the operating point with the cost of the method. Abstentions count as sensitivity 0. Report sensitivity at a matched realised FPR (from the ROC within each cohort) or as the loss relative to an oracle threshold set at the cohort's true 90% specificity.
7. **Protocol bookkeeping.**
   - Commit 7fe8ca7 changed the Holm code after the protocol freeze ("tested on partial output"). Say which output was used (the smoke test or a locked partial run).
   - The RF result depends on `resume_final.py` replaying the random number generator. The replay was checked on LASSO only. Deposit the resume log and a checksum of the replayed split indices for ZellerG_2014.
   - SI lines 17-19 say "each locked analysis was run once". Commit d4b48e6 shows provisional tables made from partial locked output. Disclose this, and state that no decision followed from it.
8. **The ctrl10 comparator at alpha = 0.05** cannot produce a threshold (it needs at least 19 controls) and abstains everywhere. Say so where Table S2 is cited, or use 20 controls for alpha = 0.05.
9. **Holm family.** The family of 9 tests includes rpool (a variant of the primary rule) and local_q. That is acceptable, but state the family explicitly in the SI.
10. **SI line 42 vs main text line 68.** pi_max = 0.05 is fixed in the locked analysis. The sample-size discussion (lines 85-86) uses pi_max = 1%, 5% and 10% without saying that only 5% was evaluated.
11. **Line 79 ("as designed").** Give the abstention condition explicitly: rpoolmean returns no threshold when floor((n0 + 1) alpha) = 0, i.e. fewer than 9 pool samples at alpha = 0.10 and fewer than 19 at alpha = 0.05. At pool sizes of 9-14 the rule uses the pool maximum (r = 1). Readers should know how small pools behave.
12. **Figure 2A** should show cluster CIs for each cohort-RMSE, not only point estimates.

---

## Number check (manuscript vs results/main_tables.md vs raw data)

| Manuscript statement | Source | Status |
|---|---|---|
| FPR 0.00-0.74; median 0.10 | overdispersion block; raw median 0.104 | OK |
| P = 2e-52 / 5e-88 | 1.82e-52 / 4.93e-88 | OK (see minor 1) |
| RF dev mean 0.092, RMSE 0.125; 0.33 / 0.87 | development log only | Not in locked tables (minor 3) |
| 0.41 / 0.34 / 0.32 / 0.20 / 0.15 vs 0.19 | alpha 0.1, pi 0.01 table | OK (rounding inconsistent with 0.185, minor 2) |
| 0.031 vs 0.185; -0.108 [-0.160, -0.065] | paired table | OK (CI not cohort-level, M4) |
| ctrl10 0.027; 0.006 [0.001, 0.010], P = 0.048 | paired table | OK (does not hold under clustering, M4) |
| LASSO 0.031 vs 0.170; RF 0.031 vs 0.199 | recomputed from raw | OK |
| smallest cohort, 6 pool controls, abstained | HallAB_2017 | OK |
| CRC sensitivity 0.48 vs 0.65 | CRC table | OK |
| 199 vs 87 healthy referrals per 1,000 | 995 x FPR | OK |
| 360 / 610 / 1,500 | `needed_pool_size` | OK |
| 19 studies, 24 pairs, 3,626 unique samples | table_s1_cohorts.csv (4,051 - 425 reused controls) | OK |

Check scripts are in the reviewer's scratch directory (r1_stats/c1.py-c4.py) and can be supplied on request.
