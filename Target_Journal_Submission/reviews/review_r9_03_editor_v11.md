# Review r9-03 — Handling editor report, iMeta Letter

**Manuscript:** "A false-positive-rate atlas of gut-microbiome disease tests across 36 healthy populations" (v11)
**Article type:** Letter
**Reviewer:** 3 (handling editor: clarity, fit, reproducibility, ethics, comparison with iMeta)

**Overall score: 7 / 10**
**Decision: Minor revision** (no new data needed; but MAJOR items 1–3 must be fixed before the paper can go to
external review, because the editorial office would return it at technical check as it stands)

Scorecard (blind, benchmark anchors): **76 / 100** vs benchmark P75 69.25 and max 78. Below P75 on significance (7 vs 8)
and reproducibility (7 vs 7.25). Details in `reviews/scorecard_r9_v11.md`.

## What I checked
- Manuscript text (1,902 words main text, 126-word graphical-abstract summary, 21 references, 2 figures): inside the iMeta
  Letter band (style_v2: ~1,850–2,500 words, ~20 refs, 2 figures).
- Both v11 figures (PNG).
- SI files present in `manuscript/`: `supporting_information.md`, `si_tables_v11.md`.
- Released tool: `python3 -m pytest -q tests` → 11 passed (36 s). `fprcal atlas IBD`, `fprcal plan` run as documented.
- Re-derived the headline numbers from the shipped atlas files (`fprcal/data/*.csv`): 489 LASSO pairs; 45% > 0.15, 26% > 0.25,
  24% < 0.05; I² 0.64–0.97, median 0.94, 28/28 ≥ 0.5; out-of-band share 50–97%, median 66%; Spearman ρ = −0.06, P = 0.76;
  16 classifiers with AUROC ≥ 0.65; 36 populations, 20 countries, 6,525 people; LASSO range in n ≥ 100 populations 0–0.77;
  maximum 0.87 (HF RF, n = 110); P(FPR > 0.15) = 0.055 (N = 100) and 0.015 (N = 200). All match, except one (MAJOR 4).

## Summary for the reader
The Letter asks a question the field has not asked in this form: what FPR does a microbiome classifier's published cut-off
deliver in healthy people it has never seen? Across 28 classifiers and 36 healthy populations, the answer is "almost
anything", heterogeneity is not predicted by AUROC, and it belongs mostly to the test–population pair. A label-free
local burn-in fixes it within a site (−62% error), fails across sites, and costs sensitivity if patients enter the burn-in.
The writing is clear, the honesty about failed hypotheses is unusual and welcome, and the fit with iMeta (cross-cohort
microbiome ML, released tool, atlas heatmap, map panel) is good. The problems are mostly about consistency between the
paper, its SI and its repository, plus two analysis-framing issues.

## MAJOR concerns

1. **The Supporting Information does not describe this study.** `supporting_information.md` (the only narrative SI)
   describes the earlier CRC-only design (eight development cohorts, `site_shift`, `em`, `pool_q`, 200 random splits,
   "post-hoc analyses added after peer-review round 1"). It has no methods for the 14-test atlas, the strict/full
   population definitions, duplicate removal, the DerSimonian–Laird model, the crossed random-effects model, the taxon
   decomposition, the within-site burn-in design (which 13 populations; how the 646 evaluations arise) or the
   replication addendum. The Letter's METHODS section points entirely to this SI, so the core methods are currently
   unavailable to a reader. The manuscript also cites "Tables S1–S15" and "Supporting Information S2–S4", while
   `si_tables_v11.md` has Tables S1a–S8 and says Tables S9–S23 live in a different file (`si_tables_v4.md`).
   *Fix:* write one SI document for v11 with numbered sections S1–S5 that match the in-text pointers (S1 data and
   populations; S2 robustness checks; S3 taxon decomposition; S4 earlier CRC/IBD/T2D analyses and cross-site burn-in;
   S5 analysis plans and deviations), include Tables S9–S23 in it, and make every in-text table/section reference
   resolve. Move the old CRC-only methods into S4 and label them as such.

2. **Repository, DOI and back matter are placeholders.** The Data Availability statement says "[GitHub repository URL and
   Zenodo DOI to be added]", ends with the unedited journal template ("online in DOI or http://www.imeta.science/"),
   and Authors, Author Contributions, Conflict of Interest, Funding and the AI Use statement are empty. iMeta requires the
   AI-use and COI statements at submission. The paper's claims about time-stamped plans "committed to the code
   repository" cannot be checked without the repository.
   *Fix:* make the repository public, archive a tagged release on Zenodo (with the per-person scores, duplicate list,
   metadata file, plans with commit hashes, and figure source data), cite both, and complete all back matter. Replace the
   template sentence with the journal's exact standard wording.

3. **Classifiers at or below chance are counted in the headline claims.** Three RF classifiers have out-of-fold AUROC
   below 0.5 (adenoma 0.444, IGT 0.447, fatty liver 0.449) and training sensitivity as low as 0.07; several LASSO
   classifiers are 0.54–0.56. These tests carry no disease signal, so their between-population FPR spread mostly
   measures how the population shifts an uninformative score; they inflate "28/28 classifiers" and populate the left of
   Fig 1D. The text mentions "several had a low AUROC" only in the limitations, and Fig 1D plots them without comment.
   *Fix:* (a) report the main heterogeneity numbers on the 16 classifiers with AUROC ≥ 0.65 in the main text, not only
   as a one-line check, and say how many of the 28 are below 0.6; (b) mark AUROC < 0.6 points in Fig 1D; (c) consider
   dropping below-chance classifiers from the atlas shipped in `fprcal`, or flag them in `fprcal atlas` output.

4. **One headline number does not match the data, and the abstract mixes models.** The text says the upper end of the
   LASSO 95% prediction interval "reached 0.34 to 0.81". In the shipped heterogeneity table the LASSO upper ends run from
   0.218 (CRC) to 0.809 (IGT); 0.34 is hypertension, the second lowest. The graphical-abstract summary's "0% to 87%"
   comes from an RF classifier (HF, LiuW_2016), while the body's "0 to 0.77 in populations ≥ 100" is LASSO-only.
   *Fix:* correct to "0.22 to 0.81" (or state the exclusion); in the abstract either give the LASSO n ≥ 100 range
   (0–77%) or say "across both model types". Then re-run a scripted check of every number in the text against the
   result files, and ship that check in the repository.

5. **The fix is validated within site only, and its costs sit in the SI.** The burn-in works within a site (13
   populations, a non-random split) and fails across sites, and with 1–10% patients in the burn-in group, sensitivity
   falls from 0.46 to 0.21–0.23. Those two results decide whether the fix is usable, but neither appears in a figure, and
   the graphical-abstract summary reports only the −62%. The headline −62% has no uncertainty interval, and the 646
   evaluations are not independent (13 populations × 28 classifiers × splits).
   *Fix:* add Fig 2D (sensitivity vs patient share in the burn-in, with the labelled-local-control comparator at 0.245)
   and, if space allows, a cross-site point in Fig 2B. Give a population-clustered bootstrap CI for the −62%. Add
   "within the same site" and "for screening use" to the graphical-abstract sentence on recalibration.

## MINOR concerns

1. **Wording on pre-registration is inconsistent.** The intro says the plans are "internal, time-stamped plans, not
   external pre-registrations", but the geography section says "we pre-registered a replication", and SI table titles
   say "pre-registered". Use "pre-specified (time-stamped, internal)" everywhere.
2. **"Our earlier analysis" is undefined.** It appears three times (cut-offs from other cohorts, cross-site burn-in,
   control augmentation). Say once that this was a first-stage analysis of the CRC, IBD and T2D tests reported in SI S4,
   with its design in one sentence.
3. **The strict set was chosen after seeing results.** This is disclosed, which is good. Also state in the main text
   that the full set gives I² ≥ 0.5 in 28/28 with median 0.92 *and* the within-site burn-in result on the full set, so the
   reader sees that neither headline depends on the choice.
4. **The "accession order as a stand-in for time" assumption.** Accession order is not collection time. Call it
   "a fixed, non-random order" and note that a time-ordered cohort is still needed (see "stand out" below).
5. **AUROC labelling.** The Fig 1D x-axis says "AUROC (leave-one-cohort-out)", but nine tests use five-fold CV on one
   cohort (caption says "out-of-fold"). Align the axis label with the caption. In the Spearman test LASSO and RF share
   tests; say that ρ is unchanged when computed per model (or report both).
6. **Single-cohort tests with tiny control groups.** Hypertension (41 controls), fatty liver (36) and ME/CFS (50) set a
   90th-percentile cut-off from 36–50 out-of-fold scores, so the training cut-off itself has a sampling error of several
   FPR points. Say how much of the "test" variance component this explains (Table S1a has `train_fpr`, which only shows
   the in-sample value).
7. **Taxon names.** *Bacteroides vulgatus* is now *Phocaeicola vulgatus*; give the current name with the MetaPhlAn3 label
   in parentheses.
8. **References 9 and 10 (2026).** Ref 10 (Cell 2026, doi …2026.10.016) is very recent; confirm volume/pages or mark
   "online ahead of print". Check ref 9's article number against the publisher page.
9. **Title.** Fine as a resource title. A finding-sentence title would match the most visible iMeta Letters better, for
   example "One cut-off, many false-positive rates: a 36-population atlas of gut-microbiome disease tests".
10. **Tool details.** (a) `tests/test_plan_monotone` asserts nothing: its assertion is commented out inside the comment
    on the line above. Either restore it for N ≥ 100 (where it holds) or delete the test. (b) README says atlas data were
    "copied from `experiments/atlas/v5/results/`", a path that does not exist in the tool tree; give the repository path
    and commit. (c) `fprcal verify` defaults (alpha 0.10, tolerance 0.05) match the paper; say so in `--help`. (d) Add a
    `CITATION.cff` and a version-pinned requirements line for scipy (`binomtest` needs scipy ≥ 1.7).
11. **Methods line.** "Full methods, the analysis plans and deviations, every correction we tried …" — add one sentence
    of key settings in the Letter itself (MetaPhlAn3; LASSO C = 0.1, RF 500 trees; cut-off = 90th percentile of
    out-of-fold control scores; DerSimonian–Laird on logit FPR). iMeta Letters with methods in the SI usually keep one
    such sentence.
12. **Ethics and language about populations.** The ethics statement is adequate for public de-identified data. However,
    labels such as "over-flagged populations" and the bold "non-westernised" columns can read as if the populations
    were abnormal. Keep the framing on the test ("the IBD test over-flags these populations because its training
    controls came from four Western countries"), and add one sentence on the under-representation of these populations
    in training data as the cause, not a property of the people.

## Figure-by-figure comments

**Figure 1 (atlas).**
- *1A map:* clear and in iMeta style (geography drawn, not listed). The colour scale (false-alarm index on the logit
  scale) is hard to read for non-statisticians; add "≈ FPR × e^index" or give two labelled anchor values. Overlapping
  circles in Europe and China hide populations; add small leader lines or a European inset. The legend sizes are fine.
- *1B heatmap:* this is the paper's strongest panel and the right iMeta template (cf. imt2.212 transfer matrix). Use
  the test names as written in the text (e.g. "fatty liver", "ME/CFS" already fine); state population n somewhere
  (a thin bar above the columns). Colour bar top label 0.80 while values reach 0.87; extend or note clipping. The
  white-centred diverging scale at 0.10 works.
- *1C prediction intervals:* informative, but the RF intervals for IGT, adenoma and hypertension reach down to
  0.0004, 0.0024 and 0.0026 on a log axis. They take up most of the panel width while describing classifiers with AUROC
  0.44–0.57 (MAJOR 3). Mark AUROC < 0.6 rows (hollow dot or grey), or clip the axis at 0.003 with an arrow.
- *1D AUROC vs τ:* the take-home "Better AUROC ≠ portable FPR" is good. Fix the axis label (MINOR 5), mark AUROC < 0.6
  points, and resolve the overplotted hollow square near AUROC 0.45, τ 1.07.
- *Missing:* iMeta Letters usually put a design panel in Fig 1A (style_v2 §3). A small schematic strip (train on 26
  case–control cohorts → fixed cut-off at 90th percentile → score 36 unseen healthy populations → FPR) would let Fig 1
  "tell the whole study at a glance", which is what a 9 on the figure dimension requires.

**Figure 2 (what a site can do).**
- *2A exact risk:* correct (I reproduced 0.055 at N = 100 and 0.015 at N = 200). The y-label is P(FPR > 0.15) but the PAC
  rule bounds P(FPR > 0.10); readers will ask why the orange line is near zero. Either plot each rule's own guarantee
  or say so in the legend. The saw-tooth is explained in the caption; good.
- *2B burn-in vs training cut-off:* convincing, but the 28 rows have no labels. Label rows (test + model) or colour by
  model; otherwise the reader cannot see which tests gain most. Add the cross-site comparator (MAJOR 5).
- *2C verification power:* four n values joined by lines imply a continuum; use points only, or compute the full
  curve. Legend says "true FPR" while the caption says observed FPR treated as true; use "observed FPR" in the legend.
- *Missing:* a sensitivity-cost panel (MAJOR 5) and a one-row schematic of the burn-in rule (score first N → take rank
  k → flag above). The graphical abstract could reuse it.

## Fit and comparison with iMeta Letters
- Format: matches the 2025–2026 Letter template (To the Editor, "Here, we…", three ALL-CAPS finding headings, short
  CONCLUSION with limitations, METHODS pointer). Length and reference count are in the band.
- Closest analogue imt2.212 (periodontitis signature, 8 cohorts, transfer matrix + LODO) scored 61; this paper is broader
  (36 populations, 14 tests), reports failures more fully and ships a tool. imt2.70192 (78) sets the bar for one-number
  framing and openness, which is exactly where this paper is weakest right now (placeholders, outdated SI).

## What would make this paper stand out among iMeta Letters
1. **Ship the models, not only the atlas.** Add `fprcal score` with the 28 trained classifiers (feature lists,
   coefficients/forests, MetaPhlAn3 species names) so a laboratory can score its own profiles, check the cut-off and
   recalibrate in three commands. That makes the resource a 9 and is cheap.
2. **Apply the atlas to a classifier the field actually uses.** Score one published, externally trained model (e.g. the
   SIAMCAT CRC meta-analysis model or the Piccinno 2025 CRC signature) in the same 36 populations. A single row in Fig 1B
   showing that an established model also swings from <5% to >30% would turn significance from 7 to 8–9.
3. **Translate FPR into referrals.** One sentence with numbers: at 10,000 screened, an FPR of 0.05 vs 0.40 means 500 vs
   4,000 colonoscopy referrals. This is the "one number that sticks" for clinical readers.
4. **A time-ordered test of the burn-in.** Any cohort with collection dates (or a longitudinal cohort) used as a true
   prospective burn-in would move actionable insight to 9 and answer the "accession order" caveat.
5. **A reporting checklist item.** Offer a two-line proposed STORMS addendum (per-population FPR at the fixed cut-off,
   I², prediction interval) as a box; Letters with a clear policy call (imt2.70192) are the ones that get cited.
6. **A browsable atlas.** A static web page (GitHub Pages) of Fig 1B with hover values and per-population n would cost
   little and match the web-resource pattern of imt2.70004 and imt2.70011.
