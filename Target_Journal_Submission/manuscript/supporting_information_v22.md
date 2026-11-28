# Supporting Information

Reference numbers [n] refer to the main-text reference list. Supporting Figures S1 and S2 are supplied as separate files.
All tables are in the Supporting Tables file (Tables S1–S25; Tables S26–S27 are in S7 below; numbered in order of first citation in the main text or here), generated from result files. Code paths are relative to
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

**Inference.** Population-cluster bootstrap (2,000 resamples) and Wilcoxon signed-rank tests on population means
(two-sided). Sidedness of the other tests: replication sign tests (H5) one-sided; GMWI2 out-of-band test (G2, exact
Poisson-binomial) one-sided; GMWI2 burn-in bootstrap P (G4) one-sided (share of draws ≤ 0); East Asian contrasts
one-sided except in the developers' GMWI2 training data (two-sided); Spearman correlations two-sided. Post hoc
analyses are marked † in the main text. Holm correction
within each plan's confirmatory family, and across all 34 population-level P values of the earlier analysis (Table S20).


### S2.1 Additional results
- **Variance decomposition, LASSO.** Population 17%, classifier 21%, sampling noise 14%, classifier–population pair 48%
  of the variance in logit FPR. The plan defines the population share as a share of total between-unit variance (17%);
  this planned (gross) measure is primary and is inconclusive. Net of sampling noise (post hoc) it is 20.2%, which
  would pass the threshold narrowly. RF: population 7.5% in the strict set (falsified) and 10.2% in the full set
  (inconclusive); for RF the classifier explains most of the variance (46%).
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
- **Fold models (three-disease analysis).** Scoring with the cross-validation fold models instead of the refitted model
  changed little for the CRC, IBD and T2D classifiers (Tables S11–S25). For all 28 atlas classifiers see S2.3, where the
  change is larger for some LASSO classifiers.
- **GMWI2 G2.** Of the 12 unseen strict populations outside 0.10–0.31, eight lie below the band and four above it; the
  miscalibration is in both directions. α = 0.208 is the training FPR, itself raised by the East Asian training studies.
- **Reweighting (v6b).** B2: point estimate −88%, corrected study-clustered CI of the relative reduction 41–149% (6% of
  draws below the 50% criterion). B4 was met on the logit scale (τ 1.16 → 0.81); on the FPR scale the between-study median
  absolute deviation was 0.13 in both arms, and several European studies were flagged more often after reweighting.
  Within-study AUROC fell only from 0.669 to 0.649 (−0.020; CI −0.052 to 0.013; post hoc).
- **Burn-in sensitivity.** With no patients in the burn-in group, sensitivity was about 0.25 (100 labelled local
  controls: 0.245); 1–10% patients cost a further 0.02–0.04.
- **Binomial check.** n = 100: 98% power for pairs with observed FPR > 0.25 and 72% for > 0.15 (average over the LASSO atlas pairs; 97% for RF);
  lower at an FPR of exactly 0.25.

### S2.2 Further detail on the main-text results
This section gives numbers behind the main-text statements; each is traceable to the result files named in S1–S6.
- **Atlas, pair level.** Of 489 LASSO classifier–population pairs (strict set), 45% had an FPR above 0.15 and 24% below
  0.05. Across the LASSO tests alone, FPRs ranged from 0 to 0.77 in populations of at least 100 people; impaired glucose
  tolerance (LASSO) spanned 0.09–0.77.
- **Atlas, prediction intervals and pooled FPRs.** The upper end of the 95% prediction interval for a new population
  ranged from 0.22 (CRC) to 0.81 (impaired glucose tolerance, a near-chance classifier, AUROC 0.54) across the LASSO
  classifiers. Pooled over populations, the CRC LASSO classifier had an FPR of 0.06. The maximum of 0.87 in populations
  of at least 100 people is one RF pair (heart failure, AUROC 0.75, LiuW_2016, n = 110).
- **GMWI2 reference FPR.** 20.8% of the developers' healthy training samples fall below the published cut-off (their
  own scores). The developers published a cut-off, not a target rate; we use this training-implied FPR as the reference.
- **Atlas, sampling noise.** Sampling noise alone would put 15–16% of populations outside 0.05–0.15 (half to one and a
  half times the target); the observed share was 50–97%.
- **Atlas, covariates.** In the three-test analysis (S2), adjusting for age, sex, body-mass index and sequencing depth
  left a population effect. The variance decomposition was clearly below the pre-stated 20% threshold for RF.
- **GMWI2, developers' training data.** The 44 studies are those with at least 20 healthy people; scores are the
  developers' own. East Asian = China, Japan, South Korea (Mongolia counted as other; see S7 for a sensitivity check).
  Healthy people in rural Africa were almost never mislabelled (Tanzania, Madagascar, Burkina Faso, Cameroon, Ghana:
  0–7%).
- **GMWI2, unseen populations.** Of the 12 populations outside the band, eight were below and four above. East Asian
  (4 populations) vs other (11): median 0.38 vs 0.06, one-sided P = 0.020 (post hoc; one-sided in the direction set by
  the training-data result). Full set: East Asian median 0.38 vs 0.20 in the others (one-sided P = 0.065). We had expected a lower FPR in populations seen in
  training; this was falsified (one-sided P = 0.72).
- **Atlas, robust summary and AUROC (post hoc; `v5/posthoc_r17_numbers.py`).** 26% of LASSO and 16% of RF
  classifier–population pairs had an FPR above 0.25. Pooled FPRs ranged from 0.06 to 0.42 (LASSO) and 0.01 to 0.25
  (RF). Spearman ρ between AUROC and τ: −0.06, Fisher-z 95% CI −0.42 to 0.32 (approximate for a rank correlation).
  The variance share of 20.2% for LASSO population is net of sampling noise (post hoc, `h2_sampling_v13.json`); the
  pre-specified measure is 17% (LASSO) and 7.5% (RF).
- **GMWI2 verification.** Released coefficients matched the paper's Supplementary Data for 95/95 taxa; our scores
  matched the developers' published scores on the 704 samples shared by both data sets (r = 0.991). The 15 unseen
  strict populations hold 1,914 people.
- **Taxa.** *Bacteroides plebeius*: carried by 72% of East Asian vs 17% of other healthy people; *Klebsiella*: 59% vs
  22%.
- **Case mix.** East Asian samples were 1,574 of 2,522 non-healthy and 1,097 of 5,547 healthy GMWI2 training samples (odds ratio 6.7).
  *Clostridium* sp. CAG_167, weighted as "healthy", was carried by 2% of East Asian vs 28% of other healthy people.
- **Retraining (plan v6b).** The between-study spread fell on the logit scale (the pre-stated criterion) but not on
  the FPR scale, and the East Asian median after reweighting (0.29) stayed above the training FPR. Within-country
  label balancing: absolute reduction 95% CI −0.04 to 0.31. Equal country × label weighting also shrinks the countries
  that dominate the data.
- **Burn-in.** GMWI2 burn-in error 0.21 → 0.04 (−79%, population-clustered 95% CI 64–85%). Pooled references that
  failed (S4) included one of about 4,000 healthy people. With 100 labelled local controls, sensitivity was 0.25.
- **Binomial check.** An exact binomial test on 100 local healthy people flags, on average, 98% of LASSO atlas pairs
  (97% for RF) whose FPR exceeds 0.25. This uses observed atlas FPRs as true values, which is mildly optimistic. At
  fixed true FPRs the power is 0.35 (FPR 0.20), 0.79 (0.25) and 0.97 (0.30) (H₀: FPR ≤ 0.15, level 0.05, reject at
  ≥ 22 flagged; `v5/posthoc_r18_checks.py`).
- **Taxon share.** The 39% is the sum of the five largest taxon contributions (weight × difference in carriage) divided
  by the sum over all 95 taxa, i.e. the net East Asian–other gap in mean score. As a share of the negative
  (gap-widening) contributions only, the same five taxa give 35%.
- **Burn-in, unit level.** 28/28 is at classifier level; at the level of the 646 classifier × population × split units,
  74.6% improved. All within-site burn-in tests used healthy-only groups (no patients); the effect of patients in the
  burn-in group rests on three case–control cohorts (Figure 3B; S4).

### S2.3 Fold-model check for all 28 classifiers (post hoc; `v5/posthoc_r20_perfold.py`, `v5/posthoc_r19_foldmodel.py`)
The cut-off is the 90th percentile of out-of-fold control scores, but populations were scored with the model refitted
on all training data, as a developer would release it. Plan v4 P7 checked this for the three-disease analysis only. We
refitted all 28 classifiers exactly as in the atlas (scores reproduced to 9 × 10⁻¹⁶) and rescored the same people with
the cross-validation fold models in two ways.

| Strict set, 978 classifier–population pairs | Refit model (main text) | Per-fold flags, averaged (primary check) | Mean-logit ensemble of fold models |
|---|---|---|---|
| Pairs outside 0.05–0.15 | 70% | 65% | 70% |
| Pairs below 0.05 | 34% | 27% | 43% |
| Pairs above 0.15 | 36% | 38% | 27% |
| LASSO pairs above 0.25 | 26% | 19% | 15% |
| Classifiers with I² ≥ 0.5 (median I²) | 28 (0.94) | 28 (0.91) | 26 (0.92) |
| Largest FPR, populations ≥ 100 (LASSO) | 0.87 (0.77) | 0.80 (0.54) | 0.83 (0.65) |
| Spearman ρ, AUROC vs τ (P) | −0.06 (0.76) | 0.41 (0.032) | 0.23 (0.23) |

- **Per-fold flags** are the closer comparator: each fold model is the scorer whose out-of-fold scores set the cut-off.
  Each person is flagged by every fold model and the flags are averaged (an expected FPR over fold models). The
  mean-logit ensemble averages scores before thresholding, which shrinks extreme scores and pushes FPRs down; it was
  our first check (review r19) and is kept for completeness.
- **Pooled FPRs** of some LASSO classifiers move (per-fold: fatty liver 0.26 → 0.08, impaired glucose tolerance 0.42 →
  0.29, hypertension 0.14 → 0.17); RF changes little. Per-pair FPRs under refit and per-fold scoring correlate
  (Spearman 0.90).
- **In-sample check.** The refitted models flag a median of 0.4% of their own training controls at the cut-off (range
  0–14%). This is uninformative for RF, which fits its training data almost perfectly (13 of 14 RF values are 0).
- **Interpretation.** The population dependence and its heterogeneity do not depend on the refit model. The extreme
  values and the AUROC correlation do: with per-fold scoring, classifiers with higher AUROC spread more, not less. A
  developer who releases a refitted model with a cross-validated cut-off ships this mismatch; the main text reports
  the refit model and this check.

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
| v5/protocol_v5.md, Addendum A | replication H5/H6 | H5 inconclusive (primary, LASSO); RF supported as a secondary result; H6 inconclusive |
| v6/protocol_v6.md | GMWI2 audit G1–G4 | G1, G2, G4 supported; G3 falsified |
| v6/protocol_v6b.md | case-mix retraining B1–B4 | B1 and B4 (logit scale) supported; B2 supported on the point estimate only (CI 41–149% includes values below the criterion); B3 falsified |
| v6/protocol_v6c.md | balancing the 5 disease tests C1–C3 | written before running but committed together with its results, so treated as POST HOC; C1 logit-scale only (not on the FPR scale); C2 and C3 failed; C1–C3 uninterpretable because the implementation deviated from the plan (S6.6) |

Deviations:
- v4 D1–D4 are listed in v4/protocol_v4.md.
- The strict set and the extended covariate model were not pre-specified.
- Geography and distance analyses are exploratory unless covered by Addendum A.
- **Burn-in (H4) implementation choices not fixed by the plan.** The code uses populations of at least 120 people
  (accession-order design), while plan v4 P4(a) asked for at least 150 for the covariate halves; the sex split (women →
  men) of P4(a) was not run. Post hoc check (`v5/posthoc_r18_checks.py`): every covariate-half unit already comes from
  a population of at least 251 people, so restricting the covariate halves to n ≥ 150 changes nothing (646 units, 13
  populations, 0.101 → 0.038, 28/28).
- **Motivation recorded in the plan files.** Plans v6 and v7 state that they were written in response to internal
  review rounds of earlier drafts (simulated editor and reviewer checks used while preparing the manuscript). The plans
  were committed before the analyses they specify were run; their text is unchanged.
- **Holm families.** In plan v6, Holm covers the tests with a P value (G2–G4); G1 (heterogeneity, judged by I²) has no
  P value and is not in the family. In plan v7, the Holm family was kept as planned (H2 and H4–H6), although H4–H6 are
  not interpreted after the failed Q2 gate; H2 has the largest P in its family, so its adjusted P equals its raw P.
- Failed development attempts are recorded in the repository (state/variants_tried.csv); this includes geography-stable feature
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
commit 87fe9f6); the R script was not executed. Code: `v7/run_gmhi.py`; post hoc: `v7/posthoc_gmhi_matching.py`,
`v7/posthoc_gmhi_names.py`.

**Q1 (passed).** On the developers' example our GMHI equals their output (max |difference| 4.9e-15).

**Training FPR.** alpha_GMHI = 0.236: share of the 2,636 healthy samples in the developers' data with GMHI < 0
(20 exact zeros counted as not flagged).

**Developers' own data (pre-specified; not affected by the issues below).**
- H1 heterogeneity: I² 0.96 over 21 studies with ≥ 20 healthy people (share flagged 0.03–0.90). Supported.
- H2 East Asian excess: median 0.67 (8 studies) vs 0.21 (13); one-sided Mann–Whitney
  P = 0.0007, Holm-adjusted 0.0007. Supported.

**Overlap with GMWI2 (post hoc).** 83% of GMHI's 2,636 healthy training samples are also GMWI2 training samples
(BioSample accessions; `v7/posthoc_gmhi_gmwi2_overlap.py`), and 15 of the 21 studies are mostly shared. H2 is therefore a
replication in a second model on largely shared data. In the 6 studies not shared with GMWI2: East Asian median
0.63 (3 studies) vs 0.17 (3); one-sided P = 0.10 (underpowered).

**curatedMetagenomicData part: Q2 failed; H3–H6 not interpreted.** Deviation found on re-checking, after the
pre-specified results had been seen (so the decision not to interpret H3–H6 was itself taken after seeing results; it
moves the paper towards claiming less): the plan matched samples
by accession, but the developers record BioSample accessions and curatedMetagenomicData records sample names and run
accessions, so the original run matched only 2 studies (101 samples; r = 0.80) and misclassified at least 10
"unseen" strict populations as unseen (corrected: 24 of 36 unseen). Matching also through the developers'
sample titles and subject IDs (post hoc) gives 2,190 samples in 19 studies: Pearson r = 0.795 (gate ≥ 0.80: failed),
within-study r = 0.71. Following the plan, H3–H6 are reported only for completeness and are not interpreted
(original run: H3 I² 0.96; H4 26/34 outside the band; H5 Spearman ρ with GMWI2 0.70; H6 burn-in error
0.26 → 0.05). Exact zeros (no MH or MN species detected) were counted as not flagged; there are
137 in the strict set, concentrated in non-industrialised populations (e.g. SmitsSA_2017 29/31, PasolliE_2019 17/111, RubelMA_2020 17/76, RampelliS_2015 16/33),
which the plan required to be reported separately.

**Why Q2 fails (post hoc).** Four of the seven health-prevalent species (Alistipes senegalensis, Bacteroidales bacterium
ph8, Lachnospiraceae bacterium 8_1_57FAA, Sutterella wadsworthensis) and 13 of the 43 health-scarce species do not occur
under these names in any of the 61 curatedMetagenomicData studies (MetaPhlAn3); four health-scarce species have clear
new names, and renaming them changed little. On the 2,190 matched samples the share flagged was 23% with the
developers' MetaPhlAn2 profiles and 43% with curatedMetagenomicData MetaPhlAn3 profiles; per study the shift ranged from
0 to 74 percentage points (Spearman ρ of study flag rates across versions 0.69; Figure S2B).

**Additional checks (post hoc; `v7/posthoc_r16_sensitivity.py`,
`v7/results/posthoc_r16_sensitivity.json`).**
- *Uncertainty of the Q2 correlation.* A study-clustered bootstrap (2,000 resamples of the 19 studies, seed 100) gives a
  95% CI for r of 0.69–0.86; 37% of resamples reach the 0.80 gate. The gate is therefore not distinguishable from its
  threshold either way, and we follow the plan's point-estimate rule (not interpreted).
- *Mongolia counted as East Asian.* One study per index is from Mongolia (share flagged: GMWI2 0.05, GMHI 0.07).
  Counting it as East Asian gives GMWI2 median 0.61 (14 studies) vs 0.13 (30), two-sided P = 5 × 10⁻⁶; GMHI 0.65 (9) vs
  0.23 (12), one-sided P = 0.010. Both contrasts remain.
- *Superseded fields.* `gmhi_results.json` (pre-specified run) reports Q2 as passed (r = 0.803, n = 101) and lists 15
  missing health-scarce species (first study only). Both fields are superseded by `posthoc_gmhi_matching.json` and
  `posthoc_gmhi_names.py` (13 of 43 across all 61 studies); see `v7/results/README.md`.

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

### Table S27. The same samples scored from two profiler versions (studies with ≥ 20 matched healthy samples)

| study               |   n |   flag_dev |   flag_cmd | country   |   shift |
|:--------------------|----:|-----------:|-----------:|:----------|--------:|
| HMP_2012            |  85 |      0.294 |      0.647 | USA       |   0.353 |
| JieZ_2017           |  85 |      0.824 |      0.941 | CHN       |   0.118 |
| LeChatelierE_2013   | 217 |      0.194 |      0.382 | DNK       |   0.189 |
| LiJ_2017            |  35 |      0.314 |      0.857 | CHN       |   0.543 |
| Obregon-TitoAJ_2015 |  29 |      0.655 |      0.655 | PER       |   0     |
| QinJ_2012           | 115 |      0.809 |      0.948 | CHN       |   0.139 |
| QinN_2014           | 100 |      0.41  |      0.94  | CHN       |   0.53  |
| RaymondF_2016       |  23 |      0.174 |      0.913 | CAN       |   0.739 |
| SchirmerM_2016      | 451 |      0.102 |      0.146 | NLD       |   0.044 |
| VogtmannE_2016      |  51 |      0.588 |      0.824 | USA       |   0.235 |
| ZeeviD_2015         | 883 |      0.088 |      0.322 | ISR       |   0.233 |
| ZellerG_2014        |  61 |      0.459 |      0.59  | FRA       |   0.131 |
