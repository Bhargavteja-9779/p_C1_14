# iMeta — Reviewer report (Round 1)

**Manuscript:** "Gut microbiome cancer tests over-flag people with chronic disease, and routine colonoscopy outcomes can keep their false alarms on target" (Letter)
**Reviewer expertise:** gut microbiome machine learning; biostatistics / diagnostic accuracy
**Materials examined:** Manuscript.md; SI_methods.md; SI_tables.md; RESULTS_locked.md; analyze_final.log; addendum_results_confirm.log, addendum_results_dev.log, addendum_metformin_explore.log; novelty_escalation_log.md; protocol.md, protocol_addendum_drugs.md, data_lock.md; posthoc_within_crc_comorbidity.log/.py; src/calibrate.py, src/models.py, src/data.py, experiments/final/run_final.py; cutoffguard/tests; pilot/pilot_threshold_transfer.py; Figure1.png, Figure2.png; and the curatedMetagenomicData sample metadata in data_cache (to check MetaCardis covariates).

---

## 1. Summary and recommendation

The Letter makes three claims. (i) A cut-off set for 90% specificity on source cohorts gives realised false-positive rates (FPRs) that vary widely at new sites. (ii) A CRC microbiome classifier gives higher scores to people with chronic disease (heart failure and T2D in the locked MetaCardis/QinJ cohorts), mostly through oral-origin taxa, and drugs (PPI, metformin) shift the score. (iii) A sequential "verified-positive" recalibration rule that uses only the colonoscopy outcomes of test-positive people has a finite-sample guarantee on expected FPR. In simulation it keeps FPR on target overall and within comorbidity groups. It is released as `cutoffguard`.

The work has real strengths. There is a written data lock and a frozen protocol enforced by the runner. Failures are reported (H3 partly supported, H5 not supported). Every idea tried is logged. The core rule is simple and useful. Counting unverified people as possible false positives is a clean way to deal with verification bias, and the counting argument is essentially correct.

**Recommendation: Major revision.**

My reasons are as follows.

- **Selective reporting.** The authors ran a post hoc analysis in the population that matters most: comorbid versus healthy colonoscopy-negative controls inside CRC cohorts. It contradicts the headline claim. Comorbid controls were flagged *less* often (LASSO 4.3% vs 16.4%; RF 1.4% vs 16.4%, OR 0.10, p = 0.04; `posthoc_within_crc_comorbidity.log`). The authors' own log says "Manuscript claims must be narrowed accordingly". This analysis is absent from the manuscript, and the title and Highlights were not narrowed.
- **Uncontrolled confounding in the locked comorbidity confirmation.** MetaCardis was adjusted for sex only. Heart-failure patients come 77% from Denmark and 0% from Germany, whereas 43% of controls are German (see M2). The statement that the within-cohort comparison "removes the site effect" is therefore incorrect for the key cohort.
- **Weak evidence for superiority over simpler label-free rules.** The advantage of the proposed rule over these rules on the primary endpoint is driven largely by FPR discreteness at very small "sites" (12–24 controls). There even the oracle exceeds the target in 100% of months. When populations are smoothed, the proposed rule is *worse* than both label-free comparators on the primary endpoint.
- **Proposition S1 is narrower than the text implies.** It bounds the *marginal expected* FPR under a realised-count assumption. The primary endpoint, however, is the per-month exceedance probability, and the drift-alarm and per-group corollaries are not proven.
- **Several text–table–figure mismatches** (Section 4).

Most issues can be fixed with the existing public data and code. If the claims are narrowed to what the evidence supports, the Letter could make a useful contribution: cut-off transfer failure, an outcome-based recalibration rule with a guarantee, and a comorbidity/drug signal in a cardiometabolic cohort. As written, it overclaims.

---

## 2. Major comments

### M1. A post hoc analysis that contradicts the headline was run but not reported; title and Highlights overclaim

- **What is wrong.** `posthoc_within_crc_comorbidity.py/.log` looked at colonoscopy-confirmed CRC cohorts that record comorbidity: FengQ_2015, ThomasAM_2018a and the locked site YuJ_2015 (T2D, hypertension, fatty liver, hypercholesterolaemia). There were 137 controls, 70 of them comorbid.
  - Comorbid controls were flagged less often than healthy controls: LASSO 4.3% vs 16.4%, adjusted OR 0.26 (0.06–1.10); RF 1.4% vs 16.4%, OR 0.10 (0.01–0.93), p = 0.04.
  - The score difference was about zero.
  - Comorbid CRC cases did not score higher (LASSO +0.10, p = 0.79).
  - The development log concludes: "CONTRADICTS a general 'chronic disease raises the cancer score' claim … Manuscript claims must be narrowed accordingly."
  - The manuscript nonetheless keeps the general title "Gut microbiome cancer tests over-flag people with chronic disease". It does not mention this analysis anywhere, even though this is the population closest to real screening (colonoscopy-negative people).
- **Why it matters.** This is selective reporting of an analysis that bears directly on the main claim. The Letter's own "All numbers reported, including failures" commitment (protocol §7) is undermined.
- **Fix.**
  - Report the post hoc analysis in the main text, with a table in the SI.
  - Retitle, e.g. "…flag some severe or drug-treated chronic conditions more often…", and narrow Highlight 2 and the Conclusion.
  - State that the excess is seen for cirrhosis, ACVD and heart failure, and for T2D in MetaCardis largely among metformin users, but not for mild cardiometabolic labels inside CRC screening cohorts.
  - Use the post hoc finding that comorbid CRC cases do not score higher when discussing the per-group sensitivity cost (it supports the proxy and should be cited there).

### M2. The locked comorbidity confirmation (MetaCardis) is confounded by country, age and drugs; "within-cohort comparison removes the site effect" is not true here

- **What is wrong.**
  - Table S3b shows MetaCardis was adjusted for sex only.
  - From the cMD metadata used by the authors (one sample per subject), recruiting country differs sharply by group: HF DNK 73 / FRA 22 / DEU 0; CAD DNK 151 / FRA 118 / DEU 0; controls DEU 273 / DNK 192 / FRA 177.
  - Country in MetaCardis is a proxy for recruitment centre, diet and sample handling, i.e. a within-study batch.
  - Age and BMI are recorded for 70% of controls, 91% of T2D, 23% of HF and 44% of CAD. Median age is 48 in controls versus 59.5–62 in the disease groups. The authors dropped age and BMI entirely rather than using the available cases.
  - Inconsistency: the exploratory metformin analysis *does* adjust MetaCardis for age, BMI and sex (Table S6d).
  - HF patients take many drugs that were not modelled (loop diuretics, anticoagulants, PPIs). The T2D effect is largely explained by metformin, since non-users are flagged at the control rate (Table S6d; main text).
  - MetaCardis "controls" are not healthy: median BMI is about 37 (the cohort recruited obese, metabolically unhealthy participants). The text repeatedly calls them "healthy controls".
- **Why it matters.** The two "confirmed" locked effects (HF and T2D) may reflect country/batch, age and medication rather than disease.
- **Fix (existing data).**
  - Re-fit H3 with country as a fixed effect, and stratified by country (e.g. Denmark-only HF vs Denmark-only controls).
  - Run an available-case analysis adjusted for age and BMI, plus multiple imputation.
  - Fit a model that includes all recorded drugs, and a model of T2D adjusted for metformin.
  - Report these as sensitivity analyses next to the pre-specified result, which should remain the primary.
  - Delete "This within-cohort comparison removes the site effect". Replace it with "reduces between-study batch effects; residual within-study differences (recruitment country, age, medication) remain".
  - Call MetaCardis controls "controls without the condition", not "healthy".
  - Clarify in the main text that MetaCardis was adjusted for sex only. Figure 1B's axis label "adjusted for age, BMI, sex where recorded" currently reads as if all three were used.

### M3. The primary-endpoint advantage over label-free comparators is a small-site discreteness artefact, and it reverses in smoothed populations

- **What is wrong.**
  - The per-site primary endpoint (analyze_final.log) shows where the proposed rule's advantage over local_q and contam comes from.
    - HallAB_2017 has 12 controls: local_q 0.35/0.50, contam 0.27/0.37, vp 0.00, and **oracle 1.0**.
    - SankaranarayananK_2015 has 18 controls: local_q 0.31–0.32, vp 0.00.
    - ThomasAM_2018a adenoma has 24 controls: RF local_q 0.86, contam 0.33, vp 0.01, **oracle 1.0**.
  - With 12 control scores, the realised FPR can only take values in steps of 1/12. Any threshold aimed at 0.10 will show "FPR > 0.12" in many months. The proposed rule "wins" by being conservative (FPR 0.083), not by being more accurate.
  - The overall oracle FPR is 0.112, with 11.6% of months above 0.12, which confirms the discreteness.
  - In the pre-specified *smoothed* setting (Table S2 "smooth"), which removes discreteness, the primary endpoint is local_q 0.020, contam 0.004 and **vp 0.026**. The proposed rule is worse than both label-free rules.
  - The text says the rule is "robust" in all settings and "favoured the new rule over a prevalence-bounded quantile (−0.04, p = 0.049)". It does not disclose this reversal.
- **Further statistical problems with the H1 tests.**
  - The Wilcoxon test treats 32 site × model units as independent. LASSO and RF on the same site are highly correlated.
  - The 16 "sites" are only 11 distinct cohorts. Four of the five adenoma sites are CRC development cohorts, and YachidaS_2019 appears twice, sharing its controls.
  - A p of 0.049 against contam would not survive a site-clustered test.
  - The contam comparison was not one of the protocol's H1 comparators (protocol §7 names source and local_q). It is presented alongside the pre-specified ones.
  - By disease, the comparison against the source cut-off is significant only for CRC (IBD p = 0.31, T2D p = 0.094, adenoma p = 0.48; RESULTS_locked.md). The main text does not say this.
- **Fix.**
  1. Report the per-disease H1 results in the main text.
  2. Add a site-level analysis (average the two models within a site; one unit per cohort; sign test or permutation test over sites).
  3. Re-run H1 excluding sites with fewer than 50 controls, and report the smoothed setting next to the primary one.
  4. Compare methods at *matched* realised FPR, or use mean |FPR − α| (a secondary endpoint already computed), rather than only the exceedance share.
  5. Rephrase the claim versus contam as "similar FPR control; the proposed rule is less affected by prevalence and recovers from drift". Those are its real advantages: contam and local_q become conservative at π = 0.10–0.30 and have no restart.

### M4. The simulation is close to circular, the comparators have no restart, and the costs (sensitivity, burn-in load) are under-reported

- **What is wrong.**
  - **Exchangeability holds by construction.** Each "site population" is the cohort itself, resampled with replacement. True FPR is computed on the same finite set. Assumption A1 of Proposition S1 therefore holds exactly, so the primary simulation mostly re-confirms the theorem.
  - **The setting is not a screening setting.** Cancer cases come from case-control studies, which over-represent advanced or symptomatic disease. For the IBD and T2D "sites", "colonoscopy verification of test positives" has no clinical meaning, yet these sites provide 16 of the 32 units and drive the pooled H1.
  - **Drift was tested only upward (+0.5 logit).** Because unverified people above any candidate cut-off are counted as false positives, the rule can easily *raise* its cut-off but can lower it only into a region where people were already verified (a ratchet). When the true control distribution shifts *down*, or the source cut-off is too conservative, the rule may stay conservative indefinitely and lose sensitivity. The drift alarm only fires on excess false positives, so it does not help here.
  - **The comparators were not given a restart.** local_q and contam use an ever-growing pool with no window or alarm. Their failure after drift (Figure 2B) therefore reflects the comparison design, not a property of label-free rules. The positivity rate itself is an unlabelled drift signal that could trigger a restart.
  - **Sensitivity cost.** At the CRC sites, sensitivity falls from 0.644 (source) to about 0.515 (vp). At 1% prevalence there are 10 cancers per 1,000, so "1.1 more missed cancers per 1,000" is an ~11% relative loss of detected cancers. That is about 75 colonoscopies avoided per extra missed cancer. This trade-off needs to be stated plainly; it is a clinical choice, not a side note.
  - **Burn-in load.** The month-1 referral rate is 0.33 at CRC sites and 0.35 at T2D sites, versus 0.21–0.26 for the source cut-off (analyze_final.log). That is roughly three times the target referral load for one month, with real implications for endoscopy capacity.
- **Fix.**
  - Add −0.5 logit and gradual (linear) drift scenarios, and a scenario where the source cut-off is conservative (true FPR about 0.03).
  - Give local_q and contam the same windowing or restart, e.g. restart when the monthly positivity rate departs from its running mean by a binomial test.
  - State the sensitivity loss and the burn-in referral rate in the main text.
  - Describe the simulation honestly as a check of operating characteristics under exchangeable resampling, not as evidence of real-world deployment performance.
  - Drop, or move to the SI, the IBD and T2D "screening" sites, or restrict the headline H1 to CRC and adenoma.

### M5. Proposition S1: correct core argument, but the stated scope is wider than the proof (details in Section 5)

- **What is wrong.**
  - Assumption A2 concerns the *realised* number of cases in the window (m1 ≤ ⌊π_max·m⌋), not the prevalence. The main text says "if … prevalence stays below the bound". With π = π_max (the simulation uses π_max = max(0.05, π), so π = π_max at π = 0.05 and 0.10), A2 fails in about half of windows.
    - My own check with `cutoffguard` at π = π_max and uninformative case scores gave a mean FPR of 0.0995 (MC SE 0.0003), so the rule seems robust in practice. The proof, however, does not cover this case.
  - The guarantee is on the expected (marginal) FPR. The primary endpoint is the per-month probability of FPR > 0.12, and the Highlights claim the FPR was kept "on target at each site". The package's own test gives P(FPR > 0.12) ≈ 9.7% per deployment at m = 200.
  - Corollary (b), on the drift alarm, chooses the window start from the data, which breaks the exchangeability used in step (iii).
  - Corollary (a), per group, needs A1 and A2 *within each group*. CRC prevalence plausibly differs by comorbidity group, and very small group windows (HF ≈ 6 tests per month) make A2 on realised counts fragile.
  - SI §S7(c) says the numerical check "gave a mean FPR of at most 0.105". In fact 0.105 is only the assertion tolerance in `test_guarantee.py`. Re-running the test gives a mean of 0.092 (MC SE 0.0003).
- **Fix.**
  - Restate A2 as a realised-count condition, or replace it with a high-probability bound, e.g. m1 ≤ the binomial (1 − δ) quantile, giving P(X ≥ t*) ≤ α + δ.
  - Say clearly that the guarantee is marginal.
  - Either add a training-conditional (PAC) version, which is straightforward with a binomial tail as in `pac_controls`, or drop the "kept on target at each site" wording.
  - Downgrade corollary (b) to an empirical observation.
  - State the per-group prevalence requirement in (a).
  - Report the true value of the numerical check.

### M6. "Locked" and "independent" status is overstated

- **What is wrong.**
  - The pilot, run before the data lock, computed the realised FPR of the source cut-off at all 11 CRC cohorts, including the three locked CRC sites (data_lock.md: "Only the pilot … has touched all CRC cohorts"). The overdispersion p-value in the main text comes from these cohorts. The main text says methods were fixed "before touching the locked test cohorts".
  - The "16 new sites" in the Highlights are 11 distinct cohorts. Four adenoma "sites" are CRC development cohorts whose controls were used to develop the method.
  - The sensitivity analyses for smoothing, 70% attendance, 5% missed cancers, drift and combined stresses are called "pre-specified" in SI §S4, but protocol.md §8 lists only (a)–(e). They were in the frozen code (log round 6 calls them "f–j") but not in the frozen protocol text.
  - The mechanism analysis (round 9) and the post hoc analysis P1 came after the freeze. That is disclosed for round 9 only.
- **Fix.**
  - Disclose that the pilot touched the locked CRC sites, and that the source-cut-off result at those sites was therefore known before locking.
  - Say "16 site analyses in 11 distinct cohorts", and flag that the adenoma sites are only partly independent in the main text.
  - Align the SI with the protocol on which analyses were pre-specified.

### M7. Medication results are spun in the Highlights and the metformin interpretation is partly inaccurate

- **What is wrong.**
  - **PPI.** The primary hypothesis H5 failed for the primary (LASSO) model (+0.04, p = 0.24; positivity RR 1.21, 0.89–1.59). Highlight 3 nonetheless leads with "Proton-pump inhibitors raised the oral-taxa part of the cancer score, as predicted".
    - H6 is close to tautological: PPIs are known to raise oral Streptococcus/Veillonella, and the "oral part" is a weighted sum of exactly those taxa.
    - After adjustment for the oral component, the PPI effect on the total score is *negative* (−0.12, −0.23 to −0.01). In other words, the mechanism does not carry through to test results for the primary model.
  - **Metformin.**
    - The text says "Enterobacterales and *Streptococcus salivarius* drove this effect". In addendum_metformin_explore.log, however, the largest contributors are Lachnoclostridium (0.097) and depletion of *E. eligens* (0.091), followed by *S. salivarius* (0.055), Firmicutes CAG110 (0.052), and Enterobacterales only 0.037 (plus Morganellaceae 0.023).
    - "Two cohorts with few metformin users did not [show the same direction]" is inaccurate for KarlssonFH_2013, where β is positive in both models (+0.04, +0.05) but tiny and imprecise.
    - The "smaller cohort" with the same direction (LiJ_2014) is a development cohort, and its RF positivity goes the other way (15.5% vs 23.8%).
    - Within T2D, metformin non-users differ systematically: insulin-treated, newly diagnosed, or with renal contraindications. This confounding by indication is not discussed.
- **Fix.**
  - Rewrite Highlight 3 as "PPI use did not raise the primary model's score, although it raised the oral-taxa component; metformin use was associated with higher scores (exploratory)".
  - Correct the description of the metformin drivers.
  - Describe the replication cohorts accurately.
  - Add confounding by indication as a limitation.
  - In MetaCardis, adjust the within-T2D metformin analysis for disease duration, HbA1c or insulin use if recorded.

### M8. The mechanism and "cannot be cleaned" claims rest on thin, single-model evidence

- **What is wrong.**
  - "78–100% of the increase came from oral-origin taxa" includes fatty liver, whose total effect is null (+0.21, −0.26 to 0.68; Table S3c). A percentage decomposition of a non-significant difference is not interpretable.
  - The decomposition is LASSO-only and linear. RF, which drives several locked results, is not decomposed.
  - The second-largest contributor overall (Lachnoclostridium) is not oral, so how taxa are assigned to the "oral" group matters. The classification rule ("genera typical of the oral cavity") should be listed per species in the SI.
  - Table S4's caption promises a "None = full model" row that is missing. The baseline AUROC of 0.76 is not in any SI table (it appears only in the development log as 0.763).
  - The control-augmentation result ("lowered false alarms overall but kept the gap") has no table at all.
  - "Removing … lowered cancer detection before it removed the excess false alarms": at K = 2, comorbid positivity is still 0.133 versus 0.044 in controls (a 3× ratio), so the claim is plausible. However, only three K values were tried and there are no uncertainty intervals.
- **Fix.**
  - Restrict the percentage statements to conditions with a significant gap.
  - Add the per-species oral/non-oral classification, the full-model row in Table S4, a control-augmentation table, and bootstrap CIs for the decomposition shares.
  - Ideally, show the decomposition for a second linear model (e.g. elastic net) or SHAP values for RF.
  - Soften the heading "…why the signature cannot simply be cleaned" to "…why cleaning the signature is costly".

### M9. The overdispersion test is anti-conservative and not reproducible from the deposited outputs

- **What is wrong.**
  - `pilot_threshold_transfer.py` compares realised false-positive counts with Binomial(n0, 0.10) using a χ² statistic with df equal to the number of cohorts.
  - This ignores the sampling variability of the source threshold itself. That threshold is an estimated quantile from a finite number of out-of-fold source controls, and the same threshold is shared across held-out cohorts in a correlated way.
  - Extra-binomial variation is therefore expected even with no site effect.
  - Only the RF p-value is reported, and the pilot output log is not deposited, so p = 2 × 10⁻⁷ cannot be verified.
- **Fix.**
  - Use a parametric bootstrap that re-draws the source controls and re-estimates the threshold, or a random-effects (beta-binomial) model of logit-FPR across sites.
  - Report both models.
  - Deposit the pilot log.

---

## 3. Minor comments

1. **Figure 1A clips a data point.** The x-axis stops at 0.6, but the RF point for one T2D site is at about 0.74. It is implied by the T2D mean source FPR of 0.259 over 8 units, and the text says "0.00 to 0.75". Extend the axis.
2. **Figure 2A title and legend are wrong.** They say "16 sites × 2 models, 1% prevalence", but adenoma was simulated only at π = 0.10/0.30. The panel therefore shows 11 sites. Its source-FPR line (0.198) matches the CRC + IBD + T2D mean, not the all-site 0.171.
3. **Table S2b is mislabelled.** It says "months 7–12", but its values match months 1–12 (including the burn-in month). For example, CRC vp 0.105–0.108 in Table S2b versus 0.087–0.091 for months 7–12 in analyze_final.log. As printed, it suggests the rule exceeds α at CRC and T2D sites, contradicting Proposition S1.
4. **Figure 2D labels overlap.** The x-axis labels ("missed/1,000: 3.6 vs 4.7 …") are illegible. Also, "missed cancers" for IBD and T2D sites are missed IBD/T2D cases, not cancers.
5. **Wrong citation.** "T2D in a second cohort [16]" cites Forslund 2015, but the cohort is QinJ_2012 (Qin J et al., *Nature* 2012). KarlssonFH_2013, MetaCardis (Forslund 2021 / Fromentin 2022), YachidaS_2019, YuJ_2015 and the other cohorts in Table S1 should be cited in the SI.
6. **Cohort count.** "32 public cohorts" requires VincentC_2016 and LeeKA_2022, which are missing from Table S1. Table S1 lists 30 distinct cohorts.
7. **Unexplained cohort counts.** HMP_2019_ibdmdb has 103/27 in Table S1 but 57/14 in Table S3 (presumably the adult filter; say so). IjazUZ_2017 is listed as a locked comorbidity cohort but is absent from Table S3 without explanation.
8. **Bootstrap upper bounds of "999.00".** These come from division by ~0 when there are no control positives. Use a Wilson or Katz CI for the risk ratio, or report "not estimable".
9. **Unadjusted estimates labelled as adjusted.** "+0.33 hypertension" is described as adjusted, but LiJ_2017 has no covariates (crude = adjusted in Table S3c). The same applies to LoombaR_2017.
10. **Mis-described reference.** Ref. 23 (Tong et al., Neyman–Pearson classification) is not a conformal method. Cite a split-conformal reference (e.g. Vovk; Angelopoulos & Bates) or rephrase.
11. **Reproducibility of the LASSO model.** `LogisticRegression(l1_ratio=1, solver="liblinear")` gives an L1 penalty only in scikit-learn ≥ 1.8. In earlier versions `penalty` defaults to "l2" and `l1_ratio` is ignored, so a ridge model would be fitted silently. Pin the version or pass `penalty="l1"`.
12. **Ties in RF scores.** RF probabilities are clipped to [1e-4, 1 − 1e-4] before the logit. With 500 trees this produces many tied scores at the bounds, which interacts with "≥ t" thresholds and quantiles. State how ties are handled.
13. **"Settled at 0.085 from month 2".** 0.085 is the months 7–12 mean pooled over all prevalences. At 1% prevalence (Figure 2A) the value is about 0.08. Report the month-1 FPR (about 0.29) explicitly.
14. **"Robust … FPR on target".** At α = 0.05 the realised FPR was 0.034, a conservative bias of 32%. Report it as conservative.
15. **Group recalibration in small groups.** It brought mean FPR to 0.08–0.09, but HF still exceeded 0.12 in 15% (LASSO) and 13% (RF) of months (Table S5). Mention this next to "kept the false-positive rate on target … within patient groups".
16. **Arbitrary group shares.** The Part C shares (CAD 0.10, T2D 0.15, HF 0.03, IGT 0.15) are not justified. Give a source or a sensitivity range.
17. **Batch-correction comparator.** A batch-correction analysis was started (dev/explore_v10_batchcorr.py, empty log) but is not mentioned in the development log or the manuscript. Site-wise standardisation is an obvious label-free alternative and should be reported, or its absence explained.
18. **Sensitivity proxy.** The Part C "sensitivity proxy" uses out-of-fold development CRC case scores for every group. Make this explicit in the main text, not only in the legend.
19. **Taxonomy version.** MetaCardis_2020_a comes from a different cMD release (2022-10-19). Confirm that the MetaPhlAn database and taxonomy version match the training data; species absent from the training feature set are silently set to 0.
20. **Letter length.** The Letter is dense for an iMeta Letter. Consider moving the drug section, or the robustness paragraph, to the SI so the main claims can be stated with their caveats.

---

## 4. Numeric claims in the main text: verification table

| # | Claim (main text / Highlights) | Source checked | Status |
|---|---|---|---|
| 1 | "32 public cohorts … including 16 locked test sites" | Table S1 (30 distinct cohorts listed; +VincentC, LeeKA from Table S6a = 32); 16 site analyses = 11 distinct cohorts | **Partial mismatch**: Table S1 omits 2 cohorts; the "16 sites" are not 16 independent cohorts |
| 2 | Highlights: FPR "0% to 75% at 16 new sites" | analyze_final.log source FPR; Figure 1A | Verified numerically (implied RF T2D point ≈ 0.74), but **Figure 1A clips it** |
| 3 | CRC FPR 0.11–0.28 | Figure 1A | Verified |
| 4 | IBD 0.02–0.41 | Figure 1A; mean 0.144 consistent | Verified |
| 5 | T2D 0.00–0.75 | Figure 1A (max shown ≈ 0.59) + mean 0.259 | Verified by inference; **figure mismatch** |
| 6 | Adenoma 0.00–0.26 | Figure 1A | Verified |
| 7 | "15 of 32 site–model pairs (47%) > 0.12" | analyze_final.log per-site source P_over = 1.0 in 15 units | Verified |
| 8 | Overdispersion p = 2 × 10⁻⁷ (RF) | pilot script; no log deposited | **Not verifiable** |
| 9 | Cirrhosis 52% vs 8% | novelty_escalation_log round 7 | Verified (not in SI tables) |
| 10 | Cirrhosis +1.30 (0.99–1.60) | Table S3c 1.297 (0.993–1.601) | Verified |
| 11 | ACVD 52% vs 19%; +0.87 (0.62–1.12) | log round 7; Table S3c 0.871 (0.622–1.119) | Verified |
| 12 | Hypertension +0.33, ME/CFS +0.39 significant | Table S3c 0.333 (p 0.014; unadjusted), 0.392 (p 0.006) | Verified (hypertension is not covariate-adjusted) |
| 13 | "higher in every condition" (7 dev cohorts) | Table S3c: all β > 0, 3 n.s. | Verified for point estimates; wording overstates |
| 14 | HF test-positive 2.3× | Table S3 2.25 (LASSO), 2.30 (RF) | Verified |
| 15 | HF LASSO +0.33 (0.14–0.51), Holm-significant both models | Table S3b 0.3276 (0.1416–0.5137), p_holm 0.0026 / RF 0.0174 | Verified (sex-only adjustment not stated) |
| 16 | T2D 1.7 (LASSO) to 3.1 (RF)× | Table S3 1.70, 3.08 | Verified |
| 17 | T2D +0.35 (0.25–0.45), Holm p < 10⁻⁴ | Table S3b 0.3532 (0.2547–0.4517), p_holm 0 | Verified |
| 18 | QinJ T2D RF +0.35, Holm p = 0.0002; LASSO nominal | Table S3b 0.3492, 0.0002; LASSO p 0.035 / Holm 0.24 | Verified; **citation [16] wrong** |
| 19 | CAD, IGT (MetaCardis), Karlsson T2D: no increase | Table S3b | Verified |
| 20 | IBD nominal in one cohort, not after correction | Table S3b NielsenHB p 0.016/0.013, Holm 0.13/0.089 | Verified |
| 21 | Oral taxa 78–100% (cirrhosis, ACVD, fatty liver) | log round 9 (78%, 83%, ~100%); Figure 1C | Verified (fatty liver gap is null) |
| 22 | Hypertension 81% commensal depletion | log round 9; Figure 1C | Verified |
| 23 | AUROC 0.76 → 0.72 | log round 9 (0.763 → 0.721); Table S4 K = 2 0.721 | Verified; **baseline row missing from Table S4** |
| 24 | Control augmentation keeps gap | log round 7 only | **No SI table** |
| 25 | MetaCardis 1,831 adults, 295 PPI users | Table S6b; Table S3 group sums = 1,831 | Verified |
| 26 | PPI oral part +0.18 (0.14–0.21), p < 10⁻¹⁰ | Table S6b 0.1751 (0.1443–0.2058), p ≈ 0 | Verified |
| 27 | PPI total RF +0.09, p = 0.014; 16.6% vs 11.9% | Table S6b 0.0865, 0.0143; Table S6c 0.1661 / 0.1191 | Verified |
| 28 | PPI LASSO +0.04, p = 0.24 | Table S6b 0.0382, 0.2444 | Verified |
| 29 | Metformin +0.43 (0.30–0.55), both models | Table S6b 0.4267 (0.3048–0.5485); RF 0.374 | Verified |
| 30 | Metformin in T2D 2.4 (LASSO) to 3.9 (RF)× | Table S6d 0.2054/0.0851 = 2.41; 0.2787/0.0709 = 3.93 | Verified |
| 31 | Non-users flagged at control rate | 0.085 vs 0.103 (LASSO); 0.071 vs 0.073 (RF) | Verified |
| 32 | Enterobacterales and *S. salivarius* drove metformin effect | addendum_metformin_explore.log: top = Lachnoclostridium 0.097, *E. eligens* 0.091 | **Mismatch** |
| 33 | "two cohorts … did not" (metformin) | Table S6d: Karlsson β +0.04/+0.05 | **Partly inaccurate** |
| 34 | Source cut-off FPR 0.17; 49% of months > 0.12 | Table S2 primary 0.171 / 0.488 | Verified |
| 35 | vp FPR 0.085; 0.6% of months > 0.12 | Table S2 0.085 / 0.006 | Verified (months 7–12, all π) |
| 36 | H1 vs source −0.46 (−0.66 to −0.20), p = 0.011 | analyze_final.log −0.462 (−0.658, −0.195), p 0.01146 | Verified |
| 37 | vs local_q −0.10, p = 2.5 × 10⁻⁷ | −0.095, p 2.489e-07 | Verified |
| 38 | vs contam −0.04, p = 0.049 | −0.040 (−0.093, −0.006), p 0.04896 | Verified (not a protocol H1 comparator; reverses in "smooth") |
| 39 | Sensitivity within 0.015 of oracle (−0.021 to −0.009) | H2 log | Verified (oracle operates at FPR 0.112, not matched) |
| 40 | 83 fewer unnecessary colonoscopies / 1,000 (CRC, 1%) | log: source (185.27 + 188.88)/2 = 187.1; vp (100.32 + 107.04)/2 = 103.7 | Verified |
| 41 | +1.1 missed cancers / 1,000 | (4.54 + 4.80)/2 − (3.28 + 3.84)/2 = 1.11 | Verified (≈ 11% relative loss not stated) |
| 42 | Robust: FPR on target, ≤ 3% of months > α + 0.02 | Table S2: max vp P_over 0.029 (α 0.20); α 0.05 FPR 0.034 | Verified for exceedance; "on target" is conservative at α = 0.05 |
| 43 | Drift: back to 0.09 within 3 months | RESULTS: months 10–12 0.086 | Verified |
| 44 | Combined: FPR 0.10, 20% of months > 0.12 (months 13–18) | RESULTS 0.102 / 0.202 | Verified |
| 45 | Part C pooled overall 0.095; HF 0.21, T2D 0.14, controls 0.08 | log Part C (LASSO 0.212, 0.144, 0.083; overall 0.095) | Verified |
| 46 | Group rule: all groups 0.08–0.09, overall 0.092 | log 0.084–0.093; 0.092 | Verified (HF P_over 15% not stated) |
| 47 | HF sensitivity 0.36 vs 0.45 | Table S5 0.360 / 0.453 | Verified |
| 48 | CRC 1.9 M cases, 0.9 M deaths (2020) | GLOBOCAN [1] | Verified (external) |
| 49 | Figure 2A "16 locked sites, 1% prevalence" | adenoma not simulated at 1% | **Mismatch** (11 sites) |
| 50 | Table S2b "months 7–12" | values match months 1–12 | **Mismatch** |
| 51 | S7(c): numerical check "mean FPR at most 0.105" | test_guarantee.py tolerance; re-run mean 0.092 | **Misreported** |

---

## 5. Check of Proposition S1 and its proof

**Statement.** Under (A1) exchangeability of window controls with a future control X, (A2) m1 ≤ ⌊π_max·m⌋, and (A3) no false-positive reference results, P(X ≥ t*) ≤ α conditional on m0.

**Step (i).** Controls with s ≥ t* are never verified cases under A3, so FP(t*) ≤ FP_ub(t*). **Correct.** Missed cancers (cases labelled as controls) only add to FP_ub and lower C1, which is conservative, as claimed.

**Step (ii).** m0_lo = m − max(C1, ⌊π_max·m⌋) ≤ m − m1 = m0 needs max(C1, ⌊π_max·m⌋) ≥ m1. This follows from A2, since C1 ≤ m1 ≤ ⌊π_max·m⌋. **Correct given A2.** Then FP(t*) + 1 ≤ α(m0_lo + 1) ≤ α(m0 + 1). Because FP is an integer, FP(t*) ≤ ⌊α(m0 + 1)⌋ − 1 = k. If at most k controls are ≥ t*, the (k+1)-th largest control, S_(m0−k), is < t*. **Correct.**

**Step (iii).** By A1, the rank of X among the m0 + 1 controls is uniform. P(X > S_(m0−k)) ≤ (k+1)/(m0+1) = ⌊α(m0+1)⌋/(m0+1) ≤ α. This stays valid with ties, because the strict inequality makes it conservative. Since t* > S_(m0−k) holds pointwise, P(X ≥ t*) ≤ α. **Correct.** The pointwise inequality also justifies "any verification pattern, including score-dependent ones". The bound does not require t* to be independent of the controls.

**Errors, gaps and overstatements.**

1. **The k < 0 edge case is not handled.** If α(m0_lo + 1) < 1, no finite t satisfies the rule. The code returns +∞ (`verified_positive_seq`), but the proof and rule should state t* = +∞, with P = 0. This happens whenever m0_lo < (1 − α)/α, e.g. fewer than 9 controls at α = 0.10. It is relevant to small group windows in Part C.
2. **A2 is a realised-count condition, not a prevalence condition.** The main text says "if … prevalence stays below the bound". With binomial sampling, P(m1 > ⌊π_max·m⌋) is about 0.4–0.5 when π = π_max, which is the case in the simulation at π = 0.05 and 0.10. The proposition then gives no guarantee. Empirically the rule remains valid; my check gave mean FPR 0.0995 at π = π_max with uninformative case scores, because unverified cases are already counted in FP_ub. A corrected statement is either:
   - P(X ≥ t*) ≤ α + P(m1 > ⌊π_max·m⌋); or
   - a version in which m0_lo uses a binomial upper confidence bound for m1.
3. **"Conditional on m0".** This is fine, but then A1 must hold conditional on m0 and on the case scores and verification pattern. That holds under i.i.d. sampling and should be said explicitly.
4. **The guarantee is marginal.** It averages over windows. It says nothing about the probability that a given month's FPR exceeds α + 0.02, which is the primary endpoint, or about "each site". A PAC (training-conditional) analogue follows from the same counting argument with a Beta/binomial tail. Choose the largest k such that P(Bin(m0_lo, α) ≤ k) ≤ δ. The text should either add it or reword.
5. **Corollary (a), per group,** needs A1 and A2 within each group, with a group-specific π_max. Also, edge case 1 applies frequently in small groups.
6. **Corollary (b), drift alarm, is not proven.** The restart month is a data-dependent stopping time selected *because* it had excess false positives. Conditioning on the restart changes the distribution of window scores, so exchangeability with a future control is not guaranteed. Also, a gradual drift inside a window violates A1 without triggering the alarm. Present this as an empirical property only.
7. **Sequential re-use.** The bound holds at each update separately. Statements about averages over months are fine by linearity of expectation, but any statement that the FPR stays within a band across months needs a uniform-in-time (union or martingale) argument.
8. **Corollary (c).** "A false-positive colonoscopy result … its effect is bounded by the number of such errors" is stated without proof. If e controls are mislabelled as cases, then C1 and m0_lo shift by at most e and FP_ub falls by at most e. A bound such as P(X ≥ t*) ≤ (k + 1 + 2e)/(m0 + 1) seems derivable and should be written out.
9. **The S3 and S7 formulas agree.** m − C1 − max(0, ⌊π_max·m⌋ − C1) = m − max(C1, ⌊π_max·m⌋). The code (`calibrate.verified_positive_seq`, `cutoffguard.core`) matches the stated rule. The returned threshold `bad[len−k−1] + 1e-9` leaves at most k non-verified-case scores at or above t, which is the smallest valid t. No coding error was found.
10. **The numerical check is misreported** ("at most 0.105" is the assertion tolerance; the observed mean is 0.092).

**Verdict on the proof.** The core counting argument is correct. The statement needs:

- the realised-count form of A2, or a high-probability version;
- an explicit t* = +∞ case;
- a statement that the guarantee is marginal;
- the drift-alarm corollary removed or downgraded;
- explicit within-group assumptions for the per-group corollary.
