# Supporting Information

Reference numbers [n] refer to the main-text reference list. Supporting Figures S1 and S2 are supplied as separate files.
All tables are in the Supporting Tables file (Tables S1–S25; Table S26 is in S7 below; numbered in order of first citation in the main text or here), generated from result files. Code paths are relative to
`Target_Journal_Submission/code/`. Every confirmatory analysis followed an analysis plan committed to git before it was
run (S5); everything else is labelled post hoc or exploratory.

## S1. Data, classifiers and healthy populations

**Profiles.** MetaPhlAn3 relative abundances of all clades (kingdom to species; features present in > 5% of training
samples) and metadata from curatedMetagenomicData (release 2021-03-31;
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


### S2.1 Additional results
- **Variance decomposition, LASSO.** Population 17%, classifier 21%, sampling noise 14%, classifier–population pair 48%
  of the variance in logit FPR. The plan defines the population share as a share of total between-unit variance (17%);
  net of sampling noise it is 20.2%, exactly at the 20% threshold, so the verdict is inconclusive under either definition.
- **Bands.** The atlas band 0.05–0.15 and the GMWI2 band 0.10–0.31 are both half to one and a half times the target or
  training FPR (α/2 to 1.5α). They are reference ranges, not confidence intervals.
- **Sidedness.** Training-data East Asian vs other comparison: two-sided Mann–Whitney (P = 5 × 10⁻⁷). Unseen East Asian
  vs other (P = 0.020 strict; 0.065 full set): one-sided (greater). G3 seen vs unseen (P = 0.72): one-sided (less).
- **Reweighting detail.** τ on the logit scale 1.16 → 0.81; pooled AUROC 0.715 → 0.676 (point estimate beyond the
  pre-stated margin; CI −0.12 to +0.02 includes values within it).
- **Burn-in CI.** The pre-specified H4 criterion was ≥ 75% of tests improved (met, 28/28). The population-clustered CI
  (51–70%) and the 13/13 count are post hoc. Splits used: accession order, age and BMI (646
  evaluations); sex splits appear only in the three-test analysis (S4). Populations: full set, ≥ 120 people (13; 11 for
  T2D), including MetaCardis_2020_a and ShaoY_2019, which are not in the strict set.
- **Variance decomposition, RF.** Classifier 46%, population 7.5%, classifier–population pair 25%, the rest sampling
  noise (Table S3). For LASSO the population share (17%) is inconclusive against the pre-stated 20% threshold (plan v5
  grading); for RF it is falsified.
- **AUROC restriction.** Restricting to the 16 classifiers with out-of-fold AUROC ≥ 0.65: I² median 0.94 (minimum 0.71),
  median 62% of populations outside 0.05–0.15. Seven classifiers have AUROC < 0.6 (three < 0.5).
- **Fold models.** Scoring with the cross-validation fold models instead of the refitted model changed little (Tables S11–S25).
- **GMWI2 G2.** Of the 12 unseen strict populations outside 0.10–0.31, eight lie below the band and four above it; the
  miscalibration is in both directions. α = 0.208 is the training FPR, itself raised by the East Asian training studies.
- **Reweighting (v6b).** B2: point estimate −88%, corrected study-clustered CI of the relative reduction 41–149% (6% of
  draws below the 50% criterion). B4 was met on the logit scale (τ 1.16 → 0.81); on the FPR scale the between-study median
  absolute deviation was 0.13 in both arms, and several European studies were flagged more often after reweighting.
  Within-study AUROC fell only from 0.669 to 0.649 (−0.020; CI −0.052 to 0.013; post hoc).
- **Burn-in sensitivity.** With no patients in the burn-in group, sensitivity was about 0.25 (100 labelled local
  controls: 0.245); 1–10% patients cost a further 0.02–0.04.
- **Binomial check.** n = 100: 98% power for pairs with observed FPR > 0.25 and 72% for > 0.15 (average over the atlas);
  lower at an FPR of exactly 0.25.

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
| v6/protocol_v6b.md | case-mix retraining B1–B4 | B1 and B4 (logit scale) supported; B2 supported on the point estimate only (CI 41–149% includes values below the criterion); B3 falsified |
| v6/protocol_v6c.md | balancing the 5 disease tests C1–C3 | written before running but committed together with its results, so treated as POST HOC; C1 logit-scale only (not on the FPR scale); C2 and C3 failed; C1–C3 uninterpretable because the implementation deviated from the plan (S6.6) |

Deviations:
- v4 D1–D4 are listed in v4/protocol_v4.md.
- The strict set and the extended covariate model were not pre-specified.
- Geography and distance analyses are exploratory unless covered by Addendum A.
- Failed development attempts are recorded in state/variants_tried.csv; this includes geography-stable feature
  penalisation (`v5/dev_gsp.py`), which failed.

## S6. External audit of a published classifier (GMWI2) and the case-mix mechanism

### S6.1 Model and verification

GMWI2 (Chang et al. 2024 [20]) is an L1-penalised logistic regression on presence (relative abundance > 1e-5) of 95 MetaPhlAn3 clades, with intercept 0 and the decision rule GMWI2 = w·presence; GMWI2 > 0 = healthy. We obtained the model from bioconda (gmwi2 1.6, MIT licence) and read its coefficients with a whitelisted unpickler (code/experiments/atlas/v6/extract_gmwi2.py); they are identical to Supplementary Data 3 of [20] (95/95, max |Δ| 1e-15). Our re-scored GMWI2 on the 704 samples shared with the developers' Supplementary Data 5 correlated with the published scores at Pearson r = 0.991 (same healthy/non-healthy call for 98.4%). The training FPR is the share of the developers' healthy training samples below the cut-off in the 44 studies with at least 20 healthy people (5,514 of the 5,547 healthy samples), α = 0.208.

### S6.2 Analysis plan v6 (pre-specified) and outcomes

Plan committed before any score was computed (code/experiments/atlas/v6/protocol_v6.md). Holm over the tests with a P value (G2, G3, G4; holm_v6_v13.py): adjusted G2 1.8e-12, G4 < 0.0004 (5,000 bootstrap draws), G3 0.72.

| Hypothesis | Pre-stated criterion | Result | Verdict |
|---|---|---|---|
| G1 heterogeneity | I² ≥ 0.5 across unseen strict populations | I² = 0.92 (τ 1.06), 15 populations | supported |
| G2 miscalibration | out-of-band share exceeds binomial expectation by ≥ 20 pp | 80% vs 9% expected, P = 6.1e-13 | supported |
| G3 in-sample optimism | seen populations lower FPR than unseen (MW, P<0.05) | mean FPR seen 0.26 vs unseen 0.20, one-sided P = 0.72 | falsified |
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

In GMWI2's training data (Supplementary Data 2 of [20]), East Asian samples are 62% of non-healthy but 20% of healthy samples (odds ratio 6.7; no P value is given because samples within a study are not independent; the study-clustered analysis is below). Plan v6b (protocol_v6b.md) retrains a GMWI2-recipe classifier on 10,986 cMD subjects, leave-one-study-out, pooled vs country-balanced sample weights.

| Hypothesis | Criterion | Result | Verdict |
|---|---|---|---|
| B1 mechanism | naive East Asian−other FPR gap ≥ 0.15 | 0.52 (EA 0.71 vs 0.19) | supported |
| B2 intervention | balancing cuts the gap ≥ 50% | −88% (corrected study-clustered CI 41–149%; 6% of draws below 50%) | supported (point estimate); CI includes values below the criterion |
| B3 cost | balanced pooled AUROC within 0.03 of naive | 0.715 → 0.676 (-0.040, CI -0.12/+0.02) | falsified |
| B4 heterogeneity | balanced τ < naive τ | 1.16 → 0.81 | supported |

Post hoc: within-study AUROC (cases vs controls of the same study, 24 studies) fell only 0.669 → 0.649 (-0.020, CI -0.052/+0.013); much of the pooled-AUROC loss was the geographic shortcut, not within-study discrimination.

### S6.5 Analysis plan v6c (POST HOC: written before running, but committed together with its results): balancing the disease classifiers (Table S10)

| Hypothesis | Criterion | Result | Verdict |
|---|---|---|---|
| C1 heterogeneity | mean τ lower when balanced | 0.92 → 0.78 (difference −0.14; corrected population-clustered 95% CI −0.22 to −0.01) | uninterpretable: the implementation deviated from the plan (S6.6) |
| C2 calibration | share of populations outside 0.05–0.15 lower | 0.66 → 0.82 | falsified |
| C3 discrimination | AUROC drop ≤ 0.03 | 0.656 → 0.623 (−0.033) | falsified |

On the FPR scale, balancing did not reduce heterogeneity: the median absolute deviation of per-population FPR fell in 2 of
5 tests (mean 0.093 → 0.110), and the mean absolute error from 0.10 rose (0.150 → 0.249) because balancing moved FPR levels
away from target (median CRC 0.04 → 0.33; T2D 0.12 → 0.54). A lower logit-scale τ is expected when FPRs move from near 0
towards 0.5, so C1 is not evidence of more uniform FPRs. The v6c weighting also differs from v6b (it gives each country
equal total weight as well as balancing labels within country). We therefore do not claim that balancing generalises to the
disease classifiers. Code: `experiments/atlas/v6/run_v6c.py`; corrections: `corrected_boot_v13.py`.

### S6.6 What the v6b reweighting does, and why v6c is uninterpretable (post hoc)
The pre-specified v6b weight 1/n(country, label) gives every country × label group the same total weight. Besides balancing
healthy and non-healthy within each country, it shrinks the weight of large countries (China, Japan) and gives small groups
large weight. A post hoc variant that balances labels within each country but keeps each country's original share of the
data (posthoc_v6b_withincountry.py) reduced the East Asian–other gap from 0.52 to 0.33 (37%; absolute 0.19, study-clustered
95% CI −0.04 to 0.31), against 0.46 (CI 0.18–0.58; 88%) for the pre-specified weighting. Between-study spread on the FPR
scale was 0.132 (naive), 0.127 (pre-specified) and 0.167 (within-country) as median absolute deviation.
run_v6c.py's weights() first gives each country × label cell equal weight and then divides again by the country's sample
count, so a few samples from small countries dominate (e.g. five Canadian samples carry most of the CRC training weight).
This does not match protocol_v6c.md; the v6c balanced arm is uninterpretable and is not used in the main text.
In the within-country variant, countries with only one label (e.g. NLD, ISR) keep their original weight.
Note: rerunning run_v6c.py gives slightly different numbers (τ difference −0.147 vs −0.143) because liblinear was not
seeded; the committed result files are the reported ones.

### S6.7 Corrections to two cluster bootstraps
Two cluster bootstraps in the original analysis were wrong and are corrected in `corrected_boot_v13.py` (original result files
kept unchanged): run_v6c.py drew populations with `set()`, which drops repeated draws (a ~63% subsample, not a bootstrap);
analyse_v6b.py kept study names on repeated draws, so `groupby` merged duplicates into one study with doubled n. Corrected
intervals: v6c C1 −0.22 to −0.01 (was −0.23 to −0.03); v6b B2 41–149% (was 54–121%); v6b B3 AUROC −0.12 to +0.02
(unchanged).

## S7. Audit of a second published index: GMHI (plan v7)
Plan `code/experiments/atlas/v7/protocol_v7_gmhi.md`, committed before any GMHI score was computed. GMHI (Gupta et al.
2020) was re-implemented in Python from the developers' released script `GMHI.R` (repository jaeyunsung/GMHI_2020,
commit 87fe9f6); the R script was not executed. Code: `v7/run_gmhi.py`; post hoc name check: `v7/posthoc_gmhi_names.py`.

**QC.** Q1: on the developers' example, our GMHI equals their output (max |difference| 4.9e-15). Q2: on
101 samples present in both curatedMetagenomicData (MetaPhlAn3) and the developers' profiles
(MetaPhlAn2), r = 0.80 (criterion ≥ 0.80; passed narrowly), sign agreement 85%.
Four of the seven health-prevalent species (Alistipes senegalensis, Bacteroidales bacterium ph8, Lachnospiraceae
bacterium 8_1_57FAA, Sutterella wadsworthensis) and 13 of the 43 health-scarce species do not occur under these names in
any of the 61 curatedMetagenomicData studies. Post hoc, four health-scarce species have clear MetaPhlAn3 names
(Hungatella hathewayi, Erysipelatoclostridium ramosum, Streptococcus anginosus group, Streptococcus mitis); renaming
them changed little (r = 0.81; population ranking ρ = 0.996). On the overlapping
samples, the share flagged was 70% with the developers' profiles and 85% with curatedMetagenomicData
profiles, so flag levels in curatedMetagenomicData are inflated by the profiler version.

**Training FPR.** alpha_GMHI = 0.236: share of the 2,636 healthy samples in the developers' data with GMHI < 0
(20 ties at exactly 0 counted as not flagged).

| Hypothesis | Criterion | Result | Verdict |
|---|---|---|---|
| H1 heterogeneity, developers' data | I² ≥ 0.5 | I² 0.96 over 21 studies; range 0.03–0.90 | supported |
| H2 East Asian excess, developers' data | one-sided MW P < 0.05 | median 0.67 (8 studies) vs 0.21 (13); P = 0.0007, Holm 0.0007 | supported |
| H3 heterogeneity, unseen strict cMD | I² ≥ 0.5 | I² 0.96 over 34 populations | supported (level confounded by profiler, see QC) |
| H4 miscalibration beyond noise | excess ≥ 20 pp, P < 0.05 | 26/34 outside 0.12–0.35 (23 above, 3 below) vs 4% expected; Holm P = 9.9e-43 | criterion met, not interpreted as a population effect (profiler version) |
| H5 shared population effect with GMWI2 | Spearman ρ > 0, one-sided P < 0.05 | ρ = 0.70, 36 populations; Holm P = 2.3e-06 | supported |
| H6 within-site burn-in | clustered 95% CI < 0 | mean error 0.257 → 0.054 (-79%); difference -0.252, CI -0.387 to -0.133; 12/13 populations; P < 0.0002 | supported |

Full set (sensitivity): 53 unseen populations, I² 0.96; East Asian unseen median 0.84 vs 0.48.

### Table S26. GMHI in the developers' own healthy data, by study

| study                       | author                                                | region                                       | East Asian   |   n |   flagged |   share flagged |
|:----------------------------|:------------------------------------------------------|:---------------------------------------------|:-------------|----:|----------:|----------------:|
| V-15                        | Petersen (2017)                                       | USA                                          | no           |  33 |         1 |           0.03  |
| S-8                         | Liu (2016)                                            | Mongolian Population                         | no           | 107 |         8 |           0.075 |
| V-25                        | Zeevi (2015)                                          | Israel                                       | no           | 883 |        78 |           0.088 |
| V-22                        | Schirmer (2016)                                       | Netherlands                                  | no           | 467 |        46 |           0.099 |
| V-44                        | Backhed (2015)                                        | danish                                       | no           |  89 |        14 |           0.157 |
| V-1                         | Rampeli (2015)                                        | HADZA                                        | no           |  30 |         5 |           0.167 |
| V-46                        | Le Chatelier (2013)                                   | Danish population                            | no           |  39 |         8 |           0.205 |
| V-23 & V-24 (HMP1 and HMP2) | HMP1: Huttenhower (2012) and HMP2: Lloyd-Price (2017) | USA                                          | no           | 222 |        56 |           0.252 |
| V-38                        | Li (2017)                                             | China                                        | yes          |  35 |        11 |           0.314 |
| V-19                        | Feng (2015)                                           | Samples collected from a hospital of Austria | no           |  21 |         8 |           0.381 |
| V-10                        | Qin (2014)                                            | China                                        | yes          |  92 |        37 |           0.402 |
| V-6                         | Zeller (2014)                                         | France                                       | no           |  42 |        17 |           0.405 |
| V-16                        | Nielsen (2014)                                        | danish                                       | no           |  58 |        24 |           0.414 |
| V-43                        | Vogtmann (2016)                                       | White not Hispanic                           | no           |  30 |        15 |           0.5   |
| V-12                        | Liu (2017)                                            | Chinese                                      | yes          | 101 |        64 |           0.634 |
| V-18                        | Obregon-Tito (2015)                                   | Tunapuco                                     | no           |  20 |        13 |           0.65  |
| V-29                        | Zhang (2015)                                          | China                                        | yes          |  55 |        36 |           0.655 |
| V-32                        | Nishijima (2016)                                      | Japanese                                     | yes          |  26 |        18 |           0.692 |
| V-8                         | Qin (2012)                                            | Chinese                                      | yes          |  61 |        48 |           0.787 |
| V-2                         | Jie (2017)                                            | Chinese                                      | yes          |  75 |        62 |           0.827 |
| S-7                         | He (2017)                                             | Chinese                                      | yes          |  39 |        35 |           0.897 |
