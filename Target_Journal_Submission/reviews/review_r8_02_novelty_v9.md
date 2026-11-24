# Referee report, round 8: novelty and related work (manuscript_v9.md)

**Score:** 8/10
**Decision:** Accept after minor revision (no MAJOR concerns).

## Summary judgement

v9 places its contribution accurately. The burn-in rule is called "not new" and credited to conformal and
Neyman–Pearson work [22–25]. Control augmentation is presented as a disagreement with [7], not a refutation.
DEBIAS-M, MMUPHin and ConQuR are cited and said not to have been run. Line 126 now concedes the health-index
literature [11, 12] and states the novelty as the size of the per-test FPR shift in each population, which
resolves r7 concern 1 in substance.

I searched with eight or more phrasings. I found no published work that reports the fixed-cut-off FPR of microbiome
disease classifiers cohort by cohort across general healthy populations with I² and prediction intervals. I also
found none that compares site-local label-free recalibration against borrowed references (pooled, nearest,
same-country, augmentation) for microbiome tests. The central claims therefore stand. What remains is wording
and some optional citations.

I spot-checked the characterisation of [7] against the SIAMCAT full text (bioRxiv v2). It reports "a more than
twofold increase in false positives on average" for naive transfer, and says that "the control augmentation
strategy did not strongly depend on the set of controls used". The manuscript's sentences at lines 55–56 and
166–167 are therefore accurate.

## Claim → closest prior work → exact difference

| # | Claim (v9) | Closest prior work | Exact difference |
|---|---|---|---|
| C1 | Fixed-cut-off FPR varies between healthy populations (I² 70–95%, PI up to 1–63%) | Wirbel 2021 SIAMCAT https://doi.org/10.1186/s13059-021-02306-1 ; Zhang 2026 CRC-TrustBench https://doi.org/10.3389/fmicb.2026.1971707 | SIAMCAT reports an average >2-fold FPR excess on external controls, with no per-population dispersion or heterogeneity statistics. CRC-TrustBench is CRC-only and reports AUROC, Brier score, log-loss and conformal coverage under LOSO/LOCO, not per-cohort FPR at one cut-off. **New.** |
| C2 | A few taxa, often training-cohort "health markers", carry the score shift; Asian populations are over-flagged by IBD tests and non-westernised ones by T2D tests | Poyet 2026 *Cell* https://doi.org/10.1016/j.cell.2026.10.016 (preprint 10.1101/2025.10.20.683358) ; Gupta 2020 GMHI https://doi.org/10.1038/s41467-020-18476-8 | Prior work shows that health-index markers are scarce in non-industrialised people (GMHI median ~0) and that European-trained predictors transfer poorly. The manuscript adds a pre-specified taxon decomposition for three disease classifiers and the effect on the FPR. **Partly new**; the mechanism is conceded at line 126. |
| C3 | Borrowed cut-offs (pooled, nearest, same-country) and augmentation do not restore the FPR | Wirbel 2021 (augmentation removed most of the excess; benefit did not depend on control set) | No overall gain (P = 0.58), benefit only for IBD and mostly when the same population is in the pool. This directly qualifies [7]'s "set of controls did not matter" finding. **New, fairly framed.** |
| C4 | Batch/processing corrections should be judged by the FPR they deliver | DEBIAS-M https://doi.org/10.1038/s41564-025-01954-4 ; MMUPHin https://doi.org/10.1186/s13059-022-02753-4 ; ConQuR https://doi.org/10.1038/s41467-022-33071-9 | These papers evaluate AUROC/AUPRC and batch-mixing; none reports the FPR at a fixed cut-off. The recommendation is new, and the methods were not run (disclosed). |
| C5 | Site-local label-free burn-in lowers mean FPR error but not tail risk, and fails across sub-sites | Roschewitz 2023 https://doi.org/10.1038/s41467-023-42396-y ; Qiu 2026 SACSIM https://doi.org/10.1093/biomtc/ujag138 ; Yilmaz & Heckel arXiv:2210.04166 ; Kalan et al. arXiv:2511.06641 | Label-free operating-point correction is established (imaging, NP, conformal). **New:** an empirical map, for microbiome tests in three diseases, of where it works (within a site) and where it breaks (other sub-site, neighbouring cohort). |
| C6 | Order-statistic rule bounds the expected FPR for prevalence up to π_max | Lei 2018; Bates 2023; Bashari 2025 arXiv:2502.04807; Tong 2018 | Correctly credited and explicitly not claimed as new. |
| C7 | Clinical analogues: local reference-interval verification and model updating | Ozarda 2018; refineR/kosmic; Janssen 2008; Van Calster 2023 | Cited accurately apart from "in the same way" (concern 2). |

## Concerns

1. **MINOR: credit [9] for the health-index finding, not only for poor transfer.** Line 126 concedes the health-index
   literature via [11, 12]. Lines 140–142 still credit Poyet [9] only with "predictors trained on industrialised
   populations transfer poorly". Coverage of the Poyet work (GMbC) reports that a Western-built health index scored a
   median of ~0 in non-industrialised populations because its markers were absent. That is the same direction as the
   T2D/CRC non-westernised over-flagging reported here.
   *Resolution:* change [9]'s clause to "...and that health-index markers learned in industrialised populations are
   scarce elsewhere [9, 11]". Keep "we add the size of the effect on the FPR..." as written.

2. **MINOR: "in the same way" overstates the analogy to indirect reference intervals (lines 183–184).** refineR and
   kosmic fit a parametric (Box–Cox normal) model to the non-pathological part of a mixed distribution. They do not use
   an order statistic with a prevalence bound.
   *Resolution:* "Laboratory medicine likewise derives reference limits from routine, partly abnormal results [26, 27]".

3. **MINOR: [8] is characterised incompletely (lines 56 and 182).** CRC-TrustBench also shows that Platt scaling,
   evaluated without outer-test labels, lowered the cross-country Brier score (0.180→0.169) and log-loss. Conformal
   coverage fell below target. "Lose calibration" is therefore true but one-sided, and [8] is the closest
   microbiome-specific attempt at label-free recalibration.
   *Resolution:* line 56: "...lose calibration, which Platt scaling only partly restores, and conformal coverage across
   countries [8]". Line 182 can stay as it is.

4. **MINOR (optional citations): label-free threshold adaptation.** Two close methodological works are not cited:
   test-time recalibration of conformal thresholds from unlabelled target data (Yilmaz & Heckel, arXiv:2210.04166), and
   NP classification under shift of both classes (Kalan et al., arXiv:2511.06641, ICLR 2026). Neither changes the
   novelty claim, because the rule is already credited as not new. Adding one would strengthen line 62 ("have also been
   proposed for medical imaging [17] and for Neyman–Pearson classifiers [18]").

5. **MINOR: absolute novelty phrasing (line 65).** "What has not been shown..." should be hedged as "To our knowledge,
   it has not been shown...". My search supports the claim but cannot prove a negative.

6. **MINOR (reference hygiene).** [24] is still an arXiv preprint; Crossref finds no published version, so it is
   acceptable as cited. [9] has no volume or pages yet (Crossref, 2026-11-24); update it at proof stage.

I found no over-claiming in the title, highlights, graphical summary or conclusion. Each limits the burn-in to the
average error within a site, reports that tail risk is not removed, and reports the cross-site failure. I found no
fabricated or mis-attributed citation.

## Sources checked

Searches (WebSearch):
1. Microbiome classifier specificity/FPR on external healthy cohorts at a fixed threshold.
2. SIAMCAT control augmentation and disease specificity (full text checked on bioRxiv v2).
3. DEBIAS-M / MMUPHin / ConQuR cross-study prediction benchmarks.
4. Label-free threshold recalibration with conformal / Neyman–Pearson methods and an unlabelled target (Yilmaz & Heckel;
   Kasa; arXiv:2605.20956, which concerns conformal triage under prevalence shift, needs labels and is not relevant).
5. NP classification with an unlabelled target (Kalan et al. 2025; SACSIM).
6. Clinical prediction model updating and recalibration in a new setting (Binuya review; Steyerberg).
7. Gut microbiome disease classifiers in non-industrialised populations (GMbC/Poyet preprint 10.1101/2025.10.20.683358).
8. Gut health or dysbiosis index cut-offs across countries (GMHI, GMWI2, q2-predict-dysbiosis).
9. Indirect reference intervals from routine data (refineR, kosmic).
10. Thresholds for CRC metagenomic classifiers across countries.

Crossref checks: title, venue, volume, pages and date matched for [3], [4], [6], [9], [10], [13]–[18], [21]–[23], [25],
[26], [28]–[30]. I also read the abstracts of [8] and [18], which support their sentences. arXiv check: [24] exists with
the stated title.
