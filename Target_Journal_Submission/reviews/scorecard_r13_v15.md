# Blind scorecard r13: manuscript v15 (handling editor)

Scale and anchors: `journal_selection/benchmark_v2/scorecard.md` (10 dimensions, 1–10, P75 from 12 benchmark iMeta
papers). The v2 anchors are defined in that file itself; `benchmark_v3/scorecard_v3.md` uses a different 8-dimension 1–5
scale and gives no P75 per dimension, so v2 is used. Scored blind: earlier scorecards were not read.
Materials: manuscript_v15.md, figures_v15 (all PNG), graphical abstract v15, supporting_information_v15.md,
si_tables_v15.md, fprcal (tests 13/13 pass; CLI run, including `score` end-to-end).

| # | Dimension | P75 | Score | Evidence (one line) |
|---|---|---|---|---|
| 1 | Biological / clinical significance | 8.0 | **8** | Shows that a fixed cut-off's FPR, the number that sets colonoscopy/referral load, is population-specific for 14 diseases, and that a released index mislabels healthy cohorts. |
| 2 | Scale and breadth of data | 8.0 | **8** | 36 strict populations / 6,525 people / 20 countries (full set 55 / 8,160), 26 training cohorts, plus 8,069 GMWI2 training samples and a 10,986-person retraining; one database and one pipeline keep it from 9. |
| 3 | Novelty vs prior art | 7.0 | **7** | First field-wide measurement of FPR heterogeneity at fixed cut-offs and a quantified audit of a released index; the spectrum effect and conformal burn-in are known, as the text says. |
| 4 | Methodological rigor and statistics | 7.25 | **8** | Time-stamped pre-specified plans with reported falsifications, I²/τ/prediction intervals, clustered bootstrap CIs, Holm, full-set and covariate sensitivity, corrected bootstrap code; post hoc choices labelled. |
| 5 | External validation | 7.0 | **8** | Every classifier scored only in populations it never saw; GMWI2 tested on 15 unseen populations; leave-one-study-out retraining; cross-site burn-in failure reported and explained. |
| 6 | Resource / tool value | 5.75 | **6.5** | Installable `fprcal` (5 commands, tests, plan table, 14 shipped LASSO models, atlas lookup); but `score` gives ~97% flags with the species-only input its README describes, and no public DOI or web tool yet. |
| 7 | Figure quality and visual story | 7.0 | **7** | Fig 1 map + heatmap + intervals is strong and panel titles are finding-style; no design schematic, Fig 2B lacks the band the text tests, Fig 3 is light, graphical abstract has overlapping text. |
| 8 | Clarity, framing and writing | 7.25 | **7** | One-sentence problem and a memorable number, 1,822 words; but the title's "the same test ... 0–77%" is inaccurate for any single test, an undefined band/"these twelve" in the GMWI2 paragraph, and many statistics per sentence. |
| 9 | Reproducibility and openness | 7.25 | **7** | All inputs public, exact metadata file deposited, code and plans committed, pinned package versions, 13 tests; source data still v12 for changed v15 figures, no Python version/lock file or REPRODUCE guide, "species" mis-describes the all-rank features, URL/DOI placeholders. |
| 10 | Actionable insight / mechanism | 7.0 | **8** | Mechanism tested by retraining (gap 0.52 → 0.06) and a concrete local fix evaluated on held-out non-random splits (−62%, 28/28), with its cost and failure mode stated; retrospective only. |
| | **Total (of 100)** | 69.25 | **74.5** | |

**Below P75:** dimension 8, clarity (7 vs 7.25), and dimension 9, reproducibility (7 vs 7.25). All other dimensions are
at or above P75; 4, 5 and 10 are clearly above it, 6 is above it by a small margin.

**Cheapest gains (in order of effort):**
1. *Clarity, +0.5 to +1 (minutes):* fix the title (plural tests or a real single-test range such as IGT 9–77%), define
   the 0.10–0.31 band and the "twelve", replace "Beta law"/π_max/"full set 28/28" shorthands with words, and move 5–8
   secondary numbers to SI S2.1.
2. *Reproducibility, +0.5 to +1 (an hour):* `source_data_v15/` covering every v15 panel, S1 and the graphical abstract;
   `REPRODUCE.md` mapping figures/tables/numbers to scripts; `environment.yml` with the Python version; correct
   "species" → all-rank clades. The GitHub + Zenodo DOI (author action) adds a further point.
3. *Resource, +0.5 (an hour):* make `fprcal score` fail loudly on missing higher-rank features (or aggregate from
   lineage strings), fix the README, add a test; a tagged release with DOI (author action).
4. *Figures, +0.5:* a small design/workflow schematic in Fig 1A or Fig 3, the band in Fig 2B, and a schematic graphical
   abstract.
