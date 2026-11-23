# Locked-run results (protocol.md, run once 2026-11-23; full numbers in endpoints.txt / endpoints_by_task.csv)

Run: 16 held-out cohorts (3 external CRC, 4 IBD, 4 T2D, 5 adenoma) x 2 models x alpha in {0.10, 0.05}, R=200 splits
(R=20 for em/site_shift). No deviations from protocol.

## Pre-stated success criterion (alpha = 0.10)
- Drift claim: status-quo threshold has cohort-mean FPR outside [0.05, 0.15] in **68.8%** of 32 cohort x model pairs
  (needed >= 30%) -> **MET**. Overdispersion vs binomial significant in all 8 task x model cells (p from 1e-3 to 1e-177).
- Recommended protocol (conformal, n=20 local controls): **100%** of 20 feasible pairs within band (needed >= 90%);
  SD of cohort-mean FPR smaller than status quo in every task with >= 2 feasible cohorts (CRC 0.007 vs 0.089,
  T2D 0.005 vs 0.298, adenoma 0.008 vs 0.075; IBD only one feasible cohort) -> **MET**.
- Cohort-bootstrap SD difference (conformal_n20 - source): LASSO -0.161 [95% CI -0.232, -0.048], RF -0.218 [-0.323, -0.061].

## Key numbers (alpha = 0.10, pooled)
| method | pairs | cohort-mean FPR in band | max |FPR - alpha| | P(split FPR > 0.15) | mean sens |
|---|---|---|---|---|---|
| source (status quo) | 32 | 0.31 | 0.63 | 0.38 | 0.39 |
| cohort-wise standardisation (batch correction) | 32 | 0.28 | 0.22 | 0.32 | 0.31 |
| EM prevalence correction | 32 | 0.16 | 0.90 | 0.68 | 0.59 |
| unlabeled pool quantile | 32 | 0.28 | 0.14 | 0.08 | 0.14 |
| site-shift mixture (our v1) | 32 | 0.66 | 0.16 | 0.23 | 0.29 |
| anchor (median/IQR of 20 controls) | 20 | 0.40-0.50 | 0.19-0.23 | 0.43-0.45 | 0.36-0.37 |
| **conformal, 20 local controls** | 20 | **1.00** | **0.02** | 0.19 | 0.28 |
| Tong 95%-confidence, 30 controls | 12 | 0.00 (conservative) | 0.07 | 0.02 | 0.08 |

## Honest caveats for the manuscript
1. Conformal controls the *expected* FPR by construction; the band criterion is close to guaranteed. Per-split FPR still
   exceeds 0.15 in ~19% of splits with n=20 — single-site variability from a small calibration set. High-confidence
   (Tong) control removes this (P(FPR > 0.15) ~ 1-2%) but costs sensitivity (0.08-0.11 at alpha=0.10).
2. At alpha=0.05, conformal needs n >= 19; with n=10 the rule is infeasible (threshold = inf, sens = 0). Tong at
   alpha=0.05 needs n >= 59; with n<=50 it is infeasible.
3. Sensitivity cost is real: at alpha=0.10 the status quo looks more sensitive because it is usually over-calling.
   For external CRC at prevalence 0.5%: per 1,000 screened, status quo gives 112-308 false positives and 1.3-2.5 missed
   cancers; conformal_n20 gives 86-112 false positives and 1.5-3.4 missed (about 100-200 fewer colonoscopies for
   ~1 more miss per 1,000 in two of three cohorts; YuJ_2015 trade is smaller).
4. All three external CRC cohorts had FPR ABOVE target under the status quo (0.11-0.31).
5. T2D and adenoma classifiers are weak (AUC 0.54-0.69), so absolute sensitivities are low for every method.
6. IBD: only NielsenHB_2014 has enough controls for n=20; HallAB_2017 and SankaranarayananK_2015 only inform drift.
7. EM prevalence correction is harmful (max deviation 0.90): it confounds class-conditional shift with prevalence.
