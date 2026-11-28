# Reviewer 3 (handling editor) — manuscript v21, iMeta Letter

Focus: clarity for a broad iMeta readership, fit for a Letter, reproducibility, ethics.
Materials read: manuscript_v21.md, supporting_information_v21.md, si_tables_v16.md (skimmed), highlights.md,
cover_letter_v21.md, README.md of the package, all six PNG figures (viewed), REPRODUCE.md, environment.yml,
fprcal README and tests, scorecard anchors. Spot checks run (read-only; tool tests run on a scratch copy).

## 1. Summary of the submission

The Letter scores 28 gut-microbiome disease classifiers (14 diseases, LASSO and RF), each with a cut-off set for a 10%
false-positive rate (FPR), in 36 healthy adult populations (6,525 people, 20 countries). The FPR leaves 0.05–0.15 in
70% of classifier–population pairs. AUROC does not predict the spread. Two released gut-health indices (GMWI2, GMHI)
flag most healthy people in their own East Asian training studies. Retraining GMWI2 with reweighted data links this to
the geographic make-up of the training data. A known order-statistic rule on 100 unlabelled local people cuts the FPR
error by 62% within sites, not across sites, and costs sensitivity. A small Python tool (fprcal) is released.

## 2. Fit for an iMeta Letter

- The question is clear and useful. It speaks to benchmark authors, index developers and sites. Good fit.
- The title is a finding sentence. The section headings are finding sentences. This works well.
- Length: about 2,010 words from "To the Editor" to the end of the Conclusion, 3 main figures, 2 supporting figures,
  34 references. This is at the upper end for a Letter. The authors must check the current iMeta Letter limits
  (their own README says this was not verified).
- The "Graphical-abstract summary" block at the top is not a standard iMeta Letter element. Check whether iMeta wants
  it in the main file or only in the submission system.
- Headings in capitals: check iMeta house style.

## 3. Clarity and readability

### 3.1 Number density
- About 180 numerals in about 2,010 words (one per 11 words, reference numbers included). Ten post hoc daggers and
  13 pointers to SI sections. For a broad reader this is heavy.
- The heaviest paragraphs are: the GMHI paragraph (four numbers, a P value, an overlap share, a sub-analysis P, a
  profiler shift, then a gate that "passed narrowly ... but failed"), and the reweighting paragraph (0.52 → 0.06, a
  50% criterion, a CI, 37%, a pre-stated margin). Each sentence is short and plain. But a reader meets four caveats
  in a row and loses the main point.
- Suggestion: keep one headline number per claim in the main text. Move the second-tier numbers (the 37%, the
  six-unshared-study P = 0.10, the gate history, the 27% vs 36% fold-model shares) to SI, and keep one sentence
  that names the caveat.

### 3.2 Flow
- The opening (problem → spectrum effect → SIAMCAT → what is new) is good and fair to prior work.
- The atlas → audit → cause → site fix order is logical.
- The jump from "A released model is usually refitted..." (fold-model check) interrupts the atlas story right after
  the headline. It would read better after the AUROC paragraph, or in one sentence.
- The Conclusion gives four clear recommendations. Good.

### 3.3 Terminology
- "test", "classifier" and "index" are used for overlapping things. Figure 1 says "14 gut-microbiome disease tests";
  the text says "28 classifiers". Define once: a "test" is a disease; each has two classifiers (LASSO, RF).
- "FPR error" is used before it is defined. Define it once as mean |FPR − 0.10|.
- "cMD" appears in Figure 1B and 2B labels but not in the main text. Spell out or define.
- Figure 3B labels say "cases in burn-in"; the text and legend say "patients". Use one word.
- Figure S1A legend says "PAC rule" and "E[FPR] ≤ 0.10 rule"; the caption describes them in words. Align the names.

### 3.4 Small inconsistencies a careful reader will notice
- Text: "bringing the FPR to or below the target cut sensitivity from 0.46 to about 0.22". SI S2.1: with no patients in
  the burn-in, sensitivity is about 0.25 (labelled controls 0.245). The 0.22 is the 1–10% patient arms. Say which.
- Text: "the FPR ranged from 0 to 0.87" (populations ≥ 100). SI S2.2 gives 0 to 0.77 for LASSO. The 0.87 is RF. Say
  so, since Figure 1B shows LASSO only.
- Fold-model check: under fold-model scoring the AUROC–τ Spearman ρ is +0.23 (SI S2.3) against −0.06 in the main
  analysis. Both are null. One clause in the main text would pre-empt the question.
- Figure 2D: medians 0.29 and 0.22 give a gap of 0.07; the panel title says 0.06. Rounding; note it in the legend
  or quote the unrounded values.

### 3.5 Figures (each PNG viewed)
- **Figure 1.** Strong. The heatmap (B) carries the paper. The map (A) is attractive but its markers overlap in
  Europe and eastern China; the colour index is hard to read at print size. Consider insets or dropping A to give B
  more room. Column labels in B are small but legible at full page. Panel C log axis and arrow are clear. Panel D
  reports P = 0.76; the text reports a CI; give the CI in the panel too.
- **Figure 2.** Clear. A and B tell the audit story at a glance. C is good. D has many thin lines; the diamonds carry
  the message. The y-axis in D has empty space above 1.0 for the legend; fine.
- **Figure 3.** Clear. A shows 28/28 well. B is sparse (four points) and could be a smaller inset.
- **Figure S1.** A: the saw-tooth shape (integer k) is not explained; add one phrase. B: clear.
- **Figure S2.** Clear. B makes the profiler point well.
- **Graphical abstract.** Clear three-step story. Panel 1 shows LASSO only and populations ≥ 100; the subtitle says so.

### 3.6 Highlights and cover letter
- Highlights are long (each two or more clauses, 40–60 words). Shorten each to one claim.
- The cover letter still contains a bracketed instruction to the authors ("[Before submission: confirm that the GMWI2
  and GMHI developers were sent the audits ...]"). Remove before submission.

## 4. Reproducibility

Checked:
- REPRODUCE.md gives every step from data download to figures, number audit and tool tests. Good.
- environment.yml pins Python 3.13 and all direct and indirect packages. The installed versions here match.
- fprcal tests: I ran `pytest` on a scratch copy: **19 passed** (67 s). The score tests check scores against atlas
  scores.
- Number audit (`scripts/audit_numbers.py` on manuscript_v21.md): **79 numbers checked, 0 unmatched**. The script is
  lenient (any rounding match passes), as REPRODUCE.md says.
- `data/sampleMetadata.sha256` matches the decompressed CSV (not the .gz). State this in REPRODUCE.md.
- Referenced scripts (make_graphical_abstract_v21.py, rebuild_cache.sh, audit_numbers.py, v6/v7 inputs, logs) exist.

Gaps:
- Repository URL and DOI are placeholders. Public code and a Zenodo DOI are a condition of acceptance.
- The pixel-identical figure rebuild covers the v16 figures. The submitted v21 Figures 1 and 2 and the v21 graphical
  abstract are regenerated by scripts but not shown to match. Extend the rebuild check to the submitted files.
- Several run times are "not logged". Minor.
- `run_v6c.py` is unseeded (disclosed; its results are not used in the main text).
- The atlas and GMWI2 scripts skip missing studies silently. REPRODUCE.md warns about this. A hard check in code
  would be safer.
- The data depend on ExperimentHub staying online; the processed per-person scores are deposited, which mitigates.

## 5. Ethics, transparency and statements

- Ethics statement is adequate for public de-identified data. The sentence that region labels come from study
  metadata, not self-reported ethnicity, is good. The text states twice that the East Asian result is a property of
  the models and training data, not of East Asian microbiomes. Good and necessary.
- Right of reply: the audits of GMWI2 and GMHI name released tools. The developers should be sent the audits before
  submission, and the cover letter should say so. This is still open.
- Author list, contributions, conflicts, funding and the AI-use statement are placeholders. The AI-use statement
  matters here: SI S5 states that plans v6 and v7 were written in response to "simulated editor and reviewer checks".
  The AI-use statement must describe this plainly.
- Pre-specification is handled honestly: failed and inconclusive hypotheses are listed (S5), post hoc analyses are
  marked, and the post hoc choice of the strict set and the East Asian comparisons is stated in the limits.
- SI contains drafting-process language: "moved here for readability" (S2.2), "requested in the final editorial
  review" (S7), and a pointer to `state/variants_tried.csv`. Rephrase as plain analysis notes, and make sure every
  path cited in the SI exists in the public repository.

## 6. Major concerns

1. **Readability of the main text for a broad readership.** The numbers and caveats are accurate but too dense in the
   GMHI and reweighting paragraphs and in the fold-model paragraph. Keep one headline number per claim and move
   second-tier numbers to SI.
2. **Open items that block acceptance.** Public repository and DOI; author statements; an AI-use statement that
   covers the simulated review rounds named in SI S5; right of reply to the GMWI2 and GMHI developers.
3. **Figure reproducibility for the submitted versions.** Extend the pixel-identical rebuild to the v21 figures and
   graphical abstract.

## 7. Minor concerns

1. Sensitivity "about 0.22" vs 0.25 with no patients: say which arm.
2. FPR range 0–0.87 is RF; LASSO is 0–0.77. Say so.
3. Mention the fold-model AUROC–τ ρ (+0.23) in one clause.
4. Define "cMD", "FPR error", and the test/classifier distinction at first use.
5. Use "patients" consistently (Figure 3B says "cases").
6. Align rule names in Figure S1A and its caption; explain the saw-tooth.
7. Figure 1A: reduce marker overlap or shrink the panel; add the ρ CI to 1D.
8. Figure 2D: gap 0.06 vs medians 0.29/0.22; note rounding.
9. Shorten the highlights.
10. Remove the bracketed author instruction from the cover letter.
11. Remove drafting-process language from SI S2.2, S5 and S7.
12. Check iMeta Letter limits, heading style and whether the graphical-abstract summary belongs in the main file.
13. REPRODUCE.md: say the checksum is of the decompressed metadata CSV; log the missing run times.

## 8. Scorecard (my scores; benchmark P75 in brackets)

| # | Dimension | Score | P75 |
|---|---|---|---|
| 1 | Biological / clinical significance | 8 | 8.0 |
| 2 | Scale and breadth of data | 8 | 8.0 |
| 3 | Novelty vs prior art | 7 | 7.0 |
| 4 | Methodological rigor and statistics | 8 | 7.25 |
| 5 | External validation / cross-cohort | 8 | 7.0 |
| 6 | Resource / tool value | 7 | 5.75 |
| 7 | Figure quality and visual story | 7 | 7.0 |
| 8 | Clarity, framing and writing | 6 | 7.25 |
| 9 | Reproducibility and openness | 8 | 7.25 |
| 10 | Actionable insight / mechanism | 7 | 7.0 |
| | Total | 74 | 69.25 |

Clarity (8) is the one dimension below P75, because of number density, not because of poor prose.
Reproducibility (9) is scored on the materials in the repository; it holds only once the repository is public.

## 9. Overall

Overall score: 7/10.

Decision: minor revision.
