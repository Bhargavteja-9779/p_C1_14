# Response to review round 5 (manuscript v6 -> v7), 2026-11-24
Reports: statistics 7/10 minor (review_r5_01), novelty 8/10 accept with minor revision (r5_02), editor 7.5/10 minor (r5_03).

| # | Concern | Action in v7 |
|---|---|---|
| S-Holm | 0.022 mislabelled as within-site | Holm re-run over 12 tests incl. post hoc within-site (holm_v5.csv); each survivor labelled with what it shows. |
| S-designs | Within-site designs may be mild | Burn-in error under within-site splits (0.033-0.034) equals random (0.033) - stated, with "may have been mild shifts". |
| S/E-GA | GA local arm mislabelled; "costs sensitivity" from another experiment | GA: "100 labelled local controls", "post hoc", sensitivity note removed (figures_v6). |
| S/E-case mix | "case mix" misleading | Highlight 4: "differed in age, BMI, sex or sampling order". |
| S-near-dups | duplicates below r=0.99 | Post hoc: no clean gap (most best matches r 0.85-0.90); r>0.95 removes 8 more; heterogeneity and the India augmentation repair unchanged (Table S13). |
| S-minor | shift-FPR partly by construction; augmentation on full set; PPV pooled; LASSO-only qualifiers | All stated. |
| N-major | Poyet now in Cell | Citation updated (Crossref-verified); preprint limitation removed; WHY section credits [9] for industrialisation reshaping microbiome; only claims verified from the abstract used. |
| N-minor | CRC-TrustBench recalibration; ConQuR uncited | "calibration and conformal coverage" [8]; ConQuR cited (Ling 2022, ref 31, Crossref-verified). |
| E-minor | strict burn-in sensitivity; italics; Fig 1 colours; worked example; fresh-clone record | Sensitivity 0.13-0.15 in text; italic taxa (Fig 2); grey prediction band (Fig 1); worked example k = 92; fresh-clone log committed (logs/repro_fresh_clone_2026-11-24.log, scripts/repro_fresh_clone.sh). |
| E-title | Fits screening only | Kept "should be recalibrated at the site of use"; scope section limits it to screening. |
