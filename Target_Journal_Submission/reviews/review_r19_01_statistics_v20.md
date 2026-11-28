# Review r19, Reviewer 1 (methods and statistics), manuscript v20

Manuscript: "Gut-microbiome disease classifiers flag 0–87% of healthy people at the same cut-off, depending on the population" (Letter, iMeta).
Materials read: manuscript_v20.md, supporting_information_v20.md, si_tables_v16.md (S1a, S1b), highlights.md, cover_letter_v20.md, all seven figure PNGs, protocols v5, v6, v6b, v7, and the result files in atlas/v4–v7/results. I recomputed several numbers from the CSV files.

## 1. Summary

The authors score 28 classifiers (14 diseases, LASSO and RF) at a fixed cut-off in 36 strict healthy populations (6,525 people). The false-positive rate (FPR) varies far beyond sampling noise. They audit two released indices (GMWI2, GMHI) and find high FPRs in East Asian training studies. They retrain GMWI2 with reweighting to probe the cause. They test a label-free burn-in cut-off within sites. The work is careful, open about failed hypotheses, and mostly well labelled. Most numbers match the result files. My concerns are about one untested source of test-level bias, some claim wording, and a few internal inconsistencies.

## 2. Numbers checked against result files (26 checks)

| # | Claim (location) | Source | Result |
|---|---|---|---|
| 1 | 36 populations, 6,525 people | v5_perpop_strict.csv (36 studies; sum of max n 6,525) | match |
| 2 | Full set 55 populations, 8,160 people | v5_perpop_full.csv (55; 8,160) | match |
| 3 | 26% of LASSO pairs FPR > 0.25 | posthoc_r17_numbers.json 0.2597 (489 pairs) | match |
| 4 | Max FPR 0.87, HF RF, AUROC 0.75, n ≥ 100 | perpop: HF rf LiuW_2016 n=110, 96/110 = 0.873; AUROC 0.748 | match |
| 5 | LASSO-only range 0–0.77 (S2.2); IGT 0.09–0.77 | numbers_v11.json; IGT BritoIL_2016 0.770, min 0.088 | match |
| 6 | I² median 0.94; 28/28 strict and full | v5_summary.json 0.9365; 28 and 28 | match |
| 7 | PI upper 0.22 (CRC) to 0.81 (IGT), LASSO | v5_het_strict.csv 0.218, 0.809 | match |
| 8 | Pooled CRC 0.06; LASSO pooled 0.06–0.42; RF 0.01–0.25 | het_strict; r17 json | match |
| 9 | Spearman ρ −0.06, CI −0.42 to 0.32, P = 0.76 | recomputed: −0.0597, P = 0.763; Fisher CI in r17 json | match |
| 10 | 16 classifiers AUROC ≥ 0.65, I² median 0.94, min 0.71 | recomputed: 16, 0.942, 0.705 | match |
| 11 | 7 classifiers AUROC < 0.6 (3 < 0.5) | recomputed | match |
| 12 | Population share 17% LASSO, 7.5% RF; net 20.2% | v5_summary H2; h2_sampling_v13.json | match (but see minor 3) |
| 13 | 45% > 0.15, 24% < 0.05 (LASSO pairs) | recomputed 0.446, 0.239 | match |
| 14 | Sampling-noise out-of-band 15–16%; observed 50–97% | numbers_v11.json | match |
| 15 | GMWI2 training: 44 studies, 0–0.84, I² 0.96, 8 studies > 50% all CHN/JPN | gmwi2_published_training.json | match |
| 16 | EA median 0.64 (13) vs 0.12 (31), two-sided P = 5 × 10⁻⁷ | gmwi2_eastasia.json 0.636, 0.124, 5.3e-7 | match |
| 17 | Unseen: 15 pops, 0–0.54, 12/15 out of band vs 9%, Holm P 2 × 10⁻¹² | gmwi2_results.json; holm_v6_v13.json 1.8e-12 | match |
| 18 | Unseen EA 0.25–0.54 vs median 0.06; P = 0.020; full 0.065 | posthoc_eastasia_strict_v15.json | match |
| 19 | GMHI EA 0.67 (8) vs 0.21 (13), P = 0.0007; 83% overlap; unshared P = 0.10 | gmhi_results.json; posthoc_gmhi_gmwi2_overlap.json | match |
| 20 | Profiler shift 23% → 43%, r = 0.795, 2,190 samples, 19 studies | posthoc_gmhi_matching.json | match |
| 21 | Five taxa explain 39% of gap | numbers_v14.json 0.389 (net gap); gmwi2_eastasia.json gives 0.345 of negative contributions | match to stated definition (see minor 5) |
| 22 | Case mix 62% vs 20%, OR 6.7; 8,069 samples | gmwi2_casemix.json; counts_v12.json | match |
| 23 | Retraining 10,986 people, 61 studies; gap 0.52 → 0.06; 88%, CI 41–149% | v6b_results.json; corrected_boot_v13.json | match |
| 24 | Within-country balancing 37%, CI −0.04 to 0.31; AUROC 0.715 → 0.676 | posthoc_v6b_withincountry.json; v6b_results.json | match |
| 25 | Burn-in 0.101 → 0.038, −62%, 28/28, CI 51–70%, 646 units, 13 pops; GMWI2 0.21 → 0.04 (79%, 64–85%, 11/13) | v5_summary H4; h4_cluster_ci_v11.json; gmwi2_results G4 | match |
| 26 | Sensitivity 0.46 → 0.21–0.23 at FPR 0.29 → ≤ 0.10; P(FPR > 0.15) = 0.055 at N = 100; binomial power 98% / 72%, fixed-FPR power 0.35/0.79/0.97 | deploy_v4_cc_summary.csv (N=100); recomputed Beta(10,91) tail 0.0551; verify_power_v5.json; posthoc_r18_checks.json | match |

One mismatch: S2.2 says the GMWI2 score check used "unseen populations (1,914 people, r = 0.991)". The result file shows the check used 704 overlapping samples (gmwi2_results.json qc.n_overlap = 704), as S6.1 correctly says. 1,914 is the number of unseen people. The Figure 2B legend also places the r = 0.99 QC next to the unseen panel, which implies the same mix-up.

## 3. Test choices, sidedness and multiplicity

- Study is the unit in all East Asian contrasts (Mann–Whitney on study-level rates). This is correct and avoids pseudo-replication.
- Sidedness is stated in S2 and S2.1. The two-sided test in GMWI2's own data (post hoc, exploratory) and one-sided tests later (direction fixed by that earlier result, or by plan v7) is a defensible order. The unseen-population EA contrast is post hoc, one-sided, rests on 4 populations, and gives P = 0.020 (strict) and 0.065 (full). It is not multiplicity-adjusted. The text labels it † and gives the full-set P. Good, but it should be called suggestive, not used as support in the section heading.
- Holm families are defined per plan (v5 H1–H4, v6 G2–G4, v7 H2/H4–H6). The v7 family keeps H4–H6 although they are not interpreted; this is conservative and disclosed.
- Post hoc P values (EA unseen, GMHI unshared studies, Mongolia sensitivity, within-country CI) are not adjusted. That is acceptable if they are presented as descriptive. Most are.
- G4 bootstrap P is reported as an upper bound (0 of 5,000 draws). Fine.
- Spearman CI via Fisher z is approximate for n = 28 and a rank correlation. Disclosed.

## 4. Pre-specification vs post hoc labelling

Labelling is mostly correct and better than usual. I checked the plans:
- v5 H1 (I² ≥ 0.5 in ≥ 20/28): met 28/28. Correctly reported.
- v5 H2: plan threshold 20% supported, < 10% wrong. LASSO 17% inconclusive, RF 7.5% falsified: correct for the strict set. The full set gives RF 10.2% (v5_summary.json H2_full_rf), which is inconclusive, not falsified. The text says "every analysis" was repeated on the full set but reports only the strict verdict.
- v5 H3: correctly "not supported" (2 taxa recur in 3 tests, so not falsified either).
- v5 H4: met. Unit-level, only 74.6% of 646 units improved (numbers_v11.json). Not stated anywhere. It should be.
- Addendum A H5 is defined on LASSO; RF is "secondary" in the plan. S5 reports "H5 supported (RF)". That goes beyond the plan. The primary H5 verdict is inconclusive.
- v6b B2: the plan criterion is the point estimate. The text reports the wide CI honestly.
- v6c: correctly called post hoc and uninterpretable.
- v7: the decision not to interpret H3–H6 was taken after seeing results. Disclosed, and it reduces claims.
- The strict set was defined after first results (v4). Disclosed in the main text and Limitations.

## 5. Do claims match the evidence?

Mostly yes. Exceptions:
- Conclusion: "AUROC does not warn when it is off." The evidence is ρ = −0.06 with 95% CI −0.42 to 0.32 over 28 classifiers, several near chance. That cannot exclude a moderate relationship. "We found no evidence that..." (Results) is right; the Conclusion, highlights and Figure 1D title ("AUROC does not predict the spread") overstate it.
- Title and headline "0–87%": this is the extreme of about 300 classifier–population pairs (n ≥ 100). The maximum comes from one pair (HF RF, LiuW_2016, n = 110). The 26% > 0.25 figure and the prediction intervals are more robust headline numbers. The title is not wrong, but a maximum is the noisiest summary.
- "36 general-population cohorts": Table S1b includes control arms of case–control studies (e.g. YachidaS_2019, WirbelJ_2018, QinJ_2012, QinN_2014, ZhuF_2020, LiJ_2017, XieH_2016). Some of these controls came from colonoscopy or hospital settings. "Healthy control groups" is more accurate than "general-population".
- "Retraining linked this to the geographic make-up of the training data" (highlights, GA). The reweighting also shrinks large countries. The within-country label-only balancing removed 37% (CI includes zero). So the evidence supports "training-data composition by country", but cannot separate label case mix from country dominance. The Results text says this; the highlights and GA are stronger.

## 6. MAJOR concerns

M1. Cut-off/model mismatch not tested for 25 of 28 classifiers. In atlas_v5.py the cut-off is the 90th percentile of out-of-fold control scores, but populations are scored with the model refitted on all data (`p.score`). A refitted model can have a shifted score scale. This would move every population's FPR in the same direction for that test. Pooled FPRs of 0.42 (IGT LASSO), 0.26 (fatty liver LASSO) and 0.008 (IGT RF) look like such test-level offsets. This does not affect I² or τ, but it does affect the pooled FPRs, the "26% of pairs > 0.25" figure, the 0–87% range and the burn-in error reductions. The fold-model check (S2) was done only for the CRC, IBD and T2D tests in the earlier analysis. Please (a) report the refitted model's in-sample FPR on its own training controls, and (b) repeat the atlas summary with fold-model scoring (mean of fold-model scores, or each fold model with its own fold cut-off) for all 28 classifiers.

M2. Claim calibration in headline places. Revise the Conclusion, highlights and Figure 1D title on AUROC (Section 5). Make "36 general-population cohorts" accurate. Make the highlights and graphical abstract say what the reweighting can and cannot separate. Consider a headline number that is not a maximum.

## 7. MINOR concerns

1. S2.2: the GMWI2 QC used 704 shared samples, not 1,914 unseen people. Fix S2.2 and the Figure 2B legend.
2. Report the full-set H2 RF result (10.2%, inconclusive) next to the strict verdict (falsified).
3. S2.1 says the net LASSO population share of 20.2% is "exactly at the 20% threshold, so the verdict is inconclusive under either definition". 20.2% ≥ 20% would meet the plan's support threshold under the net definition. Say instead that the planned (gross) measure is primary and is inconclusive, and that the net measure would pass narrowly.
4. S5: H5 for RF is secondary per Addendum A. Report H5 as inconclusive (primary, LASSO) and RF as a secondary result.
5. The 39% taxon share uses the net gap as denominator. As a share of negative contributions it is 35% (gmwi2_eastasia.json). Net-gap shares can exceed 100% per taxon in principle. State the gross share too, or use it.
6. Report unit-level H4: 74.6% of 646 units improved. The 28/28 is at classifier level.
7. Main text: the unseen EA contrast (n = 4 populations, post hoc, one-sided) should be called suggestive. The section heading rests on the training-data result, which is fine.
8. Figure 3B: the burn-in point with no patients (FPR 0.098, sensitivity 0.245) is hidden behind the labelled-controls diamond. Say so in the legend. The three cohorts were those with high training-cut-off FPR (29%); state how they were chosen.
9. Graphical abstract: the panel 1 title ("…(LASSO)") overlaps the panel 2 title ("2 A released index…"). Fix the layout.
10. Burn-in: all within-site tests use healthy-only populations (π = 0). The contamination analysis rests on 3 cohorts and 6 units. Say this in the main text where the 62% is given.
11. The sensitivity-vs-FPR trade-off is shown for N = 100 only; one sentence on how it changes at N = 50 would help sites.
12. Repository URL and DOI are placeholders. I could not check the fprcal tool or the "fresh-clone rerun" claim.

## 8. Scorecard (1–10; benchmark P75 in brackets)

| # | Dimension | Score | P75 |
|---|---|---|---|
| 1 | Biological / clinical significance | 8 | 8.0 |
| 2 | Scale and breadth of data | 8 | 8.0 |
| 3 | Novelty vs prior art | 7 | 7.0 |
| 4 | Methodological rigor and statistics | 7 | 7.25 |
| 5 | External validation / cross-cohort generalisation | 8 | 7.0 |
| 6 | Resource / tool value | 6 | 5.75 |
| 7 | Figure quality and visual story | 7 | 7.0 |
| 8 | Clarity, framing and writing | 7 | 7.25 |
| 9 | Reproducibility and openness | 7 | 7.25 |
| 10 | Actionable insight / mechanism | 7 | 7.0 |
| | Total | 72 | 69.25 |

Rigor is held just below P75 by M1 and the small inconsistencies. Reproducibility and resource scores are capped because the repository cannot be checked.

## 9. Decision

Overall score: 7/10. The statistics are mostly sound and transparently reported, and 25 of 26 checked numbers match the result files. One untested scoring choice (M1) and several overstated sentences need fixing.

**Decision: minor revision.**
