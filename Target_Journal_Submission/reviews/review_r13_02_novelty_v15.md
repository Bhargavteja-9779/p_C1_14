# Referee report, round 13: Reviewer 2 (novelty and related work)

**Manuscript:** manuscript_v15.md (Letter, iMeta), with figures_v15/ and supporting_information_v15.md
**Title:** "The same gut-microbiome test flags 0–77% of healthy people, depending on the population"

**Score:** 7.5/10
**Recommendation:** Minor revision (the three MAJOR items below need text and citation changes only, with no new analysis)
**Novelty:** 21/25

---

## Summary judgement

The Letter makes three claims. I checked each against prior art with my own searches. These covered OpenAlex (about 20
phrasings, mostly limited to 2023–2026), Crossref, PubMed/PMC E-utilities (full text of GMHI, GMWI2 and Wirbel 2019) and
the arXiv export API. I also checked every DOI in the reference list on Crossref.

1. **FPR atlas (C1).** At a fixed cut-off, 28 classifiers for 14 diseases give a different FPR in each of 36 healthy
   populations (I² median 0.94). AUROC does not predict this spread (ρ = −0.06). No paper I found maps FPR at a fixed
   operating point across many healthy populations and many diseases with heterogeneity statistics. **The empirical
   contribution is novel.** The framing sentence around it is now an overclaim, however (MAJOR 2). The new
   spectrum-effect sentence says "Microbiome studies have not measured it", and the next sentence cites one that did
   ([12]). The direct microbiome precedent on regional variation, He et al. 2018 (*Nat Med*), is still not cited.
2. **GMWI2 audit (C2).** The audit shows region-specific mislabelling by GMWI2 inside its own training data (East Asian
   median 0.64 vs 0.12 elsewhere). The authors trace it to the geographic case mix of the training data (odds ratio 6.7)
   and test that cause by retraining with country × label weighting. I read the GMWI2 full text (PMC11358288). It gives
   no study-level or region-level breakdown of healthy-sample mislabelling. The only related remark is a generic
   limitation sentence about representation. **Novel, with a real mechanism.** One related-work problem remains: the
   sentence that credits earlier work ("Low health-index scores in populations that lack the training markers were
   reported before [19]") cites a paper that does not report this (MAJOR 1). The paper that did support it, Poyet 2026
   (*Cell*), was removed in v15 "to save space".
3. **Site recalibration (C3).** The authors recalibrate the cut-off at each site from an unlabelled burn-in, which cuts
   the FPR error by 62% (79% for GMWI2) within a site. The same rule fails across sites. The authors correctly say "the
   rule is not new". **Incremental but honestly framed.** Over several revisions the medical-AI work on label-free
   operating-point correction (Roschewitz 2023 UPA; Qiu 2026 SACSIM) has been cut. Of the earlier conformal/NP and
   lab-medicine citations, only lab medicine (refineR, Ozarda) remains (MAJOR 3). Roschewitz 2023 is also the closest
   published precedent for C1's "AUROC transports, the operating point does not" message.

**Were the round-12 items addressed?**

| Round-12 item | Status in v15 | Verdict |
|---|---|---|
| MAJOR 1: spectrum effect uncited | Leeflang 2013 [8] added; new framing: "Clinical epidemiology has long known … Microbiome studies have not measured it." | **Partly resolved.** The precedent is now cited. The new second sentence overclaims (MAJOR 2), and Leeflang 2013 is about variation with *prevalence*. The canonical "spectrum effect" sources would fit better (MINOR 1). |
| MINOR 1: Selby 2019 FIT precedent | Declined for length | Acceptable. |
| MINOR 2: GMHI direction-of-effect | Reworded: "Low health-index scores … were reported before [19] … we add its size … and a test by retraining." | **Wording done, citation wrong.** I read GMHI 2020 in full (PMC7492273). It does not report low scores in populations that lack the training markers (MAJOR 1). Reviewer 2 accepted this citation in round 12 without checking, and I correct that here. |
| MINOR 3: prior-shift lineage | "a split-conformal argument [20, 21] that, through π_max, is a simple prior-shift correction [22]" | Done, but the equivalence is overstated (MINOR 2). |

---

## Claim → closest prior work → exact difference

| # | Claim (v15) | Closest prior work (verified DOI) | Exact difference |
|---|---|---|---|
| C1a | A fixed cut-off (90th percentile of out-of-fold training-control scores, target FPR 0.10) gives an FPR of 0–0.77 across 36 healthy populations. I² median 0.94; prediction-interval upper bounds range from 0.22 to 0.81. | **Wirbel 2019** [1], 10.1038/s41591-019-0406-6: the *same* cut-off design ("adjusted to yield a false positive rate (FPR) of 0.1 on the controls of its respective (CRC) training set"), with realised FPR reported on other-disease cohorts (0.09–0.13; full text PMC7984229). **SIAMCAT, Wirbel 2021** [12], 10.1186/s13059-021-02306-1: external-control FPR at a 10% cut-off, with a more than twofold average excess. **He 2018**, 10.1038/s41591-018-0164-x (uncited): disease models and healthy reference ranges do not transfer between 14 districts of one province. **Poyet 2026**, 10.1016/j.cell.2026.10.016 (dropped in v15): predictors trained on industrialised populations are uninformative in less-industrialised cohorts. | Earlier microbiome work measured fixed-cut-off FPR on a few external or other-disease sets (Wirbel 2019, SIAMCAT). It showed loss of transfer geographically (He 2018, Poyet 2026), but as AUROC or model failure, not per-population FPR. **New:** a systematic per-population FPR map for 14 diseases in 36 healthy general populations. It adds I², prediction intervals, a variance decomposition (pair 48%) and an overdispersion test. The cut-off design itself comes from Wirbel 2019, which the manuscript does not acknowledge (MAJOR 2). |
| C1b | AUROC does not predict FPR portability (ρ = −0.06): "A better classifier was not a more portable one." | **Roschewitz 2023**, 10.1038/s41467-023-42396-y (cited in v5–v9, now dropped): sensitivity and specificity drift under acquisition shift "even for models that generalise in terms of AUROC". **Cirolia 2026** (bioRxiv), 10.64898/2026.05.21.727052: IBD classifier performance depends mostly on the evaluation study. | The general point is anticipated in medical imaging. **New:** the quantitative demonstration across 28 microbiome classifiers that discrimination and operating-point portability are uncorrelated. |
| C1c | Specificity depends on the population of use (spectrum effect). | **Leeflang 2013** [8], 10.1503/cmaj.121286; **Usher-Smith 2016**, 10.1136/bmj.i3139; **Mulherin & Miller 2002**, 10.7326/0003-4819-137-7-200210010-00011; **Murad 2023**, 10.1503/cmaj.221802 (6,909 diagnostic-accuracy studies: specificity falls as prevalence rises). | Conceptually established. C1 is its first large microbiome-specific measurement, and v15 now frames it that way. |
| C2a | GMWI2 labels 0–84% of healthy training samples as non-healthy, depending on the study; East Asian median 0.64 vs 0.12 (P = 5 × 10⁻⁷). Unseen East Asian populations: 0.38 vs 0.06. | **GMWI2, Chang 2024** [16], 10.1038/s41467-024-51651-9: reports pooled balanced accuracy only. Its limitations say "future work should emphasize wider participant inclusion". **GMHI, Gupta 2020** [19], 10.1038/s41467-020-18476-8: generic remark that "complete elimination of biases is practically impossible". **Poyet 2026**: cross-population failure of industrialised-trained predictors. | No prior paper audits a released health index for region-specific mislabelling inside its own training scores. **New and clearly differentiated.** |
| C2b | Mechanism: East Asian samples make up 62% of non-healthy vs 20% of healthy training samples (OR 6.7). Country × label reweighting cuts the gap by 88% (CI 41–149%); within-country label balance alone cuts 37%. | **SIAMCAT** [12]: country confounding can inflate cross-study performance. **Abdill 2022**, 10.1371/journal.pbio.3001536 (uncited): public microbiome data are geographically skewed. **Hehemann 2010** [18]: *B. plebeius* porphyranase acquired in Japanese guts. | Confounding by study or country is a known risk. **New:** its size for a deployed index, and a pre-specified causal test by retraining that is honestly reported with a CI crossing the criterion and a failed AUROC hypothesis. |
| C3 | Label-free burn-in k = ⌈(N + 1)(1 − α(1 − π_max))⌉. Cuts FPR error by 62% within a site under non-random splits, fails across sites, costs sensitivity (0.46 → 0.21–0.23). Released as `fprcal`. | Split-conformal / conformal p-values [20, 21]; NP umbrella [23]; prior shift [22]; indirect reference intervals [14, 24]. **Roschewitz 2023 UPA** and **Qiu 2026 SACSIM**, 10.1093/biomtc/ujag138: label-free, site-local operating-point correction in medical AI and NP classification (both dropped since v9). **CRC-TrustBench** [13], 10.3389/fmicb.2026.1971707: label-free calibration and conformal sets for CRC metagenomic models, with under-coverage. | Method not new, as the manuscript states. **New (incremental):** a microbiome map of where label-free local recalibration works (within a site, including non-random splits) and where it breaks (across city or country), with its sensitivity cost and a tool. |

---

## Concerns

### MAJOR

**MAJOR 1: Ref [19] is cited for a finding it does not contain, and the paper that contained it was removed.**
The C2 paragraph says: "Low health-index scores in populations that lack the training markers were reported before
[19]". Ref [19] is Gupta 2020 (GMHI). I searched its full text (PMC7492273) for every population term (industrial*,
westerniz*, rural, Hadza, Matses, Mongolian, ethnic, geograph*, countr*). It reports no lower scores for any population
or region. Non-industrialised groups (Hadza, Matses/Tunapuco, Mongolian) appear only as *healthy training studies* in
Table 1. The only related text is a generic limitations remark about bias and inclusion. The finding the sentence
describes matches **Poyet et al. 2026, *Cell*, 10.1016/j.cell.2026.10.016** (Crossref- and OpenAlex-verified; abstract:
"microbiome-based disease predictors trained on industrialized populations are uninformative in less industrialized
cohorts"). That paper was ref 13 in v14 and was dropped in v15 "to save space" (round12_response, m13). This was also
missed in round 12: the round-12 report accepted the [19] citation without checking. *Fix:* restore Poyet 2026 for this
sentence, or keep [19] only for "GMHI's developers acknowledged possible geographic bias". The C2 novelty sentence ("we
add its size for a released index and a test by retraining") then holds. Poyet 2026 is also the closest 2026 precedent
for C1 and C2 in a top journal. Removing it makes the Letter look less aware of the field than it is.

**MAJOR 2: "Microbiome studies have not measured it" is contradicted by the manuscript's own next sentence and by
uncited direct precedents.** The introduction says: "Clinical epidemiology has long known that a test's specificity
changes with the population … Microbiome studies have not measured it." The next sentence then cites SIAMCAT [12]
("Controls from other studies doubled the false positives"), which is a measurement of exactly that. In addition:
(a) **Wirbel 2019 [1]** set the *same* cut-off the Letter uses (FPR 0.1 on training controls) and measured realised FPR
on other cohorts (0.09–0.13; PMC7984229). The manuscript cites [1] only for "signals carry over" and "judged by AUROC",
so a reader cannot see that the operating-point design is borrowed. (b) **He et al. 2018, *Nat Med*,
10.1038/s41591-018-0164-x**, "Regional variation limits applications of healthy gut microbiome reference ranges and
disease models", is the best-known microbiome demonstration that both healthy reference ranges and disease models fail
to transfer between regions. It is still uncited, although the repository's own citation_audit.md suggested it. *Fix
(one or two sentences):* "Microbiome studies have shown it for single diseases or within one region [1, 12, He 2018],
but have not mapped it across diseases and populations." Then credit [1] for the cut-off rule in the first Results
paragraph. The novelty claim then rests on what is actually new: breadth, heterogeneity statistics, and the AUROC
non-relation.

**MAJOR 3: The medical-AI precedent for "AUROC transfers, the operating point does not" and for label-free local
recalibration has been cut.** "AUROC did not predict the spread … A better classifier was not a more portable one" is
the Letter's headline conceptual message. **Roschewitz et al. 2023, *Nat Commun*, 10.1038/s41467-023-42396-y** showed
this for screening mammography ("drifts in clinically relevant performance metrics … even for models that generalise in
terms of area under the receiver-operating characteristic curve"). It also corrected the drift with "limited amounts of
unlabelled" target data, which is the C3 recipe. **Qiu et al. 2026, *Biometrics*, 10.1093/biomtc/ujag138 (SACSIM)**
adapts a Neyman–Pearson (FPR-constrained) rule from a small unlabelled target sample. Both were cited from v5 to v9
(added in response to round-3 novelty MAJOR 2) and have since disappeared. The current "The rule is not new" credits
only conformal theory and lab medicine. A reader therefore cannot tell that label-free operating-point correction is an
established medical-AI practice. *Fix:* restore Roschewitz 2023, which costs one reference. It can sit next to the AUROC
sentence and the "rule is not new" sentence. SACSIM is optional. If space is binding, Abdill 2022 or [6] is a better
cut than these.

### MINOR

**MINOR 1: The spectrum-effect citation.** Leeflang 2013 [8] is about variation with *disease prevalence*. It covers
spectrum as one mechanism, so it is defensible. The term "spectrum effect" itself is best sourced to **Mulherin &
Miller 2002, *Ann Intern Med*, 10.7326/0003-4819-137-7-200210010-00011**, or **Usher-Smith, Sharp & Griffin 2016,
*BMJ*, 10.1136/bmj.i3139** ("The spectrum effect in tests for risk prediction, screening, and diagnosis"). For
large-scale empirical support, **Murad et al. 2023, *CMAJ*, 10.1503/cmaj.221802** analysed 6,909 diagnostic-accuracy
studies. Either swap or add one.

**MINOR 2: "is a simple prior-shift correction [22]" overstates the link.** Saerens 2002 re-estimates class priors by
EM and adjusts posteriors. The π_max term in the burn-in rank is a worst-case contamination bound on the burn-in sample.
It is not a prior-shift estimator. Suggest: "… with π_max acting as a conservative allowance for cases in the burn-in
group (cf. prior-shift corrections [22])."

**MINOR 3: Undefined denominator in C2.** "80% of populations fell outside 0.10–0.31 … Eight of these twelve fell below
the band". The "twelve" (80% of 15) is never stated. Write "(12 of 15)".

**MINOR 4: Optional 2026 context for the screening argument.** **Birkeland et al. 2026, *Nat Commun*,
10.1038/s41467-026-75962-1** profiled 1,034 FIT-positive screening participants. CRC-associated taxa (*Hungatella
hathewayi*, *Clostridium symbiosum*) were enriched in people *without* neoplasia. This is direct evidence that markers
learned from case–control cohorts produce false positives in a real screening population. It supports the Letter's
deployment message. **Cirolia et al. 2026 (bioRxiv), 10.64898/2026.05.21.727052** found that IBD classifier performance
depends mainly on the evaluation study rather than on training geography. This matches C1's finding that the
classifier–population pair dominates. Neither is required.

**MINOR 5: Training-data geography.** The claim that pooled public data are geographically skewed, which is the C2
mechanism, would be supported by **Abdill, Adamowicz & Blekhman 2022, *PLoS Biol*, 10.1371/journal.pbio.3001536**.
Optional.

**MINOR 6: Competing indices.** Since the Conclusion says developers should check geographic case mix, a brief nod
could be given to newer health indices that claim cross-lifestyle reproducibility. One example is the HACK index (Goel
et al. 2025, *Cell Rep*, 10.1016/j.celrep.2025.115378; 45,424 samples, 42 countries), a candidate for the same audit.
Optional and space-dependent.

**MINOR 7: Ref [6].** Geng 2024 is an *oral* periodontitis signature, cited for gut-classifier AUROC practice. This is
acceptable as an iMeta example of LODO-AUROC evaluation, but "stool" classifiers are the subject. If a reference must be
cut to make room for MAJOR 1 and MAJOR 3, this is a candidate.

---

## Novelty scoring (/25)

| Dimension | Score | Basis |
|---|---|---|
| Differentiation | 3/5 | The claims are separable from prior work, but v15 weakens the differentiation it had. One credit sentence is mis-cited (MAJOR 1). The "have not measured it" overclaim is contradicted by [12], [1] and He 2018 (MAJOR 2). The closest medical-AI precedent has been removed (MAJOR 3). Score down 1 from round 12. |
| Mechanism | 5/5 | C2 gives a quantified mechanism (OR 6.7), a pre-specified retraining test that is honestly graded (CI 41–149%, AUROC hypothesis failed), and a within-country vs overall-geography decomposition. |
| Evidence | 5/5 | Atlas with I², prediction intervals and overdispersion against binomial noise. Falsified hypotheses are reported, CIs are clustered, and GMWI2 scoring is reproduced (r = 0.991, 95/95 coefficients). |
| Breadth | 5/5 | 14 diseases × 36 (55 full) populations in 20 countries, a published-index audit and a released tool. This is well beyond any single-disease precedent. |
| Significance | 3/5 | It changes how microbiome tests should be reported and deployed, but microbiome diagnostics are not yet in routine clinical use and all site-level results are retrospective. |
| **Total** | **21/25** | |

---

## Missing references (all DOIs verified on Crossref; contents checked as noted)

1. **Poyet M, Rühlemann MC, Schaan AP, et al.** Industrialization drives convergent microbiome and host physiological
   shifts in the human metaorganism. *Cell* 2026. **10.1016/j.cell.2026.10.016**. Abstract checked via OpenAlex.
   Restore for MAJOR 1.
2. **He Y, Wu W, Zheng HM, et al.** Regional variation limits applications of healthy gut microbiome reference ranges
   and disease models. *Nat Med* 2018;24:1532–1535. **10.1038/s41591-018-0164-x**. Title and metadata verified on
   Crossref; OpenAlex has no abstract. MAJOR 2.
3. **Roschewitz M, Khara G, Yearsley J, et al.** Automatic correction of performance drift under acquisition shift in
   medical image classification. *Nat Commun* 2023;14:6608. **10.1038/s41467-023-42396-y**. Abstract checked. MAJOR 3.
4. **Qiu et al.** Shift-adjusted Neyman–Pearson classifiers via single index modeling (SACSIM). *Biometrics*
   2026;82:ujag138. **10.1093/biomtc/ujag138**. Optional, MAJOR 3.
5. **Usher-Smith JA, Sharp SJ, Griffin SJ.** The spectrum effect in tests for risk prediction, screening, and diagnosis.
   *BMJ* 2016;353:i3139. **10.1136/bmj.i3139**. MINOR 1.
6. **Mulherin SA, Miller WC.** Spectrum bias or spectrum effect? Subgroup variation in diagnostic test evaluation. *Ann
   Intern Med* 2002;137:598–602. **10.7326/0003-4819-137-7-200210010-00011**. MINOR 1 (alternative to 5).
7. **Murad MH, Lin L, Chu H, et al.** The association of sensitivity and specificity with disease prevalence: analysis
   of 6909 studies of diagnostic test accuracy. *CMAJ* 2023;195:E925–E931. **10.1503/cmaj.221802**. Abstract checked.
   Optional, MINOR 1.
8. **Birkeland EE, Kværner AS, Avershina E, et al.** Microbiome signatures for detection of colorectal lesions in
   population-based FIT screening. *Nat Commun* 2026;17:8982. **10.1038/s41467-026-75962-1**. Abstract checked.
   Optional, MINOR 4.
9. **Cirolia G, Gustafson JT, Aswani AJ, Wolf AR.** Performance of IBD machine learning classifiers varies across
   microbiome training data independent of geographic diversity. bioRxiv 2026. **10.64898/2026.05.21.727052**. Abstract
   checked; preprint. Optional, MINOR 4.
10. **Abdill RJ, Adamowicz EM, Blekhman R.** Public human microbiome data are dominated by highly developed countries.
    *PLoS Biol* 2022;20:e3001536. **10.1371/journal.pbio.3001536**. Optional, MINOR 5.
11. **Goel A, Shete O, Goswami S, Samal A.** Toward a health-associated core keystone index for the human gut
    microbiome. *Cell Rep* 2025;44:115378. **10.1016/j.celrep.2025.115378**. Abstract checked. Optional, MINOR 6.

I found no 2024–2026 paper that audits GMWI2 or GMHI for population-specific false positives, or that maps fixed-cut-off
FPR across many healthy microbiome populations. The C1 and C2 cores therefore remain unanticipated. Searches were run
on OpenAlex (title/abstract, 2020–2026 and 2024–2026 filters), Crossref and the arXiv export API (microbiome ×
classifier/generalisation/false positive; operating point × unlabelled × threshold). The closest new items are listed
above.

---

## Reference integrity check

All 28 references, plus the CRC-TrustBench correction (10.3389/fmicb.2026.2021752), were queried on Crossref. **All
resolve, and first author, year, title, journal, volume and pages match the reference list.** Ref [11] (Degregori 2026,
*iMeta* e70192) has no volume yet, which is consistent with Crossref.

Each citation checked against what it shows:

| Ref | Cited for | Supported? |
|---|---|---|
| [1] Wirbel 2019 | Signals carry over; judged by AUROC | Yes. It is also the source of the fixed-FPR-0.1 cut-off design, which the text does not say (MAJOR 2). |
| [2] Thomas 2019; [3] Piccinno 2025; [4] Mei 2024 | Cross-cohort signals | Yes. |
| [5] Pasolli 2016; [6] Geng 2024 | AUROC in held-out cohorts | Yes. [6] is oral, not gut (MINOR 7). |
| [7] Selby 2018 | FIT thresholds / colonoscopy follow-up | Yes. |
| [8] Leeflang 2013 | Spectrum effect | Broadly yes. The paper is about prevalence (MINOR 1). |
| [9] Li 2023; [10] Li 2025 | Cross-cohort AUROC; best practices focus on discrimination | Yes. |
| [11] Degregori 2026 | "most studies do not deposit the metadata needed to re-test them" | Yes. The abstract says 85.5% of samples cannot be reused and only 5.9% of studies give per-sample status, age and sex. |
| [12] SIAMCAT | External controls doubled false positives; country confounding; control augmentation | Yes. Note that "of CRC classifiers" is narrower than the paper's cross-disease analysis. |
| [13] CRC-TrustBench (+ correction) | CRC models lose calibration across countries | Yes. |
| [14] Ozarda 2018; [24] refineR | Local reference-limit verification; limits from routine data | Yes. |
| [15] Pasolli 2017; [17] Beghini 2021 | curatedMetagenomicData; MetaPhlAn3 | Yes. |
| [16] Chang 2024 GMWI2 | Model, 95 taxa, 8,069 samples / 54 studies, cut-off 0 | Yes. Full text confirms 5,547 healthy / 2,522 non-healthy, matching the text. |
| [18] Hehemann 2010 | *B. plebeius* seaweed enzymes from marine bacteria | Yes. |
| **[19] Gupta 2020 GMHI** | "Low health-index scores in populations that lack the training markers were reported before" | **No (MAJOR 1).** Not in the full text. |
| [20] Lei 2018; [21] Bates 2023 | Split-conformal / conformal p-value guarantee | Yes. |
| [22] Saerens 2002 | "is a simple prior-shift correction" | Loosely. Related, but not an equivalence (MINOR 2). |
| [23] Tong 2018 | A stricter rank bounds P(FPR > α) (NP umbrella) | Yes. |
| [25] STORMS | Reporting checklist | Yes. |
| [26] DEBIAS-M; [27] MMUPHin; [28] ConQuR | Batch/processing-bias corrections | Yes. |

No fabricated reference was found. There is one mis-attributed citation ([19]) and one loose equivalence ([22]).
