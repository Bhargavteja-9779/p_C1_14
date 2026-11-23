# Novelty escalation log (D6) — development cohorts only (8 CRC, LOSO)

## Round 1 (2026-11-23) — explore_v1.py, R=30 random half-splits of each held-out cohort, target FPR alpha=0.10
Half of the target controls (+ cases at contamination pi) form the unlabeled pool / local-control pool; the other half
of controls and cases are used for evaluation. Full table: dev/explore_v1.log; raw rows: dev/explore_v1.csv.

Mean realised FPR (|FPR-0.10|, share of splits with FPR>0.15):

| method | LASSO pi=0 | LASSO pi=nat(~0.5) | RF pi=0 | RF pi=nat |
|---|---|---|---|---|
| source threshold (status quo) | 0.160 (0.127, 48%) | same | 0.091 (0.106, 27%) | same |
| local quantile of unlabeled pool | 0.137 (0.085, 39%) | 0.008 (0.092, 0%) | 0.134 (0.076, 35%) | 0.016 (0.090, 2%) |
| EM label-shift re-threshold | 0.170 (0.109, 49%) | 0.275 (0.243, 41%) | 0.142 (0.088, 40%) | 0.183 (0.144, 37%) |
| site-shift mixture (ours v1) | 0.279 (0.212, 65%) | 0.109 (0.080, 30%) | 0.375 (0.294, 77%) | 0.109 (0.121, 25%) |
| conformal, 10 local controls | 0.088 (0.078, 20%) | same | 0.088 (0.078, 22%) | same |

Findings
- Status quo: per-cohort mean FPR ranges 0.00–0.32 (LASSO) at a 0.10 target; drift confirmed on dev cohorts.
- Site-shift mixture v1 FAILS: unidentifiable when the pool is nearly all one class (fits b/a to absorb the shift;
  overflow warnings in exp). DROPPED as the headline method; kept as a negative benchmark result.
- EM label-shift does not fix FPR (as expected: prevalence change alone cannot change FPR at fixed threshold).
- Local quantile behaves as the prevalence bound predicts: ~alpha at pi=0 (slightly above due to small pools,
  n~12–33), far too conservative at pi~0.5 (sensitivity collapses to 0.23).
- Conformal with only 10 local controls has the best FPR control (mean 0.088) but sensitivity cost (0.42 vs 0.50).

Decision -> Round 2: frame as evidence + deployment protocol. Test (a) conformal / Tong-type high-confidence rule
across n local controls in {10, 20, 29, 50}; (b) local quantile with prevalence-bound correction t = quantile at
1 - alpha(1-pi_max); (c) a hybrid that shrinks the source threshold toward local controls (borrowing strength for small n);
(d) batch-correction baselines (MMUPHin-style location/scale per cohort) before the source threshold.
