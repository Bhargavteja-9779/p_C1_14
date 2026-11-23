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

## Round 2 (2026-11-23) — dev/explore_v2.py, results dev/explore_v2.csv (author chose HYBRID direction)
New: predictive (Laplace-averaged) location-scale transport with labelled local controls ("pctrl_k"), + unlabelled
pool ("hyb_free_k"), + soft Beta prior on prevalence mean 0.01 / strength 10 ("hyb_prior_k"); label-free with prior
("lf_prior"); STEP-3 baselines UPA alignment and free 2-comp GMM. k labelled controls in {5,10,20}; 50 splits.
Cohorts usable per k (pool needs >=8 controls after labelling): k=5: 7, k=10: 4, k=20: 3.

Mean |FPR-0.10| (violation rate FPR>0.15), pool all controls (pi=0) / natural case-control prevalence:
- k=5 : hyb_prior 0.087 (0.37) / 0.080 (0.05); lf_prior 0.093 / 0.083; local_q 0.098 / 0.096 (FPR 0.009, sens 0.21);
        source 0.116; EM 0.114 / 0.231; UPA 0.218 / 0.080; GMM2 0.423 / 0.103; shift_v1 0.226 / 0.096;
        conf_5 cannot set a threshold (FPR 0, sens 0); plain quantile of 5 controls 0.159 (viol 0.59).
- k=10: hyb_prior 0.073 / 0.078; conf_10 0.075 (viol 0.21); pctrl 0.094; hyb_free 0.094 / 0.076.
- k=20: hyb_prior 0.065 / 0.077; conf_20 0.065; pctrl 0.077.

Evaluation-noise check: no score ties; dev cohorts have 24-65 controls, so the FPR measured on the evaluation half
has sampling sd 0.05-0.08 by itself -> per-split |error| is dominated by evaluation noise. Per-cohort bias (mean over
splits, pi=0): source 0.114, local_q 0.055, lf_prior 0.042, hyb_prior_5 0.034, hyb_prior_10 0.031, conf_10 0.017.

Findings (honest):
1. hyb_prior is the best method at every k and prevalence for MAE, and the only usable option at k=5 (conformal
   needs >=10 controls to output a finite threshold at alpha=0.10). It cuts per-cohort bias of the source threshold
   by ~3x. The prevalence prior is what makes it work (hyb_free is clearly worse at low prevalence).
2. But margins on real data are modest: at k>=10 it ties conformal on MAE and has a larger upward bias
   (FPR 0.12-0.13 at pi=0, violation 0.32-0.39 vs 0.21-0.25). Residual bias ~0.03 = location-scale misspecification.
3. Label-free + prior (no labelled controls at all) is nearly as good as hyb_prior_5 -> the prior carries most of the
   gain at k=5; the labels' added value grows with k.
4. Dev cohorts are too small to resolve differences of ~0.01-0.02 in FPR. Must fix the evaluation design.

Decision for round 3:
- Evaluation: report bias and spread separately (per-cohort mean over splits), add a semi-synthetic benchmark with a
  known true FPR (real source scores, target generated by perturbing real control/case scores), and paired
  method-vs-method differences per split.
- Method: reduce misspecification bias — conformal-style finite-sample correction for the hybrid, or a more flexible
  (monotone) transport; plus the goodness-of-fit diagnostic with fallback to conformal.
