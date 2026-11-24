# iMeta — Reviewer report (Round 2)

**Manuscript (rev2):** "Microbiome colorectal cancer classifiers lose specificity across sites and patients; local recalibration restores it" (Letter)
**Reviewer expertise:** gut microbiome machine learning; biostatistics / diagnostic accuracy
**Materials examined:** submission_package/Manuscript.md; manuscript/SI_methods.md, SI_tables.md; REVISION_LOG.md; round-1 editor and reviewer reports; Figure1.png, Figure2.png; experiments/final/RESULTS_locked.md, analyze_final.log; addendum_results_confirm.log, addendum_metformin_explore.log; posthoc_within_crc_comorbidity.log, posthoc_metacardis_drugadjusted.log/.py, posthoc_stream_noreplacement.log/.py, posthoc_drift_restrict.log; addendum_results/*.csv; dev/explore_v9_mechanism.log, dev/explore_v10_batchcorr.log; novelty_escalation_log.md; protocol.md, protocol_freeze_hashes.txt; src/calibrate.py (diff against freeze commit 7be2b56); cutoffguard (core.py, tests — all 4 tests pass); pilot/pilot_threshold_transfer.log.
Unfilled author placeholders (names, e-mail, ORCID, repository URL, DOI) were ignored as instructed.

---

## 0. Overall assessment

The revision is a real improvement. The Letter now has one storyline. The within-CRC null (P1) is reported. The PPI primary hypothesis is reported as not supported. MetaCardis has been re-fitted with country and drugs, and the locked HF/T2D decomposition is shown. Proposition S1 has been narrowed correctly in the SI. The label-free prevalence-bounded rule is now discussed honestly. Highlights are gone, the title is 14 words, there are 19 references, and a design panel has been added. Most numbers check out (Section 3).

The remaining problems are mainly about reporting and labelling, and some were introduced by the revision itself:

- **Selective reporting in the new "no resampling" analysis.** In that analysis the label-free prevalence-bounded rule does better than the proposed standard rule (14% vs 19% of months above 0.12; Fig. 2D). The text does not mention this. In practice the analysis is also a single T2D-classifier site.
- **Post hoc material is not labelled.** Several post hoc analyses and one post hoc method change (the high-confidence option, which changed the frozen `calibrate.py` and broke its hash) appear in the main text without a "post hoc" label.
- **The heart-failure claim picks a favourable model.** "The heart-failure effect persisted" holds only for the LASSO model with country + drugs. It does not hold for random forest or for the complete-case age/BMI model.
- **A few factual mismatches.** Examples: "random forest did not improve" (Table S7); the Fig. 1C adjustment legend; rounding in two confidence intervals.

All of these can be fixed with the existing data and code.

---

## 1. Status of round-1 major points

### Editor (R1–R8)

| Point | Status | Why |
|---|---|---|
| R1 Incomplete package / verifiable pre-registration | **Partly** (placeholders ignored) | Two things remain beyond the placeholders. "Frozen in a time-stamped commit" can only be checked once a public archive (Zenodo/OSF) exists. And `src/calibrate.py` no longer matches its frozen hash (see N5). |
| R2 Novelty / prior art | **Addressed** | Wirbel 2021 and Thomas 2019 are credited for cross-disease firing. Godau, SACSIM and Tong are cited and contrasted. The increment is stated as per-site and per-group realised specificity plus outcome-based recalibration. |
| R3 One spine | **Mostly addressed** | The Letter now has a single storyline, and the guarantee and robustness details are in the SI. The new no-resampling and high-confidence material adds back some statistical weight. |
| R4 Overstated clinical premise | **Partly** | Sensitivity is now given with the harm numbers (0.52 vs 0.64). Still missing: a sentence saying that no stool-metagenomic CRC test is used in screening today ("if deployed, e.g. with FIT"), any comparison with FIT, and sensitivity next to the per-site FPR claims. |
| R5 Confounding; metformin undercuts "chronic disease" | **Mostly addressed** | The model has been re-fitted with country and drugs. Metformin non-users are now reported. "Chronic disease" has been removed from the title. But the HF result is reported selectively (N3), and confounding by indication is still not mentioned. |
| R6 Small edge over label-free rule; flattering simulation | **Partly** | The label-free comparison is now honest at stable sites, burn-in cost is reported, and small sites are analysed. However, the "no resampling" analysis uses a random order, not a time order. Random permutation keeps exchangeability, so it does not test drift. That analysis also shows the label-free rule doing better, and the text omits this (N1). |
| R7 Data reuse / locked status | **Mostly addressed** | The pilot p-value has been dropped, and the main text separates 11 fully independent sites from 16. But pilot exposure of the three locked CRC sites is disclosed only in SI S1. The main text still says methods were frozen "before 16 held-out sites were analysed once", and the GA says "16 held-out sites" without qualification. |
| R8 Format | **Addressed** | Highlights removed; title 14 words; 19 references; design panel (Fig. 1A); jargon removed from figures; Fig. 2D replaced. The graphical abstract was not re-checked here. |

### Reviewer (M1–M9; the brief names M1–M6, and M7–M9 are included for completeness)

| Point | Status | Why |
|---|---|---|
| M1 Within-CRC comorbidity analysis not reported | **Addressed, with new overclaim** | P1 is now reported (Table S8; Fig. 1C) and the title is narrowed. But "Mild cardiometabolic labels therefore do not drive false positives" turns a small null (70 comorbid controls; CI −0.60 to 0.21) into a negative claim. It also ignores that comorbid controls were flagged *less* often (RF OR 0.10, p = 0.04). P1 is not labelled post hoc in the main text. |
| M2 MetaCardis confounded by country, age, drugs | **Mostly addressed** | Table S9 adds country, drugs and complete-case age/BMI, and "healthy" has been dropped for MetaCardis controls. Not done: a Denmark-only (country-stratified) HF analysis and multiple imputation. The main text reports only the most favourable HF model (N3). |
| M3 Primary-endpoint advantage is a small-site artefact; reverses when smoothed | **Partly** | The ≥40-control analysis is reported and the comparison with the prevalence-bounded rule is honest. Still missing: per-disease H1 (only CRC is significant against source), the reversal in the smoothed setting (vp 0.026 vs prevalence-bounded 0.004), and a matched-FPR comparison. Also, at ≥40 controls the pre-specified vp-vs-source contrast is not significant (p = 0.074), and the text does not say so. |
| M4 Circular simulation; comparators lack restart; costs | **Partly** | Downward drift, sensitivity cost and burn-in cost are now reported, and simulation limits are stated in the Conclusion. Comparators still have no restart, yet Fig. 2B is titled "only the drift alarm recovers". IBD and T2D "screening" sites still drive Fig. 2A and the pooled H1, and the no-resampling result is mostly a T2D site. |
| M5 Proposition S1 scope | **Mostly addressed** | The SI now has the realised-count form of A2, the marginal wording, t* = +∞, the drift corollary marked as not proven, and the corrected numerical check (0.092). Three gaps remain. The main text still says "prevalence stays below the bound". The per-group corollary does not state that A1/A2 and π_max must hold within each group. δ is never reported. |
| M6 Locked/independent status overstated | **Partly** | The pilot and the 16/11 split are disclosed. SI S4 still calls the settings smoothing, 70% attendance, 5% missed cancers, drift and combined "pre-specified", but protocol §8 lists only (a)–(e). New post hoc analyses are not labelled in the main text (N4). |
| M7 Medication spin; metformin interpretation | **Partly** | The PPI primary is now reported as not supported. Metformin drivers are softened to "depleted commensal fermenters … Enterobacterales", but Enterobacterales contributes only 0.037; Lachnoclostridium (0.097) and *E. eligens* (0.091) are larger. The replication sentence is unchanged and still inaccurate (LiJ_2014 RF goes the opposite way; KarlssonFH β is positive). Confounding by indication is not discussed. H6, which is close to tautological, is still described as "supports the oral route". |
| M8 Mechanism evidence thin | **Partly** | Percentages are now restricted to cirrhosis and ACVD, and the "cannot be cleaned" heading and the control-augmentation claim are gone. Table S4 still has no "None" row although its caption promises one. There is no per-species oral/non-oral list, no bootstrap CIs, and no species table for the locked HF/T2D gaps. |
| M9 Overdispersion test | **Addressed (by removal)** | The p-value has been removed from the main text and the pilot log is deposited. |

---

## 2. New problems introduced by the revision

### Major

**N1. No-resampling analysis (P3, Fig. 2D, Table S10): selective reporting and a weak design.**
- **The text omits the best performer.** It reports only vp (19% of months above 0.12) and vp_hc (5%). In Fig. 2D and the log, the label-free prevalence-bounded rule reaches **14%** (FPR 0.089), better than the standard proposed rule. This is the most realistic analysis in the paper, so its result belongs in the text.
- **The comparison is unfair.** The high-confidence modification is applied only to vp. A binomial order-statistic version of the prevalence-bounded rule would be just as easy to build.
- **The analysis is effectively one T2D site.** With B = 50 per month and at least 40 controls kept unseen:
  - YachidaS_2019 (251 controls) gives only 3 months, so only month 3 enters "months ≥3".
  - QinJ_2012 (174 controls) gives 1 month and contributes nothing.
  - MetaCardis gives 11 months.
  - So the pooled estimate is driven by the MetaCardis **T2D classifier**, where "colonoscopy verification of test positives" has no clinical meaning. At that site the source cut-off is already conservative (FPR 0.038), so recalibration *raises* the FPR.
- **"Two largest held-out sites" is inaccurate.** The script ran four site–classifier analyses (Yachida CRC, Yachida adenoma, MetaCardis T2D, QinJ T2D).
- **The FPR estimate is noisy.** FPR on the controls not yet seen is measured on as few as 41–51 controls at Yachida. That is the same small-n discreteness the authors use to explain away the H1 gap against the prevalence-bounded rule.
- **"Random order" does not test drift.** A random permutation keeps exchangeability, which was the editor's point in R6. A time- or batch-ordered stream would test it. For example, MetaCardis ordered by recruitment country, which is available and differs sharply by group.
- **Table S10 does not reproduce the text.** Its simple per-site mean for vp_hc is FPR 0.068, not 0.071. The text and Fig. 2D come from the log's prevalence-pooled rows, so Table S10 should give the pooled rows too.

**N2. High-confidence option: δ not reported; metric does not match the guarantee; post hoc.**
- The P3 script uses δ = 0.10. Neither the main text nor the SI says so.
- The guarantee is P(FPR > α = 0.10) ≤ δ, but the reported metric is the share of months with FPR > 0.12. Report P(FPR > 0.10) and compare it with δ.
- Report the sensitivity cost of vp_hc. Its FPR of 0.071 means it is markedly conservative.
- The option was created after the locked analysis. It is presented as part of the method (main text, GA, Conclusion) without a post hoc label.
- The derivation in SI S7 is correct. Since BinomCDF(k; m0, α) ≤ BinomCDF(k; m0_lo, α) whenever m0 ≥ m0_lo, using m0_lo is conservative.

**N3. Heart-failure result reported selectively.**
- "The heart-failure effect persisted (+0.28, 0.06–0.51)" is true only for LASSO with sex + country + drugs.
- Under other specifications (Table S9) it is not significant:
  - LASSO, sex + drugs: +0.20 (−0.02 to 0.41).
  - LASSO, complete-case age/BMI: +0.28 (−0.12 to 0.68).
  - RF, sex + country + drugs: +0.13 (−0.03 to 0.29).
  - RF, complete-case: +0.25 (−0.05 to 0.55).
- Conversely, IGT becomes nominally positive under full adjustment (+0.12, p = 0.044), and RF CAD is positive with sex + country (p = 0.03). Neither is mentioned.
- Suggested wording: "attenuated; remained significant only for LASSO with country and drug adjustment". Add the Denmark-only contrast (73 HF vs 192 controls).

**N4. Post hoc labelling and the "frozen protocol" framing.**
- The opening paragraph says "All methods and endpoints were fixed in a protocol … before 16 held-out sites were analysed once." About half the Results are now post hoc, yet only P2 is labelled "(post hoc)" in the main text. The unlabelled post hoc material is:
  - P1 (within-CRC comorbidity);
  - P3 (no resampling);
  - P4 (downward drift and the ≥40-control restriction);
  - D10 (batch correction);
  - the high-confidence option.
- Label each one in the main text, or add one sentence listing them.

**N5. Frozen code changed after the freeze.**
- `src/calibrate.py` now hashes to `1f6ba2a1…`. The freeze record (protocol_freeze_hashes.txt) lists `989f787b…`.
- The diff against 7be2b56 only adds the optional `delta` argument, and the default behaviour is unchanged. Even so, the paper's "file hashes provided" verification now fails for the core module.
- Either restore the frozen file and put the new option in a separate module or in `cutoffguard` only, or disclose the change and give both hashes.

### Moderate

**N6. "Mild cardiometabolic labels therefore do not drive false positives".** This is an absence-of-evidence claim from 70 comorbid controls in three heterogeneous cohorts. The healthy-control positivity is 0% at FengQ and 40% at ThomasAM_2018a. Suggested wording: "were not associated with more false positives (in fact fewer)". Also describe the inverse association.

**N7. ≥40-control analysis reported in part.**
- In "vanished at the nine cohorts with at least 40 controls (FPR 0.090 vs 0.083; p = 0.72)", the FPRs are means but the p-value is for the exceedance endpoint. Say so.
- In the same analysis, vp vs source gives p = 0.074, so the pre-specified primary contrast is not significant at the larger sites. Report it.
- State that this analysis is post hoc.

**N8. Table S7 claim is wrong.** "Random forest did not improve" contradicts Table S7 and explore_v10_batchcorr.log:
- RF share of sites above 0.12: 0.375 → 0.25 with both site_z and site_rank.
- RF mean |FPR − α|: 0.102 → 0.048 with site_rank.

Only site_z for RF has a worse maximum (0.393 vs 0.361).

**N9. Locked T2D estimate taken from the post hoc refit.** The text quotes T2D "+0.36 (0.26–0.46)". That is the Table S9 sex-only refit. The pre-specified locked estimate is +0.35 (0.25–0.45) (Table S3b, RESULTS_locked.md). Quote the locked result. "Both Holm-adjusted p < 0.01" is true for LASSO only (RF HF p_holm = 0.017); say "LASSO".

**N10. Comparators in the drift scenario.** Fig. 2B's title ("only the drift alarm recovers") and "the label-free rules stayed high (0.086 vs 0.154)" describe a design choice: the comparators use an ever-growing pool with no window or alarm. Either give them a positivity-rate restart or change the title and text. Note also that 0.154 is the prevalence-bounded rule pooled over all 16 sites (local quantile 0.173), whereas Fig. 2B shows 11 sites.

### Minor

- **N11. Fig. 1C legend.** It says the development estimates are "adjusted for age, BMI and sex". Hypertension (LiJ_2017) and fatty liver (LoombaR_2017) are unadjusted (covs = nan, Table S3c). This is unchanged from round 1 (editor #7, reviewer minor 9).
- **N12. Cirrhosis positivity "52% vs 8%".** This figure is in no SI table. The later frozen-model analysis (explore_v9 "None" row) gives 43% vs 4.4% for QinN_2014. Reconcile the two, and add development positivity to the SI.
- **N13. Locked decomposition.** There is no species-level table for HF, T2D or metformin. "Enterobacterales" in the text and the Fig. 1D legend is unsupported for HF/T2D, and minor for metformin. *S. salivarius*, an oral *Streptococcus*, contributes +0.055 to the metformin gap, yet the metformin "oral" component is −0.034. Give the per-species classification and the top contributors per locked contrast.
- **N14. Citations.** SI references S2–S6 are never cited in the SI text. "Original cohort publications are listed by PMID in Table S1", but Table S1 has no PMID column. QinJ_2012 ("a second T2D cohort") is now uncited. The Data Availability Statement lists release 2022-04-13, which SI S1 does not mention.
- **N15. Rounding.** HF fully adjusted: 0.0639–0.5047 should be 0.06–0.50 (text 0.51). T2D fully adjusted: −0.0249 should be −0.02 (text −0.03).
- **N16. Unchanged from round 1.** Table S3 still shows "999.00" upper CI bounds. HMP_2019_ibdmdb is 103/27 in Table S1 but 57/14 in Table S3, unexplained. IjazUZ_2017 is missing from Table S3. The Table S4 "None" row is missing. HF per-group P_over (15%) is not mentioned next to "every group to 0.08–0.09". scikit-learn version is not pinned (S8), although `l1_ratio=1` relies on version ≥ 1.8. Group shares in Part C are not justified.
- **N17. Revision log.** It says the title has 18 words; the title has 14. Internal only.

---

## 3. Verification of every number in the main text (and GA)

| # | Claim | Source | Status |
|---|---|---|---|
| 1 | GA: 16 held-out sites, FPR 0%–75% | analyze_final per-site; Fig. 1B (axis now to 0.8; RF T2D ≈ 0.75) | ok |
| 2 | AUROC ≈ 0.8 across countries [1,2] | literature | ok (external) |
| 3 | 32 public cohorts (Table S1) | Table S1: 30 main + VincentC_2016 + LeeKA_2022 | ok |
| 4 | 3 external CRC sites; 8 development cohorts; IBD 4, T2D 4, adenoma 5 | SI S1; Table S1 | ok |
| 5 | Realised FPR 0.00–0.75 | Fig. 1B; analyze_final (T2D mean 0.259) | ok |
| 6 | 12 of 22 pairs above 0.12 in 11 independent sites | analyze_final per-site source P_over = 1: CRC 5, IBD 3, T2D 4 | ok |
| 7 | 15 of 32 including adenoma | + adenoma 3 (FengQ LASSO, Yachida ×2) | ok |
| 8 | Batch correction: LASSO sites above 0.12, 50% → 25% | Table S7 / explore_v10 (0.500 → 0.250) | ok |
| 9 | "Random forest did not improve" | Table S7: RF 0.375 → 0.25; |dev| 0.102 → 0.048 | **mismatch** (N8) |
| 10 | Cirrhosis +1.30 (0.99–1.60), adjusted for age/BMI/sex | Table S3c 1.297 (0.993–1.601), age+BMI+male | ok |
| 11 | Cirrhosis test-positive 52% vs 8% | novelty log round 7; explore_v9 gives 0.431 vs 0.044 | **not in SI / inconsistent** (N12) |
| 12 | ACVD +0.87 (0.62–1.12) | Table S3c 0.871 (0.622–1.119) | ok |
| 13 | Hypertension +0.33 | Table S3c 0.333 (crude = adjusted) | ok (text no longer says adjusted; Fig. 1C legend does — N11) |
| 14 | Fatty liver, asthma, schizophrenia absent | Table S3c p = 0.38, 0.42, 0.15 | ok |
| 15 | Within-CRC: 4% vs 16% | Table S8 LASSO 0.0429 vs 0.1642 | ok (LASSO; RF 1.4% vs 16.4% not stated) |
| 16 | Within-CRC adjusted −0.19 (−0.60 to 0.21) | Table S8 −0.1943 (−0.6005, 0.2120) | ok |
| 17 | HF +0.33 (0.14–0.51) | Table S3b 0.3276 (0.1416–0.5137) | ok |
| 18 | T2D +0.36 (0.26–0.46) | Table S3b (locked) 0.3532 (0.2547–0.4517); Table S9 refit 0.3624 (0.2633–0.4616) | **minor mismatch** (quotes post hoc refit, N9) |
| 19 | Both Holm-adjusted p < 0.01 | LASSO HF 0.0026, T2D < 1e-4; RF HF 0.0174 | ok for LASSO only |
| 20 | CAD, prediabetes no increase | Table S3b | ok |
| 21 | Second T2D cohort significant only for RF; third none | Table S3b QinJ RF Holm 0.0002 / LASSO 0.24; Karlsson n.s. | ok |
| 22 | HF after country + drugs +0.28 (0.06–0.51) | Table S9 0.2843 (0.0639–0.5047) | **rounding** (0.50); selective (N3) |
| 23 | T2D after country + drugs +0.11 (−0.03 to 0.24) | Table S9 0.1057 (−0.0249, 0.2362) | **rounding** (−0.02) |
| 24 | Metformin within T2D 2.4×; 20.5% vs 8.5% | Table S6d 0.2054 / 0.0851 = 2.41 | ok |
| 25 | Metformin adjusted +0.44, p < 10⁻⁶ | metformin log 0.4433 (0.2804–0.6063); z ≈ 5.3, p ≈ 1e-7 | ok |
| 26 | Non-users at control rate (10.3%) | 0.085 vs Table S3 control 0.103 | ok |
| 27 | "A smaller cohort showed the same direction, two cohorts … did not" | LiJ_2014 LASSO + / RF positivity opposite; Karlsson β + | **inaccurate** (unchanged, M7) |
| 28 | Oral taxa 78–83% (cirrhosis, ACVD) | explore_v9 / novelty log: ACVD 78%, cirrhosis 83%; Fig. 1D | ok |
| 29 | AUROC 0.76 → 0.72 | explore_v9 None 0.763; K=2 0.721 (Table S4 lacks None row) | ok (table incomplete) |
| 30 | Locked HF/T2D/metformin oral ≤ 0.05 logit | Table S9b 0.050 / 0.023 / −0.034 | ok |
| 31 | "Enterobacterales dominated" | metformin log: Enterobacterales 0.037 vs Lachnoclostridium 0.097, *E. eligens* 0.091; no HF/T2D species output | **unsupported / overstated** (N13) |
| 32 | PPI oral +0.18 (0.14–0.21) | Table S6b 0.1751 (0.1443–0.2058) | ok |
| 33 | PPI total LASSO +0.04, p = 0.24 | Table S6b 0.0382, 0.2444 | ok |
| 34 | Source cut-off mean FPR 0.17; 49% of months above 0.12 | Table S2 primary 0.171 / 0.488 | ok |
| 35 | vp 0.085 and 0.6% | Table S2 0.085 / 0.006 | ok |
| 36 | Sensitivity within 0.015 of oracle (−0.021 to −0.009) | analyze_final H2 | ok (oracle runs at FPR 0.112) |
| 37 | vs source −0.46 (−0.66 to −0.20), p = 0.011 | analyze_final −0.462 (−0.658, −0.195), p 0.01146 | ok |
| 38 | vs local quantile p = 2.5 × 10⁻⁷ | 2.489e-07 | ok (32 correlated units) |
| 39 | vs prevalence-bounded p = 0.049 | 0.04896 | ok |
| 40 | ≥40 controls: 9 cohorts, FPR 0.090 vs 0.083, p = 0.72 | posthoc_drift_restrict: vp 0.09, contam 0.083; P_over p = 0.715 | ok (mixed metrics; omits vs-source p = 0.074 — N7) |
| 41 | Drift: recovers in 1–2 months; months 10–12 0.086 vs 0.154 | analyze_final drift-by-period: vp pooled 0.086; prevalence-bounded pooled 0.154 (local quantile 0.173) | ok |
| 42 | 10% prevalence: CRC sensitivity 0.44 vs 0.52 | analyze_final CRC π = 0.10: contam 0.444, vp 0.517 | ok |
| 43 | MetaCardis pooled overall 0.095; HF 0.21; T2D 0.14 | Part C LASSO 0.095; 0.212; 0.144 | ok |
| 44 | Per-group every group 0.08–0.09 | Part C LASSO 0.084–0.093 (RF HF 0.078) | ok for LASSO (HF P_over 15% unstated) |
| 45 | No resampling: "two largest locked sites" | script ran 4 site–classifier units (Yachida CRC/adenoma, MetaCardis, QinJ); QinJ contributes 0 months ≥3 | **mismatch** (N1) |
| 46 | vp mean FPR 0.094; 19% of months above 0.12 | P3 log: 0.092/0.096; 0.170/0.205 | ok |
| 47 | High-confidence 5%; mean FPR 0.071 | P3 log: 0.048/0.052; 0.070/0.072 (Table S10 simple mean 0.068) | ok vs log; Table S10 not reproducible (N1); δ = 0.10 unstated (N2) |
| 48 | Burn-in month ≈ 27% referred | RESULTS_locked "vp .27 vs .19" (pooled; CRC 0.33, T2D 0.35) | ok (pooled; P3 month-1 FPR is 0.36) |
| 49 | 83 fewer referrals / 1,000 | analyze_final CRC 1%: (185.27 + 188.88)/2 − (100.32 + 107.04)/2 = 83.4 | ok |
| 50 | +1.1 missed cancers / 1,000 | (4.54 + 4.80)/2 − (3.28 + 3.84)/2 = 1.11 | ok |
| 51 | Sensitivity 0.52 vs 0.64 | analyze_final CRC 1% vp 0.515, source 0.644 | ok |
| 52 | Downward drift: all rules too strict | Table S2c / posthoc_drift_restrict (vp 0.035, months 13–18) | ok |
| 53 | Fig. 2A: 11 sites, 1% prevalence; month-1 ≈ 0.29 | Fig. 2A; adenoma excluded | ok (fixed) |
| 54 | Fig. 2D bars 24/24/14/19/5%; FPR 0.080/0.101/0.089/0.094/0.071 | P3 log pooled by π | ok vs log; text omits the 14% (N1) |
| 55 | Fig. 2C values | Table S5 LASSO | ok |
| 56 | SI S7 numerical check, mean FPR 0.092 | round-1 re-run | ok (fixed) |
| 57 | Table S2b months 7–12 | analyze_final CRC vp 0.087/0.091/0.090 | ok (fixed) |
| 58 | GA summary ≤ 100 words | 96 words | ok |

**Summary.** Of 58 items, 47 are ok. There are 4 factual mismatches (#9, #31, #45, Table S10 vs text), 3 rounding or locked-vs-refit slips (#18, #22, #23), 2 inaccurate or unsupported descriptions (#11, #27), and several items that are correct but reported selectively (#19, #40, #44, #47, #54).

---

## 4. Recommendation

**Major revision (light).** The science is now presented far more honestly, and the key analyses exist. What blocks acceptance is reporting:

- an omitted unfavourable comparison in the new analysis;
- unlabelled post hoc content, plus a frozen file that changed after the freeze;
- a model-selective HF statement;
- several small mismatches.

None of this needs new data.

### Top remaining fixes (prioritised; all feasible with existing public data and code)

1. **Report P3 fully and redesign it modestly.**
   - State that the prevalence-bounded rule had fewer exceedances than standard vp (14% vs 19%).
   - Add a high-confidence (binomial order-statistic) version of the prevalence-bounded rule as a comparator.
   - Report δ = 0.10, P(FPR > 0.10) and vp_hc sensitivity.
   - Describe the units correctly: MetaCardis is a T2D classifier, Yachida contributes one month, and QinJ contributes nothing. Use B = 25 or "months ≥ 2" so that Yachida contributes.
   - Add a *batch-ordered* stream (MetaCardis ordered by recruitment country) as a real drift test.
2. **Label all post hoc material in the main text** (P1, P3, P4, D10, the high-confidence option).
   - Restore the frozen `calibrate.py`, or disclose the change and give both hashes.
   - Correct SI S4's "pre-specified" list to match protocol §8 (a)–(e).
   - Add one clause on pilot exposure of the three CRC sites to the main text.
3. **Rewrite the HF/T2D paragraph to match Table S9.**
   - Say the HF effect is attenuated and significant only for LASSO with country + drugs, and not in RF or complete-case models.
   - Add a Denmark-only HF contrast.
   - Quote the locked T2D estimate from Table S3b.
   - Add confounding by indication for metformin and correct the replication sentence.
4. **Complete the H1 reporting.**
   - Report per-disease results (only CRC is significant against source), the smoothed-setting reversal, and vp vs source p = 0.074 at ≥40 controls.
   - Add a mean |FPR − α| or matched-FPR comparison.
   - Give comparators a positivity-rate restart in the drift scenario, or retitle Fig. 2B.
5. **Fix the factual items:**
   - Table S7 RF sentence (N8);
   - Fig. 1C adjustment legend (N11);
   - cirrhosis 52/8 vs 43/4 (N12);
   - "Enterobacterales": add a species table for the locked HF/T2D/metformin gaps and a per-species oral list, and resolve the *S. salivarius* inconsistency (N13);
   - CI rounding (N15);
   - "Mild cardiometabolic labels … do not drive" → "were not associated with" (N6).
6. **Housekeeping:**
   - Table S1 PMIDs and cohort citations (including QinJ_2012); cite SI references;
   - cMD release list consistent between SI and DAS;
   - Table S3 999 CIs → Wilson/Katz or "not estimable"; HMP n footnote; IjazUZ_2017 absence explained; Table S4 None row;
   - HF per-group P_over 15% in the text; pin the scikit-learn version;
   - in the main text, restate A2 as a realised-count condition and add within-group assumptions for per-group control;
   - one sentence on FIT and on the hypothetical deployment setting (R4).
