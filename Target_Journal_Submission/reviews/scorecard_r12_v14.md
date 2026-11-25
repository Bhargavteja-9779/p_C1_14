# Scorecard r12 — manuscript_v14 (Reviewer 3, handling editor, iMeta)

Scored blind (prior scorecards not consulted) against `journal_selection/benchmark_v2/scorecard.md`, anchors as written.
Inputs read: manuscript_v14.md, figures_v14/*.png, supporting_information_v14.md, si_tables_v12.md, code/tool (13/13 tests
pass; `fprcal atlas/plan/cutoff/verify/score` run).

| # | Dimension | Score | P75 | At/above P75? | Evidence (one line) |
|---|---|---|---|---|---|
| 1 | Biological / clinical significance | 8 | 8.0 | yes (=) | Shows a fixed cut-off flags 0–77% of healthy people by population and that a published, released health index labels 64% of healthy East Asian vs 12% other people non-healthy; relevant to every microbiome screening test, but not yet shown to change a deployed clinical test. |
| 2 | Scale and breadth of data | 8 | 8.0 | yes (=) | 6,525 healthy adults/36 populations/20 countries (8,160/55 full set), 26 training cohorts, plus GMWI2's 8,069 samples/54 studies and 10,986-person retraining; all from one database and one profiler (MetaPhlAn3), so not a field-wide census. |
| 3 | Novelty vs prior art | 7 | 7.0 | yes (=) | Population-by-population FPR at a fixed cut-off across diseases and the audit of a deployed index are new; country confounding (SIAMCAT) and the burn-in/conformal rule are known and openly credited. |
| 4 | Methodological rigor and statistics | 8 | 7.25 | yes | Time-stamped falsifiable plans, DerSimonian–Laird I²/τ/prediction intervals, crossed random effects, clustered bootstrap CIs, Holm, failed hypotheses reported (G3, B3, H2, H3); held back from 9 by a post hoc strict set, corrected bootstrap bugs, an uninterpretable v6c arm and B2 CI that crosses its own criterion. |
| 5 | External validation / cross-cohort generalisation | 8 | 7.0 | yes | Every classifier is scored only in populations it never saw (489 pairs), GMWI2 in 15 unseen populations, leave-one-study-out retraining, and failure cases reported (cross-site burn-in, references, control augmentation). |
| 6 | Resource / tool value for readers | 7 | 5.75 | yes | `fprcal` installable package (CLI: atlas/verify/cutoff/plan/score; Monte-Carlo tests pass) + 14x36 FPR atlas + LASSO coefficient tables; no web server, and the public URL/DOI is still a placeholder. |
| 7 | Figure quality and visual story | 7 | 7.0 | yes (=) | Fig 1 = map + 14x36 heatmap + prediction intervals + AUROC-vs-τ (strong atlas), Fig 2 four-step GMWI2 story, Fig 3 site fix; but no design schematic, three figures for a Letter, tiny heatmap labels, and some label/text mismatches (Fig 1D axis, Fig 2B population set). |
| 8 | Clarity, framing and writing | 7 | 7.25 | **no** | Finding-sentence headings and plain sentences, but a 21-word two-claim title, a 158-word summary carrying ~9 numbers, and a dense results text in which the headline number competes with dozens of secondary statistics. |
| 9 | Reproducibility and openness | 8 | 7.25 | yes | Public inputs with release dates, deposited metadata file with hash, code, plans, per-person scores, duplicate list, coefficient check (95/95) and tool; repository URL/Zenodo DOI not yet given, liblinear unseeded in one script, scripts hard-code local paths. |
| 10 | Actionable insight / mechanism | 8 | 7.0 | yes | Label-free burn-in cut FPR error 62% (28/28 classifiers) and 79% for GMWI2 in non-random hold-out splits; mechanism tested by retraining (gap 0.52 to 0.06); retrospective only, sensitivity cost stated, cross-site use fails. |
| | **Total** | **76** | 69.25 | above | Above benchmark P75 total; below the benchmark max (78). |

**Below P75:** dimension 8 (Clarity, 7 vs 7.25). Dimensions only at P75 (no margin): 1, 2, 3, 7.

**Cheapest gains:** shorten the title to one claim and trim the summary to 3–4 numbers (dim 8); add a small design
schematic to Fig 1 or the graphical abstract and fix the label mismatches (dim 7); add the GitHub URL + Zenodo DOI and a
pinned environment (dims 6 and 9).
