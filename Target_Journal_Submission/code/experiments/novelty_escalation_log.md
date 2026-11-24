# Novelty escalation log (D6) - development cohorts only (8 CRC dev cohorts, nested LOCO)

Target: alpha = 0.10 (90% specificity). Per replicate, each held-out cohort is split in half: calibration half
(unlabelled pool with case share pi, and up to 20 labelled local controls) and evaluation half (realised FPR, sensitivity).
"cohort-RMSE" = RMSE over cohorts of the per-cohort mean realised FPR minus 0.10 (systematic miscalibration);
"abs_err" = mean |FPR - 0.10| per replicate (includes evaluation-half sampling noise, floor ~0.04).

## Round 1 (explore_v1.py; source, local quantile, Saerens EM, site-shift v1, 10 local controls conformal)
Run 2026-11-24; LASSO finished (AUCs 0.65-0.84) but the RF half was stopped after >1.5 h without finishing a cohort
(exact-KDE site-shift v1 too slow; overflow in exp(log b)). No CSV written. All round-1 methods except v1 are re-tested
in rounds 2-3 (v1 replaced by bounded v2). Not re-run.

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

## Round 3 (explore_v3.py, LASSO R=50; RF R=30 running) - 2026-11-24
Synthetic pre-check of location-scale anchoring with 10 controls: mean FPR 0.145 vs 0.094 for conformal - scale is too
noisy from 10 points; location-only variant added.

| method | cohort-RMSE pi=0 | 0.01 | 0.05 | 0.2 | nat | mean FPR pi=0.01 | P(FPR>0.15) | sens pi=0.01 |
|---|---|---|---|---|---|---|---|---|
| source threshold | 0.141 | 0.141 | 0.141 | 0.141 | 0.141 | 0.156 | 0.485 | 0.511 |
| local quantile of pool | 0.043 | 0.043 | 0.024 | 0.044 | 0.089 | 0.137 | 0.365 | 0.512 |
| feature standardisation (pool stats, fair) | 0.368 | 0.368 | 0.325 | 0.237 | 0.092 | 0.462 | 0.978 | 0.794 |
| site-shift v2 | 0.159 | 0.159 | 0.124 | 0.084 | 0.041 | 0.252 | 0.585 | 0.602 |
| hybrid v2 + 10 controls | 0.057 | 0.057 | 0.051 | 0.045 | 0.039 | 0.154 | 0.438 | 0.527 |
| conformal, 10 controls | 0.025 | 0.025 | 0.025 | 0.025 | 0.025 | 0.086 | 0.198 | 0.420 |
| anchor loc+scale, 10 controls | 0.059 | - | - | - | - | 0.152 | 0.400 | 0.517 |
| anchor location-only, 10 controls | 0.047 | - | - | - | - | 0.108 | 0.292 | 0.458 |

Findings: (1) Per-site feature standardisation (a published label-free fix) is prevalence-dependent: case-free target
pools are standardised against ~50%-case training cohorts, so FPR explodes to 0.46 at screening prevalence. This is a
new, practically important negative result. (2) Anchoring with 10 controls gains sensitivity (+0.04) over conformal but
loses reliability (P(FPR>0.15) 0.29 vs 0.20); no method dominates. (3) At screening prevalence the unlabelled pool is
~all controls, so its quantile is close to correct - the remaining error is small-sample + ties (LASSO gives tied scores
for samples with none of the selected taxa).
Decision for round 4: build the paper around a guarantee rather than a point estimator: an order-statistic threshold on
the unlabelled screening pool that keeps P(FPR > alpha) <= delta for any case share up to a stated bound pi_max
(contamination-robust tolerance bound, Wilks-type), with a sample-size rule (how many screened samples / local controls
a lab needs), and compare its sensitivity cost to conformal with labelled controls.
