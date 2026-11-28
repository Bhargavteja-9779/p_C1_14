# Editor pre-submission check, blind (r17), manuscript v18

Reviewer role: handling editor, iMeta, reading as a statistician.
Read: scorecard anchors and P75 table; submission_final_v18 (manuscript, SI, SI tables, highlights, cover letter, all 7
PNGs); result files and scripts in code/experiments/atlas/v4–v7; all protocol_*.md files.
Not read: reviews/, SUBMISSION_REPORT.md, HANDOFF.md, FINAL_REPORT.md, state/, journal/.

## Summary of the paper

The Letter asks how many healthy people a gut-microbiome classifier flags at its published cut-off. It scores 28
classifiers (14 diseases, LASSO and RF) in 36 healthy populations (6,525 adults). The FPR at a cut-off set for 0.10
ranges from 0 to 0.87. AUROC does not predict the spread. Two released health indices (GMWI2, GMHI) flag most healthy
East Asian people in their own training data. Retraining GMWI2 with country × label balancing closes that gap. A local,
label-free burn-in of 100 people cuts the within-site FPR error by 62%, at a cost in sensitivity.

The work is careful. Plans were written before the runs. Failed hypotheses are reported in the SI. Every number I
checked matches the result files. My concerns are about framing of some null and borderline results, one deviation that
is described too briefly, and the density of the text for a Letter.

## 1. Number spot-check (55 checks)

| # | Claim (where) | Source | Status |
|---|---|---|---|
| 1 | 36 strict populations, 6,525 adults, 20 countries (MS, HL, CL, GA) | v4/results/counts_v4.json; v5_perpop_strict.csv | OK |
| 2 | 55 populations, 8,160 people (MS) | counts_v4.json; v5_perpop_full.csv | OK |
| 3 | 28 classifiers, 14 diseases, 26 training cohorts (MS) | v5/results/training_cohorts_v5.json; v5_het_strict.csv | OK |
| 4 | FPR 0 to 0.87 in populations of ≥ 100 (title, MS, HL, CL) | v5_perpop_strict.csv: max 0.873 (HF RF, LiuW_2016, n = 110) | OK |
| 5 | Max classifier AUROC 0.75 (HF RF) | v5_het_strict.csv: 0.748 | OK |
| 6 | I² median 0.94, range 0.64–0.97 | v5_summary.json H1_strict | OK |
| 7 | 28/28 also in full set | v5_summary.json H1_full I2_ge_050 = 28 | OK |
| 8 | PI upper end 0.22 (CRC) to 0.81 (IGT) | v5_het_strict.csv pi_hi 0.218 / 0.809 | OK (wording ambiguous, see R5) |
| 9 | IGT AUROC 0.54 | v5_het_strict.csv 0.537 | OK |
| 10 | Pooled CRC FPR 0.06 | v5_het_strict.csv 0.058 | OK (framing issue, R4) |
| 11 | Spearman ρ = −0.06, P = 0.76 | v5_summary.json expl_auroc_vs_tau | OK |
| 12 | 16 classifiers with AUROC ≥ 0.65, I² median 0.94 | v5_summary.json; recomputed 0.942 | OK |
| 13 | Population share 17% (LASSO) | v5_summary.json pop_share 0.174 | OK |
| 14 | 20.2% net of sampling noise | v5/results/h2_sampling_v13.json net pop 0.202 | OK (framing, R2) |
| 15 | Classifier–population pair "about half" | h2_sampling_v13.json pair 0.48 (share of total) / 0.56 (net) | OK |
| 16 | Seven classifiers with AUROC < 0.6 | v5_het_strict.csv: 7 | OK |
| 17 | 119 duplicate samples removed | counts_v4.json dedup.excluded_samples | OK |
| 18 | GMWI2: 95 taxa, 8,069 samples, 54 studies | v6/results/counts_v12.json | OK |
| 19 | GMWI2 developer FPR 20.8% | gmwi2_results.json alpha 0.2084 | OK |
| 20 | GMWI2 own data: 0–84%, 44 studies, I² = 0.96 | gmwi2_published_training.json | OK |
| 21 | All 8 studies > 50% from China or Japan | same file, over_half | OK |
| 22 | EA median 0.64 (13) vs 0.12 (31), two-sided P = 5 × 10⁻⁷ | gmwi2_eastasia.json; posthoc_r16_sensitivity.json ("two-sided") | OK |
| 23 | 15 unseen populations, 1,914 people, r = 0.991 | gmwi2_results.json | OK |
| 24 | Unseen FPR 0 to 0.54 | gmwi2_results.json | OK |
| 25 | 12/15 outside 0.10–0.31, 9% expected, Holm P = 2 × 10⁻¹² | gmwi2_results.json G2; holm_v6_v13.json 1.8e-12 | OK |
| 26 | Four unseen EA: 0.25–0.54, median 0.38 vs 0.06, one-sided P = 0.020 | posthoc_eastasia_strict_v15.json | OK (full-set P = 0.065 not in MS, R6) |
| 27 | GMWI2 burn-in error 0.21 → 0.04 | gmwi2_results.json G4 0.211 → 0.044 | OK |
| 28 | GMHI own data 3–90%, 21 studies, I² = 0.96 | v7/results/gmhi_dev_perstudy.csv; gmhi_results.json H1 | OK |
| 29 | GMHI EA 0.67 (8) vs 0.21 (13), one-sided P = 0.0007, Holm | gmhi_results.json H2 and holm | OK |
| 30 | 83% of GMHI healthy samples in GMWI2 training | posthoc_gmhi_gmwi2_overlap.json 0.825 | OK |
| 31 | Six non-shared studies 0.63 vs 0.17, P = 0.10 | same file | OK |
| 32 | Q2 as planned: 101 samples, r = 0.80 | gmhi_results.json Q2 0.803 ("pass": true) | OK (but see R1) |
| 33 | Corrected Q2: r = 0.795, 2,190 samples | posthoc_gmhi_matching.json | OK |
| 34 | 4 of 7 health-prevalent species missing under MetaPhlAn3 names | v7/results/README.md; gmhi_results.json MH list | OK |
| 35 | Share flagged 23% → 43% (MS, CL, Fig S2B) | posthoc_gmhi_matching.json 0.227 → 0.433 | OK |
| 36 | Top five taxa explain 39% of gap | v6/results/numbers_v14.json 0.389 | OK |
| 37 | B. plebeius 72% vs 17% | numbers_v14.json 0.724 / 0.175 | OK |
| 38 | Klebsiella 59% vs 22% | gmwi2_eastasia.json 0.592 / 0.216 | OK |
| 39 | EA 62% of non-healthy, 20% of healthy, OR 6.7 | gmwi2_casemix.json | OK |
| 40 | Retraining on 10,986 people, 61 studies | counts_v12.json | OK |
| 41 | Pooled training: EA 0.71 vs other 0.19 | v6b_results.json naive | OK |
| 42 | Gap 0.52 → 0.06 | v6b_results.json | OK |
| 43 | Reduction 88%, clustered CI 41–149% | corrected_boot_v13.json v6b | OK |
| 44 | Within-country balancing 37%, CI includes 0 | posthoc_v6b_withincountry.json (abs CI −0.04 to 0.31) | OK |
| 45 | B3 (AUROC cost) failed | v6b_results.json B3 supported false, diff −0.040 | OK |
| 46 | 13 populations with ≥ 120 people; 646 evaluations | v5/results/numbers_v11.json H4 | OK |
| 47 | Error 0.101 → 0.038, −62%, 28/28 | v5_summary.json H4; numbers_v11.json | OK |
| 48 | Clustered CI 51–70% | v5/results/h4_cluster_ci_v11.json 0.508–0.695 | OK |
| 49 | Training cut-off flags 29% of controls; sensitivity 0.46 → 0.21–0.23 | v4/results/deploy_v4_cc_summary.csv N = 100 | OK |
| 50 | N = 100: P(FPR > 0.15) = 0.055 | recomputed Beta(10, 91) tail = 0.0551 (k = 91) | OK |
| 51 | Binomial check detects most pairs > 0.25 at n = 100 | v5/results/verify_power_v5.json | OK |
| 52 | Fig 2D reweighted EA median 0.29, other 0.22 | v6b_results.json balanced | OK |
| 53 | GA panel 2 medians 0.64 / 0.12, 13 / 31 studies | gmwi2_eastasia.json | OK |
| 54 | GA panel 3: −62%, 28/28 | v5_summary.json | OK |
| 55 | HL/CL: "GMHI 67% vs 21%" | gmhi_results.json | OK |

No mismatches. Three numbers are correct but framed in a way a reviewer may challenge (items 8, 10, 14), and two
deviations are reported more fully in the SI than in the main text (items 26, 32).

## 2. Claims, post hoc labelling, sidedness, deviations

**Good.** Plans for v5, v6, v6b, v6c and v7 exist and are dated before the runs. SI S5 lists every plan and its outcome,
including failures (v5 H3, G3, B3, v6c C2/C3). The strict set and the East Asian contrasts are called post hoc in the
main text and in the Limitations. Sidedness is stated for the main contrasts (two-sided for GMWI2 training data,
one-sided for the unseen and GMHI comparisons), and SI line 60–61 lists it for all. Holm is used within each plan. The
v6c implementation error is disclosed and the arm is not used. The authors say clearly that index behaviour is not
evidence about East Asian microbiomes.

**Issues.**

1. *GMHI reproducibility gate (v7 Q2).* As planned, Q2 passed narrowly (r = 0.803 on 101 samples from 2 studies;
   gmhi_results.json "pass": true). The authors then fixed the accession matching and got r = 0.795 on 2,190 samples,
   so they withheld H3–H6. This is a conservative and defensible call, but it is a post-result deviation. The main text
   says "As planned, it matched only 101 samples (r = 0.80); after we corrected the matching in review". A reader will
   not know that the planned gate passed, or what "in review" means. The cluster CI for r (0.69–0.86) straddles 0.80,
   so the gate is uninformative either way. Say this in plain words.
2. *v5 H2.* The plan judged the population share of total between-unit variance, separately for LASSO and RF:
   ≥ 20% supported, < 10% wrong. LASSO 17% is inconclusive. RF 7.5% is falsified. The main text gives only LASSO, and
   puts a post hoc "20.2% net of sampling noise" next to the 20% threshold. That invites the reading that it was met.
3. *Null result read as evidence of absence.* "AUROC did not predict the spread (ρ = −0.06, P = 0.76) … A better
   classifier was not a more portable one." With 28 classifiers the 95% CI for ρ is about −0.44 to 0.34. A moderate
   link cannot be excluded.
4. *"Pooled over populations, the same tests looked well calibrated (CRC 0.06)."* Pooled LASSO FPRs range from 0.06 to
   0.42 (IGT 0.42, fatty liver 0.26, schizophrenia 0.23). Many pooled values are not well calibrated. CRC 0.06 is also
   off target, just in the safe direction.
5. *One-sided post hoc test.* Unseen East Asian vs other uses a one-sided test chosen after the training-data result.
   The direction is justified by that result, but the main text should say so and also give the full-set value
   (P = 0.065, SI line 61). Four East Asian populations is a small base.
6. *"We report the hypotheses that failed."* True for the SI, but the main text names only B3 and Q2. Pre-specified
   failures or inconclusive results not named in the main text: v5 H2 (RF), H3, H5/H6, GMWI2 G3. One sentence pointing to
   S5 fixes this.
7. *Mechanism heading.* "WHY: THE GEOGRAPHIC MAKE-UP OF THE TRAINING DATA" is stronger than the evidence: the
   88% reduction has a CI of 41–149%, within-country balancing also removes 37%, country is confounded with lab and
   sequencing, and the same idea did not carry over to the disease classifiers (v6c, uninterpretable). The body text
   is appropriately hedged; the heading is not.
8. *Title number.* "0–87%" is the extreme of about 1,000 classifier × population estimates, from one population of 110
   (Mongolia, HF RF). It is true and stated with the n ≥ 100 rule, but it is an extreme order statistic. A robust number
   exists: 26% of LASSO classifier–population pairs had FPR > 0.25 against a 0.10 target (numbers_v11.json). Not wrong,
   but a statistical reviewer may object.
9. *Cover letter.* "A fresh-clone rerun reproduces every result file." SI S6.6 says rerunning run_v6c.py gives slightly
   different numbers (liblinear). Qualify the sentence.

No claim I checked is false. The overstatement risk is in items 3, 4, 7 and 8.

## 3. Figures (all PNGs viewed)

- **Figure 1.** Strong. Map + heatmap + prediction intervals + AUROC scatter tell the whole atlas. Heatmap is dense (36
  columns) but readable. Log colour scale: FPR = 0 cells are shown at the 0.01 colour; say so. Panel D: RF points at
  AUROC ≈ 0.44–0.45 sit on the left spine and look clipped; extend the axis.
- **Figure 2.** Clear four-step story (own data, unseen data, taxa, retraining). Good.
- **Figure 3.** Clear. Panel B shows the sensitivity price honestly.
- **Figures S1, S2.** Clear. S2B makes the profiler point well.
- **Graphical abstract.** Three panels, one claim each, correct numbers. Panel 1 shows LASSO only (max 0.77) while the
  title says 87%; acceptable because the subtitle says "14 LASSO tests".

## 4. Clarity and writing (judged independently)

- Length: about 1,960 words from "To the Editor" to Methods. Mean sentence 19 words. Headings are finding sentences.
  The opening is good: the problem is stated in three sentences.
- Number density is high: about 200 numeric tokens in 1,960 words, about one every ten words. Several paragraphs read
  as a list of statistics (GMWI2 unseen paragraph; GMHI paragraphs; variance decomposition sentence).
- Too many threads for a Letter: atlas, two index audits, a mechanism test, a profiler-version finding, a local fix,
  and a verification test. The GMHI section (two paragraphs, plus the Q2 story) is the hardest to follow and adds the
  least new information, because 83% of its data is shared with GMWI2.
- Some sentences are ambiguous: the prediction-interval sentence ("reached from 0.22 to 0.81" means the upper bounds),
  "after we corrected the matching in review", and "20.2% net of sampling noise, inconclusive against our pre-stated
  20%".
- The burn-in formula is fine in the main text, but the paragraph that follows mixes three ideas (expected FPR, exact
  distribution, PAC rank). It could be two sentences.

Overall: clear framing, good headline, but the body is denser than the best iMeta Letters. Score 7, just below P75.

## 5. Scores (1–10, scorecard anchors)

| # | Dimension | Score | P75 | Reason |
|---|---|---|---|---|
| 1 | Biological / clinical significance | 8 | 8.0 | Fixed-cut-off FPR drives referrals; audit of two released indices; affects how many published tests are used. |
| 2 | Scale and breadth | 8 | 8.0 | 36 (55) populations, 6,525 (8,160) people, 20 countries, 28 classifiers, plus 8,069 and 10,986 retraining samples. |
| 3 | Novelty | 7 | 7.0 | Spectrum effect and cross-cohort FPR shifts are known; the cross-disease atlas and index audits are new. |
| 4 | Rigor and statistics | 8 | 7.25 | Dated plans with falsifiers, Holm, PIs, clustered CIs, sensitivity sets, failures reported; minus post hoc one-sided tests and H2/Q2 framing. |
| 5 | External validation | 8 | 7.0 | Every held-out population, LOSO retraining, cross-site failure of the fix reported. |
| 6 | Resource / tool | 6 | 5.75 | Atlas, coefficient tables and fprcal tool described; repository not yet public, so not verifiable by reviewers. |
| 7 | Figures | 7 | 7.0 | Fig 1 tells the study at a glance; minor axis/colour issues; Fig 1B is dense. |
| 8 | Clarity and writing | 7 | 7.25 | Good headline and finding headings, but high number density and too many threads for a Letter. |
| 9 | Reproducibility | 7 | 7.25 | Public data, code, plans, source data; URL/DOI placeholders and non-deterministic v6c rerun. |
| 10 | Actionable insight | 7 | 7.0 | Concrete label-free fix tested on non-random within-site splits; retrospective only, sensitivity cost shown. |
| | **Total** | **73** | **69.25** | Above P75 total; below P75 on 8 and 9. |

Dimension 9 should rise to 8 once the repository and Zenodo DOI are live. Dimension 8 can rise to 8 with R9.

## 6. Decision

**Send to external review.** If I were deciding after review on this version, I would expect **minor revision**. There
is no error in the numbers, the design is pre-specified and honest, and the claims are mostly hedged. The required
changes are wording and disclosure, not new analyses.

### REQUIRED changes (authors can make them now)

- **R1. GMHI gate.** Say plainly that the planned Q2 gate passed narrowly (r = 0.803, 101 samples, 2 studies), that a
  matching error was found afterwards, that the corrected r was 0.795 (study-clustered 95% CI 0.69–0.86), and that
  withholding H3–H6 is a deviation made after seeing results. Replace "in review" with "on re-checking". Add that the
  withheld results pointed the same way (S7), so the deviation is conservative.
- **R2. H2 reporting.** Lead with the pre-specified measure: LASSO 17% (inconclusive, between 10% and 20%), RF 7.5%
  (falsified). Label the 20.2% net-of-sampling figure as post hoc or move it to the SI.
- **R3. AUROC null.** Give the 95% CI for ρ (about −0.44 to 0.34) and replace "A better classifier was not a more
  portable one" with "We found no evidence that better classifiers have more portable FPRs".
- **R4. Pooled calibration sentence.** Correct it: pooled FPRs range from 0.06 to 0.42 across LASSO tests; say that a
  pooled value near target (for example CRC) can hide a wide spread.
- **R5. Prediction-interval sentence.** Say that 0.22–0.81 are the upper ends of the 95% prediction intervals.
- **R6. Unseen East Asian GMWI2 test.** State why it is one-sided (direction fixed by the training-data result) and give
  the full-set result (P = 0.065) next to the strict-set result (P = 0.020).
- **R7. Failed hypotheses in the main text.** Add one sentence: "Pre-specified hypotheses that failed or were
  inconclusive (v5 H2–H3, H5–H6; GMWI2 G3; v6b B3) are listed in S5."
- **R8. Cover letter reproducibility claim.** Qualify "reproduces every result file" (v6c rerun differs slightly;
  SI S6.6).
- **R9. Readability.** Cut number density in the main text by about a quarter. Suggested: merge the two GMHI paragraphs
  into one (keep 0.67 vs 0.21, the 83% overlap and the 23% → 43% profiler shift; move the Q2 detail to S7 with a
  one-line pointer); move secondary statistics already in figures (exact-interval counts, repeated Holm P values) to
  legends or the SI; split the burn-in theory paragraph into two short sentences.

### Recommended changes

- Soften the heading "WHY: …" to "A LIKELY CAUSE: …".
- Add a clause that the same balancing did not reduce FPR spread for the disease classifiers (v6c, post hoc and
  uninterpretable), so readers do not over-generalise the GMWI2 mechanism.
- Consider a robust headline number next to 0–87% (for example, "a quarter of classifier–population pairs flagged more
  than 25% of healthy people at a 10% target").
- Figure 1B: state that FPR = 0 is drawn at the lowest colour. Figure 1D: widen the x-axis so AUROC 0.44–0.45 points
  are not on the spine.
- State the sidedness of the Spearman test and the exact Poisson-binomial test in the main text or legends.
- In the burn-in paragraph, note that the P(FPR > 0.15) = 0.055 value is for π_max = 0.
- One sentence on what a sensitivity of about 0.21 at FPR 0.10 means for positive predictive value in screening.

### Author-only items

- Author list, affiliations, contributions (CRediT), conflicts, funding, acknowledgments.
- AI