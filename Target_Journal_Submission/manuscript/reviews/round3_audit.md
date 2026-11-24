# Round 3 statistical audit: submission_package/Manuscript.md (rev3)

Auditor role: pre-submission factual and statistical check. No other files were edited.
Sources recomputed: `final/analyze_final.log`, `final/results/sequential.csv.gz`, `posthoc_crc_audit.log` and `addendum_results/posthoc_crc_audit_sites.csv`, `posthoc_crc_deploy.log` and `.csv.gz`, `posthoc_stream_v2.log` and `.csv.gz`, `posthoc_drift_restrict.log`, `posthoc_metacardis_drugadjusted.log` and `.csv`, `posthoc_metacardis_decomposition.csv`, `posthoc_within_crc_comorbidity.log`, `posthoc_group_labelfree.log` (P7), `addendum_results_confirm.log`, `addendum_metformin_explore.log`, `metformin_within_T2D.csv`, `dev/explore_v7_comorb.log`, `dev/explore_v7b_fits.csv`, `dev/explore_v9_mechanism.log`, `dev/explore_v9_constrained.csv`, `dev/explore_v9b_axes.csv`, `dev/explore_v10_batchcorr.log`, `protocol.md`, `protocol_addendum_drugs.md`, `data_lock.md`, `novelty_escalation_log.md`, `make_figures.py`, Figure1.png and Figure2.png. Recomputations were done with pandas from the csv/csv.gz files.

Status codes: **OK** = matches the source; **MISMATCH** = a number or description differs from the source or the figure; **UNSUPPORTED** = no source in the SI or results, or the claim goes beyond the evidence; **LABEL** = wrong or missing pre-specified / post hoc / exploratory label.

---

## 0. Most important finding

**The submission file is stale.** `manuscript/manuscript.md`, the working copy, was corrected in commit fa27f13 (post hoc P7). That correction never reached `submission_package/Manuscript.md`, the file being submitted. The submission file still says "The verified-positive rule helped where label-free rules cannot … running the rule within recorded groups brought every group to 0.08–0.09". P7 (Table S11; `posthoc_group_labelfree.log`) shows that the label-free prevalence-bounded rule, run within groups, does the same:

| LASSO, months 7–18 | Label-free | Verified-positive |
|---|---|---|
| HF | 0.086 | 0.080 |
| T2D | 0.093 | 0.094 |
| Controls | 0.092 | 0.093 |

The sensitivity proxy is also equal between the two rules. The submitted text therefore credits per-group control to the verified-positive rule, which the authors' own data contradict, and Table S11 is never cited. The package (Manuscript.md, .docx, zip) must be regenerated from the corrected source; see correction 1.

---

## 1. Claim-by-claim table (main text, graphical abstract, figure legends, figures)

### 1a. Graphical abstract and introduction

| # | Claim | Source | Recomputed value | Status |
|---|---|---|---|---|
| 1 | GA "≤100 words" | GA paragraph | **105** whitespace-delimited words | **MISMATCH** (over the limit) |
| 2 | GA: 11 CRC sites, FPR 0%–37% | posthoc_crc_audit sites | min 0.000; max 0.367 (LASSO, GuptaA) | OK |
| 3 | GA: "far beyond sampling noise" | P5 χ² vs Binomial(n0, 0.10) | χ² = 102.1, df 11, p = 6.9e-17 | OK (but post hoc; see #13) |
| 4 | GA: cirrhosis/atherosclerosis over-flagged "through oral-origin marker taxa" | explore_v9b_axes | oral share 83% / 78% | OK (exploratory, development) |
| 5 | GA: diabetes cohort excess tracked metformin (exploratory) | Table S6d | +0.44, p = 1.4e-7 | OK |
| 6 | GA: label-free local reset restored specificity at stable sites | P6 / P3b | local rules mean FPR 0.08–0.10 | OK |
| 7 | GA: colonoscopy-only rule recovered from large drift | drift by period | vp month 8: 0.095 (all) / 0.089 (π = 1%) | OK |
| 8 | AUROC ≈ 0.8 [1, 2] | literature | n/a | OK (external) |
| 9 | "FIT … programmes already set positivity cut-offs locally [6]" | Selby 2019 is a meta-analysis of threshold effects on accuracy | n/a | **UNSUPPORTED** (citation does not show local cut-off setting; add a programme-level source or rephrase) |
| 10 | 32 public cohorts (Table S1) | Table S1 | 11 CRC + 4 IBD + 4 T2D + 11 comorbidity + 2 medication = 32 | OK |
| 11 | Pilot evaluated the source cut-off at all 11 CRC cohorts, including the 3 held-out sites | SI S1; data_lock.md; pilot log | yes | OK (disclosed) |
| 12 | "post hoc analyses are labelled as such" | see #13, #43, #66, #80 | several are not | **LABEL** |

### 1b. Section 1: cut-offs do not hold at new CRC sites

| # | Claim | Source | Recomputed value | Status |
|---|---|---|---|---|
| 13 | Audit at all 11 CRC cohorts (3 locked + 8 LOCO) | posthoc_crc_audit.py, docstring "POST HOC P5" | post hoc | **LABEL** (main text and Fig. 1B do not say post hoc) |
| 14 | Realised FPR 0.00–0.37 (Fig. 1B) | crc_audit_sites | LASSO 0–0.367; RF 0–0.361 | OK |
| 15 | FPR > 0.12 at 6 of 11 sites per classifier | crc_audit_sites | LASSO 6 (Gupta, Thomas18a, Vogtmann, Zeller, Yachida, Thomas19c); RF 6 (Thomas18a, Vogtmann, Zeller, Yachida, Yu, Thomas19c) | OK |
| 16 | Exact 95% CI excluded the 10% target at 4–5 sites | crc_audit_summary `n_ci_excludes_010` counts both directions | LASSO 5, all above; RF 4 = 3 above + FengQ RF (0/61, CI 0–0.059) **below** | **MISMATCH** (in context the reader assumes all lie above target; for RF it is 3) |
| 17 | χ² = 102 on 11 df, p < 10⁻¹⁵ | crc_audit_summary | 102.08 / 102.14, df = 11, p = 6.9e-17 | OK numerically. The test is against Binomial(n0, **0.10**), so it measures miscalibration (mean shift plus spread), not pure overdispersion. Expected counts are as low as 2.4. |
| 18 | Between-site SD of logit FPR 0.58–0.65 | crc_audit_summary tau | 0.5795 / 0.6485 | OK |
| 19 | "sensitivity rose and fell with the FPR" | crc_audit_sites | Spearman ρ(FPR, sens) = 0.69 (LASSO), 0.67 (RF) | OK |
| 20 | Other diseases: IBD and T2D sites FPR 0.00–0.75 (Table S2) | sequential.csv primary, source, per site | 0.000 (Karlsson RF) – 0.747 (QinJ RF) | Number OK; **UNSUPPORTED by cited table**: Table S2 gives only pooled means, no per-site FPR |
| 21 | Batch correction: development sites above 0.12, LASSO 50% → 25% | explore_v10 / Table S7 | 0.500 → 0.250 (site_z) | OK |
| 22 | RF 38% → 25% | Table S7 | 0.375 → 0.250 (site_z and site_rank) | OK (N8 fixed) |
| 23 | Batch correction "reduced but did not remove the spread"; labelled post hoc | Table S7 | RF site_z max FPR 0.393 > 0.361 | OK |

### 1c. Section 2: over-flagged patient groups

| # | Claim | Source | Recomputed value | Status |
|---|---|---|---|---|
| 24 | Cirrhosis +1.30 logit (0.99–1.60), adjusted age/BMI/sex | v7b_fits / Table S3c | 1.297 (0.993–1.601), age+BMI+male | OK |
| 25 | Cirrhosis test-positive 52% vs 8% | dev/explore_v7_comorb.log LASSO 0.525 vs 0.079 | Not in any SI table. explore_v9 frozen-model "None" row gives 0.431 vs 0.044 | **UNSUPPORTED** in SI; inconsistent with v9 (N12 unresolved) |
| 26 | ACVD +0.87 (0.62–1.12) | Table S3c | 0.871 (0.622–1.119) | OK |
| 27 | Hypertension small (+0.33) | Table S3c | 0.333 (0.068–0.598), **unadjusted** (covs nan) | OK in text (text does not claim adjustment) |
| 28 | Absent for fatty liver, asthma, schizophrenia | Table S3c | p = 0.38, 0.42, 0.15 | OK |
| 29 | (Omission) ME/CFS | Table S3c; Fig. 1C plots it | +0.39 (0.12–0.67), p = 0.006 (BMI+sex) | **MISMATCH** text vs Fig. 1C: ME/CFS is shown and is larger than hypertension, but the text omits it |
| 30 | Within-CRC (post hoc): comorbid controls 4% vs 16% | Table S8 LASSO | 0.0429 vs 0.1642 | OK (labelled post hoc) |
| 31 | Adjusted score difference −0.19 (−0.60 to 0.21) | Table S8 | −0.194 (−0.600, 0.212) | OK |
| 32 | "were not associated with more false positives" | Table S8 | RF positivity 1.4% vs 16.4%, OR 0.10 (0.01–0.93), p = 0.04: *fewer* | OK (N6 wording fixed); the inverse association is still unreported |
| 33 | MetaCardis pre-specified, sex-adjusted: HF +0.33 (0.14–0.51) | Table S3b LASSO | 0.3276 (0.1416–0.5137) | OK |
| 34 | T2D +0.35 (0.25–0.45) | Table S3b LASSO | 0.3532 (0.2547–0.4517) | OK (N9 fixed) |
| 35 | "both Holm-adjusted p < 0.01" | Table S3b | LASSO HF 0.0026, T2D < 1e-4; RF HF **0.0174** | OK for LASSO only; the model is not named |
| 36 | CAD and prediabetes no increase | Table S3b | p_holm 1.0 / 0.94 | OK (pre-specified) |
| 37 | Second T2D cohort significant only for RF; third none (Table S3) | Table S3b | QinJ RF p_holm 0.0002, LASSO 0.24; Karlsson n.s. | OK |
| 38 | Country and medication added (post hoc) | Table S9 | yes | OK |
| 39 | HF LASSO +0.28 (0.06–0.50) | Table S9 | 0.2843 (0.0639–0.5047) | OK (N15 fixed) |
| 40 | HF RF +0.13, p = 0.11 | Table S9 | 0.1282, p = 0.1127 | OK |
| 41 | HF not significant in complete case (n = 1,310) | Table S9 | LASSO 0.28 (−0.12, 0.68), p = 0.16; RF p = 0.11 | OK (N3 fixed) |
| 42 | T2D +0.11 (−0.02 to 0.24) | Table S9 | 0.1057 (−0.0249, 0.2362) | OK |
| 43 | (Omission) fully adjusted prediabetes | Table S9; Fig. 1C | LASSO +0.12 (0.003–0.245), p = 0.044: Fig. 1C CI excludes 0 | **MISMATCH** text vs Fig. 1C (text says prediabetes showed no increase; the plotted fully adjusted estimate is nominally positive) |
| 44 | Metformin users 2.4× (20.5% vs 8.5%) | Table S6d | 0.2054 / 0.0851 = 2.41 | OK |
| 45 | Adjusted +0.44, p < 10⁻⁶ | Table S6d | 0.4433 (0.280–0.606), p = 1.38e-7 | OK |
| 46 | Non-users flagged at a rate similar to controls (10.3%) | Table S3 LASSO controls | 8.5% vs 10.3% | OK |
| 47 | "A smaller cohort showed the same direction, but two cohorts with few users did not" | Table S6d | LiJ_2014: β +0.40 (p = 0.18) / RF +0.28 (p = 0.12), but RF positivity goes the other way (15.5% vs 23.8%). QinJ (15 users): β ≈ 0 / −0.12. Karlsson (20 users): β +0.04 / +0.05 | Partly OK. "Same direction" holds for β, not for RF positivity. Confounding by indication is not mentioned (R5/M7 unresolved) |
| 48 | Metformin finding labelled exploratory | protocol_addendum: metformin secondary; within-T2D analysis post hoc | — | OK |
| 49 | Decomposition exploratory (Methods S5) | SI S5 | — | OK |
| 50 | Oral taxa 78–83% of gap in cirrhosis and ACVD | explore_v9b share of gap | ACVD 0.78, cirrhosis 0.83 | OK |
| 51 | Named oral markers are in the model | v9b oral list | S. oralis, F. nucleatum, V. parvula, G. morbillorum present | OK |
| 52 | AUROC 0.76 → 0.72 (Table S4) | explore_v9_constrained | None 0.763; K = 2 mean 0.721 | Number OK; **Table S4 still has no "None" row** although its caption defines None (N16 unresolved) |
| 53 | Excess not removed before AUROC loss | v9_constrained K = 2 QinN ratio 6.7 | — | OK |
| 54 | Locked HF, T2D, metformin oral ≤ 0.05 logit | Table S9b | 0.0498 / 0.0225 / −0.0344 | OK |
| 55 | Depletion and other enriched taxa dominated (Table S9b) | Table S9b | HF: dep 0.080 + other 0.195; T2D 0.191 + 0.157; metformin 0.318 + 0.180 | OK |
| 56 | PPI raised oral component +0.18 (0.14–0.21), pre-specified H6 | Table S6b | 0.1751 (0.1443–0.2058) | OK |
| 57 | PPI total LASSO score +0.04, p = 0.24; H5 not supported | Table S6b | 0.0382, p = 0.2444 | OK. Not reported: the pre-specified secondary RF model was significant (+0.09, 0.01–0.16, p = 0.014) |

### 1d. Section 3: local recalibration

| # | Claim | Source | Recomputed value | Status |
|---|---|---|---|---|
| 58 | 12-month deployments, four rules, monthly updates, liberal first month, restart rule | protocol §4–5; SI S3 | — | OK |
| 59 | Proposition S1: "if controls … exchangeable and prevalence stays below the bound, expected FPR ≤ target" | SI S7 (A1–A3) | A2 is a condition on the *realised* case count; A3 (no false-positive verification) is omitted | Minor **MISMATCH** with SI (M5 unresolved) |
| 60 | 11 CRC sites, 1% prevalence, labelled post hoc | posthoc_crc_deploy (P6) | — | OK |
| 61 | Source mean FPR 0.14; 55% of months above 0.12 | P6 log, all sites | 0.142 / 0.545 | OK |
| 62 | Local quantile 0.11 (21%) | P6 | 0.108 / 0.205 | OK |
| 63 | Prevalence-bounded 0.10 (13%) | P6 | 0.103 / 0.130 | OK |
| 64 | Verified-positive 0.083 (0.3%) | P6 | 0.083 / 0.003 | OK |
| 65 | Sensitivity 0.50 vs oracle 0.52 | P6 | 0.495 vs 0.517 | OK |
| 66 | (Omission) 8 of the 11 sites are development cohorts on which the vp rule was designed | posthoc_crc_deploy.py docstring: "optimistic for the verified-positive rule … reported separately" | locked-only: source 0.189/0.833, contam 0.099/0.071, vp 0.087/0.004 | **LABEL**/caveat missing from text and Fig. 2A legend |
| 67 | Pre-specified, 16 sites: vp − source −0.46 (−0.66 to −0.20), p = 0.011 | analyze_final H1 | −0.462 (−0.658, −0.195), p = 0.01146 | OK |
| 68 | Significant for CRC, not for IBD, T2D or adenoma | analyze_final | CRC p = 0.031; IBD 0.31; T2D 0.094; adenoma 0.48 | OK |
| 69 | vs local quantile p = 2.5 × 10⁻⁷ | analyze_final | 2.489e-7 | OK |
| 70 | Sensitivity within 0.015 of oracle | H2 | −0.015 (−0.021, −0.009) | OK (point estimate; the CI reaches 0.021) |
| 71 | vs prevalence-bounded p = 0.049 | analyze_final | 0.04896 | OK |
| 72 | ≥40 controls (post hoc): 9 cohorts, "equivalent (FPR 0.090 vs 0.083; p = 0.72)" | P4 log | vp 0.090, contam 0.083; p = 0.715 is for the **exceedance** endpoint | **UNSUPPORTED** ("equivalent" claimed from a non-significant test; no equivalence test). Mixed metrics (N7) |
| 73 | vs source p = 0.074 at ≥40 controls | P4 log | 0.0742 | OK |
| 74 | Source too strict at some large sites | Table S2d | source P_over 0 at Karlsson, MetaCardis, Nielsen, Zeller | OK |
| 75 | No resampling (post hoc): "three large held-out sites" | posthoc_stream_v2.csv tags | 3 cohorts but **4 site–classifier units**: Yachida CRC, **Yachida adenoma**, MetaCardis T2D, QinJ T2D. MetaCardis supplies 53% of rows and 24 of 37 months | **MISMATCH** (adenoma test omitted; Fig. 2D legend and Table S10 merge the two Yachida tests) |
| 76 | FPR measured on controls not yet seen | stream_v2.py | random order: yes. Country order: falls back to *all* current-country controls, including seen ones, when fewer than 20 remain | Minor **MISMATCH** for the country analysis |
| 77 | Random order: prevalence-bounded 15%, vp 18% of months above 0.12 | stream_v2 recomputed (months ≥ 3, pooled) | 0.147 / 0.183 | OK |
| 78 | All local rules kept mean FPR near target | stream_v2 | local_q 0.102, contam 0.087, vp 0.092 | OK |
| 79 | High-confidence: 3–5% random order, 12–17% country shift | stream_v2 | contam_hc 0.032, vp_hc 0.045; country 0.121 / 0.167 | OK |
| 80 | High-confidence mean FPRs 0.06–0.07 | stream_v2 | 0.061, 0.065, 0.068, 0.073 | OK; labelled "added after the locked analysis" (OK). Sensitivity cost and P(FPR > 0.10) vs δ still unreported (N2) |
| 81 | (Omission) under the country shift, standard rules exceed 0.12 in 27% (contam), 27% (vp), 34% (local_q) of months; the source cut-off in 1.4% | Table S10 | — | Selective: the text gives only the high-confidence numbers for the country shift |
| 82 | Drift +0.5 logit described as "pre-specified" | run_final.py SETTINGS (hash frozen at 7be2b56); **not** in protocol §8 (a)–(e) | — | OK in substance; wording should say "specified in the frozen analysis code" (M6) |
| 83 | Alarm restored FPR within two months | sequential drift | vp month 8: 0.095 (all) / 0.089 (π = 1%) | OK (actually within one month) |
| 84 | "label-free rules stayed high (months 10–12: 0.086 vs 0.154; Figure 2B)" | sequential drift: 0.086/0.154 are **all 16 sites × all π** and the prevalence-bounded rule only. Fig. 2B plots CRC/IBD/T2D at π = 1%: vp **0.082**, contam **0.174**, local_q **0.183** | — | **MISMATCH** with the cited figure (N10 unresolved). "Rules" (plural) is quoted with one rule's value |
| 85 | Fig. 2B title "only the drift alarm recovers" | figure | comparators have no restart by design; contam falls to 0.145 by months 13–18 | **UNSUPPORTED** overstatement (N10) |
| 86 | 10% prevalence: CRC sensitivity 0.44 vs 0.52 | analyze_final CRC π = 0.10 | contam 0.444, vp 0.517 (**locked** CRC sites) | OK; should say "locked CRC sites" |
| 87 | MetaCardis pooled overall FPR 0.095 | RESULTS_locked Part C | 0.095 | OK |
| 88 | HF 0.21, T2D 0.14 under pooled recalibration | Table S5 LASSO | 0.212 / 0.144 | OK |
| 89 | Per-group every group 0.08–0.09 | Table S5 LASSO | 0.084–0.093 (RF HF 0.078) | OK (LASSO). HF still exceeds 0.12 in 15% of months; not stated (N16) |
| 90 | Placed under "verified-positive helped where label-free rules cannot" | P7 / Table S11 | label-free per-group: HF 0.086, T2D 0.093 | **MISMATCH** (see Section 0; stale file) |
| 91 | Comorbid CRC patients did not score higher (Table S8) | Table S8 | +0.10 (−0.63, 0.83) LASSO | OK |
| 92 | Per-group recalibration lowers sensitivity in over-flagged groups | Table S5 | HF 0.36 vs 0.45; T2D 0.39 vs 0.45 | OK |
| 93 | Liberal first month: about 27% referred | analyze_final burn-in | 0.27 is pooled over **all diseases** (16 sites). CRC locked: **0.328**; 11 CRC sites (P6): **0.254** | Imprecise in this CRC-focused paragraph; should give the CRC figure |
| 94 | 83 fewer FP referrals per 1,000 at locked CRC sites | harms table | (185.27 + 188.88)/2 − (100.32 + 107.04)/2 = 83.4 | OK |
| 95 | +1.1 missed cancers per 1,000 | harms table | (4.54 + 4.80)/2 − (3.28 + 3.84)/2 = 1.11 | OK |
| 96 | Sensitivity 0.52 vs 0.64 | analyze_final CRC π = 0.01 | 0.515 vs 0.644 | OK |
| 97 | Downward drift: all rules too strict (post hoc; Table S2c) | P4 | vp 0.035, contam 0.040, local_q 0.043 at months 13–18 | OK |

### 1e. Conclusion

| # | Claim | Source | Recomputed value | Status |
|---|---|---|---|---|
| 98 | Metformin "one cohort" | Table S6d | only MetaCardis significant | OK |
| 99 | Label-free prevalence-bounded rule "in its high-confidence form" suffices at stable sites | P3b | contam_hc 3% / 12% | OK, but the high-confidence form is post hoc and not labelled here |
| 100 | vp adds recovery from upward drift and robustness to higher prevalence | drift; π = 0.10 | — | OK |
| 101 | Limitations list (simulation, pilot, perfect reference, downward drift, one cohort) | — | — | OK |
| 102 | Both rules and a site audit released in cutoffguard | commit 93c0538 (label-free rule added to core.py) | — | OK |

### 1f. Figure 1

| # | Claim | Source | Recomputed value | Status |
|---|---|---|---|---|
| 103 | Fig. 1A: development has 8 CRC + 11 other-condition + 2 medication cohorts; locked has 3 CRC + 13 other | SI S1; Table S1 | 3 + 4 + 4 + 5 = 16 locked | OK |
| 104 | 1B: exact 95% CI; grey = development LOCO, black = locked; circles LASSO, squares RF; n = controls | make_figures.py; crc_audit_sites | — | OK. No post hoc label (P5) |
| 105 | 1B: "IBD, T2D and adenoma sites are shown in Table S2" | Table S2 | pooled means only; no per-site rows | **UNSUPPORTED** |
| 106 | 1C: development estimates (open) "for age, BMI and sex" | v7b_fits covs | cirrhosis, ACVD, schizophrenia: age+BMI+sex. **Hypertension and fatty liver: unadjusted. ME/CFS: BMI+sex. Asthma: age+BMI** | **MISMATCH** (N11, unchanged for three rounds) |
| 107 | 1C: MetaCardis filled, sex + country + PPI/metformin/statin/aspirin/beta-blocker, post hoc | posthoc_metacardis_drugadjusted.py line 34 | matches | OK |
| 108 | 1C: within-CRC diamond, site FE + age, BMI, sex | Table S8 | −0.19 (−0.60, 0.21) | OK |
| 109 | 1C panel title "fully adjusted" | as #106 | 2 of 7 development estimates are crude | **MISMATCH** |
| 110 | 1D: oral-origin taxa "(a priori genus list, Methods S5)" | explore_v9b_axes.py: list written in development round 9b, after round 9 had ranked the top contributing species | — | **LABEL**: "a priori" holds for the locked decomposition, not for the development percentages |
| 111 | 1D in-figure legend "Other taxa (e.g. Enterobacterales)" | metformin top species: Enterobacterales 0.037 (5th); no species output for HF or T2D | — | **UNSUPPORTED** (N13) |
| 112 | 1D values | v9b_axes; Table S9b | cirrhosis 1.018 / 0.131 / 0.080; HF 0.050 / 0.080 / 0.195; metformin −0.034 / 0.318 / 0.180 | OK |
| 113 | 1D locked decomposition | Table S9 caption "post hoc P2" | legend says only "exploratory" | Minor **LABEL** |

### 1g. Figure 2

| # | Claim | Source | Recomputed value | Status |
|---|---|---|---|---|
| 114 | 2A: 11 CRC sites, 1%, two classifiers, 100 streams each, post hoc; band P10–P90 for vp | posthoc_crc_deploy.py (R = 100); make_figures.py | 100 reps per site × model | OK. The development/locked optimism caveat is missing (#66) |
| 115 | 2B: "Locked CRC, IBD and T2D sites … +0.5 logit from month 7 (pre-specified)" | make_figures: drift, π == 0.01 | 11 sites, π = 1% (not stated) | OK, but the text numbers come from a different population (#84) |
| 116 | 2C: FPR by condition, months 7–18, LASSO; source / pooled / per-group | partC_groupcal; Table S5 | control 0.103 / 0.083 / 0.093; HF 0.232 / 0.212 / 0.084 | OK. Table S5 not cited |
| 117 | 2D: random order at Yachida [CRC test], MetaCardis and QinJ [T2D test] | stream_v2 tags | Also includes **Yachida adenoma test** (38,400 rows) | **MISMATCH** |
| 118 | 2D: 25 per month, 1% and 5%, 200 orders; country by country at 5%, all six orders; δ = 0.10; months ≥ 3 | stream_v2.py | B = 25; 200 permutations; 6 orders × 50 reps × 2 models | OK (50 reps per order and both classifiers are not stated) |
| 119 | 2D bar heights | stream_v2 recomputed | random: source .358, local_q .261, contam .147, contam_hc .032, vp .183, vp_hc .045; country: .014 / .344 / .268 / .121 / .265 / .167 | OK |
| 120 | 2D in-figure legend "3 large sites" | as #117 | 4 site–classifier units | **MISMATCH** |

### 1h. SI consistency affecting main-text claims

| # | Item | Status |
|---|---|---|
| S-a | SI S7b still describes the **old** P3: 50 per month, 300 random orders. Main text, Fig. 2D and Table S10 use P3b: 25 per month, 200 orders, plus the country-ordered stream | **MISMATCH** |
| S-b | P5 (CRC audit), P6 (CRC deployment), P3b and P7 are not described in SI S7b. The P5 per-site results (χ², τ, CIs) and P6 results have **no SI table**, although the GA, Section 1, Fig. 1B and Fig. 2A rest on them | **UNSUPPORTED** in SI |
| S-c | SI S4 calls smoothing, 70% attendance, 5% missed cancers, drift and combined "pre-specified". Protocol §8 lists only (a)–(e); the others exist only in the frozen run_final.py | **LABEL** (M6) |
| S-d | Smoothed populations: vp exceedance 0.026 vs prevalence-bounded 0.004 (Table S2), the reverse of H1; not mentioned in the main text | Selective (M3 unresolved) |
| S-e | Table S3: "999.00" upper CIs; HMP_2019_ibdmdb 103/27 in Table S1 vs 57/14 in Table S3; IjazUZ_2017 absent from Table S3 | Unresolved (N16) |
| S-f | DAS lists release 2022-04-13; SI S1 lists only 2021-03-31 and 2022-10-19. SI S1 ends "listed by PMID in Table S1", but Table S1 has no PMID column. SI references S2–S6 are not cited in the SI text. scikit-learn version is not pinned (S8), although l1_ratio = 1 needs ≥ 1.8 | Unresolved (N14, N16) |
| S-g | S7c discloses the calibrate.py change but gives no new SHA-256 | Minor (N5 partly fixed) |
| S-h | Table S10 rows "YachidaS_2019" pool the CRC and adenoma classifiers | **MISMATCH** |

**Tally (120 main-text, legend and figure items).** 86 OK. 20 MISMATCH. 7 UNSUPPORTED. 7 LABEL. Several further items are OK but selectively reported (#35, #57, #80, #81, #89, S-d).

### Round-2 factual errors: status

| Round 2 | Status in rev3 |
|---|---|
| N1 no-resampling selective reporting / design | Mostly fixed: P3b, contam_hc comparator, country order, 15% vs 18% reported. **Open:** unit description (Yachida adenoma), SI S7b, hc sensitivity, P(FPR > α) vs δ |
| N2 δ, metric, post hoc | δ fixed; post hoc fixed; metric and sensitivity cost **open** |
| N3 HF selective | **Fixed**. IGT nominal p = 0.044 still unmentioned (#43); Denmark-only analysis not added |
| N4 post hoc labelling | Mostly fixed; **P5 (CRC audit) unlabelled** (#13) |
| N5 frozen code changed | Disclosed (S7c); new hash not given |
| N6 "do not drive" | **Fixed** wording; inverse association not reported |
| N7 ≥40 controls | p = 0.074 and post hoc now reported; mixed metrics remain, and a new "equivalent" overclaim (#72) |
| N8 Table S7 RF | **Fixed** |
| N9 locked T2D, LASSO-only Holm | T2D fixed; model still unnamed (#35) |
| N10 drift comparators / 0.154 | **Not fixed** (#84, #85) |
| N11 Fig. 1C adjustment legend | **Not fixed** (#106, #109) |
| N12 cirrhosis 52/8 | **Not fixed** (#25) |
| N13 Enterobacterales / species table | Text fixed; in-figure legend **not fixed** (#111); no HF/T2D species table |
| N14 citations / releases / PMIDs | **Not fixed** (S-f) |
| N15 CI rounding | **Fixed** |
| N16 Table S3 999, HMP n, Table S4 None row, HF P_over, sklearn version | **Not fixed** (S-e, #52, #89, S-f) |

---

## 2. Required corrections (with exact replacement text)

**1. Regenerate the submission package from the corrected source (critical).** In `submission_package/Manuscript.md`, paragraph "The verified-positive rule helped…", replace

> The verified-positive rule helped where label-free rules cannot.

with

> The verified-positive rule helped mainly where label-free rules cannot.

and replace

> running the rule within recorded groups brought every group to 0.08–0.09 (Figure 2C).

with

> running a local rule within recorded groups brought every group to 0.08–0.09 (Figure 2C; LASSO; heart failure still exceeded 0.12 in 15% of months), and the label-free rule did so as well as the verified-positive rule (post hoc; Table S11).

Then rebuild Manuscript.docx and iMeta_submission_package.zip from this text.

**2. Graphical abstract: cut to ≤100 words (currently 105).** Replace the last two sentences

> Resetting the cut-off locally from unlabelled scores restored specificity at stable sites. A rule that uses only colonoscopy results of test-positive people also recovered from large score drift. Both are released as cutoffguard.

with

> Resetting the cut-off locally from unlabelled scores restored specificity at stable sites; a rule using colonoscopy results of test-positives also recovered from drift. Both are in cutoffguard.

This brings the GA to 98 words (checked with `wc -w`).

**3. Label the CRC audit as post hoc.** Section 1, replace

> We audited this cut-off at all 11 CRC cohorts:

with

> In a post hoc audit, we evaluated this cut-off at all 11 CRC cohorts:

In the Fig. 1B legend, after "(exact 95% CI)", insert "; post hoc".

**4. Direction of the CIs that exclude the target.** Replace

> and the exact 95% confidence interval excluded the 10% target at four to five sites

with

> and the exact 95% confidence interval lay entirely above the 10% target at five (LASSO) and three (random forest) sites (and entirely below it at one further random-forest site)

**5. Name the test correctly.** Replace

> (overdispersion χ² = 102 on 11 df, p < 10^−15^; between-site SD of the logit FPR 0.58–0.65)

with

> (χ² test against Binomial(n, 0.10) = 102 on 11 df, p < 10^−15^; between-site SD of the logit FPR 0.58–0.65)

**6. Cite a table that actually has per-site FPRs.** Replace

> (IBD and T2D sites: FPR 0.00–0.75; Table S2)

with

> (IBD and T2D sites: FPR 0.00–0.75; Table S12)

Add a new SI **Table S12** giving per-site source-cut-off FPR, exact CI, n controls and sensitivity for all 11 CRC sites (from posthoc_crc_audit_sites.csv) and all 13 non-CRC held-out sites (sequential.csv.gz, primary, source), plus the P5 summary row (χ², df, p, τ, I²). In the Fig. 1B legend, replace "IBD, T2D and adenoma sites are shown in Table S2." with "Per-site values for all sites, including IBD, T2D and adenoma, are given in Table S12."

**7. Mention ME/CFS (text vs Fig. 1C).** Replace

> Effects were small for hypertension (+0.33) and absent for fatty liver, asthma and schizophrenia.

with

> Effects were smaller for ME/CFS (+0.39, 0.12–0.67) and hypertension (+0.33, unadjusted), and absent for fatty liver, asthma and schizophrenia.

**8. Cirrhosis positivity.** Either add a positivity column (LASSO: 52.5% vs 7.9%, explore_v7) to Table S3c and state which model produced it, or replace

> (+1.30 logit after adjustment for age, BMI and sex; 95% CI 0.99–1.60; test-positive 52% vs 8%)

with

> (+1.30 logit after adjustment for age, BMI and sex; 95% CI 0.99–1.60)

Also reconcile with the explore_v9 frozen-model value (43% vs 4.4%) in the SI.

**9. Name the model for the Holm p-values.** Replace

> (+0.35, 0.25–0.45; both Holm-adjusted p < 0.01)

with

> (+0.35, 0.25–0.45; LASSO, both Holm-adjusted p < 0.01; random forest p = 0.017 and < 10^−4^)

**10. Prediabetes after full adjustment (text vs Fig. 1C).** After "The T2D effect largely disappeared (+0.11, −0.02 to 0.24)." insert

> Prediabetes became nominally positive (LASSO +0.12, 0.00–0.25, p = 0.044; random forest p = 0.24).

**11. Metformin replication and confounding.** Replace

> A smaller cohort showed the same direction, but two cohorts with few users did not (Table S6), so this finding is exploratory.

with

> In a smaller cohort the score difference had the same sign but was not significant (LASSO +0.40, p = 0.18; random forest +0.28, p = 0.12), and two cohorts with 15 and 20 users showed no difference (Table S6d). Because metformin use also marks treated, longer-standing diabetes, confounding by indication cannot be excluded, and this finding is exploratory.

**12. Report the secondary PPI model.** Replace

> Their effect on the total LASSO score was not significant (+0.04, p = 0.24), so that primary hypothesis was not supported.

with

> Their effect on the total LASSO score was not significant (+0.04, p = 0.24), so that primary hypothesis was not supported; the secondary random-forest model showed a small increase (+0.09, 0.01–0.16, p = 0.014).

**13. Proposition wording (match SI A2/A3).** Replace

> If controls at a site are exchangeable and prevalence stays below the bound, the expected FPR is at most the target, whatever the referral, attendance or delay (Proposition S1).

with

> If controls at a site are exchangeable, the number of cases in the window does not exceed the prevalence bound and colonoscopy never labels a control as a case, the expected FPR is at most the target, whatever the referral, attendance or delay (Proposition S1).

**14. Development-site optimism in the 11-site simulation.** After "…against 0.52 for an oracle cut-off set on each site's true controls." insert

> Eight of these sites are development cohorts on which the rule was designed; at the three locked sites alone the values were 0.19 (83% of months above 0.12) for the source cut-off, 0.099 (7%) for the prevalence-bounded quantile and 0.087 (0.4%) for verified-positive recalibration.

In the Fig. 2A legend, after "post hoc", add "; development sites are optimistic for verified-positive recalibration".

**15. Remove the "equivalent" overclaim and the mixed metrics.** Replace

> at the nine cohorts with at least 40 controls (post hoc), the two rules were equivalent (FPR 0.090 vs 0.083; p = 0.72)

with

> at the nine cohorts with at least 40 controls (post hoc), the two rules did not differ detectably (mean FPR 0.090 for verified-positive vs 0.083 for prevalence-bounded; months above 0.12, p = 0.72)

**16. No-resampling units.** Replace

> at three large held-out sites, each sample entered once in random order

with

> at the three held-out cohorts with at least 100 controls (four site–classifier pairs: Yachida 2019 with the CRC and adenoma tests, MetaCardis and Qin 2012 with the T2D test), each sample entered once in random order

In the Fig. 2D legend, replace "random order at Yachida 2019 [CRC test], MetaCardis and Qin 2012 [T2D test]" with "random order at Yachida 2019 [CRC and adenoma tests], MetaCardis and Qin 2012 [T2D test]". In make_figures.py, change the label "Random order, 3 large sites" to "Random order, 3 cohorts / 4 tests". In Table S10, split the YachidaS_2019 rows by classifier.

**17. Country-shift results for the standard rules.** Replace

> reduced this to 3–5% in random order and 12–17% under the country shift

with

> reduced this to 3–5% in random order and, under the country shift (where the standard rules exceeded 0.12 in 27% of months and the conservative source cut-off in 1%), to 12–17%

**18. Drift numbers must match Fig. 2B.** Replace

> its alarm restored the FPR within two months, while the label-free rules stayed high (months 10–12: 0.086 vs 0.154; Figure 2B)

with

> its alarm restored the FPR within one to two months, while the label-free rules, which have no restart, stayed high (months 10–12 at 1% prevalence: 0.082 vs 0.174 for the prevalence-bounded and 0.183 for the local quantile; Figure 2B)

Replace "pre-specified upward drift" with "upward drift specified in the frozen analysis code". In make_figures.py, change the Fig. 2B title "Upward drift: only the drift alarm recovers" to "Upward drift: the drift alarm recovers fastest". In the Fig. 2B legend, after "(pre-specified)", add "; 1% prevalence; comparators have no restart".

**19. Specify the 10% prevalence population.** Replace

> (CRC sites: sensitivity 0.44 vs 0.52)

with

> (locked CRC sites: sensitivity 0.44 vs 0.52, FPR 0.057 vs 0.090)

**20. Burn-in referral rate for CRC.** Replace

> in which about 27% of people are referred

with

> in which about a third of people are referred at the locked CRC sites (33%; 27% across all held-out sites)

**21. Fig. 1C adjustment legend and title (third round).** In the legend, replace

> development cohorts (open) for age, BMI and sex;

with

> development cohorts (open) for age, BMI and sex where recorded (hypertension and fatty liver unadjusted; ME/CFS BMI and sex; asthma age and BMI; Table S3c);

In make_figures.py, change the panel title "Which patients are over-flagged (fully adjusted)" to "Which patients are over-flagged (adjusted where recorded)".

**22. Fig. 1D labels.** In the legend, replace

> (a priori genus list, Methods S5)

with

> (genus list fixed in development, before the locked decomposition; Methods S5)

and add "post hoc" after "locked MetaCardis". In make_figures.py, change "Other taxa (e.g. Enterobacterales)" to "Other enriched taxa". Add a per-species table (top 15 contributors) for the locked HF, T2D and metformin gaps to the SI (Table S9c).

**23. Label the high-confidence option in the Conclusion.** Replace

> in its high-confidence form, suffices

with

> in its high-confidence form (added post hoc), suffices

**24. Cite the SI tables behind Fig. 2C and 2D.** Append "(Table S5)" to the Fig. 2C legend sentence and "(Table S10)" to the Fig. 2D legend.

**25. Fix SI Methods S7b.** Replace the P3 sentence with

> P3b: evaluation without resampling at held-out cohorts with ≥ 100 controls (Yachida 2019 CRC and adenoma tests; MetaCardis and Qin 2012 T2D test): controls streamed once in random order (25 per month, 200 random orders), cases inserted at prevalence 1% or 5%, FPR measured on controls not yet seen; and MetaCardis controls streamed country by country (T2D test, 5% prevalence, all six orders × 50, both classifiers), FPR on not-yet-seen controls of the current country (all current-country controls when fewer than 20 remained) (Table S10).

Add:

> P5: CRC-specific audit of the source cut-off at all 11 CRC cohorts (exact CIs, χ² vs Binomial(n, 0.10), DerSimonian–Laird τ; Table S12). P6: CRC-only deployment simulation at the 11 CRC sites (1% prevalence, 100 streams; Table S13). P7: per-group label-free recalibration at MetaCardis (Table S11).

Add Table S13 (from posthoc_crc_deploy.log, development and locked rows separately).

**26. SI S4 "pre-specified" list (M6).** Replace

> Pre-specified sensitivity analyses: alpha in {0.05, 0.20}; misspecified pi_max; one-month follow-up delay; B in {50, 200}; liberal burn-in at 1 - 3 alpha; kernel-smoothed site populations; 70% colonoscopy attendance; 5% of cancers missed at colonoscopy; a +0.5 logit shift of all scores from month 7; all combined.

with

> Pre-specified sensitivity analyses (protocol §8): alpha in {0.05, 0.20}; misspecified pi_max; one-month follow-up delay; B in {50, 200}; liberal burn-in at 1 - 3 alpha. Further settings fixed in the frozen analysis code before the locked run but not listed in the protocol text: kernel-smoothed site populations; 70% colonoscopy attendance; 5% of cancers missed at colonoscopy; a +0.5 logit shift of all scores from month 7; all combined.

**27. Report the smoothed-population reversal (M3).** After "…because the source cut-off was too strict at some large sites." insert

> With kernel-smoothed site populations, the prevalence-bounded quantile exceeded 0.12 less often than the verified-positive rule (0.4% vs 2.6% of months; Table S2).

**28. Housekeeping (carried over from round 2):**
- Table S4: add the None row (AUROC 0.763; disease and control positivity per held-out condition).
- Table S3: replace the "999.00" bounds with "not estimable".
- Footnote the HMP_2019_ibdmdb counts (103/27 vs 57/14) and the absence of IjazUZ_2017.
- SI S1: add release 2022-04-13, or remove it from the DAS.
- Either add the PMID column to Table S1 or delete "listed by PMID in Table S1".
- Cite SI references S2–S6 in the SI text, or remove them.
- Pin the scikit-learn version (≥ 1.8) in S8.
- Give the post-change SHA-256 of src/calibrate.py in S7c.
- Replace or supplement ref. 6 for the claim that FIT programmes set cut-offs locally.
