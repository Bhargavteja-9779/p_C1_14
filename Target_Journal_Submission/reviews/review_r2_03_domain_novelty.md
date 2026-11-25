# Referee report R2-03: domain, novelty and clinical realism (round 2)

**Manuscript:** "The decision threshold of a stool-metagenome classifier must be set at each site, on that site's own samples" (iMeta Letter, draft v0.3, 2026-11-25)
**Reviewer expertise:** microbiome diagnostics, metagenomic machine learning, clinical prediction-model updating, label-shift and conformal methods, CRC screening
**Material examined:** manuscript.md, supporting_information.md, Figure1.png, Figure2.png, results/main_tables.md, results/posthoc_r1_tables.md, journal_selection/novelty_map.csv, journal_selection/novelty_search_log.md, code/experiments/protocol.md, code/src/models.py (feature-standardisation baseline), round-1 report R1-03 and the response. All 27 reference DOIs were checked against Crossref (arXiv DOIs against OpenAlex/arXiv). I ran new searches (web, Crossref, OpenAlex) for 2024-2026 work.

---

## 1. Summary of the submission

The authors take LASSO and random-forest classifiers built on species profiles from curatedMetagenomicData. They set the cut-off at 90% specificity on out-of-fold training scores and score 16 cohort-task pairs that were held back (3 external CRC cohorts and the IBD, T2D and adenoma cohorts, the last three by leave-one-cohort-out). They report four findings:

1. The realised FPR of the training cut-off ranges from 0 to 0.74 and is not predicted by AUROC.
2. Four published label-free methods and one method of the authors' own (EM, MLLS-BCTS, two-Gaussian unsupervised calibration, per-site feature standardisation and a location-scale mixture) do not repair the cut-off.
3. A contamination-padded order statistic on an unlabelled pool from the same cohort meets the target (cohort-RMSE 0.031 vs 0.185). The authors say plainly that the rule is not new.
4. Post hoc, a pool from another centre of MetaCardis or from another cohort does not meet the target.

The revision is much more candid than v0.2. The rule is now credited to Wilks, Neyman-Pearson umbrella and contamination-robust conformal work. The deviations are disclosed, and the cross-site experiments that round 1 asked for were run. This makes the manuscript more honest, but it also leaves less to publish. The paper is now a cautionary empirical note: a known rule works when exchangeability holds by construction, and fails when it does not.

## 2. Recommendation

**Major revision. As framed, the contribution falls below iMeta's bar for novelty and impact.** If the authors cannot address Major issues 1-4 with new evidence, I would recommend rejection with an invitation to submit a methods-and-practice note to a more specialised venue.

Reasons:
- The rule is classical and the authors concede it.
- The negative finding about label-shift methods follows from their known assumptions.
- The single new, actionable claim ("the pool must come from the same centre") rests on one study with three centres and 12 pool-target-model combinations. The training cut-off performed as well as the cross-centre pool in that study, which the main text does not say.
- The step that matters in practice, a pool collected now and applied to later samples, is not tested at all.
- Closely related 2025-2026 work on label-free threshold alignment is not cited (Section 5).

---

## 3. MAJOR issues

### M1. Novelty: the contribution as framed is thin, and the central "same-site" claim has narrow support

- **Location:** Title; Highlights 3; "THE SAMPLES MUST COME FROM THE SAME SITE"; Conclusion.
- **Problem, by component:**
  - **(a) Training cut-offs fail.** This is expected from the clinical prediction-model literature, which the authors themselves cite [8, 9]. It has been shown for omics classifiers [17] and for microbiome CRC classifiers in CRC-TrustBench [10]: under leave-one-country-out, conformal coverage there fell below the 90% and 95% targets, and Platt calibration was evaluated without outer-test labels. Wirbel et al. [2] already showed specificity varying across cohorts at a fixed cut-off.
  - **(b) Label-shift methods fail when class-conditional score distributions move.** This follows from their stated assumption. It is a useful check, not a finding.
  - **(c) The rank rule works in random halves of the same cohort.** This holds by construction (Note S1). The locked experiment is essentially a finite-sample check of a theorem.
  - **(d) The pool must come from the same centre.** This is the only claim that is new and has practical consequences. It rests on E5: one study (MetaCardis), three centres that are also three countries, T2D only, six ordered off-diagonal pairs × 2 models.

  The title and Conclusion ("The cut-off ... belongs to the site that runs it"; "not to the study or the country") generalise far beyond that evidence. MetaCardis centre is confounded with country, recruitment pathway and medication patterns, so "population" and "laboratory process" cannot be separated. That is a problem, because the main text says the cut-off belongs to "the population and the laboratory process together".
- **Fix:**
  - Reframe the title and Conclusion as a conditional result: "a local unlabelled pool restores the intended FPR when it is exchangeable with the tested population; pools from other cohorts or centres did not".
  - Add at least one more multi-centre or multi-batch dataset in which population and processing can be separated. Candidates: cohorts sequenced in several batches, or the multi-centre CRC collections in Piccinno et al. 2025.
  - State the E5 sample size (pairs × models) in the main text.

### M2. The comparison that matters in deployment, a pool collected earlier and applied later, is missing

- **Location:** "A RANK RULE ON THE SITE'S OWN SAMPLES"; Conclusion ("repeated when the population or laboratory process changes"); Limitations.
- **Problem:** Every locked pool is a random half of the evaluation cohort, so pool and target are exchangeable by design. A laboratory, however, calibrates on its first n samples and then tests for months or years. Kit lots, extraction batches, sequencer runs, reference databases (MetaPhlAn version) and seasonal or demographic intake all drift.

  The manuscript's own evidence suggests that small departures from exchangeability are enough to break the rule. Moving between MetaCardis centres, with the same protocol and sequencer, raised the error from 0.009 to 0.067. A temporal split within a site could well do the same. Without a temporal or batch-wise split, the headline result (RMSE 0.031) is an upper bound on real-world performance, not an estimate of it. The highlight "kept the intended rate" overstates what was shown.
- **Fix:**
  - Run a time-ordered or batch-ordered split wherever collection dates or sequencing batches are available. Several cMD cohorts and the MetaCardis metadata may allow this, and other public data with run or date metadata could serve.
  - If no such data exist, state in the Highlights and Conclusion that the rule was validated only under random within-cohort splits.
  - Give a concrete monitoring rule for recalibration (for example, a positivity-rate control chart of the kind FIT programmes already run [7]).

### M3. Clinical realism: the "almost every sample is healthy" premise holds for CRC screening only, yet 13 of 16 locked cohorts are IBD, T2D or adenoma

- **Location:** Introduction; first paragraph of "A RANK RULE ..."; Table S2 by disease; Figure 1A.
- **Problems:**
  - **(a) IBD.** Microbiome or calprotectin testing is used in symptomatic referral populations, where IBD prevalence is roughly 5-30%, not in population screening.
  - **(b) T2D.** Prevalence in adults is about 10%, and HbA1c/glucose are cheap and definitive. No one would screen with a stool metagenome.
  - **(c) Adenoma.** In a screening population, any adenoma is found in 25-40% of colonoscopies and advanced adenoma in about 5-10%. This sits at or above the assumed π_max = 5%. If adenoma is the target condition, as in the adenoma task, the pool assumption is violated by design.
  - **(d) Weak classifiers.** For the T2D and adenoma tasks the classifiers have AUROC 0.54-0.69, and mean sensitivity at 10% FPR is around 0.25 across all units (Table S2, rpoolmean 0.249). Restoring the FPR of a near-random classifier has little clinical value. Including these tasks inflates the "16 cohorts" evidence base for a CRC-screening argument.
  - **(e) Case-control controls.** These are mostly colonoscopy-negative "healthy" people. In screening, a "false positive" means a positive test without advanced neoplasia, a group that includes non-advanced adenomas, hyperplastic polyps, haemorrhoids, diverticular disease and medication users (PPIs, metformin, antibiotics). The realised FPR in case-control controls is therefore not the screening FPR, and the pool controls of a real screening population will differ from the controls used here.
- **Fix:**
  - Restrict the screening-prevalence argument and the per-1,000 numbers to CRC.
  - Present IBD and T2D as stress tests of threshold transport, not as screening use cases. Either justify a realistic deployment setting for each or drop them from the primary endpoint.
  - For adenoma, re-run with π_max matched to screening adenoma prevalence (≥ 10-30%) or remove it from the rank-rule claims.
  - Validate in at least one cohort recruited from a screening or FIT-positive population. CrcBiomeScreen reports 2,252 microbiome samples from a real-world CRC screening cohort, and screening-recruited cohorts exist within cMD (e.g., YachidaS_2019 is colonoscopy-recruited). If none can be accessed, state this as the principal limitation in the Highlights.

### M4. The per-site feature-standardisation baseline was implemented in a way that makes it fail

- **Location:** "LABEL-FREE FIXES ..." paragraph; SI Methods "Per-site feature standardisation [17]"; `code/src/models.py`, `train_and_score_featstd`.
- **Problem:**
  - Each training cohort is standardised with the mean and SD of *all* its samples, which are roughly half cases. The target is standardised with the mean and SD of the unlabelled pool, which at π = 0 contains only controls. A target control therefore sits further from the "average" sample after standardisation than a training control does, and the FPR is pushed upward (mean FPR 0.23 vs target 0.10). The manuscript's explanation, that pools and case-control studies "hold different shares of patients", describes a mismatch the authors built into the baseline.
  - The fair analogue is control-referenced standardisation: training cohorts standardised on their controls, as in the percentile normalisation of Gibbons et al. [18]. Zheng et al. [17] found sample-wise rank normalisation (a strictly inductive transform needing no target statistics) to be the most robust option. It was not tested.
  - The statement that four of five methods "made it worse" depends partly on this baseline (featstd 0.203 vs source 0.185).
- **Fix:**
  - Add (i) control-referenced per-site standardisation (training standardised on controls, target on the pool with the same π_max contamination) and (ii) sample-wise rank or CLR-based normalisation with a fixed training cut-off.
  - Label these runs as post hoc.
  - Revise the "four made it worse" claim to match the results.

### M5. Factual error in the Highlights: the "five published methods" include the authors' own mixture fit

- **Location:** Highlights bullet 2 ("Five published label-free adaptation methods"); main text "We therefore tested published methods ... a location-scale mixture fit"; SI Methods ("Location-scale mixture fit (ours, development)").
- **Problem:** The location-scale mixture is the authors' development-stage method, by the SI's own description, and has no citation. It is also the only method that beat the training cut-off.
- **Fix:** Write "four published methods and one location-scale mixture fit of our own". Also say that this was the method the authors originally designed and then abandoned (the novelty log shows this), because that history is relevant to how the comparison should be read.

### M6. E5 is reported without its key comparator, and the result cuts against the headline message

- **Location:** "THE SAMPLES MUST COME FROM THE SAME SITE"; Figure 2B; Table S4 E5.
- **Problem:**
  - In MetaCardis, the training cut-off had realised FPR 0.005-0.088 at every centre (Table S4, `source` column), so it never exceeded the target. Its RMSE (0.072) is almost the same as that of the cross-centre pool (0.067).
  - The cross-centre pool produced FPRs up to 0.24. Here a "local" recalibration done with the wrong local samples was *more dangerous* than doing nothing.
  - The main text gives the training-cut-off comparison for E3 (0.173) but omits it for E5.
- **Fix:** Report the E5 training-cut-off RMSE and maximum FPR in the main text. Discuss the asymmetry: a conservative training cut-off loses sensitivity, while a miscalibrated borrowed pool raises the FPR. This finding is clinically useful and currently hidden.

### M7. Missed directly relevant prior work; the gap statement is overstated

- **Location:** Introduction, final sentence ("it is not known whether a laboratory can restore an intended FPR without new diagnoses, nor where the samples for doing so must come from").
- **Problem:**
  - **Gal et al., ICLR 2025.** This paper addresses exactly "decision threshold setting" across hospital sites using unlabelled target samples, on multi-site eICU EHR data.
  - **Kalan et al. (arXiv 2025; ICLR 2026 poster).** This paper treats Neyman-Pearson classification when the null (control) distribution shifts. That is the mechanism the authors say defeats label-shift methods.
  - **Si et al., ICLR 2024.** PAC prediction sets under label shift.
  - **Indirect reference-interval methods** (refineR, kosmic). These are the operational analogue in laboratory medicine and are validated algorithms, not merely "the same spirit". Ref. [24] is a review; the actual algorithms should be cited and arguably compared.
  - **FIT programmes.** These already set and re-set cut-offs from the observed positivity in their own population [7]. A programme-level positivity target is itself a rank rule.

  Several of these papers are listed in the authors' own novelty map (Kalan 2026, Scott 2019, Podkopaev 2021, Popordanoska 2024 LaSCal, Ziegler 2019) but are not cited. The statement that "newer label-shift estimators" were not tested should name them.
- **Fix:**
  - Cite and briefly position against Gal 2025, Kalan 2025/2026, Si 2024, refineR, and the FIT positivity-targeting practice.
  - Soften the gap statement to the microbiome-specific empirical question.
  - Ideally add refineR-style deconvolution of the healthy component as a baseline. Its assumption, a majority of non-pathological results, is the same as the rank rule's.

---

## 4. MINOR issues

1. **Description of training (main text, para 3).** "We trained ... on eight development CRC cohorts" is true only for the CRC task. IBD, T2D and adenoma used leave-one-cohort-out among the locked cohorts of the same task (protocol.md). State this; at present the reader may think a CRC model was applied to T2D.
2. **"Pre-registered" wording.** The protocol is an internal commit dated 2026-11-24, one day before this draft, not a public registration (OSF, ClinicalTrials, etc.). Use "frozen analysis protocol committed before scoring the locked cohorts" and give the commit hash.
3. **Abstention counted as FPR 0 (Figure 2A, Table S2).** This makes the strict rule look excellent ("1%" above 15%) while it abstains in 50% of units (75% at α = 0.05). Show the abstention share next to each box in Fig. 2A, as is done in the text, and give an abstention-excluded summary.
4. **Figure 2C composition changes along the x-axis.** QinJ_2012 contributes only up to n = 100 and YachidaS_2019 up to n = 200 (Table S4 per-cohort table). Different pool sizes therefore average different cohorts. Plot per-cohort lines or restrict to sizes available in all cohorts. The caption says "three cohorts", but posthoc code says "four large cohorts" (Yachida CRC and adenoma share controls); harmonise.
5. **Figure 2B mixes sources.** The "same/other centre" rows are MetaCardis T2D only, while the "other cohort" row covers all tasks. Add n per row and a visual separator, or split into two panels. The training-cut-off points in the "same centre" row are all below target. Make that visible in the caption (see M6).
6. **Figure 1A.** Many units sit at FPR ≈ 0 (RF in adenoma and T2D), so failure runs in both directions. Say so in the text ("from over-conservative to 7× the target"). Over-conservative cut-offs cost sensitivity and are also a transport failure.
7. **Figure 1C** shows only failing methods. Add the pool quantile and rank rule as reference lines so readers can see the scale of the improvement in one figure. Panel B lacks its own model legend.
8. **Sensitivity context (practice paragraph).** At 10% FPR the rank rule gave CRC sensitivity 0.48, measured on mostly diagnosed, often symptomatic cancers. FIT achieves about 74% CRC sensitivity at about 95% specificity (Imperiale 2014 [6]), and next-generation mt-sDNA reaches about 94% at about 91% specificity for advanced neoplasia (Imperiale 2024, NEJM). Say explicitly that a stand-alone metagenomic test at this operating point is not competitive. The realistic use case is as a FIT adjunct or triage among FIT-positives, which changes both prevalence and the pool composition.
9. **"Stool tests are being developed for CRC screening [5, 6]."** mt-sDNA (ref. 6) has been approved and in use since 2014. Ref. 5 (Baxter 2016) is 16S-based and combined with FIT. Rephrase as "stool DNA tests are in use, and microbiome-based tests are being developed".
10. **Per-1,000 arithmetic.** "Sent 199 healthy people" uses 995 × FPR. Say "false-positive referrals among 995 people without cancer" so that true-positive referrals are not conflated. The table column is labelled "colonoscopies_per_1000" (202) and includes true positives.
11. **Regulatory and equity implications are not discussed.** A rank-based local cut-off makes an individual's result depend on who else was in the calibration pool. In IVDR/FDA terms, changing a cut-off is a device modification requiring re-verification. Fixing positivity per site also gives the same referral rate to populations with different underlying risk. One or two sentences are needed in a paper whose message is "set the cut-off at each site".
12. **Pool logistics.** State how the first 360-610 samples are handled. Are results withheld until the pool is complete, or are early samples re-reported? Who pays for sequencing a calibration run? How are confirmed cases removed retrospectively? In a centralised commercial laboratory, which is the realistic model for metagenomic tests, "site" means "served population", and E5 implies population-specific cut-offs. Say this explicitly.
13. **MetaCardis controls and confounding.** MetaCardis T2D cases are often metformin-treated, and control recruitment differed by country. Report the n of controls per centre in E5 and note recruitment differences.
14. **Reference 27** (Angelopoulos & Bates) is listed in the main reference list but cited only in the SI. Either cite it in the main text (the ten-labelled-controls rule) or move it to an SI reference list.
15. **Reference 10 (CRC-TrustBench) is undersold.** It explicitly evaluated label-free calibration (Platt), conformal-style sets and abstention under leave-one-study-out and leave-one-country-out, and found coverage below target. Describe it as such; it is the closest microbiome precedent.
16. **Reference 17 (Zheng 2026).** Its best-performing approach was sample-wise rank normalisation, with robust external-cohort scaling performing similarly. "Per-site feature standardisation ... recently reported to rescue fixed cut-offs" is accurate only for the second, which is what was tested here, and in a different form (M4).
17. **Reference 13 (SIAMCAT)** is cited for setting the cut-off at 90% specificity on out-of-fold scores. Wirbel 2019 [2] is the more direct precedent for the 90%-specificity operating point in CRC metagenomics; cite it here too.
18. **Highlights bullet 1.** "16 locked test cohorts" should be "16 cohort-task pairs from 14 studies" (the Yachida controls are used twice, and four adenoma cohorts share controls with development cohorts).
19. **Equivalence margin (±0.02).** Where was this margin specified? If it was not in protocol.md, label the TOST as post hoc in the main text.
20. **Reference metadata (Crossref-verified).** All 27 DOIs resolve to the stated works. Small corrections:
    - Ref. 22 (Yao et al.) was published online in 2022; the print issue is 2023;118(543):1824-1836, as given. OK.
    - Ref. 8 lists the STRATOS group as a corporate author on Crossref; optional.
    - Ref. 15: arXiv preprint year 2019, ICML 2020 proceedings, PMLR 119. OK.
    - Ref. 23: verify that the ICML 2025 proceedings citation (PMLR volume and pages) exists; only the arXiv DOI was verifiable.

---

## 5. Missed or misdescribed prior work (DOIs verified via Crossref/OpenAlex unless noted)

| Work | DOI / ID | Relevance |
|---|---|---|
| Gal E, Thakur A, Molaei S, Soltan AAS, Clifton DA. Leveraging shared feature representation in cross-domain alignment of decision thresholds for EHR data. ICLR 2025 | OpenReview id oqHWR27vnt (no DOI) | Label-free threshold alignment across hospital sites using unlabelled target samples; the closest clinical-ML precedent. Not cited, and not in the novelty map |
| Kalan MM, Deng Y, Neugut EJ, Kpotufe S. Neyman-Pearson classification under both null and alternative distributions shift. arXiv 2025 / ICLR 2026 | 10.48550/arXiv.2511.06641 | NP transfer when the control distribution shifts: the mechanism that breaks label-shift methods here. In the novelty map but not cited |
| Scott C. A generalized Neyman-Pearson criterion for optimal domain adaptation. ALT 2019 | 10.48550/arXiv.1810.01545 | NP with an unlabelled target sample; immune to target shift. In the map, not cited |
| Si W, Park S, Lee I, Dobriban E, Bastani O. PAC prediction sets under label shift. ICLR 2024 | 10.48550/arXiv.2310.12964 | Conformal/PAC guarantees under prior shift; relevant to the "strict" version |
| Podkopaev A, Ramdas A. Distribution-free uncertainty quantification for classification under label shift. UAI 2021 | 10.48550/arXiv.2103.03323 | Same; in the map, not cited |
| Popordanoska T et al. LaSCal: label-shift calibration without target labels. NeurIPS 2024 | 10.52202/079017-2088 (from novelty map; not re-verified) | A "newer label-shift estimator" the Limitations allude to; name it |
| Ammer T, Schützenmeister A, Prokosch HU, et al. refineR: a novel algorithm for reference interval estimation from real-world data. Sci Rep 2021;11:16023 | 10.1038/s41598-021-95301-2 | Validated algorithm for estimating the healthy distribution from unlabelled routine samples; the operational analogue of the rank rule and a natural baseline |
| Selby K, Levine EH, Doan C, et al. Effect of sex, age, and positivity threshold on FIT accuracy: systematic review and meta-analysis. Gastroenterology 2019;157:1494-1505 | 10.1053/j.gastro.2019.08.023 | Evidence that stool-test cut-offs are already set per programme and subgroup; context for "site-specific" cut-offs |
| Imperiale TF, Porter K, Zella J, et al. Next-generation multitarget stool DNA test for colorectal cancer screening. N Engl J Med 2024;390:984-993 | 10.1056/NEJMoa2310336 | Current benchmark operating point for stool-based CRC screening (sensitivity and specificity); needed for clinical context |
| Piccinno G, Thompson KN, Manghi P, et al. Pooled analysis of 3,741 stool metagenomes from 18 cohorts ... colorectal cancer. Nat Med 2025;31:2416-2429 | 10.1038/s41591-025-03693-9 | Largest current cross-cohort CRC metagenome analysis (LODO AUC ~0.78-0.85); should replace or supplement the 2019 references as the state of the art, and offers more multi-centre data for M1 |
| CrcBiomeScreen: a reproducible workflow for class imbalance and cross-cohort generalisability in CRC microbiome prediction. Research Square 2026 (preprint) | 10.21203/rs.3.rs-10488713/v1 | Uses a 2,252-sample real-world CRC screening cohort, the kind of data needed for M3 |
| Flores GA, Smith AH, Fukuyama JA, Wilson AC. Aligning evaluation with clinical priorities: calibration, label shift, and error costs. NeurIPS 2025 | 10.48550/arXiv.2506.14540 | Threshold and calibration evaluation under prevalence uncertainty; optional |
| Zhang K, Schölkopf B, Muandet K, Wang Z. Domain adaptation under target and conditional shift. ICML 2013 (PMLR 28:819-827) | no DOI (PMLR) | Formalises the "healthy scores moved and prevalence changed" case that the authors describe informally |

Misdescribed or undersold (see Minor 15-17): ref. 10 (CRC-TrustBench), ref. 17 (Zheng 2026), ref. 24 (indirect reference-interval methods are validated algorithms, not only a "spirit"). The Highlights misdescribe the authors' own mixture fit as a published method (M5).

The "Bao 2026, Calibration and threshold transportability of omics classifiers across cohorts" Zenodo deposit (10.5281/zenodo.23236394), flagged in the authors' own watch list, still has no findable manuscript in Crossref/OpenAlex as of 2026-11-25. It should be re-checked before submission.

---

## 6. Do the conclusions follow from the evidence?

| Claim | Supported? |
|---|---|
| Training cut-offs do not transfer; AUROC does not reveal it | Yes. Strong overdispersion evidence, two models, 16 cohort-task pairs |
| Label-free ML fixes do not repair it | Partly. Yes for EM/MLLS/two-Gaussian; the feature-standardisation baseline is unfair (M4), and "five published" is wrong (M5) |
| The rank rule on the site's own samples keeps the intended rate | Only under random within-cohort splits (exchangeable by design); not tested over time or batch (M2); small pools; abstention flatters the strict version |
| The pool must come from the same centre/site | Suggestive, from one study, three confounded centres, T2D only; the training cut-off did equally well there (M1, M6) |
| Deployment protocols should include a local calibration run | Reasonable, but the pool logistics, regulatory and equity aspects are not addressed (Minor 11-12) |

Overall the revision is honest and technically careful. To reach iMeta, the paper needs either (i) evidence on the deployment-relevant question (temporal or batch exchangeability, a screening-recruited cohort, additional multi-centre data that separates population from processing) or (ii) a substantially reframed, narrower claim focused on CRC.
