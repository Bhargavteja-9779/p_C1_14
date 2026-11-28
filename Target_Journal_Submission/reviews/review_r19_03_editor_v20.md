# Review r19, Reviewer 3 (handling editor): manuscript v20, iMeta Letter

Scope: clarity for a broad iMeta readership, fit for a Letter, figure legibility, reproducibility, ethics.
Materials read: manuscript_v20.md, supporting_information_v20.md, si_tables_v16.md, highlights.md, cover_letter_v20.md,
all six PNG figures, REPRODUCE.md, environment.yml, code/requirements.txt, fprcal README, result files in
code/experiments/atlas/{v4,v5,v6,v7}, scorecard.md (anchors and P75 only).

## 1. Summary of the submission

The Letter asks how far the false-positive rate (FPR) of a fixed cut-off moves between healthy populations.
It scores 28 classifiers (14 diseases, LASSO and RF) in 36 healthy cohorts (6,525 people, 20 countries).
It audits two released gut-health indices (GMWI2, GMHI) and finds high "non-healthy" rates in East Asian training studies.
It retrains GMWI2 with country-by-label reweighting to test a case-mix mechanism.
It tests a label-free local cut-off reset (an order-statistic rule on 100 local people) and ships it as fprcal.

The question is useful and well framed. The message fits iMeta. The work is unusually open about failed hypotheses.
My concerns are mainly about readability, the headline number, figure polish and a few reproducibility gaps.

## 2. Checks I ran myself

- fprcal tests: 19 passed (71 s; REPRODUCE.md says about 40 s). fprcheck tests: 7 passed.
- Number audit script on manuscript_v20.md: 84 numbers checked, 0 unmatched. The check is lenient, as disclosed.
- Independent rerun in a scratch copy, with the 61-file data cache:
  - atlas_v5.py: tests_v5.csv and coefs_v5.csv byte-identical; atlas_rows_v5.csv.gz identical after decompression
    (gzip header only differs). Run time 73 s.
  - analyse_v5.py: v5_summary.json identical; v5_perpop_strict, v5_het_strict, v5_h4_units identical.
  - run_gmwi2.py, posthoc_published_scores.py, posthoc_eastasia.py: four key outputs identical.
- Spot checks against result files: 26% of LASSO pairs above 0.25 (rf 16%); I² median 0.94; population share 17%
  (LASSO) and 7.5% (RF); Spearman -0.06, P = 0.76; burn-in error 0.101 to 0.038, 28/28; GMWI2 medians 0.64 vs 0.12,
  P = 5e-7; retraining gap 0.52 to 0.06, rel. reduction 88%, corrected CI 41-149%; Holm G2 P = 1.8e-12. All match.
- The 0.87 maximum is one pair: heart failure RF in LiuW_2016 (Mongolia, n = 110, 96 flagged).
- Submitted figures match the build folders (Fig 1 = figures_v19; Fig 2, 3, S1, S2 = figures_v17).
- fprcal `atlas CRC` runs from source and prints a clear one-line summary.

## 3. Clarity and readability

### 3.1 Flow and headings
- The order is good: problem, atlas, audit, mechanism, fix, conclusion. Each heading states a finding. This works well.
- The opening two paragraphs explain the spectrum effect in plain terms. A clinician can follow them.
- The headings are in all capitals. iMeta Letters normally use sentence case. Please check the style.
- The text opens with "To the Editor,". Published iMeta Letters do not use a salutation. Please check and likely remove.
- A "Graphical-abstract summary" sits above the main text. It repeats the highlights. Check whether iMeta wants it there.

### 3.2 Number density
- The main body has about 222 numerals in about 2,250 words (about 10 per 100 words).
- The two GMWI2 result paragraphs reach 21-22 numerals per 100 words. They read like a results table.
- Example: "Twelve of the 15 fell outside the pre-specified band of 0.10-0.31, against 9% expected ... Holm-adjusted
  P = 2 x 10^-12 ... 0.25-0.54 ... median of 0.06 in the 11 others ... P = 0.020; full set P = 0.065".
- A broad reader needs one number per claim. Move secondary P values, full-set repeats and CIs to the legends or SI.
- Suggested keep-list per section: atlas (26% of pairs > 0.25; PI upper end; rho), GMWI2 (0.64 vs 0.12; 12/15 out of
  band), mechanism (62% vs 20%; 0.52 to 0.06), fix (0.101 to 0.038; sensitivity 0.46 to about 0.22).

### 3.3 Terminology
- The same object is called "test", "classifier", "model", "classifier-population pair" and "test-population pair".
  Pick one ("classifier" for the 28 models, "test" for the 14 diseases) and use it everywhere, including Fig S1.
- "False-alarm index" (Fig 1A) is new jargon. It is a mean logit deviation. Readers will not know its scale.
- "PAC rule (delta = 0.05)" appears in Fig S1A and Table S8 but not in the main text. The legend calls it a "rule bounding
  P(FPR > 0.10) at 0.05". Use one name.
- "FPR" is used for GMWI2/GMHI, where the meaning is "share of healthy people labelled non-healthy". The figure axes say
  this well. Say once in the text that this is the FPR for an index.
- "Strict set" and "full set" are clear. "Non-westernised" in Fig 1B is the cMD label; the legend says so. Good.

### 3.4 Headline and title
- The title says "0-87%". The 87% is a single pair: RF heart failure in one Mongolian cohort of 110 people.
- This number is not visible in any main figure. Fig 1B shows LASSO only (maximum about 0.8). The graphical abstract
  also shows LASSO only (maximum about 0.77).
- A range driven by one extreme pair is fragile. A reader who checks will not find it.
- Better: put a robust number in the title, for example "a quarter of classifier-population pairs flagged more than
  25% of healthy people at a 10% target". Or show the RF heatmap (SI) and mark the 0.87 cell.

### 3.5 Claims versus evidence
- "AUROC does not warn when it is off" (Conclusion) is stronger than the evidence. The result is rho = -0.06 with a 95%
  CI of -0.42 to 0.32 over 28 classifiers. That is absence of evidence. Use "did not predict" as in the Results.
- The within-site burn-in is tested on splits of the same cohort (same lab, same protocol). This is a mild stress test.
  The text says "retrospective" and reports the cross-site failure, which is fair. Say plainly that a non-random split
  within one study is close to the conditions the rule assumes.
- The East Asian framing is careful. The text states that this is a property of models and training data, not of
  East Asian microbiomes, and that country is confounded with lab and sequencing. Good.

### 3.6 Methods paragraph
- The Methods is one long paragraph of semicolon-joined items. It is hard to scan. Use short sentences or a short list.
- The split-conformal argument and the k formula are compact and correct (k = 91 for N = 100, alpha = 0.10,
  pi_max = 0). A one-line worked example would help non-statisticians.

## 4. Figures

### Figure 1 (atlas)
- Strong design: map, heatmap, prediction intervals, AUROC scatter. It tells the story at a glance.
- It is dense for a full page. At 18 cm width the 36 column labels and 14 row labels are small but legible.
- Panel A: European circles overlap. The colour scale (logit deviation) is hard to read. Consider median FPR instead.
- Panel D: the "Spearman rho" text touches the dotted line. The "open symbols" note sits on a data point. Move both.
- Panel C: the arrow for an interval below 0.001 is explained in the legend. Good.

### Figure 2 (GMWI2)
- Clear and readable. Exact intervals are shown. Colours are distinguishable.
- Panel D: the diamonds have no legend entry. Only the East Asian value (0.29) is labelled; label the other (0.22) too.
- Panel C shows eight taxa; the text discusses five. Fine, but mark the five in the panel.

### Figure 3 (site)
- Clear. Panel A labels every row. Panel B shows the sensitivity cost honestly.
- Panel B: the x-axis runs to 0.30 to fit one point. A broken or log axis would give the burn-in points more room.

### Figures S1 and S2
- S1 has no title in its legend; S2 has one. S2's legend appears before S1's in the manuscript. Reorder.
- S2B: clear 1:1 comparison; the pooled 23% to 43% note is helpful.

### Graphical abstract (v20)
- Clear defect: the panel 1 title "Same cut-off, different populations (LASSO)" runs into the panel 2 title
  "2 A released index, its own data". The text overlaps and is unreadable. This must be fixed before submission.
- Otherwise the three-panel story is good and matches the highlights.

## 5. Fit for an iMeta Letter

- Length: about 2,020 words of main text (README), 3 main figures, 34 references. Check the current Letter limits in the
  submission system; the authors note they could not read the author page.
- The SI is very large (S1-S7, 27 tables, about 11,000 words). This is acceptable for transparency. But the main text
  leans on it often ("S2.1", "S2.2", "S4", "S6", "S7"). Each pointer should say in a few words what is there.
- Highlights are clear and within length. The cover letter is clear.

## 6. Reproducibility

Strengths:
- REPRODUCE.md is detailed: environment, data fetch with a count check, step-by-step scripts, run times, a number audit,
  tool tests. The environment is pinned. Seeds are fixed. Figure source data are provided.
- My partial rerun of the v5 atlas and the v6 GMWI2 audit gave identical outputs. Tool tests pass.
- Deviations and code errors (v6c weights, set()-based bootstrap) are disclosed and corrected in S6.6-S6.7.

Gaps:
- The logged fresh-clone rerun (logs/repro_fresh_clone and repro_full, 2026-11-24) covers the v4 pipeline only.
  There is no logged end-to-end rerun of v5, v6 and v7, which give the reported numbers. The cover letter says
  "a fresh-clone rerun reproduces the result files of the reported analyses". That is broader than the logs show.
  My own reruns support v5 and part of v6, but a single logged run of all reported steps should be added.
- There is no single entry point. Many versioned scripts co-exist (make_figures_v4..v8, make_fig_atlas_v11/v15/v19,
  make_graphical_abstract_v15..v20). Provide one script or Makefile that builds exactly the v20 numbers and figures,
  and move superseded scripts to an archive folder.
- Several scripts skip a missing study silently. REPRODUCE.md warns about this, but the scripts should fail instead.
- The pixel-identical rebuild covers the v16 figures, not the submitted Fig 1 (v19), Fig 3 and S2 (v17) or the GA.
- REPRODUCE.md cites HANDOFF.md, an internal file. environment.yml says "versions ... reported in manuscript v15". Update.
- fprcal has a licence only in pyproject.toml. Add a LICENSE file before the Zenodo archive.
- The repository URL and DOI are placeholders. This is expected at this stage but must be filled before acceptance.

## 7. Ethics and editorial requirements

- The ethics statement is adequate for reanalysis of public, de-identified data.
- Region labels come from study metadata, not self-reported ethnicity; this is stated. Good.
- The cover letter says the GMWI2 and GMHI developers will be sent the audits. The editor expects confirmation that this
  was done, and any response, before review proceeds.
- Author list, contributions, conflicts, funding and the AI-use statement are placeholders. All must be completed.
- The fprcal README says "Research use only; not a diagnostic device". Add the same sentence to the manuscript.

## 8. Major concerns (must be addressed; no new analysis needed)

1. Graphical abstract: overlapping panel titles make it unreadable. Fix and re-check at journal size.
2. Headline number: "0-87%" rests on one RF pair in one cohort of 110 people and is not shown in any main figure.
   Use a robust headline or show and mark the cell.
3. Number density: GMWI2/GMHI paragraphs carry about 20 numerals per 100 words. Cut to one key number per claim and
   move the rest to legends or SI.
4. Reproducibility claim: provide one logged fresh-clone run of all v5-v7 steps behind the v20 numbers and figures,
   or narrow the cover-letter claim to what is logged.
5. Editorial completeness: right-of-reply confirmation, author statements and AI-use statement.

## 9. Minor concerns

1. Use one term for classifier/test/model and for pair; define or drop "false-alarm index" and "PAC rule".
2. Soften "AUROC does not warn" to match the rho CI.
3. Say plainly that within-site splits are close to the rule's exchangeability assumption.
4. Rewrite the Methods paragraph as short sentences; add a worked k example.
5. Fig 1A overlap and colour scale; Fig 1D text placement; Fig 2D diamond legend and second label; Fig 2C mark top five;
   Fig 3B axis; Fig S1 title and legend order.
6. Remove "To the Editor,"; check heading case and the place of the graphical-abstract summary.
7. Make each SI pointer in the text say what it holds.
8. Add a single build entry point; archive superseded scripts; make missing-study handling fail hard.
9. Update stale references in REPRODUCE.md (HANDOFF.md) and environment.yml (v15); update the test run time.
10. Add a LICENSE file to fprcal and the "not a diagnostic device" note to the manuscript.

## 10. Scorecard (1-10; P75 of the iMeta benchmark in brackets)

| # | Dimension | Score | P75 |
|---|---|---|---|
| 1 | Biological / clinical significance | 8 | 8.0 |
| 2 | Scale and breadth of data | 8 | 8.0 |
| 3 | Novelty vs prior art | 7 | 7.0 |
| 4 | Methodological rigor and statistics | 8 | 7.25 |
| 5 | External validation / cross-cohort generalisation | 8 | 7.0 |
| 6 | Resource / tool value | 7 | 5.75 |
| 7 | Figure quality and visual story | 6 | 7.0 |
| 8 | Clarity, framing and writing | 6 | 7.25 |
| 9 | Reproducibility and openness | 8 | 7.25 |
| 10 | Actionable insight / mechanism | 7 | 7.0 |
| | Total | 73 | 69.25 |

Below P75: figures (6 vs 7.0) and clarity (6 vs 7.25). Both are fixable by editing, not new analysis.

## 11. Overall

The science is sound, checked and open. The results I reran reproduce exactly. The Letter fits iMeta.
It is not yet easy to read for a broad audience, the headline number is fragile, and the graphical abstract is broken.

Score: 7/10

Decision: minor revision
