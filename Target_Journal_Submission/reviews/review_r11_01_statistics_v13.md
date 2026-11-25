# Statistical review, round 11 — manuscript v13 (iMeta Letter)

**Reviewer 1 (methods and statistics)**
**Score: 6/10. Recommendation: major revision.**

## Summary

v13 fixes the round-10 items well. v6c is now labelled post hoc. The two cluster bootstraps are corrected. G3 is reported as falsified. Holm-adjusted P values are given. The generalisation claim for v6c is withdrawn. I re-derived almost every number in the main text from the result files. All but a handful agree; those are listed at the end.

I also re-read the code behind the balancing experiments, and this round found three new problems.

1. The v6b "country-balanced" weights do more than balance labels within each country, which is what the text says they do. They give every country × label cell equal total weight. This also down-weights large countries, China and Japan among them. It also gives single samples from Estonia, Norway, Hungary and Finland each 1/18 of all non-healthy weight. I ran a weighting that balances labels within each country but keeps each country's total weight. It removed only 37% of the East Asian gap (49% after level-matching the cut-off), not 88%. The stated mechanism, label case-mix within country, therefore explains roughly half the effect, not all of it.
2. The v6c weighting does not do what plan v6c and SI S6.5 describe ("each country carries equal total weight"). It makes a country's weight inversely proportional to its size. The result is that 4–5 single samples carry 95–98% of the T2D and IGT training weight, and 5 Canadian samples carry 74% of the CRC weight. The v6c "balanced" arm is therefore uninterpretable. It is not merely a "related but not identical weighting".
3. The variance decomposition in the main text is the confirmatory hypothesis H2, which was not supported. The text does not say so. Its 62% "pair" share also includes binomial sampling noise.

The headline atlas results (H1, the binomial out-of-band comparison and the prediction intervals) and the GMWI2 audit (QC, G1, G2, G3, G4) are sound and reproducible from the files. The burn-in maths is correct.

## Checks performed (scratch code in /tmp/claude-0/r11_stats/; nothing written to the repository)

- **Git timing.** Each plan was committed before its results:
  - protocol_v5 at 19:07:55, v5 results at 19:10:51;
  - protocol_v6 (df2677c, 10:22:48) before the GMWI2 results (28b2acd, 10:25:25);
  - protocol_v6b (28b2acd) before the v6b results (baf7218, 10:31:11);
  - protocol_v6c only in 3fde340, together with its results. This is correctly disclosed now.
  - Each gap is 3–6 minutes. The analysis code (atlas_v5.py, run_gmwi2.py, run_v6b.py) was committed only with the results. The v5 results commit says "path bug fixed", so the code had been run before. Git timestamps are set by the authors' own automated agent, so they bound the commit order but cannot show that no result was seen before a commit. The manuscript's wording, "time-stamped internal analysis plans", is appropriate. It should not be strengthened to "pre-registered".
  - protocol_v6b was written after the post hoc v6 exploration, and it says so. That is fine.
- **Heterogeneity.** I recomputed the following from v5_perpop_strict.csv / v5_het_strict.csv: I² median 0.94, range 0.64–0.97; shares of LASSO pairs above 0.15, above 0.25 and below 0.05 of 45%, 26% and 24%; FPR range 0–0.77 for n ≥ 100; out-of-band share expected by chance 14.8–16.2% against 50–97% observed; upper PI 0.22 (CRC) to 0.81 (IGT); 7 classifiers below AUROC 0.6 (3 below 0.5); 16 at AUROC ≥ 0.65; Spearman ρ −0.06, P = 0.76. All agree.
- **Variance decomposition.** var_test 0.366, var_pop 0.306 and var_resid 1.090 give shares of 21%, 17% and 62%. These agree with the text.
- **GMWI2.** I checked the following against the result files:
  - QC r = 0.991, 98.4% agreement on 704 samples;
  - α = 0.2084 (5,514 people in 44 studies);
  - I² 0.92, PI 0.018–0.685;
  - 12 of 15 populations out of band (80%) against 9.0% expected, P = 6.1e-13 (Poisson-binomial DP), Holm-adjusted 1.8e-12;
  - G3 0.257 vs 0.204, P = 0.72;
  - G4 0.211 → 0.044 (−79%, CI 64–85%, 11/13);
  - training-data I² 0.96, East Asian 0.64 vs 0.12, P = 5.3e-7, 657/1,067;
  - case-mix 1,574/2,522 vs 1,097/5,547, OR 6.74.
- **v6b.** analyse_v6b.py and corrected_boot_v13.py are now correct: each draw is relabelled as its own cluster, and the 41–149% CI reproduces. I also ran:
  - a level-matched gap;
  - a region-stratified bootstrap;
  - a CI for the absolute gap reduction;
  - a retraining ablation of the weighting scheme, which reproduces the authors' balanced scores at r = 0.999999.
- **v6c.** I computed the effective country weights produced by run_v6c.py's `weights()`.
- **Burn-in.** k = ⌈101 × 0.9⌉ = 91 gives an FPR distributed as Beta(10, 91). P(FPR > 0.15) = 0.0551 and E[FPR] = 0.099. Both are correct. For the binomial verification test at n = 100 the critical count is 22, the size is 0.039, the power at FPR 0.25 is 0.79 and at 0.30 it is 0.97. I also checked the fprcal unit tests, and the contaminated-burn-in results in deploy_v4_cc_summary.csv.
- **Control augmentation.** 0.087 → 0.078 with Wilcoxon P = 0.58 (29 populations) reproduces.

## MAJOR concerns

**M1. The intervention that removed 88% of the gap is not the "within-country case-mix" balancing that the text and the mechanism describe.**
Plan v6b and run_v6b.py set w = 1 / n(country, label). Every country × label cell therefore gets the same total weight. The main text says "within each country, healthy and non-healthy people carried equal weight". That is true, but this scheme also:
- equalises countries, which down-weights China (774 non-healthy samples, 611 healthy), Japan, France and the other large countries;
- gives 1/18 of all non-healthy weight to each of EST (1 sample), NOR (1), HUN (1), FIN (1) and SVK (3). These 7 samples, five cells out of 18, carry about 28% of the non-healthy weight.

I retrained the GMWI2 recipe leave-one-study-out (same features, C, solver and class_weight) under three weightings. Scripts: /tmp/claude-0/r11_stats/v6b_ablate.py and abl_an.py.

| Weighting | EA median | Other median | Gap | Reduction | Gap after level-matching | Pooled AUROC |
|---|---|---|---|---|---|---|
| Naive | 0.711 | 0.186 | 0.524 | — | — | 0.715 |
| Authors' balanced (reproduced) | 0.289 | 0.224 | 0.065 | 88% | 0.079 | 0.676 |
| Within-country label balance, country totals preserved: w = n_c / (2 n_c,l) | 0.572 | 0.240 | 0.332 | 37% | 0.266 (49%) | 0.709 |
| Authors' scheme, cells < 20 samples dropped | 0.378 | 0.314 | 0.063 | 88% | 0.088 | 0.666 |

"Level-matching" re-thresholds the balanced scores so that the pooled healthy FPR equals the naive 0.257.

Three conclusions follow:
- The tiny cells do not drive the result.
- Pure within-country label balancing, which is the operation the mechanism paragraph implies, removes only about 37–49% of the gap. That is below the pre-stated 50% criterion.
- Most of the 88% comes from equalising country weight, that is, from down-weighting the large East Asian (and European) studies overall.

These are my post hoc analyses on one seed, so they need confirmation. Even so, they mean that "pooled training across geographically unbalanced studies" is supported, while "case-mix" (more non-healthy than healthy samples from East Asia) as the sole mechanism is only partly supported.

*Resolution:*
1. Describe the v6b weights exactly, as "each country × label cell given equal total weight, which also equalises countries".
2. Report the decomposition above, or the authors' own version of it, as a post hoc ablation.
3. Reword the mechanism. For example: "country-level imbalance in pooled training explains most of the gap; label balance within country alone removed about 40%".
4. Change the graphical-abstract wording "balancing training data by country removed 88%" accordingly, and give its uncertainty.

**M2. The v6c weighting does not implement its plan, and the SI misdescribes it.**
run_v6c.py first sets w = 1 / n(country, label) and then divides by n(country). Every country × label cell already has the same total, so the extra division makes a country's weight inversely proportional to its size. The plan and SI S6.5 say "each country carries equal total weight". In the actual training sets:
- **CRC:** 5 Canadian samples carry 74% of the weight, and 509 Japanese samples carry 0.7%.
- **T2D:** 5 single samples (EST, FIN, HUN, ISL, SVK) carry 98% of the weight.
- **IGT:** 4 samples carry 95%.
- **IBD:** 37 British samples carry 66%.

The "balanced" disease classifiers were therefore fitted, and their weighted cut-offs set, almost entirely on a handful of people. This fully explains the FPR level shifts (T2D median 0.12 → 0.54; CRC 0.04 → 0.33) and the AUROC loss. The authors already withdrew the generalisation claim, which is correct. But the main text still presents v6c as "a related but not identical weighting" that "did not carry over cleanly". That reads as a substantive negative result about balancing. It is in fact an implementation artefact.

*Resolution:* either
- re-run v6c with the planned weights, w = 1 / (n(country, label) × number of labels in that country), excluding or merging cells below a minimum size, and report it as post hoc; or
- remove the v6c paragraph from the main text, and state in the SI that the weights were misimplemented and give the effective weight shares.

Do not report the C1 τ difference or its CI as evidence in either direction.

**M3. The variance decomposition is the failed confirmatory hypothesis H2, presented without saying so, and its "pair" component includes sampling noise.**
Plan v5 pre-stated H2 as "population variance component ≥ 20% of total; WRONG if < 10%". The result was 17% for LASSO (inconclusive) and 7.5% for RF (falsified). SI S5 records this. The main text instead reports "population 17%, classifier 21%, pair 62%" as a finding. It does not mention H2, the RF result (population 7%, classifier 46%) or the failure. This conflicts with the introduction's promise to "report the hypotheses that failed".

Separately, smf.mixedlm with one observation per pair puts binomial sampling variance into the residual. The mean sampling variance of the empirical logit is 0.25 for LASSO, about 23% of var_resid (1.09) and 14% of the total. For RF it is 0.57, about 47% of var_resid. The true classifier × population interaction share is therefore about 48% for LASSO, not 62%. For RF it could be well below its 47% residual share.

*Resolution:*
1. State in the main text that H2 was not supported (LASSO inconclusive, RF falsified), and give the RF shares.
2. Refit with the known sampling variances, for example a crossed-effects meta-regression in metafor::rma.mv with V = 1/(k+0.5) + 1/(n−k+0.5), or subtract the mean sampling variance. Report the interaction share net of noise.
3. Soften "the error was mostly specific to the pairing" if the corrected share falls below 50%.

**M4. Heterogeneity on the logit scale is used selectively.**
For v6c the authors rightly argue that a lower logit τ is not evidence of more uniform FPRs when levels move, and they report the median absolute deviation (MAD) of the FPR instead. They do not apply the same check to v6b B4 (τ 1.16 → 0.81, reported in the main text as "lowered between-study heterogeneity"). From v6b_loso_scores I get:

| v6b | Naive | Balanced |
|---|---|---|
| MAD of per-study FPR | 0.132 | 0.127 |
| SD of per-study FPR | 0.254 | 0.213 |

Balancing raised the FPR in many European studies; LifeLinesDeep, for example, went from 0.055 to 0.35. The B4 claim on the FPR scale is therefore weak.

*Resolution:* report the MAD (or SD) of the FPR next to τ for B4. Describe the result as "the East Asian excess was removed, but between-study spread on the FPR scale changed little; FPRs of several European studies rose". Also state that the pooled FPR rose from 0.257 to 0.282 and the median in non-East Asian studies from 0.19 to 0.22.

**M5. The uncertainty for B2 is reported on an unstable scale, and the graphical abstract states the 88% without it.**
The CI of the ratio of a gap in medians (9 East Asian studies) is 41–149%. It is wide because the denominator varies across draws, and an upper bound above 100% is not meaningful. The absolute gap reduction is well determined: 0.46, study-clustered 95% CI 0.20–0.58 (region-stratified 0.19–0.59). The level-matched reduction is 85%.

*Resolution:* report the absolute gap reduction with its CI as the primary uncertainty, keeping the ratio CI as secondary, and add the level-matched estimate. In combination with M1, the abstract should not state "88%" without qualification.

## MINOR concerns

1. **H4/G4 population set.** The within-site burn-in tests (v5 H4, v6 G4) use the full set, not the strict set: `r` in analyse_v5.py, and `R` (full) in run_gmwi2.py. They include colonoscopy-referral, case-control and mother–infant controls (YachidaS_2019, JieZ_2017, QinJ_2012, MetaCardis_2020_a, ShaoY_2019), and antibiotic users. This is allowed by the plan, but the text presents the "13 populations" next to the strict atlas. *Fix:* state that H4/G4 use the full set. Report that the burn-in did better in 74.6% of the 646 units, and give a random-split noise floor so readers can judge how close 0.038 is to the best achievable value.

2. **"Price of recalibration" framing.** In deploy_v4_cc_summary.csv (N = 100) the training cut-off gives FPR 0.288 and sensitivity 0.464. A clean burn-in (π = 0) gives FPR 0.098 and sensitivity 0.246, the same as 100 labelled controls (0.246). With 1–10% patients, sensitivity is 0.206–0.227. Most of the "fall from 0.46" is therefore the cost of bringing the FPR from 0.29 down to 0.10, a property of the ROC curve and not of the unlabelled rule. Contamination itself costs 0.02–0.04. The analysis also rests on 3 populations and 6 units. *Fix:* rephrase, and state the n.

3. **Verification power.** "Detects … observed FPR > 0.25 with probability 0.98" is the average power over atlas pairs, treating the observed FPRs (noisy, and biased upward in the tail) as true values. The power at exactly FPR 0.25 with n = 100 is 0.79, and at 0.30 it is 0.97. *Fix:* report the power curve at fixed true FPRs. Call the 0.98 and 0.72 figures averages over atlas pairs.

4. **Burn-in guarantee and its test.**
   - The "exact Beta law" and "expected FPR ≤ α" hold for an all-healthy burn-in with continuous scores. With patients present, the π_max rule protects only if the realised number of patients is at most π_max·N. With random sampling at prevalence π_max, it exceeds that about 26% of the time at N = 100, π = 0.01.
   - test_contamination_bound places the patient far above the healthy scores, which is the benign case. A patient scoring below the healthy people lowers the cut-off and is the case the bound must survive.
   - *Fix:* state the conditions in the text. Add unit tests for the adversarial case (patients at the low end) and for random binomial contamination.

5. **Holm details.** holm_v6_v13.json says "0 of 2000 bootstrap draws", but run_gmwi2.py used 5,000 draws for G4, so the bound is P < 2 × 10⁻⁴. G1 has no P value, and plan v6 listed Holm "over G1–G4". Say which tests the Holm family contains.

6. **Labelling.**
   - The within-training-data analysis of GMWI2 (0–84% range, I² = 0.96, Figure 2A) is not in plan v6. Label it post hoc.
   - Plan v6b was written after that exploration. Say "pre-specified after exploratory analysis of the published scores".
   - The Fisher P < 1e-300 for the case-mix table treats samples as independent. Drop it, or give a study-level test.

7. **Decomposition reporting.**
   - The largest contributor is *Lachnoclostridium* (−0.155), not *B. plebeius* (−0.083).
   - The fourth largest is *Clostridium* sp. CAG_167 (−0.063), a "healthy"-weighted taxon that is absent from East Asian guts. The text omits it.
   - The top 5 taxa account for only 35% of the negative contributions.
   - *Fix:* list the taxa in order and state the 35%.

8. **Pooled versus within-study AUROC.** Both bootstraps hold the trained models fixed and resample only the held-out predictions, so training variability is not included. State this.

9. **Figure 2B.** The title is "Healthy populations it never saw", but the panel plots 55 full-set populations including seen ones. The text describes 15 strict unseen populations. Either retitle the panel or show the 15 unseen strict populations, with the seen ones marked.

10. **Figure 3.** The legend omits panel D (sensitivity). The panel B title "Burn-in better in 28/28" should note that it uses the full-set populations.

11. **"Sampling noise alone would put 15–16% outside 0.05–0.15; observed 50–97%".** This mixes miscalibration of level with between-population spread. For example, IGT-LASSO has a pooled FPR of 0.42 and IGT-RF 0.008. *Fix:* also report the out-of-band share around each classifier's own pooled FPR, or point to I² as the spread measure.

12. **Stated GMWI2 FPR.** α is the training-sample FPR, inflated by the East Asian training studies. It is not a figure the developers published. The G2 "miscalibration" is driven mainly by low-FPR populations: 8 of the 12 out-of-band populations lie below 0.104. Say so, so that readers do not read G2 as "GMWI2 over-flags new populations".

## Numbers I could not reconcile, or that are inconsistent

1. SI S6.1 says α is "the share of the developers' 5,547 healthy training samples below the cut-off". The value 0.2084 is computed on the 5,514 healthy people in the 44 studies with at least 20 (gmwi2_published_training.json, pooled_fpr = alpha). The main text is right; the SI is not.
2. Main text: "Restricting to the 16 classifiers with AUROC ≥ 0.65 … with 62% of populations outside the band." 0.620 is the **median** across the 16 classifiers. The mean is 0.648, and the pooled share over all pairs is 0.649. Say "median 62%".
3. holm_v6_v13.json: "0 of 2000 bootstrap draws". run_gmwi2.py used 5,000 draws for G4.
4. SI S6.5 / main text: v6c "gives each country equal total weight as well". The code gives weight inversely proportional to country size (M2).
5. Main text: "Weighting … so that, within each country, healthy and non-healthy people carried equal weight". The code equalises every country × label cell (M1).

All other numbers I checked match the result files: about 60 values across v5_summary, numbers_v11, h4_cluster_ci_v11, gmwi2_*, v6b_*, corrected_boot_v13, holm_v6_v13, deploy_v4_cc_summary and control_augmentation_v4.

## Do the conclusions follow?

- **Supported:**
  - the FPR at a fixed cut-off is population-dependent (atlas H1, GMWI2 G1/G2);
  - a published index mislabels East Asian healthy people at high rates in its own training data;
  - within-site recalibration works on non-random within-cohort splits, at the stated sensitivity cost;
  - verification on local healthy people is feasible.
- **Partly supported:** "pooled training turns a region's normal microbiome into a disease signal". The retraining shows that geographically unbalanced pooled training produces the gap and that reweighting removes it. The ablation (M1) shows that the case-mix part, label imbalance within country, explains only about half of it. The title and section headings can stay if the mechanism text is corrected.
- **Not supported as written:**
  - the main-text v6c paragraph (M2);
  - "error mostly specific to the pairing" without the H2 failure and the sampling-noise correction (M3).
