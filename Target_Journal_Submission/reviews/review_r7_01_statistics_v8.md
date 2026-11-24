# Statistical review, round 7 (manuscript_v8)

**Score: 8/10. Decision: MINOR REVISION.**

I checked the main-text numbers against summary_v4.json, heterogeneity_v4.csv, hypotheses_v4.csv, h2h_v4.json, the r3 and r6 post hoc files, holm_v6.csv, the PPV and contaminated burn-in files, and ga_inband.json. Every number I checked matches. These include the pooled FPRs, I², τ and prediction intervals, A2 and A3, augmentation, the within-site, accession, sub-site and contaminated burn-in results, and the PPV.

I found no leakage. Inference is made at the population level, so pseudo-replication is handled. Round-6 concerns 1–3, 5, 6 and 8 have been addressed.

## Concerns

**1. MINOR (closest to MAJOR): the post hoc within-site grouping carries the headline, and the pre-specified result is reported less fully.** The pre-specified H-NX1 pools covariate, sub-site and accession splits. The text reports its 48% reduction (the threshold was 50%), but not two other results:
- Its tail endpoint goes the wrong way: BURN P(FPR > 0.15) is 0.158 versus 0.136 for SRC (summary_v4.json, stress/NX1_pooled/N100).
- Its N = 100 Wilcoxon does not survive Holm (adjusted P = 0.059; holm_v6.csv).

The surviving test cited in the main text ("within-site burn-in, adjusted P = 0.022") is the post hoc regrouping. That regrouping drops exactly the units that failed (the sub-sites). Holm does not correct for choosing the grouping. In the graphical abstract, panel 2 ("same site, 13 populations") also uses the post hoc grouping without a label.

*What would resolve this:* in the Holm paragraph, add "the pre-specified pooled design (NX1) did not survive (0.059), and its P(FPR > 0.15) was 0.158 for the burn-in versus 0.136 for the training cut-off". Label GA panel 2 "post hoc grouping, sub-sites excluded".

**2. MINOR: the neighbour-site test does not match its claim.** The text gives "P(FPR > 0.15) 0.30 versus 0.31; P = 0.57". That P comes from the mean-absolute-error Wilcoxon (stress/neighbour/N100/BURN_minus_SRC_mad), not from a test of the tail endpoint. The text also never says that pre-stated H-NX2 was supported (0.295 > 0.20).
*What would resolve this:* write "(mean absolute error 0.096 vs 0.081, P = 0.57)" or test the tail directly, and state the H-NX2 outcome.

**3. MINOR: the "cost in sensitivity" is framed unfairly.** The training cut-off's sensitivity of 0.46 comes with an FPR of 0.29 in these cohorts, so the halving mostly reflects a move along the ROC curve, not a cost specific to the burn-in. The LAB arm (labelled local controls) has the same sensitivity, 0.245, as BURN (ppv_v4.csv).
*What would resolve this:* in the Highlights and text, say that any cut-off meeting the 10% FPR target, including one from labelled local controls, has this sensitivity.

**4. MINOR: the Holm family is not literally "all P values computed".** It leaves out A1 (χ²), Cochran's Q, and the CIs for the A2 Spearman correlations. Nothing would change.
*What would resolve this:* write "all population-level comparison P values (A1 heterogeneity tests excluded)".

**5. MINOR: there is a stale number in the SI.** The revision-history row v4-1 (si_tables_v4.md) gives "Holm P = 0.125" for ALIGN. holm_v6 gives 0.297 for locked BURN−ALIGN.
*What would resolve this:* regenerate the row from holm_v6.csv.

**6. MINOR: the cluster bootstrap rests on few clusters.** The CIs from 7 populations (for example, mean FPR 0.106, 0.101–0.112) and the one resting on 2 studies (sub-site) are likely anti-conservative.
*What would resolve this:* note this, or add a t-based interval.

**7. MINOR: a post hoc label is missing in the Highlights.** Highlight 2 states that the T2D LASSO test over-flagged non-westernised populations without the "post hoc" label that the main text carries (RF null, P = 0.37).
*What would resolve this:* add "(post hoc)".

**8. MINOR: the headline extreme rests on a small cohort.** The 0.62 figure in the graphical-abstract summary and Figure 1 comes from n = 29. The main text gives n, but the summary paragraph's "0% to 62%" does not.
*What would resolve this:* quote the n ≥ 100 range (0.4–61%), or add n.

## Overall
The numbers are reproducible and the comparators are fair. The remaining issue is emphasis: the "halved error" message rests on a post hoc grouping, and the pre-specified design, which fails Holm and the tail endpoint, should be reported as plainly. The qualitative conclusion does not change.
