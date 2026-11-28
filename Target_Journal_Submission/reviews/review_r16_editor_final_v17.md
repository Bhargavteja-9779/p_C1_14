# Review r16: handling-editor final pre-submission check, manuscript v17 (iMeta Letter)

Reviewer role: handling editor at iMeta, reading as a statistician. I scored this blind: I read no earlier review
reports or scorecards, only the anchors and P75 table in `journal_selection/benchmark_v2/scorecard.md`.
Materials checked: `submission_final_v17/` (manuscript, SI, highlights, cover letter, all six figure PNGs including
Figure S2 and the graphical abstract), result files in `code/experiments/atlas/v5|v6|v7/results`, plan
`v7/protocol_v7_gmhi.md` and its git history. Tool tests: `python3 -m pytest -q` in `code/tool` gave **19 passed**.

## 1. Number spot-check (40 numbers checked)

All of the numbers below match the result files. Rounding is correct unless a comment says otherwise.

| # | Claim (where) | Source | Result |
|---|---|---|---|
| 1 | 0–87% across 28 classifiers, populations ≥ 100 (title, highlights, cover letter, text) | v5_perpop_strict.csv (n ≥ 100: 0–0.8727, HF RF, LiuW_2016) | OK |
| 2 | 36 populations, 6,525 people | v5_perpop_strict.csv (36; sum of n = 6,525) | OK |
| 3 | 20 countries | v4 counts_v4.json `countries: 20` | OK |
| 4 | Full set 55 populations, 8,160 people | v5_perpop_full.csv | OK |
| 5 | 119 duplicated samples removed | counts_v4.json `excluded_samples: 119` | OK |
| 6 | 26 training cohorts | training_cohorts_v5.json | OK |
| 7 | 489 LASSO pairs; 45% > 0.15; 24% < 0.05 | numbers_v11.json (0.446, 0.239) | OK |
| 8 | LASSO range 0–0.77 (n ≥ 100); IGT 0.09–0.77, AUROC 0.54 | perpop_strict, tests_v5 | OK |
| 9 | HF RF out-of-fold AUROC 0.75 | v5_het_strict (0.748) | OK |
| 10 | I² median 0.94, range 0.64–0.97, 28/28 | v5_summary H1_strict | OK |
| 11 | Noise alone 15–16% outside the band; observed 50–97% | numbers_v11.json | OK |
| 12 | Upper PI: CRC 0.22 to IGT 0.81; pooled CRC 0.06 | v5_het_strict | OK |
| 13 | Spearman ρ −0.06, P = 0.76; 16 classifiers with AUROC ≥ 0.65 | v5_summary | OK |
| 14 | Population 17% (20.2% net); pair about half | v5_summary; h2_sampling_v13 (net pair 0.555) | OK |
| 15 | Seven classifiers with AUROC < 0.6 | v5_het_strict (7, three of them < 0.5) | OK |
| 16 | GMWI2: 8,069 samples, 54 studies; training FPR 20.8% | counts_v12, gmwi2_results | OK |
| 17 | 44 studies, 0–84%, I² 0.96; 8 studies > 50%, all CHN/JPN | gmwi2_published_training.json | OK |
| 18 | East Asian 0.64 (13 studies) vs 0.12 (31); P = 5 × 10⁻⁷ | gmwi2_eastasia.json | OK |
| 19 | Rural Africa 0–7% | gmwi2_published_training_perstudy.csv (TZA, MDG, BFA, CMR, GHA: 0–0.073) | OK |
| 20 | 15 unseen populations, 1,914 people, r = 0.991, range 0–0.54 | gmwi2_results.json | OK |
| 21 | 12/15 outside the band, 9% expected, Holm P = 2 × 10⁻¹²; 8 below, 4 above | gmwi2_results, holm_v6_v13, gmwi2_perpop_strict.csv (counted) | OK |
| 22 | East Asian unseen 0.25–0.54; 0.38 vs 0.06, P = 0.020; full set 0.38 vs 0.20, P = 0.065; G3 P = 0.72 | posthoc_eastasia_strict_v15, gmwi2_results | OK |
| 23 | GMHI 3–90%, 21 studies, I² 0.96, 24% overall | gmhi_results.json H1, alpha | OK |
| 24 | GMHI East Asian 0.67 (8 studies) vs 0.21 (13); P = 0.0007 | gmhi_results.json H2 | OK |
| 25 | **82%** of GMHI healthy samples shared with GMWI2; 15/21 studies | posthoc_gmhi_gmwi2_overlap.json (0.8251) | **Mismatch with SI**: SI S7 says 83%, the main text says 82% |
| 26 | Independent studies 0.63 vs 0.17, three each | same file | OK (one-sided P = 0.10, not reported in the main text) |
| 27 | Q2 r = 0.795 on 2,190 samples | posthoc_gmhi_matching.json | OK; `gmhi_results.json` still says `"pass": true` (r = 0.803, n = 101), see §2 |
| 28 | Share flagged 23% → 43%; per-study shift 0–74 points; 12 studies | posthoc_gmhi_matching.json, Table S27 | OK |
| 29 | 4 of 7 health-prevalent species absent | gmhi_results.json Q2 | OK |
| 30 | SI: 13 of 43 health-scarce species absent in all 61 studies | json lists **15**, because it checks only the first study. I recomputed over all 61 cached studies and got **13**. | Claim correct; the result file's label is misleading |
| 31 | Top-five taxa explain 39%; *B. plebeius* 72% vs 17%; CAG_167 2% vs 28%; *Klebsiella* 59% vs 22% | numbers_v14, gmwi2_eastasia | OK |
| 32 | East Asian samples 62% of non-healthy (1,574/2,522), 20% of healthy (1,097/5,547); OR 6.7 | gmwi2_casemix.json | OK |
| 33 | Retraining 10,986 people, 61 studies; gap 0.71 vs 0.19 → 0.06; 88%, CI 41–149%; EA 0.29 | counts_v12, v6b_results, corrected_boot_v13 | OK |
| 34 | Within-country variant 37%, CI −0.04 to 0.31 | posthoc_v6b_withincountry.json | OK |
| 35 | Burn-in 0.101 → 0.038 (−62%), 28/28, CI 51–70%, 13/13 | v5_summary H4, h4_cluster_ci_v11 | OK |
| 36 | GMWI2 burn-in 0.21 → 0.04, −79%, CI 64–85% | gmwi2_results G4 | OK |
| 37 | Sensitivity 0.46 → 0.21–0.23; labelled controls 0.25; training cut-off FPR 29% | v4 deploy_v4_cc_summary.csv | OK (burn-in FPR is 0.075–0.087, so "reaching the 10% target" means at or below it) |
| 38 | Binomial check flags 98% of pairs with FPR > 0.25 | verify_power_v5.json | LASSO only (RF 97%); say "LASSO atlas pairs" |
| 39 | N = 100: P(FPR > 0.15) = 0.055 | Beta order statistic, recomputed: k = 91, 0.0551 | OK |
| 40 | Graphical abstract: medians 0.64 and 0.12, −62%, 28/28; Figure S2: 21 studies, 0.24, 2,190, 23% → 43%, 12 points | figures vs result files | OK |

**Mismatches:**
- (a) GMHI–GMWI2 overlap is 82% in the main text and 83% in the SI. The true value is 82.5%.
- (b) `gmhi_results.json` reports Q2 `"pass": true`, but the paper reports Q2 as failed. The paper's verdict is the right
  one; the stale result file is not.
- (c) The 98% binomial power holds for LASSO only.
- (d) `gmhi_results.json` labels 15 health-scarce species as missing from cMD, but that list comes from the first study
  only. The SI's 13 is correct; I verified it across all 61 studies.

I found no mismatch in the title, highlights, graphical-abstract summary or cover letter.

## 2. GMHI section against plan v7

- **Timing.** The plan was committed (8b70d70, 03:32) before the results (32a7351, 03:35). Q1, H1–H6 and the Holm
  family match the plan. The East Asian definition was fixed in advance. Under the word rule, Mongolia counts as
  "other", and the paper says so.
- **Q1** passed (max difference 4.9 × 10⁻¹⁵). The claim that the re-implementation "reproduced the developers' script
  exactly" refers to the developers' example data, which is the correct scope.
- **H1 and H2** use the developers' own profiles, so Q2 does not affect them, as the plan states. They are reported
  correctly. The Holm adjustment for H2 is numerically the raw P, because H2 has the largest P in its family. This holds
  whether or not H4–H6 stay in the family.
- **Q2 gate → non-interpretation.** The main text follows the plan: H3–H6 (unseen-population FPR, band test, ρ with
  GMWI2, GMHI burn-in) are not interpreted, and the earlier claims of GMHI burn-in −79% and ρ = 0.70 were removed. The SI
  lists them "for completeness". That is acceptable, because the SI says plainly that they are not interpreted. This is
  the correct handling.
- **One disclosure gap.** The plan as literally implemented *passed* Q2 (101 samples, 2 studies, r = 0.803). The failure
  appeared only after a post hoc correction of the matching procedure, found in review. The deviation is conservative:
  it moves the paper towards claiming less. It is disclosed in SI S7 but not in the main text. Because the margin is tiny
  (0.795 vs 0.80), the main text should say this in one clause.
- **My checks of the corrected matching.** I reran the matching in my scratchpad without changing any repository file.
  - Every match came through accession numbers (101) or sample titles (2,089).
  - None came through subject IDs, and none was ambiguous, so spurious matches across studies do not drive the 0.795.
  - A study-clustered bootstrap gives a 95% CI for r of 0.69–0.86. So the gate is not statistically distinguishable
    from its threshold either way. Following the point-estimate rule and not interpreting H3–H6 is the right call.
- **Post hoc profiler-shift finding (23% → 43%).** It is labelled post hoc in the main text and in Figure S2B. It is
  supported directly: the same samples, flag rate on both profiles, 12 studies. It has two limits:
  - It covers one index, and its mechanism is largely mechanical: species names absent in MetaPhlAn3 change Shannon's
    index and the richness ratio.
  - Developers' and cMD read preprocessing may also differ.

  So "profiling pipeline" (the main text and conclusion) is accurate. "Profiling software version" (highlights) and
  "which shows that a released cut-off also depends on the profiling software version" (cover letter) slightly
  overstate it and do not carry the post hoc label.
- **Independence.** The main text now correctly calls H2 "a replication in a second model rather than in independent
  data" (82–83% sample overlap). The six-study check (three vs three) has a one-sided P of 0.10. The main text gives the
  medians without this P, which reads more favourably than the data allow. Add the P.
- **In-sample caveat.** H1 and H2 measure in-sample miscalibration of a model fitted on pooled data. That fits the
  mechanism argument, but readers should know it does not test transport to new populations, which is exactly the part
  that failed QC. The limitations paragraph covers this implicitly ("its audit rests on the developers' own data").

**Overclaim verdict.** No material overclaiming. The highlights and graphical-abstract summary state medians correctly
and attribute the mechanism by retraining to GMWI2 only. Small wording issues:
- the profiler sentence in the highlights and cover letter;
- graphical abstract panel 3 says "first 100 local people", but the −62% pools accession-order, age and BMI splits;
- "reaching the 10% target": the achieved FPR is 0.08.

## 3. Blind score (scorecard v2 anchors; P75 in brackets)

| # | Dimension | Score | P75 | Reason |
|---|---|---|---|---|
| 1 | Biological/clinical significance | 8 | 8.0 | Fixed-cut-off FPR across populations; two released indices; CRC colonoscopy framing. Most atlas classifiers are research refits. |
| 2 | Scale and breadth | 9 | 8.0 | 36 (55) healthy populations, 20 countries, 28 classifiers, plus 8,069 and 2,636 developer samples |
| 3 | Novelty | 7 | 7.0 | Spectrum effect and country confounding are known [8–13]. New: the cross-disease atlas, an audit of released indices, a test by retraining. |
| 4 | Rigor and statistics | 8 | 7.25 | Pre-specified plans with falsifiers, Holm, DL/I²/prediction intervals, corrected cluster bootstraps, failures reported. Held below 9 by the post hoc strict set and East Asian contrasts, the post hoc Q2 matching fix, and a borderline gate. |
| 5 | External validation | 8 | 7.0 | Every held-out population; leave-one-study-out retraining; burn-in fails across sites and this is reported |
| 6 | Resource/tool value | 7 | 5.75 | fprcal (19 tests pass), atlas, 14 LASSO coefficient tables. Not yet public; no web front end. |
| 7 | Figures | 7 | 7.0 | Fig 1 (map + heatmap + PI + AUROC) is strong; Fig 2 tells the mechanism; GA is clear. Fig 1B is dense; GA omits GMHI. |
| 8 | Clarity and writing | 7 | 7.25 | Finding-sentence headings, a number that sticks. Paragraphs are dense with numbers, which is heavy for a Letter. |
| 9 | Reproducibility | 8 | 7.25 | Full code, environment, source data, per-person scores, fresh-clone rerun claimed. Repo not yet public; one stale result flag (Q2). |
| 10 | Actionable insight/mechanism | 8 | 7.0 | Tested label-free fix on retrospective non-random hold-outs; mechanism tested by retraining; no prospective test |
| | **Total** | **77/100** | 69.25 | At or above P75 on 9 of 10 dimensions; clarity 0.25 below |

## 4. Decision

**Ready to submit after minor required changes.** As handling editor I would send it to review, not desk-reject it.
I would expect minor-to-major revision.

### REQUIRED changes (manuscript and package; the agent can make these)
1. **Main text, GMHI paragraph.** Add one clause disclosing the Q2 deviation. Suggested wording: "(the pre-specified
   accession matching found only 101 samples, r = 0.80; correcting the matching, found in review, gave 0.795 on 2,190
   samples; S7)".
2. **Report the six-independent-study P.** "median 0.63 vs 0.17, three studies each; one-sided P = 0.10; post hoc".
3. **Overlap figure.** Make the main text and SI agree (82.5%, or "83%" in both).
4. **Highlights and cover letter.**
   - Change "profiling software version" to "profiling pipeline (MetaPhlAn2 vs 3)".
   - Mark the profiler finding as post hoc in the highlights.
   - In the cover letter, replace "which shows that" with "and on the same samples the share flagged rose from 23% to
     43%".
5. **Binomial check.** Change "98% of atlas pairs" to "98% of LASSO atlas pairs".
6. **Result-file consistency.** Make the stale v7 files visibly superseded without editing the committed originals: add
   a note in the SI/README, or a small superseding JSON, stating that `gmhi_results.json` Q2 `"pass": true` and its
   `missing_species_in_cMD` list (first study only) are replaced by `posthoc_gmhi_matching.json` and the 13/43 count.
   A reviewer who reruns the code will otherwise see a passing gate.

Recommended, not required:
- "reaching the 10% target" → "bringing the FPR to or below the 10% target (0.08)".
- Graphical abstract panel 3 subtitle → "cut-off from 100 local people (no labels)".
- Add the study-clustered CI for the Q2 r (about 0.69–0.86) to S7.
- Give a Mongolia-as-East-Asian sensitivity check for both indices in one SI line.
- Trim number density in the atlas paragraph.

### Author-only items (these cannot be done by the agent)
- Author list, affiliations, corresponding author; CRediT contributions; conflict of interest; funding;
  acknowledgments.
- AI-use statement (Wiley policy).
- Make the GitHub repository public, archive it on Zenodo, tag the fprcal release; insert the URL and DOI (Data
  Availability, cover letter).
- Right of reply: send both the GMWI2 and GMHI audits to their developers before submission and state this in the cover
  letter.
- Suggested reviewers; check current iMeta Letter limits (words, figures, graphical abstract, keywords).
- Sign the cover letter and confirm all authors approve.

## 5. Estimated acceptance probability at iMeta: about 45% (plausible range 35–55%)

**For acceptance:**
- The question is clinically meaningful and practical: a fixed-cut-off FPR in healthy populations.
- The data are field-wide.
- An audit of two released indices brings a mechanism test.
- Pre-registration-style rigour is unusual in this literature.
- A tested tool is included.
- The paper is above the benchmark P75 on most dimensions.

**Against acceptance:**
- The spectrum effect and country confounding are known, so some reviewers will call it incremental.
- 27 of 28 atlas classifiers are research refits.
- The GMHI transport part failed QC, so the second-index evidence is in-sample on largely shared data.
- Results are retrospective only.
- The Letter is very dense.
- An audit of named published indices invites a defensive developer review; right of reply mitigates this.

Base rates for well-prepared Letters at iMeta, adjusted upwards for quality, give about 45%.
