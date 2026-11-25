# Statistical review, round 12 — manuscript v14 (iMeta Letter)

**Reviewer 1 (methods and statistics)**
**Score: 8/10. Recommendation: minor revision.**

## Summary

v14 fixes every round-11 statistics item I raised, and I could verify each fix in the text and in the code, not just in
the reply. The two main-text overclaims are gone: the mechanism is now hedged as "both within-country case mix and the
overall geographic make-up", the 88% is out of the graphical abstract, v6c is out of the main text, and the H2 failure is
stated with the sampling-noise split. I re-derived essentially every number in the main text from the result files and
re-ran the three balancing weightings, the variance decomposition (including a full REML with known sampling variance),
the burn-in and conformal maths, the Holm family and the heterogeneity. Almost everything agrees.

Two things keep this at minor rather than accept. First, the one unseen-East-Asian comparison in the main text (median
0.38 vs 0.20, P = 0.065) uses the **full-set** comparison numbers inside a paragraph that is otherwise about the strict
set; the authors' own strict-set version (posthoc_eastasia_strict_v15.json: 0.38 vs 0.06, P = 0.020) was computed after
v14 was committed and is not in the text. Second, a handful of round-11 minors are only half-done (the Fisher P < 1e-300
survives in SI S6.4; G2 is still not described as driven by low-FPR populations). None of these change a conclusion.

The headline results are sound and reproducible: the FPR is population-specific (atlas H1, GMWI2 G1/G2), a published index
mislabels East Asian healthy people in its own training data, retraining reproduces and removes the gap, and the
within-site burn-in works at the stated sensitivity cost.

## Checks performed (scratch code in /tmp/claude-0/r12_stats/; nothing written to the repository)

- **Round-11 fixes, verified in text and code.**
  - M1 (weights). I rebuilt the three weightings from v6b scores (CMD_CACHE=/home/user/p_C1_14/data_cache,
    v6b_variants.py / v6b_an.py). Reproduced the authors' balanced arm at r = 0.99999. Within-country label balance that
    keeps each country's share: gap 0.52 → 0.33, abs 0.19, study-clustered CI −0.04 to 0.31, 37%. Full country×label
    equalisation: gap → 0.065, abs 0.46, CI 0.18–0.58, 88%. Both match posthoc_v6b_withincountry.json exactly. The main
    text and SI S6.6 now describe the weights correctly and the mechanism is hedged. Fixed.
  - M2 (v6c). weights() in run_v6c.py divides by country size twice; v6c is removed from the main text and SI S6.6
    documents the bug. Fixed.
  - M3 (H2). Main text now states the ≥20% population hypothesis failed and gives RF shares; h2_sampling_v13.json
    separates sampling noise. I reproduced its shares (LASSO: pop 17%, test 21%, noise 14%, pair-net 48%; RF: test 46%,
    pop 7.5%, pair-net 25%) and confirmed them with an independent crossed REML carrying the known binomial variance
    (LASSO pair ≈ 0.52 net of noise, RF pair ≈ 0.39). Consistent. Fixed.
  - M4 (logit vs FPR scale). τ claim for v6b dropped; FPR-scale MAD now reported (0.13 both arms); European studies
    flagged more often is noted. Fixed.
  - M5 (B2 uncertainty). Absolute gap reduction 0.46 (CI 0.18–0.58) is reported as primary; 88% is out of the abstract.
    Fixed.
  - Minors: H4/G4 full set stated ("≥ 120 people, full set"); sensitivity price decomposed; verification power called an
    atlas average with lower power at exactly 0.25; low-scoring-patient contamination unit test present and passing;
    Holm note corrected to 5,000 draws; GMWI2 in-training analysis labelled post hoc; taxa reordered by contribution with
    Clostridium sp. CAG_167 included and top five = 39%; SI 5,514/5,547 corrected.
- **Git timing / pre-specification.** protocol_v6 (df2677c 10:22:48) before GMWI2 results (28b2acd 10:25:25); protocol_v6b
  in the same results commit's parent chain before baf7218 (10:31:11); protocol_v6c committed together with its results
  (3fde340) and correctly treated as post hoc. The round-12 strict-set East-Asian post hoc (posthoc_eastasia_strict_v15)
  is in commit 160b884 (13:55), **after** the v14 manuscript (6d88bb9, 13:51) — which is why its numbers are not in the
  text (see below). "Time-stamped internal analysis plans", not "pre-registered", remains the right wording.
- **Atlas (atlas_check.py).** I² median 0.937, range 0.64–0.97, 28/28 ≥ 0.5 (full 0.92); LASSO pairs above 0.15 / 0.25 /
  below 0.05 = 45% / 26% / 24%; FPR 0–0.77 for n ≥ 100; out-of-band expected 14.8–16.2% vs observed 50–97%; upper PI
  0.218 (CRC) to 0.809 (IGT); 7 classifiers AUROC < 0.6 (3 < 0.5); 16 at AUROC ≥ 0.65 with I² median 0.94 and median 62%
  out of band; Spearman ρ = −0.06, P = 0.76. All agree.
- **GMWI2.** QC r = 0.991, 98.4% on 704 samples; α = 0.208 on 5,514 people in 44 studies; G1 I² 0.92, PI 0.018–0.685;
  G2 80% out vs 9% expected, P = 6.1e-13, Holm 1.8e-12; G3 0.257 vs 0.204, P = 0.72; G4 0.211 → 0.044 (−79%, CI 64–85%,
  11/13); training I² 0.96, EA 0.64 vs 0.12, P = 5.3e-7, 657/1,067; case-mix 1,574/2,522 vs 1,097/5,547, OR 6.74. All
  agree. Taxon decomposition: Lachnoclostridium (−0.155) largest, top five 39% of the total gap.
- **Burn-in / conformal / verification.** N = 100, α = 0.10: k = 91, FPR ~ Beta(10,91), P(FPR>0.15) = 0.0551,
  E[FPR] = 0.099; PAC k = 96, P(FPR>0.15) = 0.0004. Binomial check n = 100, H0 FPR ≤ 0.15: critical count 22, size 0.039,
  power 0.35 / 0.79 / 0.97 at true FPR 0.20 / 0.25 / 0.30. verify_power_v5.json: n = 100 mean power 0.98 (>0.25) and 0.72
  (>0.15), max false alarm 0.033. All reproduce. fprcal: 13 unit tests pass (41 s), including the adversarial
  low-scoring-patient test and the atlas-coefficient reproduction.
- **Control augmentation.** 0.087 → 0.078, Wilcoxon P = 0.579 on 29 populations. Reproduces.

## MAJOR concerns

None that block the conclusions. The round-11 majors are resolved.

## MINOR concerns

1. **The unseen-East-Asian comparison in the main text uses full-set numbers in a strict-set paragraph.** The sentence
   reads "The four unseen East Asian populations had FPRs of 0.25–0.54 (median 0.38 vs 0.20 elsewhere; P = 0.065; post
   hoc)". 0.20 and 0.065 are the **full-set** "other" median and P (gmwi2_results / posthoc_eastasia). The strict
   comparison, over the 15 strict unseen populations that the same paragraph is about, is 0.38 vs **0.06**, P = **0.020**
   (posthoc_eastasia_strict_v15.json). The strict version is both more consistent with the paragraph and more significant.
   *Fix:* report the strict-set numbers (0.38 vs 0.06, P = 0.020), with the full set as the check, or state explicitly
   that this one comparison is on the full set. This is cheap — the result file already exists.

2. **Fisher P < 1e-300 survives in SI S6.4.** Round 11 asked for this to be dropped or replaced by a study-level test,
   because it treats the 8,069 samples as independent. The main text correctly now gives only the OR (6.7), but SI S6.4
   still prints "Fisher OR 6.7, P < 1e-300" (gmwi2_casemix.json fisher_p = 5e-304). *Fix:* drop the P in the SI, or give a
   study-clustered statistic. The mechanism is anyway established by the retraining, not by this test.

3. **G2 is still not described as driven by low-FPR populations.** 8 of the 12 out-of-band strict populations lie below
   the band (Table S9), and α = 0.208 is itself inflated by the East Asian training studies. A reader can misread G2 as
   "GMWI2 over-flags every new site". *Fix:* one sentence noting most out-of-band populations are below the band, and that
   α is the (EA-inflated) training rate, not a developer target.

4. **"H2 failed for both models" is slightly stronger than the plan's own grading.** Plan v5 marks H2 WRONG only if the
   population share is < 10%. LASSO is 17% (inconclusive by that rule), RF 7.5% (failed). SI S5 says "inconclusive or
   falsified"; the main text says "failed for both models". This is conservative, not an overclaim, but it is inconsistent
   with the plan and the SI. *Fix:* "inconclusive for LASSO (17%), falsified for RF (7.5%)", or reword to "did not reach
   the pre-stated 20%".

5. **Within-country weighting keeps single-label countries at full weight.** posthoc_v6b_withincountry.py's "within" arm
   uses w = n_c/(L·n_{c,l}); for a single-label country L = 1, so large healthy-only cohorts (NLD 1,580, ISR 900) keep
   full naive weight while only the mixed East Asian countries are balanced. The 37% figure is defensible, but the choice
   is worth one line in SI S6.6, because it is part of why within-country balance alone removes less than half the gap.
   (My region-level balance variant removed 65%; the full country×label scheme 88% — consistent with "both mechanisms".)

6. **G2 "expected" band is an arbitrary ±ratio band around α.** The out-of-band test uses [α/2, 1.5α] both for the atlas
   and for GMWI2. This is fine as a calibration check but is a design choice, not a standard interval; state that the band
   is α/2 to 1.5α so readers do not read it as a confidence interval.

## Numbers I could not reconcile, or that are inconsistent

1. Main text, unseen East Asian: "median 0.38 vs 0.20 elsewhere; P = 0.065". These are full-set values
   (posthoc_eastasia). In the strict set, which the paragraph is about, the comparison is 0.38 vs 0.06, P = 0.020
   (posthoc_eastasia_strict_v15.json). (Minor 1.)
2. SI S6.4 still reports "Fisher OR 6.7, P < 1e-300" for the case-mix table, treating samples as independent. (Minor 2.)

Every other number I checked matches the result files: roughly 70 values across v5_summary, v5_het_strict, h2_sampling_v13,
h4_cluster_ci_v11, verify_power_v5, gmwi2_results, gmwi2_published_training, gmwi2_casemix, gmwi2_eastasia, numbers_v14,
v6b_results, posthoc_v6b_withincountry, corrected_boot_v13, v6b_within_study_auroc, deploy_v4_cc_summary and
control_augmentation_v4.

## Do the conclusions follow?

- **Supported:** the FPR at a fixed cut-off is population-dependent (atlas H1, GMWI2 G1/G2); a published index mislabels
  East Asian healthy people at high rates in its own training data (I² 0.96, 0.64 vs 0.12); retraining reproduces the gap
  and reweighting removes it; within-site recalibration works on non-random within-cohort splits at the stated sensitivity
  cost; local verification is feasible. The burn-in, conformal and PAC maths are correct.
- **Appropriately hedged now:** the mechanism. The retraining shows geographically unbalanced pooled training produces the
  gap and that reweighting removes it; the 37% (within-country case mix) vs 88% (full equalisation) split, which I
  reproduced, is now correctly described as "both within-country case mix and the overall geographic make-up". v6c is out
  of the main text.
- **No remaining unsupported claim.** The outstanding items are the strict-set comparison to insert and three
  SI/reporting tidies.
