# Referee report, round 7: novelty and related work (manuscript_v8.md)

**Score:** 8/10
**Decision:** Accept after minor revision.

## Summary judgement

v8 is honest about what is and is not new, and the one novelty-relevant concern I can still raise is minor.
The framing throughout is careful: the burn-in order-statistic rule is stated to be "not new" and credited to
split-conformal and contaminated-reference work [22–25]; control augmentation is framed as a disagreement
("behaved differently here"), not a refutation; DEBIAS-M is an "untested competitor"; and the claim that the
burn-in "held" is now correctly narrowed to average error, with tail risk (P(FPR>0.15)) reported as not removed.
The N2 fix from r6 landed — line 184 distinguishes probability recalibration across countries [8] from FPR at a
fixed cut-off. The E2 fix landed ("Grey band"). My independent search found no published work that reports
fixed-threshold FPR for microbiome disease classifiers cohort by cohort across general healthy populations with
I²/prediction intervals, so the central contribution stands.

The core contributions remain new as far as I can find:
- per-cohort fixed-cut-off FPR heterogeneity (I² 70–95%, PI up to 1–63%) across 32–35 general healthy populations
  with proper heterogeneity statistics;
- a pre-specified taxon decomposition of the score shift for three disease classifiers;
- a head-to-head showing site-local burn-in beats borrowed references (pooled, nearest-neighbour, same-country,
  augmentation), plus a map of where the burn-in breaks (cross-site, neighbouring cohort).

## Claim → closest prior work → exact difference

| # | Claim (v8) | Closest prior work | Exact difference |
|---|---|---|---|
| C1 | Fixed-cut-off FPR varies widely across healthy populations (I² 70–95%, PI 1–63%) | Wirbel 2021 SIAMCAT https://doi.org/10.1186/s13059-021-02306-1 ; Zhang 2026 CRC-TrustBench https://doi.org/10.3389/fmicb.2026.1971707 | SIAMCAT reports elevated type-I error / loss of disease specificity on external controls, no heterogeneity statistics, no healthy-population frame. CRC-TrustBench is CRC-only, reports AUROC/Brier/log-loss, not per-cohort FPR dispersion with I²/PI. **New.** |
| C2 | Over-flagged populations lack the training cohorts' "health-marker" taxa | Poyet 2026 *Cell* https://doi.org/10.1016/j.cell.2026.10.016 ; Gupta 2020 GMHI https://doi.org/10.1038/s41467-020-18476-8 | GMHI/industrialisation literature already shows health markers are rare/absent in non-industrialised populations (GMHI median ~0). Manuscript adds per-population FPR, a pre-specified taxon decomposition for 3 disease classifiers, Asian IBD over-flagging. **Partly new**; mechanism overlaps (Concern 1). |
| C3 | Borrowed cut-offs (same-country, augmentation) do not restore FPR | Wirbel 2021 (augmentation largely removed the excess) | Manuscript finds no mean gain (P=0.58), IBD-only benefit, mostly when the same population is in the pool. **New and fair.** |
| C4 | Processing-bias corrections should be judged by delivered FPR | DEBIAS-M https://doi.org/10.1038/s41564-025-01954-4 ; ConQuR https://doi.org/10.1038/s41467-022-33071-9 ; MMUPHin | These report AUROC/AUPRC only; recommendation is **new**; none run (disclosed), all cited. |
| C5 | Site-local label-free burn-in restores FPR; borrowed/cross-site do not | Roschewitz 2023 https://doi.org/10.1038/s41467-023-42396-y ; Qiu 2026 SACSIM https://doi.org/10.1093/biomtc/ujag138 ; CRC-TrustBench [8] | Method established, manuscript says so. **New:** empirical map of where it breaks for microbiome tests across 3 diseases at a fixed cut-off. |
| C6 | Order-statistic rule bounds expected FPR up to π_max | Bates 2023; Bashari 2025 arXiv:2502.04807; Tong 2018 | Correctly credited, not claimed new. |
| C7 | Health indices apply one cut-off across cohorts | Gupta 2020 GMHI; Chang 2024 GMWI2; Hiseni 2026 | Cited [10–12], accurate. |

## Concerns

1. **MINOR (prior-work acknowledgment, carried from r6-N1): the health-marker mechanism is already known and
   should be conceded in one clause.** Lines 131–133 attribute over-flagging to training "health marker" taxa being
   scarcer, and lines 141–143 credit Poyet [9] only with "predictors transfer poorly" plus "we add ... the taxa that
   carry it." My search confirms the absence-of-health-markers mechanism is already documented (GMHI median ~0 in
   non-industrialised populations; industrialisation reshapes the community). The taxon-by-FPR decomposition for
   *disease* classifiers is genuinely additive, but the sentence reads as if the mechanism itself were new.
   *Resolution:* one clause, e.g. "that health-index markers are scarce in non-industrialised populations is known
   [9, 11]; we show the same mechanism sets the FPR of specific disease classifiers and name the taxa." The response
   log (N1) declined this because the *Cell* abstract could not be opened; the GMHI reference [11], already in the
   manuscript, supports the concession independently, so the gate has been removed.

2. **MINOR: "non-westernised" over-flagging is framed as a novel disease-classifier finding but closely parallels GMHI.**
   The T2D/CRC non-westernised result (lines 119–121, 136–139) is sound and pre-specified/post-hoc as labelled, but a
   half-sentence noting that GMHI already flagged healthy non-industrialised people as "dysbiotic" would place it and
   underline that the novelty is the *per-test FPR magnitude*, not the direction.

No over-claiming found beyond these. Title, highlights, abstract and conclusion are matched to the evidence base
(7–13 populations, two multi-site studies); hedging is consistent ("in the cohorts we could test"). No fabricated or
mis-attributed citation found.

## Citations spot-checked (Crossref, this round)

Verified existing and matching their sentences, exact title + venue + date: [8] Zhang 2026 CRC-TrustBench
(*Front Microbiol*, 25 Sep 2026), [9] Poyet 2026 (*Cell*, Nov 2026 — published record confirmed), [10] Hiseni 2026
(*Gut Microbes*, Jul 2026), [18] Qiu 2026 SACSIM (*Biometrics*, Jul 2026), [28] Austin 2025 DEBIAS-M
(*Nat Microbiol*, Mar 2025). Consistent with prior rounds' verification of [3], [11], [12], [17], [23], [30], [31].

## Sources checked (8 search phrasings + Crossref)

1. microbiome classifier FPR/specificity external healthy cohorts at fixed threshold
2. SIAMCAT control augmentation / type-I-error control on external controls
3. DEBIAS-M / MMUPHin / ConQuR batch-correction prediction benchmark 2026
4. label-free threshold recalibration under shift, conformal / Neyman–Pearson 2025 (Yilmaz & Heckel; Kasa ECP)
5. clinical prediction model recalibration, intercept update, new setting (Steyerberg/Binuya/Van Calster)
6. microbiome prediction bias in non-industrialised populations (GMbC; GMHI median ~0)
7. gut health index fixed cut-off across countries (GMHI/GMWI2/Hiseni)
8. indirect reference intervals from routine lab data (refineR, kosmic)
Plus Crossref verification of 5 newest DOIs (all resolved and matched exactly).
