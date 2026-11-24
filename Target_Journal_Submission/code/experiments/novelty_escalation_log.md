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

### Round 4 novelty check (2026-11-23, web search)
- No method found that re-sets a diagnostic cut-off at a new site from routinely verified positives with a finite-sample
  FPR guarantee. Closest: apple tasting theory (Helmbold et al. 2000; Raman et al. 2023, arXiv 2310.19064) - regret
  bounds, no calibrated threshold / FPR guarantee; verification-bias correction literature (Begg & Greenes; Alonzo &
  Pepe; de Groot et al. 2008 BMC Med Res Methodol 8:75) - corrects sensitivity/specificity estimates, not thresholds.
- Why verification bias does not break our rule: the FP count above t only needs labels of referred samples (all
  verified). Unverified negatives enter only via the denominator, bounded with pi_max. Sensitivity is NOT estimated
  by the rule (it would be biased); report it only from held-out evaluation.
- Threats to state: colonoscopy is an imperfect reference (missed lesions); follow-up window definition; burn-in
  over-referral must fit endoscopy capacity.
Rating (provisional): method novelty 3.5/5 (new combination with a guarantee, simple), framing 4/5.

## Round 5 (2026-11-23) - explore_v5.py: sequential deployment simulation; full output explore_v5.log
Design: each held-out DEV cohort = the site's population; true FPR/sensitivity of any threshold computed exactly on
all its controls/cases (removes evaluation noise). 12 monthly batches of B = 100 tests drawn with replacement at
prevalence pi in {0.01, 0.05, 0.10}; R = 100 streams per cohort. Thresholds updated monthly on the cumulative pool.
vp = verified_positive_seq (burn-in month at the source 70% control quantile; vp2 = 80% quantile); unverified samples
above a candidate t counted as possible false positives -> valid whatever the history of thresholds.
oracle = 90% quantile of the site's true control scores (FPR .111 by discreteness of small cohorts).

LASSO, months 7-12: mean FPR / P(monthly FPR > 0.12) / sens / referral rate
| pi | source | local_q | contam | vp / vp2 | oracle |
|---|---|---|---|---|---|
| .01 | .160/.50/.51/.16 | .109/.22/.48/.11 | .104/.15/.47/.11 | .082/.002/.48/.09 | .111/.13/.50/.12 |
| .05 | .160/.50/.51/.18 | .094/.08/.46/.11 | .088/.04/.46/.11 | .086/.003/.48/.11 | .111/.13/.50/.13 |
| .10 | .160/.50/.51/.20 | .073/.004/.43/.11 | .065/.001/.40/.10 | .085/.004/.48/.13 | .111/.13/.50/.15 |
RF: same pattern (vp months 7-12 FPR .081-.086, P(>.12) .001-.009, sens .50).
Burn-in month: vp FPR .345 / referral .35; vp2 FPR .274 / referral .28 (one month only); from month 2 both identical.
Harms per 1,000 screened, 12-month average, LASSO pi = .01: unnecessary referrals (FP) source 158, local_q 113,
contam 108, vp 103, vp2 97, oracle 110; missed cancers 4.95 / 5.17 / 5.26 / 5.06 / 5.14 / 5.01.

Verdict: **sequential verified-positive recalibration is the frozen candidate (vp2: 2*alpha burn-in)**.
- Only method whose per-month FPR almost never exceeds 0.12 at every prevalence (<= 0.4% of site-months after
  month 6 vs 22% local_q, 15% contam, 50% source at pi = .01), in every cohort (per-cohort FPR .079-.091).
- Sensitivity within ~0.02 of the oracle (gap from round 3-4 was a small-pool artefact).
- vs status quo (source cut-off, LASSO): ~55-60 fewer unnecessary colonoscopies per 1,000 screened per year at
  essentially unchanged missed cancers (+0.2 per 1,000).
- Price: one burn-in month with ~28% referrals; needs referral outcomes within one month (follow-up delay is a
  sensitivity analysis for the final protocol).
Limitations: cohort-as-population resampling uses <= 65 control scores per site (discrete), case-control cohorts
stand in for screening populations, colonoscopy treated as perfect reference.

## Round 6 (2026-11-23) - explore_v6.py: realism stress tests (18 months, R = 60); full output explore_v6.log
Scenarios: KDE-smoothed site population; colonoscopy attendance 70%; colonoscopy misses 5% of cancers; 1-month
follow-up delay; drift (+0.5 logit for all scores from month 7); all combined. Variants: cumulative pool (vp),
6-month window (vp_win6), drift alarm (vp_alarm: restart pool when the newest month's exact verified FP count
exceeds Binomial(m0, alpha) at p < 0.01).
Results (LASSO+RF, pi = .01/.05; mean FPR / P(FPR > .12)):
- attendance 70%, miss 5%, delay 1: no degradation (months 10-18 FPR .078-.085, P(>.12) <= .003).
- smoothed populations: FPR .095-.099; P(>.12) 3-8% in months 4-9 falling to <= 0.5% by months 13-18. The near-zero
  exceedance in round 5 was partly an artefact of discrete <= 65-score populations.
- drift: cumulative vp too slow (months 8-9 .26, months 13-18 .13-.14); window recovers only by months 13-18;
  **vp_alarm recovers in 1-2 months (months 8-9 .09, then .08-.09)** and is identical to vp without drift.
- combined: vp_alarm months 8-9 .18, 10-12 .11, 13-18 .10 with P(>.12) .23 - slower recovery with low attendance +
  delay (fewer verified FPs -> weaker alarm). Stated limitation.
Decision: frozen candidate = SequentialRecalibrator (vp + drift alarm), added to protocol (section 4.6, sensitivity
analyses f-j). Runner and analysis updated; DEV dry run passes.

## Round 7 (2026-11-23) - NEW ANGLE: CRC microbiome tests mistake chronic disease for cancer
explore_v7_comorb.py / explore_v7b_confound.py (DEV CRC model; 11 extra NON-locked cohorts downloaded:
JieZ_2017, QinN_2014, LiJ_2017, ChengpingW_2017, ZhuF_2020, LoombaR_2017, LiJ_2014, VilaAV_2018, HMP_2019_t2d,
NagySzakalD_2017, XieH_2016). Positivity at the source 90%-specificity threshold, within cohort (condition vs own
healthy controls), LASSO: cirrhosis 52% vs 8% (6.6x); ACVD 52% vs 19% (2.8x); hypertension 26% vs 7% (3.6x);
fatty liver 20% vs 6% (3.5x); ME/CFS 18% vs 10%; asthma/migraine ~1.6x; schizophrenia 5% vs 3%; T2D 30% (LiJ_2014,
n_ctrl = 10). RF same direction everywhere.
Confounding: score difference (logit) disease - control adjusted for age + BMI + sex: ACVD +0.87 (0.62-1.12),
cirrhosis +1.30 (0.99-1.60), hypertension +0.33 (0.07-0.60), ME/CFS +0.39 (0.12-0.67); fatty liver, asthma,
schizophrenia n.s. => not explained by age/BMI/sex.
Control augmentation (Thomas 2019; other conditions added as negatives in training) lowers positivity overall but the
disparity persists (ACVD 13% vs 2%).
Prior art: Wirbel 2019 (multi-study CRC models more disease-specific), Thomas 2019 (control augmentation), Duvallet
2017 (shared non-specific dysbiosis), Tito 2024 Nat Med (calprotectin/BMI dominate). Not found: false-alarm burden by
comorbidity in screening terms, or a deployment-time fix per group.

## Round 8 (2026-11-23) - explore_v8_groupcal.py: comorbidity-conditional sequential recalibration
Sites = comorbidity cohorts, screened population = healthy + condition share w (ACVD .20, cirrhosis .05,
hypertension .40, fatty liver .25, ME/CFS .05) + CRC 1%; B = 200/month, 18 months, R = 100.
Months 7-18, LASSO (RF same): pooled recalibration hits overall FPR (.085-.092) but comorbid FPR .19-.52 and
P(comorbid FPR > .12) = 99-100%, healthy pushed to .03-.08. Group-conditional: healthy .08-.09, comorbid .08-.09,
P(>.12) 1-4% (cirrhosis 12-15%: only ~10 comorbid tests/month).
Trade-off: comorbid-group sensitivity (proxy from OOF CRC case scores) falls (e.g. ACVD .31 -> .23; cirrhosis .50 -> .20)
while healthy sensitivity rises. Proxy likely overstates the loss (CRC patients with comorbidity probably score higher).
Equal false-alarm burden vs equal sensitivity is a policy choice; the method makes it explicit and controllable.

=> NEW STORY (stronger): "where and whom you screen" decides a microbiome test's false-alarm rate; pooled
recalibration hides a 2-6x excess false-alarm burden in people with common chronic diseases; routine colonoscopy
outcomes allow per-site, per-group recalibration with guarantees.
Locked confirmation of the comorbidity effect (never touched): MetaCardis_2020_a (CAD, HF, T2D, IGT vs controls),
QinJ_2012 and KarlssonFH_2013 (T2D), IBD cohorts (IBD as comorbidity).

## Round 9 (2026-11-23, after freeze; DEV cohorts only -> any locked use is POST HOC) - mechanism
explore_v9_mechanism.py, explore_v9b_axes.py. Score gap (condition - own controls) decomposed into species
contributions (LASSO coefficient x mean z-score shift). The CRC model's species explain the full adjusted gap.
Top drivers across 7 conditions: Streptococcus oralis, Lachnoclostridium, Fusobacterium nucleatum, Veillonella
parvula, Peptostreptococcus, Gemella morbillorum, Lactobacillus salivarius (enriched; oral-origin, and several are
the hallmark CRC markers) and depletion of Dialister CAG357, Bacteroides intestinalis, Eubacterium eligens, Roseburia.
Two routes to a false alarm: oral-taxa enrichment explains 78% (ACVD), 83% (cirrhosis), ~100% (fatty liver) of the gap;
commensal depletion explains 81% (hypertension), 56% (asthma); 'other enriched' 77% (ME/CFS).
Specificity-constrained signature (drop CRC species whose shift is shared with >= K of the other DEV conditions,
leave-one-condition-out): K = 4: 8 species dropped, CRC AUC .763 -> .748, disparity barely changes (mean comorbid
positivity .212 -> .213); K = 2: 32 dropped, AUC .721, sensitivity .474 -> .429, disparity reduced but not removed.
=> Training-side fixes cannot remove the excess without losing cancer detection, because the hallmark CRC species are
themselves shared with chronic disease. This motivates the deployment-side (group-conditional) fix.

## Addendum A1 results (2026-11-24; protocol_addendum_drugs.md committed before analysis)
Development check (direction only): PPI users flagged 1.1-2.7x as often in VincentC_2016, LeeKA_2022, JieZ_2017
(n_PPI 9-41; none significant).
MetaCardis (n = 1,831; 295 PPI users), adjusted for condition group, sex and other drugs:
- H5 (PPI raises the CRC score): LASSO +0.04 (95% CI -0.07, 0.15), p = 0.24 -> NOT supported for the primary model;
  RF +0.087 (0.009, 0.164), p = 0.014; positivity RR 1.21 (0.89-1.59) LASSO, 1.39 (1.02-1.81) RF.
- H6 (PPI raises the oral-taxa component): +0.175 (0.144, 0.206), p < 1e-10 -> SUPPORTED. The oral increase is offset by
  other score components in LASSO (PPI coefficient becomes -0.12 when the oral component is adjusted for).
- Secondary/exploratory: metformin +0.43 (0.30, 0.55) LASSO, +0.37 (0.29, 0.46) RF, p < 1e-10; beta-blocker +0.09
  (p = 0.03, LASSO only); statin, aspirin ~0.
Exploratory follow-up (addendum_metformin_explore.py): within T2D, metformin users vs non-users flagged
20.5% vs 8.5% (LASSO; adj. +0.44, p < 1e-6) and 27.9% vs 7.1% (RF) in MetaCardis (379 vs 124); LiJ_2014 same direction
(+0.40, p = 0.18; RF +0.28, p = 0.12; 58 vs 17); QinJ_2012 (15 users) and KarlssonFH_2013 (20 users) null.
Drivers: Lachnoclostridium, Enterobacterales/Morganellaceae, Streptococcus salivarius enriched; E. eligens,
Firmicutes CAG110 depleted. => hypothesis-generating: the T2D false-alarm excess in MetaCardis is largely a metformin signal.
