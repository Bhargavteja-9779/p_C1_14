# Scorecard — Reviewer 3 (handling editor), manuscript_v13.md

Scored blind against the iMeta benchmark v2 anchors (`benchmark_v2/scorecard.md`). Benchmark P75 and "at/above P75?"
shown per dimension (12-paper benchmark; P75 by the benchmark's own interpolation).

| # | Dimension | Score | Evidence (one line) | P75 | ≥ P75? |
|---|---|---|---|---|---|
| 1 | Biological / clinical significance | 7 | Shows a fixed cut-off flags 0–77% of healthy people and a published index mislabels whole regions; a relevant, plausible clinical use (CRC screening → colonoscopy), but microbiome tests are not yet deployed at scale, so impact is largely on how the field should report and use tests rather than on patients today. | 8.0 | No |
| 2 | Scale and breadth of data | 8 | 28 classifiers / 14 diseases across 36 strict (55 full) healthy populations, 6,525–8,160 people, 20 countries, plus the 8,069-sample GMWI2 training set re-audited — dozens of cohorts across many countries. | 8.0 | Yes |
| 3 | Novelty vs prior art | 8 | Asks a question the field has not: specificity at a fixed cut-off has never been mapped across healthy populations; overturns the assumption that a good held-out AUROC implies a portable operating point, with evidence (ρ = −0.06). | 7.0 | Yes |
| 4 | Methodological rigor and statistics | 8 | Pre-committed analysis plans with falsification criteria, failed hypotheses reported, effect sizes with clustered CIs, crossed random-effects variance decomposition, I²/prediction intervals, a corrected-bootstrap erratum (S6.6) — near the top anchor; one key plan (v6c) honestly flagged post hoc. | 7.25 | Yes |
| 5 | External validation / cross-cohort generalisation | 8 | Systematic transfer across 36 populations with LODO cut-offs, a train×test FPR atlas, and failure cases reported and explained (cross-site burn-in fails; balancing fails on the FPR scale); GMWI2 audited in 15 unseen populations. | 7.0 | Yes |
| 6 | Resource / tool value for readers | 8 | Installable, tested Python package (`fprcal`: cutoff/verify/plan/atlas/score CLI, 12 Monte-Carlo tests pass) shipping the 14 LASSO atlas classifiers and per-population FPR table; no web server, so short of the full "9". | 5.75 | Yes |
| 7 | Figure quality and visual story | 7 | Three clear, well-sequenced figures (world map, FPR atlas heatmap, prediction intervals, mechanism, site fixes); each panel advances one claim, but Fig 1 lacks the study-design/test schematic that is the iMeta Fig-1 norm, so it does not quite tell the whole study at a glance. | 7.0 | Yes |
| 8 | Clarity, framing and writing | 8 | One-sentence problem, finding-sentence ALL-CAPS headings, numbers that stick (0–77%, 64% vs 12%, 88%, 62%/79%), plain active voice; only the two-clause title and dense "Here we" paragraph hold it below 9. | 7.25 | Yes |
| 9 | Reproducibility and openness | 8 | All inputs public and versioned (release dates + SHA-256), full code, time-stamped analysis plans in git, per-person scores, duplicate list, figure source data, released tool; held below 9 only because the GitHub/Zenodo location is still a placeholder at review. | 7.25 | Yes |
| 10 | Actionable insight / mechanism | 8 | Delivers a concrete, tested fix (label-free local burn-in: mean |FPR−α| 62% lower, 28/28 classifiers; 79% for GMWI2) and tests the mechanism by retraining — but all site-level evidence is retrospective hold-out, not prospective. | 7.0 | Yes |
| | **Total (of 100)** | **78** | | **69.25** | |

**Totals.** Draft total 78/100 vs benchmark median 63.5 and P75 69.25; equals the benchmark top paper (imt2.70192, 78).

**Below P75:** Dimension 1 (significance), 7 vs 8.0 — the only dimension under the bar.

**At/above P75:** Dimensions 2, 3, 4, 5, 6, 7, 8, 9, 10 (9 of 10). Clearly above P75 on the four target dimensions the
benchmark flagged as weak and our design strong: 4 (rigor), 5 (validation), 6 (resource), 10 (mechanism/fix).
