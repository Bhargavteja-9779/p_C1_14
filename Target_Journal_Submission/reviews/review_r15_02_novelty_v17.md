# Review r15-02: Novelty and related work (Reviewer 2), manuscript v17

**Manuscript:** "Gut-microbiome disease classifiers flag 0–87% of healthy people at the same cut-off, depending on the population" (Letter, iMeta)
**Files reviewed:** manuscript_v17.md, supporting_information_v17.md, highlights.md, figures/ (Fig. 1–3, S1, S2)
**Reviewer focus:** novelty, positioning against prior work, accuracy of citations. Earlier review reports were not read.

**Score: 5.5 / 10**
**Recommendation: Major revision**

## Summary of the submission

The authors score 28 fixed-cut-off classifiers (14 diseases, LASSO and RF on MetaPhlAn3 profiles) in 36 strict healthy populations of curatedMetagenomicData and report wide between-population variation in FPR (I² median 0.94). AUROC does not predict this spread. They audit two released health indices. GMWI2 flags a median 64% of healthy people in East Asian training studies against 12% elsewhere. GMHI is offered as a "pre-specified replication" (67% vs 21%), with a profiler-version (MetaPhlAn2 vs 3) shift in the GMHI flag rate. Retraining the GMWI2 recipe with country × label weighting narrows the East Asian gap. Finally, a label-free burn-in quantile rule (split-conformal) recalibrates the cut-off within a site, though not across sites.

## Overall assessment of novelty

The best new contribution is empirical: a systematic, multi-disease **atlas of FPR at a fixed cut-off across healthy populations**, reported with I² and prediction intervals. Microbiome ML has reported almost only AUROC, and the explicit framing as a spectrum effect is useful. The GMWI2 regional audit, with the case-mix retraining test, is also new as far as I can find. I found no published study that stratifies GMWI2 errors by region or tests the training-data case-mix explanation.

Three of the headline claims are less novel than presented, or are positioned inaccurately:

1. **The GMHI cross-population audit has a direct precedent in a paper the authors already cite (ref. 12, Poyet et al., Cell 2026).** Secondary reports of that paper describe an explicit test of "cross-population portability of the Gut Microbiota Health Index (GMHI)" in healthy adults. GMHI "performed poorly in non-industrialized societies, yielding a median score of zero across six countries", "because relevant microbial health markers were uncommon or absent". The manuscript cites ref. 12 only for "disease predictors" and frames its own GMHI audit as a test of "whether this was specific to GMWI2". The authors must acknowledge that GMHI's population dependence in healthy people has already been reported. They must also state what they add: East Asian rather than non-industrialised populations, the developers' own data, and the profiler effect.
2. **The recalibration rule is, by the authors' own account, not new** ("The rule is not new", refs 14, 24–28). In a Letter, however, the highlights and abstract give it equal weight with the atlas. CRC-TrustBench (ref. 13) is cited only for "lose calibration across countries". Its abstract states that it also evaluated Platt calibration and conformal-style sets "without outer-test labels" across countries in microbiome CRC models, and that conformal coverage fell below target. That is the closest microbiome precedent for label-free calibration and conformal methods under country shift, and it is mis-described by omission.
3. **The recommendation to report per-population performance with I² and a prediction interval** comes straight from established clinical-prediction methodology: Riley et al. 2016 and Debray et al. 2017 on meta-analysis of calibration and performance across clusters. The manuscript cites none of this, so the recommendation reads as if it were new.

Taken together, the paper is a solid and honest empirical resource. Its novelty should be stated as "the first multi-disease, per-population FPR atlas and the first regional audit of GMWI2", not as the discovery that health indices or cut-offs are population-dependent.

## Claim → closest prior work → difference

| # | Claim in manuscript | Closest prior work | What is actually new here |
|---|---|---|---|
| 1 | FPR at a fixed cut-off varies widely across healthy populations (0–0.87; I² 0.94) | Wirbel 2019 [1] (CRC FPR on other-disease cohorts 0.09–0.13); Wirbel 2021 SIAMCAT [10] (external controls raise CRC false positives); He 2018 [11] (regional non-transfer within Guangdong); Poyet 2026 [12]; CRC-TrustBench 2026 [13]; Roschewitz 2023 [14] (imaging) | Breadth (14 diseases, 36 healthy populations, 20 countries) and the FPR-specific heterogeneity statistics. Single-disease or single-region precedents exist, so the novelty is in scale and metric, not phenomenon. Adequately cited. |
| 2 | AUROC does not predict FPR portability | Clinical prediction literature: calibration and discrimination are distinct (Van Calster 2019); operating-point drift with stable AUROC (Roschewitz 2023 [14]) | First demonstration across many microbiome classifiers. Modest novelty. Van Calster et al. should be cited. |
| 3 | Report per-population FPR with I² and prediction interval | Riley et al. BMJ 2016; Debray et al. BMJ 2017; Steyerberg & Harrell 2016 (internal–external validation) | Transfer of an established method to microbiome. **Not cited, needs adding.** |
| 4 | GMWI2 flags a median 64% of healthy people in East Asian training studies (vs 12%) | Chang 2024 [20]: per-study ISV accuracy varied, and external healthy cohort H5 had only 28.1% accuracy (66/235), unexplained; no analysis by geography. Abdill 2022 (geographic skew of public microbiome data) | **New.** No prior region-stratified audit of GMWI2 found. The developers' own H5 result (72% of a healthy external cohort mislabelled) should be cited and its country identified. If it is the Japanese control group of Nagata et al. 2022 (n = 235; authors to verify from Chang 2024 Suppl. Data 6), it is direct prior support. |
| 5 | Mechanism: geographic case mix in training (62% of non-healthy vs 20% of healthy samples East Asian) | Wirbel 2021 [10] (country confounding); Gupta 2020 [22] (bias hard to remove); Poyet 2026 [12]; Deschasaux 2018 (ethnicity structures the microbiome independently of geography) | The quantification for a released index and the retraining test are new. Shortcut learning from study and country identity is also shown in CRC-TrustBench (MiLCA audit), which should be acknowledged here. |
| 6 | GMHI "pre-specified replication" (67% vs 21% in developers' data) | **Poyet et al. 2026 [12]: GMHI audited in healthy adults of 6 non-industrialised countries, median score 0**; Zhu et al. 2023 Microbiome (hiPCA; critique of GMHI's limits) | Partially new: East Asian focus within developers' data. The cross-population GMHI failure itself is precedented. The replication is not independent either: GMWI2's 54-study training set appears to extend GMHI's pool, so many Table S26 studies are probably shared (see MAJOR 2). |
| 7 | Released cut-off shifts with profiler version (GMHI flag 70% → 85% on 101 samples, MetaPhlAn2 vs 3) | Beghini 2021 [21]; Blanco-Míguez 2023 (MetaPhlAn 4: taxonomy re-defined as SGBs); general profiler-disagreement benchmarks | Small, useful, new observation. Novelty is limited because the effect is driven by species renaming, which is predictable. MetaPhlAn 4 has already changed names again, which strengthens the practical warning and should be noted. |
| 8 | Label-free burn-in quantile recalibration (split-conformal) | Lei 2018 [24]; Bates 2023 [25]; Tong 2018 NP umbrella [27]; Roschewitz 2023 [14]; refineR [28]; indirect reference-interval methods (Jones 2018); CRC-TrustBench [13] (label-free calibration and conformal sets under country shift); clinical model updating (Janssen 2008) | Not new as a method (the authors say so). New are the empirical test under non-random within-site splits and the cross-site failure. Should be framed as validation, not contribution. |
| 9 | "Microbiome diagnostics have no such [local verification] step" | Mykinso cohort, Japanese reference ranges for gut microbial indices (2021); He 2018 [11] (regional reference ranges) | Overstated. Local reference ranges for microbiome indices have been proposed and built. Soften to "no routine step for classifier cut-offs". |

## MAJOR issues

**MAJOR 1. Poyet et al. (ref. 12) already audited GMHI across healthy populations, and the manuscript does not say so.**
Ref. 12 is described only as showing that "predictors trained on industrialised populations were uninformative in less-industrialised cohorts". According to published summaries of the Cell paper, it explicitly tested GMHI portability in healthy adults and found a median GMHI of 0 across six non-industrialised countries, attributed to the absence of marker species. This bears on the paper in three ways. (a) The GMHI section must cite it as prior evidence of GMHI population dependence. (b) It points in a different direction from the authors' GMWI2 finding: GMWI2 "almost never mislabelled" rural Africans (0–7%), whereas Poyet report GMHI failing in non-industrialised societies. The authors should report GMHI flag rates in the non-westernised cMD populations (bold columns in Fig. 1B) and discuss the contrast. (c) A median score of exactly 0 interacts with the authors' tie rule ("20 ties at exactly 0 counted as not flagged", S7). In populations where markers are absent, ties at 0 may be common, and the GMHI flag rate becomes an artefact of tie handling. Report the share of ties per population and a sensitivity analysis with ties counted as flagged.
*Fix:* Add one or two sentences in the GMHI section and the introduction: "Poyet et al. reported that GMHI scores collapse to 0 in healthy non-industrialised populations [12]; we show that the same index also over-flags healthy East Asian cohorts in its developers' own data, and that its level depends on profiler version." Add the tie sensitivity analysis to S7. Revise the highlight's "pre-specified replication" to make clear that GMHI's population dependence was already known.

**MAJOR 2. The GMHI "replication" is not independent of the GMWI2 finding.**
GMWI2 was built by the same group on an expanded version of the GMHI training pool. Several Table S26 studies (e.g., Qin 2012, Qin 2014, Jie 2017, Zeller 2014, Feng 2015, Nielsen 2014, Le Chatelier 2013, Schirmer 2016) are likely among GMWI2's 54 studies too. The East Asian excess in GMHI's own data (8 studies) may therefore be largely the same healthy samples as in the GMWI2 analysis, scored by a related model. Likewise the cMD ρ = 0.70 between GMHI and GMWI2 flag rates (Fig. S2B) is visibly driven by a cluster of East Asian populations. It may reflect shared training studies and the shared marker logic (prevalence-based health and non-health taxa), not an independent population effect.
*Fix:* Report the overlap of studies and samples between the GMHI and GMWI2 training sets. Repeat the GMHI H2 test on GMHI-only studies, or state plainly that it is not independent. Report ρ without the East Asian populations, or a partial correlation adjusting for region. Replace "replication" with "consistent finding in the predecessor index" unless independence is shown.

**MAJOR 3. Missing methodological lineage for the reporting recommendation and spectrum effect.**
The conclusion that benchmarks "should report the FPR at a fixed cut-off in each held-out population, with I² and a prediction interval" is the standard in clinical prediction-model validation (Riley et al. BMJ 2016; Debray et al. BMJ 2017; Steyerberg & Harrell 2016). Calibration-in-the-large and its heterogeneity across centres is the direct analogue of FPR drift. Ransohoff & Feinstein 1978, the origin of the spectrum concept, is also absent.
*Fix:* Cite Riley 2016 and Debray 2017 where I² and prediction intervals are introduced and in the recommendation. Cite Van Calster 2019 for "AUROC does not imply calibration". Optionally cite Ransohoff & Feinstein 1978 next to [8, 9].

**MAJOR 4. Under-description of CRC-TrustBench (ref. 13) and of the developers' own external-validation signal (ref. 20).**
(a) CRC-TrustBench explicitly evaluated label-free calibration, conformal-style sets (coverage below target under LOCO) and study/country shortcut learning (MiLCA). It is the nearest microbiome precedent for both the mechanism (country shortcuts) and the fix (label-free conformal calibration). Citing it only for "lose calibration across countries" is inaccurate by omission.
(b) Chang et al. [20] themselves report a healthy external cohort (H5) with 28.1% accuracy (66 of 235) and leave it unexplained. The manuscript states that the developers' training FPR is 20.8% but does not mention this external result, which is the most direct prior evidence for the paper's GMWI2 claim.
*Fix:* Expand the ref. 13 citation in the introduction and in the recalibration section, and say how the burn-in rule differs: it bounds FPR at a fixed operating point rather than calibrating probabilities. Identify cohort H5 from Chang 2024 Supplementary Data 6, report its country, and discuss it.

**MAJOR 5. Novelty framing in the graphical-abstract summary and highlights is inconsistent and overstated.**
The graphical-abstract summary contains two contradictory consecutive sentences: "Two published gut-health indices ... each labelled most healthy people ..." followed by "A published gut-health index labelled 64% ...". This is an unedited leftover. The recalibration result ("cut the FPR error by 62%") is presented as a finding of equal standing although the method is acknowledged as not new, and the within-site improvement is partly true by construction (S5: "met, but true by construction" for the random-split version).
*Fix:* Delete the duplicated sentence. In the highlights, present recalibration as "an existing split-conformal rule, tested under non-random within-site splits". Keep the cross-site failure prominent, since it is the more informative and less obvious result.

## MINOR issues

1. **"Microbiome diagnostics have no such step"** (introduction) is overstated. Japanese reference ranges for gut microbial indices have been established from a 5,843-person testing-service cohort (Mykinso, 2021), and He 2018 [11] built regional reference ranges. Reword to "no established step for verifying classifier cut-offs on local healthy people".
2. **Definition of "East Asian".** It is never defined. Mongolia is in Eastern Asia (UN geoscheme), yet the GMHI table classifies "Liu (2016), Mongolian Population" (flag rate 0.075) as not East Asian, and Fig. 1 shows MNG·Liu separately. Define the region a priori (country list) and show sensitivity to including Mongolia, since that one study could weaken the GMHI contrast.
3. **Geographic skew of training data.** Cite Abdill et al. 2022 (PLoS Biol) for the dominance of a few countries in public microbiome data. It is the natural citation for the "geographic make-up of training data" argument.
4. **Ethnicity and geography.** Deschasaux et al. 2018 (Nat Med) showed that ethnicity structures gut microbiota within one city. Cite it alongside He 2018 [11], since the manuscript cannot separate country from laboratory or ancestry.
5. **Profiler versions.** Note that MetaPhlAn 4 (Blanco-Míguez et al. 2023) re-defines taxa as SGBs. GMWI2's 95 MetaPhlAn3 clade names will therefore face the same mapping problem the authors document for GMHI, a concrete and timely implication.
6. **Ref. 6 (Geng 2024, oral periodontitis signature)** is cited for gut-classifier AUROC evaluation practice. It is an oral, not gut, study. A gut example would be more apt, or say "microbiome" rather than imply gut.
7. **Ref. 22 paraphrase.** "The developers of an earlier health index noted that such biases are hard to remove": please give the exact location in Gupta 2020, or quote it. I could not confirm this wording.
8. **Ref. 26 (Saerens 2002)** is an EM prior-shift estimator, not a conservative bound. "cf." is acceptable, but say that π_max is a worst-case allowance rather than an estimated prior.
9. **Ref. 13** lists the article and its correction. Check that the correction does not affect the figures cited.
10. **Ref. 12** is the Cell 2026 version (online November 2026). Volume and pages are not yet assigned; cite the bioRxiv preprint (10.1101/2025.10.20.683358) as well if the GMHI analysis is described in it, and check that the GMHI result is in the final Cell version.
11. **Ref. 19** (Pasolli 2017) describes the original curatedMetagenomicData. The release used (2021-03-31, MetaPhlAn3) is curatedMetagenomicData 3. State the package version explicitly.

## Reference verification (Crossref API, all 33 DOIs)

All 33 DOIs resolve, and titles, journals, volumes and pages match the reference list. Specific checks:
- [12] Poyet et al., Cell 2026, 10.1016/j.cell.2026.10.016: resolves (issued 2026-11, no volume or pages yet). The abstract confirms "disease predictors trained on industrialized populations are uninformative in less industrialized cohorts". The description is accurate but incomplete (MAJOR 1).
- [13] Zhang et al., Front Microbiol 2026;17:1971707 and correction 10.3389/fmicb.2026.2021752: both resolve. The description is incomplete (MAJOR 4).
- [17] Degregori et al., iMeta 2026, e70192: resolves. The abstract (5.9% of studies deposit per-sample disease, age and sex; 85.5% of samples not reusable) supports the description.
- [20] Chang et al., Nat Commun 2024;15:7447: resolves. The full text confirms MetaPhlAn3, 8,069 samples, 54 studies and no geographic stratification of performance.
- [3], [4], [14], [16], [30], [31], [32]: all verified, with metadata matching.
- No DOI failed. No retraction notices were found in Crossref metadata.

## Missed or under-used prior work (DOIs verified via Crossref)

| Work | DOI | Why it matters |
|---|---|---|
| Poyet et al. 2025, bioRxiv preprint of ref. 12 | 10.1101/2025.10.20.683358 | GMHI cross-population audit in healthy non-industrialised adults (MAJOR 1) |
| Riley et al. 2016, BMJ 353:i3140, external validation using big datasets / IPD meta-analysis | 10.1136/bmj.i3140 | Heterogeneity of calibration across clusters; I² and prediction intervals for performance |
| Debray et al. 2017, BMJ 356:i6460, meta-analysis of prediction model performance | 10.1136/bmj.i6460 | Methodological source for pooling performance with prediction intervals |
| Van Calster et al. 2019, BMC Med 17:230, "Calibration: the Achilles heel of predictive analytics" | 10.1186/s12916-019-1466-7 | Discrimination ≠ calibration; supports "AUROC did not predict the spread" |
| Steyerberg & Harrell 2016, J Clin Epidemiol 69:245, internal–external validation | 10.1016/j.jclinepi.2015.04.005 | Leave-one-cluster-out validation framework the atlas uses |
| Janssen et al. 2008, J Clin Epidemiol 61:76, updating methods for prediction models | 10.1016/j.jclinepi.2007.04.018 | Local recalibration of models at new sites (intercept updating) |
| Ransohoff & Feinstein 1978, NEJM 299:926, spectrum and bias | 10.1056/NEJM197810262991705 | Origin of the spectrum concept |
| Abdill, Adamowicz & Blekhman 2022, PLoS Biol 20:e3001536 | 10.1371/journal.pbio.3001536 | Geographic skew of public microbiome data |
| Deschasaux et al. 2018, Nat Med 24:1526, ethnicity in HELIUS | 10.1038/s41591-018-0160-1 | Ethnicity vs geography confounding of microbiome composition |
| Blanco-Míguez et al. 2023, Nat Biotechnol 41:1633, MetaPhlAn 4 | 10.1038/s41587-023-01688-w | Next profiler-version shift (SGB taxonomy) relevant to released indices |
| Zhu et al. 2023, Microbiome 11:184, hiPCA health-status monitoring | 10.1186/s40168-023-01614-x | Alternative health index developed partly to address GMHI limitations |
| Mykinso cohort 2021, Biosci Microbiota Food Health, Japanese reference ranges for gut microbial indices | 10.12938/bmfh.2020-038 | Counter-example to "no local verification step" |
| Jones et al. 2018, Clin Chem Lab Med 57:20, indirect reference-interval methods | 10.1515/cclm-2018-0073 | Label-free reference limits from routine data (alongside refineR [28]) |
| Nagata et al. 2022, Gastroenterology, multinational PDAC metagenomics | 10.1053/j.gastro.2022.03.054 | Possible source of GMWI2 external healthy cohort H5; authors to verify |

## Questions to the authors

1. Which study is GMWI2 external healthy cohort H5 (28.1% accuracy), and from which country?
2. How many of the 21 GMHI studies (Table S26) are also among the 44 GMWI2 studies in Fig. 2A?
3. What are the GMHI flag rates, and the proportion of GMHI = 0 ties, in the non-westernised cMD populations?
4. Was the East Asian country list fixed before the GMWI2 analysis, and does it include Mongolia and Korea?

## Bottom line

This is a careful, transparent analysis with an unusually honest account of failed hypotheses, and the FPR atlas is a useful resource for the field. Its novelty is currently overstated in two places. The GMHI audit has a direct precedent in a paper the authors cite but do not describe fully, and it is not independent of the GMWI2 data. The recalibration rule and the reporting recommendation also both have established lineages, in conformal and clinical prediction methodology, that are partly uncited. With repositioning, the tie and overlap checks, and the added citations, the Letter would make a clear contribution suited to iMeta.
