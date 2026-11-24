# Review round 4 (manuscript_v5) — Statistical referee

**Score: 7/10. Decision: MINOR REVISION.**

I checked every main-text number against the v4 result files and found no mismatches. The numbers I checked were the heterogeneity statistics, prediction intervals, n ≥ 100 ranges, covariate ICCs, A2/A3, the taxon ρ (recomputed: 0.76/0.91/0.90), the stress tests, ALIGN, augmentation (recomputed: 0.087/0.078), the contaminated burn-in, PPV and Holm. Git history shows protocol_v4.md committed (03:56) before the first v4 result (03:57). The round-3 post hoc analyses (r3_posthoc.py) are labelled post hoc. The atlas finding (I² 70–95%, PI up to 1–63%) is sound. My check scripts are in /tmp/claude-0/r4_stats/.

## Concerns

**1. MAJOR — Two of the three Holm "survivors" are still framed as evidence for the burn-in, which they are not.** The text (lines 162–166) now says random splits show only that the training cut-off is miscalibrated. The Holm paragraph (lines 230–233) still lists "burn-in versus training cut-off in the strict set (adj. P = 0.0098)" as a result. That P is a random-split comparison, and the BURN arm there does not depend on the data (11/11, the smallest P an exact Wilcoxon can give). The second survivor, "the pre-stated within-site design (0.022)", is "BURN-SRC NX1 pooled" in holm_v4.csv. That pool includes the cross-site sub-site transfers, which is the same mislabel as round-3 concern 2. *What would resolve this:* label the first survivor as evidence of training cut-off miscalibration. Call the second "the pre-stated H-NX1 pool (within-site designs plus sub-site transfers)".

**2. MAJOR — The within-site "non-random" designs barely shift the data, so they test the assumption only weakly.** I matched the same population, classifier and N = 100 (stress_vs_random.py). BURN error under accession order was 0.034, against 0.033 under random splits in those 13 populations. Under covariate halves it was 0.033 against 0.027 (7 populations). SRC error was unchanged as well. So accession order behaves like a random split, and age/BMI/sex halves add little. The real stress tests are the cross-site ones (sub-site and neighbour), and the burn-in failed both. The 57%, 12/13, P = 0.0007 result therefore shows that the training cut-off was off within these sites. It does not show that the burn-in is robust to shift. *What would resolve this:* report each design's BURN error next to its random-split benchmark. State that the within-site designs did not induce a measurable shift. Rephrase "the burn-in held" accordingly.

**3. MINOR — The Holm family breaks its own stated rule.** The rule is "every test comparing a correction with the training cut-off… in the main text". The within-site Wilcoxon (P = 0.0007, line 177) is not in Table S10. It would survive (12 × 0.0007 ≈ 0.009), but the family must match the rule. The A2 Spearman CIs and the full-set T2D non-westernised test (P = 0.009) are also outside the family, and the text does not say why. *What would resolve this:* add the within-site test and state the exclusions.

**4. MINOR — The fair A5 comparison has no inference, and the text cites the wrong table.** Lines 133–136 cite Table S9, but the result is in Table S12. The 79% vs 46% comes from 46 pairs in only 8 populations. By test and model, the country reference wins for IBD RF (0.88 vs 0.79) and nearly ties for IBD LASSO (0.75 vs 0.81). It loses badly for T2D LASSO (0.00). A population-level Wilcoxon I ran (post hoc) gives P = 0.008, with 7 of 8 populations favouring the local arm and 1 tie. *What would resolve this:* cite Table S12, report the population-level test and the per-test split, and add it to the Holm family. Also update "Tables S1–S11" (line 246) to S1–S12.

**5. MINOR — The Indian anecdotes rest on n = 29 and an overlapping cohort.** The headline "India 0.62" and the augmentation repair "0.62 → 0.03" both come from GuptaA_2019 (n = 29; 18/29 flagged). DhakanDB_2019, whose controls were added to the augmentation pool, shared 60 duplicate profiles with GuptaA (Table S7). Two cohorts with that much overlap (likely the same research group) suggest more shared people or a shared batch below r = 0.99. The repair may then reflect the same lab or batch rather than the "same population". *What would resolve this:* give n and the CI wherever these numbers appear. State the possible lab/batch confound. Report the maximum remaining cross-cohort correlation between GuptaA and DhakanDB.

**6. MINOR — The augmentation comparator is not matched to the primary set.** control_augmentation_v4.py builds the pool from all DEV healthy cohorts, including non-strict ones. It evaluates on all 29 locked populations, also full set, not strict. Round 3 asked for a strict-only rerun, and it was not done. *What would resolve this:* rerun with strict-only pool and evaluation, or state the mismatch in the text and in Table S6.

**7. MINOR — The Highlights over-generalise.** The T2D non-westernised excess holds for LASSO only (RF: −0.010, P = 0.37), and it was a post hoc test. "Asian populations over-flagged by IBD" is based on the top five populations, with no group test. The decomposition behind "tracks lower abundance" is LASSO-only. *What would resolve this:* write "the T2D LASSO test (post hoc)" and "the five most over-flagged IBD populations were Asian".

**8. MINOR — The shift–FPR correlation is partly built in.** The mean logit score shift and the FPR at a fixed cut-off are both summaries of the same score distribution, so a high ρ is expected. What the decomposition adds is which taxa drive the shift. *What would resolve this:* say this in one sentence, and drop "closely" as evidence for the mechanism.

**9. MINOR — Small samples are presented with precise-looking uncertainty.**
- (a) Cluster bootstraps with 7 clusters (BURN–ALIGN, BURN–augmentation) under-cover. Figure 3B shows a "95% CI from resampling populations" for 2 sub-site populations.
- (b) The PPV (1.6% → 2.6%) pools CRC and T2D cohorts (3 cohorts) but is framed for CRC screening.
- (c) Figure 3A uses 5 populations, and its augmentation line (~0.077) differs from the text's 7-population 0.064.
- (d) The contaminated T2D cohorts are leave-one-cohort-out held-out cohorts, not "locked".
- (e) The sub-site failure relies mainly on MetaCardis_2020_a, which the authors exclude from the primary set as disease-enriched.

*What would resolve this:* drop the CIs for k ≤ 3, report the PPV for the CRC cohort alone, reconcile the populations in Figure 3A with the text, and fix the labels.

## Verified as correct
- Counts.
- Table S2 (all columns).
- Table S5 ranges (−24% to +28%; ICC 15–49%; extended −39% to −50% for IBD).
- A2/A3 values.
- Taxon ρ (recomputed).
- Table S4 stress numbers (48%; 0.30 vs 0.31; 37%).
- ALIGN (−0.012, CI −0.017 to −0.007, 7/7).
- Augmentation means and P = 0.58.
- BURN–augmentation (−0.034; 4/7; P = 0.22).
- Contaminated FPR and sensitivity (0.075–0.087; 0.082 when π_max is mis-specified; 0.21–0.23).
- The burn-in contamination bound k (derivation checked).
- Holm-adjusted values.
