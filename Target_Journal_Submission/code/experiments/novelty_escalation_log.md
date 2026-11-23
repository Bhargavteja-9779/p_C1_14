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

## Round 2 (2026-11-23) - explore_v2.py, R = 200 draws of n local controls per held-out cohort
Methods with n labelled local controls: conformal order statistic (baseline with finite-sample E[FPR] <= alpha),
normal (mean + z*sd of controls, no source info), and control-anchored transport of the source control distribution:
shift (location only), moment (mean/sd), robust (median/MAD). Full table: explore_v2.log.

Key numbers (n = 10; mean FPR / mean |err| / P(FPR > 0.15) / sens):
- LASSO: conformal .090/.080/.22/.42; shift .098/.068/.22/.45; moment .134/.089/.35/.49; source .159/.127/.48/.51
- RF:    conformal .090/.078/.21/.48; shift .085/.089/.23/.46; moment .146/.093/.44/.56; source .089/.104/.21/.48

Verdict:
- **Location-scale transport FAILS**: moment/robust are anti-conservative (FPR 0.13-0.21) - estimating scale from
  5-20 controls is too noisy, and the source score shape does not transfer (per-cohort FPR of 'shift' ranges
  0.00-0.27). The score-distribution *shape* changes across cohorts, not only location/scale.
- Location-only shift helps LASSO a little on average (|err| .068 vs .080) but has large per-cohort bias -> not robust.
- The conformal order statistic stays the only method that hits target in every cohort (per-cohort mean FPR
  0.076-0.103). With n = 5 it cannot reach alpha = 0.10 at all (k > n -> threshold = +inf), so n >= 9 is required
  at alpha = 0.10 (n >= (1-alpha)/alpha).
- So far no new threshold method beats the simple guarantee-backed baseline. A method contribution needs a different
  angle (see the decision in PROGRESS.md).

## Round 3 (2026-11-23) - explore_v3.py, R = 300; full table explore_v3.log
New methods:
- pac_controls: order-statistic threshold from n labelled controls with P(FPR > 0.15) <= 0.10 (binomial/Beta bound).
- contam_quantile (label-free): conformal rank of the unlabeled pool at level (1-alpha)(1-pi_max)+pi_max. Needs only an
  upper bound pi_max on prevalence; valid for ANY case-score distribution (no transport/shape assumption).
Pool = half of the held-out cohort's controls (m = 12-32) + cases drawn at true prevalence pi.

Mean FPR / P(FPR > 0.15) / sens (LASSO; RF similar):
| true pi | source | local_q (assumes pi = 0) | contam pi_max=.02 | .05 | .10 |
|---|---|---|---|---|---|
| 0 | .160/.49/.51 | .140/.40/.51 | .082/.19/.42 | .074/.15/.41 | .070/.14/.40 |
| .01 | .160/.49/.51 | .136/.39/.50 | .078/.18/.41 | .072/.15/.40 | .067/.13/.39 |
| .05 | .160/.49/.51 | .121/.32/.48 | .062/.12/.38 | .060/.12/.38 | .055/.10/.36 |
| .10 | .160/.49/.51 | .104/.25/.46 | .049/.08/.34 | .048/.08/.34 | .045/.07/.33 |
Labelled controls: conf_n20 .095/.25/.52; pac_n20 .051/.09/.43; pac_n10 impossible (n too small).

Verdict:
- **contam_quantile WORKS as a label-free method**: mean FPR <= target in every setting, even when true pi > pi_max
  (cases mostly score high, so contamination only makes it more conservative), and it matches the labelled
  'conf_all' (same pool, labelled) at pi = 0. Price: conservative -> sensitivity ~0.40 vs ~0.50 for source, mainly
  because DEV pools are tiny (m = 12-32 -> rank rounding). Must show convergence to target as m grows (screening
  sites accumulate hundreds of tests/month) - simulate with larger cohorts / bootstrap pools in final experiments.
- CAVEAT on P(FPR > 0.15): evaluation halves have only 12-33 controls, so realised FPR is itself noisy. Needs an
  oracle noise floor (threshold set on the true held-out controls) before per-deployment claims are made.
- Novelty check needed: "conformal with contaminated calibration / reference data" (outlier-detection literature,
  PU learning, mixture proportion estimation bounds) may already contain this bound. If so, the contribution is
  its application + evaluation for microbiome diagnostics, not the bound itself.
- Candidate frozen method set for the final protocol: source (status quo), local_q, EM, contam_quantile(pi_max),
  conformal-n and PAC-n local controls; LASSO + RF.

### Round 3 novelty check (2026-11-23, web search)
- Bashari, Sesia & Romano 2025 (ICML, PMLR v267; arXiv 2502.04807): conformal calibration on a contaminated reference
  set gives conservative type-I control under non-adversarial contamination; they add active cleaning with a small
  labelling budget. => our label-free contam_quantile is a close relative (we add the explicit pi_max rank correction,
  which makes validity hold without their non-adversarial condition). Method novelty: LOW.
- Blanchard, Lee & Scott 2010 (JMLR): semi-supervised novelty detection reduced to NP classification with a mixture
  of nominal + novel data; mixture-proportion estimation. Related foundation.
=> The method side is a principled application of known tools. A realistic contribution claim for an iMeta Letter is:
   (1) first systematic evidence that microbiome classifier cut-offs drift across sites, hidden by AUROC-only LOSO;
   (2) a deployment recipe with guarantees (label-free pi_max-bounded pool quantile; >= 20 local controls with
   conformal/PAC) shown to restore target specificity across 3 diseases; (3) harms per 1,000 screened.

## Round 4 (2026-11-23) - explore_v4.py, R = 300; full table explore_v4.log
Idea (deployment fact): in screening every test-positive is referred to colonoscopy, so labels ABOVE the referral
threshold arrive for free; labels below it never do (one-sided / verification-biased feedback).
verified_positive(): during a burn-in, refer pool samples above a liberal t0 (contam quantile at 2*alpha or 3*alpha,
or min(source, that)); count false positives EXACTLY among verified referrals; contamination by unverified cases
only enters the denominator via the prevalence bound pi_max. Threshold = smallest t >= t0 with
(FP(t)+1)/(m0_lo+1) <= alpha. Reference 'oracle_pool' = conformal threshold with ALL pool labels known.
Prevalence bound used: pi_max = max(0.05, true pi).

Mean FPR / sens (LASSO; RF same pattern); burn-in referral fraction in brackets:
| true pi | source | local_q | contam | oracle_pool | vp_2a | vp_3a | vp_src |
|---|---|---|---|---|---|---|---|
| 0 | .159/.50 | .137/.51 | .071/.40 | .078/.42 | .078/.42 [.17] | .078/.42 [.27] | .078/.42 [.23] |
| .05 | .159/.50 | .119/.48 | .059/.37 | .078/.42 | .078/.42 [.18] | .078/.42 [.27] | .078/.42 [.24] |
| .10 | .159/.50 | .101/.45 | .042/.33 | .078/.42 | .075/.41 [.17] | .077/.41 [.26] | .076/.41 [.24] |
| .30 | .159/.50 | .041/.32 | .008/.16 | .078/.42 | .032/.31 [.13] | .061/.39 [.20] | .061/.40 [.28] |

Verdict:
- **verified_positive WORKS**: equals the fully-labelled oracle for pi <= 0.10 in every DEV cohort (per-cohort FPR
  0.062-0.101 at pi = .05), never exceeds target, and does not degrade with prevalence like contam/local_q.
  At pi = 0.30 (e.g. adenoma, symptomatic clinics) a more liberal burn-in (3*alpha) is needed.
- Costs: one burn-in batch with 17-27% referrals instead of 10%. Sensitivity gap vs source (.42 vs .50) is the price
  of honesty on DEV pools of 12-32 controls (even the oracle sits at FPR .078 by rank rounding) - must re-measure with
  larger pools (YachidaS 251 controls is locked; use bootstrapped deployment streams in final experiments).
- Prior art to position against: apple tasting / one-sided feedback (Helmbold, Littlestone & Long 2000), selective
  labels (Lakkaraju 2017), verification bias in diagnostic accuracy (Begg & Greenes 1983). Novelty claim: a
  finite-sample FPR-valid re-thresholding rule that uses only routinely verified positives + a prevalence bound,
  evaluated for microbiome diagnostics. To check in a targeted search before freezing.
- Next: sequential version (monthly batches, threshold updated as verified referrals accrue) and harm per 1,000.
