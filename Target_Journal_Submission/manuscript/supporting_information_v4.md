# Supporting Information (v4)

Tables S1–S11 are in `si_tables_v4.md` (generated from result files by `code/experiments/atlas/v4/make_si_v4.py`).
Figure S1 is `figures_v4/FigureS1_atlas_rf_strict.pdf`. Code paths are relative to `Target_Journal_Submission/code/`.

## S1. Methods

### Data
Species-level relative abundances (MetaPhlAn3) and sample metadata came from curatedMetagenomicData: release
2021-03-31 for all cohorts, release 2022-10-19 for MetaCardis_2020_a. The exact metadata file used is deposited in
the repository (`data/sampleMetadata.csv.gz`, SHA-256 recorded). Two healthy cohorts listed in the metadata
(BedarfJR_2017, PehrssonE_2016) have no abundance table in the release and were not used.

### Training cohorts and classifiers
CRC: FengQ_2015, GuptaA_2019, HanniganGD_2017, ThomasAM_2018a, ThomasAM_2018b, VogtmannE_2016, WirbelJ_2018,
YachidaS_2019, YuJ_2015, ZellerG_2014. IBD: HMP_2019_ibdmdb, HallAB_2017, IjazUZ_2017, NielsenHB_2014. T2D:
KarlssonFH_2013, MetaCardis_2020_a, QinJ_2012, SankaranarayananK_2015. We kept stool samples labelled case or control
and one sample per subject (first time point). Within-cohort near-duplicate profiles were removed.
Features were log10(relative abundance/100 + 10⁻⁵) for taxa present in more than 5% of training samples, z-scored with
training means and SDs. LASSO logistic regression: L1 penalty, C = 0.1, balanced class weights (scikit-learn,
liblinear). Random forest: 500 trees, minimum leaf size 2, balanced-subsample class weights. Settings were fixed in
advance and not tuned. Scores are on the logit scale.

### Cut-off (status quo, "training cut-off")
The 90th percentile of leave-one-cohort-out out-of-fold scores of training controls (target FPR α = 0.10), following
Wirbel et al. (2019). The final model was refitted on all training data. Check P7: scoring with the mean logit of the
fold models instead moved the pooled FPR by at most 0.04 (Table S2, columns *_folds).

### Healthy populations
Adult or senior stool samples with study_condition = control from cohorts with at least 20 such people, one per
person, excluding every cohort used to train that classifier.

**De-duplication (P0).** All profiles used anywhere (training cases and controls, healthy populations) were compared
across cohorts. Pairs with log-profile Pearson r > 0.99 were treated as one person. The copy in the case–control study
was kept. If both copies were in healthy-only cohorts, the copy in the smaller cohort was removed. A cohort that lost at
least 50% of its people was dropped. Result: 119 samples removed (ThomasAM_2019_c = YachidaS_2019, all 80; DhakanDB_2019
copies of GuptaA_2019; JieZ_2017 copies of QinJ_2012), ThomasAM_2019_c dropped (Table S7). No duplicates were found
between case–control cohorts.

**Strict set (primary; P1).** Person level: disease recorded as healthy, not on antibiotics, not pregnant or lactating,
no family role recorded (mothers in mother–infant studies). Study level: 20 cohorts whose controls are not general
population adults were excluded. These were hospital in-patients, metabolic-disease-enriched or comorbidity-enriched
controls, mothers in pregnancy or postpartum studies, an antibiotic trial, symptomatic referrals or IBD kindred,
colonoscopy-referred people, and a longitudinal methods set (Table S1). Populations need at least 20 people after
filtering. The list came from recruitment descriptions, not from FPRs, but it was made after the v3 results were known.
The full de-duplicated set is the sensitivity analysis.

### Atlas statistics (P2)
For each classifier and population we computed the realised FPR. Heterogeneity: DerSimonian–Laird random effects on
logit FPR (0.5 continuity correction), with pooled FPR, τ, I², Cochran's Q and a 95% prediction interval (t with k − 2
df). Out-of-band share (FPR outside 0.05–0.15) was compared with its expectation under perfect calibration: for each
population, P(Binomial(n, 0.10)/n outside the band), averaged. We also report ranges for populations with n ≥ 100, and
10th–90th percentiles.

### Covariates (P3)
Linear mixed models of the standardised score with a random intercept per population, fitted in statsmodels.
As specified: age, sex, BMI and log10 read depth. Extended (deviation): + Shannon diversity and richness. People with
missing covariates were dropped. Populations with fewer than 10 complete records were dropped. ICC = between variance /
(between + residual).

### Pre-specified atlas hypotheses (protocol_atlas.md)
A1: overdispersion (χ² against Binomial(0.10)). A2: Spearman correlation of population FPR between tests (bootstrap
95% CI). A3: non-westernised > westernised FPR for the CRC test (one-sided Mann–Whitney on population FPRs). A5: labelled
local controls (n = 100, conformal quantile, 200 random draws) put the mean FPR in 0.05–0.15 in ≥ 90% of populations,
while a reference pooled from the other cohorts of the same country does not. Results: Table S9.

### Taxon decomposition (P8)
For LASSO, a population's mean score shift relative to training controls equals Σ_j w_j (z̄_j,pop − z̄_j,train controls).
Oral genera were fixed in code before the run (taxa_v4.py). Results: Table S8, Figure 2.

### Burn-in rules
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

### Statistics and inference
Units that share a population are not independent. Confidence intervals therefore come from a population-cluster
bootstrap (2,000 resamples of distinct evaluation populations). Tests are Wilcoxon signed-rank tests on population
means. We report the number of distinct populations behind every comparison. Holm correction was applied across the 11
population-level P values reported in the main text (Table S10). Under random splits, the share of burn-ins with
FPR > 0.15 follows a beta-binomial law whatever the data. This only checks the implementation; it is not evidence about
exchangeability.

### Software and reproducibility
Python 3.13; packages are pinned in `code/requirements.txt`. Seeds are derived from names, so runs are deterministic.
Run order: `code/experiments/atlas/v4/README.md`. Data rebuild: `scripts/rebuild_cache.sh`. Number audit:
`scripts/audit_numbers.py` checks every number in the manuscript against the result files.

## S2. Analysis plans and deviations
The analysis plans are `code/experiments/atlas/protocol_atlas.md` (atlas, A1–A5), `atlas_split.md` (DEV/LOCKED cohort
split), `protocol_deploy.md` (v3 burn-in evaluation) and `v4/protocol_v4.md` (this revision). Each was committed to git
before the analysis it governs. They are internal plans, not external pre-registrations.
Deviations:
- D1: oral-genus matcher bug fixed before interpretation.
- D2: random-split design uses all de-duplicated people of a population; strict filtering is applied at study level only.
- D3: non-random designs (a), (b) and (d) use the full set.
- D4: A1–A5 re-tested in v4, and A5 reported for the first time.
- Extended covariate model (Shannon, richness) not pre-specified.
- Strict set chosen after the v3 results.
- Control augmentation and ALIGN are comparators added in revision. ALIGN was pre-stated in protocol_v4 before running.

## S3. Revision history (what a first internal review changed)
Manuscript v3 reported FPRs of 0–87% across 60 cohorts and 8,329 people. It also called the close fit of the
beta-binomial law evidence of exchangeability, and reported burn-in versus control augmentation as P = 0.0004. An
internal statistical review found the following problems.
- Cross-cohort duplicates (above), one of which made augmentation look like it repaired GuptaA_2019 through leakage.
- Non-healthy "controls", including the 0.87 maximum, which came from hospital in-patients (VincentC_2016).
- A validation that was true by construction.
- Units that repeated the same seven populations.

v4 corrects all four. It also adds non-random splits, a batch-correction comparator, population-level inference, Holm
correction and the taxon decomposition. The v3 files are kept unchanged in `code/experiments/atlas/results/`.

## S4. What we tried that did not work (summary of Table S3)
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

## S5. Earlier case–control analysis (v1–v2)
The first version of this work studied threshold transfer within case–control cohorts (CRC leave-one-study-out). Its
methods, results and review history are archived unchanged in `supporting_information.md`, `si_tables.md` and
`code/experiments/final/`. Two of its findings carry over:
- AUROC did not predict the FPR error (Spearman ρ = −0.18);
- controls borrowed from another site did not fix the cut-off.
