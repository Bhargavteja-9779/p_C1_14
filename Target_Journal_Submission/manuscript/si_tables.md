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

## Table S2. Heterogeneity of realised FPR across held-out cohorts under the transferred threshold
Chi-square test of equal false-positive proportions across cohorts (all controls of each cohort). Replaces the pre-registered test against Binomial(alpha) (see Deviations); a common bias shared by all cohorts (as in external CRC) is not detected by this test.

| alpha | task | model | cohorts | realised_FPR_range | chi2_equal_props | df | P |
|---|---|---|---|---|---|---|---|
| 0.100 | CRC | lasso | 3 | 0.11–0.28 | 4.300 | 2 | 0.12 |
| 0.100 | CRC | rf | 3 | 0.13–0.30 | 4.200 | 2 | 0.12 |
| 0.100 | IBD | lasso | 4 | 0.05–0.41 | 22.300 | 3 | 5.7e-05 |
| 0.100 | IBD | rf | 4 | 0.02–0.33 | 20.500 | 3 | 0.00013 |
| 0.100 | T2D | lasso | 4 | 0.05–0.59 | 296.300 | 3 | 6.3e-64 |
| 0.100 | T2D | rf | 4 | 0.00–0.73 | 510.000 | 3 | 3.3e-110 |
| 0.100 | adenoma | lasso | 5 | 0.04–0.26 | 14.500 | 4 | 0.0058 |
| 0.100 | adenoma | rf | 5 | 0.00–0.14 | 26.400 | 4 | 2.6e-05 |
| 0.050 | CRC | lasso | 3 | 0.04–0.28 | 11.100 | 2 | 0.004 |
| 0.050 | CRC | rf | 3 | 0.06–0.15 | 2.300 | 2 | 0.31 |
| 0.050 | IBD | lasso | 4 | 0.03–0.08 | 1.200 | 3 | 0.76 |
| 0.050 | IBD | rf | 4 | 0.02–0.22 | 14.300 | 3 | 0.0025 |
| 0.050 | T2D | lasso | 4 | 0.03–0.52 | 302.300 | 3 | 3.1e-65 |
| 0.050 | T2D | rf | 4 | 0.00–0.66 | 489.300 | 3 | 9.9e-106 |
| 0.050 | adenoma | lasso | 5 | 0.00–0.20 | 17.300 | 4 | 0.0017 |
| 0.050 | adenoma | rf | 5 | 0.00–0.04 | 7.100 | 4 | 0.13 |

## Table S3a. Pooled endpoints, target FPR = 0.1
Band = [alpha/2, 1.5 alpha]. At alpha=0.05, conformal with n=10 (needs n>=19) and the 95%-confidence rule with n<=50 (needs n>=59) are not feasible and are omitted. The 95%-confidence rule's secondary endpoint is P_split_FPR_le_a (target >= 0.95).

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
Band = [alpha/2, 1.5 alpha]. At alpha=0.05, conformal with n=10 (needs n>=19) and the 95%-confidence rule with n<=50 (needs n>=59) are not feasible and are omitted. The 95%-confidence rule's secondary endpoint is P_split_FPR_le_a (target >= 0.95).

| method | pairs | share_in_band | min_cohort_FPR | max_cohort_FPR | mean_sens | P_split_FPR_gt_1p5a | P_split_FPR_le_a |
|---|---|---|---|---|---|---|---|
| anchor_loc_n10 | 28 | 0.286 | 0.000 | 0.227 | 0.278 | 0.424 | 0.451 |
| anchor_loc_n20 | 20 | 0.350 | 0.000 | 0.231 | 0.291 | 0.515 | 0.357 |
| anchor_loc_n30 | 12 | 0.333 | 0.000 | 0.226 | 0.191 | 0.515 | 0.319 |
| anchor_locscale_n10 | 28 | 0.250 | 0.010 | 0.271 | 0.314 | 0.492 | 0.402 |
| anchor_locscale_n20 | 20 | 0.400 | 0.035 | 0.272 | 0.283 | 0.466 | 0.421 |
| anchor_locscale_n30 | 12 | 0.667 | 0.028 | 0.190 | 0.156 | 0.372 | 0.472 |
| cohortstd | 32 | 0.125 | 0.000 | 0.279 | 0.243 | 0.401 | 0.500 |
| conformal_n20 | 20 | 1.000 | 0.038 | 0.052 | 0.179 | 0.213 | 0.677 |
| conformal_n30 | 12 | 1.000 | 0.025 | 0.034 | 0.076 | 0.104 | 0.780 |
| em | 32 | 0.125 | 0.000 | 1.000 | 0.558 | 0.659 | 0.325 |
| pool_q | 32 | 0.281 | 0.000 | 0.221 | 0.075 | 0.092 | 0.822 |
| site_shift | 32 | 0.344 | 0.000 | 0.222 | 0.205 | 0.269 | 0.578 |
| source | 32 | 0.312 | 0.000 | 0.658 | 0.304 | 0.381 | 0.505 |

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

## Table S6. Status-quo threshold with matched scoring (fold-model ensemble) vs refitted model

Post hoc.
```
                     pairs  share_out_of_band  min_fpr  max_fpr  sd_fpr   sens
alpha scoring                                                                 
0.05  fold-ensemble     32              0.844      0.0    0.575   0.129  0.235
      refit (main)      32              0.656      0.0    0.661   0.153  0.304
0.10  fold-ensemble     32              0.750      0.0    0.678   0.152  0.337
      refit (main)      32              0.688      0.0    0.730   0.177  0.386
heterogeneity a=0.05 fold-ensemble  CRC      lasso: FPR 0.04-0.25, chi2=9.2, df=2, P=0.01
heterogeneity a=0.05 fold-ensemble  CRC      rf: FPR 0.04-0.12, chi2=2.5, df=2, P=0.28
heterogeneity a=0.05 fold-ensemble  IBD      lasso: FPR 0.00-0.08, chi2=3.0, df=3, P=0.39
heterogeneity a=0.05 fold-ensemble  IBD      rf: FPR 0.00-0.15, chi2=10.2, df=3, P=0.017
heterogeneity a=0.05 fold-ensemble  T2D      lasso: FPR 0.00-0.39, chi2=264.8, df=3, P=4.1e-57
heterogeneity a=0.05 fold-ensemble  T2D      rf: FPR 0.00-0.57, chi2=434.5, df=3, P=7.5e-94
heterogeneity a=0.05 fold-ensemble  adenoma  lasso: FPR 0.00-0.13, chi2=20.1, df=4, P=0.00047
heterogeneity a=0.05 fold-ensemble  adenoma  rf: FPR 0.00-0.02, chi2=3.5, df=4, P=0.48
heterogeneity a=0.05 refit (main)   CRC      lasso: FPR 0.04-0.28, chi2=11.1, df=2, P=0.004
heterogeneity a=0.05 refit (main)   CRC      rf: FPR 0.06-0.15, chi2=2.3, df=2, P=0.31
heterogeneity a=0.05 refit (main)   IBD      lasso: FPR 0.03-0.08, chi2=1.2, df=3, P=0.76
heterogeneity a=0.05 refit (main)   IBD      rf: FPR 0.02-0.22, chi2=14.3, df=3, P=0.0025
heterogeneity a=0.05 refit (main)   T2D      lasso: FPR 0.03-0.52, chi2=302.3, df=3, P=3.1e-65
heterogeneity a=0.05 refit (main)   T2D      rf: FPR 0.00-0.66, chi2=489.3, df=3, P=9.9e-106
heterogeneity a=0.05 refit (main)   adenoma  lasso: FPR 0.00-0.20, chi2=17.3, df=4, P=0.0017
heterogeneity a=0.05 refit (main)   adenoma  rf: FPR 0.00-0.04, chi2=7.1, df=4, P=0.13
heterogeneity a=0.1 fold-ensemble  CRC      lasso: FPR 0.11-0.28, chi2=4.4, df=2, P=0.11
heterogeneity a=0.1 fold-ensemble  CRC      rf: FPR 0.15-0.25, chi2=1.5, df=2, P=0.47
heterogeneity a=0.1 fold-ensemble  IBD      lasso: FPR 0.00-0.19, chi2=7.3, df=3, P=0.063
heterogeneity a=0.1 fold-ensemble  IBD      rf: FPR 0.02-0.22, chi2=12.1, df=3, P=0.0071
heterogeneity a=0.1 fold-ensemble  T2D      lasso: FPR 0.00-0.49, chi2=287.0, df=3, P=6.4e-62
heterogeneity a=0.1 fold-ensemble  T2D      rf: FPR 0.00-0.68, chi2=522.1, df=3, P=7.7e-113
heterogeneity a=0.1 fold-ensemble  adenoma  lasso: FPR 0.00-0.15, chi2=9.6, df=4, P=0.049
heterogeneity a=0.1 fold-ensemble  adenoma  rf: FPR 0.00-0.12, chi2=23.2, df=4, P=0.00012
heterogeneity a=0.1 refit (main)   CRC      lasso: FPR 0.11-0.28, chi2=4.3, df=2, P=0.12
heterogeneity a=0.1 refit (main)   CRC      rf: FPR 0.13-0.30, chi2=4.2, df=2, P=0.12
heterogeneity a=0.1 refit (main)   IBD      lasso: FPR 0.05-0.41, chi2=22.3, df=3, P=5.7e-05
heterogeneity a=0.1 refit (main)   IBD      rf: FPR 0.02-0.33, chi2=20.5, df=3, P=0.00013
heterogeneity a=0.1 refit (main)   T2D      lasso: FPR 0.05-0.59, chi2=296.3, df=3, P=6.3e-64
heterogeneity a=0.1 refit (main)   T2D      rf: FPR 0.00-0.73, chi2=510.0, df=3, P=3.3e-110
heterogeneity a=0.1 refit (main)   adenoma  lasso: FPR 0.04-0.26, chi2=14.5, df=4, P=0.0058
heterogeneity a=0.1 refit (main)   adenoma  rf: FPR 0.00-0.14, chi2=26.4, df=4, P=2.6e-05
model                                  lasso                         rf             
scoring                        fold-ensemble refit (main) fold-ensemble refit (main)
task    cohort                                                                      
CRC     ThomasAM_2019_c                0.275        0.275         0.250        0.300
        YachidaS_2019                  0.167        0.175         0.195        0.195
        YuJ_2015                       0.111        0.111         0.148        0.130
IBD     HMP_2019_ibdmdb                0.185        0.407         0.222        0.222
        HallAB_2017                    0.083        0.083         0.167        0.333
        IjazUZ_2017                    0.000        0.053         0.053        0.026
        NielsenHB_2014                 0.085        0.068         0.017        0.017
T2D     KarlssonFH_2013                0.000        0.047         0.000        0.000
        MetaCardis_2020_a              0.025        0.053         0.003        0.020
        QinJ_2012                      0.489        0.592         0.678        0.730
        SankaranarayananK_2015         0.278        0.333         0.222        0.278
adenoma FengQ_2015                     0.148        0.262         0.000        0.000
        HanniganGD_2017                0.000        0.071         0.000        0.000
        ThomasAM_2018a                 0.042        0.042         0.000        0.000
        YachidaS_2019                  0.068        0.124         0.124        0.139
        ZellerG_2014                   0.033        0.066         0.000        0.000
```

## Table S7. Cohort characteristics (controls)

Post hoc. Median read depth in millions; control_disease = most frequent 'disease' labels among controls.

| task | cohort | country | platform | controls | cases | median_reads_M | median_age | median_BMI | control_disease |
|---|---|---|---|---|---|---|---|---|---|
| CRC | FengQ_2015 | AUT | IlluminaHiSeq | 61 | 46 | 50.800 | 68.000 | 29.000 | healthy:16,fatty_liver;hypertension:13,hypertension:11 |
| CRC | GuptaA_2019 | IND | IlluminaNextSeq | 30 | 30 | 9.300 | 40.000 | 22.000 | healthy:30 |
| CRC | HanniganGD_2017 | USA | IlluminaHiSeq | 28 | 27 | 6.700 | 54.000 | 25.200 | healthy:28 |
| CRC | ThomasAM_2018a | ITA | IlluminaHiSeq | 24 | 29 | 98.700 | 67.500 | 25.000 | healthy:14,hypercholesterolemia:5,hypertension:3 |
| CRC | ThomasAM_2018b | ITA | IlluminaHiSeq | 28 | 32 | 38.200 | 58.000 | 24.200 | healthy:28 |
| CRC | ThomasAM_2019_c | JPN | IlluminaHiSeq | 40 | 40 | 43.700 | 66.000 | 22.800 | healthy:40 |
| CRC | VogtmannE_2016 | USA | IlluminaHiSeq | 52 | 52 | 67.600 | 63.000 | 24.000 | healthy:52 |
| CRC | WirbelJ_2018 | DEU | IlluminaHiSeq | 65 | 60 | 35.900 | 58.000 | 24.600 | healthy:65 |
| CRC | YachidaS_2019 | JPN | IlluminaHiSeq | 251 | 258 | 44.200 | 63.000 | 22.400 | healthy:246,few_polyps:5 |
| CRC | YuJ_2015 | CHN | IlluminaHiSeq | 54 | 74 | 59.100 | 63.000 | 22.800 | healthy:38,T2D:16 |
| CRC | ZellerG_2014 | FRA | IlluminaHiSeq | 61 | 53 | 64.900 | 63.000 | 24.000 | healthy:61 |
| IBD | HMP_2019_ibdmdb | USA | IlluminaHiSeq | 27 | 103 | 30.800 | 21.000 | 23.200 | healthy:27 |
| IBD | HallAB_2017 | USA | IlluminaMiSeq | 12 | 20 | 29.500 |  |  | healthy:12 |
| IBD | IjazUZ_2017 | GBR | IlluminaHiSeq | 38 | 12 | 4.400 | 39.000 |  | healthy:38 |
| IBD | NielsenHB_2014 | ESP | IlluminaHiSeq | 59 | 82 | 56.900 | 41.000 | 23.900 | healthy:59 |
| T2D | KarlssonFH_2013 | SWE | IlluminaHiSeq | 43 | 53 | 26.400 | 70.000 | 25.700 | healthy:43 |
| T2D | MetaCardis_2020_a | DEU | IonProton | 642 | 550 | 21.000 | 48.000 | 37.000 | MS:365,healthy:234,IGT:43 |
| T2D | QinJ_2012 | CHN | IlluminaHiSeq | 174 | 170 | 36.300 | 42.000 | 23.700 | healthy:174 |
| T2D | SankaranarayananK_2015 | USA | IlluminaHiSeq | 18 | 19 | 45.700 | 47.000 | 32.500 | healthy:18 |

## Table S8. Read depth, MetaCardis control subgroups, percentile normalisation, adenoma positivity

Post hoc. B: depth vs control-score shift; C: MetaCardis control subgroups; D: percentile normalisation against 20 local controls (external CRC, R=50); E: positivity of Yachida adenoma carriers.

```
B. log10 depth ratio (target/training controls) vs shift: rho=-0.02 P=0.9 (n=32)
B. log10 depth ratio (target/training controls) vs fpr: rho=0.06 P=0.73 (n=32)
B. log10 depth ratio vs |FPR-0.10|: rho=0.20 P=0.27
C. MetaCardis lasso controls=healthy (n=234): status-quo FPR=0.021
C. MetaCardis lasso controls=MS (n=365): status-quo FPR=0.074
C. MetaCardis lasso controls=IGT (n=43): status-quo FPR=0.047
C. MetaCardis lasso healthy-only conformal n=20: mean FPR=0.092, P(FPR>0.15)=0.195
C. MetaCardis rf controls=healthy (n=234): status-quo FPR=0.004
C. MetaCardis rf controls=MS (n=365): status-quo FPR=0.025
C. MetaCardis rf controls=IGT (n=43): status-quo FPR=0.070
C. MetaCardis rf healthy-only conformal n=20: mean FPR=0.102, P(FPR>0.15)=0.235
E. Yachida adenoma carriers (n=67) lasso: positivity status-quo=0.284, conformal n=20 mean=0.131
D. percentile-norm (20 local controls) + training threshold lasso YachidaS_2019: mean FPR=0.102 P(FPR>0.15)=0.160 sens=0.119
D. percentile-norm (20 local controls) + training threshold lasso YuJ_2015: mean FPR=0.093 P(FPR>0.15)=0.160 sens=0.244
D. percentile-norm (20 local controls) + training threshold lasso ThomasAM_2019_c: mean FPR=0.123 P(FPR>0.15)=0.220 sens=0.187
E. Yachida adenoma carriers (n=67) rf: positivity status-quo=0.239, conformal n=20 mean=0.114
D. percentile-norm (20 local controls) + training threshold rf YachidaS_2019: mean FPR=0.028 P(FPR>0.15)=0.000 sens=0.070
D. percentile-norm (20 local controls) + training threshold rf YuJ_2015: mean FPR=0.036 P(FPR>0.15)=0.020 sens=0.228
D. percentile-norm (20 local controls) + training threshold rf ThomasAM_2019_c: mean FPR=0.002 P(FPR>0.15)=0.000 sens=0.137
```

## Table S9. Twenty labelled controls from another centre or cohort

Post hoc. Conformal rule, n=20, alpha=0.10, R=200. same_site=True rows use the half-split design of the main analysis.
```
             setting model             cal          deploy  mean_fpr  p_gt_015  same_site
External CRC cohorts lasso ThomasAM_2019_c ThomasAM_2019_c     0.095     0.180       True
External CRC cohorts lasso ThomasAM_2019_c   YachidaS_2019     0.061     0.000      False
External CRC cohorts lasso ThomasAM_2019_c        YuJ_2015     0.019     0.000      False
External CRC cohorts lasso   YachidaS_2019 ThomasAM_2019_c     0.164     0.545      False
External CRC cohorts lasso   YachidaS_2019   YachidaS_2019     0.098     0.210       True
External CRC cohorts lasso   YachidaS_2019        YuJ_2015     0.041     0.090      False
External CRC cohorts lasso        YuJ_2015 ThomasAM_2019_c     0.279     1.000      False
External CRC cohorts lasso        YuJ_2015   YachidaS_2019     0.168     0.865      False
External CRC cohorts lasso        YuJ_2015        YuJ_2015     0.090     0.155       True
External CRC cohorts    rf ThomasAM_2019_c ThomasAM_2019_c     0.095     0.175       True
External CRC cohorts    rf ThomasAM_2019_c   YachidaS_2019     0.081     0.030      False
External CRC cohorts    rf ThomasAM_2019_c        YuJ_2015     0.041     0.000      False
External CRC cohorts    rf   YachidaS_2019 ThomasAM_2019_c     0.110     0.275      False
External CRC cohorts    rf   YachidaS_2019   YachidaS_2019     0.095     0.180       True
External CRC cohorts    rf   YachidaS_2019        YuJ_2015     0.059     0.025      False
External CRC cohorts    rf        YuJ_2015 ThomasAM_2019_c     0.175     0.515      False
External CRC cohorts    rf        YuJ_2015   YachidaS_2019     0.134     0.270      False
External CRC cohorts    rf        YuJ_2015        YuJ_2015     0.093     0.170       True
  MetaCardis centres lasso      Copenhagen      Copenhagen     0.088     0.140       True
  MetaCardis centres lasso      Copenhagen         Leipzig     0.233     0.735      False
  MetaCardis centres lasso      Copenhagen           Paris     0.180     0.565      False
  MetaCardis centres lasso         Leipzig      Copenhagen     0.024     0.000      False
  MetaCardis centres lasso         Leipzig         Leipzig     0.097     0.180       True
  MetaCardis centres lasso         Leipzig           Paris     0.060     0.045      False
  MetaCardis centres lasso           Paris      Copenhagen     0.044     0.005      False
  MetaCardis centres lasso           Paris         Leipzig     0.138     0.490      False
  MetaCardis centres lasso           Paris           Paris     0.087     0.150       True
  MetaCardis centres    rf      Copenhagen      Copenhagen     0.091     0.185       True
  MetaCardis centres    rf      Copenhagen         Leipzig     0.151     0.480      False
  MetaCardis centres    rf      Copenhagen           Paris     0.154     0.580      False
  MetaCardis centres    rf         Leipzig      Copenhagen     0.052     0.035      False
  MetaCardis centres    rf         Leipzig         Leipzig     0.101     0.190       True
  MetaCardis centres    rf         Leipzig           Paris     0.089     0.115      False
  MetaCardis centres    rf           Paris      Copenhagen     0.047     0.030      False
  MetaCardis centres    rf           Paris         Leipzig     0.088     0.205      False
  MetaCardis centres    rf           Paris           Paris     0.096     0.185       True

Summary (mean over pairs):
                               mean_fpr               p_gt_015              
                                   mean    min    max     mean    min    max
setting              same_site                                              
External CRC cohorts False        0.111  0.019  0.279    0.301  0.000  1.000
                     True         0.094  0.090  0.098    0.178  0.155  0.210
MetaCardis centres   False        0.105  0.024  0.233    0.274  0.000  0.735
                     True         0.093  0.087  0.101    0.172  0.140  0.190
```

## Table S10. Single-site FPR of the conformal rule by number of local controls

Post hoc. Theory: FPR ~ Beta(n+1-k, k).
```
Theory (alpha=0.10, exchangeable local controls):
  n  mean_FPR  q025  q975  P_gt_015  P_in_005_015
  9       0.1 0.003 0.336     0.232         0.399
 19       0.1 0.013 0.260     0.198         0.556
 29       0.1 0.022 0.228     0.168         0.656
 49       0.1 0.034 0.196     0.123         0.780
 99       0.1 0.050 0.166     0.060         0.914
199       0.1 0.062 0.145     0.016         0.982
299       0.1 0.069 0.136     0.005         0.995

Empirical (large cohorts; includes evaluation-half sampling noise):
                       file  n  mean_FPR  q025  q975  P_gt_015
   T2D_MetaCardis_2020_a_rf 19     0.100 0.009 0.283     0.214
   T2D_MetaCardis_2020_a_rf 49     0.098 0.028 0.198     0.130
   T2D_MetaCardis_2020_a_rf 79     0.101 0.039 0.181     0.096
T2D_MetaCardis_2020_a_lasso 19     0.102 0.009 0.251     0.200
T2D_MetaCardis_2020_a_lasso 49     0.101 0.028 0.217     0.140
T2D_MetaCardis_2020_a_lasso 79     0.099 0.040 0.181     0.098
    CRC_YachidaS_2019_lasso 19     0.094 0.008 0.266     0.188
    CRC_YachidaS_2019_lasso 49     0.095 0.020 0.211     0.140
    CRC_YachidaS_2019_lasso 79     0.098 0.032 0.190     0.118
       CRC_YachidaS_2019_rf 19     0.099 0.008 0.290     0.208
       CRC_YachidaS_2019_rf 49     0.101 0.032 0.206     0.168
       CRC_YachidaS_2019_rf 79     0.100 0.032 0.190     0.158
        T2D_QinJ_2012_lasso 19     0.096 0.005 0.259     0.200
        T2D_QinJ_2012_lasso 49     0.101 0.023 0.218     0.142
        T2D_QinJ_2012_lasso 79     0.101 0.023 0.195     0.124
           T2D_QinJ_2012_rf 19     0.096 0.000 0.253     0.182
           T2D_QinJ_2012_rf 49     0.101 0.023 0.224     0.140
           T2D_QinJ_2012_rf 79     0.099 0.023 0.195     0.108
```

## Table S11. Label-free threshold from simulated screening pools

Post hoc. Pools resampled from each cohort's calibration-half controls (with replacement) plus cases at prevalence pi; effective number of distinct controls is therefore limited by cohort size.
```
Cohort-mean FPR across 32 cohort x model pairs, and per-draw P(FPR>0.15):
             mean    min    max    std  p_gt_015   sens
pi    N                                                
0.005 100   0.125  0.107  0.175  0.016     0.316  0.321
      300   0.120  0.101  0.170  0.017     0.282  0.316
      1000  0.117  0.097  0.169  0.019     0.268  0.315
0.010 100   0.123  0.104  0.173  0.016     0.307  0.319
      300   0.118  0.099  0.169  0.017     0.278  0.315
      1000  0.116  0.098  0.169  0.020     0.265  0.314
0.050 100   0.114  0.082  0.169  0.019     0.270  0.308
      300   0.110  0.084  0.169  0.020     0.245  0.304
      1000  0.109  0.080  0.169  0.022     0.236  0.303
```