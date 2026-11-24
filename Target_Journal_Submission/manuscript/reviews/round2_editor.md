# Handling editor screening report: iMeta Letter

**Manuscript:** "Microbiome colorectal cancer classifiers lose specificity across sites and patients; local recalibration restores it"
**Files screened:** submission_package/Manuscript.md; manuscript/SI_methods.md; manuscript/SI_tables.md; manuscript/cover_letter.md; Figure1.png, Figure2.png, Graphical_Abstract.png
**Format check:** main text about 1,600 words (To the Editor to Conclusion), 2 figures, 19 references, graphical abstract plus summary, no Highlights. Format is compliant. Author placeholders were ignored as instructed.

---

## 1. Decision

**Desk reject in current form, with encouragement to resubmit. Probability of being sent to review as submitted: 35%.**

The work is careful and better than most submissions in this area. It uses only public data, the protocol was frozen before the locked analysis, null results are reported, and there is a released tool. These are real strengths for iMeta. Three problems would still lead me, or the first reviewer, to stop:

- The title promises a finding about colorectal cancer (CRC) classifiers. Most of the site-level evidence actually comes from IBD and T2D classifiers.
- The headline range ("0% to 75%") is driven by sites with very few controls, and the text never tests whether the spread is more than sampling noise.
- The proposed verified-positive rule is presented as the main result. On the authors' own numbers, a simpler label-free rule does as well at stable sites, and better in the analysis without resampling (Figure 2D). The text does not say this.

All three can be fixed with existing code and public data. If items 1 to 3 below are fixed and the text is tightened, I estimate a 60 to 65% chance of being sent to review.

---

## 2. Remaining reasons for desk rejection (most important first), with feasible fixes

### R1. Story and evidence do not match: a "CRC" paper whose site-level evidence is mostly IBD and T2D
- Of the 11 fully independent held-out sites, 8 are IBD or T2D classifiers trained leave-one-cohort-out (Figure 1B; Table S1). Only 3 are CRC sites. The top of the "0 to 75%" range is a random-forest **T2D** classifier (Figure 1B), not a CRC test.
- Figures 2A, 2B and 2D present recalibration with colonoscopy feedback, yet they pool T2D and IBD sites. Figure 2D's two "large locked sites" are YachidaS_2019 (CRC) and MetaCardis_2020_a, which there is a **T2D-classifier** deployment (source FPR 0.038, Table S10). Figure 2C uses MetaCardis with the **CRC** classifier (control FPR 0.103, Table S5). A microbiome reader will not see that one cohort plays two different roles in Figure 2.
- At the 3 CRC sites, every site-model pair lies above the target (FPR about 0.11 to 0.28). For CRC, the finding is a **systematic liberal shift**: cut-offs from development cohorts are too lenient at new sites. That is a sharper message than "does not travel", and it is the one the title should carry.

**Fix (existing code):**
(a) Build the CRC evidence base from 11 CRC sites: the 8 development cohorts' leave-one-cohort-out realised FPR (already computed, Table S7 "pooled") plus the 3 locked CRC sites. Label them clearly as development versus locked.
(b) Present IBD and T2D as a generalisation panel or a supplementary figure, and drop "0 to 75%" from the title, summary and graphical abstract unless it is stated per disease.
(c) In Figure 2, either restrict A, B and D to CRC sites (YachidaS_2019, YuJ_2015, ThomasAM_2019_c, plus development leave-one-cohort-out sites if needed) or split the panels by disease. Say explicitly that Figure 2C applies the **CRC** test to a non-cancer cohort, and say how the "sensitivity proxy" in Table S5 was obtained (where the cases come from).
(d) Or, if the authors want a general claim, retitle around "stool microbiome disease classifiers" and make CRC the worked example. Pick one framing. The current mixture is the main reason the paper does not read as one story.

### R2. The headline variability is not shown to exceed sampling noise, and its blinding is overstated
- Several held-out sites have 12 to 43 controls (HallAB_2017 has 12, HMP_2019_ibdmdb has 27 or 14, SankaranarayananK_2015 has 18). With 12 controls, a true FPR of 10% gives an observed FPR of 0.25 about 10% of the time. "0% to 75%" and "12 of 22 pairs above 0.12" are therefore partly binomial noise. The pilot (SI S1) already used a chi-square overdispersion test, but its result is not reported for the locked sites.
- SI S1 states that the pilot computed source-cut-off specificity at the 3 CRC sites that were later held out. The main text says the protocol was "frozen ... before 16 held-out sites were analysed once". For the CRC sites this is not strictly true, and a reviewer reading the SI will notice.
- "16 held-out sites" counts 5 adenoma sites. Four of these are development CRC cohorts with shared controls, and the fifth (YachidaS_2019) is also a locked CRC site. Only 11 are independent.

**Fix:**
(a) Add exact binomial 95% CIs to every point in Figure 1B.
(b) Report the overdispersion test (observed FPR versus Binomial(n0, 0.10)) per disease. Better still, report a random-effects estimate of the between-site SD of logit FPR with its CI, since this is the quantity that "does not travel" actually refers to.
(c) Quote the headline as "11 independent sites" and give the range for sites with at least 40 controls.
(d) Add one sentence to the "Here, we" paragraph: "A pilot before the data lock had already shown the source-cut-off FPR at the three held-out CRC sites; all other locked results were unseen."

### R3. The proposed rule's added value is overstated and selectively reported
- At stable sites, the advantage of the verified-positive (VP) rule over the prevalence-bounded quantile disappears at sites with at least 40 controls (p = 0.72; per-cohort p = 0.715, Table S2d). Against the source cut-off, the per-cohort test is not significant either (p = 0.074, Table S2d). The main text reports only the site-by-model test (p = 0.011).
- VP's very low exceedance (0.6% of site-months above 0.12) comes from running **below** target: mean FPR 0.085, and about 0.08 in Figure 2A, while the oracle exceeds 0.12 in 11.6% of months. In Figure 2A the prevalence-bounded quantile actually sits closest to the 0.10 line. Readers will see this.
- **Figure 2D (no resampling, the most realistic analysis):** the prevalence-bounded rule exceeded 0.12 in 14% of months, against 19% for standard VP. The text reports VP's 19% and the high-confidence option's 5% but omits the 14%. This is the kind of omission that loses a reviewer's trust.
- Per-group recalibration needs groups that are defined and recorded in advance. Yet the mechanism section ends with "the over-flagged groups ... cannot be fully predicted in advance". As written, the two sections contradict each other.
- The high-confidence option gets its 5% partly by being stricter (mean FPR 0.071), which costs sensitivity. That cost is not reported in the text.

**Fix (existing code and tables):**
(a) Reframe Finding 3 honestly: "At stable sites, any local recalibration, including a label-free one, restores specificity. Outcome feedback is what adds recovery from upward drift, control within recorded groups and a high-confidence option."
(b) Report the prevalence-bounded result for Figure 2D in the text.
(c) Report the sensitivity of every rule next to its FPR in Figures 2A and 2D, and in the high-confidence comparison.
(d) For fairness, either add a high-confidence version of the prevalence-bounded quantile (a binomial order statistic; easy with existing code) or state why there is none.
(e) Replace "cannot be fully predicted in advance" with "differ between settings, so they should be monitored. Recorded groups can be recalibrated separately."
(f) Show the failure mode in the main text: after downward drift, all rules, VP included, stay too strict (Table S2c). The authors state it, but one clause is not enough for a deployment paper.

### R4. Mechanism claims go beyond the data
- **Heart failure "persisted":** this holds only for LASSO with sex, country and drugs (+0.28, 0.06 to 0.51). It is not significant for random forest (+0.13, -0.03 to 0.29) and not significant in the complete-case analysis with age and BMI (+0.28, -0.12 to 0.68; Table S9). Write "was attenuated and became uncertain after adjustment for age and BMI".
- **Metformin:** the only clear signal is from one cohort (MetaCardis). It is correctly called exploratory in the text, yet it sits in the title of Figure 1D ("drug-linked shifts"), in the summary and in the graphical abstract. Pool the four cohorts in Table S6d with a random-effects meta-analysis and report the pooled estimate with its heterogeneity (existing numbers).
- **PPI:** the pre-specified primary hypothesis (H5, LASSO total score) failed. The graphical abstract nevertheless lists "PPIs raise the oral component" as a finding. Remove it from the graphical abstract. In the text, mention that random forest gave a small positive effect (+0.09, p = 0.014) so the reporting is balanced.
- **"Two routes":** the decomposition (coefficient times mean shift) is descriptive and depends on the model. Call the two patterns "two patterns of species contributions", not "routes", unless a supporting analysis is added. Feasible supporting analysis: show that the oral-taxa component predicts over-flagging in a cohort that was not used to define the oral list.
- "Removing such shared species ... cost cancer detection (AUROC 0.76 to 0.72) before it removed the excess": at K = 2, disease positivity is 0.133 against control 0.044 (Table S4), so the excess is not removed at all. Say so plainly.

### R5. The deployment simulation is less realistic than the wording implies
- Controls resampled from case-control studies stand in for a screening population. Colonoscopy is treated as a perfect reference (only "5% missed" is varied). The same colonoscopy language is applied to IBD and T2D sites, where the confirmatory test is different.
- The clinical trade-off is real but is stated only once: at CRC sites, 83 fewer false-positive referrals per 1,000 against 1.1 more missed cancers per 1,000 (sensitivity 0.64 to 0.52). Microbiome tests at 90% specificity already have lower sensitivity than FIT. A clinical reader will ask whether the fix makes the test clinically unusable.

**Fix:** use YachidaS_2019 (the largest colonoscopy-based CRC cohort) as the primary illustration. Add one sentence putting the trade-off in context: what a programme gains, and that the trade-off is set by the target FPR, not by the rule. Name the verification test generically ("confirmatory test, e.g. colonoscopy") wherever non-CRC sites are pooled.

### R6. Internal inconsistencies a reviewer will find within minutes
| Location | Problem | Fix |
|---|---|---|
| Main text, batch correction | "random forest did not improve". Table S7 shows site-z random forest improved the share of sites above 0.12 (0.375 to 0.25) and the mean absolute deviation (0.102 to 0.084); only mean FPR and maximum FPR got worse. | "For random forest the share of sites above 0.12 fell (38% to 25%) but the worst site did not improve (0.36 to 0.39)." Also, this was tested only in development. Run site-wise standardisation on the locked sites with the existing code, since it is the obvious competitor to local recalibration. |
| Metformin sentence | "non-users were flagged at the control rate (10.3%)". Non-users were at 8.5% and controls at 10.3%. | "non-users (8.5%) were flagged no more often than controls (10.3%)". |
| Figure 2A vs text | The text gives a source mean FPR of 0.17 (Table S2, adenoma included). Figure 2A ("11 CRC/IBD/T2D sites") shows about 0.20. | Use the same site set and number in both places. |
| Figure 2D vs text | High-confidence mean FPR 0.071. The unweighted mean of Table S10 is 0.068. | Check, and state how sites and prevalences are averaged. |
| Figure 1A vs SI S1 | "13 other-condition cohorts" vs "eleven non-cancer cohorts" (+2 medication-only cohorts). | Use 11 + 2 consistently. Also reconcile the "32 cohorts" count. |
| Comorbid controls in CRC cohorts | "4% vs 16%". Comorbid controls were flagged **less** often (OR 0.26, p = 0.07 for LASSO; OR 0.10, p = 0.04 for random forest). | Say this directly. It is a notable result and needs one clause (a possible explanation is selection of healthier, medically screened comorbid controls). |
| Hypertension | Called "small" (+0.33), but its CI excludes 0 (0.07 to 0.60), and ME/CFS (+0.39, 0.12 to 0.67) is not mentioned at all. | Report both, or state the rule used to choose which conditions are named. |

### R7. Too dense for a microbiome reader
The recalibration section asks a microbiome audience to absorb verification bias, apple tasting, exchangeability, Neyman-Pearson rules, prevalence bounds and drift alarms in about 250 words. The paper also uses about 15 acronyms (AUROC, FPR, FIT, LASSO, IBD, T2D, PPI, HF, CAD, IGT, VP, BMI, ...). **Fix:** move the related-methods sentence (refs 16 to 19) to the SI. Explain the rule in one plain sentence plus one sentence on the guarantee. Spell out "false-positive rate" each time it heads a sentence or panel.

---

## 3. Line-level edits

### Title
Current (14 words): "Microbiome colorectal cancer classifiers lose specificity across sites and patients; local recalibration restores it"
- "across ... patients" is vague, and "restores it" hides the sensitivity cost. "Classifiers" is jargon; iMeta readers say "tests" or "signatures".
- Option A (CRC framing, after R1a): **"Stool microbiome colorectal cancer tests lose specificity at new sites and in comorbid patients; colonoscopy feedback restores it"** (17 words; trim "Stool" if needed).
- Option B (general framing): **"Fixed cut-offs of stool microbiome disease classifiers do not hold at new sites; outcome-based recalibration restores specificity"**.
- Make the running title match: "Specificity of microbiome tests at new sites".

### Graphical-abstract summary (currently ~100 words, dense, with jargon: "locked cardiometabolic cohort", "per-group control")
Suggested replacement (~95 words):
> Stool microbiome tests for colorectal cancer are judged by AUROC, but in use they work at a single cut-off. We asked whether a cut-off set for 90% specificity on published cohorts keeps that specificity elsewhere. At new sites, false-positive rates were mostly above target. People with cirrhosis or atherosclerosis were over-flagged through oral-origin CRC marker taxa. In a diabetes cohort, the excess tracked metformin use (exploratory). Re-setting the cut-off locally restored specificity. Using only colonoscopy results of test-positive people also recovered from score drift and controlled specificity within patient groups. The method is released as cutoffguard.

### First paragraph
- "with an AUROC of about 0.8 across countries [1, 2]": fine.
- "Two kinds of shift can break that specificity. First ... Second, the people tested differ." Good structure, but the second shift should be stated as a mechanism: "Second, the people tested include patients with other diseases or drugs that change the gut microbiome."
- The FIT sentence is the strongest motivation, but it is buried. Move it up: "For the fecal immunochemical test (FIT), screening programmes already set positivity cut-offs locally [6]. Microbiome tests have no equivalent practice."
- Final two sentences: merge into "Microbiome studies rarely report the specificity a fixed cut-off actually achieves at a new site or in specific patient groups, or how to restore it without a new labelled study."

### Second paragraph ("Here, we ...")
- Add the result numbers, as iMeta Letters do: "...in 32 public cohorts ... Cut-offs set for 90% specificity gave false-positive rates above 12% at X of 11 independent sites."
- Add the pilot disclosure (R2d).
- "Local recalibration restored the intended specificity, and a rule based on colonoscopy outcomes of test-positive people added robustness that matters in practice." "Robustness that matters in practice" is vague. Replace with: "...and a rule that uses only colonoscopy results of test-positive people also recovered from score drift and controlled specificity within patient groups."

### Section headings
1. "CUT-OFFS SET ON PUBLISHED COHORTS DO NOT HOLD AT NEW SITES": good. For CRC, consider "...ARE TOO LENIENT AT NEW CRC SITES" if R1 confirms a systematic shift.
2. "WHICH PATIENTS ARE OVER-FLAGGED DEPENDS ON DISEASE SEVERITY AND MEDICATION": overclaims, since "medication" rests on one cohort and the PPI hypothesis failed. Use **"PATIENTS WITH SEVERE DISEASE, AND POSSIBLY METFORMIN USERS, ARE OVER-FLAGGED"**, or "OVER-FLAGGED PATIENT GROUPS DIFFER BETWEEN SETTINGS".
3. "LOCAL RECALIBRATION RESTORES THE INTENDED SPECIFICITY": acceptable. After R3, consider "ANY LOCAL RECALIBRATION RESTORES SPECIFICITY; COLONOSCOPY FEEDBACK ADDS DRIFT AND GROUP CONTROL".

### Body sentences
- "Sensitivity moved with the FPR, so AUROC-based validation does not reveal the problem." The logic is implicit. Replace with: "Because sensitivity rose with the false-positive rate, the AUROC at these sites stayed similar, so AUROC-based validation would not reveal the problem."
- "It exceeded the 10% target by more than two percentage points in 12 of 22 site-model pairs in the 11 fully independent sites, and in 15 of 32 pairs when the adenoma sites are included". Too long. Keep the 11-site figure only and put the adenoma figure in the legend.
- "Mild cardiometabolic labels therefore do not drive false positives." This is overclaimed from n = 70 comorbid controls in 3 cohorts. Use "...were not associated with more false positives in these cohorts".
- "Because these groups differ in country and medication, we then added both to the model (post hoc)." Fine. Then apply the heart-failure correction from R4.
- "Metformin strongly reshapes the gut microbiome [11]." Move this before the metformin result, as the rationale.
- The verified-positive paragraph: cut from about 180 to about 90 words. Suggested core: "In screening, people who test positive have a colonoscopy, so their true status becomes known. The rule counts confirmed false positives above each candidate cut-off, treats everyone not yet confirmed as a possible false positive, and picks the lowest cut-off whose worst-case false-positive rate is at or below the target. It is updated monthly and restarts when a month has more false positives than chance allows. If controls at a site are exchangeable and prevalence stays below a stated bound, the expected false-positive rate is at most the target, whatever the referral, attendance or delay (Proposition S1)." Move refs 16 to 19 and the high-confidence detail to the SI, or to one short clause.
- Stable-site paragraph: report the prevalence-bounded quantile's FPR and exceedance next to VP's, not only the p values.
- "The verified-positive rule helped in three situations:" The bullet list breaks the Letter format. Convert it to prose.
- "At 10% prevalence, the prevalence-bounded rule became conservative (CRC sensitivity 0.44 vs 0.52)." Name the site set, and note that VP is conservative too (mean FPR 0.085).
- "The costs are a burn-in month with about 27% of people referred": a microbiome reader will be startled. Explain that this is a deliberate liberal start to collect verified outcomes, and give an alternative (start at the source cut-off).

### Conclusion
- "Local recalibration is therefore needed." Fine.
- "A rule that uses only colonoscopy outcomes recovers from drift, controls the FPR within groups and offers a high-confidence version." Add the honest qualifier: "...whereas at stable sites a label-free local quantile performs as well."
- "Excess false positives can come from severe disease through oral taxa, or from drugs such as metformin." Change "drugs such as metformin" to "possibly from metformin (one cohort)".
- Limitations: also name the small control sets, the pilot exposure of the 3 CRC sites, and the downward-drift failure.
- The final recommendation sentence is the best sentence in the conclusion. Keep it, and consider ending the paper on it.

### Figure 1
- **A:** Clear. Fix "13" to 11 (+2). Drop the line about the medication addendum, which belongs in the legend. The "Simulated deployments" box duplicates Figure 2. Consider removing it to free space for B.
- **B:** Add binomial CIs. Mark sites with fewer than 40 controls (for example with open grey markers). Put the IBD and T2D rows visually below a separator labelled "other disease classifiers", or move them to the SI (R1). The panel title "Specificity does not travel across sites" sits over an x-axis of false-positive rate. Use "False-positive rate at new sites" for consistency. The legend overlaps the IBD and T2D data region; move it outside.
- **C:** Eleven rows mix development, locked and post hoc results and three adjustment sets. Show only the fully adjusted estimate per condition, with the progressive adjustment in Table S9. Orange is used here for comorbid CRC controls and in D for oral taxa, while blue means "locked" in C and "depleted commensals" in D. Use distinct colour semantics across panels. Add ME/CFS (+0.39) or explain why it is omitted.
- **D:** Retitle "Two patterns of species contributions". "Drug-linked shifts" is inaccurate, because heart failure and T2D are disease labels. Give the absolute logit scale in a second axis or annotate the totals. State in the legend that the oral-taxa list was defined a priori (SI S5) and name its genera.

### Figure 2
- **A:** VP sits visibly below the 0.10 line (conservative). Add a sensitivity inset or a second row of sensitivity, or readers will read "below target" as "best". Make the site set match the text (0.17 vs 0.20). "(ours)" is informal for iMeta; use "Verified-positive (proposed)".
- **B:** Good and clear. This is the single most persuasive panel for the VP rule. Consider adding the downward-drift case as a mirror panel (Table S2c) for honesty.
- **C:** Say in the panel title that this is the CRC test applied to a cardiometabolic cohort ("CRC test at MetaCardis, by condition"). Add sensitivity per group (Table S5 Sens_proxy) and state where the cases come from.
- **D:** The prevalence-bounded rule (14%) must be discussed in the text. The y-axis label is long; use "Months with false-positive rate > 12%". Note that the two sites differ in disease (CRC vs T2D classifier), or replace MetaCardis with a CRC site (YuJ_2015 has 54 controls; or justify the 100-control rule).

### Graphical abstract
- It has no data graphic. iMeta graphical abstracts work best with one small visual: a mini Figure 1B dot plot plus a mini Figure 2B line.
- Remove "PPIs raise the oral component" (primary hypothesis failed). Remove "0-75% at 16 sites" (R1, R2). "AUROC hides both" is not shown by the data; drop it or support it.
- The arrows imply that the fix follows from the two routes, but recalibration does not use the mechanism. Replace the second arrow with a separator, or reorder as problem, fix, and why groups differ.

### Cover letter
- Remove "report honestly where each works". Show it instead, by reporting the Figure 2D result.
- Restate the headline consistently with the revised title (per disease, 11 independent sites).
- Add one sentence on why this fits iMeta, for example the microbiome-specific mechanism (oral taxa, metformin) plus an open tool.

---

## 4. Does the paper tell one clear story?

**Almost, but not yet.** It currently tells three stories: (i) a site-transport audit that mixes three diseases, (ii) a microbiome-mechanism story (oral taxa, metformin) and (iii) a statistics method. Each is supported to a different degree, and they are joined by "therefore". The paper becomes one story if it is framed as: *"A microbiome CRC test's specificity depends on where and whom it tests, and the cut-off must be reset locally. Colonoscopy results of test-positive people are enough to do this, even under drift and within patient groups."* The mechanism section then serves as the "whom" (why groups differ, and why groups must be monitored rather than predicted). It should not be presented as a separate discovery.

**The single most important sentence (as it should read):**
> "A cut-off set for 90% specificity on published cohorts gave false-positive rates above target at most new sites, and resetting it locally, using only colonoscopy results of people who test positive, restored the intended specificity."

The closest existing sentence is the first line of the Conclusion: "A microbiome CRC test does not keep its specificity when it moves to a new site or to a different patient mix." It states the problem but not the remedy, and it should appear, in this form, in the "Here, we" paragraph.
