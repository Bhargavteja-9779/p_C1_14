# Analysis plan v4 (review round 2 revision) — written 2026-11-24 BEFORE any v4 result was computed

Status of what came before: the v3 atlas and the v3 locked burn-in run were done once and are kept unchanged on disk
(../results/). Review round 2 found cross-cohort duplicated people and an evaluation that is exchangeable by
construction. This plan fixes the data, adds tests that can fail, and is committed to git before it is run.
It is an internal analysis plan (not an external pre-registration). No classifier, cut-off rule, N grid, alpha, or
method is changed. Every analysis below is run once; bugs fixed afterwards are logged in DEVIATIONS at the end.

## P0. Global cross-cohort de-duplication (profiles only, no labels/outcomes used)
Pool every stool profile used anywhere: all samples of the case-control training cohorts (CRC, IBD, T2D incl. cases)
plus all adult healthy-population samples (one per subject, within-cohort near-duplicates already removed).
Two samples from different studies with log-profile Pearson r > 0.99 (same transform as src/data.py) are one person.
Rules: (i) the copy in a case-control (disease) study is kept; the copy in the other study is removed everywhere;
(ii) if both copies are in healthy-only studies, the copy in the smaller study is removed; (iii) a healthy population
that loses ≥50% of its samples is dropped whole (expected: ThomasAM_2019_c). Output: v4/results/duplicates.csv,
v4/results/excluded_samples.txt. All v4 analyses use the de-duplicated data.

## P1. Strict healthy subset (primary) and full set (sensitivity)
Person level (strict): disease == "healthy"; antibiotics_current_use != "yes"; pregnant != "yes"; family_role empty;
lactating != "yes". Study level (strict): drop studies whose controls are not general-population adults:
VincentC_2016 (hospital inpatients), MetaCardis_2020_a (metabolic-disease-enriched), FengQ_2015, LoombaR_2017, YuJ_2015,
ThomasAM_2018a (comorbidity-enriched controls), BackhedF_2015, YassourM_2018, FerrettiP_2018, ShaoY_2019,
TettAJ_2019_a/b/c (mothers / pregnancy cohorts), RaymondF_2016 (antibiotic trial), HMP_2019_ibdmdb, IjazUZ_2017
(symptomatic referrals / IBD kindred), ZellerG_2014, VogtmannE_2016, HanniganGD_2017 (colonoscopy-referred),
CosteaPI_2017 (longitudinal methods set). (20 studies; list taken from the round-2 domain report, which named them
from recruitment descriptions, not from FPR.) A population enters an analysis if it has ≥ 20 people after filtering.
Full set = v3 inclusion after P0. Both are reported; strict is primary because it matches the question
"what happens in a general healthy population". This choice is made after seeing v3 results and is disclosed.

## P2. Heterogeneity (primary statistics for the atlas)
Per classifier (3 diseases × LASSO/RF), per population: realised FPR at the frozen source cut-off.
DerSimonian–Laird random effects on logit FPR (0.5 continuity correction): pooled FPR, tau, I², 95% prediction
interval. Out-of-band share (FPR outside 0.05–0.15) observed vs expected under perfect calibration (each population
Binomial(n, 0.10)); excess = observed − expected. Ranges reported for populations with n ≥ 100.
Also the 10th–90th percentile of population FPR (replaces "ten-fold").

## P3. Covariates (A4 as specified + extended)
As specified: linear mixed model of standardised score on age, sex, BMI, log10 depth with population random intercept,
vs intercept-only on the same people. Extended (deviation, disclosed): + Shannon, richness. Report n people, n
populations used (vs available), ICC raw/adjusted, change in between-population variance with its sign.

## P4. Burn-in under NON-exchangeable splits (the test that can fail)
Frozen rules: BURN (k = ceil((N+1)(1−alpha))), BURN-PAC (delta 0.05), SRC; alpha = 0.10; healthy people only (pi = 0).
Units (both DEV and LOCKED populations, since no method is tuned here):
 (a) within-population covariate shift: populations with n ≥ 150 and the covariate available for ≥ 80%: burn-in drawn
     at random (N = 50, 100) from the lower half of age, evaluate on the upper half; same for BMI; sex: women → men
     and men → women (each side ≥ 60). R = 200 draws.
 (b) within-study sub-sites: MetaCardis_2020_a Leipzig/Copenhagen/Paris (6 ordered pairs), AsnicarF_2021 GBR↔USA,
     BritoIL_2016 village_1↔village_5, LiuW_2016 westernised↔non-westernised. N = 50, 100 where the burn-in side allows
     N + 0 and the evaluation side has ≥ 40. R = 200.
 (c) neighbouring site: burn-in from population A, evaluate on all of population B, A ≠ B from the same country
     (strict set; both n ≥ 60). N = 50, 100. R = 200.
 (d) accession order: burn-in = first N by NCBI accession (then sample_id) order, evaluate on the rest (1 draw).
Reference: the same population under random splits (the v3 design).
Endpoints: mean |FPR − 0.10|, P(FPR > 0.15), mean FPR, per unit, then averaged over units (each unit weight 1) and
summarised by distinct population with a population-cluster bootstrap (B = 2000).
Pre-stated hypotheses (stated before running):
 H-NX1 (a)+(b)+(d): BURN(N=100) mean |FPR−0.10| is ≥ 50% lower than SRC, and P(FPR>0.15) ≤ 0.20.
 H-NX2 (c): burn-in at a neighbouring site of the same country does NOT keep P(FPR > 0.15) ≤ 0.20 (i.e., local means local).
Either outcome is reported.

## P5. Label-free batch-correction comparator (ComBat-style location–scale alignment)
At a new population, take the same N burn-in people; for each model feature (log10 abundance, as in the pipeline),
shift and scale the burn-in features so their mean/SD equal the training controls' mean/SD; apply the same map to the
evaluation people; score with the unchanged model and the unchanged SRC cut-off. Label-free like BURN.
(MMUPHin/ConQuR/DEBIAS-M need batch labels with cases or retraining and are not run; stated as a limitation.)
Evaluated with the P6 random-split design, N = 100, R = 200, same populations. Pre-stated: BURN mean |FPR−0.10| lower than
ALIGN with population-cluster bootstrap 95% CI of the difference excluding 0.

## P6. Corrected re-analysis of the v3 endpoints (same code paths, de-duplicated data)
Atlas (A1–A3 descriptive), deploy healthy (SRC/ATLAS/BURN/BURN-PAC, N ∈ {25,50,100,200}, R = 200, same seeds) and
contaminated pools (same design), control augmentation head-to-head. The v3 success criterion is re-evaluated, with the
honest note that P(FPR>0.15) for BURN and P(FPR>0.10) for BURN-PAC under random splits are fixed by N and M (calibration
check of the code, not evidence). Inference on BURN − SRC and BURN − augmentation: population-cluster bootstrap
(B = 2000) and population-level sign test; number of distinct populations reported.

## P7. Fold-model scoring check
Re-score healthy populations with the mean logit of the inner leave-one-cohort-out fold models (the models that
produced the OOF scores behind the cut-off) and report pooled and per-population FPR vs the refit model.

## P8. Taxon decomposition (pre-specified secondary in protocol_atlas.md, not yet reported)
LASSO only: population logit-score shift vs training controls = Σ_j w_j Δz̄_j; top 8 taxa for the 3 most over-flagged
populations per disease (strict set), and share of the shift from taxa with oral habitat (list fixed in code before run).

## P9. Clinical translation numbers
PPV at 0.5% and 1% prevalence from the locked case-control sensitivity/FPR of SRC and BURN (N = 100).

## DEVIATIONS (filled in after running)
