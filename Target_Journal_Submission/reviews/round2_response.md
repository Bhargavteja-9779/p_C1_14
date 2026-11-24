# Response to review round 2 (manuscript v3 -> v4), 2026-11-24
All v4 numbers come from code/experiments/atlas/v4/results/ (plan: v4/protocol_v4.md, written before running; deviations D1-D4).

## Statistics report (MAJOR REVISION)
| # | Concern | Action | Where |
|---|---|---|---|
| 1 | Beta-binomial law true by construction; 2 of 3 criteria fixed by N, M | Claim dropped; random-split fit described as a code check. Added pre-stated non-exchangeable tests (age/BMI/sex halves, accession order, sub-sites, neighbouring cohort). H-NX1 NOT supported (48% < 50%); H-NX2 supported. | v4 "Random splits check the code"; Fig 3B; summary_v4.json |
| 2 | Cross-cohort duplicates (ThomasAM_2019_c, DhakanDB~GuptaA, JieZ~QinJ) | Global profile-level dedup (119 samples; ThomasAM_2019_c dropped); everything re-run. GuptaA IBD augmentation fix persists after dedup (remaining DhakanDB people are the same population) - reported. | v4/dedup.py, duplicates.csv |
| 3 | Small cohorts inflate range / out-of-band share | DerSimonian-Laird tau, I2, 95% PI primary; ranges for n>=100; out-of-band excess over binomial expectation; 10th-90th percentiles. | heterogeneity_v4.csv; Results para 1-2 |
| 4 | 38 units = 7 populations; pseudo-replication | Distinct populations reported; population-cluster bootstrap + Wilcoxon on population means. Burn-in vs augmentation now P = 0.22 (4/7), not 0.0004. | summary_v4.json, h2h_v4.json |
| 5 | ICC text wrong | As-specified model (age, sex, BMI, depth) reported: -24% to +28%; extended model labelled deviation (IBD -39 to -50%, others up); populations used 24-27 of 32-35 stated. | covariates_v4.csv |
| 6 | Fold-model vs refit level shift | Checked: pooled FPR moves <= 0.04 (CRC LASSO 0.044 vs 0.037). | heterogeneity_v4.csv cols *_folds |
| minor | PAC infeasible small N; mis-specified pi_max; augmentation harms T2D RF; missing augmentation script; protocol wording; multiplicity | PAC infeasible at N=25 stated in legend; augmentation harm stated; script added (control_augmentation_v4.py); "analysis plans, not pre-registration"; T2D non-westernised labelled post hoc. Multiplicity: open (see below). | |

## Editor report
| # | Concern | Action |
|---|---|---|
| 1 | Circular guarantee validation | As stats 1. |
| 2 | A5 never reported; A4 as specified; cohort counts | A5 reported (local 100% in band vs country reference 22-58%); A4 as specified; counts from counts_v4.json (strict 6,525/36/20; full 8,160/55/27). CONSORT-style flow figure: NOT yet done. |
| 3 | "Explained none" false | Rewritten. |
| 4 | Non-healthy controls | Strict general-population subset primary (20 studies + person rules), full set sensitivity; post hoc choice disclosed. Recruitment-context table: NOT yet done (SI). |
| 5 | Head-to-head buried | In main text + Fig 3A, labelled post hoc, population-level test. |
| 6 | Fig 2B population set changes with N | Fig 3A uses fixed set of 5 locked populations. |
| 7 | Sensitivity cost; PPV; status quo 0.29 vs 0.05 | Sensitivity 0.46 -> 0.21-0.23 and PPV at 1% (1.6% -> 2.6%) in text. Explanation of 0.29 (case-control controls) vs 0.05 (healthy general population): partly addressed (CRC tests conservative in healthy populations). |
| 8 | No batch-correction comparator | Label-free ComBat-style ALIGN added (pre-stated, supported: BURN better 7/7). MMUPHin/ConQuR/DEBIAS-M not run - limitation. |
| 9 | Format | CONCLUSION and ACKNOWLEDGMENTS added; CIs on key numbers. Workflow schematic: NOT done. |
| title / over-claims | Title changed to site-level message; "exact guarantee", "nothing short of it works", "first ~100" (random) wording removed or qualified. |

## Domain report
| # | Concern | Action |
|---|---|---|
| 1 | Non-healthy controls | Strict primary; extremes (0.87) attributed to hospital cohort in text. |
| 2 | Mechanism thin; pre-specified taxon decomposition missing | Reported (Fig 2): IBD over-flags Asian populations via Western health-marker taxa; T2D non-westernised via Enterobacteriaceae etc.; oral share small except CRC. |

## Still open (for round 3)
- SI v4 tables (S1 cohort/recruitment table, S2 heterogeneity, S3 fix attempts, S4 deploy, S6 augmentation, S7 dedup list, S8 taxa), flow diagram, workflow schematic.
- Multiplicity across the many tests (Holm over the family of v4 hypothesis tests) not yet applied.
