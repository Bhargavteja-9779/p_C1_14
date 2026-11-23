# Round 1 — triage and response (editor, statistics, domain, citation audit)

| # | Issue (source) | Action |
|---|---|---|
| 1 | Conformal success near-tautological; no test with mismatched calibration (editor, stats M1, domain 2) | Added calibration with controls from another centre/cohort (Table S9; Fig 2 orange): FPR 0.02–0.28, worst pair 100% > 0.15. Same-site result now called a best case. |
| 2 | Single-site variability under-reported (stats M2) | New control-budget analysis (theory + large cohorts; Fig 3B, Table S10): 95% range 0.01–0.26 at n=19, 0.05–0.17 at n=99. Recommendation changed from 20 to ~100 controls. |
| 3 | OOF-vs-refit score mismatch may create drift (stats M3) | Matched fold-ensemble scoring: drift persists (75% out of band; Table S6). |
| 4 | Over-dispersion test wrong hypothesis; P-values overstated (stats M4) | Replaced by test of equal proportions (Table S2); CRC shared bias reported as such (P=0.12); deviation listed. |
| 5 | EM a straw man (stats M5) | Explained why prevalence correction cannot change FPR in principle; degenerate variant moved to SI. |
| 6 | Pool quantile only tested at 65–89% cases; works at screening prevalence (stats M6, domain 4) | Simulated screening pools (Table S11); now presented as a valid label-free route at low prevalence. |
| 7 | Batch-correction claim too broad (domain 6, stats M7) | Added percentile normalisation (Table S8); claim restricted; DEBIAS-M/MMUPHin named as untested. |
| 8 | Control definitions, confounders (domain 1, 5) | Cohort characteristics (Table S7); MetaCardis healthy-only analysis; depth not explanatory; HMP2 symptomatic controls discussed. |
| 9 | Harm numbers: abstract misstated, no uncertainty, adenoma carriers, FIT (domain 3, stats M13) | Abstract rewritten; 95% ranges in Fig 3A; labelled illustrative; adenoma positivity added; FIT question stated as out of scope. |
| 10 | "≥30 controls / 95% rule" recommendation useless (domain 7) | Removed; rule described as too conservative at small n; n ≥ 29 stated consistently. |
| 11 | Overclaims; unreported adverse results; number mismatches (editor 3, stats checklist) | All 6 mismatches fixed; sensitivity costs and in-band shares reported. |
| 12 | Data overlap adenoma/CRC dev cohorts (editor 4, stats M12) | Disclosed in Conclusion and SI. |
| 13 | Deviations not declared (stats M8, M10) | "Deviations from the protocol" section added (SI + protocol.md). |
| 14 | Citation fixes 1–9 (audit) | GLOBOCAN removed; Wirbel/CRC-TrustBench described precisely; Roschewitz and Gibbons re-described; STORMS and Lei 2018 added; renumbered in order. |
| 15 | Title/pitch (editor 2) | Retitled around drift and AUROC; "Twenty" removed. |
| 16 | sklearn version dependency (stats minor 1) | Version pinned; L1 active verified (101/544 non-zero). |
| — | Not done (stated as limitations) | MMUPHin/ConQuR/DEBIAS-M, SIAMCAT pipeline, boosting model, second profiler, CD/UC split, temporal drift, FIT benchmark, placeholders (authors' input needed). |
