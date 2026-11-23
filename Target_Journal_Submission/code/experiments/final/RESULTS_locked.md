# Locked analysis results (run once after freeze commit 7be2b56; 2026-11-23)
Full output: analyze_final.log / results/summary.txt. Nothing below was changed after seeing results.

## Part A - sequential recalibration (primary)
- H1 pooled (32 site x model units): share of months 7-12 with FPR > 0.12, vp minus comparator:
  source -0.462 (95% CI -0.658, -0.195), Wilcoxon p = 0.011; local_q -0.095 (-0.187, -0.028), p = 2.5e-7;
  contam -0.040 (-0.093, -0.006), p = 0.049. -> SUPPORTED.
  By disease vs source: CRC -0.826 (p = 0.031); IBD -0.374 (p = 0.31); T2D -0.492 (p = 0.094); adenoma -0.291 (p = 0.48)
  -> significant only for CRC (few sites per disease; source threshold happens to be conservative at some sites).
- H2: sens(vp) - sens(oracle) = -0.015 (-0.021, -0.009); non-inferior at -0.05 -> SUPPORTED.
- Primary means (months 7-12; all diseases): FPR vp .085 (P(>.12) .006) vs source .171 (.488), local_q .098 (.100),
  contam .088 (.047), oracle .112.
- Harms per 1,000 screened at 1% prevalence, 12-month average: CRC unnecessary referrals vp 104 vs source 187
  (83 fewer), missed cancers 4.7 vs 3.6 (+1.1; the source cut-off overshoots its FPR target, which also raises
  sensitivity); IBD 88 vs 143; T2D 102 vs 257.
- Burn-in month referral rate: vp .27 vs .19 (source).
## Sensitivity analyses (months 7-12, mean FPR / P(FPR > alpha + .02))
  B50 .083/.025; B200 .085/.001; alpha .05: .034/.002; alpha .20: .182/.029; attendance 70% .078/.003;
  miss 5% .083/.005; delay 1 month .082/.004; pi_max misspecified .091/.022; burn-in 3*alpha .085/.007;
  smoothed populations .096/.026.
  Drift (+0.5 logit from month 7), vp: months 7-9 .173/.456, 10-12 .086/.066, 13-18 .085/.025
  (source .350/.895; local_q 13-18 .139/.705). Combined stresses, vp: 7-9 .207/.822, 10-12 .110/.390, 13-18 .102/.202.
## Part B - comorbidity confirmation (H3; adjusted score difference, Holm within model)
  Confirmed: MetaCardis T2D (LASSO beta .35, p_holm < 1e-4; RF .34, < 1e-4); MetaCardis heart failure (LASSO .33,
  p_holm .003; RF .19, .017); QinJ T2D (RF .35, p_holm .0002; LASSO .21, nominal p .035, Holm .24).
  Not confirmed: MetaCardis CAD, IGT; KarlssonFH T2D/IGT; IBD cohorts (NielsenHB nominal p .013-.016, Holm .09-.13).
  Positivity ratios vs own controls: MetaCardis HF 2.25x (LASSO) / 2.30x (RF); T2D 1.70x / 3.08x; QinJ T2D 1.93x / 1.63x;
  NielsenHB IBD 2.16x / 13.7x. MetaCardis adjusted for sex only (age/BMI not sufficiently recorded).
  -> H3 PARTLY SUPPORTED (heart failure and T2D; not CAD/IGT; IBD suggestive).
## Part C - group-conditional recalibration at MetaCardis (H4), months 7-18
  pooled: HF FPR .21 (LASSO)/.16 (RF), P(>.12) .998/.980; T2D .14/.21, P .974/1.00; controls .083/.066.
  group-conditional: HF .084/.078 (P .152/.129); T2D .093/.094 (P .072/.060); CAD .088/.092; IGT .092/.090;
  controls .093/.093. Overall FPR group .092 vs pooled .095. Sensitivity proxy: HF .36/.44, T2D .39/.42 vs pooled .45/.53.
  -> H4 SUPPORTED, with the stated sensitivity trade-off in the over-flagged groups.
