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

## Round 3 (2026-11-23) — dev/explore_v3.py, results dev/explore_v3.csv.gz, dev/explore_v3_selfcal.csv
New: (1) source-side SELF-CALIBRATION — rehearse deployment among the training cohorts (their out-of-fold scores;
no target data), choose the nominal level whose mean realised FPR equals alpha (chosen levels 0.036-0.12, mostly
0.06-0.09); "hyb_sc_k", label-free "lf_sc". (2) GoF (KS) gate with conformal fallback "hyb_gof_k" (flags 4-10%).
(3) SEMI-SYNTHETIC benchmark with known truth: each held-out dev cohort's real control/case score KDEs are the truth;
k labelled controls + pool of 60 controls (+cases) drawn from them; FPR/sensitivity exact. All 8 cohorts, k up to 40.

Semi-synthetic, controls-only pool (screening-like), mean |FPR-0.10| / mean FPR / P(FPR>0.15):
- hyb_sc: k=5 0.038/0.091/0.09; k=10 0.036/0.090/0.09; k=20 0.033/0.095/0.09; k=40 0.032/0.097/0.11
- conformal: k=5 no threshold; k=10 0.066/0.090/0.20; k=20 0.049/0.093/0.16; k=40 0.037/0.097/0.13
- label-free: local_q 0.032/0.114/0.17; lf_sc 0.042/0.089/0.10; source 0.102/0.135/0.38
Cohort-cluster bootstrap (16 model x cohort clusters), paired differences hyb_sc minus comparator:
- hyb_sc_5 vs conf_40: MAE +0.002 [-0.006, 0.012], violations -0.036 [-0.085, 0.033] -> 5 labelled controls match
  conformal with 40 (8x fewer).  At pi=0.05: MAE +0.008 [0.000, 0.017], violations -0.071 [-0.120, -0.016].
- hyb_sc_10 vs conf_10: MAE -0.030 [-0.037, -0.021], violations -0.110 [-0.159, -0.041].
- hyb_sc_5 vs hyb_prior_5: violations -0.10 [-0.14, -0.07] (self-calibration removes the upward FPR bias).
Real splits (noisy, 6-14 clusters): hyb_sc_5 vs local_q MAE -0.015 [-0.027, -0.004], violations -0.17 [-0.21, -0.12];
hyb_sc_5 vs conf_20 MAE -0.003 [-0.014, 0.015], violations -0.077 [-0.12, -0.03]; vs source MAE -0.040 [-0.075, -0.007].

Findings (honest):
1. Self-calibration fixes the residual bias: mean FPR 0.090-0.097 at target 0.10 for every k, violation rate ~0.09.
2. Headline: with 5 labelled local controls the method matches conformal with 40 on error, with fewer violations.
3. Labelled controls add only a small gain over the self-calibrated label-free variant (MAE -0.004 to -0.006),
   so the method is mainly "self-calibrated transport + prevalence prior", and labels are a cheap anchor.
4. With a nearly pure control pool, the naive local quantile is competitive on MAE (semi-synthetic) but violates the
   target ~2x more often and collapses as prevalence rises (FPR 0.009, sensitivity 0.21 at case-control prevalence).
5. Limitation: with case-control-like pools (~50% cases) all prior-based variants are conservative (FPR 0.02-0.04,
   lower sensitivity) because the prior is set for screening (1%). The direction is safe; must be stated.
6. GoF gate adds nothing over hyb_sc on average -> keep it as a reported diagnostic, not part of the method.

CANDIDATE METHOD (to be frozen after round 4 robustness): hyb_sc_k = predictive location-scale transport, k labelled
local controls + unlabelled pool, Beta prevalence prior (deployment prevalence, strength 10), source-side
self-calibration of the nominal level.
