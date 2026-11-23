# Novelty escalation / method exploration log (DEV cohorts only)

Every idea tried during development is recorded here, including failures. Development data = 8 DEV CRC cohorts
(see data_lock.md). Target: FPR alpha = 0.10 (90% specificity).

## Round 1 (2026-11-23) - explore_v1.py, R = 30 random splits per held-out cohort
Setup: leave-one-cohort-out over the 8 DEV cohorts; held-out cohort split in half: half 1 = "unlabelled pool" (controls +
cases at prevalence pi in {0, 0.05, 0.2, natural ~0.5}), half 2 = evaluation. ctrl10 = 10 labelled local controls from half 1.

Mean realised FPR / mean |FPR - 0.10| / mean sensitivity:

| model | pi | source | local_q | EM | site_shift v1 | ctrl10 (conformal) |
|---|---|---|---|---|---|---|
| LASSO | 0 | .160/.127/.50 | .137/.085/.51 | .170/.109/.55 | .282/.215/.62 | .088/.078/.42 |
| LASSO | .05 | .160/.127/.50 | .113/.078/.48 | .169/.117/.54 | .250/.184/.59 | .088/.078/.42 |
| LASSO | .2 | .160/.127/.50 | .065/.079/.37 | .184/.139/.54 | .181/.123/.54 | .088/.078/.42 |
| LASSO | nat | .160/.127/.50 | .008/.092/.23 | .275/.243/.56 | .108/.079/.45 | .088/.078/.42 |
| RF | 0 | .091/.106/.48 | .134/.076/.55 | .142/.088/.55 | .374/.293/.73 | .088/.078/.48 |
| RF | .05 | .091/.106/.48 | .111/.067/.53 | .125/.082/.53 | .295/.232/.69 | .088/.078/.48 |
| RF | .2 | .091/.106/.48 | .050/.078/.42 | .123/.099/.51 | .197/.162/.61 | .088/.078/.48 |
| RF | nat | .091/.106/.48 | .016/.090/.24 | .183/.144/.57 | .109/.090/.50 | .088/.078/.48 |

Verdict:
- Problem confirmed on DEV: source threshold misses target by 0.11-0.13 on average (LASSO mean FPR 0.16).
- **site_shift v1 FAILS** at low prevalence (the realistic screening setting): with no/few cases, the mixture
  re-labels the control upper tail as "cases", shifts location down, and the threshold drops (FPR up to 0.37).
  Location shift and prevalence are weakly identifiable from unlabelled scores alone. Confirmed on synthetic data
  (bias -0.4, SD 0.66 at pi = 0). Only competitive at natural ~50% case-control prevalence (not a deployment setting).
- EM label-shift does not fix site shift (it only re-estimates prevalence).
- Naive local quantile is good only if the pool is nearly all controls; biased when cases present.
- 10 labelled local controls (conformal order statistic) give the best |error| but are conservative (k = n -> max of 10
  controls) and lose sensitivity.
=> Drop fully label-free v1 as headline. Round 2 idea: **control-anchored transport** - use a small number n of
  labelled local controls to fit a location-scale map of the source control score distribution (a, b by ML / quantile
  matching), threshold = a + b * t_src; optionally add the unlabelled pool with prevalence constrained small.
  Hypothesis: lower variance than the order statistic at the same n -> FPR closer to target and higher sensitivity.
