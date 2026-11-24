# Novelty escalation log (D6) - development cohorts only (8 CRC dev cohorts, nested LOCO)

Target: alpha = 0.10 (90% specificity). Per replicate, each held-out cohort is split in half: calibration half
(unlabelled pool with case share pi, and up to 20 labelled local controls) and evaluation half (realised FPR, sensitivity).
"cohort-RMSE" = RMSE over cohorts of the per-cohort mean realised FPR minus 0.10 (systematic miscalibration);
"abs_err" = mean |FPR - 0.10| per replicate (includes evaluation-half sampling noise, floor ~0.04).

## Round 1 (explore_v1.py; source, local quantile, Saerens EM, site-shift v1, 10 local controls conformal)
Run 2026-11-24; LASSO + RF, R=100. Results: see Round 1 summary below (pending at time of writing).

## Round 2 (explore_v2.py, LASSO, R=50) - 2026-11-24
| method | cohort-RMSE pi=0 | 0.05 | 0.2 | nat(~50%) | mean FPR pi=0 | sens pi=0 |
|---|---|---|---|---|---|---|
| source threshold | 0.144 | 0.144 | 0.144 | 0.144 | 0.160 | 0.506 |
| local quantile (pool = controls assumed) | 0.043 | 0.021 | 0.043 | 0.087 | 0.140 | 0.510 |
| Saerens EM | 0.130 | 0.140 | 0.162 | 0.325 | 0.182 | 0.551 |
| MLLS-BCTS | 0.204 | 0.195 | 0.213 | 0.361 | 0.225 | 0.581 |
| DyS | 0.183 | 0.180 | 0.212 | 0.331 | 0.207 | 0.567 |
| 2-Gaussian unsupervised calibration | 0.339 | 0.271 | 0.154 | 0.044 | 0.419 | 0.725 |
| site-shift v2 (ours, unlabelled only) | 0.181 | 0.157 | 0.117 | 0.034 | 0.272 | 0.616 |
| hybrid v2 + 10 local controls | 0.060 | 0.061 | 0.053 | 0.030 | 0.155 | 0.522 |
| conformal, 10 local controls | 0.018 | 0.018 | 0.018 | 0.018 | 0.085 | 0.419 |
| conformal, 20 local controls | 0.023 | 0.023 | 0.023 | 0.023 | 0.080 | 0.415 |
| feature standardisation | INVALID (used full target cohort, not the pool) | | | | | |

Findings: (1) the problem is confirmed: source thresholds give mean FPR 0.16 (target 0.10), cohort-RMSE 0.144.
(2) All prior/label-shift methods (EM, MLLS, DyS) make it WORSE: they assume the score distributions per class do not
move, which is false across sites. (3) Unlabelled mixture methods (2-Gaussian, our site-shift) work only near 50%
prevalence and fail badly at screening prevalence (pi<=5%): they "invent" a case component inside the controls
(identifiability failure; also seen in synthetic tests). (4) Labelled local controls are what fixes the bias;
order-statistic conformal is unbiased but conservative (sensitivity 0.42 vs 0.51) and noisy per replicate.
Decision: unlabelled-only site-shift is DROPPED as the headline method. Next: (a) fair feature standardisation,
(b) use source shape + few local controls (anchoring) to cut the variance of conformal, (c) screening prevalence 1%.

## Round 3 (explore_v3.py) - running
Synthetic pre-check of location-scale anchoring with 10 controls: mean FPR 0.145 vs 0.094 for conformal - scale is too
noisy from 10 points; location-only variant added.
