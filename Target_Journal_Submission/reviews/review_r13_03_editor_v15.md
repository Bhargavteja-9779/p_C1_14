# Review r13-03: Handling editor (iMeta), manuscript v15

**Manuscript:** "The same gut-microbiome test flags 0–77% of healthy people, depending on the population" (Letter)

**Materials read:** manuscript_v15.md (main text To the Editor → Conclusion/limitations 1,822 words; legends 471 words;
28 references); figures_v15 (Fig 1–3 and Supporting Fig S1, PNG, all viewed); graphical_abstract/graphical_abstract_v15.png;
supporting_information_v15.md; si_tables_v15.md; source_data_v12/README.md; code/tool (README, pyproject, package,
tests); requirements.txt; previous editor report review_r12_03_editor_v14.md and round12_response.md. Statistics and
novelty reports and earlier scorecards were not read.

**Tool checks.** `python3 -m pytest -q tests`: 13 passed (43 s). CLI: `--help` lists all five subcommands; `atlas CRC`
gives pooled FPR 0.058, PI 0.013–0.218, I² 0.80 (matches Fig 1C and the "0.22 (CRC)" in the text); `plan` matches
Table S8 (N = 100: P(FPR > 0.15) = 0.055); `cutoff` on 100 scores works and prints its guarantee clearly.
**`score` end-to-end:** scoring LiJ_2017 (cMD table with full clade strings, `--taxa-rows`, CRC) flags 8.2% of samples
(32 model taxa absent). Scoring the *same samples* as a species-only table, the input format the README describes
("columns = MetaPhlAn3 species names ... e.g. `s__Fusobacterium_nucleatum`"), flags **96.9%** (92 model taxa absent;
flag agreement 11%). The shipped LASSO models use taxa of every rank (CRC: 119 species + 70 k/p/c/o/f/g clades;
`atlas_v5.py` keeps `split("|")[-1]` of every MetaPhlAn row), so a species-only input silently zeroes a third of the
features. See MAJOR 2.

**Spot checks against result files (all ✓):** 489 LASSO classifier–population pairs, 44.6% > 0.15, 23.9% < 0.05,
range 0–0.77 in populations ≥ 100, 36 populations / 6,525 people (`v5_perpop_strict.csv`); I² and τ per test
(`v5_het_strict.csv`; heatmap rows are in ascending τ); GMWI2 training data 44 studies, 13 East Asian, median 0.64 vs
0.12, all eight studies > 0.5 from China/Japan, MW P = 5.3 × 10⁻⁷ (`gmwi2_published_training_perstudy.csv`);
unseen strict East Asian 0.38 vs 0.06, P = 0.020; full 0.38 vs 0.20, P = 0.065 (`posthoc_eastasia_strict_v15.json`);
Fig 2B shows 15 points, 11 blue / 4 orange, 8 below 0.10 and 4 above 0.31 (matches "eight ... four"); Fig 2C prevalences
(*B. plebeius* 72/17%, *Klebsiella* 59/22%, CAG_167 2/28%) match the text; `run_v6c.py` now seeded (`random_state=0`).

**Editor score: 7.5 / 10**

**Decision: Minor revision.** The round-12 editorial items were genuinely addressed and the paper now reads as a Letter.
Two new problems block a clean pass and are cheap to fix: the title claims more than the data show for any single test,
and the released `score` command gives wrong answers when used as its README says. Neither needs new analysis.

## Summary of the submission

The authors measure the false-positive rate (FPR) at the published-style cut-off (90th percentile of training-control
scores) of 28 LASSO/RF classifiers for 14 diseases in 36 strict healthy adult populations (6,525 people, 20 countries)
from curatedMetagenomicData. FPRs range 0–0.77 between populations, I² median 0.94, and AUROC does not predict the spread.
They audit GMWI2, a released gut-health index: in its own training data it labels 64% of healthy people in 13 Chinese/
Japanese studies non-healthy versus 12% elsewhere; in 15 unseen populations the East Asian median is 0.38 vs 0.06.
They attribute this to geographic case mix (East Asian samples 62% of non-healthy vs 20% of healthy training samples) and
test it by retraining with country × label reweighting (gap 0.52 → 0.06; CI of the relative reduction 41–149%). A
label-free within-site burn-in (split-conformal quantile) cuts FPR error by 62% within sites in retrospective
non-random splits, fails across sites and costs sensitivity (0.46 → 0.21–0.23). A small Python tool (`fprcal`) is
released.

## Fit for iMeta readers

Good fit. The paper connects iMeta's cross-cohort classifier Letters (imt2.212) and its reproducibility audit
(imt2.70192, cited) with a concrete reporting change (FPR per held-out population with I² and a prediction interval), an
equity-relevant mechanism, and a tool. The pre-specified plans with reported falsifications remain a strength. At 1,822
words, three figures and an 89-word summary it is now within a normal Letter footprint. The remaining editorial risk is
accessibility: the main text still packs a statistic into almost every sentence and uses terms (split-conformal,
π_max, exact Beta law, logit-scale τ) that a typical iMeta microbiologist will not parse without help.

## Round-12 editor items: verification

| r12 item | Status in v15 |
|---|---|
| M1 B2/B4 overstated | **Resolved.** Main text gives the 88% point estimate with the 41–149% CI and states that B4 was met on the logit scale only; 0.29 stays above the training FPR. |
| M2 strict/full denominators, Fig 2B | **Resolved.** Strict numbers in text with full-set check; Fig 2B shows the 15 strict unseen populations; verified against the JSON. |
| M3 regional wording, batch caveat, courtesy | **Resolved in text** (title has no region; "properties of the model and its training data"; country travels with laboratory/extraction/sequencing). Right of reply to the GMWI2 developers: **author action, open.** But the new title introduced an accuracy problem (MAJOR 1). |
| M4 statements, repository, DOI, environment | **Open, author action** (authors, contributions, COI, funding, AI-use statement, GitHub URL + Zenodo DOI, tagged release). Package versions pinned in requirements.txt, but no Python version or lock/conda file; figure source data still the v12 set (MAJOR 3). |
| M5 length | **Resolved.** 2,590 → 1,822 words; summary 89 words; Fig 3 two panels; secondary statistics moved to SI S2.1. |
| m1 "stated" FPR | Resolved ("training FPR (0.21)" throughout). |
| m2 Fig 1D | Resolved (axis "out-of-fold AUROC", open symbols, RF violet). New small issue: the three AUROC < 0.5 points sit on the left spine (figure comments). |
| m3 Fig 3 "646 evaluations" | Resolved in legend. |
| m4 old Fig 3D | Resolved (now Fig 3B, labelled points). |
| m5 table numbering/file refs | Resolved (S1–S25; SI header v15). |
| m6 SI citation numbers | Resolved. |
| m7 *Klebsiella*; 39% | Resolved in text and legend; the five taxa that make up 39% are not marked in Fig 2C. |
| m8 "non-westernised" | Resolved. |
| m9 summary claims | Resolved ("within a site ... retrospective"). |
| m10 tool docs | Partly resolved: `score` documented, research-use note present, but the documented input format is wrong for the shipped models (MAJOR 2). Tagged release: author action. |
| m11 determinism, paths | Resolved in code. SI S6.6 still reads as if liblinear were unseeded; say it is now seeded and that the reported v6c numbers come from the earlier unseeded run. |
| m12 ethics | Resolved. |
| m13 references | Acceptable. Refs 11 and 13 are 2026 items (13 with a correction notice); check at proof. |
| m14 graphical abstract | Image now exists (`graphical_abstract/graphical_abstract_v15.png`) but has layout faults and no schematic (figure comments). |
| Design schematic | Not added to Fig 1 or to the graphical abstract. |

## MAJOR concerns

1. **The title overstates the result for a single test.** "The same gut-microbiome test flags 0–77% of healthy
   people" reads as one test spanning 0–77%. No test does: in populations of ≥ 100 people (the basis of the 0–0.77 range
   in the text) the widest single-test ranges are IGT 0.09–0.77, fatty liver 0.07–0.71, T2D 0.01–0.61; CRC spans
   0.00–0.14. The 0–77% is the range over all 14 tests pooled. The graphical-abstract summary words this correctly ("the
   same cut-offs of 28 disease classifiers flagged 0% to 77%"); the title does not. A title is what readers quote, and a
   reviewer who checks it will find it inaccurate. *Fix:* make the subject plural or quote one real single-test range,
   e.g. "Gut-microbiome disease tests flag 0–77% of healthy people at the same cut-off, depending on the population", or
   "...one test flags 9% to 77% of healthy people...". Make the first results paragraph give one single-test example
   too (e.g. IGT 0.09–0.77), so the headline number belongs to a named test.

2. **The released `score` command gives wrong results when used as documented, and the Methods mis-describe the
   features.** The main text ("MetaPhlAn3 species profiles"), Methods ("MetaPhlAn3 species"), SI S1 ("Species-level
   MetaPhlAn3 relative abundances") and the README ("columns = MetaPhlAn3 species names") all say species. The code
   (`atlas_v5.py`: every MetaPhlAn row reduced to its last level) and the shipped coefficients use clades of every rank
   (CRC 70 of 189 features are k__–g__; T2D 79 of 209). A user who supplies the species table the README asks for gets
   flag rates near 100% (LiJ_2017, CRC: 96.9% vs 8.2% with the full clade table), with only a one-line "taxa absent"
   note. This undercuts the resource claim (scorecard dimension 6) and the reproducibility claim. *Fix:* (a) correct
   Methods, SI S1 and the main text to "MetaPhlAn3 relative abundances of all clades (kingdom to species) present in
   > 5% of training samples"; (b) in `fprcal score`, accept full clade strings and, if only species are given but lineage
   strings are available, sum to higher ranks; otherwise stop with an error (or require `--allow-missing`) when the
   missing features carry more than a set share of |w|; report the missing-weight share per sample; (c) add a test that
   scores a cMD-format table and a species-only table and checks the error path; (d) correct the README example.

3. **Reproducibility package lags the v15 figures (agent-fixable part of r12 M4).** The figure source data are the v12
   set (`source_data_v12/`), but v15 changed Fig 2B (now `gmwi2_perpop_strict.csv`, not the full set), Fig 3 (two
   panels; old panels moved to Fig S1) and added Fig S1 and a graphical abstract (script
   `make_graphical_abstract_v15.py`). There is no top-level README that maps each figure/table and each main-text number
   to a script and result file, no Python version, and no environment/lock file; the curatedMetagenomicData download step
   (`fetch_cmd.py`) is at the repository root and not described. *Fix:* create `source_data_v15/` with one folder per
   figure (including S1 and the graphical abstract) and a README table; add `REPRODUCE.md` (fetch → atlas → GMWI2 →
   figures, with run times); add `environment.yml` or a lock file with the Python version. The GitHub URL, Zenodo DOI and
   tagged fprcal v0.1.0 release remain **author actions**, as do the statements (below); they should not by themselves
   drive the decision, but iMeta will require them at submission.

## MINOR concerns

1. **Undefined band in the GMWI2 paragraph.** "80% of populations fell outside 0.10–0.31 ... Eight of these twelve fell
   below the band" — the band is not defined anywhere in the main text or SI (presumably training FPR ± 0.10), and
   "these twelve" has no antecedent. Write: "12 of the 15 (80%) fell outside the pre-specified band of 0.21 ± 0.10
   (0.10–0.31), against 9% expected from sampling noise; eight below and four above it." Draw this band in Fig 2B.
2. **Cryptic shorthands.** "(I² median 0.94, range 0.64–0.97; full set 28/28)" — say "also in the full set, 28/28
   classifiers". "GMWI2 > 0 = healthy" → "a score above 0 means healthy". "an exact Beta law" → "an exact,
   known distribution (Beta)". Define π_max in words at first use ("the highest share of patients expected among those
   tested").
3. **Fig 1A is never cited in the text.** Cite it in the first results paragraph (map of the false-alarm index).
4. **Statistic density.** Several paragraphs still carry 6–10 numbers (variance shares, τ, two CIs, AUROC shifts). For a
   Letter, keep one number per claim in the main text and move e.g. the LASSO variance shares, the τ 1.16 → 0.81, and the
   AUROC 0.715 → 0.676 detail to SI S2.1/S6, leaving words ("the population alone explained less than a fifth";
   "reweighting cost some discrimination").
5. **G3 summary in SI S6.2** ("seen 0.26 vs unseen 0.20") does not say these are means (the strict unseen median is
   0.10); label the statistic.
6. **SI S6.6** determinism note is stale (see table above).
7. **Spectrum effect citation.** Leeflang et al. 2013 is about variation with prevalence; the classic spectrum-effect
   references (Ransohoff & Feinstein 1978 NEJM; Mulherin & Miller 2002 Ann Intern Med) would be the expected citation.
   Consider adding one if space allows.
8. **Taxon names.** Use italics and one spelling: *Clostridium* sp. CAG_167 in the text vs "Clostridium sp CAG 167" in
   Fig 2C.
9. **"Population" includes sample handling.** The limitation is stated; repeat it once in the atlas results paragraph
   (one clause), since the first claim of the paper ("depends on the population") is where readers will raise it.
10. **Main-text Methods (~70 words).** Acceptable for a Letter with SI, but add the de-duplication rule, the strict-set
    definition in one clause and the software versions (scikit-learn 1.9.1) so the main text is self-standing.
11. **`fprcal plan` output.** PAC columns at N = 25 print NaN without explanation; print "infeasible (k > N)".
12. **Statements (author action, not decision-driving):** authors and affiliations, author contributions, conflict of
    interest, funding, AI-use statement (Wiley policy requires a concrete description), acknowledgments, repository URL
    and Zenodo DOI, tagged fprcal release, and confirmation in the cover letter that the GMWI2 developers were sent the
    audit before submission (right of reply). The cover letter on file is v9 and must be rewritten for v15.

## Figure comments

- **Figure 1 (atlas).** Still the strongest figure: map + heatmap + prediction intervals + AUROC panel tell the atlas
  story. Remaining issues: (i) no study-design schematic, which iMeta Letters usually carry in Fig 1A or the graphical
  abstract, and neither has one; (ii) panel D: the three RF classifiers with AUROC < 0.5 sit on the left spine at
  x ≈ 0.44–0.45 and overlap it, and the axis shows only two ticks; extend the x-limits to 0.4–1.0 with ticks at 0.5 and
  0.7; (iii) panel C rows are in an order the legend does not explain (say "ordered by LASSO upper prediction limit" or
  similar); (iv) panels A and B use the same blue–red palette for two different quantities (mean logit deviation vs FPR)
  — acceptable, but say so in the legend or use a different map palette; (v) the column labels (≈6.5 pt) are at the
  lower limit of legibility at print width.
- **Figure 2 (GMWI2).** Clear four-step narrative. Fixes: (i) panel B lacks the 0.10–0.31 band that the text tests
  against and its dashed line is unlabelled; add the band and label the line; (ii) label the 15 populations in B
  (country·author, as in Fig 1B) — readers will want to know which are the East Asian ones; (iii) panel C: italicise taxa,
  mark the five that explain 39%, and order by contribution to the gap; (iv) large empty vertical space between the
  rows; tighten; (v) panel D: the regional-median diamonds are offset from the line ends; add a small note "n = 61
  studies".
- **Figure 3 (site).** Panel A works (28/28 dumbbells; "Burn-in closer to target in 28/28" is a good finding title) but
  its y-axis has no labels; distinguish LASSO and RF (marker shape) or label the top five. Panel B is clear. As a main
  figure it is light; the best use of the space would be a small workflow panel showing what a site does with `fprcal`
  (atlas → verify → burn-in cut-off), which would also carry the resource message.
- **Figure S1.** Panel A legend says "PAC rule (δ = 0.05)" while the figure legend says "rule bounding P(FPR > 0.10) at
  0.05"; use one name. Explain why the PAC curve starts at N ≈ 30 (infeasible below).
- **Graphical abstract.** Exists now, but: the panel-1 subtitle runs into the panel-2 subtitle ("...≥ 100 peopleGMWI2:"),
  the "median 0.12" label sits on top of data points, and it is three data plots rather than the iMeta style of a
  schematic summary. Redraw as map/icon schematic: many populations → one cut-off → 0–77% flagged; training data make-up
  → regional bias; site burn-in → FPR back near target (retrospective).

## Recommendation to the authors (priority order)

1. Make the title accurate for the data (plural tests, or a real single-test range) (MAJOR 1).
2. Correct "species" to all-rank clades in Methods/SI/README and make `fprcal score` refuse or warn loudly on missing
   higher-rank features; add a test (MAJOR 2).
3. Update figure source data to v15, add REPRODUCE.md and an environment/lock file (MAJOR 3).
4. Define the 0.10–0.31 band, show it in Fig 2B, and clean the shorthands; cite Fig 1A (MINOR 1–3).
5. Thin the statistics in the main text; redraw the graphical abstract with a schematic; fix the Fig 1D/2C/3A details.
6. Author actions before submission: statements, GitHub + Zenodo DOI + tagged release, right of reply to the GMWI2
   developers, new cover letter.
