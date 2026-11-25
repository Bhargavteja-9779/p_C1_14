# Post-hoc analyses after review round 2 (EXPLORATORY, not pre-registered)

## T1. Locked run: rank-rule FPR predicted by order-statistic theory (alpha 0.10, no cases)

cohort-RMSE observed 0.031; predicted from r/(n0+1) alone 0.030; without the abstaining cohort (HallAB_2017): observed 0.018, predicted 0.017.

|    | disease   | cohort                 | model   |   fpr |   ab |   theory |   pool_n |
|---:|:----------|:-----------------------|:--------|------:|-----:|---------:|---------:|
|  9 | IBD       | HallAB_2017            | rf      | 0     |    1 |    0     |        6 |
|  8 | IBD       | HallAB_2017            | lasso   | 0     |    1 |    0     |        6 |
| 20 | T2D       | SankaranarayananK_2015 | lasso   | 0.099 |    0 |    0.1   |        9 |
| 21 | T2D       | SankaranarayananK_2015 | rf      | 0.095 |    0 |    0.1   |        9 |
| 27 | adenoma   | ThomasAM_2018a         | rf      | 0.084 |    0 |    0.077 |       12 |
| 26 | adenoma   | ThomasAM_2018a         | lasso   | 0.077 |    0 |    0.077 |       12 |
|  6 | IBD       | HMP_2019_ibdmdb        | lasso   | 0.062 |    0 |    0.071 |       13 |
|  7 | IBD       | HMP_2019_ibdmdb        | rf      | 0.067 |    0 |    0.071 |       13 |
| 25 | adenoma   | HanniganGD_2017        | rf      | 0.059 |    0 |    0.067 |       14 |
| 24 | adenoma   | HanniganGD_2017        | lasso   | 0.069 |    0 |    0.067 |       14 |
| 11 | IBD       | IjazUZ_2017            | rf      | 0.104 |    0 |    0.1   |       19 |
| 10 | IBD       | IjazUZ_2017            | lasso   | 0.101 |    0 |    0.1   |       19 |
|  0 | CRC       | ThomasAM_2019_c        | lasso   | 0.094 |    0 |    0.1   |       20 |
|  1 | CRC       | ThomasAM_2019_c        | rf      | 0.098 |    0 |    0.1   |       20 |
| 15 | T2D       | KarlssonFH_2013        | rf      | 0.097 |    0 |    0.095 |       21 |
| 14 | T2D       | KarlssonFH_2013        | lasso   | 0.083 |    0 |    0.095 |       21 |
|  5 | CRC       | YuJ_2015               | rf      | 0.074 |    0 |    0.074 |       27 |
|  4 | CRC       | YuJ_2015               | lasso   | 0.074 |    0 |    0.074 |       27 |
| 12 | IBD       | NielsenHB_2014         | lasso   | 0.068 |    0 |    0.069 |       29 |
| 13 | IBD       | NielsenHB_2014         | rf      | 0.07  |    0 |    0.069 |       29 |
| 31 | adenoma   | ZellerG_2014           | rf      | 0.112 |    0 |    0.1   |       30 |
| 30 | adenoma   | ZellerG_2014           | lasso   | 0.098 |    0 |    0.1   |       30 |
| 23 | adenoma   | FengQ_2015             | rf      | 0.093 |    0 |    0.1   |       30 |
| 22 | adenoma   | FengQ_2015             | lasso   | 0.101 |    0 |    0.1   |       30 |
| 19 | T2D       | QinJ_2012              | rf      | 0.093 |    0 |    0.095 |       87 |
| 18 | T2D       | QinJ_2012              | lasso   | 0.093 |    0 |    0.095 |       87 |
|  3 | CRC       | YachidaS_2019          | rf      | 0.097 |    0 |    0.1   |      125 |
|  2 | CRC       | YachidaS_2019          | lasso   | 0.094 |    0 |    0.1   |      125 |
| 29 | adenoma   | YachidaS_2019          | rf      | 0.096 |    0 |    0.1   |      125 |
| 28 | adenoma   | YachidaS_2019          | lasso   | 0.095 |    0 |    0.1   |      125 |
| 17 | T2D       | MetaCardis_2020_a      | rf      | 0.092 |    0 |    0.098 |      321 |
| 16 | T2D       | MetaCardis_2020_a      | lasso   | 0.091 |    0 |    0.098 |      321 |

## T2. Locked run: cohort-RMSE per classifier (alpha 0.10)

|                |   ctrl10 |    em |   featstd |   gauss2 |   local_q |   mlls |   rpool |   rpoolmean |   shift2 |   source |
|:---------------|---------:|------:|----------:|---------:|----------:|-------:|--------:|------------:|---------:|---------:|
| ('lasso', 0.0) |    0.027 | 0.375 |     0.258 |    0.305 |     0.043 |  0.338 |   0.08  |       0.031 |    0.161 |    0.17  |
| ('lasso', 0.2) |    0.027 | 0.396 |     0.197 |    0.232 |     0.042 |  0.366 |   0.084 |       0.062 |    0.112 |    0.17  |
| ('rf', 0.0)    |    0.027 | 0.443 |     0.126 |    0.34  |     0.049 |  0.34  |   0.08  |       0.031 |    0.144 |    0.199 |
| ('rf', 0.2)    |    0.027 | 0.456 |     0.094 |    0.285 |     0.044 |  0.349 |   0.084 |       0.055 |    0.086 |    0.199 |

## F. Feature standardisation, training cohorts standardised on all samples vs on controls only (alpha 0.10)

|                 |   featstd_all |   featstd_controls |
|:----------------|--------------:|-------------------:|
| ('lasso', 0.0)  |         0.259 |              0.319 |
| ('lasso', 0.05) |         0.246 |              0.312 |

## E2b. Pool size with fixed evaluation sets (5% binomial cases in the pool, alpha 0.10)

Share of deployments with FPR > 0.15. 'oracle' = cut-off at the true (1 - alpha) quantile of all the cohort's controls: its exceedance is the evaluation-noise floor.

|                                |   ctrl10 |   local_q |   oracle |   rpool |   rpoolmean |   source |
|:-------------------------------|---------:|----------:|---------:|--------:|------------:|---------:|
| ('CRC:YachidaS_2019', 25)      |    0.19  |     0.24  |     0    |   0.005 |       0.065 |    0.875 |
| ('CRC:YachidaS_2019', 50)      |    0.17  |     0.175 |     0    |   0     |       0.04  |    0.875 |
| ('CRC:YachidaS_2019', 75)      |    0.21  |     0.125 |     0    |   0.005 |       0.025 |    0.875 |
| ('CRC:YachidaS_2019', 100)     |    0.195 |     0.085 |     0    |   0     |       0.025 |    0.875 |
| ('T2D:MetaCardis_2020_a', 25)  |    0.22  |     0.29  |     0    |   0.02  |       0.1   |    0     |
| ('T2D:MetaCardis_2020_a', 50)  |    0.26  |     0.225 |     0    |   0     |       0.055 |    0     |
| ('T2D:MetaCardis_2020_a', 75)  |    0.195 |     0.095 |     0    |   0     |       0.04  |    0     |
| ('T2D:MetaCardis_2020_a', 100) |    0.17  |     0.055 |     0    |   0     |       0.015 |    0     |
| ('T2D:MetaCardis_2020_a', 150) |    0.165 |     0.04  |     0    |   0     |       0.025 |    0     |
| ('T2D:MetaCardis_2020_a', 200) |    0.18  |     0.035 |     0    |   0     |       0.015 |    0     |
| ('T2D:MetaCardis_2020_a', 300) |    0.185 |     0.02  |     0    |   0     |       0     |    0     |
| ('T2D:QinJ_2012', 25)          |    0.23  |     0.255 |     0.01 |   0.015 |       0.055 |    1     |
| ('T2D:QinJ_2012', 50)          |    0.19  |     0.175 |     0.01 |   0     |       0.04  |    1     |
| ('T2D:QinJ_2012', 75)          |    0.175 |     0.145 |     0.01 |   0.005 |       0.08  |    1     |
| ('adenoma:YachidaS_2019', 25)  |    0.23  |     0.255 |     0    |   0.01  |       0.09  |    0.11  |
| ('adenoma:YachidaS_2019', 50)  |    0.2   |     0.175 |     0    |   0.005 |       0.005 |    0.11  |
| ('adenoma:YachidaS_2019', 75)  |    0.18  |     0.18  |     0    |   0     |       0.07  |    0.11  |
| ('adenoma:YachidaS_2019', 100) |    0.195 |     0.13  |     0    |   0.005 |       0.025 |    0.11  |

Mean over the four tasks and both models, at pool sizes available in all tasks:

|   n_pool |   ctrl10 |   local_q |   oracle |   rpool |   rpoolmean |   source |
|---------:|---------:|----------:|---------:|--------:|------------:|---------:|
|       25 |    0.218 |     0.26  |    0.002 |   0.012 |       0.078 |    0.496 |
|       50 |    0.205 |     0.188 |    0.002 |   0.001 |       0.035 |    0.496 |
|       75 |    0.19  |     0.136 |    0.002 |   0.002 |       0.054 |    0.496 |

Mean FPR:

|   n_pool |   ctrl10 |   local_q |   oracle |   rpool |   rpoolmean |   source |
|---------:|---------:|----------:|---------:|--------:|------------:|---------:|
|       25 |    0.094 |     0.119 |    0.103 |   0.033 |       0.07  |    0.236 |
|       50 |    0.095 |     0.106 |    0.103 |   0.034 |       0.071 |    0.236 |
|       75 |    0.09  |     0.102 |    0.103 |   0.048 |       0.083 |    0.236 |

## E3b. Pool from another cohort vs from the target cohort itself (same model, same pool size; alpha 0.10)

|                               |   rmse |   share_gt_15 |
|:------------------------------|-------:|--------------:|
| ('other cohort', 'local_q')   |  0.189 |          0.48 |
| ('other cohort', 'rpool')     |  0.115 |          0.1  |
| ('other cohort', 'rpoolmean') |  0.133 |          0.3  |
| ('other cohort', 'source')    |  0.175 |          0.54 |
| ('same cohort', 'local_q')    |  0.051 |          0.32 |
| ('same cohort', 'rpool')      |  0.085 |          0    |
| ('same cohort', 'rpoolmean')  |  0.035 |          0    |
| ('same cohort', 'source')     |  0.175 |          0.54 |

Rank rule, |FPR - 0.10| other cohort minus same cohort: mean 0.073, 95% CI clustered by target cohort 0.046 to 0.106 (50 pair-model units, 16 target cohorts).

## E6. Time drift, HMP_2019_ibdmdb (pool: controls days 0-120 of half the subjects; evaluation: the other subjects)

|                                                     |   mean_fpr |   p90_fpr |   share_gt_15 |   sens |   n_pool |   n_eval |
|:----------------------------------------------------|-----------:|----------:|--------------:|-------:|---------:|---------:|
| ('lasso', 'later period (days > 180)', 'local_q')   |      0.14  |     0.286 |         0.505 |  0.349 |    95.02 |    84.47 |
| ('lasso', 'later period (days > 180)', 'rpool')     |      0.102 |     0.203 |         0.37  |  0.24  |    95.02 |    84.47 |
| ('lasso', 'later period (days > 180)', 'rpoolmean') |      0.123 |     0.269 |         0.455 |  0.304 |    95.02 |    84.47 |
| ('lasso', 'later period (days > 180)', 'source')    |      0.206 |     0.29  |         0.725 |  0.477 |    95.02 |    84.47 |
| ('lasso', 'same period (days 0-120)', 'local_q')    |      0.142 |     0.271 |         0.465 |  0.329 |    95.02 |   100.98 |
| ('lasso', 'same period (days 0-120)', 'rpool')      |      0.094 |     0.211 |         0.32  |  0.223 |    95.02 |   100.98 |
| ('lasso', 'same period (days 0-120)', 'rpoolmean')  |      0.121 |     0.25  |         0.4   |  0.285 |    95.02 |   100.98 |
| ('lasso', 'same period (days 0-120)', 'source')     |      0.2   |     0.269 |         0.775 |  0.469 |    95.02 |   100.98 |
| ('rf', 'later period (days > 180)', 'local_q')      |      0.161 |     0.342 |         0.51  |  0.374 |    95.02 |    84.47 |
| ('rf', 'later period (days > 180)', 'rpool')        |      0.118 |     0.277 |         0.385 |  0.211 |    95.02 |    84.47 |
| ('rf', 'later period (days > 180)', 'rpoolmean')    |      0.14  |     0.319 |         0.46  |  0.3   |    95.02 |    84.47 |
| ('rf', 'later period (days > 180)', 'source')       |      0.131 |     0.226 |         0.485 |  0.269 |    95.02 |    84.47 |
| ('rf', 'same period (days 0-120)', 'local_q')       |      0.143 |     0.289 |         0.415 |  0.351 |    95.02 |   100.98 |
| ('rf', 'same period (days 0-120)', 'rpool')         |      0.098 |     0.255 |         0.29  |  0.186 |    95.02 |   100.98 |
| ('rf', 'same period (days 0-120)', 'rpoolmean')     |      0.118 |     0.275 |         0.38  |  0.275 |    95.02 |   100.98 |
| ('rf', 'same period (days 0-120)', 'source')        |      0.115 |     0.192 |         0.285 |  0.26  |    95.02 |   100.98 |
