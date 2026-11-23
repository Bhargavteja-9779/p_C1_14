# Handling-editor desk screen — iMeta Short Communication (Letter)

**Manuscript:** "Twenty local controls keep gut-microbiome diagnostic thresholds honest at new sites"
**Screened:** manuscript.md, supporting_information.md, si_tables.md, Figures 1–3 and S1 (PNG). Spot-checked against `code/experiments/final/endpoints.txt` and `results_locked.md`.
**Date:** 2026-11-23

---

## 1. Desk decision

**Decision: SEND TO REVIEW, but only just.** In its current form I estimate **P(sent out) ≈ 0.55** and **P(eventual acceptance) ≈ 0.30**. If items 1–5 in Section 5 are fixed before submission, these rise to about 0.75 and 0.50.

**Separate technical issue (this is not a desk rejection, but it does block submission):** Authors, Author Contributions, Conflict of Interest, the AI-use statement and the GitHub URL are all still placeholders. There is also no graphical-abstract image. The editorial office would return the file unsubmitted before any editor reads it.

**The three reasons behind the decision**

1. **For sending out: the drift result is real, useful and new for this field.** The paper shows that a cut-off set for 10% FPR gives 0–73% FPR at new sites. 22 of 32 cohort–model pairs fall outside 0.05–0.15. The drift is a property of the site: the two models agree at ρ = 0.69, and AUROC does not predict the error (ρ = −0.18). This is a practical finding that iMeta readers, who build these classifiers, have not seen tabulated. The paper uses 19 public cohorts, a pre-registered protocol, a locked external CRC test and public code. That is above the iMeta Letter median on every rigour dimension.
2. **Against: the headline "fix" is guaranteed by the design, not shown by the data.** Calibration and evaluation controls are random halves of the *same* cohort, so they are exchangeable by construction. Under exchangeability, the conformal rule's expected FPR is exactly (n+1−k)/(n+1): 0.091 at n = 10 and 0.095 at n = 20. The single-split exceedance P(FPR > 0.15) follows Beta(n+1−k, k): 0.20, 0.18 and 0.15 at n = 10, 20 and 30. The paper reports cohort means of 0.08–0.11 and exceedances of 0.21, 0.19 and 0.19. That is the theorem reproduced. The title, the summary and the third results section sell this as the main result. A methods-literate reviewer will say so in the first paragraph of the report.
3. **Against: method novelty is zero and the paper half-admits it.** The conformal and Neyman–Pearson order-statistic threshold, local verification with about 20 reference samples (CLSI EP28), and "anchor" (intercept) recalibration are all textbook. Two close papers are also under-acknowledged. Wirbel 2019 already set an FPR = 0.1 cut-off on training controls and plotted study-to-study FPR. CRC-TrustBench (ref 9) already applies conformal calibration under leave-one-study-out. The submission can only succeed as an **audit plus a reporting and deployment recommendation**, not as a method paper. The framing is currently halfway between the two.

---

## 2. Is the novelty enough for iMeta?

**The objection, stated as a reviewer will state it:** "This is local recalibration. Split-conformal or Neyman–Pearson thresholds from n held-out negatives are known (Vovk; Tong 2018; Bates 2023). Labs already verify cut-offs on about 20 local samples (EP28). Site heterogeneity in specificity is known (Leeflang 2013; Van Calster 2023; Wirbel 2019). The empirical demonstration is circular because the calibration and test controls come from one random split."

**Point by point**

| Component | Novel? | Comment |
|---|---|---|
| Conformal threshold from n local controls | **No** (method) | The paper cites [17, 18] honestly, but the title still makes this the contribution. |
| Evidence that the conformal rule works on these data | **No, as designed** | Random within-cohort splits make the 20/20 success a mathematical certainty. It says nothing about real deployment, where the local controls (for example colonoscopy-negative volunteers) may not resemble the screened population. |
| Fixed-threshold FPR is over-dispersed across microbiome cohorts, in both directions, in 4 diseases | **Yes, modestly** | Wirbel 2019 showed the CRC case in one figure. This paper is the first systematic, multi-disease, pre-registered quantification with an over-dispersion test. This is the real contribution. |
| AUROC does not predict threshold failure; drift belongs to the site | **Yes** | This is the most quotable insight for iMeta readers. It is currently buried in paragraph 4 of Section 1. |
| Label-free fixes fail: z-score batch correction, EM prevalence correction, unlabelled quantile | **Partly** | The EM argument is neat: under pure label shift the FPR at a fixed threshold cannot move, so the drift must be a shift in control scores. So is the prevalence bound for the pool quantile. But the batch-correction arm is a straw man: only within-cohort z-scoring was tested, not MMUPHin, ComBat-seq or DEBIAS-M. |
| Explanation of *why* control scores shift | **Not shown** | ρ = 0.80 between the median control-score shift and the realised FPR is close to a tautology: the FPR is a function of where the control scores sit relative to the threshold. The proposed causes (extraction, depth, diet, geography, how controls were defined) are listed but never tested, even though curatedMetagenomicData metadata would allow it. |

**Verdict:** The novelty is enough for an iMeta Letter **only if** the paper (a) is reframed as "fixed operating points do not transfer, AUROC hides this, and label-free fixes fail", with local verification offered as the recommended practice rather than the discovery, and (b) adds at least one test where the conformal rule is *not* guaranteed to work. This would be calibration controls taken from a different source than the evaluation controls. Without (b), reviewers will call the third section trivial. Without (a), the editor's two-minute read is "they rediscovered conformal prediction". iMeta values audits that change practice. Its own Letters include benchmark and audit papers, so the reframed paper fits. The current framing does not.

Concrete non-exchangeable stress tests, all possible with the existing data:
- **Within-cohort source mismatch.** Calibrate on controls from one country, site or stratum and evaluate on another. Options: MetaCardis split by country; HMP2 split by recruitment site; Yachida split by sex or age tertile; any cohort split by sequencing-depth tertile.
- **Neighbour-cohort calibration.** Calibrate on 20 controls from a *different* cohort in the same country or from the same lab, and evaluate on the target cohort. This mimics a lab that borrows "local" controls.
- **Control-definition mismatch.** Where both exist, calibrate on population-sampled controls and evaluate on colonoscopy-negative controls, or the reverse.

Report how far the realised FPR then moves from α. If it stays in the 0.05–0.15 band, the paper is much stronger. If it fails, that is an honest and important boundary condition. Either outcome makes the paper.

---

## 3. What the editor sees in 2 minutes

**Title.** "Twenty local controls keep gut-microbiome diagnostic thresholds honest at new sites"
- "Keep … honest" is cute and vague, and it reads like a blog headline.
- "Twenty" is arbitrary. n = 10 performs the same at α = 0.10 (28/28 pairs in band). The number 20 comes from the α = 0.05 floor and from the reference-interval analogy, not from the data.
- The title sells the *non-novel* part (the fix) and hides the novel part (thresholds drift, and AUROC hides it).
- Suggested titles (10–14 words, iMeta style):
  - **"Gut-microbiome classifier thresholds do not transfer across cohorts, and AUROC hides it"**
  - "Cross-cohort AUROC hides decision-threshold failure in gut-metagenome diagnostics"
  - "Fixed decision thresholds of gut-microbiome classifiers drift across cohorts and need local verification"

**Graphical-abstract summary.** It is clear and numerical, which is good. But it **overclaims**:
- "Setting the threshold from 20 labelled local controls kept every cohort within 0.08–0.11." This applies only to the 10 of 16 cohorts with enough controls. The values are means over 200 splits, while a single deployment still exceeds 0.15 in 19% of calibration sets. The sentence must say so.
- "19 public cohorts" next to "16 held-out cohorts", with an introduction listing 11 + 4 + 4 + 5 = 24 cohorts, confuses the reader. The adenoma task re-uses CRC controls, and this is never stated in the main text.
- "Batch correction … did not fix this" generalises from a single z-scoring baseline.

**Opening.** "To the Editor" plus a problem paragraph matches iMeta style well. The reference-interval analogy is excellent and should stay. Weaknesses:
- "Whether it still gives the promised FPR … is rarely reported [8, 9]" is unfair to Wirbel 2019 [1], which reported this for CRC. Say what is missing: no per-cohort, multi-disease audit and no test of fixes.
- The "Here, we" paragraph ends with "about 20 local controls are needed to fix them". This is again the textbook part.

**Figures.**
- **Figure 1 (dot plot by cohort, LASSO): strong.** It is the best item in the paper and an editor understands it in 5 seconds. Problems:
  - 6 of 16 cohorts have no green diamond, which looks like missing data. Mark them "too few controls" (for example a grey "n/a" tag) or split the panel.
  - The green diamonds sit almost exactly on 0.10, which invites the "of course" reaction. Add error bars (5th–95th percentile across splits) so the per-deployment spread is visible and honest.
  - There is no schematic. Every iMeta Letter in the benchmark has a workflow or schematic panel.
- **Figure 2: busy but informative.**
  - Panels are labelled lowercase "a, b, c" but the legend says (A)–(C).
  - The in-figure footnote says "Aqua" but the legend says "Green".
  - The x-axis of panel A runs 0–1 because of EM, which squashes the region that matters (0–0.4). Break the axis or clip EM with arrows.
  - The 95%-confidence rule sits visibly *below* the band (FPR about 0.03, sensitivity 0.08). The text never says that it fails the authors' own band criterion: its share in band is 0/12 in Table S3a.
- **Figure 3.**
  - Panel A is the clinical hook, but the three trajectories are hard to follow, and the cohort labels sit only on the status-quo points.
  - Panel B mixes cohort sets across n (stated in the legend). Its key message, that conformal exceedance barely falls with n, is again just Beta-distribution theory.
  - Panel labels are lowercase again.
- **Count.** Three main figures sits within the allowed 1–3, but every observed iMeta Letter used two. Merge Figure 3 into Figure 2, or move Figure 3B to the SI and make Figure 1 a two-panel figure with a schematic.

**Does it sell?** Half. Figure 1 and the AUROC-hides-it message sell. The title, the summary and Section 3 sell a textbook method that the experimental design guarantees, and that is what reviewers will attack.

---

## 4. Format compliance (iMeta Letter)

| Item | iMeta norm | This submission | Status |
|---|---|---|---|
| Main-text words (To the Editor → Conclusion) | 1,500–3,000; Letters observed 1,907–2,503 | ≈1,690 | OK. There are about 400 spare words, enough for the stress test and the novelty paragraph. |
| Graphical-abstract summary | about 100 words + **graphical abstract image** | 117 words; **no image** | Trim the text; the image is **missing**. |
| Abstract / Highlights | none for Letters | none | OK |
| Main figures | 1–3 (observed: always 2), multi-panel, with schematic, vector | 3, no schematic; PDF vectors present | Acceptable; 2 is better |
| Main-text tables | none | none | OK |
| Headings | 2–4 ALL-CAPS finding sentences | 3 + CONCLUSION | OK |
| METHODS | one line pointing to SI | yes | OK |
| References | about 20, Wiley numbered style | 20 | OK at the cap. Some slots are used poorly (see item 9). |
| Back matter order | Author contributions, Acknowledgments, COI, Funding, Ethics, AI statement, Data availability, ORCID, References, Supporting Information | **FUNDING missing, ORCID missing, final "SUPPORTING INFORMATION" section missing**; 3 placeholders; GitHub URL missing | **Fail until completed** |
| Data availability | GitHub + source; iMeta prefers an archived DOI (Zenodo) | Source given; URL is a placeholder | Add GitHub + Zenodo DOI |
| SI table order | sequential | Table S5 appears before S4 in si_tables.md; S3a/S3b are not cited distinctly | Fix |
| Panel lettering | uppercase A, B, C | lowercase in figures | Fix |

---

## 5. Required changes, ranked by impact

**1. Add a non-exchangeable calibration test (the decisive change).**
The current conformal result is guaranteed by the random within-cohort split, and reviewers will see this immediately.
*Fix:* Add one SI analysis and one main-text paragraph (about 150 words) on calibration controls from a mismatched source. Use any of: MetaCardis by country, HMP2 by site, a sequencing-depth tertile, or a neighbour cohort from the same country. Report the realised FPR, in-band share and exceedance. Pre-specify the analysis in a protocol addendum (post-hoc, labelled as such). Also say in the text that within-cohort performance matches theory:
> "Because calibration and evaluation controls were random halves of one cohort, the conformal rule is expected to give a mean FPR of (n+1−k)/(n+1) = 0.095 at n = 20; the observed 0.08–0.11 confirms the implementation rather than the rule. The practical question is how robust it is when local controls differ from the screened population. We tested this by …"

**2. Reframe the title, the summary and the "Here, we" paragraph around the drift and the AUROC blind spot, not the fix.**
*Fix:* New title (see Section 3), for example **"Gut-microbiome classifier thresholds do not transfer across cohorts, and AUROC hides it."** Rewrite the end of the "Here, we" paragraph:
> "The threshold-setting rule we end up recommending is not new: it is the order-statistic rule of conformal and Neyman–Pearson classification, and it mirrors how clinical laboratories verify reference intervals. What is new is the evidence that microbiome tests need it. Fixed thresholds drift far beyond chance in every disease we examined, the drift is invisible to AUROC, and none of the label-free corrections we tried removes it."

Rewritten summary (about 100 words):
> "Gut-metagenome classifiers are validated by AUROC across cohorts, but a deployed test runs at one fixed threshold. Across 16 held-out cohorts in four diseases (19 public cohorts), a threshold set for 10% false positives on training data gave 0–73% at new sites; 69% of cohort–model pairs missed the target by more than half. AUROC did not predict which sites failed. Batch standardisation and prevalence correction did not help. Re-setting the threshold on 20 confirmed local controls, a standard conformal rule, restored the mean false-positive rate in all 10 cohorts large enough to test, although single calibrations still exceeded 15% about one time in five."

**3. Correct the overclaims and the unreported adverse findings.**
- "kept every cohort within 0.08–0.11": add "of the 10 cohorts with ≥ 40 controls; mean over 200 splits".
- Cohort-wise standardisation *lowered* the in-band share (0.31 → 0.28) and sensitivity (0.39 → 0.31). The phrase "narrowed the spread" is misleading. Say: "it did not increase the share of pairs on target (28% vs 31%) and cost sensitivity."
- The 95%-confidence rule had **0 of 12** pairs in the band (FPR 0.03–0.04) and sensitivity 0.08. Say this plainly, and soften Conclusion (ii) "≥ 30 for a 95%-confidence guarantee". As written it recommends a rule that over-corrects and nearly halves sensitivity again.
- The anchor rule with location–scale at n = 30 reached 83% in band. The text reports only "40–50%". Report it or explain why it is excluded.
- Pooled mean sensitivity falls from 0.39 to 0.28 under the conformal rule. State this in Section 3. At present only the CRC per-1,000 numbers appear.

**4. Disclose the overlap between held-out cohorts and development data, and the shared controls.**
The 5 adenoma "held-out" cohorts are FengQ, HanniganGD, ThomasAM_2018a and ZellerG, which are 4 of the 8 CRC *development* cohorts, plus YachidaS, which is also an external CRC cohort. Their controls were seen during method development, and YachidaS controls are counted twice. The independence implied by "16 held-out cohorts" is overstated.
*Fix:* One sentence in the main text: "The adenoma task re-uses the controls of five CRC cohorts, four of which were development cohorts; adenoma cases were never used in development." Report the headline drift numbers with and without the adenoma task, and reconcile 11 + 4 + 4 + 5 = 24 with the stated 19 cohorts.

**5. Complete the submission package (or it is returned unread).**
Fill in Authors and affiliations, Author Contributions (CRediT), COI, Funding, the AI-use statement and ORCID. Add the GitHub URL **and** a Zenodo DOI for the frozen code, scores and protocol. Provide a graphical-abstract image. Add the closing "SUPPORTING INFORMATION" section listing Figure S1, Tables S1–S5, the protocol and the development log.

**6. Strengthen the batch-correction comparison, or narrow the claim.**
A single within-cohort z-scoring is a straw man for "batch correction does not fix it". Within-cohort standardisation that uses the target cohort's *cases* also behaves differently at 0.5% screening prevalence than at about 50% case–control prevalence, which deserves a sentence.
*Fix:* Add MMUPHin (Ma et al., Genome Biol 2022), the standard microbiome meta-analysis batch tool, built for curatedMetagenomicData-style data, and ideally DEBIAS-M [20]. Report both in Table S3. If that is not possible, change the heading to "Simple batch standardisation and prevalence correction do not restore the operating point", and the summary to "simple batch standardisation".

**7. Replace the near-tautological "cause" analysis with a real one.**
ρ = 0.80 between the control-score shift and the FPR follows almost by definition. *Fix:* Present it as a diagnostic ("drift is visible in control scores alone, so it can be monitored without cases"), which is actually useful. Then test metadata explanations with the 16 cohorts × 2 models: median sequencing depth, DNA extraction kit, country, and control definition (colonoscopy-confirmed vs not). Even a simple rank correlation or a small table adds the "biological or technical insight" that iMeta ML Letters are expected to carry.

**8. Fix the figures.**
- Uppercase panel letters A–C in all figures.
- Make "Aqua" vs "Green" consistent.
- Figure 1: show 5th–95th percentile intervals across splits for the green diamonds and mark cohorts that are "too few controls".
- Figure 2A: break or clip the x-axis at 0.4.
- Figure 3A: label every point or use per-cohort colours.
- Add a schematic panel showing the deployment protocol: train → transfer threshold → realised FPR at the site vs score 20 local controls → take the 19th of 20 → monitor. This could be panel 1A, which would make Figure 1 two-panel.
- Target 2 main figures: fold Figure 3A into Figure 2 as panel D and move Figure 3B to the SI.

**9. Fix the related-work positioning and reference use (within 20 refs).**
- Acknowledge Wirbel 2019's per-study FPR plot explicitly.
- Contrast with CRC-TrustBench [9]: "[9] evaluated calibration and conformal coverage under leave-one-study-out at a fixed 0.5 threshold; it did not audit realised specificity at a pre-specified operating point or test site-level re-thresholding."
- Ref 7 (GLOBOCAN) does not support "every false positive becomes a colonoscopy". Replace it with a FIT follow-up or US Multi-Society Task Force citation, or drop it.
- Add MMUPHin, and a clinical model-updating reference (for example Vergouwe 2017 or Steyerberg's updating hierarchy) to frame the "anchor" as known intercept recalibration.
- Cite CLSI EP28-A3c directly next to Ozarda [10].
- Drop or merge Godau [16] to stay at 20.
- Verify every 2025–2026 reference (Piccinno 2025, Godau 2025, CRC-TrustBench 2026) against the publisher record before submission.

**10. Make the title number defensible, or remove it.**
n = 10 works equally well at α = 0.10. *Fix:* Remove "Twenty" from the title. In the text, give the rule as "n ≥ ⌈1/α⌉ − 1 for a finite threshold (9 at α = 0.10, 19 at α = 0.05). We recommend 20 so that the same set works at both targets and to match reference-interval verification practice." The "hard floor" paragraph already contains the logic; promote it.

**11. Make the clinical framing honest.**
At FPR 0.10, sensitivity of about 50–70% and 0.5% prevalence, these classifiers are clearly worse than FIT, which has about 5% positivity and about 75% sensitivity for CRC. An editor or clinical reviewer will note that "unnecessary colonoscopies" are being saved relative to a test nobody would deploy.
*Fix:* Add one sentence: "These models are not competitive with FIT; the point is that any microbiome test, including future better ones, will inherit this calibration failure." The "confirmed local controls" also come from colonoscopy, so they are typically FIT-positive or symptomatic referrals, not average-risk screenees. Mention this as a limitation, because it bears directly on exchangeability (item 1).

**12. Statistical presentation.**
- Report P-values like "P < 10⁻¹⁰⁰" rather than "6.1 × 10⁻¹⁷⁷". At these magnitudes the precision is meaningless.
- Note that the over-dispersion test treats the training threshold as fixed and ignores its estimation error. This is minor given the size of the training data, but reviewers will ask.
- The 32 pairs are not independent: there are 2 models per cohort, and the YachidaS controls are re-used. Say so where 69% is reported.
- Table S4 appears after S5. Renumber.
- "Both pre-stated success criteria were met" needs a caveat. The criterion of a lower SD "in every disease task" could not be assessed for IBD at n = 20, because only one IBD cohort was feasible (Table S5 has empty IBD cells). Say this explicitly or cite the n = 10 result for IBD.

---

## Bottom line for the authors

The data, the rigour and Figure 1 are good enough for iMeta. The pitch is not. Sell the audit ("AUROC hides threshold failure across 16 cohorts and 4 diseases; label-free fixes fail"), present the conformal rule as the recommended standard practice, and add one test where that rule could fail. Fix the package placeholders. Then this is a credible iMeta Letter.
