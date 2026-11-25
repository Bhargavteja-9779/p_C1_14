# Scorecard r9 — manuscript_v11 (Reviewer 3, handling editor, iMeta)

Scored blind on the 10 anchors of `journal_selection/benchmark_v2/scorecard.md`, as written, from the manuscript text,
the two v11 figures, the Supporting Information files that ship with it (`supporting_information.md`,
`si_tables_v11.md`) and the released tool (`code/tool`, 11/11 tests pass). Prior reviews and responses were not read
before scoring. Integer scores, as for the 12 benchmark papers. The paper is scored as it would be submitted today
(placeholders count as missing).

| # | Dimension | Score | Benchmark P75 | At/above P75? | Evidence (one line) |
|---|---|---|---|---|---|
| 1 | Biological / clinical significance | 7 | 8.0 | **No** | Shows that a published cut-off can mean 0–77% FPR depending on where it is used, which matters for every microbiome diagnostic study; but the 28 classifiers are the authors' research models (several near or below chance), not tests in use, so it falls short of "changes how a common test is used". |
| 2 | Scale and breadth of data | 9 | 8.0 | Yes | 6,525 healthy adults, 36 populations, 20 countries, 26 training cohorts, 14 diseases, plus a 55-population / 8,160-person full set; larger and more diverse than imt2.169 (19 cohorts, 6 countries, scored 8). |
| 3 | Novelty vs prior art | 7 | 7.0 | Yes (at) | First per-population FPR map across many tests and populations; partly anticipated by Wirbel 2021 (external controls double CRC FPR) and the burn-in rule is openly borrowed from conformal / reference-interval practice. |
| 4 | Methodological rigor and statistics | 8 | 7.25 | Yes | Time-stamped analysis plans with falsification criteria, random-effects I² and prediction intervals, crossed random-effects decomposition, confounder adjustment, full-set sensitivity, exact Beta/binomial laws, failed hypotheses reported; held back from 9 by the post hoc strict set, below-chance classifiers kept in "28/28" claims, no CI on the headline −62%, and one numeric error (PI upper end 0.34 vs 0.22 in the data). |
| 5 | External validation / cross-cohort generalisation | 8 | 7.0 | Yes | Every classifier is scored in 32–36 unseen populations, a replication on 19 extra populations (failed, reported), cross-site burn-in failure reported; the fix itself is validated only within site (13 populations), so not a 9. |
| 6 | Resource / tool value for readers | 7 | 5.75 | Yes | Installable, MIT-licensed `fprcal` with CLI, 4 commands, Monte-Carlo unit tests and a queryable 14 × 2 × 36 atlas; but it ships no trained models (a site cannot score its own samples with these tests), is not on PyPI/Zenodo, has no repository URL in the paper, and one test (`test_plan_monotone`) asserts nothing. |
| 7 | Figure quality and visual story | 7 | 7.0 | Yes (at) | Fig 1 = map + 14 × 36 heatmap + prediction intervals + AUROC scatter, clean and in reading order; no study-design schematic, Fig 2 has no schematic of the burn-in, unlabelled rows in 2B, and the sensitivity cost and cross-site failure are not shown. |
| 8 | Clarity, framing and writing | 8 | 7.25 | Yes | One-sentence problem, ALL-CAPS finding-sentence headings, plain language, "0% to 87%" and "−62%" stick; minus internal inconsistencies ("pre-registered" vs "not external pre-registrations", abstract 87% vs text 77%, "our earlier analysis" never defined). |
| 9 | Reproducibility and openness | 7 | 7.25 | **No** | Inputs public and versioned (curatedMetagenomicData 2021-03-31 / 2022-10-19), code, scores and plans exist; but the repository URL and Zenodo DOI are placeholders, the SI Methods file describes the earlier CRC-only design rather than the atlas, and Tables S9–S23 point to a different file (si_tables_v4.md). |
| 10 | Actionable insight / mechanism | 8 | 7.0 | Yes | Delivers a concrete, hold-out-tested fix (label-free burn-in: 0.101 → 0.038 mean error, 28/28 classifiers) plus a verification rule with power analysis; not 9 because it fails across sites, halves sensitivity when patients enter the burn-in, and has no prospective or time-ordered test. |
| | **Total** | **76** | **69.25** | Yes | Second only to imt2.70192 (78) in the benchmark; above the benchmark median (63.5) by 12.5 points. |

## Below P75
- **Dimension 1 (7 vs 8.0):** move by applying the atlas to at least one published or externally trained classifier
  (for example the SIAMCAT CRC model or the Piccinno 2025 CRC signature) and by stating the referral burden in numbers
  (extra colonoscopies per 10,000 screened at the observed FPR range).
- **Dimension 9 (7 vs 7.25):** move by filling in the GitHub URL and Zenodo DOI, replacing the SI Methods with the atlas
  (v5) methods, putting Tables S9–S23 in the submitted SI file and depositing figure source data.

## Against the stated target ("clearly above P75 on 4, 5, 6 and 10")
Met: 4 (+0.75), 5 (+1), 6 (+1.25), 10 (+1). Only 6 is clearly above; 4 is within one point.
Not met: "at or above P75 on every dimension" (1 and 9 below; 3 and 7 exactly at P75).
