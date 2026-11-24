# Handling editor screening report: iMeta Letter (round 3, read cold)

**Manuscript:** "Microbiome colorectal cancer tests lose specificity at new sites; local recalibration restores it"
**Files screened:** submission_package/Manuscript.md; manuscript/SI_methods.md; manuscript/SI_tables.md; manuscript/cover_letter.md; code/figures/out/Figure1.png, Figure2.png, Graphical_Abstract.png. style_notes.md was used for context only.
**Format check:** The main text runs about 1,830 words from "To the Editor" to the end of the Conclusion, within the 1,500–3,000 limit. There are 2 figures, 19 references, a graphical abstract and a summary of 100 words or fewer, and no Highlights. Headings follow the iMeta Letter pattern. Format passes. Author placeholders were treated as filled.

---

## 1. Decision

**Send to review, narrowly. Probability of being sent to review as submitted: about 50% (range 45–55%).**

Strengths an iMeta editor will value:
- The question is a real deployment problem, framed as specificity at one fixed cut-off rather than AUROC.
- Only public curatedMetagenomicData cohorts are used.
- The protocol was frozen before the analysis and the freeze is time-stamped.
- Null results are reported, including the pre-specified PPI hypothesis.
- Post hoc analyses are labelled throughout.
- There is a released package (cutoffguard).
- There is a microbial explanation (oral-origin CRC marker taxa, and possibly metformin) rather than a purely statistical argument.

Most submissions in this area show none of this care.

Why it is not a clear send-out:
1. **The paper tells three stories in 1,800 words.** These are a site audit, a comorbidity and mechanism analysis, and a new recalibration rule. They are dense with numbers and none is developed fully. A busy board member will read the abstract and Figure 2 and ask what the one take-home is.
2. **The second half of the title rests largely on post hoc or non-significant evidence.** The CRC-site deployment (Figure 2A) is post hoc. The pre-specified primary comparison pools IBD, T2D and adenoma classifiers, where colonoscopy verification does not apply. At sites with at least 40 controls, the proposed rule no longer beats the source cut-off (p = 0.074). In the most realistic analysis (Figure 2D, country-by-country shift), the status-quo source cut-off exceeded 12% in 1% of months, and every local rule did worse (12–34%).
3. **The clinical trade-off is not argued.** The verified-positive rule avoids 83 false-positive referrals per 1,000 screened but misses 1.1 more cancers per 1,000. That is about 75 avoided colonoscopies per missed cancer, and many screening programmes would not accept that. The text presents specificity as the goal without saying why.

If R1–R3 below are fixed, I would put the probability at 65–70%.

---

## 2. Remaining desk-rejection risks (most important first), each with a feasible fix

### R1. The title's "local recalibration restores it" is stronger than the evidence
- Figure 2A (11 CRC sites) is post hoc. The pre-specified primary analysis (16 held-out sites) is significant overall (p = 0.011), but it is not significant separately for IBD, T2D or adenoma. Per cohort at sites with at least 40 controls it is also not significant against the source cut-off (p = 0.074, Table S2d).
- In Figure 2D (no resampling), local rules still exceed 12% in 15–27% of months. The high-confidence versions are post hoc code additions (SI S7c). Under the real country shift at MetaCardis, the source cut-off is the best performer (share above 12% = 0.001, Table S10). The text does not mention this, and a reviewer reading Figure 2D will see it at once.
- The verified-positive rule reaches its 0.3% exceedance by running below target (mean FPR 0.083), so part of the "restoration" is simply conservatism.

**Fix (text plus existing outputs):**
(a) Retitle to what is shown. For example: *"Stool microbiome colorectal cancer tests lose specificity at new sites and in some patient groups"*, with the recalibration as the second clause in softer form ("...and local recalibration can recover it").
(b) In the recalibration section, report the pre-specified result first, the CRC-only result second (labelled post hoc), and the per-cohort result for sites with at least 40 controls third.
(c) Add one sentence on Figure 2D: "Under the country-by-country shift at MetaCardis, the source cut-off happened to be too strict (FPR 0.04), so it rarely exceeded the target; local rules move the FPR towards 10% from either side." This turns an apparent failure into the correct reading: local rules target 10%, not "low".
(d) Report the FPR **and sensitivity** of the high-confidence options in the main text (FPR 0.06–0.07; sensitivity from Table S10/S2), so readers can see their cost.

### R2. The clinical value of fixing specificity is asserted, not shown
- The headline benefit is fewer false-positive referrals. The locked CRC numbers show a sensitivity loss from 0.64 to 0.52. Without a net-benefit framing, a clinical-microbiome reviewer will argue that recalibration makes the test worse.
- A sensitivity of 0.50 at 90% specificity is well below FIT. The paper should say in one sentence why this matters anyway: microbiome tests may be used together with FIT, cut-offs are being fixed now in product development, and the problem generalises to any microbiome classifier.

**Fix (existing simulation output):** Add a two-row summary to Figure 2 or Table S2: unnecessary colonoscopies avoided and cancers missed per 1,000 screened, for each rule. Add the net benefit at one or two exchange rates, for example 1 missed cancer counted as 20 or 50 unnecessary colonoscopies. Then state plainly that the rules **keep the specificity a programme has chosen**. Whether 90% is the right target is a policy choice, and the package lets a site choose alpha. All of this can be computed from the per-month FPR and sensitivity already stored.

### R3. "New sites" and "locked" are weaker than the framing implies
- 8 of the 11 "new CRC sites" are development cohorts evaluated leave-one-cohort-out. The pilot had already seen the source-cut-off FPR at all 11, including the 3 locked CRC sites (disclosed in SI S1 and in the "Here, we" paragraph). So the headline "0% to 37%" result is not a blinded locked result. The sentence "Because the audit evaluates a fixed cut-off and involves no method choice, development cohorts are valid audit sites" is defensive and will draw exactly the objection it tries to prevent.
- At several sites the classifier matters as much as the site. At Gupta 2019, the LASSO FPR is 0.37 and the random-forest FPR is 0.00 (Figure 1B). In the development cohorts, random forest is on target on average (mean FPR 0.089, Table S7), and LASSO is liberal (0.16). "Specificity does not travel" therefore partly means that the LASSO cut-off is systematically liberal. That is a different point.
- The overdispersion statistic (χ² = 102 on 11 df) and the between-site SD (0.58–0.65) are not tabulated anywhere in the SI that I could find. The single χ² for two classifiers is ambiguous: which model, or are they pooled?

**Fix:**
(a) Call them "11 held-out CRC cohorts (8 by leave-one-cohort-out, 3 external)" in the title and abstract wording, and drop the defensive sentence.
(b) Add a small SI table with the overdispersion χ², df, p and the random-effects between-site SD of logit FPR (with CI), **per classifier**. Also report the mean FPR per classifier (systematic shift) separately from the spread. It is computed from data already in hand.
(c) Report the locked-only range in one clause (3 sites: 0.11–0.28) so readers see that every locked CRC site-model pair was at or above target.

### R4. The mechanism section mixes adjustment sets and overstates replication
- Figure 1C places development effects (adjusted for age, BMI and sex) next to MetaCardis effects (adjusted for sex, country and five drugs, post hoc). The text first quotes the sex-only MetaCardis estimates (+0.33, +0.35) and then the adjusted ones, while Figure 1D decomposes the **unadjusted** gaps (T2D about 0.37 in 1D vs +0.11 in 1C). A reader comparing the panels sees three different "T2D effects".
- "A smaller cohort showed the same direction" for metformin refers to LiJ_2014. The LASSO estimate is +0.40 and not significant (p = 0.18), and the random-forest **positivity** goes the other way (15.5% vs 23.8%, Table S6d). This is not replication.
- ME/CFS has a clearly positive effect in Figure 1C (about +0.39, CI excludes 0), but the text does not mention it.
- Comorbid controls inside CRC cohorts were flagged *less* often (4% vs 16%; random-forest OR 0.10, p = 0.04). "Not flagged more often" understates an odd result, which probably reflects which cohorts recorded comorbidity. Say so.
- Section 2 ends with "cannot be fully predicted in advance", and Section 3 then recommends per-group recalibration within *recorded* groups. Reconcile the two: per-group recalibration covers groups you can record (diagnoses, drugs), and the site-level audit catches the rest.

**Fix:** In Figure 1D, decompose the **same adjusted contrast** shown in 1C, or label 1D "unadjusted gap" and give the unadjusted value beside each bar. Change "same direction" to "a directionally similar but non-significant LASSO estimate in one smaller cohort and no effect in two others". Add ME/CFS to the sentence on effects. All of this uses existing tables.

### R5. Disease scope of the simulations
- Figure 2B pools "locked CRC, IBD and T2D sites" for a rule motivated by colonoscopy verification. Figure 2D uses MetaCardis and Qin 2012 **with the T2D classifier**, while Figure 2C uses MetaCardis **with the CRC classifier**. The same cohort plays two roles in one figure.
- In real screening, colonoscopy-negative "controls" exclude people with adenomas, but a screening population includes 5–10% adenoma carriers whose scores are raised. The prevalence bound needs to account for them, and the paper does not discuss this.

**Fix:** Restrict 2B and 2D to CRC sites (the drift and no-resampling runs exist for Yachida; add YuJ_2015 and ThomasAM_2019_c with the existing scripts) and move the non-CRC runs to the SI. Run the existing adenoma settings (pi = 0.10 or 0.30, already in Table S2) as "adenoma carriers among test-negatives" and add one sentence on the pi_max needed in a real screening population.

### R6. Small consistency and reference items that reviewers will catch
- The Data Availability statement lists three curatedMetagenomicData releases (2021-03-31, 2022-04-13, 2022-10-19); SI S1 names two. Make them match.
- Figure 1A says "3 CRC + 13 other sites". Five of the 13 are adenoma comparisons from development CRC cohorts, so "other sites" misleads.
- Ref. 14 cites a PMLR volume with an arXiv DOI: give the PMLR URL. Ref. 18 (Biometrics 2026;82:ujag138) should be checked against the published record before submission. SI ref. S5 duplicates the topic of main ref. 17 (Godau): remove one or explain why both are cited.
- "months 10–12: 0.086 vs 0.154" for a drift run plotted to month 18 (Figure 2B). Say why months 10–12 were chosen, or use 13–18.

---

## 3. Clarity: the five hardest sentences for a microbiome reader, with rewrites

1. **Original:** "Methods and endpoints were fixed in a protocol, frozen in a time-stamped commit before the held-out sites were analysed once; a pilot before the data lock had evaluated the source cut-off at all 11 CRC cohorts, including the three later held-out CRC sites."
   **Rewrite:** "We fixed the methods and endpoints in a protocol before analysing the held-out cohorts, and analysed them once. An earlier pilot had already measured the false-positive rate at all 11 CRC cohorts, so this part of the audit was not blinded."

2. **Original:** "The spread was far beyond sampling noise (overdispersion χ² = 102 on 11 df, p < 10^−15^; between-site SD of the logit FPR 0.58–0.65)."
   **Rewrite:** "The differences between sites were far larger than chance alone would produce with these control numbers (p < 10^−15^; Table Sx)." Move the χ² and the logit SD to the SI.

3. **Original:** "The verified-positive rule counts confirmed false positives above each candidate cut-off, treats everyone not yet confirmed as a possible false positive, and picks the lowest cut-off whose worst-case FPR is at or below the target."
   **Rewrite:** "Each month, the rule looks at the people who scored above a candidate cut-off. It counts those whose colonoscopy was negative, and conservatively also everyone whose result is not yet known, as false positives. It then chooses the lowest cut-off at which this pessimistic false-positive rate is still 10% or less."

4. **Original:** "If controls at a site are exchangeable and prevalence stays below the bound, the expected FPR is at most the target, whatever the referral, attendance or delay (Proposition S1)."
   **Rewrite:** "Provided the site's population does not change within the update window and cancer prevalence stays below the assumed maximum, the rule keeps the average false-positive rate at or below 10%, however referral, attendance or reporting delays behave (proof in Proposition S1)."

5. **Original:** "Its advantage over the prevalence-bounded quantile (p = 0.049) came from sites with few controls: at the nine cohorts with at least 40 controls (post hoc), the two rules were equivalent (FPR 0.090 vs 0.083; p = 0.72), and even the comparison with the source cut-off was no longer significant (p = 0.074), because the source cut-off was too strict at some large sites."
   **Rewrite:** "At the nine cohorts with at least 40 controls (post hoc), the two local rules performed alike (FPR 0.090 vs 0.083). Neither was significantly better than the source cut-off there (p = 0.074), because at some large sites the source cut-off was too strict rather than too lenient. The verified-positive rule's advantage came from small sites."

**Jargon to remove or define once in plain words:**
- **"exchangeable"**: remove from the main text and replace it with the plain-language condition above.
- **"apple tasting" / "online learning"**: remove. It adds nothing for microbiome readers. Keep the verification-bias citation.
- **"Neyman–Pearson rules", "outlier tests on contaminated reference data"**: reduce to "related statistical methods require labelled local controls or a model of the shift [17–19]".
- **"overdispersion", "logit FPR", "between-site SD"**: move to the SI.
- **"source cut-off", "prevalence-bounded quantile", "verified-positive recalibration"**: define once with an intuitive phrase. For example: "fixed cut-off", "local cut-off allowing for up to x% cancers", "colonoscopy-feedback cut-off". Use exactly these names in the text, figures and GA. At present the GA says "label-free" and "colonoscopy feedback", while the text and figures say "prevalence-bounded quantile" and "verified-positive".
- **"site-months", "δ = 0.10", "high-confidence version"**: say "a stricter version that keeps most single months on target".
- **"post hoc"** appears many times. Group post hoc analyses in one sentence per section instead of tagging each clause.

---

## 4. Novelty and significance for iMeta

**Is it clear?** Only partly. Readers already know that CRC microbiome signatures fire in other diseases (Wirbel 2021; Thomas 2019) and that oral taxa drive CRC signatures (Thomas 2019; Schmidt 2019). The genuinely new contributions are:
- quantifying the *specificity at a fixed cut-off* across sites, with the finding that most cut-offs are too lenient;
- the possible metformin route, which is exploratory;
- a recalibration rule with a guarantee that uses only colonoscopy results of test-positives, released as software.

The cover letter says this better than the manuscript does. For iMeta, the weak point is that the site-level failure, which is the headline, has **no microbial explanation**. The microbiome biology (oral taxa, metformin) explains the *patient-group* excess, not why Gupta, Zeller or Thomas 2019c over-flag. The paper therefore reads as a statistics or diagnostics paper with a microbiome appendix.

**The one change that would most raise it:** **explain the between-site spread microbially.** Regress each site's control FPR (11 CRC sites × 2 classifiers, optionally the IBD and T2D sites too) on properties of that site's **control** microbiomes that are available from curatedMetagenomicData:
- the summed abundance of oral-origin taxa in controls (using the same a priori genus list as Methods S5);
- alpha diversity;
- sequencing depth (number_reads);
- the DNA extraction kit and sequencing platform where recorded;
- country.

Pair this with the species decomposition already used in Figure 1D, applied to *site* gaps (site controls vs pooled source controls). If oral-taxon load or depth in controls predicts the site FPR, the paper gains:
- one mechanism linking Sections 1 and 2;
- an *a priori* warning a new site can check before deployment from unlabelled samples;
- a natural new function for cutoffguard ("audit" that flags at-risk sites).

This uses public data and the existing decomposition code, and could replace Figure 1C or be added as Figure 1E. Even a null result ("site FPR is not explained by depth or oral load, so local recalibration is unavoidable") strengthens the argument for recalibration.

---

## 5. Figure-by-figure

### Figure 1
- **A (design):** Text-heavy boxes with small font, and box text touching the borders ("+ 2 medication cohorts", "3 CRC + 13 other sites;"). It does not show which analyses are pre-specified and which are post hoc, which is the key to reading the rest of the paper. "13 other sites" misleads (see R6). Either shrink it to a 3-box flow with a "pre-specified / post hoc" colour key or move it to the GA.
- **B (site FPR):** This is the best panel. Remaining problems:
  - Development (dark grey) and locked (black) markers are almost indistinguishable at print size. Use colour, or a separate block for the three locked sites.
  - The legend shows grey markers but not the development/locked encoding.
  - Paired LASSO and random-forest markers overlap at several sites (Wirbel, Thomas 2018b, Hannigan).
  - The x-axis runs to 0.6 when the maximum CI is about 0.56. That is fine, but shade the zone where the CI is consistent with 0.10, or annotate how many sites exclude 10%, so the "4–5 sites" claim is visible.
  - Consider writing the "n = controls" labels as "(n = 30 controls)".
- **C (over-flagged groups):** The in-plot labels "development (open)" and "locked / CRC cohorts (filled)" overlap data: the first sits on the schizophrenia CI and the second on the heart-failure row. It mixes three adjustment sets on one axis (see R4). Put the adjustment in the row label or use subpanel headers. The diamond row ("Comorbid controls in CRC cohorts") is a different contrast (comorbid vs healthy controls), so separate it with a gap and label it. ME/CFS is shown but not discussed in the text.
- **D (decomposition):**
  - Bar totals do not match the effects in C (T2D about 0.37 in D vs 0.11 in C; heart failure 0.32 vs 0.28) because D is unadjusted. Label it, or decompose the adjusted contrast.
  - The legend sits below the panel, far from the bars.
  - "Other taxa (e.g. Enterobacterales)": say whether Enterobacterales is in fact the main contributor, or drop the example.
  - Small negative segments (blue for atherosclerotic CVD, orange for metformin) are hard to read. Add the net total as a marker on each bar.

### Figure 2
- **A (CRC deployments):**
  - The lower sensitivity sub-panel carries an "oracle" label with no matching line in the legend, and it is unclear which line is the oracle.
  - The 10–90% band is shown only for the proposed rule, which visually favours it. Show bands for all rules or none.
  - Burn-in month 1 (VP FPR 0.25) dominates the y-range; begin the axis at month 2 or annotate the value.
  - The panel title says "(8 development, 3 locked)" but not "post hoc", which the legend text requires.
- **B (drift):** It pools CRC, IBD and T2D classifiers (see R5). The baseline source FPR (0.20) differs from 2A (0.14) without explanation. The title "only the drift alarm recovers" is fair, but the proposed rule again sits clearly below target (about 0.08), and this should be acknowledged. The y-axis reaching 0.5 wastes space.
- **C (MetaCardis by condition):** This is a clear panel. It needs the sensitivity cost of per-group recalibration (Table S5: heart failure 0.36 vs pooled 0.45), otherwise the panel shows only benefit. The x-axis category "No condition" should read "Controls". State "LASSO, CRC test" in the panel itself.
- **D (no resampling):** This is the most overloaded panel.
  - The legend swatches are grey (dark = random order, light = country order), but the bars are coloured by rule, and the hatch meaning (high-confidence, post hoc) is absent from the legend.
  - The tick labels are abbreviated and cramped ("Prev.-b. high-conf.", "Verified-p. high-conf.").
  - The source bar under the country shift (about 0.01) is the lowest in the panel and unexplained (see R1).
  - The panel mixes the CRC test (Yachida) with the T2D test (MetaCardis, Qin).
  - **Fix:** restrict it to CRC or split it by test, put rule names on a horizontal axis with a separate hatch key, and add mean FPR above each bar so a reader can see that low exceedance comes from strictness.

### Graphical abstract
It is text only, with no visual element. iMeta GAs are normally illustrative. "χ² p < 10⁻¹⁵" is jargon for a GA. The rule names ("label-free", "colonoscopy feedback") differ from the figure names. "Local recalibration ... restores specificity" repeats the overclaim in R1. **Fix:** replace box 1 with a miniature of Figure 1B (dots against the 10% line), box 2 with a gut icon carrying oral-taxa and pill symbols, and box 3 with a miniature FPR-over-time line. Use the same rule names as the figures and drop the p-value.

### Consistency between text and figures (checked)
- 6 of 11 sites above 0.12 for each classifier: matches Figure 1B.
- 78–83% oral share: matches 1D.
- Figure 2C values (heart failure 0.21, T2D 0.14 pooled; 0.08–0.09 per group): match Table S5.
- Figure 2D values (15%, 18%; high-confidence 3–5% and 12–17%): match.
- Metformin 20.5% vs 8.5%: matches Table S6d.
- Not traceable in the SI: the overdispersion χ² and the between-site SD.
