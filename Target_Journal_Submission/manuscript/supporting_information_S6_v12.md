## Supporting Information S6 — External audit of a published classifier (GMWI2)

### S6.1 Model and verification

GMWI2 (Chang et al. 2024 [22]) is an L1-penalised logistic regression on presence (relative abundance > 1e-5) of 95 MetaPhlAn3 clades, with intercept 0 and the decision rule GMWI2 = w·presence; GMWI2 > 0 = healthy. We obtained the model from bioconda (gmwi2 1.6, MIT licence) and read its coefficients with a whitelisted unpickler (code/experiments/atlas/v6/extract_gmwi2.py); they are identical to Supplementary Data 3 of [22] (95/95, max |Δ| 1e-15). Our re-scored GMWI2 on the 704 samples shared with the developers' Supplementary Data 5 correlated with the published scores at Pearson r = 0.991 (same healthy/non-healthy call for 98.4%). The stated false-positive rate is the share of the developers' 5,547 healthy training samples below the cut-off, α = 0.208.

### S6.2 Analysis plan v6 (pre-specified) and outcomes

Plan committed before any score was computed (code/experiments/atlas/v6/protocol_v6.md). Holm over G1–G4.

| Hypothesis | Pre-stated criterion | Result | Verdict |
|---|---|---|---|
| G1 heterogeneity | I² ≥ 0.5 across unseen strict populations | I² = 0.92 (τ 1.06), 15 populations | supported |
| G2 miscalibration | out-of-band share exceeds binomial expectation by ≥ 20 pp | 80% vs 9% expected, P = 6.1e-13 | supported |
| G3 in-sample optimism | seen populations lower FPR than unseen (MW, P<0.05) | seen 0.26 vs unseen 0.20, P = 0.72 | falsified |
| G4 local fix | within-site burn-in lowers mean \|FPR−α\|, clustered CI excludes 0 | 0.21 → 0.04 (−79%, CI 64–85%), 11/13 | supported |

Full set (24 unseen populations): I² = 0.93; out-of-band 67% vs 10% expected (P = 1.9e-13); G3 P = 0.51.

### S6.3 Table S16 — GMWI2 false-positive rate in unseen healthy populations (strict)

| population | n | FPR |
|---|---|---|
| KaurK_2020 | 30 | 0.00 |
| BritoIL_2016 | 152 | 0.03 |
| KarlssonFH_2013 | 43 | 0.05 |
| RubelMA_2020 | 76 | 0.05 |
| Bengtsson-PalmeJ_2015 | 35 | 0.06 |
| RampelliS_2015 | 33 | 0.06 |
| KeohaneDM_2020 | 110 | 0.07 |
| LifeLinesDeep_2016 | 1117 | 0.10 |
| YassourM_2016 | 20 | 0.25 |
| ZhuF_2020 | 77 | 0.27 |
| HansenLBS_2018 | 57 | 0.28 |
| NagySzakalD_2017 | 50 | 0.34 |
| ThomasAM_2018b | 28 | 0.46 |
| YeZ_2018 | 45 | 0.49 |
| LiJ_2017 | 41 | 0.54 |

### S6.4 Analysis plan v6b (pre-specified): geographic case-mix confounding

In GMWI2's training data (Supplementary Data 2 of [22]), East Asian samples are 62% of non-healthy but 20% of healthy samples (Fisher OR 6.7, P < 1e-300). Plan v6b (protocol_v6b.md) retrains a GMWI2-recipe classifier on 10,986 cMD subjects, leave-one-study-out, pooled vs country-balanced sample weights.

| Hypothesis | Criterion | Result | Verdict |
|---|---|---|---|
| B1 mechanism | naive East Asian−other FPR gap ≥ 0.15 | 0.52 (EA 0.71 vs 0.19) | supported |
| B2 intervention | balancing cuts the gap ≥ 50% | −88% (CI 54–121%) | supported |
| B3 cost | balanced pooled AUROC within 0.03 of naive | 0.715 → 0.676 (-0.040, CI -0.12/+0.02) | falsified |
| B4 heterogeneity | balanced τ < naive τ | 1.16 → 0.81 | supported |

Post hoc: within-study AUROC (cases vs controls of the same study, 24 studies) fell only 0.669 → 0.649 (-0.020, CI -0.052/+0.013); much of the pooled-AUROC loss was the geographic shortcut, not within-study discrimination.
