# Handling-editor pre-submission check (clarity and presentation), package v22

Reviewer role: iMeta handling editor, blind. Read: scorecard anchors and P75, style_v2.md, manuscript_v22.md,
highlights.md, cover_letter_v22.md, all eight PNGs in figures/, and result files in code/experiments/atlas/v5-v7.

## 1. Clarity, framing and writing

**What works.**
- The title is a finding sentence. The problem is clear by the end of paragraph one: a test needs one cut-off, and
  the cut-off sets how many healthy people go to colonoscopy.
- Section headings are finding sentences, in the iMeta Letter style. The order is logical: problem, cause, fix.
- Main text is about 1,800 words to the Conclusion (about 2,000 with Methods). This sits in the Letter band.
- Limits are stated plainly and paired with a next step. Post hoc work is marked. Tone is calm, not hyped.
- Numbers agree across text, figure legends, graphical abstract and cover letter (64/12, 67/21, 0.52 to 0.06,
  62%, 28/28, 23% to 43%).

**What hurts a broad reader.**
- No "Here, we..." sentence. Paragraph three lists four extensions and pre-registration, but the headline result
  (70% of pairs outside 5-15%; 62% less error after a local reset) first appears in the Results. iMeta Letters put
  the scale and the main result at the end of the opening.
- Number density is very high in places. Section 1, paragraph 2 holds nine numbers in four sentences (70%,
  0.05-0.15, 65%, 0.65, 15%, I² 0.94, 0-0.77, 0-0.87, 0.81). Section 4, paragraph 3 has the same problem.
- FPR notation switches between percent and proportion. The graphical-abstract summary says "64%" and "12%"; the
  text says "0.64" and "0.12". The band is "5-15%" in the summary and "0.05-0.15" in the text.
- Highlight 1 is wrong on the unit. It says the target was missed "in 70% of healthy populations". The 70% is of
  classifier-population pairs (978 pairs).
- The formula k = ⌈(N + 1)(1 − α(1 − π_max))⌉, the exact Beta distribution and the P(FPR > α) rank bound are
  for specialists. The worked example ("the 91st smallest of 100 scores") carries the message alone.
- Some sentences are long and have a clause in the wrong place. Example, intro paragraph 2: "predictors trained on
  industrialised populations were uninformative elsewhere [12], although without a per-population FPR, and CRC
  models lost calibration...". The same paragraph packs SIAMCAT, three other studies, imaging, benchmarks and the
  iMeta audit into five sentences.
- Terms drift: test / classifier / index; population / group / cohort / study / site. The graphical abstract says
  "36 groups", the text "36 groups" then "populations". Fig. 1A adds a new term, "false-alarm index". Define each
  once and keep it.
- Heading 1 says "IN EVERY POPULATION". About 30% of pairs fall inside the band, so "every" overstates.
- The "error" in highlight 4 and the summary is not defined there. Say "distance from the 10% target".

## 2. Figures (all PNGs viewed)

- **Fig. 1.** Strong. Map, atlas heatmap, prediction intervals and AUROC scatter tell the first claim at a glance.
  The 36 rotated column labels in 1B are small; check they stay legible at iMeta print width. There is no study
  design schematic, which style_v2 notes is the norm for panel A.
- **Fig. 2.** Clear. In 2D the diamond labels read 0.29 and 0.22 (gap 0.07) while the title says 0.06. The legend
  explains the rounding, but a reader will not look there. Show 0.06 without the clash (e.g. drop the end labels).
- **Fig. 3.** 3A is clear and matches "28/28". In 3B the no-patient burn-in point is hidden under the
  labelled-controls marker, yet the text quotes "about 0.25" for it. Make it visible.
- **Graphical abstract.** Good three-panel story that matches the summary. The file is named "_v21" inside the
  v22 package; confirm it is current and rename.
- **Figs S1, S2.** Legible; captions match. S2B shows 12 studies, as stated.

**Cover letter.** Content matches the manuscript. It carries internal detail an editor does not need
("REPRODUCE.md", "script (v6c)", "file for file"). The bracketed note on contacting the GMWI2 and GMHI developers
must be resolved before submission.

## 3. Spot-check of numbers (all 10 match)

| Claim | File | Value |
|---|---|---|
| 70% pairs outside 0.05-0.15; ~15% expected | v5/posthoc_r20_numbers.json | 0.698; 0.157 |
| 65% among AUROC ≥ 0.65 | same | 0.649 |
| I² median 0.94 | v5/v5_summary.json | 0.937 |
| ρ = −0.06, CI −0.42 to 0.32 | v5/posthoc_r17_numbers.json | −0.060; −0.423 to 0.321 |
| Fold-model: 65% outside, ρ = 0.41 | v5/posthoc_r20_perfold.json | 0.648; 0.406 |
| 0.101 to 0.038, −62%, CI 51-70%, 75% units | v5/v5_summary, h4_cluster_ci_v11, numbers_v11 | match |
| GMWI2 0.64 vs 0.12, P = 5 × 10⁻⁷ | v6/gmwi2_eastasia.json | 0.636, 0.124, 5.3e-7 |
| 12/15 unseen outside band, P = 2 × 10⁻¹² | v6/gmwi2_results.json, holm_v6_v13.json | 0.80; Holm 1.8e-12 |
| Gap 0.52 to 0.06; 88%, CI 41-149% | v6/v6b_results.json, corrected_boot_v13.json | 0.524, 0.065; 0.877, 0.41-1.49 |
| GMHI 0.67 vs 0.21, P = 0.0007; 23% to 43% | v7/gmhi_results.json, posthoc_gmhi_matching.json | 0.673, 0.205, 6.7e-4; 0.227, 0.433 |

Also matched: top-five taxa 39%, East Asian share 62% vs 20%, 83% sample overlap, QC r = 0.99 on 704 samples.

## 4. Scores (1-10; P75 in brackets)

| # | Dimension | Score | P75 |
|---|---|---|---|
| 1 | Biological / clinical significance | 8 | 8.0 |
| 2 | Scale and breadth of data | 8 | 8.0 |
| 3 | Novelty vs prior art | 7 | 7.0 |
| 4 | Methodological rigor and statistics | 8 | 7.25 |
| 5 | External validation | 8 | 7.0 |
| 6 | Resource / tool value | 7 | 5.75 |
| 7 | Figure quality and visual story | 7 | 7.0 |
| 8 | Clarity, framing and writing | 7 | 7.25 |
| 9 | Reproducibility and openness | 7 | 7.25 |
| 10 | Actionable insight | 8 | 7.0 |
| | **Total** | **75** | 69.25 |

Dimension 8 notes. Strengths: a one-sentence problem, finding headings, an honest limits paragraph. Weaknesses:
the headline is held back from the opening, the number density is high, the notation is mixed, one highlight is
wrong, and there is specialist algebra in the main text. This is a solid 7, not yet 8. The four required changes
below would lift it to 8.
Dimension 9 is 7 only because the repository URL and DOI are still placeholders. With them in place it is 8.
Dimension 7: Fig. 1 is strong, but there is no design schematic and two small panel issues remain.

## 5. Changes

**REQUIRED**
1. Highlight 1: replace "in 70% of healthy populations tested" with "in 70% of classifier-population pairs".
2. Add a "Here, we..." sentence at the end of the opening, giving scale (28 classifiers, 36 populations,
   6,525 people, 20 countries) and the two headline numbers (70% of pairs outside 5-15%; 62% less error after a
   local reset).
3. Use one FPR notation for prose, summary, highlights and cover letter (percent is easier for a broad reader;
   keep proportions on axes). Define "FPR error" once as the distance from the 10% target.
4. Cut the number load. In Section 1, paragraph 2 keep 70%, 15% and the 0.81 interval; move the AUROC ≥ 0.65
   subset, the I² median and the per-model ranges to the legend or SI. Move the k formula, the Beta result and the
   rank bound to SI S3; keep the "91st smallest of 100" example. Split the long intro sentences (the [12] clause).

**Recommended**
- Heading 1: "...GIVES A DIFFERENT FALSE-POSITIVE RATE FROM POPULATION TO POPULATION" (drop "every").
- Fix terminology drift (test/classifier; population/group/cohort/site); define "false-alarm index" or drop it.
- Fig. 2D: remove the 0.29/0.22 clash with the 0.06 title. Fig. 3B: make the no-patient burn-in point visible.
- Fig. 1B: check column-label size at print width; consider a small design inset.
- Rename the graphical abstract to v22 after confirming it is current.
- Cover letter: drop internal file and script names; resolve the developer-contact note.
- Add the repository URL and Zenodo DOI (also lifts dimension 9).
- Consider a shorter title (about 12 words), in line with the most visible Letters.

**Decision: Minor revision before submission. Total 75/100 (P75 69.25). Eight of ten dimensions are at or above
P75; dimensions 8 and 9 are 0.25 below. Ready to submit once the four REQUIRED changes are made and the repository
link is added.**
