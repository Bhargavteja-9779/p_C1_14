# Novelty escalation, round 3 (this session, 2026-11-24). Ideas tried so far across all lines: 7 (round 1) + 2 (round 2) + those below.

Scorecard at start of round 3: 12/30 (RECHECK line), weakest = insight/scale and distance from prior work.

| # | Idea | Pre-stated test | Result | Status |
|---|---|---|---|---|
| 10 | Healthy-population FPR atlas (62 cohorts, 3 tests x 2 models) | A1 overdispersion | chi2 P 1e-111 to ~0; 61-70% of populations outside [0.05,0.15]; range 0-0.56 (LASSO CRC) / 0-0.87 (RF CRC) | KEPT (core finding) |
| 11 | Shared over-flagging propensity across tests | A2 rho>=0.3 | rho 0.16-0.38, 1/6 pairs significant | FALSIFIED (reported: drift is test x population specific) |
| 12 | Non-westernised populations over-flagged (CRC) | A3 | CRC no (MW P 0.32 / 0.89); post hoc T2D LASSO yes (0.22 vs 0.11, P=0.005) | FALSIFIED as pre-stated; T2D noted post hoc |
| 13 | Individual covariates explain cohort effect | A4 ICC>=0.10 after adj. | ICC 0.20-0.42 raw, 0.21-0.35 adjusted; between-cohort variance change -24% to +39% | CONFIRMED: cohort effect not explained by age/sex/BMI/depth/diversity |
| 14 | Healthy-context residual threshold (score minus prediction from k healthy PCs) | DEV: lower atlas spread without AUROC loss | spread 0.156 -> 0.139-0.098, but CRC AUROC 0.76 -> 0.68-0.61; RF worse | FALSIFIED |
| 15 | Large pooled healthy reference threshold | DEV LOO | no better than source | FALSIFIED |
| 16 | Composition-matched reference (k nearest populations by CLR-PCA centroid) | DEV LOO vs random-k | not better than random-k | FALSIFIED |
| 17 | Label-free burn-in self-calibration with contamination bound + exact sample-size law | protocol_deploy.md | pending | NEXT |
| 18 | (post hoc, after prior-art check) Control augmentation (Wirbel 2021 Genome Biol): add DEV healthy cohorts as training controls | LOCKED healthy populations, paired | 50 units (n>=70): mean abs error naive 0.070, augmented 0.066 (Wilcoxon P=0.69), burn-in N=50 0.039 (P=0.0004 vs augmented; better in 34/50). In-band 0.42 both. CRC external: augmented FPR Yachida 0.26/0.15, YuJ 0.06/0.06 | FAILS to restore per-population FPR; strongest foil for the paper |

Scorecard after round 3 (honest): problem 4, distance from prior work 3 (per-population scale + cohort partition + head-to-head vs control augmentation new; burn-in guarantee is an adaptation of conformal / NP / indirect RI), evidence 5 (60 cohorts, locked split, pre-registered criterion met, exact-law validation), insight 4, practical 4, rigour 4 => 24/30.
