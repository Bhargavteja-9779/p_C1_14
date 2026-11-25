# Referee report R1-03: domain, novelty and clinical realism

**Manuscript:** "Stool-metagenome classifiers miss their intended false-positive rate in new laboratories, and a label-free rank rule fixes it" (iMeta Letter, draft v0.2, 2026-11-25)
**Reviewer expertise:** microbiome diagnostics, metagenomic machine learning, clinical prediction-model updating, label shift and conformal methods
**Material read:** manuscript.md, supporting_information.md, Figure 1 and Figure 2 (PNG), results/main_tables.md, results/cohort_level_summary.csv, results/table_s1_cohorts.csv, code/experiments/protocol.md, journal_selection/novelty_map.csv, journal_selection/novelty_search_log.md. I checked all 20 reference DOIs against Crossref (and DataCite for the arXiv DOI), and ran my own OpenAlex/Crossref searches for prior work the authors missed.

---

## 1. Summary of the submission

The authors train LASSO and random forest classifiers on curatedMetagenomicData stool profiles. They set the cut-off at 90% specificity on out-of-fold training scores and measure the realised false-positive rate (FPR) in 16 "locked" cohort-task pairs (3 external CRC cohorts, plus leave-one-cohort-out IBD, T2D and adenoma models). The realised FPR ranges from 0.00 to 0.74. Five label-free adaptation methods (Saerens EM, MLLS-BCTS, two-Gaussian unsupervised score calibration, the authors' location-scale mixture, and per-site feature standardisation) do not repair this, and most make it worse. The proposed fix sets the cut-off at the r-th highest score of an unlabelled local pool. r is chosen from Beta order statistics, with an allowance for a maximum case share pi_max. It reaches a cohort-RMSE of 0.031, against 0.185 for the training cut-off. The paper converts this into colonoscopies per 1,000 at 0.5% CRC prevalence and gives a sample-size curve for the high-probability version.

The question is relevant to iMeta readers. Reporting the realised FPR at each external cohort is a recommendation the field should adopt, and the negative results for label-shift methods at low prevalence are useful. My concerns are with the novelty framing, the evaluation design, and the clinical realism. (i) The proposed rule is an established idea in at least three neighbouring literatures: Neyman-Pearson order-statistic thresholds with contaminated or noisy class-0 data, conformal outlier detection with a contaminated reference set, and positivity-rate-based cut-off setting in FIT screening programmes and indirect reference intervals in laboratory medicine. None of these is cited. (ii) The within-cohort split, together with pools of median about 20 controls, makes the rule's main result close to true by construction. (iii) Several statements about prior work are inaccurate.

## 2. Recommendation

**Major revision.** As written, the title and the key claims ("Nobody has checked", "a label-free rank rule fixes it", "comes with a finite-sample guarantee") are not supported against prior work or by an evaluation that tests the rule's critical assumption. A rescoped letter could be publishable. It would present (a) a decision-level audit of threshold transfer for microbiome classifiers and (b) a careful, honestly positioned demonstration that the established contamination-robust order-statistic threshold works when a local pool is available, and when it does not.

---

## 3. MAJOR issues

### M1. The proposed rule is not new. The closest prior art for the method is uncited.
*Location:* Abstract-style opening paragraph ("A simple rule fixes it ..."); section "A RANK RULE ON THE LABORATORY'S OWN SAMPLES KEEPS THE PROMISE"; SI Note S1.

The rule is: take an order statistic of an unlabelled sample that is mostly class 0, choose its rank from Beta/binomial tail bounds, and note that contamination by stochastically larger cases only makes it conservative. This is, in order of closeness:
- **The NP umbrella algorithm** (Tong, Feng & Li 2018, *Sci Adv*, 10.1126/sciadv.aao1659). It sets the threshold at the k-th order statistic of held-out class-0 scores, with k chosen from the binomial tail, so that P(type-I error > alpha) <= delta. This is exactly the authors' "high-probability version", and the authors' own novelty map lists it (bucket 4, row 55).
- **NP classification under label noise** (Yao, Rava, Tong & James 2022/2023, *JASA*, 10.1080/01621459.2021.2016423). It shows that NP classifiers trained or calibrated on a class-0 sample contaminated by class-1 points still control the type-I error, at the cost of conservativeness and power. This is precisely the claim in Note S1 (ii)-(iii) and the "price is sensitivity" paragraph.
- **Conformal outlier detection under contaminated reference data** (Bashari, Sesia & Romano, ICML 2025, 10.48550/arxiv.2502.04807). It proves that calibrating on a reference set with a small fraction of outliers yields conservative type-I error control and loses power, which is the same statement as Note S1. See also Einbinder et al. 2022 (10.48550/arxiv.2209.14295) on conformal prediction with noisy labels.
- **Laboratory medicine.** Indirect reference-interval estimation derives decision limits from routine, unlabelled, mostly healthy patient results: Jones et al. 2018, IFCC C-RIDL review, *CCLM*, 10.1515/cclm-2018-0073; refineR, Ammer et al. 2021, *Sci Rep*, 10.1038/s41598-021-95301-2. Local verification and transference of reference intervals with about 20 local reference samples (CLSI EP28-A3c) is the direct analogue of the "10 labelled local controls" comparator. This is the vocabulary a laboratory reader will expect.
- **CRC screening practice.** FIT programmes routinely set or revise the positivity cut-off from the observed positivity rate in the screened population, to match colonoscopy capacity (Toes-Zoutendijk et al. 2017, *Gastroenterology*, 10.1053/j.gastro.2016.11.022; Brenner & Werner 2017, *Clin Transl Gastroenterol*, 10.1038/ctg.2017.37). In a screening pool with less than 1% cancers, the "rank rule" is a positivity-rate target. Gastroenterologists will recognise it as such.

The authors' own novelty search (novelty_search_log.md) was run against the abandoned location-scale mixture method. Its scorecard rates method novelty 2/5 for that method. The final rank rule was never re-searched. None of the queries covered NP with label noise, contaminated conformal calibration, indirect reference intervals or FIT positivity-rate cut-offs.

*Fix:* Cite and discuss these works. Retitle (e.g., "Decision thresholds of stool-metagenome classifiers do not transfer between cohorts: an audit and a local recalibration protocol"). Present the rank rule as an application of the contamination-robust NP/conformal order-statistic threshold, not as a new method. Remove "our" and "(ours)" from Figure 2. The contribution then rests on the microbiome audit and the deployment protocol, which is defensible for a Letter.

### M2. The main evaluation of the rank rule is close to circular, and the primary endpoint cannot detect per-deployment failure.
*Location:* SI "Evaluation design"; main text "At the locked cohorts, the expected-FPR rule had a cohort-RMSE of 0.031..."; protocol.md ("Known limitations").

- The pool and the evaluation set are random halves of the same cohort's controls. They are therefore exchangeable by design, and any order statistic of the pool has expected FPR r/(n0+1) by elementary theory. The locked "result" for the rank rule (mean FPR 0.082 against r/(n0+1) of roughly 0.08-0.095) re-derives Note S1. It does not test it. The assumption that can actually fail in practice is that pool and future samples are exchangeable: run-in samples versus later batches, kit lots, sequencing runs, seasons, or changes in the invited age range. The authors admit this ("the cross-study stress test (dev round 4B) is the evidence about non-exchangeable pools"), but that stress test is on development cohorts only and is not reported in the manuscript or SI.
- The primary endpoint, cohort-RMSE of the *mean over 200 splits* of the realised FPR, measures only bias. One laboratory gets one draw. With the locked pool sizes (cohort_level_summary.csv: n_pool is 6-30 for 12 of 16 cohorts, median about 20), the realised FPR of a single deployment is roughly Beta(r, n0-r+1) with r = 1-2. That distribution has a standard deviation of about 0.06-0.09 around a target of 0.10. The table column p_fpr_over_a_plus_5 shows this: 14% of deployments of the primary rule exceed 15% FPR, and 20% for ctrl10.
- Because the pools are this small, the primary rule is in practice "the 1st-2nd largest score among about 20 local controls". It differs from the ctrl10 comparator mainly in using about twice as many samples. It is also significantly *worse* than ten labelled controls (difference 0.006, P = 0.048).

*Fix:* (a) Make the primary endpoint per-deployment: RMSE over splits and cohorts of (realised FPR - alpha), and P(FPR > alpha + 0.05). (b) Add a non-exchangeable evaluation on the locked cohorts in which the pool and the evaluation set come from different strata. Possible strata: different studies from the same country or lab (e.g., ThomasAM_2018a/b, Yachida batches), different sequencing runs or sampling dates where metadata allow, or a temporal split for longitudinal cohorts. (c) Report results by pool size, and state in the main text that 12/16 locked pools are far below the ~360 the guaranteed version needs, so that version abstains in 50% of units.

### M3. The "1% case share" primary scenario contains no cases in most cohorts.
*Location:* SI "Evaluation design"; code/experiments/final/run_final.py line 29 (`n1 = round(pi * len(c0) / (1 - pi))`).

With pools of 6-30 controls, round(0.01 x n/0.99) = 0. The pool therefore contains zero cases in 13/16 cohorts at pi = 0.01, and in several at pi = 0.05 as well. The pi = 0 and pi = 0.01 tables are nearly identical for this reason. The headline claims ("at a 1% case share", "label-free fixes fail at screening prevalence") are effectively evaluated at 0% cases. This also handicaps the mixture and label-shift baselines asymmetrically: they must estimate a case component that is not there.

*Fix:* Report the realised number of cases per pool. Either use a stochastic case count (Binomial(n, pi)) or restrict the contamination analysis to cohorts with pools of at least 100. Re-label the primary scenario honestly.

### M4. Near-chance tasks drive the "failure" claims, and the AUROC statement is inaccurate.
*Location:* Opening paragraph ("although the AUROC stays acceptable"); Figure 1A/B; overdispersion test.

Locked AUROCs are 0.54-0.65 for adenoma (mean 0.58) and 0.58-0.69 for T2D (mean 0.62); see cohort_level_summary.csv and Figure 1B. These classifiers have no clinical use at any threshold. Their score distributions are compressed, so tiny location shifts produce extreme FPRs (QinJ T2D: 0.60/0.74; four RF adenoma cohorts: exactly 0.000). These units dominate the overdispersion statistics (P = 10^-52, 10^-88) and the 0.00-0.74 range quoted in the abstract and introduction. In addition, 4/5 adenoma cohorts reuse control samples that were part of the development cohorts used to design the methods (SI, Table S1 note), and YachidaS_2019 appears in both the CRC and adenoma locked sets. The 32 "units" are therefore not independent: two models are fitted on the same cohort, and controls are shared across tasks.

*Fix:* Remove "AUROC stays acceptable". Stratify all headline numbers by task and report CRC and IBD separately from T2D and adenoma. Treat the adenoma task as not fully locked. Cluster the bootstrap and the Wilcoxon test at the level of the study (19 studies), not the cohort-model unit.

### M5. The case-control proxy and the screening framing are not realistic as presented.
*Location:* "What does this mean for a screening programme?"; Figure 2B; SI "Consequences per 1,000 screened used a CRC prevalence of 0.5% [5]".

- **Spectrum bias.** CRC cases in these case-control studies are largely symptomatic and later-stage, so a sensitivity of 0.48-0.65 will be much lower for screen-detected, mostly stage I-II cancers. The 1,000-person figures should be presented as illustrative upper bounds.
- **The non-cancer screening population is not "controls".** At screening colonoscopy, roughly 30-40% have adenomas, about 6-10% advanced neoplasia, and many have diverticulosis, haemorrhoids or IBD, or take PPIs or metformin, all of which move microbiome scores. Two consequences follow. (a) pi_max = 0.05 is plausible for cancer but not for "samples that score like cases": advanced adenomas alone can exceed 5%. This keeps the FPR guarantee, because contamination makes the rule conservative, but it erodes sensitivity further. (b) The reported FPR is measured on case-control "controls", whereas in a programme the relevant denominator is all non-cancer participants. The paper needs a sentence defining FPR and positivity in screening terms.
- **Choice of alpha.** A 10% FPR is not realistic for CRC screening. FIT positivity is typically 4-6% at specificity around 95% (e.g., FIT in Imperiale 2014: 73.8% CRC sensitivity, 94.9% specificity; NEJM, 10.1056/NEJMoa1311194). At the realistic alpha = 0.05, the guaranteed rule abstains in 75% of units, the primary rule in 31%, and ctrl10 in 100% (Table S2). This is the regime that matters and it is relegated to the SI.
- **Missing denominators.** PPV at the rank-rule operating point is about 2.4/89.6, roughly 2.7%. Cancers detected per 1,000 (2.4 against 3.2 with the training cut-off) are in the table but not in Figure 2B or the text. A microbiome-only test at 48% sensitivity and 9% FPR would be dominated by FIT. A realistic use case is as an adjunct to FIT (Baxter 2016, already cited as [6]), and this should be said.
- **Prevalence source.** GLOBOCAN [5] gives incidence, not screening prevalence. Cite screening cohorts instead (e.g., Imperiale 2014, 0.65% CRC; Imperiale 2024 *NEJM* 10.1056/NEJMoa2310336, about 0.5%).

*Fix:* Add these caveats. Show cancers detected, cancers missed and PPV per 1,000 in Figure 2B. Move alpha = 0.05 to the main text. Frame the rule as FIT-adjunct or positivity-rate calibration.

### M6. The "lab's own unlabelled screening pool" assumption needs an operational account.
*Location:* "A RANK RULE ..." section and Conclusion.

Obtaining 360-1,500 intended-use stool samples before the first result is issued means a run-in period. During that period the test either runs in parallel with FIT, with results withheld, or results are released under the training cut-off. For a regional lab at 100 kits per week, 1,500 samples take about 4 months. Pools also age: kit lot, extraction protocol, sequencing depth and seasonal diet change. The Conclusion's one sentence ("must repeat the calibration") is insufficient.

There is also an omitted, cheaper alternative. In a FIT-based programme, FIT-negative participants (or colonoscopy-negative participants from FIT-positive referral) provide near-labelled controls, which effectively converts the problem into ctrl-n with large n. Given that ten labelled controls already beat the label-free rule (M2), the authors must argue concretely when labelled local controls are not obtainable.

*Fix:* Add a short "deployment protocol" paragraph covering run-in design, minimum pool size by alpha and delta, a re-calibration trigger such as monitoring positivity rate with a control chart (as done in the Dutch FIT programme), and the comparison with obtaining 20-50 colonoscopy-negative controls. Pool contamination by advanced adenoma should be included in the pi_max choice.

### M7. Misstatements about prior work.
*Location:* Opening paragraph.

- "Nobody has checked whether the promise holds in a new laboratory" is false. Wirbel et al. 2019 [2] set the cut-off at 10% FPR on training data and reported cross-study FPRs (their own novelty map, row 4). SIAMCAT [14] reports cross-study FPR at fixed cut-offs. CRC-TrustBench [9] and Shi et al. 2026 (bioRxiv, 10.64898/2026.08.28.747776; transferred thresholds failed in 2/3 oral-microbiome cohorts) document related failures. The Bao et al. 2026 deposit "Calibration and threshold transportability of omics classifiers across cohorts" (Zenodo 10.5281/zenodo.23236394) explicitly evaluates fixed-threshold performance across CRC metagenomic cohorts. Its accompanying manuscript must be searched for again and cited if available.
- "[M]icrobiome benchmarks still judge transfer by AUROC [9]" mischaracterises CRC-TrustBench. Its abstract states that it evaluates Platt calibration, conformal-style sets and selective abstention "without outer-test labels", and reports calibration and coverage failures. It is the opposite of an AUROC-only benchmark.
- "[R]ecent threshold-adaptation methods need labels or measured covariates at the new site [10]". SACSIM uses an *unlabelled* target sample plus "minimal auxiliary information". Measured covariates (here, taxa) are equally available to the rank rule. State the real difference: SACSIM needs a semiparametric single-index model and auxiliary information, while the rank rule is model-agnostic and score-only.
- Ref [18] (Zheng & Chen 2026) also showed that a *strictly inductive* per-sample rank normalisation preserved fixed thresholds without any pool. For compositional microbiome data, a per-sample rank/CLR transform is an obvious baseline that the authors did not test.

*Fix:* Correct these sentences, cite the Wirbel 2019 FPR results explicitly, and add a per-sample rank-normalisation baseline.

### M8. The simplest competitor is hidden from the main text and figures.
*Location:* "LABEL-FREE FIXES..." section; Figure 2A/B.

The plain local quantile of the pool (local_q; cohort-RMSE 0.046 at pi = 0.01, and *better* than the rank rule at pi = 0.20: 0.043 vs 0.059) is what any laboratory would do first. It is absent from the main text and from Figure 2. The rank rule's real incremental contribution over local_q is a finite-sample/contamination correction, worth 0.017 in RMSE. Conversely, MLLS-BCTS and two-Gaussian calibration are cited as "Figure 2A" in the text but are not plotted.

*Fix:* Show local_q in Figure 2A/B and discuss it in the text. Plot every method the text cites as "Figure 2A", or cite the SI table instead.

---

## 4. MINOR issues

1. **Title** ("...fixes it") and opening paragraph ("A simple rule fixes it") overclaim. Use "can restore, when a local pool is available".
2. **Main text, section 1** ("We trained two standard classifiers ... on eight development CRC cohorts ... We then locked 16 test cohorts"). This reads as if the CRC model is applied to IBD/T2D. The protocol actually uses leave-one-cohort-out models for IBD, T2D and adenoma. State this in the main text.
3. **"binomial test of overdispersion"** (section 1). It is a chi-square test against fixed alpha with df = 16, so it tests calibration, not overdispersion around a fitted mean. Rename it, or use df = 15 against the pooled mean. The test also ignores the sampling variability of the training threshold, which is shared across cohorts.
4. **Figure 1C** (section 1: "0.33 (two Italian studies) and 0.87 (two US studies)"). Hannigan_2017 is US/Canada, and these cohorts have about 28 controls, so binomial 95% CIs are about ±0.17. Add CIs, and label the two bars at 0.00 (they are invisible).
5. **Figure 1A.** The legend overlaps data points (adenoma FengQ / CRC YuJ rows). "target 10%" collides with the x-axis. Colour or facet by disease, and show the AUROC next to each cohort.
6. **Figure 1B.** Colour points by task. The near-chance cluster (AUROC < 0.65) should be visually distinct (see M4).
7. **Figure 2A.** The ctrl10 and rank-rule lines overlap and cannot be told apart. Add per-deployment intervals. The x-axis treats 0/1/5/20% as equally spaced. Note that 0% and 1% are effectively identical (M3).
8. **Figure 2B.** "Mixture fit" is ambiguous: it is shift2 (304), not the two-Gaussian method (300). State "3 external CRC cohorts, mean of LASSO and RF". Add cancers detected/missed (see M5).
9. **Figure 2C.** This is an analytic calculation (alpha = 0.10, slack 0.02), not data. Say so in the legend. The categorical x-axis with uneven steps (0, 1, 2, 5, 10%) exaggerates the jump at 10%. The text quotes only delta = 0.10, but both curves are plotted.
10. **Section 3, "In the smallest cohort (six controls in the pool) the rule abstained"**. Abstention is scored as FPR = 0 in the RMSE (SI Table S2 note). This rewards abstention in the primary metric. Report abstention separately and compute the RMSE over non-abstaining units.
11. **Section 3, "Results were similar ... all four diseases"**. Table S2 shows a rank-rule cohort-RMSE of 0.055 for IBD, against 0.009-0.019 elsewhere, which is driven by HallAB abstention. Qualify the claim.
12. **SI, ties.** LASSO gives many tied scores (zero selected species). The ">= t" convention makes the rule conservative but may cause large sensitivity loss. Report how often ties occur at t.
13. **SI, "Development exploration"**. The dev round 4B cross-study stress test is the only non-exchangeable evidence (M2) and should be reported in the SI with numbers.
14. **Reference 16** (Alexandari et al.). Cite the proceedings version (PMLR 119:222-232, 2020) rather than only the arXiv DOI.
15. **Reference 17** (Brummer & Garcia-Romero 2014). Add pages 1680-1684.
16. **Reference 12** (Wang & Le Cao). Verified, *Brief Bioinform* 21:1954-1970 (online 2019). Write "Lê Cao".
17. **Reference 5.** GLOBOCAN 2020 is correct for the "1.9 million" statement, but not as the source for 0.5% screening prevalence (see M5). GLOBOCAN 2022 (Bray et al. 2024) is now available.
18. **Speaker-verification lineage** (ref 17). Cite the closer generative-calibration work the authors themselves flagged: Cumani 2021 *IEEE/ACM TASLP* 10.1109/taslp.2020.3040103, which handles low target proportion, and Auckenthaler 2000 Z-norm, 10.1006/dspr.1999.0360. Their own mixture-fit failure at low prevalence echoes this literature.
19. **Microbiome batch correction.** The only microbiome-specific methods discussed are cited as reviews [11, 12]. Cite Gibbons et al. 2018 percentile normalisation to local controls (10.1371/journal.pcbi.1006102), which is the labelled analogue of the local-control rule, and DEBIAS-M (Austin et al. 2025, 10.1038/s41564-025-01954-4), which works on unlabelled target studies. Either test one of them or explain why feature-level correction is out of scope.
20. **Data/code placeholders** ([[GitHub URL]]) and author contributions must be completed. Deposit a DOI-versioned archive.
21. **Language.** Avoid "the honest answer" and "keeps the promise" in a scientific Letter. Use "abstains when the pool is too small to guarantee the target".

---

## 5. Reference verification (Crossref, checked 2026-11-25)

All 20 DOIs resolve and match the cited title, journal, volume and pages. Exceptions and description problems:

| Ref | Status | Comment |
|---|---|---|
| 1-8, 11, 13-15, 19, 20 | Verified | Correct metadata |
| 9 CRC-TrustBench (Zhang 2026, Front Microbiol 17:1971707) | Real | **Mischaracterised**: it is not an AUROC-only benchmark (M7) |
| 10 SACSIM (Qiu, Zhao, Zheng 2026, Biometrics 82:ujag138) | Real | Description inaccurate: it uses an *unlabelled* target sample plus auxiliary information (M7) |
| 12 Wang & Lê Cao | Real | Volume 21 (2020), published online 2019; accent missing |
| 16 Alexandari (arXiv 1901.06852) | Real (DataCite) | Cite the PMLR proceedings |
| 17 Brummer & Garcia-Romero ICASSP 2014 | Real | Add pages 1680-1684 |
| 18 Zheng & Chen 2026, PLoS One 21:e0357585 | Real | Accurate, but omits that inductive per-sample rank normalisation also worked |

No fabricated references were found.

## 6. Assessment of the authors' own novelty search

The log (journal_selection/novelty_search_log.md) is careful and frank about the *abandoned* mixture method. It scores method novelty at 2/5 and recommends not claiming the estimator. It has three weaknesses:
1. It was not repeated after the pivot to the rank rule. The final contribution's nearest neighbours (NP with label noise, contaminated conformal reference sets, indirect reference intervals, FIT positivity-rate cut-offs) were never queried.
2. Several items the log flags as "must cite" did not reach the manuscript: Wirbel 2019 FPR results (cited, but contradicted by "Nobody has checked"), Tong 2018, Bao 2026, Shi 2026, Gibbons 2018, DEBIAS-M, DyS, Cumani 2021/2023, Guo 2008.
3. It relied only on OpenAlex, Crossref, arXiv and PubMed title/abstract search, with no Google Scholar or citation chasing. Its "PubMed 0 hits" for unlabelled threshold adaptation is therefore weak evidence of absence. My own search also found CrcBiomeScreen (Li et al. 2026, Research Square, 10.21203/rs.3.rs-10488713/v1), a CRC microbiome workflow developed on a **real-world screening cohort of 2,252 samples** with cross-cohort testing in nine cohorts. Such screening-cohort data would directly address the case-control-proxy limitation (M5).

## 7. Missed prior work (DOIs verified via Crossref, OpenAlex or DataCite)

**Order-statistic / NP / conformal thresholds with contaminated class-0 data (closest to the proposed rule)**
- Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. *Sci Adv* 2018. 10.1126/sciadv.aao1659
- Yao S, Rava B, Tong X, James G. Asymmetric error control under imperfect supervision: a label-noise-adjusted Neyman-Pearson umbrella algorithm. *JASA* 2022/2023. 10.1080/01621459.2021.2016423
- Bashari M, Sesia M, Romano Y. Robust conformal outlier detection under contaminated reference data. ICML 2025. 10.48550/arxiv.2502.04807
- Einbinder B-S, et al. Label noise robustness of conformal prediction. 2022 (JMLR 2024). 10.48550/arxiv.2209.14295

**Laboratory-medicine analogues (local decision limits from unlabelled routine samples)**
- Jones GRD, Haeckel R, Loh TP, et al. Indirect methods for reference interval determination: review and recommendations. *Clin Chem Lab Med* 2018. 10.1515/cclm-2018-0073
- Ammer T, et al. refineR: a novel algorithm for reference interval estimation from real-world data. *Sci Rep* 2021. 10.1038/s41598-021-95301-2

**CRC screening cut-off practice and realistic screening parameters**
- Toes-Zoutendijk E, et al. Real-time monitoring of results during first year of Dutch colorectal cancer screening program and optimization by altering FIT cut-off levels. *Gastroenterology* 2017. 10.1053/j.gastro.2016.11.022
- Brenner H, Werner S. Selecting a cut-off for colorectal cancer screening with a fecal immunochemical test. *Clin Transl Gastroenterol* 2017. 10.1038/ctg.2017.37
- Imperiale TF, et al. Multitarget stool DNA testing for colorectal-cancer screening. *NEJM* 2014. 10.1056/NEJMoa1311194
- Imperiale TF, et al. Next-generation multitarget stool DNA test for colorectal cancer screening. *NEJM* 2024. 10.1056/NEJMoa2310336

**Microbiome threshold/calibration transport and batch correction (flagged in the authors' own map but not cited)**
- Bao X, et al. Calibration and threshold transportability of omics classifiers across cohorts: code and reproduction materials. Zenodo 2026. 10.5281/zenodo.23236394 (re-search for the manuscript)
- Shi et al. Cross-cohort oral microbiome meta-analysis ... limits of OSCC classifier transportability. bioRxiv 2026. 10.64898/2026.08.28.747776
- Li C, et al. CrcBiomeScreen: a reproducible workflow for class imbalance and cross-cohort generalisability in colorectal cancer microbiome prediction. Research Square 2026. 10.21203/rs.3.rs-10488713/v1
- Gibbons SM, Duvallet C, Alm EJ. Correcting for batch effects in case-control microbiome studies. *PLoS Comput Biol* 2018. 10.1371/journal.pcbi.1006102
- Austin GI, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. *Nat Microbiol* 2025. 10.1038/s41564-025-01954-4

**Unsupervised score calibration and quantification (for the negative-results section)**
- Cumani S. On the distribution of speaker verification scores: generative models for unsupervised calibration. *IEEE/ACM TASLP* 2021. 10.1109/taslp.2020.3040103
- Auckenthaler R, Carey M, Lloyd-Thomas H. Score normalization for text-independent speaker verification systems. *Digit Signal Process* 2000. 10.1006/dspr.1999.0360
- Maletzke A, et al. DyS: a framework for mixture models in quantification. AAAI 2019. 10.1609/aaai.v33i01.33014552
