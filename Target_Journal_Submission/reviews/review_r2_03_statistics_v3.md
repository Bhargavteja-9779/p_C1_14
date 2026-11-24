# Review round 2 (on manuscript_v3) - Statistical referee report (independent reviewer agent, 2026-11-24)
Reviewer's check scripts: reviews/r2_stats_scripts/ (het.py, dups.py, icc.py). VERDICT: MAJOR REVISION.

MAJOR
1. Exact beta-binomial "law" is true BY CONSTRUCTION: random within-cohort permutation splits make the count above the
   k-th burn-in order statistic BetaBinomial(M, N+1-k, k) for ANY data (ranks only). 0.088 vs 0.085 checks the RNG, not
   exchangeability. Same for 2 of 3 success criteria (BURN P(FPR>.15)<=.10, PAC P(FPR>.10)<=.07) - fixed by N, M. Only
   ">=50% lower error than SRC" is empirical. FIX: drop the exchangeability claim; test with NON-RANDOM splits (collection
   date/sample order; burn-in on one sub-site/country/batch, evaluate on another: MetaCardis countries, TettAJ a/b/c,
   HMP_2019 sub-studies; or calibrate on one cohort, evaluate on another of same country/site).
2. CROSS-COHORT DUPLICATES (r>0.99): ThomasAM_2019_c all 40 healthy = YachidaS (still counted as healthy population for
   IBD/T2D; DEV while Yachida LOCKED). DhakanDB_2019 ~ GuptaA_2019 (30 pairs = all GuptaA controls): GuptaA is CRC
   training -> DhakanDB not unseen (dups FPR 0.00 vs 0.091); DhakanDB (DEV) used as augmentation controls and GuptaA
   is LOCKED -> IBD augmentation "fixes" GuptaA 0.62/0.76 -> 0.03/0.03 = leakage. JieZ_2017: 49/171 controls duplicate
   QinJ_2012 (T2D training). No dups LifeLinesDeep-Schirmer, LeChatelier-Nielsen. FIX: global cross-cohort dedup; drop
   ThomasAM_2019_c and GuptaA as healthy populations; exclude duplicated JieZ/DhakanDB samples per classifier; rerun atlas,
   A4, augmentation, locked evaluation; correct 8,329/60.
3. Small cohorts inflate range / out-of-band share. DerSimonian-Laird logit: I2 0.88-0.95, tau 0.9-1.4, observed/binomial
   variance 10-20x, 95% PI CRC LASSO 0.009-0.34 -> heterogeneity real. But 0% from n=23-36 cohorts; 87% = VincentC.
   n>=100: CRC RF range 0.007-0.135, 41% out of band. Perfect calibration still puts 19-21% out of band by chance; at
   pooled 0.05 rate 43-48%. Chi-square unreliable (expected <1). FIX: tau, I2, prediction intervals as primary; ranges
   for n>=100; subtract binomial expectation from out-of-band share.
4. Locked burn-in at N=100: 38 units = only 7 distinct populations (Asnicar, MetaCardis, Schirmer, Shao, Xie, Zeevi,
   Yachida); contaminated pool N=100 = 3-4 cohorts; augmentation Wilcoxon treats repeated populations as independent.
   FIX: report distinct populations; cluster bootstrap/permutation by population.
5. ICC text wrong: variance falls 38-39% for IBD, rises 14-24% for T2D (signs reversed in text). "Explained none" false
   (IBD). "Each covariate associated" false (sex p>0.1 in 4/6; age p=0.68 IBD LASSO; Shannon p=0.60 T2D LASSO). Adjusted
   model uses 28-38 of 48-56 cohorts (raw ICC stable on all: 0.20-0.41). Shannon/richness = deviation from A4 protocol.
   Normal-scores CRC LASSO ICC 0.13 vs 0.20 (tails). FIX: correct text, label deviation.
6. Cut-off from LOCO fold-model OOF scores applied to final refit model -> level shift (pooled CRC FPR 0.05) inflates SRC
   error. FIX: score with averaged fold models or show shift negligible.

MINOR: BURN-PAC infeasible below N~29 (state); PAC result mixes eval noise; mis-specified pi_max gives bound 0.104, not a
guarantee; augmentation also harmed T2D RF (0.059->0.097); n>=70 cut-off, burn-in scored on n-50 vs n; 
control_augmentation_summary.txt has no generating script in repo (it was an inline heredoc - add script); at n>=15
augmentation 0.087 vs 0.078 (P=0.45); A5 replaced -> disclose deviation; protocols same-day (not externally verifiable);
multiplicity for T2D non-westernised P=0.005 and 6 Spearman tests; cross-N comparisons use different subsets.

Core finding holds: between-cohort FPR heterogeneity real (I2~0.9), cohort-level. Burn-in rule correct but standard.
