# Statistical review, round 6 (manuscript_v7)

**Score: 7/10. Decision: MINOR REVISION.**

I checked the main-text numbers against the result files (summary_v4.json, heterogeneity, hypotheses, holm_v5, augmentation, covariates, taxa_shift, PPV, contaminated burn-in; scripts in /tmp/claude-0/r6_stats/). All the numbers I checked match. The round-5 fixes are in place: Holm labels, "labelled" in the graphical abstract, "case mix" removed, the ρ caveat added. I found no leakage: burn-in and evaluation draws are disjoint, scored populations were never used to train the classifier, and de-duplication is documented.

## Concerns

**1. MAJOR: "Within a site, the burn-in held" rests on mean absolute error only. The tail and bias endpoints show it did not fully hold.** In summary_v4.json at N = 100:
- Covariate halves: BURN mean FPR is 0.106 (95% CI 0.101–0.112), so the CI excludes α = 0.10. P(FPR > 0.15) is 0.135 for both BURN and the training cut-off (SRC).
- Pre-stated pooled design (NX1): BURN P(FPR > 0.15) is 0.158, compared with 0.136 for SRC. On this tail endpoint the burn-in is worse than the training cut-off.

These are not reported. The mean-absolute-error gain largely reflects SRC erring in both directions (CRC tests too strict), not robustness to within-site shift.
*What would resolve this:* report mean FPR and P(FPR > 0.15) for BURN and SRC next to each within-site mean-absolute-error figure. State that the burn-in exceeded α slightly but significantly under covariate shift. Change "held" to "reduced the average error but not the tail risk".

**2. MINOR: The Holm family is defined by what was reported, not by what was tested.** Table S10 leaves out post hoc tests that were run: A3 IBD LASSO/RF and T2D RF in the strict set (P = 0.56, 0.67, 0.37), T2D LASSO in the full set (0.009), ALIGN−SRC (0.078), and the separate covariate (0.016) and accession (0.0007) Wilcoxons. The A5 country-versus-local contrast still has no test. The T2D LASSO "survivor" was picked from four post hoc contrasts. Its RF counterpart is null (−0.010), which the main text omits.
*What would resolve this:* include every post hoc P value computed, or list the exclusions in S10. Add "(RF: no difference, P = 0.37)" to the T2D sentence.

**3. MINOR: The A5 comparison is near-tautological and has no inference.** The 100 labelled local controls are evaluated on an exchangeable split of the same population, so their 79% is set mostly by N and M. The 46 pairs come from 8 correlated populations, yet this is the headline panel of the graphical abstract.
*What would resolve this:* add a population-level test with a CI, and label the local arm as an exchangeable benchmark.

**4. MINOR: A small-n headline population.** "India 0.62" rests on n = 29 and has residual similarity to DhakanDB (round 5). Give n and the CI wherever 0.62 appears, and frame the augmentation repair as possibly same-lab/batch.

**5. MINOR: The section title overgeneralises.** "WHY: Health markers of the training population are rarer elsewhere" fits IBD. For T2D and CRC, the top contributors are mostly taxa that are *more* abundant (Enterobacteriaceae, *Escherichia*, *Prevotella*, *Veillonella*). "WHY" also implies causation that the text itself disclaims.
*What would resolve this:* use a descriptive title, for example "Which taxa shift the scores".

**6. MINOR: Spectrum bias in the PPV.** Sensitivity from three case–control cohorts of diagnosed patients, applied at 1% prevalence, makes the PPV of 1.6% → 2.6% optimistic. State this.

**7. MINOR: Related studies are treated as independent.** TettAJ_2019_a/b/c enter as separate populations, while MetaCardis (three countries) enters as one. The I²/PI and the A2 CIs assume independence.
*What would resolve this:* a sensitivity analysis that collapses related studies, or a sentence acknowledging this.

**8. MINOR: The augmentation contrast uses different people in each arm.** In the burn-in-versus-augmentation contrast (4/7 populations, P = 0.22), the arms are scored on different subsets of people. Say so where the CI (−0.076 to −0.007) is quoted, because the CI and the sign test disagree.

## Overall
The numbers are reproducible, and the labelling of pre-specified versus post hoc results is now mostly honest. The remaining substantive issue is concern 1: "held within sites" rests only on mean absolute error, and the bias and tail endpoints, which are less favourable, are not reported.
