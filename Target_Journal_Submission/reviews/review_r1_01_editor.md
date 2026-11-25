# Handling editor triage: iMeta Letter / Short Communication

**Manuscript:** "Stool-metagenome classifiers miss their intended false-positive rate in new laboratories, and a label-free rank rule fixes it" (draft v0.2, 2026-11-25)
**Files read:** `manuscript/manuscript.md`, `manuscript/supporting_information.md`, `figures/Figure1.png`, `figures/Figure2.png`, `journal_selection/{selected_journal.md, style_notes.md, journal_level_profile.md, journal_benchmark.csv}`. I also checked the numbers against `results/main_tables.md`, `results/table_s1_cohorts.csv` and `code/experiments/novelty_escalation_log.md`.
**Reviewer role:** handling editor (desk triage), date 2026-11-25.

---

## 1. Summary

The authors re-analyse 19 public curatedMetagenomicData studies: 24 cohort-task pairs across CRC, IBD, T2D and adenoma, with 3,626 unique stool metagenomes. Their claims are:

1. A classifier's 90%-specificity cut-off, set on training cohorts, gives realised FPRs of 0.00 to 0.74 at 16 locked external cohorts, even when the AUROC looks acceptable.
2. Five label-free adaptation methods (label-shift EM, MLLS-BCTS, unsupervised two-Gaussian calibration, a location-scale mixture and per-site feature standardisation) do not repair this when cases are rare. Four of the five do worse than doing nothing.
3. An order-statistic "rank rule" sets the cut-off at the r-th highest score in the laboratory's own unlabelled pool. It brings the cohort-RMSE of the FPR down from 0.185 to 0.031 at a 1% case share, close to the result from 10 labelled local controls (0.027). It also comes with a sample-size rule: about 360 to 1,500 samples, depending on the maximum case share.

The practical message is useful and fits iMeta: "the cut-off belongs to the laboratory", and reports should give the realised FPR at each external cohort. The analysis is pre-registered in spirit (protocol committed before the locked cohorts were scored), it compares many baselines, and its statistics are better than the benchmark median.

The draft is **not ready for submission**:

- The main text (about 1,260 words) is **below the 1,500-word minimum** for Short Communications.
- There are **no figure legends**.
- The graphical abstract, keywords and a compliant running title are missing.
- The **headline method is barely distinguishable from a trivial baseline that the main text never mentions**: the plain local quantile, `local_q`, has a cohort-RMSE of 0.046 against 0.031 for the rank rule.
- The "guarantee" and "fixes it" language goes beyond what was evaluated.

## 2. Decision

**Send to review with revisions. The REQUIRED items below must be addressed before the manuscript goes to external reviewers.**

**Candid desk-rejection risk: moderate to high (about 40-50% as currently written).** The reasons, in order:

1. **Novelty of the method.** The rule is a classical Wilks (1941) tolerance limit, also known as split-conformal quantile, applied to an unlabelled pool. An editor or statistical reviewer will ask what is new beyond "use a local quantile", and the authors' own Table S2 shows the naive local quantile already does most of the work (0.046 vs 0.185 for the training cut-off). The contribution is better framed as an **empirical finding plus a deployment recommendation**, not as a new method that "fixes" the problem.
2. **Purely computational re-analysis of public data.** iMeta Letters in the benchmark that lack wet-lab or deployment evidence usually offer a tool, a platform or a large new dataset. This submission has none of these unless the code is released as a usable tool.
3. **Evaluation realism.** Within-cohort random splits make the pool and the future samples exchangeable *by design*, which is the assumption the guarantee rests on. Most pools are tiny: half of 12 to 65 controls in 13 of the 16 locked cohorts. That is far below the 360 to 1,500 samples the authors themselves say a laboratory needs.

If the authors reframe the paper and fix the items below, the work would be competitive with the Letters in the benchmark set.

## 3. Assessment by criterion

### 3.1 Scope and audience fit
- **Good.** Microbiome diagnostics, machine learning across cohorts and data-science practice are all core iMeta topics. Examples in the benchmark are the periodontitis signature paper, "A decade-scale audit of microbiome AI-readiness" and RepliChrom.
- The topic is relevant to the wider readership (anyone publishing a microbiome classifier) and not only to methodologists. That is the paper's strongest selling point and should come first.

### 3.2 Is the significance clear in the title, first paragraph and conclusion?
- **Title:** it is clear but overclaims ("fixes it"). It is 23 words long, against 8-15 in the authors' own style notes. It also does not say that the rule is evaluated on retrospective case-control data.
- **First paragraph:** the problem is clear and well motivated (cut-off vs AUROC, local updating in clinical prediction). "Nobody has checked whether the promise holds…" is an unsupported absolute claim; ref. 9 (CRC-TrustBench) and ref. 18 (sepsis transcriptomics) partly do. Line 18 contains the phrase "the promise" before the reader has been told what promise is meant.
- **"Here, we" paragraph:** it states the headline numbers well. "A simple rule fixes it", "comes with a finite-sample guarantee" and "tells a laboratory how many samples it must collect" all need qualifying (see §3.5).
- **Conclusion:** the recommendation (report the realised FPR per external cohort; include a local calibration run) is clear and actionable. The limitations are honest but squeezed into a few clauses. The code URL is a placeholder.

### 3.3 Letter-format compliance
Format check against the iMeta guidelines, using the journal's guidelines page at journal.hep.com.cn/imeta/EN/guidelines (see §6 for what I could and could not verify):

| Item | Requirement (verified / unverified) | Manuscript status |
|---|---|---|
| Article type | "Short Communication": 1,500-3,000 words, 1-3 figures (verified) | Correct type, but the header calls it a Letter. Submit as Short Communication. |
| Main-text length | ≥1,500 words (verified); benchmark Letters 1,907-2,503 | **About 1,260 words** (title to end of Conclusion). **Below the minimum.** The draft header's "target ~2,100" is not met. |
| Figures | 1-3 (verified) | 2 multi-panel figures. Compliant. |
| Figure legends | Required by Wiley (standard) | **Missing entirely.** There is no legends section, and panel titles do not replace legends. |
| Abstract | Guidelines table lists "Abstract: Yes, Structured" for Short Communication (verified on the HEP-hosted page) | **No abstract.** Published iMeta Letters in the benchmark have no abstract, so the page and practice disagree. **Ask the editorial office**, or supply a structured abstract and let the office remove it. |
| Graphical abstract / TOC | ≤80 words or 3 sentences, image 50 × 60 mm (verified on the HEP page) | **Missing.** The Data Availability statement claims a graphical abstract is in the SI, but none exists. The style notes say "~100 words", which exceeds the 80-word limit. |
| Highlights | Not mentioned for Short Communication (verified absence on the HEP page); the authors' notes say highlights are for Research Articles only | Optional "Practitioner Points" (≤3) are allowed. Recommended: see Suggested item S7. |
| Running title | <40 characters (verified) | "Setting the decision threshold of microbiome tests at a new site" is **64 characters**. Non-compliant. |
| Keywords | Up to 7 (verified, general requirement) | **Missing.** |
| Title page | Required: authors, affiliations, corresponding author, ORCID | **Missing.** |
| Author contributions | CRediT format (verified) | Placeholder. |
| Funding statement | Required in Acknowledgments (verified) | **Missing.** |
| Data and code availability | "Data and code availability" section (verified as a main-text section) | Present, but the code URL is "[[GitHub URL]]" and there is no DOI or archive. |
| AI-use statement | Listed in the authors' style notes as used in 2026 (unverified) | Missing. |
| References | No cap stated; Chicago style, or any consistent style under free-format submission (verified); about 20 in benchmark Letters | 20 references. Compliant. Format is acceptable under free format. |
| Supporting Information | Unlimited | Present. It lacks SI figure legends and Table S1 as an actual table (it only points to a CSV). |

### 3.4 Clarity for a broad microbiome readership
- The prose is plain, short and active, which is good. Some passages are too compressed for non-statisticians. Examples are "binomial test of overdispersion" and "cohort-RMSE", which is defined only in the SI and only as the RMSE of the *mean* FPR over 200 splits. Others are "pi_max" and "delta" written in ASCII, and "order statistics".
- "Cut-off", "threshold" and "rank rule" are used interchangeably with "expected-FPR rule" and "stricter version". The SI codes (`rpoolmean`, `rpool`, `shift2`, `gauss2`, `local_q`) leak into the tables. One naming scheme should be used throughout.
- The mixture method is called "our own location-scale mixture fit" in the text, "Unlabelled mixture fit" in Figure 2A and "Mixture fit" in Figure 2B. Readers cannot tell it apart from the two-Gaussian calibration.

### 3.5 Do the claims match the results?
I checked the main numbers against `results/main_tables.md`. Most numbers match: 0.185, 0.031, 0.027, −0.108 [−0.160, −0.065], P = 0.048, 199/87 per 1,000, the overdispersion P values, the FPR ranges and the sample sizes 360/610/1,500. The substantive mismatches are:

1. **The naive local quantile is left out of the main text.** `local_q` reaches cohort-RMSE 0.046 at π = 1%, against 0.185 for the training cut-off. The rank rule's improvement over it is only 0.017 (95% CI −0.026 to −0.010). The main point, "set the cut-off locally", is carried almost entirely by `local_q`. The rank rule's contribution is the small correction for contaminating cases plus the formal bound. The main text and Figure 2 must show `local_q`.
2. **"Fixes it" and "keeps the promise".** The rank rule is *conservative*: mean FPR is 0.082 against a target of 0.10, and 0.049 at a 20% case share. It costs sensitivity: CRC 0.48 vs 0.65, and 0.25 vs 0.39 overall. At α = 0.05 it abstains in 31% of units. The high-probability ("guaranteed") version abstains in **50% of units at α = 0.10 and 75% at α = 0.05**, with sensitivity 0.076. The "guarantee" therefore holds mostly by refusing to give a cut-off. The main text should say so.
3. **The metric hides per-deployment variability.** The cohort-RMSE is computed on the *mean* FPR over 200 splits, which is the expected FPR. That is exactly what the expected-FPR rule is built to control. A real laboratory gets one realisation. Table S2 shows that for 14% of deployments the realised FPR exceeds 15% (`p_fpr_over_a_plus_5` = 0.142), against 19.9% for 10 labelled controls and 39% for the training cut-off. This per-deployment exceedance belongs in the main text.
4. **Pool sizes do not match the recommendation.** The pools are half the controls of each cohort. In 13 of the 16 locked cohorts that means about 6 to 30 controls (e.g. HallAB_2017 has 12 controls, giving 6 in the pool). Yet the text recommends "a few hundred" samples. The evaluation does not test the regime the paper recommends, and with n0 ≈ 20, r = 2 means the cut-off is the second-highest score.
5. **"The AUROC stays acceptable".** Figure 1B shows AUROCs of about 0.55 to 0.65 for many locked cohorts, which is not acceptable for screening. Rephrase this, and report the AUROC range.
6. **The "guarantee" holds only under exchangeability, which the design ensures by construction.** The limitation is stated in the Conclusion, but the claim in the "Here, we" paragraph and the Conclusion ("restores … with a guarantee") is unqualified.
7. **Some "locked" results are not fully independent.** Four of the five adenoma test cohorts reuse controls from the CRC development cohorts. That is disclosed in the SI but not in the main text. Because FPR depends *only* on controls, the adenoma FPR results are not independent external tests. Either drop them from the locked FPR claims or flag them clearly.
8. **Development-cohort results are presented next to locked results.** The values 0.092 and RMSE 0.125 (random forest) and the cross-study 0.33 and 0.87 (Figure 1C) come from the development exploration log, not from the locked run. Label them as development results wherever they appear. Figure 1C says "(dev)" but the text does not.
9. **"Two US studies" (0.87)** is HanniganGD_2017 → VogtmannE_2016. Hannigan is recorded as Canada and USA (Table S1). Rephrase as "two North American studies", or choose a cleaner pair.
10. **"Most make it worse".** At π = 1%, four of the five methods are worse than the training cut-off, while the authors' own mixture fit (0.15) is better. This is acceptable but should be said precisely.
11. **"Comes close to ten labelled local controls … without any diagnoses".** Ten labelled controls is still significantly better (P = 0.048), and only ten negatives are needed, which in CRC screening means ten FIT-negative or colonoscopy-negative people. The paper needs to explain why a laboratory could not simply obtain ten verified controls.

### 3.6 Level compared with the benchmark set
- **Strengths compared with the benchmark Letters** (`journal_level_profile.md`): more cohorts (24 pairs vs a median of 3 for Letters), more baselines (9 vs about 0), locked test cohorts, paired CIs with Holm correction, and per-1,000 deployment consequences. On rigour the manuscript is in the top quartile.
- **Weaknesses compared with the benchmark Letters:** every benchmark Letter except two delivers either a tool or platform (PSOSP, QSCNAS, scRiskCell, FluNexus, Majorbio), new data (vaginal-microbiota survey, spaceflight), or wet-lab or causal validation. This manuscript has none of these. The method is a few lines of code. To match the benchmark it should at least be released as a small, citable package or function with a worked example.
- **Format** is below the benchmark: about 1,260 words against 1,907-2,503, with no legends and no graphical abstract.

### 3.7 Figures
- **Figure 1:** there is no workflow or schematic panel, although the authors' style notes say iMeta Letters typically have one. In 1A the legend overlaps the data points and the "target 10%" label collides with the x-axis. 1B has no labels identifying which cohorts are the extreme ones. 1C shows development results without saying so in the panel title or a legend.
- **Figure 2:** 2A omits MLLS and two-Gaussian calibration (both quoted in the text) and the naive local quantile. Its y-axis does not start at 0, and the "10 labelled local controls" line is hidden under the rank-rule line. 2B mixes methods (it shows EM but not MLLS) and gives no uncertainty. 2C has a categorical x-axis with uneven spacing (0, 1, 2, 5, 10%) drawn as if it were linear.
- Both figures are PNG. iMeta asks for vector figures (verified only in the authors' notes).

---

## 4. REQUIRED changes (before external review)

1. **Bring the main text to 1,500-3,000 words.** Target about 2,000-2,300 to match the benchmark Letters (currently about 1,260). Spend the extra words on items 6 to 10, not on padding.
2. **Add a "FIGURE LEGENDS" section** after the References, with a full legend for Figure 1 (A-C) and Figure 2 (A-C). Each legend needs: a one-sentence title; what each point, bar or line is; n (cohorts, models, splits = 200); target α; case share π; the error measure; abbreviations (FPR, AUROC, RMSE, LASSO, RF, EM); and, for 1C, that these are **development** cohorts. Add legends for any SI figures.
3. **Create the graphical abstract.** It needs an image of 50 × 60 mm and a summary of **≤80 words or 3 sentences**, not the ~100 words in the style notes. Either supply it, or delete the claim in the Data Availability statement that it is in the SI.
4. **Running title of fewer than 40 characters**, e.g. "Local cut-offs for microbiome tests" (35 characters).
5. **Resolve the abstract requirement.** The guidelines table lists a structured abstract for Short Communications, but published iMeta Letters have none. Confirm with the editorial office, or prepare a structured abstract of about 150 words (Background / Results / Conclusion) ready to include.
6. **Add `local_q` (plain local quantile) to the main text and to Figure 2A/2B.** State plainly that most of the gain comes from setting the cut-off locally (0.185 → 0.046), and that the rank rule adds robustness to contaminating cases plus a formal bound (0.046 → 0.031; difference −0.017, 95% CI −0.026 to −0.010). Reframe the contribution accordingly.
7. **Report per-deployment reliability, not only the expected FPR.** In the main text give the share of splits with a realised FPR above α + 0.05 for the rank rule (0.14), 10 labelled controls (0.20) and the training cut-off (0.39). Also give the spread of realised FPR per split, for example as an IQR or a violin plot in Figure 2A or an SI figure.
8. **Report abstention and sensitivity honestly in the main text.** Give the high-probability version's abstention rates (50% at α = 0.10, 75% at α = 0.05) and sensitivity (0.08), and the expected-FPR version's 31% abstention at α = 0.05. Qualify "with a guarantee" everywhere: the guarantee is in expectation for the primary rule, and it holds only under exchangeability.
9. **Address the gap between pool sizes and the recommendation.** State the actual pool sizes, for example the median and range of n per cohort. Add an analysis, at least in the SI, of whether the rule's error shrinks as the pool approaches the recommended 360-1,500. The two large cohorts (YachidaS_2019 with 251 controls and MetaCardis_2020_a with 642) allow a partial check. Alternatively, simulate a larger pool by resampling.
10. **Strengthen or explicitly bound the exchangeability limitation.** Within-cohort splits guarantee exchangeability. Either add a test that breaks it, such as pooling on one sub-study or time block and evaluating on another where metadata allow (MetaCardis centres, YachidaS batches, longitudinal HMP visits), or move this limitation up into the "Here, we" paragraph and the Conclusion as a central caveat, not a closing clause.
11. **Tone down the overclaims.**
    - Title: drop "fixes it". For example: "Stool-metagenome classifiers miss their intended false-positive rate at new sites; a label-free local rank rule restores it" (but see item 6). Keep it to about 15-20 words.
    - Line 18, "Nobody has checked": change to "No study has systematically evaluated…" and acknowledge refs 9 and 18.
    - Line 24, "the AUROC stays acceptable": give the AUROC range instead, since some values are about 0.55.
    - Lines 90-93, "restores the intended false-positive rate with a guarantee": qualify as above.
12. **Label development-cohort results as such** in the text (0.092 and 0.125 in lines 39-40; 0.33 and 0.87 in lines 42-44) and in the Figure 1C title or legend. Correct "two US studies" (HanniganGD_2017 is Canada and USA).
13. **Flag in the main text that four of the five adenoma test cohorts share controls with the development cohorts.** Since FPR depends only on controls, either exclude those cohorts from the locked FPR claims or give results with and without them (a sensitivity analysis in Table S2).
14. **Justify the "label-free" premise against the 10-labelled-control baseline.** The baseline is better (P = 0.048) and needs only ten verified negatives. Explain why such negatives are unavailable or costly in practice (e.g. a confirmed negative requires a colonoscopy), or reposition the rank rule as the option for when even ten verified controls are infeasible.
15. **Complete all back matter.**
    - Title page: authors, affiliations, corresponding author, ORCID.
    - CRediT author contributions.
    - Funding statement (in Acknowledgments).
    - Keywords (≤7).
    - AI-use statement if applicable.
    - A real GitHub URL **plus an archived DOI** (Zenodo) in Data and Code Availability, with the exact curatedMetagenomicData package version.
16. **Fix the figures.**
    - Supply them as vector files (PDF/EPS/SVG).
    - Fig 1A: move the legend off the data and fix the "target 10%" label collision.
    - Fig 2A: start the y-axis at 0, make the labelled-controls and rank-rule lines distinguishable, and add `local_q`, MLLS and two-Gaussian calibration (or say in the legend why they are omitted).
    - Fig 2B: add MLLS and `local_q`, and add bootstrap intervals.
    - Fig 2C: use a numeric x-axis or label it clearly as categorical.
    - Use the same method names in the figures, text and SI.
17. **Make the SI self-contained.** Give Table S1 as an actual table, not a pointer to a CSV. Replace internal method codes (`rpoolmean`, `shift2` etc.) with the names used in the main text. Define cohort-RMSE in the main text the first time it appears.
18. **Verify references 9, 10 and 18 (all 2026).** Confirm that the DOIs resolve and that the cited content supports the text, especially the claim that ref. 18 "rescues fixed cut-offs in transcriptomics". Reviewers will check them.

## 5. SUGGESTED changes

1. **Add a schematic panel**, Figure 1A or a new 2A: training cohorts → cut-off → new lab → unlabelled pool → r-th highest score. It doubles as the graphical abstract and fits the house style.
2. **Release the rule as a small tool**: an R or Python function or a SIAMCAT-compatible helper that takes pool scores, α, π_max and δ and returns a cut-off or "abstain" together with the required n. This answers the "tool or platform" expectation in the benchmark Letters and raises citation potential.
3. **Lead with the reporting recommendation.** Make "report the realised FPR at each external cohort" a headline finding, perhaps in an ALL-CAPS heading. For the broad readership it is the most citable message, and it does not depend on the novelty of the method.
4. **Show worked numbers for a real screening scenario**, for example FIT-positive triage, where the case share is higher. This gives the π_max choice practical meaning. State why π_max = 0.05 was chosen for the primary analysis while the evaluation headlines π = 1%.
5. **Report sensitivity at matched realised FPR** (or partial AUROC), so readers can see that the loss in sensitivity comes from the threshold and not from the model.
6. **Discuss the sensitivity-target extension briefly** (the final limitation sentence), or drop it. As written it is an unsupported aside.
7. **Optional "Practitioner Points"** (≤3, allowed by the guidelines). For example: (i) report the realised FPR per external cohort; (ii) recalibrate the cut-off on ≥360 local screening samples; (iii) do not rely on label-shift or feature-standardisation fixes at low prevalence.
8. **Explain overdispersion in one plain sentence** ("more variable across cohorts than sampling error alone would produce") and drop the extreme P values (2 × 10⁻⁵², 5 × 10⁻⁸⁸) to the SI. Use proper symbols (π_max, δ, α) instead of ASCII.
9. **Shorten the title to about 15 words**, in line with the house style (8-15 words) and the benchmark.
10. **Add a sentence on how the rule interacts with temporal drift** (repeat calibration at intervals, or after a change in kit or sequencer), and link it to post-market monitoring in clinical laboratories.

## 6. What I could and could not verify about iMeta guidelines

- **Verified** from the iMeta guidelines page at journal.hep.com.cn/imeta/EN/guidelines, retrieved 2026-11-25:
  - Short Communication: 1,500-3,000 words and 1-3 figures.
  - Abstract listed as "Yes, Structured".
  - Running title under 40 characters.
  - Graphical abstract/TOC: no more than 80 words or 3 sentences, 50 × 60 mm.
  - Up to 7 keywords.
  - CRediT author contributions and a funding statement in the Acknowledgments.
  - Main-text sections include "data and code availability".
  - No reference cap; Chicago style, or any consistent style under free format.
  - "Practitioner Points" optional (≤3).
  - Highlights not mentioned.
  - "Letter" is not a separate submission category; the closest is Short Communication.
- **Could not verify:** the Wiley-hosted page (onlinelibrary.wiley.com/page/journal/2770596x/homepage/forauthors.html) returned **HTTP 403** to both curl and the fetch tool, so I could not check whether it differs from the HEP-hosted page. I also could not verify:
  - the vector-figure requirement (taken from the authors' notes);
  - whether published Letters really omit the abstract (taken from the authors' benchmark, not checked);
  - whether an AI-use statement is mandatory;
  - the JIF and quartile (authors' notes, unverified);
  - the APC.
  The authors should confirm these with the editorial office before submission.
