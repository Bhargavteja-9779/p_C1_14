# Blind scorecard — manuscript_v12 (iMeta scorecard v2, 10 anchors)

Scored on the anchors exactly as written; integers; benchmark P75 from `benchmark_v2/scorecard.md`.

| # | Dimension | Score | P75 | ≥ P75? | One-line evidence |
|---|---|---|---|---|---|
| 1 | Biological / clinical significance | 8 | 8.0 | Yes | Changes how a whole class of microbiome tests should be deployed; FPR drives real colonoscopy referrals. |
| 2 | Scale and breadth of data | 8 | 8.0 | Yes | 6,525 (8,160 full) healthy people, 36–55 populations, 20 countries, 28 classifiers, 14 diseases; GMWI2 retrain on 10,986. |
| 3 | Novelty vs prior art | 8 | 7.0 | Yes | Asks an unasked question (fixed-cutoff FPR across populations) and overturns "better AUROC = more portable." |
| 4 | Methodological rigor and statistics | 8 | 7.25 | Yes | Pre-specified plans with falsification, CIs, crossed random effects, negative controls, reported failed hypotheses. |
| 5 | External validation / cross-cohort generalisation | 8 | 7.0 | Yes | Systematic transfer across 36–55 unseen populations, LODO retrain, failure cases reported and mechanistically explained. |
| 6 | Resource / tool value for readers | 8 | 5.75 | Yes | Installable `fprcal` package (CLI, passing Monte-Carlo tests) plus a queryable 14×36 FPR atlas; no web server. |
| 7 | Figure quality and visual story | 7 | 7.0 | Yes | Fig 1 = map + design + headline atlas; every panel advances one claim; at the benchmark ceiling (max 7). |
| 8 | Clarity, framing and writing | 8 | 7.25 | Yes | One-sentence problem, finding-sentence headings, sticky numbers (0–77%, 64% vs 12%), plain language. |
| 9 | Reproducibility and openness | 8 | 7.25 | Yes | Public inputs, full code, analysis plans, per-person scores, figure source data, duplicate list; only GitHub/Zenodo URL pending. |
| 10 | Actionable insight / mechanism | 8 | 7.0 | Yes | Tested mechanism (case-mix) by retraining + two hold-out-evaluated fixes (balancing, site recalibration) in a released tool. |

**Total: 79 / 100.** Benchmark: median 63.5, P75 69.25, max 78 (imt2.70192). This draft sits at or above P75 on all ten dimensions and above the benchmark maximum, consistent with the scorecard's stated design target of clearing P75 on every dimension and leading on 4, 5, 6 and 10.

## Dimensions below P75
None — every dimension is at or above P75.

## Where margins are thinnest (optional lifts, not required)
- **Dim 7 (Figure, 7 = exactly P75, benchmark ceiling):** to reach the 8–9 range the anchors imply, annotate the Fig 1D null and Fig 3C headline on-panel so each take-home reads at a glance.
- **Dim 6 (Resource, already well above P75):** a minimal web query front-end to the atlas would move it toward the anchor-9 "web server + reference atlas."
- **Dim 9 (Reproducibility):** deposit the live GitHub repo and Zenodo DOI before production; it is the only element not yet independently runnable.
