# Referee report 3 (domain: gut-microbiome metagenomic diagnostics / CRC screening)

**Manuscript:** "Twenty local controls keep gut-microbiome diagnostic thresholds honest at new sites" (Short Communication, iMeta)
**Materials reviewed:** manuscript.md, supporting_information.md, si_tables.md, Figures 1–3 and S1, and `code/src/data.py` and `models.py`. I also tabulated the curatedMetagenomicData (cMD) sample metadata in the project's `data_cache/sampleMetadata.csv` to check how cohorts and labels were defined. No files were edited.

---

## Summary

The authors train LASSO and random-forest classifiers on MetaPhlAn3 species profiles from 19 cMD cohorts covering four tasks: CRC, IBD, T2D and adenoma. They set the decision threshold at 90% specificity on out-of-fold training controls and show that the realised false-positive rate (FPR) in held-out cohorts ranges from 0 to 0.73. Cohort-wise standardisation, Saerens EM prior correction, an unlabelled-pool quantile, a mixture model and median/IQR "anchoring" do not reliably restore the target FPR. A split-conformal order statistic computed on n = 10–20 labelled local controls brings cohort-mean FPR to 0.08–0.11. The authors convert the CRC results into unnecessary colonoscopies and missed cancers per 1,000 screened, and they recommend a go-live step of "20 colonoscopy-negative local controls".

The core observation is useful and under-reported in our field. AUROC transports better than operating points, and control-score shift between sites is real. The paper is clearly written, the development and test split is disclosed, and the per-cohort scores are released. My concerns are not mainly about the statistics. They are about what the cohorts can support biologically and clinically:

1. The label definitions are heterogeneous, and in some cohorts they are problematic. These definitions drive several of the headline FPRs.
2. Calibrating and evaluating on two random halves of the same case–control study makes the conformal result close to guaranteed by construction. It does not test the deployment scenario the paper recommends.
3. The "per 1,000 screened" numbers take FPRs from case–control controls and apply them to a screening population. They ignore adenoma carriers and other non-cancer findings, they are not compared with FIT, and the abstract misstates them.
4. In a real screening population with ~0.5% prevalence, the label-free pool quantile the authors dismiss would work almost exactly. That weakens the central recommendation.
5. The confounders behind the control-score shift (sequencing depth and platform, geography, age, BMI, metformin) are named but never examined, even though the metadata to do so are available.

---

## Major issues

### 1. Control and case definitions differ across cohorts, and this alone could explain several headline FPRs

The cMD metadata show:

- **MetaCardis_2020_a (T2D).** The 642 "controls" are 365 participants with metabolic syndrome, 234 healthy participants and 43 labelled IGT in the `disease` field. Their median BMI is 37 and their median age is 48. The 550 T2D cases have median age 62, and 74% have metformin recorded in `treatment`. Sequencing used Ion Proton, whereas every other cohort here used Illumina. "T2D vs control" in MetaCardis therefore means "T2D, mostly on metformin, older" versus "obese or metabolic-syndrome, younger, mostly untreated". This is a different contrast from the other three T2D cohorts.
- **IGT handling is inconsistent.** In KarlssonFH_2013, IGT participants are excluded by the `study_condition` filter. In MetaCardis, 43 IGT participants sit inside `control`.
- **KarlssonFH_2013** includes only 70-year-old Swedish women. **QinJ_2012** controls are Chinese, with median age 42 and BMI 23.7. **SankaranarayananK_2015** is a small Native American cohort. The FPR of 0.59–0.73 in Qin and the near-zero FPR in Karlsson are what you would expect from these age, ethnicity and geography contrasts, and from a metformin-loaded training signal (Forslund et al. 2015). They are not evidence of a generic "site" effect.
- **HMP_2019_ibdmdb.** The 27 "controls" are HMP2 non-IBD participants. These are people referred for GI symptoms who did not receive an IBD diagnosis, not healthy volunteers. An FPR of 0.41 in symptomatic non-IBD patients is biologically plausible and clinically important. It is the population in which an IBD stool test would actually be used. Calling it "drift" undersells the point. IBD also pools Crohn's disease and ulcerative colitis, and choosing each subject's first sample picks an arbitrary disease activity and treatment state.
- **NielsenHB_2014.** Only the 59 Spanish controls carry the control label. Some subjects contributed repeat samples (71 control samples from 59 subjects), so the first-sample rule matters here too.
- **YachidaS_2019.** The 258 CRC cases include stage 0 (intramucosal) cancers. The 251 controls include 5 participants with "few polyps". The adenoma arm (67) consists of multiple polypoid adenomas. Zeller, Feng, Hannigan and Thomas 2018a each define adenoma or advanced adenoma differently.

**Fix.**
- Add a per-cohort table listing control definition (healthy volunteer, colonoscopy-negative, symptomatic non-disease, metabolic-disease non-T2D), case definition and subtype, country, sequencing platform, median read depth, age, sex, BMI, and medication where available.
- Re-run T2D with MetaCardis restricted to `disease == healthy` controls, and add a metformin-stratified analysis: metformin-naive T2D versus controls.
- Make IGT handling consistent.
- Report IBD separately for CD and UC, or at least check that the conclusions hold for each.
- Interpret HMP2 explicitly as a symptomatic-control spectrum.

### 2. The conformal success is close to tautological: calibration and evaluation controls come from the same study, batch and recruitment

The local controls and the evaluation controls are two random halves of the same cohort's controls. They share the same recruitment, the same exclusion criteria, the same extraction kit, the same sequencing run or platform, and the same time window. Exchangeability, the one assumption the conformal rule needs, therefore holds by design. "20 of 20 pairs in band" mostly confirms a known theorem.

The deployment the paper recommends looks different. A laboratory recruits 20 colonoscopy-negative volunteers before go-live, then applies the threshold to a screening population over months or years. In that setting, exchangeability is threatened by:

- **Spectrum.** Colonoscopy-negative volunteers are not the screening population's non-cancer members, who include adenoma carriers, diverticular disease, haemorrhoids, IBD and recent antibiotic or PPI users.
- **Demography.** Age and sex mix differ between a small volunteer set and the screened population.
- **Medication.** Metformin, PPIs and antibiotics all shift stool profiles.
- **Bowel preparation.** If stool is collected after bowel preparation, the profile is perturbed for weeks.
- **Temporal drift.** Extraction kit lots, library preparation and sequencer or chemistry changes accumulate over time.

**Fix.**
- Evaluate the rule across studies wherever the data allow:
  - Calibrate on one cohort's controls and evaluate on another cohort from the same country or protocol. Possible pairs are ThomasAM_2019_c versus YachidaS_2019 (both Japan), and ThomasAM_2018a versus ThomasAM_2018b (both Italy).
  - Calibrate on colonoscopy-negative controls and evaluate on a mixture that includes adenoma carriers from the same cohort (see Issue 3).
  - Calibrate on controls from one sequencing batch or time period and evaluate on another. HMP2, MetaCardis country centres and Yachida all have usable structure for this.
- Present the within-cohort result as a best case. State plainly that it does not test robustness to spectrum, demographic or temporal shift.

### 3. The "per 1,000 screened" figures are not supported by case–control cohorts and are misreported

Three problems:

- **Who the false positives are.** In a screening population aged 50–75, roughly 25–40% of people without CRC have adenomas, and 5–10% have advanced adenomas. Your own adenoma task shows that adenoma carriers score above controls (AUROC 0.55–0.65). A threshold calibrated on polyp-free controls will therefore produce more than 10% positives among the non-cancer screened population. A colonoscopy that finds an advanced adenoma is also not "unnecessary". The harm metric needs a three-way split: CRC, advanced neoplasia, and no neoplasia.
- **The comparator is missing.** At its usual cut-offs (10–20 µg Hb/g), FIT has ~5–8% positivity and ~70–80% sensitivity for CRC. The status quo here is a microbiome test with 11–28% FPR and, after recalibration, about 99 positives per 1,000 with sensitivity ~0.33–0.70 (Figure 3A). That performance is clearly inferior to FIT. The paper should say so, and it should frame the plausible clinical role as an adjunct to FIT (Zeller 2014; Wirbel 2019) or as a triage test for FIT-positive patients. In a FIT-positive population, prevalence is ~3–5% and the controls are FIT-positive patients without cancer, so the threshold would need to be calibrated within that population, not on colonoscopy-negative volunteers.
- **The abstract misstates the trade-off.** It says "at a cost of up to one more missed cancer". Figure 3A shows ThomasAM_2019_c going from ~1.4 to ~3.35 missed cancers per 1,000, an increase of ~2. The text reports 1.3–2.3 rising to 1.5–3.3, which is consistent with Figure 3A and not with the abstract. The large "181 fewer colonoscopies" figure also comes from ThomasAM_2019_c, which has 40 controls, so each split's FPR is estimated on only 20 evaluation controls. No intervals are given.

**Fix.**
- Correct the abstract.
- Add uncertainty intervals to every per-1,000 figure.
- Recompute harm for a screening-like mixture of non-cancer participants (for example, normal / non-advanced adenoma / advanced adenoma in published screening proportions), using cohorts that sampled adenomas: Yachida, Zeller, Feng, Thomas 2018a.
- Add a FIT benchmark line to Figure 3A.
- State that per-1,000 numbers derived from case–control studies are illustrative, not estimates for a screening programme.

### 4. In the screening setting the paper targets, the dismissed label-free pool quantile is nearly exact and needs no colonoscopies

The SI itself shows that the pool-quantile FPR lies between (β − π)/(1 − π) and β/(1 − π). At π = 0.005 this pins the FPR to within about half a percentage point of the target. The method failed in this paper only because the case–control cohorts are ~50% cases. Real CRC screening programmes already manage FIT cut-offs this way: they monitor positivity rate and colonoscopy capacity on the unlabelled screened population. FIT positivity varies across programmes and analysers for the same reasons microbiome thresholds do.

The relevant label-free target is "positivity rate", not FPR among neoplasia-free people. Even so, for capacity planning, which the paper gives as its own rationale, positivity rate is exactly what a programme needs.

**Fix.**
- Simulate realistic prevalence by subsampling cases in each cohort to 0.5–5% and re-evaluate `pool_q`, `em` and `site_shift` against conformal.
- Discuss a pilot-phase positivity-rate calibration as the realistic alternative to recruiting colonoscopy-confirmed controls.
- Soften recommendation (iii) to "label-free corrections fail at case–control prevalence".
- Reserve the labelled-control recommendation for settings with high prevalence, or with no unlabelled pilot data, such as symptomatic referral clinics.

### 5. The confounders behind the control-score shift are listed but not analysed

The post-hoc finding that the shift in median control score explains the FPR ranking (ρ = 0.80) is close to definitional. What the field needs to know is what drives the shift. cMD provides `number_reads`, `sequencing_platform`, `country`, `age`, `gender`, `BMI`, `antibiotics_current_use` and, for MetaCardis, `treatment`. The ranges are large:

- **Read depth.** Median depth in controls runs from 6.7 M (HanniganGD_2017) and 9.3 M (GuptaA_2019) to 99 M (ThomasAM_2018a). MetaPhlAn detection of low-abundance species, and hence the zero pattern under the log(x + 10⁻⁵) transform, depends strongly on depth.
- **Platform.** MetaCardis was sequenced on Ion Proton.
- **Geography.** Two of the three external CRC cohorts are Japanese and one is Chinese. The CRC training set is mostly European and North American, plus India. "Drift" in CRC is therefore partly a West-to-East-Asia transfer. Please also confirm that ThomasAM_2019_c and YachidaS_2019 do not share subjects.
- **Age and BMI.** See Issue 1.

**Fix.**
- Regress control scores, or per-cohort control-score shifts, on depth, platform, country, age, sex and BMI.
- Repeat the main analysis after rarefying or subsampling reads to a common depth, or at minimum after restricting to cohorts with ≥ 20 M reads.
- Report whether drift persists within a single country or platform.

Even a short supplementary analysis would turn a descriptive claim into a mechanistic one. Extraction protocol is not in cMD, but it can be compiled from the original papers.

### 6. Batch-correction and pipeline comparisons are too narrow to support "batch correction does not restore the operating point"

The only batch-correction method tested is per-cohort z-scoring of log abundances, which is a crude location–scale adjustment. The general conclusion (iii) is not supported. A microbiome reviewer would expect:

- **MMUPHin** (Ma et al. 2022), run with the target cohort included in label-free mode.
- **ConQuR** (Ling et al. 2022), with a reference batch.
- **DEBIAS-M** (Austin et al. 2025). It is designed for exactly this cross-study use, can use unlabelled test samples, and the authors themselves name it as a gap.
- **Percentile normalisation** (Gibbons et al. 2018, which the paper cites as ref. 14). This method normalises each study to its own controls, so it uses the same labelled local controls as the conformal rule. It is the natural feature-level competitor and should be compared directly.
- **A SIAMCAT-style pipeline**: log.std normalisation, LASSO or elastic net with cross-validated λ, and SIAMCAT's own cross-study threshold reporting. This would show the drift is not a by-product of the untuned C = 0.1 and the specific prevalence filter.
- **At least one boosting model** (for example, XGBoost or LightGBM), and ideally a second profiler. mOTUs was used by Wirbel 2019; MetaPhlAn4 SGB-level profiles are available in newer cMD releases.

**Fix.** Add at least MMUPHin, DEBIAS-M or ConQuR, percentile normalisation and a SIAMCAT pipeline, or restrict the claim to "simple per-cohort standardisation".

### 7. The analogy to reference intervals is misapplied, and the 20-control protocol is under-specified

In laboratory medicine, about 20 local samples are used to verify a transferred reference interval: the interval passes if ≤ 2 of 20 fall outside it (CLSI EP28-A3c). Establishing a new interval needs about 120. The proposed rule does not verify the transferred threshold. It re-estimates a new tail quantile from the second-highest of 20 values, and the authors' own data show the realised FPR exceeds 0.15 in ~19% of such deployments.

Practical points a screening programme would need:

- Stool must be collected before bowel preparation.
- "Normal colonoscopy" must be defined (polyp-free? no advanced neoplasia? how recent?).
- Age and sex matching to the screened population.
- Medication exclusions.
- Repeat calibration after any change of kit, extraction or sequencer.
- How to monitor drift when, in screening, only test-positive people receive colonoscopy and the negatives remain unverified.

Recommendation (ii) also says "≥ 30 for a 95% guarantee". At n = 30 the realised FPR was ~0.03 and sensitivity fell to 0.08 (Figure 3B, Table S3a). That makes the test clinically useless, and the paper should say so rather than recommend it.

**Fix.**
- Reframe the protocol: 20 controls is a minimum for a mean-FPR guarantee, it carries a ~1-in-5 chance of exceeding 1.5α, and verification-style use (testing the transferred threshold, and recalibrating only on failure) is an alternative worth evaluating.
- Spell out the practical requirements listed above.
- Remove or qualify the "≥ 30" recommendation.

### 8. Clinical relevance differs by task and should be stated

- **T2D** is diagnosed by HbA1c or glucose, so a stool T2D classifier has no screening use case. The AUROC of 0.58–0.69 here mostly reflects metformin and BMI.
- **Adenoma** classifiers with AUROC 0.54–0.65 are near chance. Their threshold behaviour says little about clinical deployment.
- **IBD** testing in practice is triage of symptomatic patients, where faecal calprotectin is the comparator.

The success criterion is also met mainly because of the CRC, T2D and adenoma cohorts. Only one IBD cohort (NielsenHB, 59 Spanish controls) is evaluable at n = 20, and the most-drifted IBD cohort (HMP2) cannot be evaluated at all.

**Fix.**
- Present T2D and adenoma explicitly as methodological stress tests.
- Discuss calprotectin for IBD.
- Make clear that the feasibility restriction (≥ 40 controls) removes most small or atypical cohorts from the conformal evaluation, and say how that biases the conformal success rate.

### 9. Novelty relative to existing cross-cohort CRC work should be stated more carefully

Wirbel et al. 2019, together with the SIAMCAT framework, already set cut-offs at a fixed training FPR (10%). They examined false-positive rates of CRC models in external control cohorts and in non-CRC disease cohorts at that cut-off. Thomas et al. 2019 and CRC-TrustBench (ref. 9) also report cross-cohort operating-point behaviour. "Rarely reported" is fair. The paper should still cite these specific analyses and say what is new: the systematic quantification, the comparison of methods, and the local-control rule.

There is also a related design point. The pilot touched all 11 CRC cohorts, including the three "locked" external ones. The adenoma task reuses control samples from four development cohorts and from the locked YachidaS_2019 cohort. The SI discloses this, but the main text should not describe the external CRC cohorts as "locked away during method design" without that qualification.

---

## Minor issues

1. **Abstract wording.** "Kept every cohort within 0.08–0.11" refers to cohort means. It should say so, and it should give the 19% single-deployment exceedance alongside it.
2. **First-sample rule.** `data.py` fills missing `days_from_first_collection` with 0. State how often this happens and how ties are broken. For HMP2, report the disease activity and treatment of the selected first samples.
3. **Antibiotic exclusions.** `antibiotics_current_use` is available but unused. State whether current antibiotic users were excluded, or test sensitivity to excluding them.
4. **Prevalence assumption.** 0.5% CRC prevalence suits a screening colonoscopy population aged 50–75. Give a source, and show the 1% sensitivity analysis in the main text or the SI, not only in the Methods.
5. **Missing numbers.** Give the per-cohort sensitivity and FPR at the conformal threshold in a table (currently only figures and pooled means). Also give the realised positivity rate, which a programme would actually observe.
6. **Figure 1.** Add cohort country and n controls to the row labels, and mark the cohorts excluded from conformal evaluation (for example HMP2) so readers do not read the missing diamond as success.
7. **Figure 3A.** Add intervals, the FIT reference, and axis annotations stating that the cohorts are case–control.
8. **Feature transform.** The log10(x/100 + 10⁻⁵) transform with a prevalence filter applied to the training set means the target-cohort zero structure, which is depth-dependent, enters directly. Mention this when discussing mechanisms.
9. **Metadata release.** MetaCardis comes from a later cMD release (2022-10-19) than the other cohorts. Confirm that the MetaPhlAn version and database are identical across releases.
10. **Over-dispersion P-values.** P = 10⁻¹⁷⁷ is driven by MetaCardis and Qin, which have large n. Such extreme P-values add little; effect sizes (FPR ranges) are more informative.
11. **"The drift is therefore a property of the site".** Concordance between LASSO and RF trained on the same features shows the drift is a property of the data, not of the site as an institution. Population, protocol and label definition are confounded with site.

---

## Recommendation

**Major revision.**

The central message, that cross-cohort AUROC hides operating-point failure and that control-score shift is the mechanism, is valuable and worth publishing in a short format. In its current form, however, the paper:

- draws clinical conclusions (per-1,000-screened harms, a 20-control go-live protocol, "batch correction does not work") that the case–control, within-cohort design cannot support;
- leaves the label-definition and confounding problems unexamined, most clearly MetaCardis controls, HMP2 symptomatic controls, metformin, read depth and East Asian external cohorts;
- misstates the missed-cancer trade-off in the abstract.

A revision that analyses the confounders, tests calibration across studies and under a realistic screening spectrum and prevalence (including the pool quantile), benchmarks against FIT and stronger batch-correction pipelines, and tones down the screening claims would make this a solid contribution.
