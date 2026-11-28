# Review r18: blind handling-editor check of the iMeta Letter (package v19)

Reviewer role: handling editor at iMeta, reading as a statistician.
Blind: I did not read prior reviews, the submission report, handoff or final reports, state/, journal/, other package versions or git messages.
Material read: scorecard anchors and P75 table; manuscript_v19.md, supporting_information_v19.md, si_tables_v16.md, highlights.md, cover_letter_v19.md, README.md; all 6 PNGs in figures/ (Figures 1–3, S1, S2, graphical abstract); result files, scripts and protocols in code/experiments/atlas/v4–v7. I also ran the fprcal test suite (19 passed).

## 1. Summary of the submission

The Letter measures the false-positive rate (FPR) of 28 gut-microbiome disease classifiers (14 diseases, LASSO and RF) at a fixed cut-off (target 0.10) in 36 healthy general-population cohorts (6,525 adults, 20 countries), with the full set of 55 populations as a sensitivity analysis. It then audits two released health indices (GMWI2, GMHI). It finds that both label most healthy people in their own East Asian training studies as non-healthy. It tests a mechanism by retraining the GMWI2 recipe with country × label weights. Last, it tests a known order-statistic rule that resets the cut-off on 100 unlabelled local people. Plans were committed before the confirmatory analyses. Failed hypotheses are reported.

The headline is clear and the work is careful. Most numbers trace exactly to result files. I found one factual misstatement (the RF variance split), one plan deviation that is not flagged as a deviation (the H4 population-size threshold), a few tests whose sidedness is not stated, and some framing that slightly overreaches. All are fixable by the authors in a short revision.

## 2. Spot-check of numbers (46 checked)

Paths are relative to Target_Journal_Submission/code/experiments/atlas/. "MT" = main text, "HL" = highlights, "CL" = cover letter, "GA" = graphical abstract or its summary paragraph.

| # | Claim (where) | Stated | Result file | Found | OK |
|---|---|---|---|---|---|
| 1 | Strict populations / people (MT, HL, CL) | 36 / 6,525 | v5/results/v5_perpop_strict.csv (max n per study) | 36 / 6,525 | yes |
| 2 | Countries (MT, HL, CL) | 20 | si Table S1b, metadata | 20 | yes |
| 3 | Full set (MT) | 55 / 8,160 | v5/results/v5_perpop_full.csv | 55 / 8,160 | yes |
| 4 | FPR range, n ≥ 100, 28 classifiers (title, MT, HL, CL, GA) | 0–0.87 | v5_perpop_strict.csv | 0–0.873 (HF RF, LiuW_2016, n = 110) | yes |
| 5 | Max is HF RF, AUROC 0.75 (MT) | 0.75 | v5_het_strict.csv | 0.748 | yes |
| 6 | LASSO pairs with FPR > 0.25 (MT) | 26% | v5/results/posthoc_r17_numbers.json | 0.2597 | yes |
| 7 | RF pairs with FPR > 0.25 (SI) | 16% | same | 0.1616 | yes |
| 8 | LASSO pairs > 0.15 / < 0.05 (SI S2.2) | 45% / 24% | v5/results/numbers_v11.json | 0.446 / 0.239 | yes |
| 9 | LASSO range n ≥ 100 (SI) | 0–0.77 | numbers_v11.json | 0–0.770 | yes |
| 10 | I² median, strict (MT) | 0.94 | v5/results/v5_summary.json | 0.9365 | yes |
| 11 | I² ≥ 0.5 in 28/28, full set (MT) | 28/28 | v5_summary.json H1_full; v5_het_full.csv | 28/28; max Q p = 2.5e-15 | yes |
| 12 | Upper PI, CRC LASSO (MT) | 0.22 | v5_het_strict.csv | 0.218 (lowest of LASSO) | yes |
| 13 | Upper PI, IGT LASSO (MT) | 0.81 | v5_het_strict.csv | 0.809 (highest of LASSO) | yes |
| 14 | Pooled CRC LASSO (MT) | 0.06 | v5_het_strict.csv | 0.058 | yes |
| 15 | Spearman ρ AUROC vs τ, CI, P (MT, Fig 1D) | −0.06; −0.42 to 0.32; 0.76 | posthoc_r17_numbers.json; recomputed | −0.0597; −0.423 to 0.321; 0.763 | yes |
| 16 | Classifiers with AUROC ≥ 0.65 / their I² median (MT) | 16 / 0.94 | recomputed from v5_het_strict.csv | 16 / 0.942 | yes |
| 17 | AUROC < 0.6 / < 0.5 (MT, SI) | 7 / 3 | si Table S1a | 7 / 3 | yes |
| 18 | Population share of variance, LASSO / RF (MT) | 17% / 7.5% | v5/results/h2_sampling_v13.json | 0.174 / 0.075 | yes |
| 19 | LASSO population share net of noise (SI) | 20.2% | h2_sampling_v13.json | 0.2023 | yes |
| 20 | "Pair explained most of the rest" (MT) | — | h2_sampling_v13.json | LASSO pair 48% of 83% (true); RF classifier 46% vs pair 25% (false for RF) | **no (RF)** |
| 21 | Out-of-band expected by chance / observed (SI) | 15–16% / 50–97% | numbers_v11.json | 0.148–0.162 / 0.50–0.97 | yes |
| 22 | GMWI2 training FPR α (MT) | 20.8% | v6/results/gmwi2_published_training.json | 0.2084 | yes |
| 23 | GMWI2 training: studies, range, I² (MT) | 44; 0–0.84; 0.96 | same | 44; 0–0.843; 0.961 | yes |
| 24 | All 8 studies > 50% from China/Japan (MT) | 8 | same, over_half | 8 (7 China, 1 Japan) | yes |
| 25 | EA vs other median, 13 vs 31, P (MT, HL, CL, GA) | 0.64 vs 0.12; 5e-7 | v6/results/gmwi2_eastasia.json | 0.636 vs 0.124; 5.3e-7 | yes |
| 26 | Unseen strict populations / range (MT) | 15; 0–0.54 | v6/results/gmwi2_results.json | 15; 0–0.537 | yes |
| 27 | G2: 12/15 out of band, 9% expected, Holm P (MT) | 12/15; 9%; 2e-12 | gmwi2_results.json; holm_v6_v13.json | 0.80; 0.090; 1.8e-12 | yes |
| 28 | Unseen EA: 4 populations, 0.25–0.54, median 0.38 vs 0.06, P (MT) | as stated; 0.020 | v6/results/posthoc_eastasia_strict_v15.json | 0.25–0.537; 0.381 vs 0.061; 0.0198 | yes |
| 29 | Same, full set P (MT) | 0.065 | same | 0.0654 | yes |
| 30 | QC r with published scores (Fig 2B legend; SI) | 0.99 (704 samples) | gmwi2_results.json qc | 0.991, n = 704 | yes |
| 31 | Top five taxa explain share of EA–other score gap (MT, Fig 2C) | 39% | v6/results/numbers_v14.json | 0.389 | yes |
| 32 | B. plebeius / Klebsiella carriage EA vs other (SI) | 72/17%; 59/22% | gmwi2_eastasia.json decomposition | 0.724/0.175; 0.592/0.216 | yes |
| 33 | EA share of non-healthy / healthy training samples; OR (MT, SI) | 62% / 20%; 6.7 | v6/results/gmwi2_casemix.json | 0.624 / 0.198; 6.74 | yes |
| 34 | Retraining cohort size (MT) | 10,986 in 61 studies | v6/results/counts_v12.json | 10,986; 61 | yes |
| 35 | Pooled retraining EA vs other; gap (MT) | 0.71 vs 0.19; 0.52 | v6/results/v6b_results.json | 0.711 vs 0.186; 0.524 | yes |
| 36 | Reweighted gap; relative reduction; corrected CI (MT, Fig 2D) | 0.06; 88%; 41–149% | v6b_results.json; corrected_boot_v13.json | 0.065; 0.877; 0.406–1.494 | yes |
| 37 | Within-country balancing reduction; CI incl. zero (MT, SI) | 37%; −0.04 to 0.31 | v6/results/posthoc_v6b_withincountry.json | 0.367; −0.042 to 0.314 | yes |
| 38 | Pooled AUROC naive → balanced; CI (SI) | 0.715 → 0.676; −0.12 to +0.02 | v6b_results.json; corrected_boot_v13.json | 0.7155 → 0.6758; −0.119 to 0.023 | yes |
| 39 | GMHI training range, studies (MT) | 3–90%; 21 | v7/results/gmhi_results.json H1; Table S26 | 0.03–0.897; 21 | yes |
| 40 | GMHI EA vs other, one-sided P, Holm (MT, HL, CL) | 0.67 vs 0.21; 0.0007 | gmhi_results.json H2, holm | 0.673 vs 0.205; 6.7e-4 (Holm-adjusted equal, as it is the largest P in the family) | yes |
| 41 | GMHI healthy samples shared with GMWI2 (MT) | 83% | v7/results/posthoc_gmhi_gmwi2_overlap.json | 0.825 | yes |
| 42 | Six unshared studies, one-sided P (MT) | 0.10 | same | 0.10 | yes |
| 43 | GMHI flag rate, same samples, MetaPhlAn2 → 3 (MT, HL, CL, Fig S2B) | 23% → 43% | v7/results/posthoc_gmhi_matching.json | 0.227 → 0.433 (2,190 samples) | yes |
| 44 | Burn-in error, 28/28, CI (MT, HL, CL, GA, Fig 3A) | 0.101 → 0.038; −62%; 51–70% | v5_summary.json H4; v5/results/h4_cluster_ci_v11.json | 0.1008 → 0.0382; 0.620–0.623; 0.508–0.695 | yes |
| 45 | GMWI2 burn-in error (MT) | 0.21 → 0.04 | gmwi2_results.json G4 | 0.211 → 0.044 (−79%, 11/13 populations) | yes |
| 46 | Sensitivity price, N = 100 (MT, Fig 3B) | 0.46 → 0.21–0.23; training FPR 29% | v4/results/deploy_v4_cc_summary.csv | SRC sens 0.464, FPR 0.288; BURN π 1–10%: 0.206–0.227 | yes |
| 47 | P(FPR > 0.15) at N = 100, no patients (MT, Fig S1A) | 0.055 | Beta(10, 91) tail, recomputed | 0.0551 | yes |
| 48 | Binomial check power at n = 100, FPR > 0.25 (SI, Fig S1B) | 98% (LASSO) | v5/results/verify_power_v5.json | consistent with plotted 0.98 | yes |
| 49 | Duplicates removed (MT Methods) | 119 | v4/results/counts_v4.json | 119 | yes |

Result: 48 of 49 checks match the result files to the stated rounding. One statement is wrong (row 20; see R1 below). I also checked Figure 1B row order against τ (correct, ascending), the Figure 1C arrow for IGT RF (lower PI limit 0.0003, correct), and the four "East Asian" unseen populations, including YassourM_2016, which curatedMetagenomicData codes as KOR adult healthy (36 samples in metadata, 20 after filters).

## 3. Statistical review: overclaiming, post hoc labelling, sidedness, plan deviations

### 3.1 Overclaiming

- **RF variance split misstated (factual).** MT: "the classifier–population pair explained most of the rest (S2.1)". This holds for LASSO (pair 48% of the 83% not due to population). It is false for RF, where the classifier explains 46% and the pair only 25% (h2_sampling_v13.json; SI S2.1 says so correctly). The sentence reads as if it covers both models.
- **Title extreme.** "0–87%" is the range over 28 classifiers, and the top end is one RF heart-failure model (trained on one cohort) in one population of 110 people (LiuW_2016, Mongolia). The range is correct and the restriction to n ≥ 100 is stated in the text. But a range is the least robust summary, and the robust one (26% of LASSO pairs above 0.25, with 2.5 times the target) is already in the text. Acceptable for a Letter title. I recommend adding the robust number to the graphical-abstract summary.
- **"this is the FPR the index should deliver elsewhere" (GMWI2).** The developers published a cut-off of 0, not a target FPR. Using the training share (20.8%) as α is a sensible reference choice, and it was pre-specified (plan v6). But "should deliver" attributes a claim to the developers that they did not make. Reword it as the training-implied FPR.
- **Section heading 2.** "Two published gut-health indices label healthy East Asian cohorts as non-healthy." The evidence for both indices comes from their own training data. For unseen data it rests on GMWI2 only, with 4 East Asian populations (one of n = 20), post hoc, one-sided P = 0.020 (full set 0.065). The text is careful. The heading would be accurate with "in their own training data".
- **Mechanism.** "For GMWI2, retraining linked this to the geographic make-up of its training data." This is acceptable as worded ("linked", "A likely cause"). The text discloses the wide CI (41–149%), the failed cost criterion (B3), and that within-country balancing alone gave a 37% reduction with a CI including zero. Figure 2D shows "0.52 → 0.06" without the CI. Add the CI to the panel or legend.
- **Profiler dependence.** "A released cut-off also depends on the profiling pipeline." This is shown for one index (GMHI), post hoc, and it is partly a species-naming issue (4 of 7 health-prevalent species absent under MetaPhlAn3 names). It is labelled post hoc in MT and HL. Acceptable. "Can depend" would be more exact.
- **Binomial check power ("detects most ... pairs whose FPR exceeds 0.25").** Power is computed with the observed atlas FPR taken as the true FPR (Table S7 says so). Observed extremes are biased away from the centre, so this is mildly optimistic. It is labelled post hoc. Recommend also giving power at fixed true FPRs (0.20, 0.25, 0.30), which needs no atlas data.
- The burn-in claim is well bounded: retrospective, within-site only, fails across sites, costs sensitivity. Good.

### 3.2 Post hoc labelling

Post hoc labels are present for: the strict-set definition (disclosed in MT and in plan v4 P1), the GMWI2 training-data East Asian comparison, the unseen East Asian comparison, the taxon decomposition, within-country balancing, the six unshared GMHI studies, the GMHI profiler shift, the decision not to interpret GMHI H3–H6, the binomial check, the burn-in CI, the v6c plan (treated as post hoc because it was committed with its results). This is thorough.

Two small gaps:
- The ρ CI uses a Fisher-z interval, which is approximate for a rank correlation; the SI says so, the MT does not. Fine for a Letter.
- MT: "Five taxa explained 39% ... (post hoc)". The result file also holds a different share (34.5% of the negative contributions). Say in the SI which denominator is used (the total score gap).

### 3.3 Test sidedness

Stated in MT: Spearman (two-sided), GMWI2 training EA (two-sided), unseen EA (one-sided, with reason), GMHI H2 and the unshared-studies test (one-sided). Good.

Not stated:
- G2 exact Poisson-binomial test (MT "Holm-adjusted P = 2 × 10⁻¹²"): one-sided (excess over expectation) by construction; say so.
- H5 replication sign test (SI S3, "P = 0.090", "P = 0.029"): one-sided in plan v5 Addendum A; the SI does not say so.
- SI S2 "Wilcoxon tests on population means" and the H4 Wilcoxon (P = 7.5e-9 in numbers_v11.json): sidedness not stated.
- GMWI2 G4 bootstrap P (SI "< 0.0004"): one-sided proportion of draws ≤ 0; state it.

### 3.4 Deviations from the pre-specified plans

Checked against v4/protocol_v4.md, v5/protocol_v5.md, v6/protocol_v6.md, protocol_v6b.md, protocol_v6c.md, v7/protocol_v7_gmhi.md.

Disclosed and handled well: strict set chosen after v3 results; v4 D1–D4; v5 H2 graded on the plan's own definition, with the net-of-noise share shown as a secondary measure; v6b B2 met on the point estimate only, with the corrected CI shown; two bootstrap bugs corrected with original files kept; v6c implementation deviation; GMHI Q2 matching error found after results, with the not-interpreted decision stated as made after seeing results; Mongolia sensitivity.

Not disclosed as deviations:
- **H4 population threshold.** Plan v5 H4 says "as v4 P4". Plan v4 P4(a) required n ≥ 150 for covariate-half splits and gave no threshold for accession order. The code (v5/analyse_v5.py, line 54) uses n ≥ 120 for all designs, giving 13 populations. SI S2.1 states "≥ 120 people" as a fact but does not call it a choice not in the plan. The same n ≥ 120 is pre-specified in plan v6 G4, so it may have been carried over. It is minor and unlikely to change the 28/28 result, but it must be listed in S5 as an implementation choice. A rerun at n ≥ 150 for the covariate splits would close it.
- **Sex splits.** v4 P4(a) included women → men and men → women. The v5 H4 run used accession order, age and BMI only. SI S2.1 says so, but not as a deviation. Add it to S5.
- **Holm family in v6.** Plan v6 says Holm over "G1–G4 P values where a P value exists". G1 has a Q-test P but was left out of the Holm family. Harmless (it is tiny), but say so.
- **GMHI Holm family.** H2's Holm-adjusted P is computed together with H4–H6, which are now "not interpreted". The adjustment is still correct (H2 has the largest P), but a sentence should say the family was kept as planned.

### 3.5 Other statistical points

- The GMWI2 unseen East Asian contrast (P = 0.020) rests on 4 populations, one with n = 20; the full-set P is 0.065. The text already reports both; keep it that way and do not promote it in the abstract.
- Study-level Mann–Whitney tests treat studies as equal units regardless of size. This is reasonable for "a site's FPR" and is consistent across analyses.
- The burn-in comparison is within population; the non-random splits are the right stress test, and the across-site failure is reported. Good design.
- The pre-specified plans are internal git commits, not an external registration. Plan v4 says so. The MT says "time-stamped plans ... committed to the code repository before they were run". Reviewers can only check this once the repository and its history are public.
- The protocol files v6 and v7 state their motivation as raising internal scorecard or editor-check scores ("novelty escalation", "Blind scorecard r9", "Final editor check r14 (75/100)"). The plans themselves are sound and should not be edited (that would break the time stamps). But a reviewer who opens them will read them as score-driven analysis choices, which raises a forking-paths concern. The authors should add a short note to S5 explaining these internal review rounds, and say so in the AI-use statement if they were AI-assisted.

## 4. Figures and package (each image viewed)

- **Figure 1.** Strong. A map, a heatmap ordered by τ, prediction intervals and AUROC vs τ tell the atlas in one figure. Row order matches τ. The heatmap labels (country·first author) are small at print size; check legibility at iMeta column width.
- **Figure 2.** Clear four-step story (training data, unseen data, taxa, retraining). Panel D shows "0.52 → 0.06" without the CI 41–149%; add it.
- **Figure 3.** Panel A is clear (28/28). Panel B shows the sensitivity price honestly.
- **Figure S1, S2.** Clear. S2B annotates the pooled 23% → 43% on 2,190 samples while showing 12 studies; the legend explains this.
- **Graphical abstract.** Three panels, readable. Panel 1 shows LASSO only (max 0.77), while the summary paragraph and title say 0–87% (which includes RF). Not wrong, but a reader comparing them will notice; add "LASSO" to the panel label or use 28 classifiers. The file is named graphical_abstract_v18 while the README says v19; rename it.
- **Package.** REPRODUCE.md is headed "manuscript (v16)"; update it to v19. The repository root holds internal working files (prompts, directives, state, journal folders). The authors should decide what goes into the public release.

## 5. Clarity of the Letter (judged on its own)

The problem is stated in one paragraph, and the headline number sticks. Headings are finding sentences. The Letter is about 2,000 words with three main figures, which suits iMeta.

Weaknesses: the text is dense with numbers, CIs and labels ("pre-specified", "post hoc", "falsified") in almost every sentence. The second section packs GMWI2 training data, unseen data and a full GMHI audit, including the Q2 failure story, into one section. A general reader will find the GMHI paragraph hard. Moving the Q2 detail to the SI and keeping one sentence in the main text would help. Some sentences are long ("Not every pre-specified hypothesis held: ...").

Clarity score: 7. It is a good Letter but not yet at the top of the benchmark for plain language.

## 6. Scores (1–10 by the scorecard anchors; P75 from benchmark_v2)

| # | Dimension | Score | P75 | Reason |
|---|---|---|---|---|
| 1 | Biological / clinical significance | 8 | 8.0 | Changes what benchmarks and sites should report and check for many microbiome tests; two released indices audited; still retrospective and research-grade. |
| 2 | Scale and breadth | 8 | 8.0 | 36 (55) populations, 6,525 (8,160) people, 20 countries, 28 classifiers, plus 8,069 GMWI2 and 10,986 retraining samples; one data source. |
| 3 | Novelty vs prior art | 7 | 7.0 | The spectrum effect and the burn-in rule are known; the cross-disease FPR map and the audit of released indices are new. |
| 4 | Methodological rigour and statistics | 8 | 7.25 | Plans, falsifiers, failed hypotheses reported, CIs, Holm, full-set sensitivity, corrected bootstraps; held back by internal (not external) plans, key contrasts post hoc, and the small issues in 3.3–3.4. |
| 5 | External validation | 8 | 7.0 | Every classifier tested in held-out populations, leave-one-study-out retraining, cross-site failure reported and explained. |
| 6 | Resource / tool value | 7 | 5.75 | fprcal with 5 commands, 14 shipped models, atlas table, 19 passing tests; no PyPI or web server yet. |
| 7 | Figure quality and visual story | 7 | 7.0 | Figure 1 tells the study at a glance; Figure 2 is a clean sequence; small labels and missing CI in 2D. |
| 8 | Clarity, framing and writing | 7 | 7.25 | Clear problem and number that sticks; dense, label-heavy prose and an overloaded GMHI paragraph. |
| 9 | Reproducibility and openness | 8 | 7.25 | In the repository: full code, pinned environment, REPRODUCE.md, seeds, source data, metadata hash, result files. Not yet public (placeholder URL/DOI). Once public with a Zenodo DOI: 9. |
| 10 | Actionable insight | 8 | 7.0 | A concrete, tested fix with a hold-out (non-random split) evaluation, its cost and its failure mode; retrospective only. |
| | **Total** | **76** | **69.25** | At or above P75 on 9 of 10 dimensions; Clarity 0.25 below. |

## 7. Editor's decision

**Decision: suitable for external review after a short pre-submission revision (minor).** I would send it out for review. None of the issues changes a main result. The REQUIRED items below are about accuracy and disclosure, and reviewers would raise them.

### REQUIRED changes (authors can make these now)

- **R1. Fix the RF variance statement.** MT, first section: restrict "the classifier–population pair explained most of the rest" to LASSO, and add that for RF the classifier explained most (46%; pair 25%).
- **R2. List the H4 implementation choices as deviations in S5.** These are the n ≥ 120 population threshold (plan v4 P4(a): n ≥ 150 for covariate halves) and dropping the sex splits. Optionally report H4 at n ≥ 150 for the covariate splits.
- **R3. State the sidedness of every test that lacks it.** These are G2 (exact Poisson-binomial, one-sided), the H5 sign tests (one-sided), the H4 Wilcoxon and the "Wilcoxon tests on population means" in S2, and the G4 bootstrap P.
- **R4. Reword the GMWI2 α sentence.** Replace "this is the FPR the index should deliver elsewhere" with wording such as "we use this training-implied FPR (α) as the reference".
- **R5. Show the uncertainty of the retraining result in Figure 2D.** Add the 88% reduction with its corrected CI (41–149%), or "point estimate" to the panel or legend.
- **R6. Fix version mismatches.** Rename graphical_abstract_v18 to match the package (or fix the README), update the REPRODUCE.md header from v16 to v19, and label GA panel 1 as LASSO (or use all 28 classifiers) so it matches the 0–87% in the summary.
- **R7. Explain the plan motivations.** Add one sentence to S5 explaining that some plan files (v6, v7) cite internal review rounds as their motivation. Do not edit the plans.

### Recommended changes

- Make heading 2 exact: "... in their own training data".
- Add the robust atlas number (26% of LASSO pairs above 0.25) to the graphical-abstract summary next to 0–87%.
- Shorten the GMHI paragraph: keep the H2 result, the overlap caveat and the profiler shift in one or two sentences, and move the Q2 matching story to S7.
- Note in the SI which denominator the 39% taxon share uses.
- Give binomial-check power at fixed true FPRs (0.20, 0.25, 0.30), not only at observed atlas FPRs.
- Say in the GMHI section that the Holm family was kept as planned, including the uninterpreted H4–H6.
- Say that G1's P was not included in the v6 Holm family.
- Change "A released cut-off also depends on the profiling pipeline" to "can depend".
- Check that Figure 1B labels are readable at print width.

### Author-only items (I cannot judge or fix these)

- Author list, affiliations, contributions, conflicts, funding, acknowledgments, suggested reviewers.
- AI-use statement (Wiley policy), consistent with the internal review rounds named in the plan files.
- Make the repository public, archive it on Zenodo, tag the fprcal release, and insert the URL and DOI in the Data Availability statement and cover letter. Decide which internal working files at the repository root are released.
- Send the GMWI2 and GMHI audits to their developers and state this in the cover letter.
- Check current iMeta Letter limits (words, figures, highlights, graphical abstract).
- Check Poyet et al. (Cell 2026) for GMHI results and cite them if relevant.

## 8. Estimated acceptance probability

**About 45% at iMeta (range 35–55%), assuming R1–R7 are done and the repository is public at submission.**

Reasoning:
- For: the scorecard total (76) is well above the benchmark P75 (69.25) and near the best benchmark paper (78). The topic (calibration of microbiome tests across populations) fits iMeta. The numbers trace to result files. Failed hypotheses are reported. A working tool is released.
- Against: the main ideas (spectrum effect, order-statistic recalibration) are known in other fields, so a reviewer may call the atlas expected. The strongest cross-index finding rests on largely shared training data. The unseen East Asian result is post hoc and fragile. The burn-in is retrospective only. The plans are internal, not externally registered. Letters with dense statistics risk a "too technical for a Letter" or "send as a full article" response.
- If the repository stays private or the developers are not given a right of reply, I would lower this to about 30%.
