# Review r20-01: methods and statistics (Reviewer 1), manuscript v21

**Manuscript:** "Gut-microbiome disease classifiers set for a 10% false-positive rate miss it in most healthy populations" (Letter, iMeta)
**Materials read:** submission_final_v21 (manuscript, SI, highlights, cover letter); result files and scripts in code/experiments/atlas/v4–v7.

## Summary

The Letter scores 28 classifiers at a fixed cut-off in 36 healthy populations, audits two released indices (GMWI2, GMHI), tests a retraining explanation and a within-site burn-in rule. The statistics are mostly appropriate and well documented. Pre-specified and post hoc analyses are labelled with care, and failed hypotheses are reported. Most numbers trace exactly to result files. My remaining concerns are about the new fold-model check, how it is summarised in the main text and cover letter, and a few statements that read stronger than the evidence.

## Number check (46 values traced; all match unless noted)

| Claim (location) | Source | Result file value | OK |
|---|---|---|---|
| 36 populations, 6,525 people | v5 perpop / r19 perpop | 36 studies, 6,525 | yes |
| 70% of pairs outside 0.05–0.15 | posthoc_r19_numbers.json | 0.698 | yes |
| 15–16% expected | recomputed binomial on per-pair n | 0.157 | yes |
| I² median 0.94 | v5_summary.json | 0.9365 | yes |
| FPR range 0–0.87 (n ≥ 100) | r19 refit range_n100 | 0–0.873 (RF, HF) | yes |
| PI upper 0.22 (CRC) – 0.81 (IGT) | v5_het_strict.csv | 0.218, 0.809 | yes |
| Pooled CRC 0.06 | v5_het_strict.csv | 0.058 | yes |
| Spearman ρ −0.06, CI −0.42 to 0.32 | posthoc_r17_numbers.json | −0.060; −0.423, 0.321 | yes |
| Variance: pop 17%, RF 7.5%, net 20.2% | v5_summary / h2_sampling_v13 | 0.1735, 0.0749, 0.2023 | yes |
| Fold check: 70% (LASSO 67%, RF 73%) | posthoc_r19_numbers.json | 0.698; 0.667; 0.730 | yes |
| Fold check: 26/28 I² ≥ 0.5, median 0.92 | posthoc_r19_foldmodel.json | 26; 0.924 | yes |
| > 0.15: 36% → 27% | posthoc_r19_numbers.json | 0.363 → 0.268 | yes |
| > 0.25: LASSO 26→15%, RF 16→13% | posthoc_r19_foldmodel.json | 0.260→0.153; 0.162→0.131 | yes |
| Fatty liver 0.26→0.01; IGT 0.42→0.29 | same | 0.256→0.005; 0.419→0.289 | yes |
| Pair Spearman 0.85; AUROC–τ 0.23 (P 0.23) | same | 0.853; 0.233 (0.232) | yes |
| In-sample FPR median 0.4%, range 0–14% | same | 0.0044; 0–0.142 | yes |
| Scores reproduced to 9 × 10⁻¹⁶ | same | 8.9e-16 | yes |
| LASSO mean shift −0.06 | recomputed from perpop | −0.064 | yes |
| GMWI2 training FPR 20.8% | gmwi2_published_training.json | 0.2084 | yes |
| Per-study 0–84%; 8 studies > 50%, all CHN/JPN | same | 0–0.843; 8 | yes |
| EA 0.64 (13) vs 0.12 (31), P = 5 × 10⁻⁷ | gmwi2_eastasia.json | 0.636, 0.124, 5.3e-7 | yes |
| G2: 12/15 outside, 9% expected, Holm 2 × 10⁻¹² | gmwi2_results / holm_v6_v13 | 0.80; 0.090; 1.8e-12 | yes |
| Unseen EA 0.25–0.54 vs 0.06; P 0.020 / 0.065 | posthoc_eastasia_strict_v15 | yes | yes |
| G4 0.21 → 0.04 (−79%, CI 64–85%) | gmwi2_results.json | 0.211→0.044; 0.637–0.850 | yes |
| GMHI 0.67 vs 0.21, P = 0.0007 | gmhi_results.json | 0.673, 0.205, 6.7e-4 | yes |
| GMHI overlap 83%; unshared P = 0.10 | posthoc_gmhi_gmwi2_overlap | 0.825; 0.10 | yes |
| Profiler shift 23% → 43%; r 0.795 | posthoc_gmhi_matching | 0.227→0.433; 0.795 | yes |
| Case mix 62% vs 20%, OR 6.7 | gmwi2_casemix.json | 0.624, 0.198, 6.74 | yes |
| Five taxa explain 39% | numbers_v14.json | 0.389 | yes |
| Gap 0.52 → 0.06; others 0.19 → 0.22; EA 0.29 | posthoc_v6b_withincountry | 0.524→0.065; 0.186→0.224; 0.289 | yes |
| Within-country 37% (CI −0.04 to 0.31) | same | 0.367; −0.042, 0.314 | yes |
| Burn-in 0.101 → 0.038, −62%, CI 51–70%, 13/13 | v5_summary / h4_cluster_ci_v11 | 0.1008→0.0382; 0.623; 0.507–0.695 | yes |
| Unit level 74.6% of 646 | posthoc_r19_numbers.json | 0.746 | yes |
| Sensitivity 0.46 → ~0.22; FPR 29% | deploy_v4_cc_summary.csv (N=100) | 0.464; 0.218–0.227 with patients, 0.246 without; 0.289 | see m4 |
| P(FPR > 0.15) = 0.055 | Beta(10, 91), recomputed | 0.0551 | yes |
| Binomial power 0.35 / 0.79 / 0.97 | posthoc_r18_checks.json | 0.346, 0.789, 0.971 | yes |

I found no number that disagrees with its result file. The only mismatch is in wording (m4).

## Test choices, sidedness, multiplicity, labelling

- DerSimonian–Laird on logit FPR with a t-based prediction interval suits the question. I² is the right primary measure of spread.
- Sidedness is stated in S2 and matches the code: two-sided for the GMWI2 training contrast; one-sided for G2, G3, G4, GMHI H2 and the unseen East Asian contrast. The one-sided unseen test is justified by the direction found in the training data. It is labelled post hoc.
- Holm is applied within each plan. The v6 family (G2–G4) and v7 family are correct as reported. In v5, H1 and H2 have no P value, so Holm there is nominal. That is acceptable.
- Pre-specified and post hoc labels match S5. Deviations are disclosed: the strict set, the H4 population threshold, the GMHI Q2 decision and the v6c plan. The corrected cluster bootstraps (S6.7) are a good sign.
- The authors grade results honestly: H2 is "inconclusive" (LASSO 17%) and "falsified" (RF), B2 is met on the point estimate only (CI 41–149%), B3 is falsified, and G3 is falsified.

## MAJOR concerns

**M1. The fold-model check (S2.3) is not a clean test of the refit mismatch, and its summary hides a shift in direction.**
The script scores people with the *mean logit of the fold models*. That is an ensemble, not the scorer that produced the out-of-fold control scores behind the cut-off. Averaging logits shrinks the spread of scores, so fewer people pass an upper-tail cut-off. The results fit this. Pairs below 0.05 rise from 34% to 43% (LASSO 24% → 38%), and pairs above 0.15 fall from 36% to 27%. The share outside the band is "unchanged (70%)" only because pairs moved from above the band to below it. The LASSO pooled FPR also moves (fatty liver 0.26 → 0.01, hypertension 0.14 → 0.04). Under fold scoring, the AUROC–τ correlation changes sign (−0.06 → +0.23).
Requests:
(a) Add the per-fold version. Score each person with each fold model, apply the cut-off, and average the flags. Or explain why the mean logit is the right comparator.
(b) In the main text, report the shift to below-band pairs and say that pooled LASSO FPRs depend on the scoring.
(c) Fix the main-text cross-reference ("S2.2, fold-model check" should be S2.3). Remove or reconcile the S2.1 bullet "Fold models … changed little (Tables S11–S25)". That bullet refers to the three-test analysis and conflicts with S2.3.
(d) Soften the cover letter. It says "the result holds whether populations are scored with the released (refitted) model or the cross-validation models". That holds for heterogeneity (26/28 with I² ≥ 0.5) but not for the size or direction of the miscalibration.

**M2. "AUROC did not predict the spread" is stated as a finding, not as a lack of evidence.**
n = 28, and the 14 LASSO–RF pairs share a disease and populations, so the points are not independent. The 95% CI (−0.42 to 0.32) cannot exclude a moderate correlation, and the sign flips under fold scoring. The main text already says "no evidence". The highlights, the cover letter and the Conclusion ("AUROC did not predict how far it moves") should say the same, with the CI.

## MINOR concerns

- m1. The "15–16% expected by chance" benchmark treats the true FPR of each cut-off as exactly 0.10. It ignores error in estimating the cut-off from finite training controls; several single-cohort tests have few controls. The true chance share is therefore somewhat higher. I² is unaffected, but this sentence should be qualified, or the expected share should be computed with that error included.
- m2. Seven classifiers have AUROC < 0.6 and three < 0.5. They contribute headline extremes, for example the IGT LASSO prediction-interval end of 0.81 (AUROC 0.54) and the fatty-liver LASSO pooled FPR (AUROC 0.54). Put the AUROC ≥ 0.65 restriction (median 62% out of band) next to the 70% in the main text.
- m3. H4: the Wilcoxon P (7 × 10⁻⁹) over 28 classifiers treats classifiers as independent, but they share 13 populations. The population-clustered CI (51–70%) is the right inference and should be the one cited. The unit-level figure (74.6% improved) belongs in the main text next to "all 28 improved".
- m4. Sensitivity "0.46 → about 0.22". With no patients in the burn-in group, the file gives 0.246 (S2.1 says "about 0.25"). The value 0.22 holds only with 1–10% patients. State which case, and note that this rests on 3 cohorts (6 units) with no interval.
- m5. GMWI2 G2: 8 of the 12 out-of-band populations lie *below* the band. The main text should say this, because the narrative stresses over-flagging. α = 0.208 is treated as known in the Poisson-binomial test, although it is estimated from training data that include the East Asian excess; a short note is enough.
- m6. The in-sample FPR of the refitted models (median 0.4%) is uninformative for RF, which memorises its training data (13 of 14 RF values are 0). Drop it or add a caveat.
- m7. GMHI H2 is pre-specified, but plan v7 was written after the GMWI2 East Asian result, on 83% shared samples. The text says this. The highlight phrase "the two share most training studies" is good; keep it.
- m8. The five-taxa 39% is a share of a net gap that includes positive contributions (35% of the negative contributions only). Say "net" in the main text.

## Overall

The analyses are careful, transparent and correctly reported. The main conclusions hold: the FPR varies strongly between populations, GMWI2 and GMHI over-flag East Asian studies in their own training data, and the within-site burn-in works. The fold-model check needs a better comparator and a fairer summary. The AUROC statement needs softer wording in three places. None of this needs new data.

**Score: 7.5/10.**

**Scorecard (score / P75):** 1 Significance 8/8.0; 2 Scale 8/8.0; 3 Novelty 7/7.0; 4 Rigor and statistics 8/7.25; 5 External validation 8/7.0; 6 Resource 7/5.75; 7 Figures 7/7.0; 8 Clarity 7/7.25; 9 Reproducibility 8/7.25; 10 Actionable 7/7.0. Total 75 (P75 69.25). Below P75: dimension 8 only.

**Decision: minor revision.**
