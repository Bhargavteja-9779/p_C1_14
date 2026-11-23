# Referee report 2: statistics and methods

**Manuscript:** "Twenty local controls keep gut-microbiome diagnostic thresholds honest at new sites" (iMeta Letter)
**Scope of this report:** I checked the statistical design and the code against the outputs: protocol.md, data_lock.md, run_locked.py, analyse_locked.py, extra_analyses.py, src/*.py, endpoints.txt, results_locked.md, the per-cohort score files, and locked_rows.csv.gz. I did not re-run the locked analysis. All re-analyses below are read-only, run on the saved rows and scores. The scratch scripts are in /tmp/claude-0/review2/.

**Recommendation:** Major revision.

---

## Summary

The paper makes two claims.

1. **The drift claim.** A threshold set at the 90th percentile of training-control scores does not give 10% FPR at new sites.
2. **The fix.** A split-conformal order statistic computed from about 20 labelled local controls restores the target FPR.

The work has real strengths. The code is short and readable. A dated data lock and a pre-registration were committed before the locked run. Negative results are reported. Most numbers in the text match the outputs (see the checklist at the end).

Four statistical problems stand in the way of acceptance.

1. **The success criterion for the fix is close to guaranteed.** Calibration and evaluation controls are random halves of the same cohort, so they are exchangeable by construction. Under exchangeability, split-conformal gives E[FPR] = (n+1−k)/(n+1) = 0.095 at n = 20 by theorem. The observed cohort means (0.082–0.113) and the per-split exceedance (19.1% observed vs 17.6% predicted by the Beta(2,19) distribution) reproduce the theory almost exactly. The experiment never tests the one assumption that matters in deployment: that local controls resemble future screened people.
2. **Part of the drift may be an artefact of the pipeline, not of the site.** The threshold comes from out-of-fold scores of leave-one-cohort-out models. The target cohort is scored by a different model, refitted on all training cohorts. For random-forest adenoma, the source threshold lies above the maximum target score in 4 of 5 cohorts, which gives FPR = 0 and sensitivity = 0. In addition, the three external CRC cohorts show a shared upward offset, not between-site dispersion.
3. **The two main comparators are not fair.**
   - The EM baseline degenerates: its prevalence estimate goes to π̂ = 1, and the threshold then lands on the minimum or the maximum score.
   - The label-free pool quantile is tested only on pools with 65–89% cases. In the screening use-case the paper targets (prevalence 0.5–1%), the same label-free rule would be nearly valid.
4. **The over-dispersion chi-square tests the wrong hypothesis.** Its P-values are overstated.

---

## Major issues

### M1. The pre-stated success criterion for conformal is close to tautological, and the design cannot detect the failure that matters

**Evidence**

- run_locked.py splits each cohort's controls at random into a calibration half and an evaluation half (`p0 = rng.permutation(i0)`). Local controls and evaluation controls are therefore exchangeable draws from the same finite set.
- For k = ⌈(n+1)(1−α)⌉ the conditional FPR is Beta(n+1−k, k). This gives:

  | n | k | E[FPR] | Theoretical P(FPR > 0.15) | Observed |
  |---|---|---|---|---|
  | 10 | 10 | 0.091 | 0.197 | 0.210 |
  | 20 | 19 | 0.095 | 0.176 | 0.191 |
  | 30 | 28 | 0.097 | 0.151 | 0.186 |

  (My simulation that adds the binomial noise of the evaluation half gives 0.198 at n = 20, which matches.)
- The criterion is computed on the **cohort mean over 200 splits**. That mean converges to the finite-population expectation, about 0.095. A "within [0.05, 0.15]" result is therefore guaranteed for any data set. The SD of cohort means is driven to about 0 for the same reason.
- results_locked.md, caveat 1, already admits this ("the band criterion is close to guaranteed"). The manuscript instead presents it as an empirical finding ("Both pre-stated success criteria were met"; "kept every cohort within 0.08–0.11").

**Why it matters**

The empirical content of the conformal arm is zero beyond the theorem. The real deployment risks are left untested:
- local controls recruited differently from the screened population (colonoscopy-negative volunteers vs FIT-negative or unselected people);
- temporal drift;
- a different laboratory batch.

**Fix**

- State plainly that the within-site random-split design verifies the theorem, not deployment validity.
- Add at least one **non-exchangeable** calibration experiment. Options:
  1. calibrate on controls from one recruitment stratum and evaluate on another (MetaCardis by country; YachidaS_2019 by recruitment period or sub-group, if metadata allow);
  2. calibrate on controls from a "sister" cohort (same lab or country, e.g. ThomasAM_2018a/b → ThomasAM_2019_c) and evaluate on the target;
  3. calibrate on controls whose age, sex or BMI distribution is shifted, using reweighting.
- Report realised FPR there.
- Re-word the abstract. The fact that the average over 200 hypothetical calibration sets is 0.08–0.11 is not what a single laboratory experiences (see M2).

### M2. Single-deployment performance is under-reported; the headline averages over calibration sets

**Evidence**

From locked_rows, at α = 0.10, the share of single splits with realised FPR inside [0.05, 0.15] is:

| Method | Share in band | Share below 0.05 |
|---|---|---|
| conformal, n = 20 | 0.464 | 0.345 |
| conformal, n = 10 | 0.359 | — |
| source (status quo) | 0.274 | — |

The Beta(2,19) theory gives 0.56 in band even with a perfect evaluation set.

So a laboratory that follows the recommendation lands in the target band only about half the time, and is too strict about a third of the time. The text mentions only the upper tail (19%).

**Fix**

- Report the full distribution of the conditional FPR per method: in-band share, below-band share and above-band share.
- Preferably remove the evaluation-half noise (see M6). Compute the conditional FPR analytically, or against all non-calibration controls.
- Revise the abstract and the conclusion ("kept every cohort within 0.08–0.11") accordingly.
- Give the n needed for a stated in-band probability (for example 80%). This is the planning number a laboratory actually needs.

### M3. Score-scale mismatch between the threshold model and the scoring model confounds the drift claim

**Evidence**

- models.py `train_and_score`: the threshold is the 90th percentile of out-of-fold scores from leave-one-cohort-out models trained on K−1 training cohorts. Target scores come from `m = make(name).fit(Ztr, ytr)`, a different model trained on all K training cohorts.
- For random forest in particular, score scale depends on the composition of the training set.
- Random-forest adenoma, source threshold vs maximum target score:

  | Held-out cohort | Source threshold | Maximum target score |
  |---|---|---|
  | FengQ | 0.274 | 0.266 |
  | HanniganGD | 0.305 | −0.058 |
  | ThomasAM_2018a | 0.278 | 0.015 |
  | ZellerG | 0.289 | 0.207 |

  Every target sample falls below the threshold, so FPR = 0.000 and sensitivity = 0.000 (endpoints: adenoma RF source sensitivity 0.036).
- These degenerate pairs are counted as "drift" in the 22/32 figure, in the over-dispersion test and in the post-hoc Spearman analyses.
- The T2D and IBD leave-one-out tasks train on only 3 cohorts, so the out-of-fold models see 2 cohorts, which makes the mismatch largest exactly where the largest drift is reported.

**Fix**

Run a sensitivity analysis that removes the mismatch. Options:
- score the target with the ensemble (average) of the leave-one-cohort-out fold models whose out-of-fold scores define the threshold; or
- hold out one training cohort as a dedicated "source calibration" cohort and train the scoring model on the rest; or
- report internal–external FPR within the training cohorts using the same fold models.

In addition:
- Report how many pairs remain outside the band.
- Flag degenerate classifiers (sensitivity = FPR = 0) and exclude them from the drift statistics, or report them separately.
- Report the leave-one-cohort-out AUROC within the training cohorts so readers can see which models are usable.

### M4. The over-dispersion chi-square tests "FPR = α at every site", not over-dispersion; its P-values are overstated

**Evidence**

The statistic in analyse_locked.py is Σ(FP − α n₀)² / (n₀ α(1−α)) with df = K. It is centred at the nominal α, not at the pooled FPR. It therefore mixes two things:
- a common bias (every site miscalibrated in the same direction);
- true between-site heterogeneity.

Splitting the two (my re-analysis on fp_full):

| Cell (α = 0.10) | Pooled FPR | Heterogeneity Q (df = K−1) | P | Bias z |
|---|---|---|---|---|
| CRC LASSO | 0.177 | 4.3 | 0.12 | 4.8 |
| CRC RF | 0.197 | 4.2 | 0.12 | 6.0 |

So the three external CRC cohorts are **not** over-dispersed relative to each other. They share an upward offset, which is consistent with M3. Heterogeneity is clear for T2D, IBD and adenoma.

The binomial variance also ignores two sources of variance:
- **Threshold estimation.** The threshold is an empirical quantile of m source controls, which adds about α(1−α)/m to the variance of each site's FPR. Adding the factor (1 + n₀/m) moves the T2D RF P-value from 6×10⁻¹⁷⁷ to 1×10⁻¹³⁶ and the CRC LASSO P-value from 1.8×10⁻⁶ to 8×10⁻⁵.
- **Dependence.** Out-of-fold scores are clustered by cohort, so the effective m is much smaller than the raw count. The three CRC cohorts share one threshold, so their terms are correlated.

P-values such as 10⁻¹⁷⁷ have no meaning here.

**Fix**

- Replace the test with a random-effects (binomial-normal or beta-binomial) model per task × model. Report the pooled bias (logit scale, with CI) and the between-site SD τ (with CI).
- If a test is kept, use the heterogeneity Q around the pooled FPR (df = K−1), with variance inflated for threshold estimation. Report P-values to a sensible floor (for example "P < 10⁻¹⁰").
- Correct the text: "over-dispersion was significant in all eight cells" is false for CRC once bias is separated from dispersion.

### M5. The EM "prevalence correction" baseline is a degenerate implementation (a straw man)

**Evidence**

1. Under the label-shift assumption the class-conditional distributions are unchanged, so the correct FPR-targeting threshold is simply the source threshold. The function's own docstring says so ("-> same as source threshold"). Saerens-EM changes posteriors and accuracy-optimal decisions, not a threshold that targets FPR.
2. The code does something else. It estimates π by EM, using KDEs fitted on **out-of-fold** source scores but evaluated on **refit-model** target scores (see M3). It then deconvolves F₀ = (F_u − π̂ F₁,src)/(1−π̂) with a floor of `max(1−π, 1e-6)`.
3. Re-running `em_label_shift` on saved scores, π̂ converges to the boundary value 1.0:

   | Pair | π̂ | Resulting threshold | FPR |
   |---|---|---|---|
   | HMP2 LASSO | 1.0 | pool minimum | 1.0 |
   | Sankaranarayanan LASSO | 1.0 | pool minimum | 1.0 |
   | HanniganGD RF | 1.0 | pool minimum | 1.0 |
   | QinJ LASSO | 1.0 | pool maximum (5.33) | 0.0 |

   The cohort means of exactly 1.000 in Table S3/Figure 2A are artefacts of this boundary solution.
4. Only 20 replicates were used, and the pool has a prevalence of 65–89%, not the cohort's prevalence.

**Fix**

- Either drop EM, explaining that prevalence correction cannot change the FPR at a fixed threshold by definition, or implement a standard version: Saerens EM on calibrated posteriors (or BBSE / MLLS) with π̂ bounded away from {0, 1}, mapped to a threshold through the source control CDF. Under label shift this returns the source threshold.
- Remove the sentences "Prevalence correction made things worse" and "EM put cohort-mean FPRs anywhere between 0 and 1". They describe a bug, not the method.

### M6. The label-free pool quantile is evaluated only in an unrepresentative regime, and the prevalence-bounded variant was silently dropped

**Evidence**

- The unlabelled pool is the calibration-half controls plus **all** cases. Its prevalence is 0.65–0.89 (HMP 0.89, Sankaranarayanan 0.68, Yachida 0.67, Qin 0.66), not the "natural prevalence" or "about half cases" stated in the protocol and the manuscript.
- In the intended use-case (CRC screening, π ≈ 0.005–0.01) the SI's own bound gives FPR ≤ α/(1−π) ≈ 0.1005. The (1−α) quantile of about 20 or more consecutive **unlabelled** screened samples is then essentially the conformal rule without colonoscopy confirmation.
- Development round 1 confirms this: the pool quantile gives FPR ≈ α at π = 0.
- `pool_quantile_bounded` is implemented in calibrate.py and was planned in dev round 2(b), but it does not appear in the protocol or the results.

This undermines the central message that only labelled local controls work. Colonoscopy-confirmed controls are expensive; consecutive unlabelled samples are free.

**Fix**

- Add the pool quantile (and the prevalence-bounded variant) with pools at realistic prevalence (π ∈ {0, 0.01, 0.05, 0.1}), built by subsampling cases.
- Compare it to conformal at equal n.
- Revise the conclusions and recommendation (ii) accordingly.

### M7. The batch-correction baseline is prevalence-dependent, transductive, and not the method cited

**Evidence**

- `train_and_score_cohortstd` z-scores each species within each cohort using all target samples, cases included (case fraction 0.21–0.79 across cohorts). It also uses the evaluation-half controls.
- The centring therefore depends on the case mix. At a screening site (π ≈ 0.005) the same transform would centre on almost all controls, so the realised FPR differs from what is tested here.
- Using evaluation controls in the transform is transductive leakage. It is label-free, but it means the evaluation set is not independent of the method.
- Ref. 14 (Gibbons et al.) is percentile normalisation **to controls**, which is a different method.

**Fix**

Re-implement the batch correction in a deployment-realistic way:
- fit it on calibration-half samples only, never on evaluation controls;
- add a controls-only reference variant (percentile or z-normalisation against the n local controls), which is a natural competitor to conformal at equal labelling cost;
- add a standard tool (ComBat/MMUPHin; DEBIAS-M if feasible).

### M8. The secondary endpoint for tong95 was missed and not reported; tong95 results are pooled from weak models

**Evidence**

- The protocol pre-specifies, for tong95, "share of splits with FPR ≤ α (target ≥ 0.95)". Observed values are 0.941 (n = 30) and 0.944 (n = 50), both below target. The likely cause is evaluation-half noise; theory gives 0.958 and 0.966. The manuscript does not report this endpoint.
- At n = 30 and α = 0.10, tong95 is simply the **maximum** of the 30 controls (k = 30; E[FPR] = 1/31 = 0.032). This should be stated.
- The quoted sensitivity cost of 0.08–0.11 pools 12 and 8 pairs dominated by T2D and adenoma models with AUROC 0.54–0.64. For the only CRC cohort where tong95 is feasible (YachidaS_2019), sensitivity is 0.17–0.21, vs 0.31–0.33 for conformal n = 20.

**Fix**

- Report the endpoint and explain the shortfall.
- Report tong95 per task, with a paired comparison against conformal on the same cohorts.

### M9. Method comparisons pool different cohort sets; no paired contrasts

**Evidence**

- Figure 2 and Table S3 compare `source` (32 pairs) with conformal n = 20 (20 pairs), n = 30 (12 pairs) and tong95 n = 50 (8 pairs). Figure 3B pools a different cohort set at each n, as its legend admits.
- On the 20 feasible pairs, source sensitivity is 0.377, not 0.386. Source has 7/20 (35%) pairs within band. The source SD for T2D is 0.362, not 0.298.
- The SD comparison in the text (for example "0.30 to 0.005" for T2D) uses all cohorts for source but only feasible cohorts for conformal.

The conclusions do not change direction, but the numbers are not comparable as printed.

**Fix**

- Report all contrasts on the matched (feasible) set of cohorts, with the full-set source numbers as secondary.
- Use paired differences in sensitivity and FPR, with cohort-level CIs.

### M10. The pre-registered SD criterion "in every disease task" could not be evaluated for IBD; this is an undeclared deviation

**Evidence**

- Only NielsenHB_2014 is feasible for IBD at n = 20, so the SD is NaN (endpoints.txt).
- results_locked.md re-words the criterion as "every task with ≥ 2 feasible cohorts". The SI says "There were no deviations from the protocol", and the manuscript says both criteria "were met".

**Fix**

Add a dated deviation entry. State that the criterion was met for 3 of 3 evaluable tasks and was not evaluable for IBD.

### M11. The cohort bootstrap is under-powered and double-counts a cohort

**Evidence**

- The bootstrap pools all four tasks per model into 10 "cohorts". YachidaS_2019 appears twice, once as CRC and once as adenoma, with the **same control samples**, but is treated as independent.
- The SD across pooled tasks mixes differences between tasks with differences between sites.
- With conformal SD ≈ 0 by construction (M1), the CI is just a percentile CI for −SD(source) over 10 points. That is unstable and not a test of the method.

**Fix**

- Cluster the bootstrap by unique control set (merge the two YachidaS_2019 entries).
- Report it per task where K ≥ 3, or use the random-effects τ from M4 with a profile-likelihood CI.
- Describe it as uncertainty in the status-quo dispersion.

### M12. Leakage and independence of the held-out cohorts

- **Adenoma task.** Four of the five adenoma "held-out" cohorts (FengQ, HanniganGD, ThomasAM_2018a, ZellerG) are CRC **development** cohorts. Their controls were used to design and choose the methods (dev rounds 1–2), and the drift was observed on them during development. They are not locked data for the drift claim or for the method choice. Only the adenoma cases are new.
- **YachidaS_2019** controls are evaluated both as a CRC-external cohort and as an adenoma held-out cohort, so "16 held-out cohorts" contains 15 independent control sets.
- **The pilot** (code/pilot/pilot_threshold_transfer.py) computed status-quo FPR on all 11 CRC cohorts, including the 3 later "locked" external cohorts, before data_lock.md was committed. The drift on the external CRC cohorts was therefore seen before the lock. This is disclosed in the SI, but the main text says these cohorts were "locked away during method design", which is true only for method design.
- **Label-free methods are transductive.** The unlabelled pool contains every case used to compute sensitivity. This is acceptable for label-free methods, but should be stated.
- **Timing.** analyse_locked.py was committed 27 s after the first locked score file was written (16:39:09 vs 16:38:57). This is harmless in practice, but strictly the analysis script was not pre-registered.

**Fix**

- Disclose these points in the main text.
- Report the drift statistics with and without the development-cohort adenoma held-outs.
- Count independent control sets correctly.

### M13. The harm-per-1,000 calculation transfers case-control sensitivity to screening and has no uncertainty

**Evidence**

- The formulas (1000(1−p)·FPR; 1000·p·(1−sens)) are coded correctly. But the sensitivity comes from case-control cohorts whose CRC cases are mostly symptomatic or advanced, so there is spectrum bias for screen-detected cancer. The false-positive estimate also assumes that controls represent screened people.
- No CIs are given. With 40–74 cases per cohort, the SE of sensitivity is about 0.06–0.08, i.e. about ±0.4 missed cancers per 1,000. The "1.5–3.3 vs 1.3–2.3" contrasts lie within noise.
- "Up to one more missed cancer": the exact LASSO YachidaS difference is 5 × (0.547 − 0.330) = 1.08.

**Fix**

- Add bootstrap CIs.
- Present detected cancers and PPV alongside.
- Label the numbers as illustrative and subject to spectrum bias.
- Say "about one".

### M14. The post-hoc "cause" analysis is largely mechanical

**Evidence**

- ρ = 0.80 between the shift in median control score and realised FPR is close to an identity. FPR is the share of target control scores above a quantile of the source control scores, so moving the control distribution upward raises FPR by definition.
- The shift also includes the out-of-fold vs refit mismatch (M3).
- The AUROC-vs-error and LASSO-vs-RF correlations use 32 or 16 non-independent points, including the degenerate RF adenoma pairs and the duplicated YachidaS_2019.

**Fix**

- Present these as descriptive.
- Remove the word "cause".
- Drop the degenerate pairs and the duplicate cohort, or analyse them separately.

---

## Minor issues

1. **LASSO specification depends on the library version.** `LogisticRegression(l1_ratio=1, solver="liblinear")` gives an L1 penalty only in scikit-learn ≥ 1.8, where `penalty` is deprecated. I checked 1.9.1: 5/50 non-zero coefficients. In older versions `l1_ratio` is ignored and the model is ridge. State the version in the SI ("scikit-learn" is listed without one) and set `penalty="l1"` explicitly for older versions.
2. **Evaluation-half sizes are small.** HallAB_2017 has 6 evaluation controls, Sankaranarayanan 9, ThomasAM_2018a 12, HMP2 and HanniganGD 14. One false positive moves FPR by 0.07–0.17. P2 for `source` and the other non-local methods is inflated by this binomial noise, which does not reflect any threshold error. For methods that use no target controls, compute FPR on **all** target controls (fp_full already exists). For local methods, compute FPR against all non-calibration controls, or give the conditional FPR analytically. Show Clopper–Pearson CIs in Figure 1.
3. **The success-band definition is not symmetric in deployment terms.** [α/2, 1.5α] treats a 50% excess over target and a 50% shortfall alike. Justify this, or report the upper tail separately (it is the clinically relevant one).
4. **The "≥ 30" vs "≥ 29" minimum for tong95 is inconsistent.** The Conclusion says ≥ 30; the SI says n ≥ 29. The exact minimum is 29 (0.9²⁹ = 0.047).
5. **em and site_shift use R = 20.** This should be stated in the Figure 2 legend. The site_shift overflow warnings (run_locked.log) should be reported, together with how many fits hit the parameter boundary.
6. **site_shift identifiability.** With location, scale and mixing weight all free, the model is weakly identified when the shapes of the class distributions are similar (the dev log admits this). Report the share of fits with π̂ ∈ {0, 1} or b̂ at an extreme.
7. **Infeasible thresholds.** At α = 0.05 the +inf thresholds are averaged in as FPR = 0 and sensitivity = 0 (conformal n = 10, all tong95 rows). Table S3b reports these as valid rows with "share in band 0.000". They should be shown as "not feasible", not as numbers.
8. **Monte Carlo error is not reported.** With 200 splits, the SE of per-cohort P2 is about 0.03. P2 differences between methods of 0.02–0.05 (for example conformal n = 20 vs n = 30) are within MC noise.
9. **Figure 3B mixes cohort sets** at n = 30 (conformal and tong95 points sit at the same x over different cohorts than n = 10 and 20). The visual trend in n is confounded.
10. **"P from 1 × 10⁻³ to 1 × 10⁻¹⁷⁷"** should read 6 × 10⁻¹⁷⁷ (but see M4: such values should not be reported at all).
11. **The protocol says "using full-cohort counts" for over-dispersion,** while the manuscript's FPR ranges mix full-cohort values (Table S2) with split means (main text; for example RF CRC 0.31 vs 0.30). Use one definition.
12. **"natural prevalence"** in the protocol and SI is incorrect for the pool (see M6).
13. **AUROC rounding.** The minimum adenoma AUROC is 0.535, quoted as 0.54. This is acceptable, but give three decimals in the text or state the rounding rule.
14. **No CIs for the per-cohort AUROC** in Table S1. These are needed to show that the T2D and adenoma classifiers are better than chance (Sankaranarayanan cohort-std AUROC is 0.482).
15. **There is no oracle reference.** Report sensitivity at the true per-cohort 90% specificity (the pilot computed `sens_oracle`). This separates the sensitivity lost to threshold noise from the sensitivity lost to weak discrimination.

---

## Checklist of manuscript numbers

All values were checked at α = 0.10 unless stated. Sources: endpoints.txt, locked_cohorts.csv, locked_rows.csv.gz, extra_analyses.txt, and my own aggregation.

| # | Manuscript statement | Output | Verdict |
|---|---|---|---|
| 1 | 19 public cohorts | 11 CRC + 4 IBD + 4 T2D unique studies | OK |
| 2 | 3,626 people | 678 dev CRC + 717 ext CRC + 353 IBD + 1,669 T2D + 209 adenoma cases = 3,626 | OK |
| 3 | 16 held-out cohorts | 3 + 4 + 4 + 5 = 16 (but 15 independent control sets; M12) | OK (caveat) |
| 4 | FPR 0–73% at new sites (abstract) | 0.000–0.726 | OK |
| 5 | 69% of pairs off by > half target | 22/32 = 0.688 | OK |
| 6 | Conformal n = 20 kept every cohort within 0.08–0.11 | 0.082–0.113 | OK (but see M2) |
| 7 | 13–181 fewer unnecessary colonoscopies per 1,000 | LASSO: 12.9, 75.8, 180.8 | OK |
| 8 | Up to one more missed cancer | LASSO max 1.08 (Yachida); RF 0.94 | MINOR MISMATCH ("about one") |
| 9 | AUROC CRC 0.70–0.86 | 0.696–0.859 | OK |
| 10 | AUROC IBD 0.66–0.85 | 0.658–0.853 | OK |
| 11 | AUROC T2D 0.58–0.69 | 0.576–0.692 | OK |
| 12 | AUROC adenoma 0.54–0.65 | 0.535–0.650 | OK |
| 13 | LASSO realised FPR 0.05–0.59 | split means 0.045–0.589; full cohort 0.042–0.592 (ThomasAM_2018a adenoma) | MISMATCH (lower bound 0.04) |
| 14 | RF realised FPR 0.00–0.73 | 0.000–0.726 | OK |
| 15 | 22 of 32 pairs (69%) outside 0.05–0.15 | 22/32 | OK |
| 16 | Over-dispersion significant in all 8 cells | 8/8 by their chi-square; CRC heterogeneity not significant (P = 0.12; M4) | OK numerically / MISLEADING |
| 17 | P from 1×10⁻³ to 1×10⁻¹⁷⁷ | 9.6×10⁻⁴ to 6.1×10⁻¹⁷⁷ | MISMATCH (should be 6×10⁻¹⁷⁷) |
| 18 | External CRC LASSO 0.11–0.28 | 0.112–0.281 (split mean) | OK |
| 19 | External CRC RF 0.13–0.31 | split mean 0.128–0.310; Table S2 full cohort 0.13–0.30 | OK (inconsistent with Table S2) |
| 20 | "IBD and T2D: FPR 0.05 in Karlsson 2013 and MetaCardis" | Both are T2D cohorts (LASSO 0.049, 0.053) | MISMATCH (label) |
| 21 | T2D 0.59 in Qin 2012 | 0.589 (LASSO) | OK |
| 22 | IBD 0.41 in HMP2 | 0.407 (LASSO) | OK |
| 23 | Spearman ρ = −0.18, P = 0.31 | −0.18, 0.31 | OK |
| 24 | ρ = 0.69, P = 0.003 | 0.69, 0.0029 | OK |
| 25 | ρ = 0.80, P = 3×10⁻⁸ | 0.80, 3×10⁻⁸ | OK |
| 26 | Cohort-std: 28% within band | 9/32 = 0.281 | OK |
| 27 | Cohort-std worst cohort 0.32 | 0.321 | OK |
| 28 | Split P(FPR > 0.15) 0.38 → 0.32 | 0.384 → 0.323 | OK |
| 29 | EM cohort means between 0 and 1 | 0.000–1.000 | OK numerically (artefact; M5) |
| 30 | Pool quantile sensitivity 0.14 | 0.142 | OK |
| 31 | "about half cases" in pool | pool prevalence 0.65–0.89 | MISMATCH |
| 32 | site_shift 66% in band | 21/32 = 0.656 | OK |
| 33 | Anchor 40–50% in band | 0.40 (loc), 0.50 (loc-scale), n = 20 | OK |
| 34 | n = 20: 20 of 20 pairs, 0.08–0.11 | 20/20, 0.082–0.113 | OK |
| 35 | n = 10: 28 of 28, 0.08–0.11 | 28/28, 0.077–0.107 | OK |
| 36 | SD CRC 0.09 → 0.007 | 0.089 → 0.007 | OK |
| 37 | SD T2D 0.30 → 0.005 | 0.298 → 0.005 (source over 4 cohorts, conformal over 3; M9) | OK (non-matched) |
| 38 | SD adenoma 0.075 → 0.008 | 0.075 → 0.008 (5 vs 3 cohorts) | OK (non-matched) |
| 39 | Bootstrap LASSO −0.16 (−0.23 to −0.05) | −0.161 [−0.232, −0.048] | OK |
| 40 | Bootstrap RF −0.22 (−0.32 to −0.06) | −0.218 [−0.323, −0.061] | OK |
| 41 | Both pre-stated criteria met | IBD SD criterion not evaluable (M10) | MISMATCH vs protocol wording |
| 42 | 19% of splits > 0.15 with n = 20 | 0.191 | OK |
| 43 | tong95 risk 1–2% with 30–50 controls | 0.017, 0.008 | OK |
| 44 | tong95 sensitivity 0.08–0.11 | 0.078, 0.108 | OK (pooled weak models; M8) |
| 45 | Source LASSO 112–280 unnecessary colonoscopies | 111.8, 174.5, 279.6 | OK |
| 46 | Source LASSO 1.3–2.3 missed cancers | 1.3, 2.3, 1.4 | OK |
| 47 | Conformal about 99 unnecessary colonoscopies | 98.7–98.9 | OK |
| 48 | Conformal 1.5–3.3 missed cancers | 1.5, 3.3, 2.4 | OK |
| 49 | ⌈21 × 0.9⌉ = 19 → second-highest of 20 | correct | OK |
| 50 | α = 0.05 needs ≥ 19 controls (conformal) | (n+1)·0.95 ≤ n ⇔ n ≥ 19 | OK |
| 51 | 95% version needs ≥ 59 at α = 0.05 | 0.95⁵⁹ = 0.048 | OK |
| 52 | 10 controls at α = 0.05 gives no threshold | conformal n10 rows: sensitivity 0, FPR 0 (inf) | OK |
| 53 | "≥ 30" for 95% confidence at 90% specificity | exact minimum 29 (SI says 29) | MINOR MISMATCH |
| 54 | Only one IBD cohort feasible for n = 20 | NielsenHB_2014 only | OK |
| 55 | Figure 1/S1 values over 200 splits | yes for source / cohortstd / conformal | OK |
| 56 | Table S1 AUROCs | match locked_cohorts.csv | OK |
| 57 | Table S2 chi-square and P | match endpoints.txt | OK |
| 58 | Table S3a/b, S5 | match endpoints.txt / endpoints_by_task.csv | OK |
| 59 | SI: "no deviations from protocol" | SD criterion re-worded for IBD; tong95 endpoint unreported | MISMATCH |
| 60 | SI dev summary: SD 0.14 → 0.01 (dev round 2) | 0.141 → 0.008 (LASSO) | OK |

**Summary of the checklist:** 60 items checked. 52 match (some with caveats). 6 are mismatches (items 13, 17, 20, 31, 41, 59). 2 are minor wording mismatches (items 8 and 53). Several items are numerically correct but misleading (items 6, 16, 29, 37, 38, 44).
