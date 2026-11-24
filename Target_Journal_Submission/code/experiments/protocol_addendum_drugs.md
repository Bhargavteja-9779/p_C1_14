# Protocol addendum A1 - medication analysis (written and committed BEFORE any medication-stratified score was computed)
Date: 2026-11-24. Motivation: development round 9 showed that oral-origin taxa (Streptococcus, Veillonella,
Fusobacterium, ...) drive most CRC-test false alarms in chronic disease. Proton-pump inhibitors (PPIs) are known to
increase oral taxa in the gut (Imhann 2016 Gut; Jackson 2016 Gut). PREDICTION derived from the mechanism, stated
before looking: PPI users receive higher CRC-test scores and are flagged more often, independent of their disease.

Scope note: MetaCardis_2020_a CRC-test scores were already computed in the locked Part B analysis, but no analysis by
medication was done. This addendum is a SECOND, separate pre-specified analysis; it will be reported as such
(not as part of the original frozen protocol).

## Development check (non-locked cohorts with PPI annotation; direction only)
VincentC_2016, LeeKA_2022, JieZ_2017: CRC models (LASSO, RF) trained on the 8 DEV CRC cohorts; within cohort,
score ~ PPI (+ condition where applicable + age/BMI/sex where recorded). Reported regardless of outcome.

## Confirmatory test (MetaCardis_2020_a, adults, one sample per subject, all condition groups incl. controls)
- H5 (primary): CRC-test logit score ~ PPI + condition group (control/IGT/T2D/CAD/HF) + sex + age + BMI (age/BMI only if
  >= 80% recorded) + metformin + statin + aspirin + beta-blocker. PPI coefficient > 0, one-sided alpha = 0.05,
  LASSO primary, RF secondary. Also reported: positivity at the source 90%-specificity cut-off in PPI users vs non-users
  (risk ratio, bootstrap 95% CI).
- H6 (mechanism): the oral-taxa component of the score (sum of coefficient x z-score over the pre-defined oral-origin
  species of the LASSO model; list in explore_v9b_axes.py) is higher in PPI users in the same adjusted model; and the
  PPI coefficient on the total score shrinks when the oral component is added as a covariate (reported descriptively).
- Secondary (exploratory, no hypothesis direction fixed): metformin, statin, aspirin, beta-blocker coefficients from the
  same model.
- Consequence analysis: false alarms per 1,000 screened people attributable to PPI use at an assumed 20-30% PPI
  prevalence at screening age (descriptive).
No other medication analyses will be run on MetaCardis.
