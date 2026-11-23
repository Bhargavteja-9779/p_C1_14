# Novelty escalation log (D6) — DEVELOPMENT COHORTS ONLY (8 CRC dev cohorts; locked cohorts untouched)

## Round 1 (2026-11-23) — dev/explore_v1.py, results dev/explore_v1.csv
Setup: leave-one-cohort-out over 8 dev cohorts; target FPR alpha=0.10; each held-out cohort split 50/50 into an
unlabelled "pool" and an evaluation half; pool prevalence pi in {0, 0.05, 0.2, natural (~0.5)}; 100 splits;
LASSO and RF. Held-out AUC: LASSO 0.65-0.84, RF 0.60-0.90.

Mean realised FPR (target 0.10) / mean |FPR-0.10|:

| model | pool pi | source | local quantile | Saerens EM | site-shift v1 (ours) | 10 local controls |
|---|---|---|---|---|---|---|
| LASSO | 0    | 0.161/0.130 | 0.141/0.088 | 0.179/0.117 | 0.278/0.209 | 0.089/0.082 |
| LASSO | 0.05 | 0.161/0.130 | 0.114/0.078 | 0.170/0.116 | 0.247/0.182 | 0.089/0.082 |
| LASSO | 0.2  | 0.161/0.130 | 0.061/0.075 | 0.178/0.133 | 0.193/0.136 | 0.089/0.082 |
| LASSO | nat  | 0.161/0.130 | 0.011/0.091 | 0.262/0.230 | 0.116/**0.079** | 0.089/0.082 |
| RF    | 0    | 0.089/0.107 | 0.139/0.080 | 0.144/0.092 | 0.362/0.280 | 0.091/0.081 |
| RF    | 0.05 | 0.089/0.107 | 0.110/0.073 | 0.133/0.095 | 0.287/0.224 | 0.091/0.081 |
| RF    | 0.2  | 0.089/0.107 | 0.048/0.081 | 0.135/0.108 | 0.188/0.159 | 0.091/0.081 |
| RF    | nat  | 0.089/0.107 | 0.016/0.091 | 0.187/0.153 | 0.108/0.119 | 0.091/0.081 |

Findings (honest):
1. Problem confirmed on dev cohorts: the source threshold misses target by 0.11-0.13 on average (per-cohort FPR 0.00-0.40).
2. Site-shift v1 FAILS at low pool prevalence (the realistic screening case): FPR 0.25-0.36 at pi=0, i.e. worse
   than doing nothing. It is the best unlabelled method only at natural (~50%) case-control prevalence (LASSO).
   Diagnosis: (a, b, pi) are weakly identifiable — a controls-only pool is explained as a down-shifted mixture whose
   upper tail is "cases" (pi>0), giving too low a threshold. Overflow warnings = logit(pi) running off to extremes.
3. Saerens EM is unstable when class-conditional scores shift (GuptaA FPR 1.00, ZellerG 0.84 at natural pi).
4. Local quantile is good only when the pool is nearly all controls, and collapses (FPR ~0.01) as prevalence rises.
5. Ten labelled local controls (conformal) are the strongest and most stable option (mean |err| 0.08, unbiased).
   Any label-free method must beat or complement this to be publishable.

Decision for round 2 (not yet run):
- Do NOT pursue site-shift v1 as is.
- Candidates: (i) hybrid — few labelled local controls anchor (a, b) and the unlabelled pool only refines the
  control quantile; report "labelled controls saved" at equal error (novelty-search suggestion); (ii) regularised
  site-shift (prior on pi from the screening context, bound on b) with an abstain rule when the fit is
  unidentifiable; (iii) add baselines from STEP 3: UPA-style quantile alignment (Roschewitz 2023), Godau-style
  prevalence re-thresholding, free two-component mixture.
