# Protocol v3 - Healthy-population false-positive atlas (written 2026-11-24 BEFORE any atlas result was computed)

## Why (novelty escalation, round 3)
Rounds 1-2 (both earlier lines) showed: thresholds drift between case-control cohorts; label-free fixes fail; local
controls + conformal fix it. The fix is textbook. Score 12-15/30. The weakest point is *insight and scale*: 16-20
case-control cohorts cannot say WHO gets over-flagged or WHY. New idea: apply each disease classifier to every adult
healthy control in curatedMetagenomicData that the classifier never saw (62 cohorts, ~10,000 people, 25 countries,
12 non-westernised populations) and measure the false-positive rate as a property of the population.

## Classifiers (fixed, unchanged settings from protocol v2)
CRC (10 cohorts, ThomasAM_2019_c removed), IBD (4), T2D (4): LASSO and RF; threshold = 90th percentile of
leave-one-cohort-out out-of-fold training-control scores (target FPR alpha=0.10). Feature space = species present in >5% of
training samples; missing species in a reference cohort = 0 (same MetaPhlAn3 database for all).

## Reference populations
Adult/senior stool samples with study_condition == "control", one per subject (first time point), from studies with
>= 20 such samples, EXCLUDING every study used to train that classifier. Within-study near-duplicates removed (r>0.99).

## Hypotheses and falsifiers (stated before results)
- A1 (heterogeneity): cohort-level FPR in healthy populations is overdispersed vs binomial(alpha=0.10).
  WRONG if chi-square heterogeneity P > 0.05 for the LASSO CRC classifier.
- A2 (shared propensity): cohorts over-flagged by one disease test are over-flagged by the others (Spearman of cohort FPR
  between CRC and IBD and between CRC and T2D tests >= 0.3). WRONG if both rho < 0.3 or CIs include 0.
- A3 (equity): non-westernised populations have higher FPR than westernised populations for the CRC classifier.
  WRONG if the cohort-level difference is <= 0 or the Mann-Whitney P > 0.05. (Direction pre-specified: higher.)
- A4 (between-cohort dominance): after adjusting for individual age, sex, BMI and log sequencing depth, the between-cohort
  variance of the latent flag propensity remains (ICC >= 0.10). WRONG if ICC < 0.05.
- A5 (fix): a threshold from n local healthy controls (conformal) gives cohort FPR within [0.05,0.15] in >= 90% of
  cohorts at n=100; a lifestyle/country-matched external reference (other cohorts of same country) does not.
Secondary/descriptive: taxon decomposition of the cohort mean score shift (LASSO, w_j * delta mean_j); FPR vs mean age,
depth, BMI, country.
Every analysis not listed above is labelled post hoc.
