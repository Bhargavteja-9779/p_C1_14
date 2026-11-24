# 2026-11-24 — RESULT / SURPRISE (atlas after dedup + strict healthy subset)
Files: Target_Journal_Submission/code/experiments/atlas/v4/results/{heterogeneity_v4.csv, covariates_v4.csv, atlas_perpop_v4.csv}
- Dedup removed 119 samples (DhakanDB copies of GuptaA 60, JieZ copies of QinJ 97 pairs, ThomasAM_2019_c = Yachida, dropped).
- Strict subset (general-population healthy adults): 32-35 populations, 6,157-6,466 people per classifier.
  Heterogeneity stays: I2 0.70 (CRC RF) to 0.95 (IBD), tau 0.55-1.44 on the logit scale, all Q p < 1e-10.
  95% prediction interval for a new population: CRC LASSO 0.013-0.218, CRC RF 0.016-0.144, IBD LASSO 0.011-0.631,
  IBD RF 0.005-0.647, T2D LASSO 0.019-0.543, T2D RF 0.008-0.343.
- Out-of-band share minus what perfect calibration would give by chance: +0.45 to +0.73 (expected by chance 0.15-0.16).
- SURPRISE: the headline extremes of v3 (CRC LASSO 56%, CRC RF 87%) were one hospital cohort. In the strict set the CRC
  tests are, on average, CONSERVATIVE in healthy people (pooled FPR 0.04-0.06 vs 0.10 promised); the heterogeneity runs
  in both directions. IBD and T2D tests have heavy upper tails (max 0.62-0.76).
- Fold-model check (P7): scoring with the fold models moves pooled FPR by <= 0.04 (e.g. CRC LASSO 0.044 -> 0.037);
  the refit-model level shift does not explain the spread.
- Covariates (as specified: age, sex, BMI, depth): between-population variance changes -24% to +28%; ICC 0.15-0.49.
  Individual covariates are often significant, but they do not remove the population effect. Only 24-37 of 32-53
  populations have all four covariates. My v3 sentence "explained none" was wrong in detail (extended model removes
  37-50% for IBD) and is replaced.
