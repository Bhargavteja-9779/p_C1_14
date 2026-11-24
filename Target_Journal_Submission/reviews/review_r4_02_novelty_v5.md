# Referee report (round 4): novelty and related work, manuscript_v5

**Score:** 8/10
**Decision:** Accept with minor revision.

## Overall assessment

The empirical contribution is genuine and, to my search, unduplicated: no prior paper measures the realised
false-positive rate (FPR) of fixed-cut-off microbiome classifiers population-by-population across dozens of
general-population healthy cohorts, reports it with I²/τ and prediction intervals, decomposes the drift to taxa, and
then pits cohort-borrowed corrections against a site-local, label-free re-threshold. v5 has closed the six v4 novelty
concerns. SIAMCAT's external-control FPR finding ("more than doubled") is now stated and its disagreement with the
augmentation result is discussed; the clinical-updating and label-free-recalibration literatures are cited
(Janssen 13, Van Calster 14, Roschewitz 15, Qiu/SACSIM 16, Leeflang 11); CRC-TrustBench (8) and Poyet (9) are restored;
DEBIAS-M (26) is corrected to label-free-on-test-batch; the title is softened to a conditional ("at the site of use")
and the burn-in failure across sites is foregrounded. The paper is honest about its own misses (48% vs pre-stated 50%,
7-population locked base, Holm survivors).

**Reference integrity.** I re-verified the newer/at-risk DOIs on Crossref: CRC-TrustBench (8, Front Microbiol 2026,
vol 17), Hiseni (10, Gut Microbes 2026), Qiu/SACSIM (16, Biometrics 2026), Bates (21, Ann Stat 2023), Mei (4, Nat Med
2024), DEBIAS-M (26, Nat Microbiol 2025). All resolve; authors, journals and years match. I opened the DEBIAS-M full
text: it uses no test-set labels, allows test samples into the cross-batch similarity terms (default transductive), and
reports only AUROC/AUPRC, no fixed-threshold FPR — exactly as the manuscript now states. The v4 reviewer confirmed the
other 20 DOIs. No fabricated or mis-supported citation found.

## Claim → closest prior work → exact difference

| # | Claim (v5) | Closest prior work (opened) | Exact difference |
|---|---|---|---|
| C1 | FPR dispersion of fixed-cut-off microbiome tests across general healthy cohorts, with heterogeneity stats, is unshown | Wirbel 2021 SIAMCAT, https://doi.org/10.1186/s13059-021-02306-1 | SIAMCAT measured external-control FPR study-by-study and found >2× inflation, but no healthy-population focus, no I²/prediction interval, no mechanism, smaller scale. Now correctly cited and narrowed. |
| C2 | Over-flagged populations lack the training cohorts' "health-marker" taxa | Poyet 2025 GMbC, https://doi.org/10.1101/2025.10.20.683358 (bioRxiv, abstract) | GMbC shows industrialised-trained predictors are "uninformative" in less-industrialised cohorts, generally. Manuscript adds per-cohort FPR size and the taxon decomposition. Appropriately cited as [9]. |
| C3 | Cohort-borrowed corrections, incl. control augmentation, do not fix the cut-off | Wirbel 2021 (augmentation "did not strongly depend on controls used") | Manuscript finds no mean gain (P=0.58), benefit only when the same population is pooled — a direct, acknowledged contradiction of SIAMCAT's robustness claim. Fair. |
| C4 | DEBIAS-M/MMUPHin/ConQuR "should be judged by the FPR they deliver" | Austin 2025 DEBIAS-M, https://doi.org/10.1038/s41564-025-01954-4 (full text) | DEBIAS-M is label-free on the test batch and reports only AUROC. Manuscript now states this and lists it as an untested competitor it could not run. Accurate. |
| C5 | Site-local ~100-person label-free re-threshold works; borrowed references fail | Roschewitz 2023 UPA, https://doi.org/10.1038/s41467-023-42396-y; Qiu 2026 SACSIM | The label-free re-threshold idea is established and now cited ("The rule is not new"). New part is the microbiome-specific breakage map (sub-site, cross-cohort, contamination). Fair. |
| C6 | Fixed universal cut-offs applied across many cohorts lack per-site FPR diagnosis | Gupta 2020 GMHI (10.1038/s41467-020-18476-8); Chang 2024 GMWI2 (10.1038/s41467-024-51651-9) | Health indices apply one fixed cut-off across cohorts and report accuracy, not FPR heterogeneity. Closest "fixed cut-off across cohorts" precedent, **not cited.** See concern 1. |
| C7 | Burn-in order statistic controls FPR under contamination up to π_max | Bates 2023 (21); Bashari 2025 (22); Tong 2018 (23) | Correctly cited; "not new" claim appropriate. |

## Concerns

1. **MINOR — closest fixed-cut-off precedent uncited.** GMHI (Gupta 2020) and GMWI2 (Chang 2024) are the nearest prior
   work in which a *single fixed cut-off* is deployed across many cohorts; they are in the authors' own novelty map at
   closeness 2 and are absent. They do not do heterogeneity statistics or per-site re-thresholding, so the narrowed
   novelty claim survives, but a reader expects one sentence placing them. *Resolve:* add a half-sentence noting that
   health-index classifiers (GMHI, GMWI2) use a universal cut-off without per-site FPR diagnosis.

2. **MINOR — Highlight overstates augmentation.** Highlight 3 says control augmentation "helped only when the same
   population was in the pool," but the body reports it helped the IBD tests on average (0.103→0.064–0.067) regardless.
   The *largest* gain needed the same population; "only when" contradicts the body. *Resolve:* reword to "helped most
   when the same population was in the pool."

3. **MINOR — prescription rests on a thin base.** The abstract/title prescribe site-of-use recalibration, but the
   positive within-site evidence is 7–13 populations and two multi-site studies, and only one Holm survivor is a
   burn-in comparison. This is disclosed in the body and limitations, so it is not over-claiming, but the graphical-
   abstract sentence "Recalibrating on about 100 unlabelled people from the same site did [restore the target]" reads
   more definitively than the hedged text. *Resolve:* add "in the cohorts we could test" to that sentence, matching the
   conclusion's wording.

4. **MINOR — Poyet (9) is a preprint carrying a substantive claim.** The transfer-failure statement leans on a
   non-peer-reviewed bioRxiv source. It is labelled bioRxiv, which is adequate, but a one-clause "(preprint)" in text
   would be cleaner given it supports the paper's central "why."

5. **MINOR — label-shift ancestry.** The ComBat-style feature alignment (Fig 3A) has a direct ML ancestry in
   generalized-target-shift / label-shift adaptation (Saerens 2002; Zhang 2013), listed at closeness 3–4 in the
   authors' map but uncited. Because v5's core method is a conformal order statistic rather than an affine score-shift
   model, this is not load-bearing; optional single citation if space allows. Not required.

No MAJOR concerns remain.

## Papers opened (this round)

- Full text: DEBIAS-M (PMC10888995); SIAMCAT control-augmentation figures/text (Genome Biology).
- Crossref records verified: CRC-TrustBench (8), Hiseni (10), SACSIM (16), Bates (21), Mei (4), DEBIAS-M (26).
- Abstract/summary: Roschewitz UPA (Nat Commun 2023, PMC10587231); Poyet GMbC (Broad/news summaries, bioRxiv 2025);
  reference-interval indirect-verification literature (CCLM); Yilmaz & Heckel label-free conformal recalibration
  (arXiv 2210.04166).
- Search phrasings (9): FPR/specificity transfer across cohorts; SIAMCAT control augmentation twofold; DEBIAS-M/
  MMUPHin/ConQuR benchmark; label-free operating-point drift medical imaging; Neyman–Pearson/conformal FPR control from
  unlabeled target; CRC-TrustBench cross-country calibration; reference-interval verification from routine data;
  industrialization gut-microbiome predictor transfer; GMHI/GMWI2 fixed cut-off (map cross-check).
