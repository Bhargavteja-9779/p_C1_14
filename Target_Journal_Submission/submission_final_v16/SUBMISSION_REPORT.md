# Submission report: manuscript v16 for iMeta (Letter / Short Communication)

**Title:** Gut-microbiome disease classifiers flag 0–87% of healthy people at the same cut-off, depending on the population

## 1. What the paper shows
1. **Atlas.** 28 classifiers (LASSO and random forest) for 14 diseases, scored in 36 healthy general-population cohorts
   (6,525 adults, 20 countries). At a cut-off set for a 10% false-positive rate (FPR), the FPR ranged from 0% to 87%
   (cohorts of ≥ 100 people). The spread exceeded sampling noise for all 28 classifiers (I² median 0.94). AUROC did not
   predict the spread (ρ = −0.06).
2. **Audit of a released index.** GMWI2 labelled 64% of healthy people in its own East Asian training studies as
   non-healthy, against 12% elsewhere. In 15 unseen populations, 12 fell outside the pre-specified band. Retraining the
   published recipe reproduced the gap, and reweighting by country × label cut it from 0.52 to 0.06.
3. **Site fix.** A known order-statistic burn-in rule on 100 unlabelled local people cut the within-site FPR error by
   62% (0.101 → 0.038; 28/28 classifiers). It failed across sites and costs sensitivity. Released as `fprcal`
   (19 tests pass).

## 2. How it improved (independent reviews, 10-point scale, three reviewers per round)

| Round (version) | Statistics | Novelty | Editor | Blind score /100 | Status |
|---|---|---|---|---|---|
| r3 (v4) | 7 | 6 | 5 | — | major revision |
| r5 (v6) | 7 | 8 | 7.5 | — | minor revision |
| r8 (v9) | 7 | 8 | 8 | — | minor revision, no MAJOR |
| r10 (v12) | 6 | 8 | 8 | 79 | statistics: major (bootstrap code errors found) |
| r12 (v14) | 8 | 8 | 7.5 | 76 | minor revision, first fully clean round |
| r13 (v15) | 7.5 | 7.5 | 7.5 | 74.5 | minor revision (title, citation and tool items) |
| **r14 (v16, final)** | — | — | **send to review** | **75** | required items fixed in this package |

Benchmark: 12 published iMeta papers, median 63.5 and 75th percentile (P75) 69.25 on the same 10-dimension scale.

Main improvements from earlier drafts to v16:
- **Scope.** The paper moved from one disease (CRC) to an atlas of 14 diseases in 36 healthy populations. It added an
  audit of a published, released index (GMWI2), and the mechanism was tested by retraining.
- **Honesty of claims.** Plans were time-stamped before running. Failed hypotheses are reported (H2 inconclusive or
  falsified, G3 falsified, B3 failed). Post hoc analyses are labelled. Two bootstrap code errors were found and
  corrected. A flawed v6c analysis is marked uninterpretable rather than used.
- **Novelty positioning.** The burn-in rule is stated as known, with credit to conformal prediction, Neyman-Pearson
  classification, lab-medicine reference limits and medical-imaging drift correction (Roschewitz 2023). The cut-off
  design is credited to Wirbel 2019, and microbiome precedents are cited (SIAMCAT, He 2018, Poyet 2026). The novelty
  claim now rests on what is new: breadth, heterogeneity statistics, the AUROC non-relation, and the audit of a released
  index.
- **v16-specific fixes (round 13 and 14):**
  - Accurate title (0–87% across classifiers, with the near-chance IGT example flagged).
  - Corrected burn-in splits and population counts.
  - GMHI mis-citation removed.
  - Sidedness of tests stated.
  - Band defined and drawn in Figure 2B.
  - Graphical abstract without overlapping labels.
  - `fprcal score` handles all-rank clades and refuses silently wrong inputs.
  - Figure source data rebuild pixel-identically.
  - REPRODUCE.md and environment.yml added.
  - Version and review-round language removed from the SI.

## 3. Comparison with published iMeta papers (same 10-dimension scale)

| Paper (iMeta) | Type | Data | Key strength | Score /100 |
|---|---|---|---|---|
| Degregori et al. 2026, *A decade-scale audit of microbiome AI-readiness* (imt2.70192) | Letter | 2,896 studies audited | field-wide census + tool; no new wet-lab data | 78 |
| **This manuscript (v16)** | Letter | 36 healthy populations, 6,525 people; 28 classifiers; GMWI2 audit | per-population FPR atlas, released-index audit, tested tool, pre-specified plans | **75** |
| iMLGAM, pan-cancer immunotherapy response (imt2.70011) | Research article | 1,242 patients + in-house cohort | R package + web tool, wet-lab validation | 73 |
| Nationwide vaginal microbiota in Chinese women (imt2.70088) | Letter | 6,423 women, 18 provinces; 13 external datasets | scale + prospective validation | 69 |
| Two gut microbiome guilds predict liver tumour class (imt2.70123) | Research article | 196 new metagenomes + 2 external cohorts | new data, mechanism | 64 |
| Universal oral microbiome signature for periodontitis (imt2.212) | Research article | 8 cohorts, 341 samples | cohort-transfer matrix, LODO | 61 |

The closest analogue is the AI-readiness audit (imt2.70192). It is a Letter, uses only public data, and gives a
field-level methodological message with a tool. This is the same kind of paper as ours, and iMeta published it in 2026.
Like the periodontitis signature (imt2.212), our paper tests transfer across cohorts. Unlike it, we measure the
operating point (FPR) instead of AUROC, which is exactly the gap imt2.212-style papers leave open. Our paper sits
second among the benchmark set.

## 4. Why it can be accepted at iMeta, and the risks

**For acceptance:**
- **It fits iMeta's scope.** Microbiome data science with a translational message, in the Letter format iMeta
  publishes quickly (Letter median 33 days from receipt to acceptance).
- **It gives a clear, quotable message.** The same cut-off flags 0–87% of healthy people, and AUROC does not warn.
  This has direct consequences for benchmark reporting, for developers and for sites.
- **It is above the benchmark P75 on 8 of 10 dimensions.** Rigour, external validation, reproducibility and
  actionable insight are each 8 against a P75 of 7–7.25.
- **It audits a released, used index.** Editors value this kind of finding, and the paper states clearly that it is a
  property of the model, not of East Asian microbiomes.
- **It is fully reproducible from public data,** with pre-specified plans, a fresh-clone rerun, and a tested tool.

**Risks** (final editor's estimate: about 45% acceptance overall, about 60% once sent to review):
- **Novelty can be read as incremental.** The spectrum effect and conformal burn-in are known, and the paper says so.
- **All evidence is retrospective** and comes from one public resource and one pipeline (MetaPhlAn3). Country is
  confounded with laboratory.
- **The GMWI2 finding is sensitive.** The developers should be given a right of reply before submission.
- **Significance and clarity sit just below P75** (7 vs 8; 7 vs 7.25).

These figures are model-based estimates from independent simulated reviews, not a guarantee. Real acceptance depends
on the handling editor and the external reviewers.

## 5. Author actions before submission
See README.md: author list, CRediT, COI, funding, AI-use statement, public repository + Zenodo DOI + tagged `fprcal`
release, right of reply to the GMWI2 developers, suggested reviewers, and a final check of the current iMeta Letter
guidelines.
