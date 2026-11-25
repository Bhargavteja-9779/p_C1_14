# Statistical review, round 13: manuscript v15 (iMeta Letter)

**Reviewer 1 (methods and statistics)**

**Score: 7.5/10. Recommendation: minor revision.**

## Summary

v15 is much shorter than v14, and the statistics behind it have not changed. I re-derived almost every number in the
main text from the result files, and they match. The number audit (scripts/audit_numbers.py) gives 109/109 matched,
and the fprcal tests pass (13/13). Four of the six round-12 statistics items are fixed in both text and code. The
other two (round-12 minors 5 and 6) were not answered.

Making the text shorter has caused two problems that need fixing before acceptance. First, the new title says that
"the same test" flags 0–77% of healthy people. No single test does that: 0–0.77 is the range across all 14 LASSO tests.
Second, the sentence and Figure 3A legend behind the headline −62% list a sex split that is not in the analysis.
The sentence also no longer says that this analysis used the full set (populations with ≥ 120 people), which v14 said.
Both need text changes only, with no new analysis. Neither changes a conclusion, but the title is the claim readers
will repeat.

## Checks performed (scratch work in /tmp/claude-0/r13_stats/; no repository file changed)

- **Atlas (v5_het_strict.csv, v5_perpop_strict.csv, v5_summary.json).** 489 LASSO pairs: 45% above 0.15, 24% below 0.05.
  FPR range for n ≥ 100 (LASSO) was 0–0.770. I² median 0.937, range 0.64–0.97, 28/28 (full set 28/28, median 0.92).
  Expected share outside 0.05–0.15 was 14.8–16.2%; observed 50–97%. LASSO upper PI 0.218 (CRC) to 0.809 (IGT). CRC
  LASSO pooled FPR 0.058. Spearman ρ = −0.060, P = 0.763. AUROC ≥ 0.65: 16 classifiers, I² median 0.942. 7 classifiers
  below 0.6, 3 below 0.5. All match.
- **Variance decomposition (h2_sampling_v13.json).** LASSO: population 17.4%, classifier 20.8%, sampling 14.2%, pair
  net 47.6%. RF: population 7.5%. The text's "inconclusive for LASSO, falsified for RF" matches the plan v5 grading
  (WRONG < 10%). Round-12 minor 4 is fixed.
- **GMWI2 (gmwi2_results.json, gmwi2_published_training*.json/csv, gmwi2_eastasia.json, posthoc_eastasia_strict_v15.json,
  holm_v6_v13.json, gmwi2_casemix.json, numbers_v14.json).** α = 0.208. Training studies: 0–0.84, I² 0.96, eight
  studies above 50%, all from China or Japan. East Asian median 0.64 vs 0.12, P = 5.3e-7. African studies 0–7.3%.
  Unseen strict set: 15 populations, 1,914 people, QC r = 0.991, range 0–0.54, 80% outside band vs 9% expected,
  Holm P = 1.8e-12. Using the per-study rows of Table S9, I counted 8 populations below the band (LifeLinesDeep 0.100 is
  below 0.104) and 4 above it. Strict East Asian comparison: 0.38 vs 0.06, P = 0.020; full set 0.38 vs 0.20,
  P = 0.065. G3 P = 0.72. Top five taxa = 38.9% of the score gap. Prevalences: B. plebeius 72/17%, CAG_167 2/28%,
  Klebsiella 59/22%. Case mix: 1,574/2,522 vs 1,097/5,547, OR 6.74. All match.
- **Retraining v6b (v6b_results.json, corrected_boot_v13.json, posthoc_v6b_withincountry.json).** Gap 0.524 → 0.065;
  relative reduction 87.7%; corrected CI 41–149% (the text correctly uses the corrected CI, not the 54–121% in
  v6b_results.json). τ 1.158 → 0.809. FPR-scale MAD 0.132 vs 0.127. Balanced East Asian median 0.289. AUROC
  0.715 → 0.676. Within-country variant: 37% (absolute 0.19, CI −0.04 to 0.31). 10,986 people, 61 studies. All match.
- **Site-level work.** H4: 0.1008 → 0.0382, −62%, population-clustered CI 51–70%, 13/13, 28/28 (h4_cluster_ci_v11.json).
  G4: 0.211 → 0.044, −79%, CI 64–85%. Sensitivity price (deploy_v4_cc_summary.csv, N = 100): training cut-off has
  FPR 0.289 and sensitivity 0.464. Burn-in sensitivity is 0.246 with no patients and 0.227/0.218/0.206 with 1/5/10%
  patients. 100 labelled controls give 0.246. All match.
- **Burn-in, conformal and PAC maths.** N = 100, α = 0.10: k = 91, Beta(10, 91), P(FPR > 0.15) = 0.0551, E[FPR] = 0.099.
  Binomial check with n = 100 and H0 FPR ≤ 0.15: critical count 22, size 0.039; power is 0.35/0.79/0.97 at a true
  FPR of 0.20/0.25/0.30. Atlas mean power for pairs with observed FPR > 0.25 is 0.982 (verify_power_v5.json). The k
  formula and the exchangeability statement are correct.
- **Round-12 items.** m1 (strict vs full East Asian): fixed. m2 (Fisher P in SI S6.4): fixed, and the reason is given.
  m3 (direction of G2): fixed, but see minor 1. m4 (H2 wording): fixed. m5 (within-country weighting keeps
  single-label countries at full weight): not addressed; the round-12 response table does not list it, and SI S6.6 is
  unchanged. m6 (band α/2–1.5α not stated): not addressed.
- **Code reading.** I read analyse_v5.py (H4 block, lines 48–70), run_gmwi2.py (G4 block), deploy_v4.py (sex split) and
  h4_cluster_ci_v11.py. These give the two major concerns below.

## MAJOR concerns

1. **The title claims more than the data show.** "The same gut-microbiome test flags 0–77% of healthy people" reads as
   one test spanning 0–77%. In v5_perpop_strict.csv (n ≥ 100), the 0–0.77 range covers all 14 LASSO tests. The highest
   value is IGT LASSO (0.77), whose own range is 0.09–0.77. Tests whose range starts at 0 reach at most 0.50 (ME/CFS
   LASSO). The graphical-abstract wording ("the same cut-offs of 28 disease classifiers flagged 0% to 77%") is correct;
   the title, which is new in v15, is not.
   *Fix:* reword the title so it is not about a single test (for example "Fixed cut-offs of gut-microbiome tests flag
   0–77% of healthy people, depending on the population"). Or quote a range for one named test with its sample-size rule
   (for example IGT, 9–77% in populations of ≥ 100 people).

2. **The headline within-site result (−62%, Figure 3A) describes splits and populations it does not use.** The main text
   says the burn-in came from "the first 100 in accession order, or the younger, leaner or one-sex half". The Figure 3
   legend lists "accession order, age, body-mass index, sex". In v5_h4_units.csv, the 646 evaluations are accession 346,
   age 136 and BMI 164. There is **no sex split**. analyse_v5.py loops only over ["age", "BMI"]. Sex splits exist only in
   the three-test v4 analysis (deploy_v4.py, SI S4). Also, H4 and G4 run on the **full** set with n ≥ 120 (analyse_v5.py
   uses `r`, not `strict(r)`; run_gmwi2.py says "full set, n>=120"). Two of the 13 H4 populations, MetaCardis_2020_a and
   ShaoY_2019, are not in the strict set at all. v14 said "with at least 120 people in the full set"; v15 dropped this.
   As a result, "13/13 populations" now reads as part of the 36 strict populations. The legend's "12–13 populations" is
   also wrong for T2D (LASSO and RF: 11).
   *Fix:* in the text and legend, give the three splits actually used (accession, age, BMI). Say "13 populations of the
   full set with ≥ 120 people", and the same for G4. Change "12–13" to "11–13".

## MINOR concerns

1. **"Eight of these twelve" has nothing to refer back to.** The paragraph gives 80% of 15 but never says 12. Write
   "Of the 12 populations outside the band, eight fell below it and four above it".
2. **The prediction-interval range is LASSO-only but is not labelled.** "0.22 (CRC) to 0.81 (IGT)" follows a sentence
   about all 28 classifiers. Across all 28, the lowest upper bound is 0.11 (hypertension RF) and CRC RF is 0.14. Add
   "for LASSO".
3. **"Looked well calibrated (CRC 0.06)".** A pooled FPR of 0.058 is 42% below the 0.10 target. Write "close to or
   below target" instead.
4. **"Within-country case mix and overall geographic make-up therefore both contribute" goes slightly too far.** The
   within-country variant's absolute reduction has a study-clustered CI of −0.04 to 0.31, which includes zero. Give the
   CI, or write "may also contribute". Round-12 minor 5 is still open: in the "within" arm, single-label countries
   (NLD, ISR and others) keep full naive weight. Add one line to SI S6.6.
5. **Band definitions (round-12 minor 6, not addressed).** 0.05–0.15 and 0.10–0.31 are both α/2 to 1.5α. Say so once,
   so readers do not take them for confidence intervals.
6. **Sidedness.** P = 0.020 and P = 0.065 are one-sided (`mw_p_greater`). State this. The G3 and training-data
   Mann–Whitney tests should also state their sidedness.
7. **H2 threshold, net of sampling noise.** The plan defines the share as a share of "total between-unit variance". Net
   of sampling noise, the LASSO population share is 20.2% (h2_sampling_v13.json, net_shares.pop), which is exactly at
   the threshold. "Inconclusive" is the right verdict, but give both definitions in SI S2.1.
8. **The covariate adjustment refers to an earlier analysis.** "Adjusting for age, sex, body-mass index and sequencing
   depth left a population effect" comes from the v4 CRC/IBD/T2D analysis (SI S2), not the 28-classifier atlas. Say
   "(in the three-test analysis)".
9. **Mixed pre-specified and post hoc labels.** H4's criterion (≥ 75% of tests better) was pre-specified. The
   population-clustered CI and the 13/13 count were added in review round 9 (h4_cluster_ci_v11.py header: "POST HOC").
   Mark the CI as post hoc.
10. **B3 wording.** "Beyond our pre-stated margin" describes the point estimate (−0.040). The CI (−0.12 to +0.02)
    includes values within the margin. Write "point estimate beyond".
11. **The 98% from the binomial check is a model-based average.** It treats each pair's observed FPR as the true value.
    SI S2.1 says this; the main text should say "on average".

## Numbers that did not match

None of the numbers themselves were wrong; the audit gave 109/109. The mismatches are in what the numbers are said to
describe:
- Title: "the same test … 0–77%" (single-test ranges are narrower; major 1).
- Main text and Figure 3 legend: a "one-sex half" or "sex" split is not among the 646 evaluations (major 2).
- Figure 3 legend: "12–13 populations"; T2D has 11 (major 2).
- "0.22 (CRC) to 0.81 (IGT)" is LASSO only (minor 2).

## Do the conclusions follow?

Yes, once the text is corrected. Population dependence of the FPR, the GMWI2 training-data artefact, the retraining
result (now correctly hedged) and within-site recalibration at the stated sensitivity cost are all supported and
reproducible. The required changes are wording changes to the title, one results sentence and two legends.
