# Handling-editor final pre-submission check: iMeta Letter, v16

**Manuscript:** "Gut-microbiome disease tests flag 0–77% of healthy people at the same cut-off, depending on the population"
**Package checked:** `submission_final_v16/` (manuscript_v16.md/.docx, supporting_information_v16.md/.docx, si_tables_v16.md, figures incl. graphical abstract, highlights.md, cover_letter_v16.md), `code/tool` (fprcal), `REPRODUCE.md`, `environment.yml`, `manuscript/source_data_v16/README.md`.
**Date:** 2026-11-25. I scored this blind: I did not read earlier reviews or scorecards. From `journal_selection/benchmark_v2/scorecard.md` I read only the dimension anchors and the P75 table.

---

## 1. What I checked independently

| Check | Result |
|---|---|
| `python3 -m pytest -q` in code/tool | **19 passed** (42 s) |
| Submission PNGs vs `manuscript/figures_v16/` and `graphical_abstract/` | byte-identical (all 5) |
| Atlas numbers vs Table S2a and `source_data_v16/figure1/v5_perpop_strict.csv` | I² range 0.64–0.97, out-of-band 50–97%, LASSO PI upper end 0.22 (CRC) to 0.81 (IGT), pooled CRC 0.058, 489 LASSO pairs, 45% > 0.15 and 24% < 0.05: **all match** |
| IGT LASSO range in populations ≥ 100 | 0.088–0.770: **matches "0.09 to 0.77"** |
| Exact Beta law, N = 100, k = 91: P(FPR > 0.15) | 0.0551: **matches 0.055** |
| GMWI2 training studies (source data, 44 studies) | 13 East Asian (CN/JP/KR) median 0.636, 31 others 0.124; all 8 studies > 0.5 are CN/JP; Mann–Whitney P = 5.3 × 10⁻⁷; rural Africa 0–7%: **all match** |
| GMWI2 unseen strict (Table S9, results json) | 15 populations, 1,914 people, range 0–0.54, 12/15 outside 0.104–0.313 (8 below, 4 above), 9% expected, raw P 6.1 × 10⁻¹³ → Holm 1.8 × 10⁻¹² ≈ "2 × 10⁻¹²"; East Asian median 0.38 vs 0.06; QC r = 0.991: **all match** |
| Case-mix odds ratio (1,574/948)/(1,097/4,450) | 6.73: **matches 6.7** |
| Within-site burn-in, Table S5 | 28/28 improved, 646 evaluations (2 × 323), 11–13 populations: **matches** |
| Key references (Poyet *Cell* 2026, CRC-TrustBench 2026, Degregori *iMeta* 2026, Li 2025, Piccinno 2025) | resolve on Crossref with the cited titles |
| Body length | about 2,050 words of main text plus about 110 words of Methods; 3 figures + 1 SI figure; 32 references |

The numbers are unusually well controlled. All but one of the problems below are about labelling or framing, not computation.

---

## 2. Title, highlights and abstract-level claims against the text

**(a) "0–77%" is described as "28 classifiers", but it holds only for the 14 LASSO tests in populations of ≥ 100.** The main text states the restriction correctly ("in populations of at least 100 people ... across tests", LASSO paragraph), and so does graphical-abstract panel 1 ("14 LASSO tests; dots = populations of ≥ 100"). The following do not:
- Highlight 1: "28 gut-microbiome classifiers for 14 diseases flagged 0–77% of healthy people across 36 general-population cohorts".
- The graphical-abstract summary paragraph: "the same cut-offs of 28 disease classifiers flagged 0% to 77%".
- The cover letter: "the realised rate ranged from 0% to 77%".

From the source data, with RF included the maximum in populations ≥ 100 is **0.87** (HF RF in LiuW_2016, n = 110, AUROC 0.75). Over all strict populations (≥ 20 people) it is 0.87 for both LASSO and RF. The claim is therefore understated, not inflated, but it is wrong as worded. **REQUIRED:** either say "14 LASSO tests ... in populations of ≥ 100 people", or report 0–87% for the 28 classifiers.

**(b) The headline 77% comes from a near-chance classifier.** IGT LASSO has out-of-fold AUROC 0.537 and a pooled FPR of 0.42. The title, graphical abstract and first Results paragraph all use it as the leading example. Among LASSO tests with AUROC ≥ 0.65, the maximum in populations ≥ 100 is 0.59 (CAD). A reviewer will notice this within minutes. The finding survives, because HF RF (AUROC 0.75) reaches 0.87 and the AUROC ≥ 0.65 restriction leaves I² unchanged. **REQUIRED:** give the IGT AUROC (0.54) where IGT is used as the example. **RECOMMENDED:** take the title or highlight number from a classifier with credible discrimination, for example "up to 87%" (HF RF) or "up to 59% for tests with AUROC ≥ 0.65".

**(c) "AUROC did not predict which cohorts failed"** (Highlight 1) is not what was tested. The text tests whether AUROC predicts the *between-population spread τ* (ρ = −0.06). **REQUIRED:** change to "AUROC did not predict how much the FPR varied".

**(d) The title says "Gut-microbiome disease tests".** The 28 atlas classifiers are the authors' own refits with fixed settings, and seven have AUROC < 0.6 (three < 0.5). They are not published or deployed tests; only GMWI2 is. **RECOMMENDED:** use "classifiers" in the title, or a phrase such as "disease classifiers, and a published index,", so readers do not take them for clinical tests.

**(e) The GMWI2 mechanism wording is somewhat stronger than the evidence.** The highlight says "retraining traced this to the geographic make-up of the training data", and the section heading reads "...mislabels healthy East Asian cohorts through its training data". The evidence:
- Pooled retraining on cMD reproduces the gap.
- Country × label reweighting cuts it by 88%, but the CI is 41–149% and the East Asian median (0.29) stays above the training FPR.
- Within-country label balancing removes 37% (absolute CI −0.04 to 0.31).
- Country is confounded with laboratory.

The body states all of this candidly. The highlight and heading should match. **RECOMMENDED:** "retraining links this to..." or "is consistent with...".

**(f) Other headline numbers all check out:** 36 populations / 6,525 / 20 countries; 64% vs 12%; −62% (0.101 → 0.038, 28/28); I² 0.94; the sensitivity cost 0.46 → 0.21–0.23.

**(g) Minor precision point.** The main text says the population "explained less than a fifth of the variance ... so our pre-stated threshold of 20% ... was not met". S2.1 says the share is 17% of total variance but 20.2% net of sampling noise, "exactly at the threshold, inconclusive under either definition". **REQUIRED (one clause):** align the two, for example "17% (20.2% net of sampling noise), at the pre-stated 20% threshold: inconclusive".

---

## 3. Remaining REQUIRED changes (content; authors can fix in under a day)

1. Fix the "28 classifiers / 0–77%" wording in Highlight 1, the graphical-abstract summary and the cover letter (§2a).
2. Give the IGT LASSO AUROC (0.54) where IGT is the example (§2b).
3. Change "AUROC did not predict which cohorts failed" to the claim that was actually tested (§2c).
4. Align the variance-decomposition wording between the main text and S2.1 (§2g).
5. **Remove internal-process language from the SI.** It is present in both the .md and the .docx:
   - Heading S6.6 "Review round 11: ..." → for example "Post hoc analysis of the v6b weighting; why v6c is uninterpretable".
   - Heading S6.7 "Corrections after review round 10 (bootstrap code)" → "Corrections to two cluster bootstraps".
   - S2.1 "Results moved from the main text (unchanged numbers)" → "Additional results".
   - S2.1 "added in review round 9 (post hoc)" → "(post hoc)".
   - "the v12 analysis" → "the original analysis".
   - In S6.6 and S6.7, the script names (`posthoc_v6b_withincountry.py`, `corrected_boot_v13.py`) are acceptable, but the round numbers are not.
6. **Stale version labels in the submitted SI:**
   - The title says "Supporting Information (manuscript v15)".
   - S1 points to `figures_v15/figureS1_site_methods.pdf` and `si_tables_v15.md`.
   - The si_tables header reads "(v15; content as v12)" and cites `supporting_information_v15.md`.
   - Code paths are given as `Target_Journal_Submission/code/` and should be repository-relative once the repository is public.

   Remove all version tags and refer to "Figure S1" and "Tables S1–S25 (this file / Supporting Tables file)".
7. **The v6c result is still displayed as if it were interpretable.** The S6.5 table and the S5 plan table give C1 as "met on the logit scale". S6.6 then says the v6c implementation did not match the plan and the balanced arm is "uninterpretable". Mark the S6.5 table and the S5 row as uninterpretable (implementation deviated from plan) so a reader of the table alone is not misled.
8. **S5 table, v6b row:** "B1, B2, B4 supported" should say "B2 supported on the point estimate only; CI 41–149% includes values below the criterion", as the main text already does.
9. **Supporting tables file format.** `si_tables_v16.md` must be supplied in a format the journal accepts (it is already embedded in supporting_information_v16.docx; confirm this, and drop the .md from the upload set).
10. **Check the format against the current iMeta author guidelines for Letters:** word limit, reference cap (32 here), number of highlights and words per highlight, and graphical-abstract dimensions. The content is close to the usual Letter size, but I could not confirm the current limits offline.
11. **Clean up the reproducibility documents.** REPRODUCE.md is titled "Reproducing manuscript v15". source_data_v16/README.md is headed "manuscript v15", calls the v16 scripts "in progress", and says the rebuild check compares against `figures_v15/`. Update these to v16 and re-run `rebuild_figures.py` against `figures_v16/` (Figures 2 and GA changed in v16). This does not block submission, but reviewers who open the repository will see it.

### Figure notes (RECOMMENDED, not blocking)
- **Fig 3A:** the 28 rows have no labels, so a reader cannot tell which classifier is which (the IGT LASSO outlier at 0.32 especially). Add test/model labels or mark the two outliers.
- **Fig 2D:** the regional-median diamonds are offset from the line ends. State this in the legend, or align them. Also give the other-region median after reweighting (≈ 0.22), so the 0.06 gap can be read off the figure, and note that part of the gap closes because non-East-Asian FPRs rise (S2.1: "several European studies were flagged more often").
- **Fig 1B:** the colour bar is labelled "log scale". Confirm the ticks are log-spaced and not logit-spaced. They read as roughly log, which is fine.

---

## 4. Author-only items (cannot be completed by the editor or the analysis)

- Author list, affiliations, ORCID, corresponding author (manuscript and cover letter).
- CRediT author contributions.
- Funding statement.
- Conflict-of-interest statement (manuscript and cover letter "[Competing interests: authors to confirm]").
- AI-use statement. Describe the use of AI in analysis code and drafting; this must be accurate and specific.
- Repository URL and Zenodo DOI (Data Availability, cover letter, SI code paths). Mint the DOI from the tagged submission commit, and make sure the deposit includes the GMWI2 inputs only as licences permit. The Nat Commun Supplementary Data are CC BY and gmwi2 is MIT.
- **Right of reply to the GMWI2 developers** (cover-letter placeholder). Send the audit (Fig 2, S6) to the corresponding authors of Chang et al. 2024 before submission, record the date and any response, and remove the bracketed note. Given that the paper names a released index and an ethnic/geographic group, I regard this as a precondition for submission, not a courtesy.
- Further acknowledgments, the cover-letter date and signature, and suggested reviewers. Choose reviewers with no link to GMWI2 or to the authors; one diagnostic-test methodologist and one microbiome ML expert are advisable.

---

## 5. Blind score (iMeta scorecard v2 anchors)

| # | Dimension | Score | P75 | Rationale |
|---|---|---|---|---|
| 1 | Biological / clinical significance | **7** | 8.0 | The question is clinically real: a screening cut-off decides how many colonoscopies follow. But 27 of the 28 atlas classifiers are the authors' research refits, not tests in use. The GMWI2 audit is the concrete, high-relevance part. Between the 6 and 9 anchors, nearer 6–7 for the atlas and 8 for the audit. |
| 2 | Scale and breadth | **8** | 8.0 | 36 strict / 55 full healthy populations, 6,525 / 8,160 people, 20 countries; GMWI2 data of 8,069 samples / 54 studies; retraining on 10,986 / 61 studies. Not a field-wide census. |
| 3 | Novelty vs prior art | **7** | 7.0 | The spectrum effect and cross-population failure are known: refs 1, 10–13 already show pieces of it. New here: a cross-disease FPR atlas with prediction intervals, a quantified audit of a released index with a retraining test, and a non-random-split test of a known label-free rule. Partly anticipated, but it adds a clear new angle. |
| 4 | Rigor and statistics | **8** | 7.25 | Time-stamped pre-specified plans with falsification criteria, failed hypotheses reported, I² and prediction intervals, clustered CIs, Holm, full-set sensitivity, AUROC restriction, covariate models, exact Beta/binomial laws. Points lost: the strict set is post hoc; two bootstrap bugs were found late (now corrected and disclosed); B2 has a wide CI; v6c had an implementation error. |
| 5 | External validation | **8** | 7.0 | Every classifier is evaluated in up to 36 never-seen populations; leave-one-study-out retraining for GMWI2; cross-site burn-in failure and failed corrections are reported. The one weakness is a single profiling pipeline (MetaPhlAn3). |
| 6 | Resource / tool value | **7** | 5.75 | fprcal: documented, tested (19 tests pass), CLI with atlas lookup, verify, cut-off, plan and score (14 LASSO models), plus the atlas tables. Not yet on PyPI or conda, no web interface, and the repository URL/DOI are pending. |
| 7 | Figures | **7** | 7.0 | Fig 1 (map + heatmap + PI + AUROC) tells the atlas story at a glance, Fig 2 tells the audit, Fig 3 the fix and its cost, and the graphical abstract is clean. Fig 3A rows are unlabelled; Fig 2D median markers are offset. |
| 8 | Clarity and framing | **7** | 7.25 | One-sentence problem, finding-sentence headings, a sticky number, candid limits. Points lost: dense numeric sentences in the GMWI2 reweighting paragraph; the "28 classifiers 0–77%" and "which cohorts failed" mismatches; the headline number comes from a near-chance classifier; process language in the SI. |
| 9 | Reproducibility | **8** | 7.25 | All inputs public; pinned environment; step-by-step REPRODUCE.md; per-panel source data with a pixel-identical rebuild script; fresh-clone rerun logged; result files committed. Not 9 yet: no public URL/DOI, and stale v15 labels in the documentation. |
| 10 | Actionable insight | **8** | 7.0 | A concrete fix tested on retrospective non-random within-site hold-outs (28/28 classifiers, 13/13 populations), with its failure mode (across sites) and its price (sensitivity) quantified; the GMWI2 mechanism is tested by retraining. Not prospective, so not 9. |
| | **Total** | **75 / 100** | 69.25 | Above P75 overall and above the benchmark maximum of 73 except imt2.70192 (78). Below P75 on dimension 1 (7 vs 8) and marginally on dimension 8 (7 vs 7.25). |

If the required text fixes in §3 are made, dimension 8 would reasonably move to 8 (total 76). Dimension 1 is limited by design: the atlas uses research classifiers. Wording cannot fix that, but it can stop readers overreading it.

---

## 6. Decision

**Send to review**, after the required items in §3 and the author items in §4 are completed. Nothing here warrants a desk reject:
- the topic fits iMeta's microbiome data-science and translation readership;
- the data are broad;
- the analysis is unusually transparent;
- a released index is audited with care over the group-labelling issue.

**Predicted first-round outcome:** major revision (about 55%), minor revision (about 30%), reject after review (about 15%). Reviewers are likely to press on five points:
1. The atlas classifiers are the authors' own and include near-chance models; ask for the headline on credible classifiers only, or on published models with released weights.
2. "Population" is confounded with study processing. They may ask for at least one batch-correction comparator (MMUPHin or ConQuR), whose omission the authors acknowledge.
3. The GMWI2 mechanism rests on a reweighting with a wide CI and a lab–country confound. Expect a response from the GMWI2 developers if they review.
4. The burn-in rule is acknowledged to be standard (conformal / order-statistic). Its contribution is the empirical stress test, and reviewers may call it incremental.
5. The strict set and the East Asian contrasts were chosen post hoc.

## 7. Probability of acceptance at iMeta

**About 45% overall from submission** (plausible range 35–55%). Conditional on going to review, about 60%.

The manuscript is numerically sound: every headline number I recomputed from the source data matched. It is reproducible to a standard above the iMeta benchmark median, and it has a clear, practice-relevant message: report the FPR per held-out population with a prediction interval next to AUROC, and verify cut-offs locally. The GMWI2 audit gives it a concrete, citable hook, and the pre-specified, falsification-style reporting will reassure statistical reviewers.

Three things hold the estimate below 50%:
- **Desk-rejection risk.** iMeta selects strongly at the desk for Letters, and the core idea (the spectrum effect) is known in clinical epidemiology and partly shown for microbiome CRC models.
- **The atlas classifiers.** They are research refits, some near chance, which invites the objection that the heterogeneity is partly a property of weak models.
- **The GMWI2 audit.** It concerns a released tool and a named geographic group, so it will draw careful and possibly adversarial review. The outcome depends on the developers' right of reply and on how persuasive the reweighting test (88% gap reduction, CI 41–149%) is judged to be.

Fixing the highlight and title framing (§2a–d) and completing the author statements before submission removes the avoidable risks. The remaining uncertainty is scientific and normal for a review.
