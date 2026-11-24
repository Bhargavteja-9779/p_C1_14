# Review round 5 (manuscript_v6) — Statistical referee

**Score: 7/10. Decision: MINOR REVISION.**

All main-text numbers I checked match the v4 result files. The atlas result is sound. Round-4 citation fixes were made, but most other round-4 concerns were not addressed. My check scripts are in /tmp/claude-0/r5_stats/.

## Concerns

**1. MAJOR — The Holm paragraph still mislabels a survivor and contradicts the text.** Lines 241–242 call adj. P = 0.022 "the pre-stated within-site design". In holm_v4.csv it is "BURN-SRC NX1 pooled", which includes the cross-site sub-site transfers. Lines 189–190 say this same pooled hypothesis "is not supported" (48% < 50%). The strict-set survivor (0.0098) is a random-split comparison in which the BURN arm does not depend on the data (lines 166–167). It shows that the training cut-off is miscalibrated, not that the burn-in works. *What would resolve this:* relabel both survivors as stated in round 4.

**2. MAJOR — "Within a site, the burn-in held" is not a stress test (round 4 concern 2, not addressed).** From deploy_v4_units.csv at N = 100, the BURN error is 0.034 for accession order, 0.031–0.034 for the covariate halves and 0.033 under random splits. The Highlight also says the 57% came "when the case mix shifted". No design changed the case mix: these are healthy-only age/BMI/sex/accession splits. *What would resolve this:* report the random-split benchmark beside each design and drop "case mix".

**3. MAJOR — The graphical abstract mislabels the A5 local arm.** Panel 2 says "100 local unlabelled people". The text (line 138) and r3_a5_fair.csv describe 100 *labelled* local controls (π = 0). 79% is therefore set by N and M, not an empirical win. The comparison is post hoc with no inference, yet the panel title reads "Only local calibration fixes it". *What would resolve this:* correct the label, mark the panel post hoc, and add the population-level test (8 populations) to the Holm family.

**4. MINOR — The Holm family still breaks its own rule.** The within-site Wilcoxon (P = 0.0007, line 180) is a correction-versus-cut-off test in the main text, but it is not in Table S10. A5 has no test either. *What would resolve this:* add both, or state the exclusions.

**5. MINOR — There are residual sub-threshold duplicates between GuptaA and DhakanDB.** I recomputed species-level log-profile correlations after de-duplication. DHAK_HCJ, which is retained and scored as a healthy population, has r = 0.970 with GupDM_HCR, a CRC training control. (unrelated cohorts: ≤ 0.70). GupDM_HDB has r = 0.983 with DHAK_HBR, a removed copy of GupDM_HBR. The text still presents "India 0.62" and the augmentation repair "0.62 → 0.03" without n (29) or a lab/batch caveat. *What would resolve this:* re-screen at r > 0.95, report n and CIs, and frame the repair as same lab/batch, not "same population".

**6. MINOR — The augmentation comparator is not matched to the primary set.** The pool and the evaluation use the full set (29 locked populations). The text does not say this, and it is not labelled post hoc in the main text. *What would resolve this:* rerun on the strict set only, or disclose the mismatch in the text and in Table S6.

**7. MINOR — The Highlights over-generalise.** The T2D non-westernised excess holds for LASSO only (RF −0.010, P = 0.37) and was a post hoc test. Line 19 omits both qualifiers. *What would resolve this:* write "T2D LASSO test (post hoc)".

**8. MINOR — The shift–FPR ρ is partly built in.** Both summarise the same score distribution, yet the text says "closely". *What would resolve this:* add one sentence saying so.

**9. MINOR — Small-k presentation.**
- Figure 3B shows a "population-resampling" 95% CI for 2 studies.
- The PPV (1.6% → 2.6%) pools one CRC cohort and two T2D cohorts, but is framed for CRC screening.
- The T2D contaminated cohorts are called "locked".
- Under the BMI and age halves, the burn-in's P(FPR > 0.15) (0.16, 0.17) exceeded the training cut-off's (0.12, 0.18 respectively). This is not mentioned.

*What would resolve this:* drop the CIs for k ≤ 3, report the PPV for the CRC cohort alone, and fix the labels.

## Verified
Heterogeneity statistics, PIs, band shares, the n ≥ 100 ranges, A2/A3, augmentation, the stress designs, A5, the contaminated results, PPV and the Holm arithmetic.
