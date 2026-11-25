# Round 12 triage and response (manuscript v14 -> v15), 2026-11-25

Reports: statistics 8/10 minor (no MAJOR); novelty 8/10 minor, 22/25 (1 MAJOR); editor 7.5/10 minor (5 MAJOR, editorial);
blind scorecard 76 (only dimension 8, clarity, below P75: 7 vs 7.25). First round with all three at accept/minor after
round 11 (stats major) -> round 13 is needed for two clean rounds in a row.
New files: manuscript_v15.md, supporting_information_v15.md, si_tables_v15.md, figures_v15/ (scripts:
atlas/v5/make_fig_atlas_v15.py, atlas/v6/make_fig_gmwi2_v15.py, atlas/v5/make_fig_site_v15.py). Number audit v15:
109/109 matched (logs/audit_manuscript_v15.md.txt). fprcal tests 13/13.

## Editor (r12-03)
| Item | Action |
|---|---|
| M1 B2 overstated; B4 vs "spread barely changed" | Fixed text: "point estimate (88%) met the criterion ... CI of the relative reduction (41–149%) includes values below it"; B4 stated as met on the logit scale only; East Asian median after reweighting (0.29) said to stay above training FPR. |
| M2 strict/full denominators; Fig 2B set | Strict-set numbers in text (0.38 vs 0.06, P = 0.020; full 0.38 vs 0.20, P = 0.065; posthoc_eastasia_strict_v15.json). Fig 2B now shows the 15 unseen strict populations only. |
| M3 regional wording, batch confounding, courtesy | Title now one claim about the test, no region. Heading: "...mislabels healthy East Asian cohorts through its training data". Added: "properties of the model and its training data, not evidence that East Asian microbiomes are less healthy"; country travels with laboratory/extraction/sequencing. Right of reply to GMWI2 developers: AUTHOR ACTION (listed in HANDOFF; cannot be done by the agent). |
| M4 statements, repository, DOI, pinned env | AUTHOR ACTION (placeholders kept). requirements.txt already pins versions. |
| M5 length | Main text 2,590 -> 1,827 words; summary 158 -> 89 words, 4 numbers. RF variance decomposition, AUROC restriction, within-study AUROC, binomial power numbers moved to SI S2.1. Fig 3 reduced to two panels (burn-in vs training; sensitivity price); old 3A/3C -> Supporting Figure S1. Kept three main figures (Fig 3 is two panels). |
| m1 "stated" FPR | "training FPR (0.21)" throughout text, SI S6.1 and Fig 2. |
| m2 Fig 1D | Axis "out-of-fold AUROC"; AUROC < 0.6 shown as open symbols. RF colour changed to violet (no orange overloading). |
| m3 Fig 3 "646 evaluations" | Explained in legend. |
| m4 Fig 3D | Now Fig 3B: points labelled by burn-in case share; training cut-off shown once; x-axis "FPR"; PAC series moved out (in S4). |
| m5 table numbering / file refs | SI header v15, points to si_tables_v15.md; Methods says S1–S25. |
| m6 SI citation numbers | SI uses main-text numbering ([16] for GMWI2); stated in SI header. |
| m7 Klebsiella; 39% | Sentence added (pathobiont); legend states five largest explain 39%. |
| m8 "non-westernised" | Defined in Fig 1 legend as the database metadata term. |
| m9 summary claims | Summary says "within a site ... retrospective"; sensitivity size in main text (0.46 -> 0.21–0.23). |
| m10 tool docs | README lists `score` with input format and "research use only"; CLI docstring lists score. Tagged release: AUTHOR ACTION (with Zenodo). |
| m11 determinism, paths | run_v6c.py liblinear seeded (random_state=0); absolute paths removed from posthoc_eastasia*.py and code/scripts/* (only the frozen v12/v14 figure scripts keep them). Re-run of posthoc_eastasia_strict_v15.py gives identical output. |
| m12 ethics | Expanded (open licence, no re-identification, country labels from metadata, not ethnicity). |
| m13 refs | Ref 13 (Poyet 2026, Cell, no volume yet) dropped to save space; others unchanged. imt2.70088 not added (vaginal microbiota; weak fit). |
| m14 graphical abstract | Summary text revised; image: open (next step). |
| Figures | Panel titles shortened, heatmap labels enlarged (6.5 pt), colour-bar title matches legend, IGT interval clipped at 0.001 with arrow, Fig 2D training-FPR line and 0.29 annotation. Design schematic: not added (space); graphical abstract to carry it. |

## Novelty (r12-02)
| Item | Action |
|---|---|
| MAJOR 1 spectrum effect | New sentence and ref [8] Leeflang et al. 2013 CMAJ (DOI verified, all five authors checked on Crossref). Claim reframed: "Clinical epidemiology has long known ... Microbiome studies have not measured it." |
| MINOR 1 FIT precedent | Not added (length; ref [7] already covers FIT thresholds). |
| MINOR 2 GMHI direction | "Low health-index scores in populations that lack the training markers were reported before [19] ... we add its size for a released index and a test by retraining." |
| MINOR 3 prior-shift lineage | "a split-conformal argument [20, 21] that, through π_max, is a simple prior-shift correction [22]". |

## Statistics (r12-01)
| Item | Action |
|---|---|
| m1 strict vs full East Asian | Fixed (as editor M2). |
| m2 Fisher P < 1e-300 in SI S6.4 | Removed; SI says why no P value is given. |
| m3 G2 direction; alpha | Main text: "Eight of these twelve fell below the band and four above it"; SI S2.1 notes alpha = 0.208 is the training FPR raised by East Asian studies. |
| m4 H2 wording | "not met (inconclusive for LASSO, falsified for RF)", consistent with SI S5 grading. |
