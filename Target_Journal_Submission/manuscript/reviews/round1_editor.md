# iMeta — Handling-editor desk screen, Round 1

**Manuscript:** "Gut microbiome cancer tests over-flag people with chronic disease, and routine colonoscopy outcomes can keep their false alarms on target" (Letter)
**Files screened:** submission_package/Manuscript.md; manuscript/SI_methods.md; manuscript/SI_tables.md; Figure1.png, Figure2.png, Graphical_Abstract.png; journal_selection/style_notes.md and benchmark_raw_notes.md
**Date:** 2026-11-24

---

## 1. Decision

**Desk reject in current form. Resubmission welcome after major revision.**

**Estimated probability of being sent to review as it stands: about 15%.**

The question fits iMeta's scope: microbiome machine learning and how it would be deployed. The work is careful in places: a frozen protocol, a locked test set, a pre-specified addendum, honest reporting of null results, and code. My main objection is not rigor. The manuscript reads as three half-papers squeezed into one Letter:
1. a site-transfer audit;
2. a cross-disease specificity and medication analysis;
3. a statistical recalibration rule with a proof and a simulation.

Two of the three are partly known. Wirbel et al. 2021 (ref 11) and Thomas et al. 2019 (ref 3) already showed that CRC signatures fire in other diseases. The fact that thresholds do not transfer between settings is textbook clinical epidemiology. The genuinely new part, the verified-positive rule, is a statistics or screening contribution. It is tested only by resampling case-control cohorts, and it beats a label-free baseline only by a small margin.

The package also has hard administrative blockers that would get it returned before any scientific reading:
- placeholder author name, e-mail, ORCID and GitHub URL;
- Highlights, which iMeta Letters do not have;
- 24 references, against a practical cap of about 20 for Letters;
- an unreadable Figure 2D axis.

---

## 2. Main reasons an iMeta editor would desk-reject, each with a concrete fix

### R1. Incomplete submission package (would be returned unread)
- Problems:
  - "[Second Author]", "[corresponding author email]", "[ORCID]" and "[GitHub repository URL, to be added before submission]" appear in the byline and the Data Availability Statement. The corresponding author is unnamed.
  - The code, the frozen protocol and the file hashes are central to the "locked, pre-specified" claim, yet no link is given. The claim therefore cannot be checked.
- **Fix:**
  - Fill in every placeholder.
  - Deposit the code, protocol and hashes in a public repository plus a Zenodo DOI, and cite the commit that holds the frozen protocol.
  - Give the protocol and addendum a timestamped identifier (a Zenodo or OSF snapshot). Without one, "pre-registered" (Graphical Abstract) cannot be claimed.

### R2. Limited novelty in the microbiome findings; the closest prior art is under-credited
- Problems:
  - Cross-disease false positives of CRC signatures were shown directly by Wirbel 2021 (SIAMCAT cross-disease analysis, ref 11) and addressed by control augmentation in Thomas 2019 (ref 3). The text cites them only for "shared changes" and "adding other-disease controls". A reviewer will say the comorbidity result replicates known work.
  - Oral-taxa enrichment in cirrhosis (Qin 2014, ref 13) is the canonical oral-gut invasion example. Finding *S. oralis* and *F. nucleatum* driving the cirrhosis gap is expected.
  - The site-transfer finding (Fig. 1A) is not new as a concept.
  - On the method side, your own novelty log names SACSIM (Qiu et al., Biometrics 2026) and Godau 2023/2025 as directly overlapping label-free Neyman-Pearson threshold adaptation. Neither is cited.
- **Fix:**
  - Add one sentence in the opening that states what Wirbel 2021 and Thomas 2019 already showed. Then state the exact increment: (i) locked, pre-specified confirmation in cardiometabolic cohorts the models never touched; (ii) quantified per-site realised FPR dispersion; (iii) a recalibration rule that needs no extra labelling.
  - Cite and contrast SACSIM, Godau, and the Neyman-Pearson umbrella algorithm (Tong 2018).
  - Free reference slots by dropping refs 1, 6, 21 and 22, or move them to the SI.

### R3. The paper lacks one focus, and the "fix" is mostly statistics, not microbiome science
- Problems:
  - The title, highlights and GA promise three stories. Sections 4–5 (medications, mechanism) and 6–7 (the rule) pull in different directions.
  - iMeta readers will judge the microbiome biology. A statistician will judge the rule. Neither part is developed enough for its own audience.
- **Fix: choose one spine.** Recommended: "a locked audit shows microbiome CRC classifiers lose specificity across sites and in cardiometabolic patients, partly through oral taxa and metformin, and outcome-based recalibration restores it". Keep the rule as the practical answer, but cut it back:
  - Move the guarantee wording, the apple-tasting and verification-bias framing, and the full robustness list to the SI.
  - Keep one robustness sentence.
  - Give the space you save to the biology. In particular, show the decomposition for the locked HF/T2D groups, not only the development conditions.

### R4. Clinical premise and significance are overstated
- Problems:
  - No stool-metagenomic CRC test is used in a screening programme. The "programme" language throughout ("programmes know", "a screening programme does observe") describes a hypothetical as current practice.
  - At 90% specificity your classifiers have only about 0.30–0.40 sensitivity (Table S2: Sens source 0.404, vp 0.316, oracle 0.33). That is far below FIT. An editor will ask why the deployment cut-off of a test this weak matters.
  - Fig. 2D at 1% prevalence: avoiding 83 colonoscopies costs 1.1 extra missed cancers per 1,000. With only 10 cancers per 1,000, that is about 11 percentage points of sensitivity (3.6→4.7 missed). The text plays this down as "because the source cut-off was too liberal".
- **Fix:**
  - Reframe as "if microbiome tests are deployed, as proposed, e.g., combined with FIT…".
  - Report sensitivity next to every FPR claim. State the missed-cancer trade-off as a relative change in sensitivity.
  - Add one sentence comparing against FIT performance.
  - Consider framing around adenoma or advanced neoplasia, the realistic screening target.

### R5. Confounding in the headline "chronic disease" result; the metformin result undercuts it
- Problems:
  - In MetaCardis, the cohort behind both locked positives (HF and T2D), the model adjusts for **sex only** (Table S3b covs = "male"). The SI says age and BMI "were not sufficiently recorded". Yet the main text and the Fig. 1B axis say "adjusted for age, BMI and sex". HF patients are older and more heavily medicated than controls.
  - The authors' own exploratory result says MetaCardis T2D **metformin non-users are flagged at the control rate** (Table S6d: 0.085 vs control 0.103 for LASSO). The T2D excess may therefore be almost entirely a drug signal. That contradicts a title that blames "chronic disease".
  - HF is not adjusted for drugs at all (diuretics, PPIs, beta-blockers; the beta-blocker LASSO effect has p = 0.033).
- **Fix:**
  - Re-fit the locked HF/T2D contrasts with all recorded drugs as covariates and report the result. Also report HF and T2D excess among non-users of metformin and PPI.
  - Correct the adjustment wording for MetaCardis in the text and the Fig. 1B axis.
  - Retitle around "cardiometabolic patients and their medications", not "chronic disease".

### R6. The proposed rule's advantage over a label-free baseline is small, and the simulation flatters it
- Problems:
  - The prevalence-bounded quantile uses **no labels** and already reaches FPR 0.088 with 4.7% of months over target (Table S2, primary). The proposed rule reaches 0.085 and 0.6%. The pre-specified difference is −0.04, p = 0.049, which is borderline.
  - At α = 0.05 the rule is overly conservative (FPR 0.034).
  - Sites are simulated by resampling, with replacement, from case-control cohorts that sometimes have 12–18 controls (HallAB_2017, SankaranarayananK_2015, HMP_2019_ibdmdb with 14 controls in Table S3). This makes the exchangeability assumption (A1) true by construction, so the guarantee is close to a tautology in the simulation. Real programmes have seasonal, kit-lot and population drift.
  - The month-1 burn-in FPR of about 0.29 (Fig. 2A) is a real harm, and the text does not count it.
- **Fix:**
  - Put the prevalence-bounded quantile result in the main text and argue the trade-off honestly. The rule's real gains are drift recovery (Table S2 drift: P_over 0.143 vs 0.684) and per-group control. Lead with those.
  - Add a time-ordered evaluation. For example, use YachidaS_2019 or MetaCardis ordered by recruitment centre or batch, or by sample date if available, instead of i.i.d. resampling.
  - Report burn-in cost per 1,000.
  - Exclude, or flag, sites with fewer than about 40 controls.

### R7. The locked-test claim is weakened by data reuse
- Problems:
  - The **pilot** (SI S1) ran leave-one-cohort-out over all 11 CRC cohorts, including the three later "locked" CRC sites, before the data lock. The main text then cites the pilot p = 2×10⁻⁷ as evidence. The locked CRC sites were therefore seen.
  - The adenoma "locked" sites reuse the controls of CRC development cohorts (Table S1, "partly independent").
  - MetaCardis serves as a locked site for the T2D classifier, the comorbidity test and the medication test.
- **Fix:**
  - State the pilot exposure explicitly. Drop the pilot p-value from the main text, or report the overdispersion test on locked sites only.
  - Either do not count adenoma among the "16 locked sites", or call them "partly independent" wherever 16 is stated (highlight, GA, Fig. 2A).

### R8. Format and presentation do not match an iMeta Letter
- Problems:
  - Highlights are present, but iMeta Letters have none (benchmark: Letters have no Highlights).
  - The title has 21 words (Letter median about 13) and uses informal phrasing ("over-flag", "keep their false alarms on target").
  - There are 24 references, against 15–20 in recent Letters.
  - Neither figure has a study-design or workflow panel, which nearly every iMeta Letter has as panel A.
  - The GA is a text-only three-box slide, not a graphical abstract.
  - Jargon leaks into the figures: "H5", "H6", "addendum A1", "contam", "vp".
- **Fix:** see Section 3.

---

## 3. Specific edits most likely to raise the chance of review

### Title (choose one; 12–15 words, declarative, no hype)
- "Locked multi-cohort audit shows gut microbiome colorectal cancer classifiers lose specificity across sites and in cardiometabolic patients" (16 words)
- "Gut microbiome colorectal cancer classifiers lose specificity across sites and in cardiometabolic disease, and outcome-based recalibration restores it" (17 words; shorten if possible)
- Running title: "Specificity of microbiome cancer classifiers in deployment".
- Avoid "over-flag", "false alarms on target" and "chronic disease" (too broad: asthma, schizophrenia and fatty liver were null).

### Highlights
- **Delete the Highlights block** (not used for Letters).
- Put the best of it into the ~100-word graphical-abstract summary. In that summary:
  - Replace "removed the excess in chronic disease" with "equalised false-positive rates across recorded comorbidity groups, at the cost of lower sensitivity in those groups".
  - Remove "common drugs shift the score too" unless the PPI primary hypothesis is reported as unsupported.
- If any highlight-like text survives, the current PPI highlight is spin. "PPIs raised the oral-taxa part … as predicted" hides that the **primary** pre-specified hypothesis (H5, LASSO total score) failed (p = 0.24).

### Opening paragraphs
- **P1:** Cut the GLOBOCAN sentence (ref 1). Open with the microbiome test: "Stool metagenomic classifiers detect colorectal cancer with cross-cohort AUROC ≈0.8 [2–4], but a test is used at a single cut-off, chosen on case-control cohorts." Then state the prior evidence directly: Wirbel 2021 and Thomas 2019 showed cross-disease positivity. The gap is whether this persists in locked cohorts, how large it is per site, and what can be done in deployment.
- **P2:** Keep the "two sources of shift" logic in two sentences.
- **"Here, we" paragraph:**
  - Give the real counts: 30 cohorts in Table S1 plus 2 medication cohorts. Say "16 held-out sites (5 partly independent)".
  - State the headline numbers with CIs. Example: "HF patients were test-positive 2.3× as often as same-site controls (95% CI 1.4–3.4)."
  - State the prevalence-bounded baseline honestly.
  - Replace "nearly half of the sites" with "15 of 32 site–model pairs".
- Remove the conditional "programme" voice everywhere, or mark it as hypothetical.

### Figures
- **Figure 1:**
  - Add a panel A schematic covering cohort roles (development / locked / pilot), classifier → cut-off → site, and the comorbidity and medication contrasts with n. Shrink 1A to make room.
  - **1A:** the x-axis stops at 0.6, but the text, highlight and GA claim a maximum of 0.75. Either the point is clipped or the text is wrong. Extend the axis or fix the number.
  - **1A:** overlapping markers hide sites. Only 3 of 4 RF T2D squares and 2 of 5 RF adenoma squares are visible. Jitter or use a strip plot with site labels.
  - **1A:** the "intended 10%" label collides with the x-tick labels.
  - **1B:** add n per group. Mark Holm-significant rows. Fix the axis text: MetaCardis is sex-adjusted only. Consider showing the positivity ratio (Table S3) as the clinically readable scale.
  - **1C:** add the locked HF and T2D decomposition. This is the result reviewers will want, and it would test whether "oral taxa" or Enterobacterales and metformin drive the locked effect.
  - **1D:** replace "H5" and "H6" with "pre-specified primary" and "pre-specified secondary". Show which items failed.
- **Figure 2:**
  - **2D:** the x-tick labels overprint and cannot be read ("3.6vs4.7d/1,000…"). Move the missed-case counts into a second bar group or a small table.
  - **2D:** for the IBD and T2D classifiers, "missed cancers" is wrong. Say "missed cases".
  - **2D:** the y-axis says "false positives" while the panel title says "unnecessary referrals". Pick one.
  - **2A:** add the sensitivity trace (a second row or inset). Show the burn-in cost.
  - **2C:** rename "None" to "Controls". Add the per-group sensitivity proxy, which is the stated trade-off. Show n per group (HF n = 95).
  - Remove internal shorthand from all panels.
- **Graphical Abstract:**
  - Replace the text-only three boxes with an actual schematic (stool → classifier → cut-off → colonoscopy feedback loop).
  - Remove "pre-registered" unless a public timestamped registration exists.
  - Fix "0–75%" to match Fig. 1A.

---

## 4. Unclear, inconsistent or unsupported statements

| # | Location | Statement | Problem |
|---|---|---|---|
| 1 | Highlight 1, Results §1, GA | FPR "0.00 to 0.75" for T2D | Fig. 1A's maximum T2D point is ~0.59 on an axis ending at 0.6. No SI table lists per-site realised FPR. **Add a per-site FPR table (Table S1b) and reconcile.** |
| 2 | Results §1 | "15 of 32 site–model pairs (47%) … above 12%" | Not verifiable from the SI. Counting from Fig. 1A gives ~13–14 visible points >0.12 (markers overlap). Needs the table above. Intro says "nearly half of the sites", which mixes sites and site–model pairs. |
| 3 | Intro, Fig. 2A legend | "32 public cohorts", "16 locked test sites" | Table S1 lists 30 unique cohorts. VincentC_2016 and LeeKA_2022 (medication check, Table S6a) are missing from Table S1. Five of the 16 locked sites are adenoma cohorts with controls shared with CRC development. |
| 4 | Intro | "fixed all methods … before touching the locked test cohorts" | SI S1: the pilot used all 11 CRC cohorts, including the 3 locked CRC sites, before the data lock. |
| 5 | Results §2 | "In seven development cohorts, the cancer score was higher in every condition" | True for point estimates only. Fatty liver (p = 0.38), asthma (p = 0.42) and schizophrenia (p = 0.15) are null (Table S3c). Say "higher in 4 of 7 conditions (95% CI excluding 0)". |
| 6 | Results §2 | Cirrhosis "52% vs 8% test-positive"; ACVD "52% vs 19%" | Positivity for development cohorts is in no SI table (Table S3 covers only locked cohorts). |
| 7 | Results §2 | "after adjustment for age, BMI and sex"; hypertension +0.33 | LiJ_2017 and LoombaR_2017 are unadjusted (covs = nan, Table S3c). Hypertension +0.33 is crude. |
| 8 | Results §2 / Table S1 vs S3c | Sample sizes | n in Table S3c differs from Table S1 without explanation: JieZ 306 vs 385; XieH 200 vs 250; LiJ_2017 140 vs 196; ZhuF 154 vs 171. In Table S3, HMP_2019_ibdmdb has 57/14 vs 103/27. Table S1 lists 11 development comorbidity cohorts, but only 7 are analysed. Four have 0–10 controls (ChengpingW, VilaAV, LiJ_2014, HMP_2019_t2d) and cannot support within-cohort contrasts. State their use or remove them. |
| 9 | Results §2, Fig. 1B axis | Locked contrasts "adjusted for age, BMI, sex" | MetaCardis is adjusted for sex only (Table S3b). |
| 10 | Results §2 | "T2D in a second cohort [16]" | Ref 16 is Forslund 2015. The cohort is QinJ_2012 (Qin J et al., Nature 2012), which is not cited. |
| 11 | Results §2 | IBD "nominally significant in one cohort" | NielsenHB_2014 is nominal in both models. The HMP_2019_ibdmdb LASSO positivity ratio is 4.91 with CI excluding 1 (Table S3). The wording undersells this. Note too that IBD classifiers and CRC-comorbidity tests share these cohorts. |
| 12 | Results §3 | "78–100% of the increase came from oral-origin taxa" | ACVD: Fig. 1C shows ~0.64 of a 0.83 net gap (~77%). *Lachnoclostridium* (non-oral) is the #2 contributor overall (Table S4b). Highlight 2 generalises "oral taxa drove most of this excess" to the locked HF/T2D effect, which was never decomposed. The metformin section attributes it to Enterobacterales and *S. salivarius*. |
| 13 | Results §3 | "AUROC 0.76 to 0.72"; control augmentation "kept the gap" | Table S4 has no full-model row (the caption mentions "None = full model", but the row is absent). Control-augmentation results appear in no table. |
| 14 | Results §4, Highlight 3 | PPI "as predicted" | Primary H5 (LASSO total score) failed (p = 0.24). Only the secondary H6 and the RF total were positive. The highlight presents a failed primary as success. The Fig. 1D legend says "addendum A1", SI says "S6b"/"H5/H6", and the text says "second protocol". Use one name. |
| 15 | Results §4 | "A smaller cohort showed the same direction" (LiJ_2014) | LASSO beta +0.40 is n.s. For RF, positivity is *lower* in metformin users (0.155 vs 0.238; Table S6d). LiJ_2014 is a development cohort. |
| 16 | Results §4 / Fig. 1D | Metformin plotted as "exploratory" | SI S6b says other drugs were pre-specified secondary outcomes (no direction). Only the within-T2D comparison was post hoc. Label consistently. |
| 17 | Results §5 | "expected FPR … at most the target … for any history" | Table S2b: vp mean FPR 0.105–0.108 at CRC sites and 0.103–0.107 at T2D sites, slightly *above* 0.10. The oracle is 0.105–0.121, above target (Table S2: oracle FPR 0.112, P_over 0.116). An oracle that misses the target more often than the proposed rule needs explaining (finite-sample ties? a different definition?). It also makes "sensitivity within 0.015 of oracle" an unfair comparison, because the oracle runs at a higher FPR. |
| 18 | Results §5, Fig. 2A | "FPR settled at 0.085 from month 2" (1% prevalence, Fig. 2A ~0.08) | Table S2 "primary" pools prevalences. At π = 0.01, Table S2b gives vp 0.105/0.089/0.103 (CRC/IBD/T2D), weighted mean ≈0.098, not ~0.08. The Fig. 2A legend says 1% prevalence at 16 sites, but adenoma was simulated only at π = 0.10/0.30 (Table S2b). |
| 19 | Results §5 | Primary p-values | vs source: diff −0.46, p = 0.011. vs local quantile: diff −0.10, p = 2.5×10⁻⁷. A 4.6-times-larger effect with a 40,000-times-larger p is implausible if both are paired Wilcoxon tests over the same 32 site–model units (SI S6). Check the unit of pairing. |
| 20 | Results §5 | Combined stress: "FPR 0.10, but 20% of months above 0.12 by months 13–18" | Table S2 "combined" gives vp FPR 0.13 and P_over 0.404 (months 7–18). The text's numbers are in no table. The oracle's P_over = 0 in "combined"/"smooth" also needs explaining. |
| 21 | Results §5 | "robust to … 5% or 20% targets (FPR on target)" | α = 0.05 gives FPR 0.034, conservative with lost sensitivity (0.245 vs oracle 0.272). "On target" is inaccurate. |
| 22 | Results §6 | Pooled overall FPR 0.095; per-group overall 0.092 | Not in Table S5. Per-group HF P_over is 0.152 (LASSO), so HF is *not* reliably on target. "Sens_proxy" is not defined anywhere in the SI. MetaCardis has no CRC cases, so the method used to estimate CRC sensitivity by comorbidity group must be stated. |
| 23 | Results §5 | "apple tasting [21]", "conformal cut-offs that need labelled local controls [23]" | Ref 23 (Tong 2018) is Neyman–Pearson classification, not conformal. The keyword "conformal prediction" is not used in the text. |
| 24 | SI S3 vs S7 | Control lower bound | m0 is defined two ways (S3 formula vs m0_lo in S7). They are algebraically equal; use one notation. The drift-alarm restart is data-dependent. Corollary (b) claims the guarantee holds after the restart without addressing selection at the restart time. |
| 25 | SI S4 | Simulation populations | Sites with 12–18 controls are resampled 1,200–2,400 times per year. State the minimum control count, and show results excluding tiny sites. |
| 26 | Main text | "Graphical abstract summary (≤100 words)" | It is ~105 words. Trim. |
| 27 | Data availability | Release mix | MetaCardis comes from release 2022-10-19 and the rest from 2021-03-31. Confirm that MetaPhlAn versions and species naming match, because feature mismatches can themselves shift scores at that site. |

---

### Bottom line for the authors
The data and the honest pre-specification are an asset. The paper fails the desk screen because of:
- an incomplete package;
- a diffuse three-story structure;
- under-credited prior art on cross-disease false positives;
- a confounded headline (sex-only adjustment; metformin);
- a method whose edge over a label-free baseline is small in an i.i.d. simulation.

A tighter Letter could pass the screen. It would:
1. lead with locked, drug-adjusted cardiometabolic specificity loss, decomposed in the locked cohorts;
2. present outcome-based recalibration mainly for drift and per-group control;
3. contain correct numbers, a design panel and a filled-in package.

Estimated chance after these revisions: 40–50%.
