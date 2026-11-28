# Handling-editor pre-submission check: iMeta Letter, manuscript v17

**Manuscript:** "Gut-microbiome disease classifiers flag 0–87% of healthy people at the same cut-off, depending on the population"
**Package checked:** `Target_Journal_Submission/submission_final_v17/`: manuscript_v17.md, supporting_information_v17.md, si_tables_v16.md (Table S3 only), highlights.md, cover_letter_v17.md, all figure PNGs including figureS2_gmhi.png and graphical_abstract_v16.png.
**Also checked:** `code/tool` (fprcal: `python3 -m pytest -q` gives **19 passed**, 66 s), REPRODUCE.md, environment.yml, manuscript/source_data_v16/README.md.
**Independence:** I scored this blind. I did not open any earlier review or scorecard. From `journal_selection/benchmark_v2/scorecard.md` I read only the dimension anchors and the P75 table.
**Date:** 2026-11-28

---

## 1. Editor's summary

This Letter makes three claims, each backed by evidence.

1. **The atlas.** At a cut-off set for an FPR of 0.10, 28 in-house classifiers (14 diseases, LASSO and RF) gave very different false-positive rates across 36 strict healthy populations (6,525 people, 20 countries). I² is 0.64–0.97, and AUROC does not predict the spread (ρ = −0.06).
2. **The audit.** Two released gut-health indices, GMWI2 and GMHI, flag most healthy people in their own East Asian training studies. A pre-specified retraining shows that the training data's geographic case mix can produce this.
3. **The site check.** A known conformal order-statistic burn-in brings the FPR back to target within a site, in retrospective tests. It fails across sites and costs sensitivity.

The question matters for practice. The design is unusually honest: plans were pre-specified, falsified hypotheses are reported, and the authors corrected their own bootstraps. The evidence is broad, and the paper comes with a tested tool and pixel-identical figure rebuilds. It fits iMeta's microbiome data-science scope.

The weak points are presentational and fixable:
- The graphical-abstract summary in the manuscript is visibly broken (a duplicated, contradictory sentence).
- Several front-matter items (title, highlights, cover letter, graphical abstract) are worded more strongly than the hedged main text.
- The author-only placeholders are still open.

None of these problems is scientific.

I re-derived the following from the source data and SI. All match the text:
- Title range 0–0.87. The 0.87 is HF RF in LiuW_2016, n = 110.
- LASSO maximum 0.77.
- 489 LASSO pairs: 45% above 0.15, 24% below 0.05.
- IGT LASSO range 0.09–0.77.
- 6,525 people.
- Variance shares: population 17% of total, 20.2% net of noise; pair 48% + noise 14% = Table S3 pair_share 0.619.
- Eight GMWI2 training studies above 50%, all East Asian; 13 East Asian studies in total.
- Four unseen East Asian populations with FPR 0.25–0.54. YassourM_2016 is KOR adult in the metadata.
- G2 Holm P 1.8 × 10⁻¹²; GMHI α 0.236; sensitivity 0.46 → 0.21–0.23.

---

## 2. Consistency check: title, highlights, graphical abstract, cover letter vs the text

| Item | Statement | Text / SI | Verdict |
|---|---|---|---|
| Title | "flag 0–87% of healthy people at the same cut-off" | 0–0.87 across 28 classifiers in populations ≥ 100 (max = HF RF, LiuW_2016, n = 110) | Correct. But the headline rests on one RF pair from a single-cohort model, and "classifiers" are the authors' own retrained models, not published tests. See R4. |
| Highlight 1 | "0–87% ... across general-population cohorts of at least 100 people (36 cohorts, 6,525 adults, 20 countries)" | Only **15** of the 36 strict populations have ≥ 100 people. 36 / 6,525 / 20 describe the whole strict set (≥ 20 people). | **Misleading parenthetical.** Fix (R3). |
| Highlight 2 | GMWI2 median 64% vs 12%; GMHI 67% vs 21%; pre-specified replication; cut-off shifts with profiling software | Matches (S6, S7). "Retraining linked this" is suitably hedged. | OK |
| Highlight 3 | 62% error reduction within sites, not across sites, cost in sensitivity | Matches (0.101 → 0.038; S4) | OK |
| GA summary (manuscript, lines 7–12) | "Two published gut-health indices, GMWI2 and GMHI, each labelled most ... **A published gut-health index labelled 64% of healthy people ...**" | Duplicated sentence. The first says two indices, the second "a" index. "64% of healthy people" is a **median of study shares**, not a pooled share. "A model artefact **traced to**" overstates the retraining result: the B2 CI of 41–149% includes values below the criterion, and within-country balancing removed only 37% (CI includes 0). | **Error. Must fix (R1).** |
| GA image, panel 2 | "cause: geographic make-up of the training data" | The text says "linked to" and notes that within-country case mix may also contribute | Overclaim. Use "linked to" (R2). |
| GA image, panel 3 | "cut-off from the first 100 local people (no labels)"; "error −62% (28/28)" | The −62% pools three non-random splits (accession order, younger half, leaner half), not only "first 100" | Minor inaccuracy (R2). |
| GA image, panel 1 | "14 LASSO tests; dots = populations of ≥ 100", x-axis to 0.8 | LASSO range 0–0.77. The title's 87% is RF and is not shown. | Acceptable. A reader may notice that the GA does not show the title number. |
| Cover letter | "labelled 64% of healthy people in its own East Asian training studies ... (67% vs 21%)" | These are medians across studies | Say "a median of 64% per study" (R3). |
| Cover letter | "The first cross-disease, cohort-by-cohort map" | Priority claim. Refs 1, 10, 11, 15 cover parts of this. | Soften to "To our knowledge, the first ..." (R3). |
| Cover letter | "a fresh-clone rerun reproduces every result file" | REPRODUCE.md cites a full rerun log (2026-11-24) and a pixel-identical figure rebuild (2026-11-25), both for v16 | Plausible. Version labels need aligning (R7). |
| Package README | Lists `SUBMISSION_REPORT.md` | File not in the folder | Remove the row or add the file (R7). Do not upload internal reports to the journal. |

Other internal checks passed: Figures 2A, 2B, S2A and S2C against the text; the Figure 3B sensitivity values; the I² values; the Holm values; reference and figure numbering.

---

## 3. Scorecard (blind; anchors from benchmark_v2)

| # | Dimension | P75 | **Score** | vs P75 | Basis |
|---|---|---|---|---|---|
| 1 | Biological / clinical significance | 8.0 | **8.0** | at | Changes what cross-cohort benchmarks and released indices should report. Concerns a common use case (screening referrals). |
| 2 | Scale and breadth of data | 8.0 | **8.0** | at | 36 strict and 55 full populations, 6,525 / 8,160 people, 20 countries, 26 training cohorts, plus GMWI2's 8,069-sample training data and GMHI's 2,636 healthy samples. |
| 3 | Novelty vs prior art | 7.0 | **7.0** | at | The spectrum effect and single-disease FPR drift are known (refs 1, 8–14), and the fix is admittedly not new. New: the cross-disease FPR atlas, AUROC ⟂ portability, and the audit of two released indices with a retraining test. |
| 4 | Methodological rigor and statistics | 7.25 | **8.0** | above | Time-stamped plans, falsifications reported (H2, H3, G3, B3, C2/C3), CIs, Holm, corrected cluster bootstraps, sensitivity sets. Docked for the post hoc strict set and post hoc East Asian comparisons (disclosed). |
| 5 | External validation / cross-cohort | 7.0 | **8.0** | above | Leave-one-cohort-out cut-offs, every unseen population, unseen-population GMWI2 test, LOSO retraining. Failure cases (cross-site burn-in, pooled references) are reported. |
| 6 | Resource / tool value | 5.75 | **7.0** | above | fprcal: installable, 19 tests pass, five CLI commands, ships the 14 LASSO models and the queryable atlas, with a clear input-format warning. Not 9: no PyPI/bioconda release or web tool yet, and the repository is not public yet. |
| 7 | Figure quality and visual story | 7.0 | **7.0** | at | Figure 1 (map + heatmap + PIs + AUROC-vs-τ) tells the atlas well. Figures 2 and 3 each advance one claim. Docks: the GA claim text; open squares clipped at the left edge of Fig 1D; the "training FPR 0.24" label overlaps a point in Fig S2A. |
| 8 | Clarity, framing and writing | 7.25 | **6.5** | **below** | Strong: finding-sentence headings, one sticky number. But the GA summary contains a duplicated, contradictory sentence. Paragraphs are dense with parenthetical statistics (e.g. the reweighting paragraph). Front matter is out of step with the main text. |
| 9 | Reproducibility and openness | 7.25 | **8.0** | above | Public inputs, deposited metadata with SHA-256, pinned environment, per-figure source data, pixel-identical rebuild, fresh-clone log. Conditional on the repository going public with a Zenodo DOI before submission. Version labels (v15/v16/v17) are inconsistent. |
| 10 | Actionable insight / mechanism | 7.0 | **7.0** | at | A tested fix (retrospective, non-random within-site splits; it fails across sites) and a retraining test of the mechanism. Not higher: there is no prospective or truly held-out site deployment, and the mechanism is supported on the point estimate only. |
| | **Total** | **69.25** | **74.5** | +5.25 | Above the P75 total and below the benchmark maximum (78). One dimension below P75 (8). |

---

## 4. Decision

**Recommendation: ready to submit after minor, mainly editorial corrections.** As handling editor I would send it to review, not desk-reject it, once R1–R3 are fixed. Do not submit the current files unchanged: R1 is the kind of visible error that costs credibility at triage.

### REQUIRED changes (can be done now, without the authors' personal input)

- **R1. Graphical-abstract summary (manuscript, lines 7–12).**
  - Delete the duplicated sentence "A published gut-health index labelled 64% ... training data."
  - Keep one sentence covering both indices, e.g. "Two published gut-health indices (GMWI2, GMHI) labelled a median of 64% and 67% of healthy people per East Asian training study as non-healthy, against 12% and 21% elsewhere; retraining linked this to the geographic make-up of the training data."
  - Replace "traced to" with "linked to".
- **R2. Graphical-abstract image.**
  - Panel 2: change "cause:" to "linked to: geographic make-up of the training data".
  - Panel 3 subtitle: change to "cut-off from 100 local people (no labels; non-random splits)". The 62% is not specific to "first 100".
  - Rebuild the GA and update the source-data README.
- **R3. Front matter vs text.**
  - Highlight 1: move "(36 cohorts, 6,525 adults, 20 countries)" so it describes the whole atlas. The 0–87% range comes from the 15 populations with ≥ 100 people. Suggested wording: "...in 36 healthy cohorts (6,525 adults, 20 countries), 28 classifiers for 14 diseases flagged 0–87% of healthy people in cohorts of ≥ 100 at a cut-off set for a 10% FPR...".
  - Cover letter: change "labelled 64% of healthy people" to "a median of 64% per study". Change "The first ... map" to "To our knowledge, the first ...".
- **R4. Title.** The title number comes from one RF pair (HF RF in LiuW_2016, n = 110) of a single-cohort model. Either keep it and state in the first Results paragraph that 0.87 is a single pair, which is already partly done, or prefer a robust headline. Suggested: "...flag between 0% and 77% of healthy people (LASSO), or 87% (any model)...". Alternatively: "Fixed cut-offs of gut-microbiome classifiers misstate the false-positive rate in most healthy populations". This is a recommendation. It is required only that the title not imply published clinical tests: consider "Gut-microbiome disease classifiers..." → "Cross-cohort gut-microbiome classifiers...".
- **R5. Framing of the sensitivity "cost".** Figure 3B compares sensitivity at FPR 0.29 (training cut-off) with sensitivity at about 0.08 (burn-in). That is a move along the same ROC curve, not a loss caused by recalibration. Add one sentence: "at a matched FPR the two cut-offs have the same sensitivity; the training cut-off's higher sensitivity was bought with a threefold FPR." Otherwise a reviewer will raise it.
- **R6. GMHI–GMWI2 concordance (ρ = 0.70).** Both indices are scored on the same curatedMetagenomicData profiles, and many of the 36 populations were in GMWI2's training data. Shared profiler and batch effects therefore inflate concordance. State this in one clause next to ρ = 0.70, and call it concordance, not independent replication. The developers'-data result (H2) is the actual replication.
- **R7. Package hygiene.**
  - Align version labels: REPRODUCE.md says v16 and environment.yml says v15, for a v17 submission. Rename the GA file or note that v16 is the current GA.
  - Remove `SUBMISSION_REPORT.md` from the package README.
  - Fix the Fig 1D clipping of the open squares at AUROC < 0.5 (extend the x-limit), and move the overlapping "training FPR 0.24" label in Fig S2A.
- **R8. Readability (dimension 8).** Cut parenthetical statistics from the main text where the SI already holds them. Main candidates: the reweighting paragraph (CI of relative and absolute reductions, logit vs FPR scale) and the variance-decomposition sentence. Aim for one number per claim in the main text, about −150 words.
- **R9. References.** Verify the volume and pages of ref. 12 (Poyet et al., Cell 2026; DOI only) and complete them if it is now issued. Confirm that ref. 13's correction notice is cited as the journal requires.

### REQUIRED changes: author-only (cannot be done by the analysis team)

- **A1.** Title page: authors, affiliations, corresponding author.
- **A2.** CRediT contributions, conflicts of interest, funding, acknowledgments, and the competing-interests line in the cover letter.
- **A3.** AI-use statement (Wiley policy) describing AI assistance in code and drafting. This is mandatory, and the statement must be specific.
- **A4.** Make the GitHub repository public, archive it on Zenodo, and tag the fprcal release. Insert the URL and DOI in the Data Availability statement and the cover letter. Dimensions 6 and 9 are scored on the assumption that this is done.
- **A5.** Right of reply: send the GMWI2 and GMHI audits to the developers (Gupta/Sung group) before submission, and say so in the cover letter. Given the East Asian finding, this protects the paper.
- **A6.** Suggested reviewers, without conflicts. Mix microbiome-ML and diagnostic-test-evaluation expertise, and consider including one East Asian microbiome epidemiologist.
- **A7.** Check the current iMeta author guidelines in the submission system:
  - Letter word limit (the main text is about 2,295 words, 2,420 with Methods);
  - figure limit (3 + 2 supporting);
  - reference limit (32);
  - highlights format (the current highlights are 36–49 words each, likely longer than iMeta's usual short bullets; shorten to about 25 words each if a limit applies);
  - graphical-abstract size and keyword count.

---

## 5. Estimated probability of acceptance at iMeta

**About 40%** (plausible range 30–50%) for eventual acceptance, possibly after one round of revision, assuming R1–R3 and A1–A5 are done.

- **For:**
  - Clear practical message.
  - Breadth comparable to or larger than the benchmark iMeta papers.
  - Exceptional transparency: pre-registration-style plans, reported failures, a tested tool, pixel-identical rebuilds.
  - The Letter format fits a single focused message.
  - The blind total (74.5) sits above the benchmark P75 (69.25).
- **Against:**
  - Desk-review risk of about 20–30%. iMeta's portfolio leans toward new biology, multi-omics and tools from large consortia. A methods-critique Letter by an unknown group with no wet-lab or prospective component may be judged "important but niche".
  - The East Asian mislabelling result will be read closely by an editorial board and reviewer pool with many East Asian microbiome researchers. The text handles this responsibly ("properties of the model ... not evidence about East Asian microbiomes"). Any overstatement in the GA or front matter (R1–R3) would be penalised.
  - Reviewers are likely to ask for a prospective or truly external deployment of the burn-in, and to note that the burn-in rule is known.
  - Seven of the 28 classifiers have AUROC < 0.6. The AUROC ≥ 0.65 sensitivity analysis answers this, but it will come up.
- **If R1–R3 are not fixed:** about 30%. The broken GA paragraph is exactly what an editor sees first.

---

## 6. What would raise each dimension

**Below P75:**

- **8 Clarity (6.5 → ≥ 7.5).**
  - Fix R1 and R3 so that every front-matter number matches the text.
  - Make each Results paragraph lead with one finding sentence and one number, and move secondary statistics (CI of relative reduction, logit- vs FPR-scale caveats, full-set replicates) to the SI.
  - Shorten the highlights to about 25 words each.
  - Use a robust title number (R4).
  - Add one plain-language sentence on what an FPR of 0.87 means in practice, e.g. "87 of 100 healthy people referred".

**At P75 (to move clearly above it):**

- **1 Significance (8):** One worked clinical-consequence example in the text, e.g. referrals per 10,000 screened at the CRC pooled vs worst-population FPR. The data already contain this.
- **2 Scale (8):** Add a second profiler (MetaPhlAn4 profiles for a subset) or non-cMD healthy cohorts. That would also address the single-pipeline limitation.
- **3 Novelty (7):** State the AUROC ⟂ FPR-portability result as the central new claim, with a direct contrast to refs 1 and 15. Add the GMHI profiler-version effect as a general warning for released indices.
- **7 Figures (7):** Make the graphical abstract carry the title number (or change the title, R4). Fix the clipping and overlaps. Consider a one-panel study schematic in Fig 1 (train → fixed cut-off → 36 populations → audit → site).
- **10 Actionable (7):** A truly held-out site evaluation: the burn-in rule frozen and applied once to a population not used anywhere in development, or a newly released cohort. Report the sensitivity at matched FPR (R5). Report the effect of a pre-specified retraining fix on the GMWI2 recipe with an interval that clears the criterion.

**Already above P75 (no action needed beyond A4):** 4, 5, 6, 9. For 6, a PyPI/bioconda release of fprcal and a minimal web lookup of the atlas would move it to 8–9.

---

*Files viewed: all items listed in the header. No repository files were modified other than this report.*
