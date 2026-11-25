# Referee report, round 11: novelty and related work (manuscript_v13.md)

**Reviewer:** Reviewer 2 (novelty / related work), iMeta Letter
**Score:** 8/10
**Recommendation:** Accept after minor revision (one positioning item is blocking but is a citation-plus-sentence fix, not re-analysis)
**Novelty:** 21/25

---

## Summary judgement

This is a careful, honestly positioned Letter. Its central empirical object — a false-positive-rate (FPR)
atlas of 28 classifiers for 14 diseases, scored at each classifier's own fixed cut-off in 36 unseen healthy
populations, with per-classifier I², prediction intervals and a crossed-random-effects variance decomposition
(pair = 62%) — is, to my reading of the literature, not previously reported. The second contribution, an
audit of the published GMWI2 index inside its *own* training scores showing region-specific mislabelling
(East Asian 0.64 vs 0.12 elsewhere), with a tested mechanism (geographic case-mix; odds ratio 6.7; retraining
with country-balanced weights removes 88% of the gap), is a genuine and well-evidenced addition that goes
beyond the prior "health-index markers are scarce in non-industrialised guts" observation. The third
contribution (label-free burn-in recalibration + released `fprcal`) is modest and the authors correctly
decline to claim the rule itself as new.

I searched OpenAlex, Europe PMC, Crossref and PubMed with more than eight phrasings (false-positive rate /
fixed cut-off / population-specific; GMWI geographic bias; health-index mislabelling non-westernised; pooled
training geographic confounding; label-free site recalibration; reference-interval verification microbiome;
conformal site-specific FPR; multi-disease cross-cohort specificity). I found no paper that reports the
fixed-cut-off FPR of microbiome disease classifiers population-by-population across 14 diseases with
heterogeneity statistics, and none that audits GMWI2's region bias within its own training data and tests it
by retraining. The core claims stand. The deductions are for incomplete positioning against three recent,
closely adjacent papers that the manuscript does not cite, which matters because the Letter leans on a
"has not been measured" framing (line 27).

**Reference integrity:** I resolved all 23 manuscript references directly against `api.crossref.org/works/<DOI>`.
All 23 resolve, and each title matches the sentence it supports (spot-checked [8] SIAMCAT = ">2-fold FPR
excess, control augmentation did not depend on control set"; [9] CRC-TrustBench incl. its correction DOI
10.3389/fmicb.2026.2021752, which resolves; [13] GMWI2; [18] Tong NP-ROC; [16/17] conformal; [11/19]
reference-interval verification). No fabricated or broken DOI found. The CRC-TrustBench correction is
correctly paired.

---

## Claim → closest prior work → exact difference

| # | Claim (v13) | Closest prior work (verified DOI) | Exact difference |
|---|---|---|---|
| C1 | Fixed-cut-off FPR is specific to the classifier–population *pair* (pair = 62% of variance; LASSO FPR 0–0.77; I² median 0.94) and is **not predicted by AUROC** (ρ = −0.06, P = 0.76) | SIAMCAT, Wirbel 2021, 10.1186/s13059-021-02306-1; CRC-TrustBench, Zhang 2026, 10.3389/fmicb.2026.1971707; Li 2023 "20 diseases", 10.1080/19490976.2023.2205386 | SIAMCAT gives one average 2-fold FPR excess, no per-population dispersion. CRC-TrustBench is CRC-only, reports AUROC/Brier/log-loss/conformal coverage under LOSO/LOCO, not per-cohort FPR at one developer cut-off. Li 2023 reports AUC across 20 diseases cross-cohort, not FPR at a fixed cut-off per healthy population. **The breadth (14 diseases × 36 populations), the pair variance decomposition, the I²/PI treatment and the AUROC-does-not-predict-portability result are new.** |
| C2 | A deployed index (GMWI2) mislabels whole regions **in its own training scores** (0.64 vs 0.12); mechanism = geographic case-mix (EA = 62% of non-healthy vs 20% of healthy; OR 6.7); **tested by retraining** (country-balancing removes 88% of gap) | SIAMCAT [8] (country confounding can inflate performance); Gupta 2020 GMHI, 10.1038/s41467-020-18476-8; Poyet 2026 [10], 10.1016/j.cell.2026.10.016 | Prior work shows confounding *can* inflate performance and that Western health-index markers are scarce in non-industrialised guts. **New:** that this surfaces as region-specific *mislabelling of a published index inside its own training data*, its magnitude (OR 6.7; 64% vs 12%), and a direct causal test by retraining with country-balanced weights. The manuscript concedes [8] at lines 102–103; the direction-of-effect is partly anticipated by Gupta 2020/Poyet (see MINOR 1). **Partly new, fairly framed.** |
| C3 | Label-free burn-in recalibration cuts mean FPR error within a site (62%; GMWI2 79%) but breaks across sub-sites; released as `fprcal` | Lei 2018 [16]; Bates 2023 [17]; Tong 2018 [18]; Roschewitz 2023 (map); refineR/Ozarda [11,19] | The order-statistic rule is explicitly **not** claimed as new and is correctly credited to conformal/NP and lab medicine. **New contribution** is the empirical where-it-works/where-it-breaks map for microbiome tests + the released atlas/tool. Modest, honest. |
| C4 | Batch/processing corrections (DEBIAS-M, MMUPHin, ConQuR) should be judged by the FPR they deliver at new sites | [21] 10.1038/s41564-025-01954-4; [22] 10.1186/s13059-022-02753-4; [23] 10.1038/s41467-022-33071-9 | These report AUROC/AUPRC/batch-mixing, not fixed-cut-off FPR. Recommendation is new; methods not run (disclosed, lines 173–174). Fair. |
| C5 | Cross-cohort benchmarks + STORMS should report per-population FPR with I²/PI alongside AUROC | STORMS [20] 10.1038/s41591-021-01552-x | STORMS does not currently request this. A reasonable, non-overclaimed suggestion. |

---

## Concerns

### MAJOR

**MAJOR 1 — the "has not been measured" framing is not defensible without citing the closest multi-disease
and same-journal audit papers.** Line 27 states "How far this happens, and why, has not been measured," and
the Letter's value rests on being first to map per-population FPR across many diseases. Three closely adjacent,
verified papers are absent from the reference list:
- Li et al. 2023, *Gut Microbes*, "Performance of Gut Microbiome as an Independent Diagnostic Tool for 20
  Diseases: Cross-Cohort Validation" (**10.1080/19490976.2023.2205386**) — the nearest multi-disease
  cross-cohort evaluation.
- Li et al. 2025, *Gut Microbes*, "Best practices for developing microbiome-based disease diagnostic
  classifiers through machine learning" (**10.1080/19490976.2025.2489074**).
- Degregori et al. 2026, *iMeta* (this journal), "A decade-scale audit of microbiome AI-readiness"
  (**10.1002/imt2.70192**).

These do not pre-empt the FPR atlas (Li 2023 reports AUC, not FPR at a fixed cut-off per healthy population;
Degregori audits data AI-readiness, not deployment FPR), so the core claim survives. But a novelty referee
cannot let a "not been measured" sentence stand while the two nearest multi-disease cross-cohort papers and a
same-journal audit go uncited.
*Resolution:* cite all three; soften line 27 to "...has not been measured at a fixed cut-off, population by
population, across diseases"; add one sentence distinguishing Li 2023 (AUC, not FPR) and Degregori 2026 (data
readiness, not deployment FPR). This is a citation-plus-sentence fix, not new analysis — hence a *minor*
revision despite being flagged MAJOR for its load-bearing role.

### MINOR

**MINOR 1 — credit the direction of the GMWI2 region finding to the predecessor index.** The health-index
audit cites GMWI2 [13] but not its predecessor GMHI (Gupta 2020, **10.1038/s41467-020-18476-8**), whose median
score ≈ 0 in non-industrialised populations is the same direction as the East-Asian over-flagging reported
here, and [10] (Poyet) is used only for "predictors lose accuracy elsewhere." *Resolution:* add Gupta 2020 and
one clause: "...consistent with health-index scores being systematically low where training markers are absent
[10, GMHI]." The *size, the in-training-data demonstration, and the retraining test remain the new part.*

**MINOR 2 — the burn-in / prior-bound rule touches the label-shift / quantification literature, which is not
acknowledged.** The π_max correction is, in effect, a prevalence/prior adjustment to an operating point; the
label-shift family (Saerens 2002, 10.1162/089976602753284446; Lipton 2018, arXiv:1802.03916) is the standard
home for "unlabelled target, correct the operating point." The authors' framing via conformal + NP + lab
medicine is legitimate, but one sentence placing the rule in that lineage would pre-empt a methods referee.
*Resolution:* add one clause and one or two citations; no claim change needed.

**MINOR 3 — a 2026 compositional "reference region for healthy microbiome" preprint exists.** My Crossref
search surfaced "Tolerance Regions for Compositional Data with Application to Reference Regions for Healthy
Microbiome Profiles" (2026, 10.64898/2026.05.06.723285). It is a different object (compositional tolerance
region on abundances, not a classifier-score FPR atlas), so it does not threaten novelty, but it is the
nearest "local healthy reference" idea in microbiome space and could be cited at line 29–30 for completeness.
*Resolution:* optional one-line citation.

**MINOR 4 — "first"/novelty wording.** The manuscript mostly avoids "first," which I commend. Keep it that
way; frame C1 as "to our knowledge not previously reported population-by-population across diseases" rather
than any absolute claim.

---

## Novelty scoring (/25)

| Dimension | Score | Basis |
|---|---|---|
| Differentiation | 4/5 | Claims cleanly separated from SIAMCAT/CRC-TrustBench/GMHI and honestly bounded; −1 for three uncited near-neighbours (MAJOR 1, MINOR 1). |
| Mechanism | 4/5 | Geographic case-mix → region commensals as disease markers is concrete and tested by retraining (88% gap removal); −1 because the direction is partly anticipated by [8] and Gupta 2020. |
| Evidence | 5/5 | Pre-specified plans with falsification criteria, reported failed hypotheses, retraining test, conformal theory + Beta-law + empirical within/across-site map. Unusually rigorous for a Letter. |
| Breadth | 4/5 | 14 diseases × 36 populations × 28 classifiers is broad; −1 for single pipeline (MetaPhlAn3), fixed classifier settings, nine classifiers on one training cohort (disclosed). |
| Significance | 4/5 | Clinically concrete (every FP = colonoscopy), actionable recommendations + released tool; −1 as scope is a Letter and the site-level fix is retrospective only. |
| **Total** | **21/25** | |

---

## Missing references (with verified DOIs)

1. Li J, et al. 2023. Performance of gut microbiome as an independent diagnostic tool for 20 diseases:
   cross-cohort validation. *Gut Microbes.* **10.1080/19490976.2023.2205386** (closest multi-disease
   cross-cohort; MAJOR 1).
2. Degregori S, et al. 2026. A decade-scale audit of microbiome AI-readiness. *iMeta.*
   **10.1002/imt2.70192** (same-journal audit; MAJOR 1).
3. Li J, et al. 2025. Best practices for developing microbiome-based disease diagnostic classifiers through
   machine learning. *Gut Microbes.* **10.1080/19490976.2025.2489074** (MAJOR 1; also supports the
   "report FPR" recommendation).
4. Gupta VK, et al. 2020. A predictive index for health status using species-level gut microbiome profiling
   (GMHI). *Nat Commun.* **10.1038/s41467-020-18476-8** (GMWI2 predecessor; MINOR 1).
5. Saerens M, et al. 2002. Adjusting the outputs of a classifier to new a priori probabilities.
   **10.1162/089976602753284446** and/or Lipton ZC, et al. 2018. Detecting and correcting for label shift.
   arXiv:1802.03916 (MINOR 2; optional).

No fabricated references were found in the manuscript; all 23 cited DOIs resolve and support their sentences.
