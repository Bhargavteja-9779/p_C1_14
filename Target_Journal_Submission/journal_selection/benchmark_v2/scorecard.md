# iMeta scorecard v2 (10 dimensions, 1-10)

Scores for 12 representative benchmark papers are in `benchmark_scores.csv` (with a one-line evidence note per paper).
They are judgement scores made from the retrieved abstracts and Europe PMC full texts, not editor ratings; use them to
see where the bar sits, not as exact values. Percentiles use linear interpolation over the 12 papers
(`scripts/09_scores.py`).

Papers scored: imt2.212, imt2.70123, imt2.70192, imt2.70088, imt2.268, imt2.169, imt2.70004, imt2.70008, imt2.70011,
imt2.70079, imt2.183, imt2.70090.

## 75th percentile per dimension

| # | Dimension | Median | **P75** | Max | Top example |
|---|---|---|---|---|---|
| 1 | Biological / clinical significance | 7.5 | **8.0** | 8 | imt2.183, imt2.70192, imt2.70011 |
| 2 | Scale and breadth of data | 8.0 | **8.0** | 9 | imt2.70192 (2,896 studies) |
| 3 | Novelty vs prior art | 7.0 | **7.0** | 8 | imt2.70192, imt2.70004 |
| 4 | Methodological rigor and statistics | 6.0 | **7.25** | 9 | imt2.183 (HR+CI, MR), imt2.268 |
| 5 | External validation / cross-cohort generalisation | 7.0 | **7.0** | 8 | imt2.212 (transfer matrix + LODO), imt2.70011 |
| 6 | Resource / tool value for readers | 3.0 | **5.75** | 9 | imt2.70011 (package + web tool) |
| 7 | Figure quality and visual story | 7.0 | **7.0** | 7 | several |
| 8 | Clarity, framing and writing | 7.0 | **7.25** | 9 | imt2.70192 |
| 9 | Reproducibility and openness | 6.5 | **7.25** | 9 | imt2.70192, imt2.70004 (Code Ocean) |
| 10 | Actionable insight / mechanism | 6.0 | **7.0** | 8 | imt2.70192, imt2.70011 |
| | **Total (of 100)** | 63.5 | **69.25** | 78 | imt2.70192 |

Target for our paper: at or above P75 on every dimension, and clearly above it on 4, 5, 6 and 10 where the benchmark
is weak and our design is strong (fixed-threshold FPR in 36 healthy populations, label-free fix, released tool).

## Dimension anchors

**1. Biological / clinical significance**
- 3: Descriptive association in one small setting; unclear who would use it.
- 6: Relevant disease, plausible clinical use, but effect or population narrow.
- 9: Changes how a common test, biomarker or practice should be used; affects many patients or many studies.

**2. Scale and breadth of data**
- 3: One cohort, < 200 samples, one country.
- 6: Several hundred to ~2,000 samples, 2-5 cohorts or one large multi-centre cohort.
- 9: Thousands of samples or dozens of cohorts/populations across many countries, or a field-wide census.

**3. Novelty vs prior art**
- 3: Re-runs a known analysis on new data with the expected result.
- 6: New angle or new combination of known methods; result partly anticipated.
- 9: Asks a question the field has not asked, or overturns a widely held assumption, with evidence.

**4. Methodological rigor and statistics**
- 3: p-values only, no correction, no confounder handling, single split.
- 6: Multiple-testing control, cross-validation, standard tests; confounders mentioned.
- 9: Pre-specified design, effect sizes with CIs, sensitivity analyses, confounder/meta-analytic modelling, negative controls.

**5. External validation / cross-cohort generalisation**
- 3: Internal CV only.
- 6: One external cohort, or pooled multi-cohort without leave-one-out.
- 9: Systematic transfer across many cohorts (train x test matrix, LODO), with failure cases reported and explained.

**6. Resource / tool value for readers**
- 3: Nothing reusable beyond accessions.
- 6: Code and derived tables on GitHub; a reusable score or reference table.
- 9: Installable package or web server with documentation, plus a reference atlas others can query.

**7. Figure quality and visual story**
- 3: Many small generic panels without a clear sequence.
- 6: Clear panels, one schematic, logical order.
- 9: Fig 1 tells the whole study at a glance (map + design + headline result); every panel advances one claim.

**8. Clarity, framing and writing**
- 3: Gap unclear; headline buried.
- 6: Standard intro; headline stated but hedged.
- 9: One-sentence problem, one number that sticks, finding-sentence headings, plain language.

**9. Reproducibility and openness**
- 3: Data "on request", no code.
- 6: Accessions + some scripts.
- 9: All inputs public or listed, full code and environment (GitHub/Zenodo/Code Ocean), figure source data.

**10. Actionable insight / mechanism**
- 3: Ends at association.
- 6: Suggests an application or a mechanism without testing it.
- 9: Delivers a concrete, tested fix or intervention (experimentally or by prospective/hold-out evaluation).

## Per-paper scores (copy of benchmark_scores.csv, order of dimensions 1-10)

| DOI | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| imt2.212 | 7 | 5 | 6 | 6 | 8 | 3 | 7 | 8 | 5 | 6 | 61 |
| imt2.70123 | 8 | 6 | 7 | 7 | 7 | 3 | 7 | 7 | 5 | 7 | 64 |
| imt2.70192 | 8 | 9 | 8 | 6 | 6 | 8 | 7 | 9 | 9 | 8 | 78 |
| imt2.70088 | 8 | 8 | 6 | 7 | 7 | 5 | 7 | 8 | 6 | 7 | 69 |
| imt2.268 | 7 | 8 | 7 | 8 | 7 | 3 | 6 | 6 | 7 | 5 | 64 |
| imt2.169 | 7 | 8 | 6 | 6 | 6 | 3 | 7 | 6 | 7 | 5 | 61 |
| imt2.70004 | 7 | 8 | 8 | 6 | 5 | 8 | 7 | 6 | 8 | 7 | 70 |
| imt2.70008 | 7 | 8 | 7 | 6 | 5 | 3 | 6 | 7 | 7 | 6 | 62 |
| imt2.70011 | 8 | 7 | 6 | 6 | 8 | 9 | 7 | 6 | 8 | 8 | 73 |
| imt2.70079 | 8 | 6 | 6 | 8 | 5 | 2 | 7 | 7 | 5 | 6 | 60 |
| imt2.183 | 8 | 8 | 7 | 9 | 7 | 2 | 5 | 7 | 4 | 6 | 63 |
| imt2.70090 | 7 | 5 | 7 | 6 | 7 | 2 | 7 | 6 | 5 | 6 | 58 |

## How to use
Score our draft on the same anchors before submission. Any dimension below P75 is a revision target. Dimension 6
(resource) has the widest spread (2-9): a small, documented calibration package plus the 14 x 36 FPR table is the
cheapest way to move from median to top quartile.
