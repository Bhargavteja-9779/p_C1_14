# Locked run v3b (protocol_deploy.md), run once 2026-11-24. No deviations. Full table: results/deploy_locked_summary.csv

Pre-stated success criterion (healthy LOCKED atlas populations, alpha = 0.10):
| criterion | needed | observed | met |
|---|---|---|---|
| BURN(N=100) mean P(FPR>0.15) | <= 0.10 | 0.085 (38 population x test x model units) | YES |
| BURN(N=100) mean abs(FPR-0.10) vs SRC | >= 50% lower | 0.029 vs 0.063 (-54%) | YES |
| BURN-PAC(N=100) mean P(FPR>0.10) | <= 0.07 | 0.045 | YES |

Exact beta-binomial law vs observed P(evaluated FPR > 0.15) for BURN: N=25 0.119/0.120; N=50 0.135/0.127; N=100 0.088/0.085; N=200 0.050/0.049.
Mean realised FPR of BURN: 0.077 (N=25, k-th order statistic discreteness), 0.097-0.100 (N>=50).
Large pooled healthy reference (ATLAS) is not better than SRC (mean abs error 0.068-0.102; P(FPR>0.15) 0.14-0.37).

Contaminated burn-in (locked case-control cohorts; CRC external YachidaS_2019, YuJ_2015 with dev-trained model; IBD, T2D LOSO):
- Status quo SRC over-calls: mean FPR 0.29 (N>=50 subset), P(FPR>0.15) 0.64-0.67.
- BURN with correct pi_max: mean FPR 0.066-0.087 (conservative as the bound predicts), P(FPR>0.15) 0.004-0.05.
- BURN with pi_max = 0.01 when true pi = 0.05 (mis-specified): mean FPR 0.082-0.093, P(FPR>0.15) 0.03-0.11.
- Sensitivity: BURN 0.18-0.28 vs SRC 0.31-0.46 - the status quo "sensitivity" is bought with 2.9x the promised FPR.
