# Supplementary tables

## Table S1. Held-out cohorts and AUROC
CRC: trained on 8 development cohorts. Others: leave-one-cohort-out. Cohort-std = features standardised within cohort.

| task | cohort | controls | cases | AUROC LASSO | AUROC RF | AUROC LASSO (cohort-std) | AUROC RF (cohort-std) |
|---|---|---|---|---|---|---|---|
| CRC | ThomasAM_2019_c | 40 | 40 | 0.833 | 0.795 | 0.797 | 0.801 |
| CRC | YachidaS_2019 | 251 | 258 | 0.731 | 0.696 | 0.711 | 0.711 |
| CRC | YuJ_2015 | 54 | 74 | 0.859 | 0.854 | 0.855 | 0.849 |
| IBD | HMP_2019_ibdmdb | 27 | 103 | 0.725 | 0.712 | 0.755 | 0.695 |
| IBD | HallAB_2017 | 12 | 20 | 0.700 | 0.658 | 0.717 | 0.796 |
| IBD | IjazUZ_2017 | 38 | 12 | 0.853 | 0.820 | 0.807 | 0.851 |
| IBD | NielsenHB_2014 | 59 | 82 | 0.696 | 0.668 | 0.718 | 0.728 |
| T2D | KarlssonFH_2013 | 43 | 53 | 0.624 | 0.692 | 0.607 | 0.626 |
| T2D | MetaCardis_2020_a | 642 | 550 | 0.636 | 0.644 | 0.640 | 0.634 |
| T2D | QinJ_2012 | 174 | 170 | 0.627 | 0.580 | 0.594 | 0.587 |
| T2D | SankaranarayananK_2015 | 18 | 19 | 0.576 | 0.576 | 0.482 | 0.573 |
| adenoma | FengQ_2015 | 61 | 47 | 0.604 | 0.558 | 0.608 | 0.607 |
| adenoma | HanniganGD_2017 | 28 | 26 | 0.596 | 0.570 | 0.607 | 0.532 |
| adenoma | ThomasAM_2018a | 24 | 27 | 0.650 | 0.535 | 0.636 | 0.627 |
| adenoma | YachidaS_2019 | 251 | 67 | 0.595 | 0.562 | 0.600 | 0.572 |
| adenoma | ZellerG_2014 | 61 | 42 | 0.591 | 0.543 | 0.577 | 0.604 |

## Table S2. Over-dispersion of realised FPR under the transferred threshold
Chi-square of observed false positives (all controls of each held-out cohort) against Binomial(n_controls, alpha); df = number of cohorts.

| alpha | task | model | cohorts | realised_FPR_range | chi2 | P |
|---|---|---|---|---|---|---|
| 0.100 | CRC | lasso | 3 | 0.11–0.28 | 29.500 | 1.8e-06 |
| 0.100 | CRC | rf | 3 | 0.13–0.30 | 43.600 | 1.8e-09 |
| 0.100 | IBD | lasso | 4 | 0.05–0.41 | 30.000 | 4.9e-06 |
| 0.100 | IBD | rf | 4 | 0.02–0.33 | 18.600 | 0.00096 |
| 0.100 | T2D | lasso | 4 | 0.05–0.59 | 495.900 | 5.1e-106 |
| 0.100 | T2D | rf | 4 | 0.00–0.73 | 823.500 | 6.1e-177 |
| 0.100 | adenoma | lasso | 5 | 0.04–0.26 | 21.400 | 0.00069 |
| 0.100 | adenoma | rf | 5 | 0.00–0.14 | 23.700 | 0.00025 |
| 0.050 | CRC | lasso | 3 | 0.04–0.28 | 81.400 | 1.5e-17 |
| 0.050 | CRC | rf | 3 | 0.06–0.15 | 28.500 | 2.9e-06 |
| 0.050 | IBD | lasso | 4 | 0.03–0.08 | 1.200 | 0.88 |
| 0.050 | IBD | rf | 4 | 0.02–0.22 | 22.100 | 0.00019 |
| 0.050 | T2D | lasso | 4 | 0.03–0.52 | 846.700 | 6e-182 |
| 0.050 | T2D | rf | 4 | 0.00–0.66 | 1404.800 | 6.4e-303 |
| 0.050 | adenoma | lasso | 5 | 0.00–0.20 | 32.900 | 4e-06 |
| 0.050 | adenoma | rf | 5 | 0.00–0.04 | 9.700 | 0.084 |

## Table S3a. Pooled endpoints, target FPR = 0.1
Band = [alpha/2, 1.5 alpha]. A threshold of +inf (too few controls for the rule) gives FPR 0 and sensitivity 0.

| method | pairs | share_in_band | min_cohort_FPR | max_cohort_FPR | mean_sens | P_split_FPR_gt_1p5a | P_split_FPR_le_a |
|---|---|---|---|---|---|---|---|
| anchor_loc_n10 | 28 | 0.429 | 0.008 | 0.289 | 0.358 | 0.389 | 0.448 |
| anchor_loc_n20 | 20 | 0.400 | 0.002 | 0.291 | 0.368 | 0.449 | 0.342 |
| anchor_loc_n30 | 12 | 0.500 | 0.000 | 0.294 | 0.267 | 0.373 | 0.357 |
| anchor_locscale_n10 | 28 | 0.429 | 0.056 | 0.336 | 0.389 | 0.476 | 0.396 |
| anchor_locscale_n20 | 20 | 0.500 | 0.062 | 0.328 | 0.360 | 0.427 | 0.398 |
| anchor_locscale_n30 | 12 | 0.833 | 0.055 | 0.218 | 0.233 | 0.290 | 0.492 |
| cohortstd | 32 | 0.281 | 0.000 | 0.321 | 0.308 | 0.323 | 0.508 |
| conformal_n10 | 28 | 1.000 | 0.077 | 0.107 | 0.272 | 0.210 | 0.670 |
| conformal_n20 | 20 | 1.000 | 0.082 | 0.113 | 0.283 | 0.191 | 0.634 |
| conformal_n30 | 12 | 1.000 | 0.089 | 0.105 | 0.201 | 0.186 | 0.600 |
| em | 32 | 0.156 | 0.000 | 1.000 | 0.593 | 0.675 | 0.287 |
| pool_q | 32 | 0.281 | 0.000 | 0.244 | 0.142 | 0.081 | 0.840 |
| site_shift | 32 | 0.656 | 0.000 | 0.255 | 0.285 | 0.231 | 0.583 |
| source | 32 | 0.312 | 0.000 | 0.726 | 0.386 | 0.384 | 0.496 |
| tong95_n30 | 12 | 0.000 | 0.027 | 0.038 | 0.078 | 0.017 | 0.941 |
| tong95_n50 | 8 | 0.000 | 0.036 | 0.046 | 0.108 | 0.007 | 0.944 |

## Table S3b. Pooled endpoints, target FPR = 0.05
Band = [alpha/2, 1.5 alpha]. A threshold of +inf (too few controls for the rule) gives FPR 0 and sensitivity 0.

| method | pairs | share_in_band | min_cohort_FPR | max_cohort_FPR | mean_sens | P_split_FPR_gt_1p5a | P_split_FPR_le_a |
|---|---|---|---|---|---|---|---|
| anchor_loc_n10 | 28 | 0.286 | 0.000 | 0.227 | 0.278 | 0.424 | 0.451 |
| anchor_loc_n20 | 20 | 0.350 | 0.000 | 0.231 | 0.291 | 0.515 | 0.357 |
| anchor_loc_n30 | 12 | 0.333 | 0.000 | 0.226 | 0.191 | 0.515 | 0.319 |
| anchor_locscale_n10 | 28 | 0.250 | 0.010 | 0.271 | 0.314 | 0.492 | 0.402 |
| anchor_locscale_n20 | 20 | 0.400 | 0.035 | 0.272 | 0.283 | 0.466 | 0.421 |
| anchor_locscale_n30 | 12 | 0.667 | 0.028 | 0.190 | 0.156 | 0.372 | 0.472 |
| cohortstd | 32 | 0.125 | 0.000 | 0.279 | 0.243 | 0.401 | 0.500 |
| conformal_n10 | 28 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| conformal_n20 | 20 | 1.000 | 0.038 | 0.052 | 0.179 | 0.213 | 0.677 |
| conformal_n30 | 12 | 1.000 | 0.025 | 0.034 | 0.076 | 0.104 | 0.780 |
| em | 32 | 0.125 | 0.000 | 1.000 | 0.558 | 0.659 | 0.325 |
| pool_q | 32 | 0.281 | 0.000 | 0.221 | 0.075 | 0.092 | 0.822 |
| site_shift | 32 | 0.344 | 0.000 | 0.222 | 0.205 | 0.269 | 0.578 |
| source | 32 | 0.312 | 0.000 | 0.658 | 0.304 | 0.381 | 0.505 |
| tong95_n30 | 12 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |
| tong95_n50 | 8 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 |

## Table S5. SD across held-out cohorts of cohort-mean FPR (alpha = 0.10)

| method | CRC lasso | CRC rf | IBD lasso | IBD rf | T2D lasso | T2D rf | adenoma lasso | adenoma rf |
|---|---|---|---|---|---|---|---|---|
| anchor_loc_n10 | 0.079 | 0.022 | 0.076 | 0.109 | 0.050 | 0.076 | 0.039 | 0.024 |
| anchor_loc_n20 | 0.085 | 0.029 |  |  | 0.060 | 0.071 | 0.029 | 0.034 |
| anchor_loc_n30 |  |  |  |  | 0.086 | 0.032 | 0.028 | 0.035 |
| anchor_locscale_n10 | 0.021 | 0.016 | 0.041 | 0.150 | 0.018 | 0.041 | 0.029 | 0.043 |
| anchor_locscale_n20 | 0.027 | 0.014 |  |  | 0.024 | 0.055 | 0.044 | 0.062 |
| anchor_locscale_n30 |  |  |  |  | 0.018 | 0.002 | 0.044 | 0.068 |
| cohortstd | 0.072 | 0.105 | 0.077 | 0.080 | 0.098 | 0.082 | 0.055 | 0.063 |
| conformal_n10 | 0.010 | 0.009 | 0.005 | 0.003 | 0.008 | 0.013 | 0.010 | 0.008 |
| conformal_n20 | 0.000 | 0.014 |  |  | 0.004 | 0.005 | 0.008 | 0.008 |
| conformal_n30 |  |  |  |  | 0.001 | 0.001 | 0.006 | 0.005 |
| em | 0.243 | 0.241 | 0.434 | 0.467 | 0.224 | 0.331 | 0.371 | 0.346 |
| pool_q | 0.013 | 0.009 | 0.020 | 0.024 | 0.109 | 0.089 | 0.041 | 0.042 |
| site_shift | 0.119 | 0.041 | 0.055 | 0.053 | 0.052 | 0.090 | 0.025 | 0.035 |
| source | 0.085 | 0.092 | 0.172 | 0.151 | 0.258 | 0.338 | 0.088 | 0.062 |
| tong95_n30 |  |  |  |  | 0.001 | 0.002 | 0.005 | 0.001 |
| tong95_n50 |  |  |  |  | 0.001 | 0.002 |  |  |

## Table S4. Post-hoc descriptive analyses (not pre-registered)

```
AUROC vs |FPR-0.10| (32 cohort x model): Spearman rho=-0.18, P=0.31
LASSO vs RF realised FPR across 16 held-out cohorts: rho=0.69, P=0.0029
Shift of median control score (target - training, logit) vs realised FPR: rho=0.80, P=3e-08
```