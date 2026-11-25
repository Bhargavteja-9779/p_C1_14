# Supporting Information (manuscript v12)

All tables are in `si_tables_v12.md`, generated from result files. Code paths are relative to
`Target_Journal_Submission/code/`. Every confirmatory analysis followed an analysis plan committed to git before it was
run (S5); everything else is labelled post hoc or exploratory.

## S1. Data, classifiers and healthy populations

**Profiles.** Species-level MetaPhlAn3 relative abundances and metadata from curatedMetagenomicData (release 2021-03-31;
MetaCardis 2022-10-19). The exact metadata file is deposited (`data/sampleMetadata.csv.gz`, SHA-256 recorded).

**Disease tests (Table S1a).** 14 diseases with at least one case–control cohort of ≥ 30 adult cases and ≥ 30 controls:
- multi-cohort (leave-one-cohort-out cut-off): colorectal cancer (10 cohorts), adenoma (5), IBD (4), T2D (4), impaired
  glucose tolerance (3);
- single-cohort (5-fold out-of-fold cut-off): coronary artery disease and heart failure (MetaCardis), atherosclerotic
  CVD, cirrhosis, hypertension, schizophrenia, ME/CFS, migraine and fatty liver (one cohort each).

26 training cohorts in total; one sample per person. Features: log10(relative abundance/100 + 10⁻⁵) for taxa present in
> 5% of training samples, z-scored. LASSO logistic regression (C = 0.1, balanced weights) and random forest (500 trees,
minimum leaf 2), fixed in advance. Cut-off = 90th percentile of out-of-fold control scores (target FPR 0.10).
Code: `experiments/atlas/v5/atlas_v5.py`.

**De-duplication.** Profiles were compared across all cohorts (log-profile Pearson r > 0.99). The copy in the case–control
study was kept; 119 samples were removed and ThomasAM_2019_c dropped (`v4/dedup.py`, Table S17). A post hoc check at
r > 0.95 removed 8 more samples and changed no result.

**Healthy populations (Table S1b).**
- *Strict (primary):* healthy adults, not on antibiotics, not pregnant or lactating, no family role in mother–infant
  studies. It excludes 20 cohorts whose controls are hospital in-patients, mothers, trial participants, colonoscopy
  referrals, comorbidity-enriched groups or a methods set. Cohorts need ≥ 20 people: 36 cohorts, 6,525 people,
  20 countries.
- *Full:* the full de-duplicated set, reported as a sensitivity analysis.

Each test skips its own training cohorts. The strict set was defined after the first results (disclosed).

## S2. Statistics and robustness

**Heterogeneity.** DerSimonian–Laird random effects on empirical logit FPR, giving I², τ and a 95% prediction interval
(Tables S2a, S2b). Out-of-band share is compared with its binomial expectation under perfect calibration. Crossed
random-effects model (test and population as crossed effects; Table S3).

**Robustness checks** (earlier analyses of the CRC, IBD and T2D tests; Tables S11–S25):
- covariate mixed models (age, sex, BMI, depth);
- scoring with the fold models instead of the refitted model;
- the full set;
- de-duplication at r > 0.95.

**Inference.** Population-cluster bootstrap (2,000 resamples) and Wilcoxon tests on population means. Holm correction
within each plan's confirmatory family, and across all 34 population-level P values of the earlier analysis (Table S20).

## S3. Taxa behind the false alarms

For LASSO, a population's mean score shift relative to training controls is Σ_j w_j (z̄_j,population − z̄_j,controls).
Table S4 lists the top contributors in each test's most over-flagged population. No taxon was a top-10 driver in four
or more tests (protocol_v5 H3 not supported).

Exploratory analyses:
- the depletion of *Bacteroides*/*Parabacteroides* plus enrichment of *Prevotella* carried a median of 11% of the
  positive shift (≥ 20% in 4 of 14 tests; `v5/genus_axis_v5.py`);
- Cameroon (LokmerA_2019) was the most over-flagged population for 5 of the 14 tests;
- a population's compositional distance from the training controls correlated with its FPR (Table S6).

The distance relationship was replicated as pre-specified on 19 other populations: LASSO 10/14 tests positive, P = 0.090
(inconclusive); random forest 11/14, P = 0.029. Two independent runs gave identical results.

## S4. Earlier, detailed analysis of the CRC, IBD and T2D tests

This analysis tested the site-level fix in depth for three tests (code `experiments/atlas/v4/`; Tables S11–S25).

### Burn-in rules and designs

BURN: cut-off = k-th smallest of N unlabelled burn-in scores, k = ⌈(N + 1)(1 − α(1 − π_max))⌉; infeasible (flag nobody)
if k > N. BURN-PAC: the smallest k with P(Beta(N + 1 − k, k) > β) ≤ 0.05, β = α(1 − π_max). LAB: BURN applied to N
labelled controls.

**Comparators.**
- Training cut-off.
- ATLAS: the 90th percentile of pooled scores of all other populations in the same split.
- ALIGN (P5): label-free location–scale alignment. Each model feature of the evaluation people is mapped so the burn-in
  group's mean and SD match those of the training controls; the evaluation people are then scored with the unchanged
  model and the training cut-off.
- Control augmentation (Wirbel et al. 2021, post hoc): retrain with every development-split healthy cohort added as
  controls, then apply the same cut-off rule.

**Designs.**
- Random split (P6): 200 random burn-in/evaluation splits per population, N ∈ {25, 50, 100, 200}, for populations with
  n ≥ N + 20.
- Non-random splits (P4):
  - (a) burn-in from the lower half of age or BMI, evaluated on the upper half; women → men and men → women;
  - (b) one sub-site → another within MetaCardis (Leipzig, Copenhagen, Paris), AsnicarF_2021 (UK, USA), BritoIL_2016
    (two villages) and LiuW_2016 (westernised, non-westernised);
  - (c) one cohort → another cohort of the same country (strict set, both n ≥ 60);
  - (d) the first N people by NCBI accession → the rest.
  Designs (a)–(c) use N ∈ {50, 100} and 200 draws.
- Contaminated pools: in the locked case–control cohorts, burn-in groups with a patient fraction π ∈ {0.01, 0.05, 0.10}.
  The case–control cohorts were the CRC cohorts YachidaS_2019 and YuJ_2015, scored by a model trained on the eight
  development cohorts, and IBD/T2D by leave-one-cohort-out.

**Endpoints.** Mean |FPR − 0.10|, P(FPR > 0.15), P(FPR > 0.10), mean FPR and sensitivity. Each was averaged per unit
(classifier × population or ordered pair) and then over units.


### Corrections that failed

Development rounds on the case–control cohorts (v1–v2):
- label-free site-shift mixture model;
- location–scale transport from a few controls;
- prevalence EM;
- borrowing controls from a neighbouring site.

Atlas round 3 (v3, development cohorts):
- healthy-context residual (cut CRC AUROC from 0.76 to 0.61–0.68);
- pooled atlas reference;
- composition-matched references.

v4:
- ALIGN (better than the training cut-off, worse than the burn-in);
- control augmentation (no overall gain);
- country-matched reference (22–58% of populations in band);
- burn-in from another sub-site or another cohort (fails).


## S5. Analysis plans and deviations

| Plan (file) | Scope | Outcome |
|---|---|---|
| protocol_atlas.md, atlas_split.md | 3-test atlas, A1–A5 | A1, A4, A5 held; A2 partial; A3 mixed |
| protocol_deploy.md | v3 burn-in, random splits | met, but true by construction |
| v4/protocol_v4.md (D1–D4) | dedup, strict set, non-random splits, ALIGN | H-NX1 not supported (48%), H-NX2 supported, ALIGN < burn-in |
| v5/protocol_v5.md | 14-test atlas, H1–H4 | H1 supported (28/28), H2 inconclusive or falsified, H3 not supported, H4 supported (28/28) |
| v5/protocol_v5.md, Addendum A | replication H5/H6 | H5 inconclusive (LASSO) / supported (RF); H6 inconclusive |
| v6/protocol_v6.md | GMWI2 audit G1–G4 | G1, G2, G4 supported; G3 falsified |
| v6/protocol_v6b.md | case-mix retraining B1–B4 | B1, B2, B4 supported; B3 falsified |
| v6/protocol_v6c.md | balancing the 5 disease tests C1–C3 | C1 supported; C2 and C3 falsified |

Deviations:
- v4 D1–D4 are listed in v4/protocol_v4.md.
- The strict set and the extended covariate model were not pre-specified.
- Geography and distance analyses are exploratory unless covered by Addendum A.
- Failed development attempts are recorded in state/variants_tried.csv; this includes geography-stable feature
  penalisation (`v5/dev_gsp.py`), which failed.

## S6. External audit of a published classifier (GMWI2) and the case-mix mechanism

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

### S6.3 Table S9 — GMWI2 false-positive rate in unseen healthy populations (strict)

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

### S6.5 Analysis plan v6c (pre-specified): balancing the disease classifiers (Table S10)

| Hypothesis | Criterion | Result | Verdict |
|---|---|---|---|
| C1 heterogeneity | mean τ lower when balanced | 0.92 → 0.78 (difference −0.14, population-clustered 95% CI −0.23 to −0.03) | supported |
| C2 calibration | share of populations outside 0.05–0.15 lower | 0.66 → 0.82 | falsified |
| C3 discrimination | AUROC drop ≤ 0.03 | 0.656 → 0.623 (−0.033) | falsified |

Balancing at training time reduced heterogeneity for the five disease tests, but it moved the overall FPR away from
target and cost AUROC. It is evidence for the mechanism, not a deployment fix. Code: `experiments/atlas/v6/run_v6c.py`.
