# Referee report, round 5: novelty and related work (manuscript_v6.md)

**Score:** 8/10
**Decision:** Accept after minor revision. One reference has become outdated and now overlaps with a claim. It must be updated before submission.

## Summary judgement

v6 makes a narrow novelty claim and backs it. It states that the label-free burn-in rule "is not new". The control-augmentation result is framed as a disagreement with SIAMCAT, not as a refutation. DEBIAS-M is described accurately as an untested competitor. All five r4 concerns are fixed:
- GMHI/GMWI2 are now cited as [11, 12].
- The highlight now reads "helped ... most when".
- The graphical abstract is hedged with "in the cohorts we could test".
- The preprint status is disclosed.
- The label-shift citation was optional.

The remaining contributions are new as far as I can find:
- per-cohort FPR heterogeneity (I², prediction interval) at a fixed cut-off across 32–35 healthy populations;
- a taxon-level breakdown of the score shift;
- a head-to-head test showing that borrowed references (pooled, nearest-neighbour, same-country, augmentation) fail where a site-local burn-in works, with a map of where the burn-in breaks (sub-site, neighbouring cohort).

My searches found no study that reports fixed-threshold FPR for microbiome classifiers cohort by cohort across general healthy populations.

The main new problem comes from outside the manuscript. Reference [9] (Poyet et al.) was published in *Cell* in November 2026 (doi:10.1016/j.cell.2026.10.016; Crossref confirms it). Secondary coverage of the published paper reports a closer overlap with this manuscript's "why" section than the preprint abstract suggested: GMHI gave a median score of zero in six non-industrialised countries "because relevant health markers were rare or absent". This is the same mechanism the manuscript claims in "WHY: health markers of the training population are rarer elsewhere". It applies to a health index rather than to disease classifiers at a fixed FPR, so C2 is still partly new. But the sentence "add the per-population size of the effect and the taxa behind it" needs to name what Poyet already showed.

## Claim → closest prior work → exact difference

| # | Claim (v6) | Closest prior work | Exact difference |
|---|---|---|---|
| C1 | Fixed-cut-off FPR varies widely across general healthy populations (I² 70–95%, prediction interval up to 1–63%) | Wirbel 2021 SIAMCAT, https://doi.org/10.1186/s13059-021-02306-1 ; Zhang 2026 CRC-TrustBench, https://doi.org/10.3389/fmicb.2026.1971707 | SIAMCAT showed that external-control FPR more than doubled, with no heterogeneity statistics, no healthy-population frame and no mechanism. CRC-TrustBench covers CRC only (15 studies, 10 countries) and reports AUROC, Brier score and log loss, not per-cohort FPR dispersion. New. |
| C2 | Over-flagged populations lack the training cohorts' "health-marker" taxa | Poyet 2026 *Cell*, https://doi.org/10.1016/j.cell.2026.10.016 (formerly the bioRxiv preprint cited as [9]) | Poyet: industrialised-trained predictors are uninformative in less-industrialised cohorts, and GMHI scores collapse because health markers are absent. Manuscript adds a per-population FPR, a pre-specified taxon decomposition for three disease classifiers, and the Asian over-flagging by the IBD test. Partly new. The mechanism overlaps and the text must acknowledge it (Concern 1). |
| C3 | Cut-offs from other cohorts, including same-country cohorts and control augmentation, do not restore FPR | Wirbel 2021 (augmentation largely removed the excess; the gain "did not strongly depend" on which controls were added) | Manuscript finds no mean gain (P = 0.58), with gains only for IBD and mostly when the same population is in the pool. Clearly presented as a disagreement. New and fair. |
| C4 | Processing-bias corrections should be judged by the FPR they deliver | Austin 2025 DEBIAS-M, https://doi.org/10.1038/s41564-025-01954-4 ; Ling 2022 ConQuR, https://doi.org/10.1038/s41467-022-33071-9 ; Ma 2022 MMUPHin | These methods report AUROC/AUPRC only. The recommendation is new. None of the three was run, as the manuscript discloses. ConQuR is named but not cited (Concern 3). |
| C5 | A site-local, label-free burn-in of about 100 people restores FPR; borrowed references and cross-site burn-ins do not | Roschewitz 2023 UPA, https://doi.org/10.1038/s41467-023-42396-y ; Qiu 2026 SACSIM, https://doi.org/10.1093/biomtc/ujag138 ; CRC-TrustBench (label-free Platt and conformal-style sets) | The method is established and the manuscript says so. New: the empirical map of where it breaks for microbiome tests. CRC-TrustBench already tried label-free recalibration for microbiome CRC, which the manuscript does not say (Concern 2). |
| C6 | The order-statistic rule bounds expected FPR up to π_max | Bates 2023, https://doi.org/10.1214/22-AOS2244 ; Bashari 2025, arXiv:2502.04807 ; Tong 2018, https://doi.org/10.1126/sciadv.aao1659 ; Zierk 2020 kosmic / Ammer 2021 refineR | Correctly credited. Bashari confirms that a contaminated reference gives conservative type-I control. Not claimed as new. |
| C7 | Health indices apply one cut-off across cohorts | Gupta 2020 GMHI; Chang 2024 GMWI2; Hiseni 2026 | Now cited [10–12]. Accurately described. |

## Concerns

1. **MAJOR (must fix; easy): reference [9] is outdated and its overlap with C2 is understated.** Poyet et al. was published in *Cell* (November 2026, doi:10.1016/j.cell.2026.10.016). The manuscript still cites the bioRxiv version, calls it "a preprint" in the Limitations, and describes it only as showing that predictors "lose accuracy". The published paper reportedly shows that GMHI fails in non-industrialised populations because health-marker taxa are rare or absent. That is the same mechanism as the "WHY" section. I saw this only in secondary coverage, not the full text, so the authors should check it.
   *Resolution:*
   - Update [9] to the *Cell* record.
   - Delete the preprint bullet from the Limitations.
   - Rewrite the text at lines 57–58 and 142–143 to read something like: "Poyet et al. showed that health-index markers are rare or absent in non-industrialised populations [9]. We show the same pattern for disease classifiers at a fixed FPR, give its per-population size, and identify the taxa."

2. **MINOR: CRC-TrustBench [8] is described too narrowly.** It also tested label-free Platt calibration and conformal-style sets on cross-country CRC hold-outs, and reported Brier and log-loss gains. That is the closest microbiome precedent for label-free recalibration.
   *Resolution:* add a clause, e.g. "...lose calibration across countries, which label-free Platt scaling only partly repairs [8]". Also state that the difference here is FPR at a fixed cut-off, not probability calibration.

3. **MINOR: ConQuR is named but not cited.** It appears twice, in the Limitations and in the "We did not run" bullet, with no reference.
   *Resolution:* cite Ling W et al., *Nat Commun* 2022;13:5418, https://doi.org/10.1038/s41467-022-33071-9.

4. **MINOR: CRC-TrustBench cross-country finding slightly strengthens C1 and should be acknowledged as concurrent.** It independently reports that microbiome CRC models drop under leave-one-country-out and that profiles predict country identity. This supports the manuscript's thesis and is not a priority threat, but a one-clause nod avoids the appearance of ignoring a 2026 concurrent benchmark.
   *Resolution:* optional one-clause citation where [8] already appears.

No other over-claiming found. The title, highlights and conclusion are now matched to the evidence base (7–13 populations, two multi-site studies), and the hedging is consistent across abstract, body and limitations.

## Citations spot-checked (Crossref / arXiv / full text)

Verified existing and matching their sentences: [1] Wirbel 2019, [3] Piccinno 2025 (Nat Med 31:2416–2429), [6] Selby 2018 (Ann Intern Med 169:439–447), [7] Wirbel 2021 SIAMCAT, [8] Zhang 2026 CRC-TrustBench (abstract read; AUROC 0.874→0.821 LOCO, Platt scaling, conformal sets), [9] Poyet — now *Cell* 2026, not the preprint (Concern 1), [10] Hiseni 2026 (Gut Microbes 18), [13] Leeflang 2013 (CMAJ 185:E537–E544; DOI 10.1503/cmaj.121286 resolves), [14] Ozarda 2018 (CCLM 57:30–37), [15] Janssen 2008 (J Clin Epidemiol 61:76–86), [16] Van Calster 2023 (BMC Med 21:70), [17] Roschewitz 2023 (Nat Commun 14:6608), [18] Qiu 2026 SACSIM (Biometrics 82), [23] Bates 2023 (Ann Stat 51:149–178), [24] Bashari 2025 (arXiv:2502.04807; confirms conservative type-I control under contaminated reference), [25] Tong 2018 (Sci Adv 4), [26] Zierk 2020 kosmic (Sci Rep 10:1704), [27] Ammer 2021 refineR, [30] Ma 2022 MMUPHin (Genome Biol 23:208). No fabricated or mis-attributed citation found.

## Searches run (10 phrasings)

1. microbiome classifier specificity / FPR external healthy cohorts at fixed threshold
2. SIAMCAT control augmentation external controls false-positive rate cross-study
3. ConQuR / MMUPHin / DEBIAS-M batch correction cross-study prediction benchmark
4. label-free threshold recalibration from unlabeled target, conformal, Neyman–Pearson
5. clinical prediction model updating / intercept recalibration in a new setting (Steyerberg)
6. gut microbiome classifier transfer to non-industrialised populations, geographic bias
7. gut microbiome health index fixed cut-off across countries, dysbiosis index
8. indirect reference intervals from routine lab data (refineR, kosmic)
9. 2026 industrialisation health-index failure in non-industrialised populations (located Poyet *Cell* 2026)
10. CRC microbiome classifier specificity varies by population / Asian cohorts / recalibration
