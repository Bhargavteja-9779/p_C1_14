# Handling editor triage, round 2: iMeta Short Communication (Letter)

**Manuscript:** "The decision threshold of a stool-metagenome classifier must be set at each site, on that site's own samples" (draft v0.3, 2026-11-25)
**Reviewer role:** handling editor (desk triage). Date: 2026-11-25.
**Files read:** `manuscript/manuscript.md`, `manuscript/supporting_information.md`, `figures/Figure1.png`, `figures/Figure2.png` (viewed), `journal_selection/{selected_journal.md, style_notes.md, journal_level_profile.md, journal_benchmark.csv}`.
**Cross-checks:** headline numbers checked against `results/cohort_level_summary.csv` and the SI tables (S2-S4). Round-1 reviews and the response were read for context.

---

## 1. Summary

The authors re-analyse 19 public curatedMetagenomicData studies: 24 cohort-task pairs, 3,626 stool metagenomes, covering CRC, IBD, T2D and adenoma. The design has three parts:

- Two classifiers, LASSO and random forest, are trained on eight CRC development cohorts.
- The cut-off is set at 90% specificity on the training scores.
- The analysis is pre-registered and run once on 16 locked test cohort-task pairs. Post hoc experiments are clearly labelled.

The manuscript makes four claims:

1. **The training cut-off does not transfer.** The realised FPR ranges from 0.00 to 0.74 across locked cohorts, and cohorts with similar AUROC have very different FPRs.
2. **Label-free adaptation methods do not fix this.** Five methods were tested: EM, MLLS, two-Gaussian calibration, per-site standardisation and a location-scale mixture fit. None repairs the cut-off, and four make it worse.
3. **A classical order-statistic ("rank") rule works locally.** It sets the cut-off from the site's own unlabelled samples. It keeps the expected FPR near the target (cohort-RMSE 0.031 vs 0.185) and roughly matches ten labelled local controls.
4. **It works only on same-site samples.** Post hoc, the rule fails when the pool comes from another cohort, or from another centre of the same study (MetaCardis).

The revision has improved a great deal since round 1:

- The novelty claim for the rule has been dropped.
- The plain local quantile and per-deployment exceedance now appear in the main text.
- The weakness of the exchangeability-by-design test is stated openly, and a cross-site test was added.
- Figure legends, keywords, running title and graphical-abstract text have been added.

I spot-checked the numbers and they match the result files. Examples:

- FPR range 0.00-0.74, median 0.10.
- Ten units with AUROC ≥ 0.70, with FPR 0.02-0.39.
- Pool sizes of 6-30 controls in 12 of 16 cohorts.
- Abstention of 31% at α = 0.05.
- 199 vs 87 healthy people referred per 1,000 screened.
- The clustered CIs and TOST.

The statistics and transparency (locked cohorts, disclosed deviations, Holm correction, clustered CIs) are well above the iMeta Letter median.

The open question for an editor is **significance, not rigour**. The take-home message is to recalibrate the cut-off locally, on the site's own samples. Clinical prediction (refs 8-9) and laboratory medicine (ref 24) already know this. The rule itself is classical. The new content is therefore an empirical demonstration for microbiome classifiers, plus the negative result on ML label-free fixes, plus the "same centre, not same study" finding. That last finding rests on one post hoc study with three centres.

## 2. Decision

**Return to authors before external review (format and claims). No desk rejection at this stage, conditional on the REQUIRED items.**

**Candid desk-rejection risk if submitted as is: moderate to high, about 40-50%.** The main drivers are:

1. **Perceived incrementality.** A handling editor who reads the title and first paragraph sees two things: a known principle (local recalibration), and a rule the authors themselves say is not new. Every benchmark Letter except the AI-readiness audit offers a tool or platform, new data, or a biological finding. This paper offers none of those. Its value is a *practice-changing reporting and deployment recommendation* for the field, and that must come through in the first 150 words.
2. **Weak clinical anchoring.** The classifiers are weak, with CRC sensitivity of 0.48 at 10% FPR under the rank rule, and the paper frames itself as CRC screening. FIT-based programmes already operate at better sensitivity and specificity. A clinically minded editor may conclude that the problem is hypothetical, because no microbiome test is deployed. The paper should frame itself as guidance for *validation and reporting of microbiome diagnostics*, not as a screening tool.
3. **The headline normative claim rests on post hoc evidence.** "Must be set at each site" relies on the cross-site experiments (E3, E5). Those are post hoc, and the centre-level test uses a single study (MetaCardis, T2D, a weak classifier). The locked success was guaranteed by design: the pools were exchangeable by construction.
4. **Signs of a previous review round in the text.** The text mentions a previous review round ("After peer review…", "the two weaknesses that reviewers raised"), and the draft header comment is still present. In a first submission this confuses the editor and invites questions about a prior rejection.
5. **Borderline length.** The main text is about 1,550 words including headings, or about 1,510 without them. That is barely above the 1,500-word minimum and well below every benchmark Letter (1,907-2,503).

If the REQUIRED items are done, I would send the paper to two reviewers (one microbiome diagnostics, one statistics). I would expect it to be competitive as a "methods-practice" Letter, comparable in genre to "A decade-scale audit of microbiome AI-readiness".

## 3. Assessment by criterion

### 3.1 Fit and significance for iMeta's broad microbiome readership
- **Fit: good.** iMeta covers microbiome machine learning, cross-cohort diagnostics and data-science practice. Anyone who publishes a microbiome classifier is in the audience.
- **Significance: moderate.** The most useful and citable message is about reporting: AUROC-based external validation hides threshold failure, so studies should report the realised FPR per external cohort. That message comes first in the Conclusion but is not in the title or highlights.
- The finding that label-free ML methods fail is useful, but mainly to methodologists.
- The same-centre finding is the most original element, but it is post hoc and based on a single study.

### 3.2 Title, highlights, first paragraph and conclusion: is the message clear and accurate?
- **Title (19 words).**
  - It is clear but prescriptive ("must"), and longer than the house style of 8-15 words and the benchmark median of 13.
  - "Must … on that site's own samples" overstates evidence that is post hoc and comes from one study at centre level.
  - Suggested direction: "Decision thresholds of gut-microbiome classifiers do not transfer between sites and need local unlabelled calibration" (15 words). Or, leading with the reporting angle: "AUROC hides threshold failure of gut-microbiome classifiers across cohorts".
- **Highlights.**
  - **Highlight 2 is inaccurate.** "Five *published* label-free adaptation methods": the location-scale mixture fit is the authors' own development method (SI Methods, "ours, development"). Only four are published.
  - The main text also says "We therefore tested published methods" before listing the mixture fit with no citation.
- **First paragraph.**
  - It is well motivated, but it is long (about 230 words before "We used…") and dense with citations (refs 1-11).
  - The gap sentence comes last and runs over 50 words.
  - The reader meets the key idea, "a cut-off decides how many healthy people get colonoscopy", in sentence 3. It should come first.
  - There is no single "Here, we show that…" sentence that states the headline result. The second paragraph describes the data but not the finding.
- **Conclusion.**
  - It is clear and actionable: report the realised FPR, and run a local calibration that is repeated after any change.
  - It overstates two points. First, "restores the intended FPR": the mean FPR is 0.082, deliberately conservative, and the FPR still exceeds 15% in 14% of deployments. Second, "a few hundred of the site's own samples": that regime was tested only post hoc, in three cohorts.
  - It ends with a placeholder, "Code and result tables: [[GitHub URL]]".

### 3.3 Format compliance (iMeta Short Communication)

| Item | iMeta requirement (source) | Manuscript | Status |
|---|---|---|---|
| Article type | Short Communication: "1500 ~ 3000 words and 1~3 figures" (HEP guidelines page, verified 2026-11-25). Published under the heading "Letter". | Letter / Short Communication, 2 figures | OK |
| Main text length | ≥1,500 words | About 1,553 including headings (body from "To the Editor" to the end of the Conclusion); about 1,510 without | Borderline. Below every benchmark Letter. |
| Abstract | The guidelines table lists "Yes, Structured" for Short Communication (verified). Published 2025-2026 Letters carry only a graphical-abstract summary (verified in PMC XML for PMC13780379 and PMC12371266). | No abstract; graphical-abstract text only | Ask the editorial office (unresolved since round 1) |
| Graphical abstract / TOC | Text "no more than 80 words or 3 sentences"; image 50 × 60 mm, legible (verified) | Text of 51 words, 2 sentences: OK. **No image supplied.** | Image missing |
| Highlights | Not listed for Short Communication on the guidelines page. Not present in published Letters' PMC XML (verified for 2 Letters). Optional "Practitioner Points", no more than 3 (verified). | 3 highlights, about 500 characters | Not required. Rename to Practitioner Points or drop. Fix the accuracy of highlight 2. |
| Title | "Brief informative title… should not contain abbreviations" (verified) | No abbreviations; 19 words | OK, but long |
| Running title | <40 characters (verified) | "Local cut-offs for microbiome tests" (35 characters) | OK |
| Keywords | "Up to seven keywords" (verified) | **8 keywords** | Non-compliant |
| Title page | Authors, affiliations, corresponding author, ORCID (standard Wiley) | Absent | Missing (author-only) |
| Author contributions | CRediT mandatory (verified) | `[[…]]` placeholder | Author-only, known |
| Funding | Statement required, in Acknowledgments (verified) | Separate FUNDING section with `[[…]]` placeholder | Author-only, known. Move into Acknowledgments or follow the editorial office. |
| Conflict of interest | Required (verified) | Present | OK |
| Ethics statement | Required where relevant (verified) | Present (re-analysis of de-identified public data) | OK |
| AI statement | Not on the guidelines page. Present as "AI STATEMENT" in a published 2026 Letter (PMC13780379, verified). | **Absent** | Add one |
| Data availability | Required (verified) | Present; code URL and archive DOI are `[[…]]` | Author-only, known |
| Figures | Vector format recommended; separate files; legends in the text (verified) | Vector PDFs and 300-dpi PNGs; legends present | OK |
| References | No cap; any consistent style (verified). Benchmark Letters have 15-20. | 27 in the list (ref 27 cited only in the SI). Wiley numeric style, consistent. | OK. Slightly above the benchmark. |
| Supporting Information | Unlimited | Methods, Note S1, Tables S1-S4 | OK. Table S1 is still a pointer to a CSV. |
| Back-matter order | House practice (style notes and published Letters) | Order follows house practice | OK |

### 3.4 Clarity and English
- **Overall.** The prose is plain, short and mostly active, and well suited to a broad readership. It is much improved over v0.2.
- **"Cohort-RMSE" needs a plain definition in the main text.** It is the root-mean-square, over cohorts, of the *mean* FPR minus the target. Readers will otherwise read it as a per-deployment error.
- **Exponents.** "P = 2 × 10^-52" and "5 × 10^-88" should use superscripts, or the values should move to the SI. Give one plain sentence for overdispersion: "far more variable between cohorts than sampling error explains".
- **"Holm-adjusted P = 0.0004 over 16 cohort-task pairs" conflates two things.** Holm corrects across the nine comparisons, while the Wilcoxon test is over 16 pairs. Rephrase.
- **"Site" is defined only in the penultimate section** ("the population and the laboratory process together"). It is the key word of the title, so define it in paragraph 1 or 2.
- **Phrases that read as notes to reviewers:** "Post-hoc, we checked the two weaknesses that reviewers raised" and "After peer review we added…". See R3.
- **Minor wording fixes:**
  - "a fifth of the pool were patients" → "was".
  - "The reasons are simple." is informal.
  - "equivalent to ten labelled local controls within ±0.02": state that this holds at α = 0.10 only. At α = 0.05 the ten-control rule always abstains.
- **Naming consistency.** "Training" (Figure 1C) means the same as "unchanged cut-off" and "training cut-off" (text). "Per-site std." and "Mixture fit" should match the text names, and the mixture fit should be marked as the authors' own.

### 3.5 Do the claims match the results?
The numbers match the result files (see the Summary). Remaining mismatches of emphasis:

1. **"Five published" methods.** One of the five, the mixture fit, is the authors' own (see 3.2).
2. **"Restores / keeps the intended FPR".** The expected-FPR rule is conservative by design: mean FPR 0.082 at α = 0.10, and 0.049 at a 20% case share. It costs sensitivity: 0.25 overall vs 0.39 for the training cut-off, and 0.48 vs 0.65 in CRC. It abstains in 6% of units at α = 0.10 and 31% at α = 0.05. The strict version abstains in 50% and 75%. Wording such as "keeps the FPR at or below the target on average" would be accurate.
3. **Comparison with ten labelled controls is selectively reported.**
   - In the locked run, ten labelled controls had a *lower* cohort-RMSE (0.027 vs 0.031; unit-level P = 0.048, Table S2). The rank rule wins only on per-deployment exceedance (14% vs 20%).
   - In post hoc E1 (Table S4), ten labelled controls reached a cohort-RMSE of 0.011 vs 0.030-0.034 for the rank rule.
   - The main text presents only equivalence. Say plainly that ten verified negatives are as good or better on average, and that the rank rule's advantages are fewer large exceedances and no need for confirmed diagnoses.
4. **"AUROC-based validation cannot reveal this failure"** is close to a tautology, because AUROC is threshold-free by definition. The informative finding is that AUROC does not *predict* which cohorts fail. Say that.
5. **The "same site" headline rests on post hoc E5.** That is one study, three centres, T2D, with a classifier whose AUROC is near 0.6. Within MetaCardis the *training* cut-off was conservative (FPR 0.005-0.09), so "no better than the training cut-off" there means a different failure mode: under-calling rather than over-calling. Present it as strong suggestive evidence, not a demonstrated rule.
6. **E3 detail omitted.** In the cross-cohort pools the strict rule did better (pair-RMSE 0.111, 11% of pairs above 15%) than the expected-FPR rule (0.158, 33%). A one-clause mention would be fair.
7. **Pool-size recommendation versus tested regime.** The 360/610/1,500 figures come from the analytic bound (Note S1). Empirically, pools of 25-500 were tested only in three cohorts (E2). Phrase it as a theoretical requirement that was checked partially.
8. **Abstention scoring flatters the strict rule in Figure 2A.** Abstention is counted as FPR 0, so the strict rule's "1% above 15%" coexists with 50% abstention. Show abstention next to the exceedance column.

### 3.6 Level compared with the benchmark papers
- **Above the benchmark Letters on:**
  - number of cohorts (24 cohort-task pairs vs a median of 3);
  - number of baselines (9 vs about 0);
  - a locked, pre-registered test;
  - clustered CIs, Holm correction and equivalence testing;
  - deployment consequences per 1,000 screened;
  - disclosed deviations.
- **Below the benchmark Letters on:**
  - **Deliverable.** There is no tool, new data or biological insight; the rule is a few lines of code. A small, citable function or package with a worked example would answer this (Suggested S3).
  - **Length.** About 1,550 words vs 1,907-2,503.
  - **Figure style.** There is no schematic or workflow panel, which appears in essentially all benchmark Letters.
- **Net:** methodologically strong, editorially "quiet". Acceptance hinges on whether the editor sees the reporting and deployment message as field-relevant.

### 3.7 Figures (viewed)
- **Figure 1.**
  - Clean and legible.
  - In 1A, the LASSO circles are partly hidden behind the RF diamonds for several cohorts (e.g. YachidaS, YuJ). Offset them vertically.
  - 1B has no cohort labels on the extreme points (e.g. T2D QinJ at 0.73).
  - 1C mixes published methods with the authors' mixture fit without marking it. The categorical x-axis (0, 1, 5, 20%) is acceptable if the legend says it is categorical.
  - No workflow schematic.
- **Figure 2.**
  - 2A is good: per-deployment spread plus an exceedance column. Add an abstention column (6%, 6%, 50%).
  - In 2B, three methods share each row with heavy overplotting, and the black median ticks are hard to see. There is no strict rule and no uncertainty interval. The "Same centre" training points near 0.03 need a sentence of explanation.
  - In 2C, the y-axis is labelled "(%)" while the text uses proportions in places. Align the units.
- Both figures are supplied as vector PDFs (about 30 kB each) and 300-dpi PNGs. Compliant.

## 4. REQUIRED changes (before external review)

1. **Correct highlight 2 and the matching text.** Say "four published methods and one mixture fit we developed on the development cohorts". In the main text, mark the location-scale mixture fit as the authors' own wherever "published methods" are listed, and in the Figure 1C legend.
2. **Reframe the opening for a broad readership.**
   - Open paragraph 1 with the consequence: the cut-off decides how many healthy people are referred, and AUROC does not show it.
   - Shorten paragraph 1 to about 150 words.
   - End the introduction with a single "Here, we show that…" sentence giving the three findings: thresholds fail; ML label-free fixes fail; a local rank rule on same-site samples works.
   - Lead with the reporting recommendation, which is the paper's most citable contribution and its main defence against an "incremental" desk decision.
3. **Remove all traces of the internal review process.**
   - Delete the HTML draft comment at the top of both files.
   - Delete "After peer review we added post-hoc experiments, which we label as exploratory". Replace it with "We also ran exploratory post hoc analyses, labelled as such".
   - Replace "Post-hoc, we checked the two weaknesses that reviewers raised" with neutral wording.
   - In the SI, replace "disclosed in response to review" and "designed after … review round 1" with "identified after the locked run".
4. **Shorten and qualify the title.** Aim for 15 words or fewer, and do not use "must" for a claim whose cross-site evidence is post hoc and comes from one study at centre level. See the options in 3.2.
5. **Qualify "restores the intended FPR".** Use "keeps the FPR at or below the target on average", or equivalent, in the highlights, graphical abstract and Conclusion. In the Conclusion, state the cost in one sentence: lower sensitivity (0.48 vs 0.65 in CRC), and abstention at small pools or a 5% target.
6. **Report the ten-labelled-control comparison in both directions.**
   - Report the locked cohort-RMSE of 0.027 vs 0.031 (labelled controls slightly better on average, unit-level P = 0.048) and E1's 0.011 vs about 0.03.
   - Then give the rank rule's advantages: fewer large exceedances, and no confirmed diagnoses needed.
   - State that the equivalence holds at α = 0.10 only.
7. **Present the same-site finding as post hoc and limited.**
   - In the section heading, highlights and Conclusion, signal that the centre-level evidence comes from one study (MetaCardis, three centres, T2D).
   - Explain that the training cut-off was conservative there, so "no better than the training cut-off" reflects a different failure.
   - Mention briefly that the strict rule was more robust cross-cohort (E3).
8. **Keywords: reduce to at most 7.** For example, merge "calibration" into "decision threshold", or drop "external validation".
9. **Supply the graphical-abstract image** (50 × 60 mm, legible at that size). Only the text exists. A schematic would do: training cohorts → transferred cut-off fails; new site's unlabelled pool → r-th highest score → cut-off.
10. **Add an AI statement** (used in 2026 iMeta Letters), even if it says that no generative AI was used, or that it was used for X.
11. **Bring the main text to at least about 1,800 words.** Use the space for content that strengthens significance, not for padding:
    - one paragraph of practical guidance (how to collect the pool, when to recalibrate, what to report);
    - the honest trade-offs from items 5-7;
    - a definition of "site" and of cohort-RMSE in plain words.
12. **Resolve the structured-abstract question with the editorial office before submission.** The guidelines table says "Yes, Structured", but published Letters have none. Have a 150-word structured abstract ready.
13. **Fix the figure points:**
    - Add an abstention column to Figure 2A.
    - Offset the overlapping LASSO and RF markers in 1A.
    - Mark the authors' mixture fit in 1C.
    - Reduce overplotting in 2B: separate rows per method, or one method per row with a median and IQR.
    - Use consistent method names across the figures, text and SI.
14. **Fix statistical wording.**
    - "Holm-adjusted P = 0.0004 (Wilcoxon over 16 cohort-task pairs; Holm across 9 comparisons)".
    - Superscript exponents, or move the overdispersion P values to the SI.
    - Rephrase "AUROC-based validation cannot reveal this failure" to "AUROC did not predict which cohorts failed".
15. **Complete the author-only items** (known placeholders; list for the authors):
    - `[[to be completed by the authors (CRediT)]]` (Author Contributions);
    - `[[to be completed by the authors]]` (Funding; place it per the iMeta Acknowledgments convention);
    - `[[GitHub URL]]` in the Conclusion;
    - `[[GitHub URL and archived DOI]]` in Data Availability.

    Also add a title page with authors, affiliations, corresponding author and ORCID. It is absent and not marked as a placeholder.

## 5. SUGGESTED changes

1. **Add a schematic panel**, as Figure 1A or a new panel. It can double as the graphical-abstract image and would match the house style of the benchmark Letters.
2. **Address clinical realism in one or two sentences.** At 10% FPR the CRC sensitivity is 0.48, below FIT performance. Position the work as guidance for validating and reporting microbiome diagnostics, so that a clinical editor does not dismiss it as a non-competitive screening test.
3. **Release the rule as a small, documented function** (Python/R, or a SIAMCAT-compatible helper). It should take pool scores, α, π_max and δ, and return a cut-off or "abstain" plus the required n. Cite it with a Zenodo DOI. This gives the Letter a concrete deliverable, as in the benchmark Letters.
4. **Convert the Highlights to "Practitioner Points"** (optional, no more than 3, as per the guidelines), phrased as actions:
   - report the realised FPR per external cohort;
   - calibrate on the site's own unlabelled samples (at least about 360 at a 1% case share);
   - do not rely on label-shift corrections at screening prevalence.
5. **Label the extreme cohorts in Figure 1B** (e.g. QinJ 2012) and add a sentence on why T2D cohorts drift most.
6. **Trim the reference list toward the about 20 typical of Letters**, for example by moving refs 22-23 or 27 to the SI. Make the SI reference for ref 27 self-contained.
7. **Give Table S1 as an actual table** in the SI rather than a pointer to a CSV.
8. **Explain the 2B "same centre" training points** (FPR about 0.03): the training cut-off was conservative in MetaCardis.
9. **Report the share of the 16 locked units in which the rank rule's mean FPR fell within ±0.02 of the target.** It is an intuitive single number for non-statisticians.
10. **Mention temporal drift and recalibration frequency briefly**, linked to laboratory quality-control practice.

## 6. What I could and could not verify about iMeta author guidelines

- **Verified** (journal.hep.com.cn/imeta/EN/guidelines, fetched 2026-11-25):
  - Short Communication: 1,500-3,000 words and 1-3 figures. Abstract listed as "Yes, Structured".
  - Running title under 40 characters. Up to 7 keywords. Title without abbreviations.
  - Graphical TOC/abstract: 80 words or fewer, or 3 sentences; 50 × 60 mm.
  - Optional Practitioner Points, no more than 3.
  - Mandatory CRediT; funding statement in the Acknowledgments; conflict of interest, ethics and data availability statements.
  - Any consistent reference style; vector figures recommended.
  - "Letter" is not a separate submission type (the closest are Short Communication and Correspondence).
- **Verified from published Letters** (Europe PMC full-text XML, PMC13780379 and PMC12371266): Letters carry a graphical-abstract summary (70-106 words in these two), no abstract, no highlights, ALL-CAPS section headings, and, in 2026, an "AI STATEMENT" section.
- **Could not verify:**
  - The Wiley-hosted author page (onlinelibrary.wiley.com/page/journal/2770596x/homepage/forauthors.html) returned HTTP 403, so I could not check whether it differs from the HEP page. This includes any Wiley-specific word counting (whether legends and references are excluded) and any highlights requirement on the Wiley submission form.
  - Whether an AI statement is mandatory, as opposed to customary.
  - Whether the editorial office enforces the structured abstract for Short Communications.
  - Any reference cap. None is stated; the benchmark shows 15-20.
  - JIF, quartile and APC (not needed for this decision).
- **References checked:** the three 2026 references (refs 10, 11, 17) resolve on Crossref with matching titles and journals. I did not verify that their content supports the specific claims made.
