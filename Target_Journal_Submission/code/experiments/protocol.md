# Frozen analysis protocol (DRAFT — becomes FROZEN when committed with the tag line "STATUS: FROZEN")

STATUS: DRAFT (awaiting round-4b robustness check on development cohorts)

## Method (final candidate, chosen on development cohorts only; see novelty_escalation_log.md rounds 1-4)
"Self-calibrated score transport" (code: src/calibrate.py — PredTransport.predictive + self_calibrate):
1. Source: out-of-fold (leave-one-cohort-out) classifier scores (logit scale) on the training cohorts.
2. Target score model: target score = a + b * source-equivalent score; class-conditional score shapes transported
   from source (KDE); target prevalence pi with Beta prior (mean = deployment prevalence, strength 10 pseudo-samples).
3. Fit (a, log b, logit pi) by penalised ML on k labelled local controls + unlabelled local pool; Laplace
   approximation of the posterior; threshold t solves posterior-predictive FPR(t) = alpha'.
4. alpha' from source-side self-calibration: rehearse deployment among training cohorts (10 draws each, grid
   alpha x [0.2, 1.8]) and choose the nominal level whose mean realised FPR equals alpha.
Fixed settings: prior strength 10; KDE Scott bandwidth; 400 posterior draws; Nelder-Mead from 3 starts.
Pre-specified deployment-prevalence prior means: CRC 0.01; adenoma 0.20; IBD 0.005; T2D 0.10.

## Comparators (all pre-specified)
Source threshold; local quantile of unlabelled pool; UPA alignment (Roschewitz 2023); Saerens EM; label-free
self-calibrated transport (lf_sc); conformal threshold from k labelled controls; plain quantile of k controls.

## Test sets (LOCKED; each run exactly once with this protocol)
- External CRC: train on the 8 development cohorts; deploy to YachidaS_2019, YuJ_2015, ThomasAM_2019_c.
- New diseases, leave-one-cohort-out within disease: IBD (4 cohorts), T2D (4), adenoma vs control (5).
Classifiers: LASSO, RF, HGB (settings in src/models.py). alpha = 0.10 primary; 0.05 and 0.20 secondary.
k in {5, 10, 20}; pool prevalence in {0, 0.01, 0.05, 0.20, natural}; pool 60 (semi-synthetic) / half the
non-labelled target samples (real splits); 50 real splits, 100 semi-synthetic draws.

## Endpoints
Primary: mean |realised FPR - alpha| at alpha = 0.10, k = 10, pool prevalence 0.01, semi-synthetic known-truth
benchmark, pooled over all locked tasks and classifiers; hybrid (hyb_sc_10) vs conformal (conf_10) and vs local
quantile; paired difference with task-cluster bootstrap 95% CI (2,000 resamples).
Secondary: violation rate P(FPR > 1.5 alpha); sensitivity; mean FPR (bias); real-split results; "labelled-controls
equivalence" (smallest k for conformal matching hyb_sc_5 error); per-1,000-screened excess colonoscopies and missed
cancers (CRC; prevalence 0.6%) vs an ideal threshold; GoF-flag rate and error in flagged vs unflagged runs.
Analyses not listed here will be labelled exploratory.
