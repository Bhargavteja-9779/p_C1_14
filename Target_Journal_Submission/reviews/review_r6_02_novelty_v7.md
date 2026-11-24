# Referee report, round 6: novelty and related work (manuscript_v7.md)

**Score:** 8/10
**Decision:** Accept after minor revision.

## Summary judgement

v7 resolves the one MAJOR concern from r5. Reference [9] (Poyet et al.) is now cited as the published
*Cell* record (doi:10.1016/j.cell.2026.10.016; Crossref confirms: *Cell*, Nov 2026); the "preprint" bullet is gone
from Limitations; ConQuR is now cited [31]; CRC-TrustBench [8] is credited for calibration/conformal loss across
countries. The novelty framing is honest throughout: the burn-in rule is stated to be "not new," control augmentation
is framed as a disagreement rather than a refutation, and DEBIAS-M is an "untested competitor."

The core contributions remain new as far as I can find:
- per-cohort fixed-cut-off FPR heterogeneity (I² 70–95%, prediction intervals up to 1–63%) across 32–35 general
  healthy populations, with proper heterogeneity statistics;
- a pre-specified taxon-level decomposition of the score shift for three disease classifiers;
- a head-to-head showing site-local burn-in beats borrowed references (pooled, nearest-neighbour, same-country,
  augmentation), plus a map of where the burn-in breaks (cross-site, neighbouring cohort).

No published work reports fixed-threshold FPR for microbiome disease classifiers cohort by cohort across general
healthy populations. Two residual prior-work acknowledgments remain (both MINOR, both easy).

## Claim → closest prior work → exact difference

| # | Claim (v7) | Closest prior work | Exact difference |
|---|---|---|---|
| C1 | Fixed-cut-off FPR varies widely across healthy populations (I² 70–95%, PI up to 1–63%) | Wirbel 2021 SIAMCAT https://doi.org/10.1186/s13059-021-02306-1 ; Zhang 2026 CRC-TrustBench https://doi.org/10.3389/fmicb.2026.1971707 | SIAMCAT showed external-control FPR >doubled, no heterogeneity stats, no healthy-population frame. CRC-TrustBench is CRC-only, reports AUROC/Brier/log-loss, not per-cohort FPR dispersion with I²/PI. **New.** |
| C2 | Over-flagged populations lack the training cohorts' "health-marker" taxa | Poyet 2026 *Cell* https://doi.org/10.1016/j.cell.2026.10.016 | Poyet: industrialised-trained predictors uninformative in less-industrialised cohorts, GMHI collapses because health markers are rare/absent. Manuscript adds per-population FPR, a pre-specified taxon decomposition for 3 disease classifiers, and Asian IBD over-flagging. **Partly new**; mechanism overlaps (Concern 1). |
| C3 | Borrowed cut-offs (same-country, augmentation) do not restore FPR | Wirbel 2021 (augmentation largely removed the excess) | Manuscript finds no mean gain (P=0.58), gains only for IBD, mostly when the same population is in the pool. Clear disagreement. **New and fair.** |
| C4 | Processing-bias corrections should be judged by delivered FPR | Austin 2025 DEBIAS-M https://doi.org/10.1038/s41564-025-01954-4 ; Ling 2022 ConQuR https://doi.org/10.1038/s41467-022-33071-9 ; Ma 2022 MMUPHin | These report AUROC/AUPRC only. Recommendation is **new**; none run (disclosed). Now all cited. |
| C5 | Site-local label-free burn-in restores FPR; borrowed/cross-site do not | Roschewitz 2023 UPA https://doi.org/10.1038/s41467-023-42396-y ; Qiu 2026 SACSIM https://doi.org/10.1093/biomtc/ujag138 ; CRC-TrustBench | Method established, manuscript says so. **New:** empirical map of where it breaks for microbiome tests. CRC-TrustBench already tried label-free recalibration for microbiome CRC (Concern 2). |
| C6 | Order-statistic rule bounds expected FPR up to π_max | Bates 2023 https://doi.org/10.1214/22-AOS2244 ; Bashari 2025 arXiv:2502.04807 ; Tong 2018 | Correctly credited, not claimed new. |
| C7 | Health indices apply one cut-off across cohorts | Gupta 2020 GMHI; Chang 2024 GMWI2; Hiseni 2026 | Cited [10–12], accurate. |

## Concerns

1. **MINOR (prior-work acknowledgment): the Poyet mechanism overlap is still understated.** The "WHY" heading is
   "Health markers of the training population are rarer elsewhere" — exactly the mechanism Poyet reports for GMHI
   (health markers rare/absent in non-industrialised populations). The text (lines 149–151) credits Poyet only with
   "predictors transfer poorly" and claims "we add ... the taxa that carry it." The taxa-by-FPR decomposition for
   disease classifiers is genuinely additive, but the sentence should name that Poyet already identified the
   absence-of-health-markers mechanism, to avoid the appearance of claiming it.
   *Resolution:* one clause, e.g. "Poyet et al. showed health-index markers are scarce in non-industrialised
   populations [9]; we show the same mechanism sets the FPR of specific disease classifiers and name the taxa."

2. **MINOR: CRC-TrustBench [8] is the closest microbiome label-free precedent and the burn-in section omits it.**
   Line 62 credits [8] for calibration/conformal loss across countries, but the "WHAT WORKED" section never notes that
   CRC-TrustBench already tested label-free Platt scaling / conformal sets for microbiome CRC. That is the nearest
   prior art to the burn-in.
   *Resolution:* one clause where the burn-in is introduced, stating that [8] attempted label-free recalibration for
   CRC and that the difference here is FPR at a fixed cut-off across three diseases, not probability calibration.

No over-claiming found beyond these. Title, highlights, abstract and conclusion are matched to the evidence base
(7–13 populations, two multi-site studies); hedging is consistent ("in the cohorts we could test").

## Citations spot-checked (Crossref, this round)

Verified existing and matching their sentences: [3] Piccinno 2025 (*Nat Med*, Jun 2025), [8] Zhang 2026
CRC-TrustBench (*Front Microbiol*, Sep 2026 — title/venue confirmed), [9] Poyet 2026 (*Cell*, Nov 2026 — now
correctly the published record), [10] Hiseni 2026 (*Gut Microbes*, Jul 2026), [11] Gupta 2020 GMHI (*Nat Commun*),
[12] Chang 2024 GMWI2 (*Nat Commun*), [17] Roschewitz 2023 (*Nat Commun*), [18] Qiu 2026 SACSIM (*Biometrics*, 2026),
[23] Bates 2023 (*Ann Stat*), [28] Austin 2025 DEBIAS-M (*Nat Microbiol*, Mar 2025). No fabricated or mis-attributed
citation found.

## Sources checked (8 web searches + Crossref)

1. microbiome classifier FPR/specificity external healthy cohorts at fixed threshold
2. SIAMCAT control augmentation external controls false positives cross-disease
3. DEBIAS-M / MMUPHin / ConQuR batch-correction prediction benchmark 2026
4. label-free operating-point recalibration, imaging / Neyman–Pearson / conformal (UPA, conformal triage)
5. clinical prediction model updating / recalibration in a new setting (Steyerberg, STRATOS)
6. gut microbiome classifier geographic/industrialisation bias, non-industrialised transfer
7. gut health index fixed cut-off / dysbiosis index across countries (located Poyet *Cell* coverage)
8. indirect reference intervals from routine lab data (refineR, kosmic, contamination)
Plus Crossref verification of 14 DOIs (all resolved and matched).
