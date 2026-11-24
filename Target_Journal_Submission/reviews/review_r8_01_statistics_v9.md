# Round 8 statistical review: manuscript_v9 (iMeta Short Communication)

**Score: 7/10. Decision: minor revision.**

**What I checked.** I traced every headline number to the v4 result files, including the heterogeneity statistics and prediction intervals, A2/A3/A5, the covariate models, the taxon ρ (recomputed), the burn-in designs, the contaminated pools, PPV and the Holm table. Nearly all match. The heterogeneity conclusion holds up (I² 0.70–0.95, Q P ≤ 5×10⁻⁹, unchanged at r > 0.95). Deviations and post hoc analyses are disclosed well.

## Concerns

1. **MINOR: related cohorts are counted as independent populations.** De-duplication removed 60 DhakanDB_2019 copies of GuptaA_2019 and the JieZ_2017 copies of QinJ_2012 (Table S7). Even so, four of the "five most over-flagged IBD populations, all Asian" are these two same-lab or same-centre pairs: GuptaA 0.62, DhakanDB 0.40, QinJ 0.41, JieZ 0.34. That is about three independent sources, not five; the limitations name only TettAJ. *Resolve:* state the relatedness of these pairs, reword the claim to "three sources", and add a sensitivity analysis that collapses related cohorts. The I² and prediction intervals will not move much.

2. **MINOR: one pair carries the augmentation mechanism claim.** The highlight "most when the same population was in the pool" and the sentence "in our data it depended on whether the pool contained the same population" rest on one n = 29 cohort (GuptaA). Its pool partner, DhakanDB, is from the same lab and shared about 60 profiles with it. "Same population" cannot be separated from same lab and same processing, or from residual relatedness (the near-duplicate r distribution has no gap). *Resolve:* test it formally, for example by comparing the augmentation gain for populations with and without a same-country cohort in the pool. If that is not done, call it a single observation.

3. **MINOR: the augmentation results are reported selectively.** Per classifier (`control_augmentation_v4.csv`), augmentation also improved T2D LASSO (0.113 → 0.082) and worsened CRC RF (0.065 → 0.072). The text reports only the IBD gains and the CRC LASSO and T2D RF losses. Also, Burn-in vs augmentation at N = 100 gives aug_mad = 0.0635 (`h2h_v4.json`), which rounds to 0.063; the text says 0.064. *Resolve:* report all six classifiers and correct the rounding.

4. **MINOR: the within-site claim should rest on the pre-specified design.** The "57%, P = 0.0007" result is a post hoc grouping, formed after pre-specified H-NX1 failed (48%). However, the pre-specified accession-order design survives Holm on its own (raw P = 0.0007, adjusted 0.022). *Resolve:* lead with the accession result, and keep the post hoc pooled figure secondary. Also report that NX1_pooled at N = 50 survives Holm (0.005). It is in the family but not in the text.

5. **MINOR: a one-sided test is used for a post hoc direction.** The post hoc T2D non-westernised test uses `alternative="greater"` (`hypotheses_v4.py` l.28), but the direction was chosen after seeing the data. *Resolve:* report it two-sided (P ≈ 0.0006). It still survives Holm.

6. **MINOR: the A5 benchmark is built to succeed.** The 79% for "local labelled controls" comes from random splits of the same population, which is exchangeable by construction. It is an oracle, not a fair competitor. *Resolve:* say explicitly that 79% is an exchangeable benchmark. The informative number is the absolute 46%.

7. **MINOR: the PPV and FP/1000 figures are framed as screening results.** The SRC FPR of 0.29 comes from three locked case–control cohorts, two of them T2D. The pooled PPV (1.6% → 2.6%) and "285 → 86 per 1,000 screened" are placed next to CRC screening, but these cohorts' FPR is far above the strict-set CRC pooled FPR of 0.06. *Resolve:* report the figures per disease or drop the screening framing.

8. **MINOR: the oral-taxa share is reported only for IBD.** "Oral taxa <3%" is true for the IBD populations (0–2.5%). For the most over-flagged CRC population (LokmerA_2019, Cameroon), the oral share of the positive shift is 23%; *Resolve:* report the oral share per test.

9. **MINOR: the strict set is applied inconsistently.** Colonoscopy-referred controls (Zeller, Vogtmann, Hannigan) are excluded, but YachidaS_2019 (Japan, 0.47 IBD) stays in. Its controls were also examined at colonoscopy. *Resolve:* justify keeping it, or run a sensitivity analysis without it.

10. **MINOR: the graphical abstract uses small-cohort extremes.** "0% to 62%" comes from n = 20–29 cohorts. Use the n ≥ 100 range (0.4–61%), or say that the extremes come from small cohorts.

**Leakage:** I found no leakage into the classifiers. Training cohorts are excluded (`common_v4.py`), and the CRC contaminated pools use a development-only model.
