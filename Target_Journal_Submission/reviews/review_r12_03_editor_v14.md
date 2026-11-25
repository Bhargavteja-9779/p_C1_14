# Review r12-03 — Handling editor (iMeta), manuscript v14

**Manuscript:** "Gut-microbiome classifiers flag healthy people at population-specific rates, and a published health
index mislabels a whole region" (Letter)

**Materials read:** manuscript_v14.md; figures_v14 (Fig 1–3, PNG); supporting_information_v14.md; si_tables_v12.md;
code/tool (README, package, tests). `python3 -m pytest -q tests`: 13 passed (~40 s). CLI run: `atlas CRC`, `plan`,
`cutoff`, `verify`, `score --help`; outputs match Table S8 and the manuscript (e.g. N = 100: P(FPR > 0.15) = 0.055).
Spot checks against result files: 15 unseen strict GMWI2 populations sum to 1,914 people (Table S9) ✓; unseen
East Asian set (LiJ_2017, YeZ_2018, ZhuF_2020, YassourM_2016 = KOR) gives median 0.38 ✓; East Asian training share
1,574/2,522 vs 1,097/5,547 ✓.

**Editor score: 7.5 / 10**

**Decision: Minor revision** (suitable for an iMeta Letter; send to external review once MAJOR items 1–4 are resolved
in the submission version — they are editorial/presentation fixes, not new analyses).

## Summary of the submission

The authors measure the false-positive rate (FPR) at the published cut-off for 28 LASSO/RF classifiers (14 diseases) in
36 strict healthy populations (6,525 people, 20 countries) from curatedMetagenomicData, finding large between-population
heterogeneity (I² median 0.94) not explained by AUROC. They then audit GMWI2, a released health index, showing that in
its own training data it labels 64% of healthy people in East Asian studies as non-healthy versus 12% elsewhere,
attribute this to the geographic case mix of pooled training data (East Asian samples 62% of non-healthy, 20% of
healthy), and test the mechanism by retraining with country × label reweighting. Finally they show that a label-free
local burn-in recalibration (split-conformal quantile) reduces FPR error within sites (−62%; −79% for GMWI2) but fails
across sites and costs sensitivity, and release a small tool (`fprcal`).

## Fit for iMeta readers

Good fit. iMeta has published cross-cohort classifier Letters (imt2.212) and a reproducibility audit (imt2.70192), and
this paper links both: it gives readers a concrete reporting change (FPR per held-out population with I² and a
prediction interval), a mechanism that matters for global equity of microbiome diagnostics, and a reusable tool. The
pre-registration-style plans with reported falsifications are unusually transparent for the journal and are a strength.
The main editorial risks are length/density for a Letter and the wording of the regional claim.

## MAJOR concerns

1. **Main text overstates the pre-specified reweighting result (B2).** The main text says reweighting "cut the gap to
   0.06 ... meeting the stated criterion of a 50% reduction". SI S6.4 records that the corrected study-clustered CI of
   the relative reduction is 41–149% (6% of draws below 50%) and labels the verdict "supported (point estimate); CI
   includes values below the criterion". The main text gives only the absolute CI (0.18–0.58) and so reads as an
   unqualified pass. *Fix:* in the main text write "the point estimate (88%) met the criterion of a 50% reduction; the
   corrected 95% CI of the relative reduction (41–149%) includes values below it". Also reconcile B4 (τ 1.16 → 0.81,
   "supported") with the main-text statement that FPR-scale spread "barely changed" — say explicitly that B4 was met on
   the logit scale only, as was done for v6c C1.

2. **Inconsistent denominators in the unseen-population East Asian comparison.** The paragraph reports 15 unseen
   *strict* populations, then "The four unseen East Asian populations had FPRs of 0.25–0.54 (median 0.38 vs 0.20
   elsewhere; P = 0.065)". From Table S9 the median of the 11 other strict unseen populations is 0.06, not 0.20; the 0.20
   comes from `posthoc_eastasia.py`, which uses all unseen populations with n ≥ 20 in the *full* set. Similarly Fig 2B
   plots 55 full-set populations (seen and unseen) while the text discusses 15 strict unseen ones. *Fix:* state which set
   each number uses (or recompute on the strict set, which will strengthen the contrast), and make Fig 2B match the text
   (strict set, unseen highlighted) or relabel it as the full set.

3. **Wording of the regional claim, causal attribution and courtesy to the GMWI2 developers.** The title ("mislabels a
   whole region") and headings attribute a property to a region; the evidence is 13 Chinese/Japanese training studies
   and 4 unseen populations (P = 0.065, post hoc). The mechanism test shows geographic composition of the training data
   matters, but country is also confounded with laboratory, DNA extraction and sequencing protocol (studies from one
   country often share pipelines), and the within-country label balancing removed only 37% of the gap with a CI
   including 0. *Fix:* (a) reword the title so the subject is the index and its training data, e.g. "...and a published
   gut-health index mislabels healthy East Asian cohorts because of its training-data make-up" or shorter; (b) add one
   sentence that country-level batch/processing cannot be separated from biology for this result (currently said only for
   the atlas in the limitations); (c) avoid language that could be read as "East Asian guts look diseased" — the finding
   is a model artefact; (d) confirm in the cover letter that the GMWI2 authors were informed of the audit before
   submission (right of reply); this is good practice for audits of named, released tools and iMeta may ask.

4. **Submission completeness.** Authors, contributions, conflict of interest, funding, AI-use statement, and the GitHub
   URL + Zenodo DOI are placeholders. The reproducibility and resource claims (dims 6 and 9) depend on the DOI; iMeta
   expects a public repository at submission. *Fix:* fill all statements; deposit code, tool, atlas, per-person scores
   and figure source data on GitHub with a Zenodo DOI; add a pinned environment (requirements with versions or a
   lock/conda file); describe AI assistance concretely in the AI-use statement as required by Wiley policy.

5. **Length and density for a Letter.** Main text ≈ 2,590 words (To the Editor → Methods), 3 multi-panel figures (12
   panels), 28 references, and a 158-word summary carrying about nine numbers. The benchmark Letters run ~1,850–2,100
   words with two figures. Each paragraph currently reports many secondary statistics (e.g. variance shares for both
   models, within-study AUROC, MAD values), which buries the headline. *Fix:* check the current iMeta Letter limits; cut
   ~400 words by moving the RF variance decomposition, the within-country balancing variant, the AUROC-restriction
   sensitivity and the binomial-check power numbers to the SI; consider moving Fig 3A and 3C to the SI (Fig 3 → two
   panels, or merge 3B/3D into Fig 2 as E/F) to reach a two-figure Letter. Shorten the title to one claim.

## MINOR concerns

1. **Training FPR called "stated".** Fig 2A ("stated rate 0.21") and Fig 3/main text ("its stated FPR") use 0.208, which
   the authors computed from the developers' training scores; the GMWI2 paper does not state an FPR. Use "training FPR
   (0.21)" consistently.
2. **Fig 1D / legend mismatch.** Axis reads "AUROC (leave-one-cohort-out)"; legend says "out-of-fold"; single-cohort
   tests use 5-fold CV (S1). Use "out-of-fold AUROC". The legend says AUROC < 0.6 is "marked", but no marking is visible
   (one open square only). Mark these points clearly or drop the statement.
3. **Fig 3B "646 evaluations".** Explain in the legend that evaluations = population × non-random split (accession
   order, age, BMI, sex) per classifier, and that 12–13 populations contribute per classifier (Table S5).
4. **Fig 3D.** Say what the three points per method are (π = 1%, 5%, 10%?) and whether they are averaged over the three
   cohorts; the PAC burn-in sensitivity (~0.13–0.15) appears only in the figure — add it to the text or drop the series.
   X-axis label "FPR (patients 1–10% of burn-in)" also applies to the training cut-off point, which does not depend on
   the burn-in; relabel "FPR".
5. **Methods/SI table range.** Methods says "Tables S1–S20"; the SI contains S1–S25 (S11–S25 imported from si_tables_v4).
   SI header says "manuscript v14" but tables file is v12 and points to `supporting_information_v12.md` for S9–S10.
   Harmonise numbering and file references; renumber tables in order of citation.
6. **SI citation numbering.** SI S6.1 cites GMWI2 as [22]; it is [16] in the main reference list. Give the SI its own
   reference list or match the main numbers.
7. **Klebsiella in Fig 2C.** Fig 2C shows eight taxa including *Klebsiella* (weight −0.15; 59% vs 22%), which is a known
   pathobiont; one sentence on why it appears (and that it is not a commensal-only story) would pre-empt reviewer
   questions. Also state in the legend that the five largest explain 39% of the gap.
8. **"Non-westernised" labels.** Fig 1B bolds "non-westernised" populations (curatedMetagenomicData term). Define it in
   the legend and attribute the term to the database metadata.
9. **Abstract-summary claims.** "It suits screening... and it costs sensitivity" — give the size (0.46 → ~0.25 in three
   cohorts) or drop. "cut the FPR error by 62%" should say "within-site, retrospective" in the summary as well.
10. **Tool documentation.** README omits the `score` subcommand and the `--help` description lists only four commands;
    add `score` with an example and the expected input format (MetaPhlAn3 relative abundance in %, taxon naming), and
    state that scoring is research use only. Add a tagged release (v0.1.0) on Zenodo.
11. **Determinism.** SI S6.6 notes liblinear was unseeded in `run_v6c.py`; seed it in the deposited code. Remove absolute
    local paths (`/home/user/...`) from deposited scripts (e.g. `posthoc_eastasia.py`).
12. **Ethics statement.** Adequate for public de-identified data; add that curatedMetagenomicData profiles are openly
    licensed and that no attempt at re-identification was made; mention that country/region labels come from study
    metadata, not self-reported ethnicity.
13. **References.** Refs 12 and 13 are 2026 items (one with a correction notice); verify volume/page details at proof.
    Consider citing an iMeta Letter on population-structured microbiome variation (e.g. imt2.70088) in the framing to
    tie to the journal's readership.
14. **Graphical abstract.** iMeta requires a graphical abstract image; prepare one (map + "same cut-off, 0–77% flagged"
    + burn-in fix) — this can carry the study-design schematic currently missing from Fig 1.

## Figure comments

- **Figure 1 (atlas).** Strong central figure; map + heatmap + prediction intervals tell the story. Issues: no design
  schematic (iMeta Letters usually put the workflow in Fig 1A); 36 column labels and the long panel B title will be
  ~5 pt at print width — shorten panel titles, enlarge labels or drop the population name prefix; panel A colour bar
  title "false-alarm index" should match the legend term; panel C RF interval for IGT extends to 0.0005 and compresses
  the log axis — clip at 0.001 with an arrow; 1D labelling issues above. Colour scale (blue–white–red, log FPR) is
  readable and colour-blind tolerable.
- **Figure 2 (GMWI2).** Clear four-step narrative (training data → unseen data → taxa → retraining). Fix the "stated
  rate" label (A, B), the set shown in B (MAJOR 2), and add n per study as point size or in SI. In D, add the stated
  0.21 line and annotate that East Asian median after reweighting (≈0.29) is still above the training FPR, which the
  text does not say.
- **Figure 3 (site).** Panel B is effective (dumbbell, 28/28). Panels A and C are methodological and could move to SI
  for a Letter. Panel D needs clearer encoding (MINOR 4). Panel titles "Burn-in better in 28/28" and "Price:
  sensitivity" are good finding-style titles; keep that style throughout.
- All figures: provide vector PDFs (present) and figure source data in the repository; ensure consistent orange =
  East Asian / RF overloading is avoided (orange means RF in Fig 1C/1D, East Asian in Fig 2, training cut-off in Fig 3)
  — use distinct colours or explicit legends in each panel.

## Recommendation to the authors (priority order)

1. Qualify B2/B4 in the main text (MAJOR 1). 2. Fix the strict/full set mismatch in the East Asian comparison and Fig 2B
(MAJOR 2). 3. Reword the title and add the batch-confounding caveat; inform GMWI2 developers (MAJOR 3). 4. Complete all
statements and deposit code with a DOI (MAJOR 4). 5. Trim to Letter length/two figures if the limits require (MAJOR 5).
