# Response to review round 6 (manuscript v7 -> v8), 2026-11-24
Reports: statistics 7/10 minor (r6_01; 1 MAJOR), novelty 8/10 minor (r6_02), editor 7.5/10 minor (r6_03; 2 MAJOR).

| # | Concern | Action in v8 |
|---|---|---|
| S1 MAJOR | "held" rests on MAE only; tail and bias not reported | Text reports mean FPR 0.106 (CI 0.101-0.112) and P(FPR>0.15) 0.135 vs 0.135 for covariate halves; accession 0.111 vs 0.167; combined 0.126 vs 0.146. Claim narrowed in highlights, GA summary and conclusion: average error halved, tail risk not removed. |
| S2 | Holm family = reported only | Holm over all 34 computed P values (holm_v6.csv, Table S10); survivors stated; T2D RF P=0.37 added. |
| S3 | A5 near-tautological, no inference | Local arm labelled "benchmark on random splits"; population-level test 8/8, P=0.0078 (not Holm-significant); removed from the graphical abstract. |
| S4 | India n=29 | n given. |
| S5 | WHY title overgeneralises | Retitled "WHICH TAXA SHIFT THE SCORES"; highlight and Fig 2 title neutral. |
| S6 | PPV spectrum bias | Stated. |
| S7 | Related studies independent | Limitation added (TettAJ a-c outside the strict set). |
| S8 | Augmentation different people | Already stated next to the CI. |
| E1 MAJOR | GA text vs panel (unlabelled vs labelled) | GA panel 2 now shows the unlabelled burn-in vs training cut-off within site (13 populations) and at another cohort (9 populations); summary text matches. |
| E2 MAJOR | Fig 1 legend "orange band" | "Grey band". |
| E3 | Length | 2,918 words (trimmed). |
| E4 | Fig 2 names; Fig 3B count | "sp. CAG-520", Collinsella without brackets; Fig 3B random split uses the 11-population strict set. |
| E5 | README heading; fresh-clone scope | Heading fixed. Fresh-clone test covered the core 5 scripts; full rerun not repeated (noted). |
| N1 | Poyet mechanism | Could not open the Cell abstract (redirect/cookie walls); only the verified preprint claim is cited. Not attributed further. |
| N2 | CRC-TrustBench recalibration | Sentence distinguishes probability recalibration [8] from fixed-cut-off FPR. |
