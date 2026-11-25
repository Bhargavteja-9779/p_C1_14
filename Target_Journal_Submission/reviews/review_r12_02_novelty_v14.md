# Referee report, round 12 — Reviewer 2 (novelty and related work)

**Manuscript:** manuscript_v14.md (Letter, iMeta)
**Title:** "Gut-microbiome classifiers flag healthy people at population-specific rates, and a published health index
mislabels a whole region"

**Score:** 8/10
**Recommendation:** Minor revision
**Novelty:** 22/25

---

## Summary judgement

The Letter makes three claims. I assessed each against prior art with my own searches (Crossref, OpenAlex, Europe PMC,
PubMed/E-utilities; at least ten phrasings across the three claims) and verified that every one of the 28 reference DOIs
resolves on Crossref and supports the sentence that cites it.

1. **A 14-disease × 36-population false-positive-rate atlas** (FPR at a fixed cut-off varies by test–population pair and
   is not predicted by AUROC, ρ = −0.06). I could find no prior work that maps specificity/FPR at a fixed operating
   point across many healthy populations and many diseases. The closest neighbours (CRC-TrustBench [12], Li 2023's
   20-disease cross-cohort study [8], SIAMCAT [11]) report AUROC or calibration, not a fixed-cut-off FPR surface, and
   none makes the AUROC-does-not-predict-portability point empirically. **Novel.**
2. **An audit of GMWI2 inside its own training data** showing region-specific mislabelling (0.64 East Asian vs 0.12
   elsewhere), mechanistically linked to the geographic case-mix of the training data (OR 6.7) and probed by retraining
   with country-balanced weights (88% of the gap removed). No prior paper audits a published, deployed microbiome index
   for region-specific over-flagging *in its own training scores* or tests the cause by retraining. SIAMCAT [11] shows
   country confounding *can* inflate performance and Gupta 2020 GMHI [19] notes low scores where training markers are
   absent, but neither quantifies mislabelling of a released index or tests it causally. **Novel; honestly bounded** (the
   manuscript concedes [11] at lines 110–111).
3. **Site-level verification + label-free burn-in recalibration** with a released tool (`fprcal`). The split-conformal /
   PAC machinery (Lei [20], Bates [21], Tong [23]) and the reference-interval analogy (Ozarda [14], refineR [24]) are
   pre-existing and the manuscript says so plainly ("The rule is not new", lines 143–145). The contribution is applying
   a label-free local burn-in to microbiome operating points and showing empirically that it works within a site (62%/79%
   error reduction) and *fails* across sites. **Incremental but fairly framed, and the honest reporting of the cross-site
   failure is a genuine strength.**

This is a round-12 draft; the round-11 MAJOR (the "has not been measured" framing was missing the closest multi-disease
cross-cohort citations) has been resolved — v14 now cites Li 2023 [8], Li 2025 [9] and the Degregori audit [10] at
lines 28–31. My one remaining MAJOR is a different, un-flagged gap in the related-work framing of claim 1.

---

## Claim → closest prior work → exact difference

| # | Claim | Closest prior work | Exact difference |
|---|-------|--------------------|------------------|
| C1 | A fixed cut-off gives a different FPR in every population; AUROC does not predict the spread (ρ = −0.06); 14 diseases × 36 populations | CRC-TrustBench, Zhang 2026 [12] (LOSO/LOCO calibration, CRC only); Li 2023 [8] (20-disease cross-cohort, AUROC); SIAMCAT [11] (external controls double CRC false positives); **clinical-epi "spectrum effect"**, Leeflang 2013 (uncited); prevalence-dependent accuracy, Balayla 2026 (uncited) | Prior work reports AUROC or CRC-only calibration, or shows FP inflation for one disease. **New:** a multi-disease FPR *atlas* at each classifier's own fixed cut-off across 36 healthy populations, with I²/prediction intervals, and the demonstration that out-of-fold AUROC is uncorrelated with between-population FPR heterogeneity. The *conceptual* precedent (specificity varies by population/spectrum) exists in diagnostic epidemiology and is not cited — see MAJOR 1. |
| C2 | A deployed index (GMWI2) mislabels whole regions **in its own training scores** (0.64 vs 0.12); mechanism = geographic case-mix (EA = 62% of non-healthy vs 20% of healthy, OR 6.7); **tested by retraining** (88% of gap removed) | SIAMCAT [11] (country confounding can inflate performance); Gupta 2020 GMHI [19] (low scores where markers absent); Poyet 2026 [13] (industrialised-trained predictors lose accuracy) | Prior work shows confounding *can* inflate performance and that Western-index markers are scarce in non-industrialised guts. **New:** that this surfaces as region-specific *mislabelling of a published index inside its own training data*, its magnitude (OR 6.7; 64% vs 12%), and a direct causal test by retraining with country-balanced weights. Fairly framed. |
| C3 | Label-free local burn-in recalibrates the cut-off (62%/79% error reduction within site; fails across sites); released as `fprcal` | Split-conformal (Lei [20]), conformal p-values (Bates [21]), NP/PAC (Tong [23]), prior-shift (Saerens [22]); reference-interval estimation (Ozarda [14], refineR [24]) | Machinery is pre-existing and acknowledged. **New (incremental):** application to microbiome operating points; empirical demonstration that a non-random within-site split still controls FPR and that cross-site burn-in does not; a tested, released tool. |

---

## Concerns

### MAJOR

**MAJOR 1 — Claim 1's novelty is stated against the microbiome literature but omits the diagnostic-epidemiology
precedent that is its conceptual parent.** The sentence "The FPR at a fixed cut-off, population by population and across
diseases, has to our knowledge not been reported" (lines 30–31) is defensible *for microbiome classifiers*, but the
general phenomenon — that a test's specificity (and therefore its FPR at a fixed threshold) varies with the population
and case-mix — is a long-established result in clinical epidemiology (the "spectrum effect"). The only non-microbiome
analogue the manuscript cites is reference-interval verification in lab medicine [14]. A novelty/related-work referee
will read the omission of the spectrum-effect literature as the Letter claiming more conceptual novelty than it holds.
*Resolution:* add one sentence situating C1 as the microbiome-specific, multi-disease instance of the known spectrum
effect, citing **Leeflang et al. 2013, CMAJ, 10.1503/cmaj.121286** (variation of a test's sensitivity and specificity
with prevalence/population) and optionally **Balayla 2026, J Eval Clin Pract, 10.1111/jep.70622** (prevalence-dependent
diagnostic accuracy). This *strengthens* the paper: the novelty is then cleanly "first empirical FPR atlas in
microbiome, confirming a known clinical phenomenon the field has ignored," which is both true and more defensible than
an unqualified "not been reported." Both DOIs verified on Crossref.

### MINOR

**MINOR 1 — The FIT-screening analogy (lines 24–25, ref [7]) could be reinforced with the direct precedent that FIT
specificity itself varies by sex/age/threshold.** The manuscript already uses FIT to motivate the colonoscopy cost; the
finding that a *stool* screening test's FP rate shifts with the population it is applied to is directly precedented for
FIT. Citing **Selby et al. 2019, Gastroenterology, 10.1053/j.gastro.2019.08.023** (effect of sex, age and positivity
threshold on FIT accuracy) would show the authors know the operating-point-shift problem is real for deployed stool
screens, not only a microbiome curiosity. Verified. Optional.

**MINOR 2 — The GMHI direction-of-effect (line 108, ref [19]) is now cited, but the phrasing "in the same direction as
the low health-index scores reported for populations that lack the training markers [19]" slightly understates that
Gupta 2020 already observed non-industrialised populations scoring low on GMHI.** One clause making explicit that the
*direction* was anticipated by GMHI, while the *mechanism test by retraining* and the *magnitude in GMWI2's own training
data* are new, would pre-empt a "this was already known" objection. The current wording is acceptable but could be
tightened.

**MINOR 3 — Claim 3's conformal/PAC citations are correct but the related-work reader may want the prior-shift lineage
made one notch more explicit.** Saerens [22] is cited parenthetically ("related to prior-shift corrections"); given that
the burn-in rule's validity rests on a prevalence bound (π_max), a half-sentence tying the method to the label-shift
literature would help. Not novelty-threatening; the honest "the rule is not new" already covers the authors.

---

## Novelty scoring (/25)

| Dimension | Score | Basis |
|-----------|-------|-------|
| Differentiation | 4/5 | Claims cleanly separated from CRC-TrustBench / SIAMCAT / GMHI / GMWI2 / Li 2023 and honestly bounded; −1 for the uncited spectrum-effect conceptual precedent for C1 (MAJOR 1). |
| Mechanism | 5/5 | C2 gives an explicit, quantified mechanism (geographic case-mix, OR 6.7) and tests it causally by retraining with country-balanced weights, decomposing the within-country vs overall-geography contributions. |
| Evidence | 5/5 | Atlas scale with I²/Cochran Q/prediction intervals; falsified pre-specified hypotheses reported; clustered CIs; GMWI2 reproduced from the released model (r = 0.991). |
| Breadth | 5/5 | 14 diseases × 36 (55 full) populations, 20 countries, plus a published-index audit and a released tool — well beyond any single-disease or single-index precedent. |
| Significance | 3/5 | Important for how the field reports and deploys tests (concrete reporting proposals + a fix), but microbiome diagnostics are not yet clinically deployed, so near-term patient impact is indirect; the authors state this honestly. |
| **Total** | **22/25** | |

---

## Missing references (verified DOIs)

1. **Leeflang MMG, Rutjes AWS, Reitsma JB, Hooft L, Bossuyt PMM. Variation of a test's sensitivity and specificity with
   disease prevalence. *CMAJ.* 2013;185:E537–E544. 10.1503/cmaj.121286** — conceptual precedent for claim 1 (MAJOR 1).
2. **Balayla J. Generalizing the Prevalence Threshold Under Prevalence-Dependent Diagnostic Accuracy. *J Eval Clin
   Pract.* 2026. 10.1111/jep.70622** — optional, supports MAJOR 1.
3. **Selby K, Levine EH, Doan C, et al. Effect of Sex, Age, and Positivity Threshold on Fecal Immunochemical Test
   Accuracy. *Gastroenterology.* 2019;157:1494–1505. 10.1053/j.gastro.2019.08.023** — optional, MINOR 1.

All three appear in the authors' own `journal_selection/novelty_map.csv` (N47, —, N49) but were not carried into the
manuscript; they strengthen rather than undercut the novelty claim and their omission is the one substantive related-work
gap I found.

---

## Reference integrity check

I queried Crossref for all 28 cited DOIs (including the CRC-TrustBench correction, 10.3389/fmicb.2026.2021752, and
Poyet 2026 Cell, 10.1016/j.cell.2026.10.016). **All 28 resolve, and author/year/title/venue match the reference list.**
Spot-checking the load-bearing novelty citations (SIAMCAT [11], CRC-TrustBench [12], GMWI2 [16], GMHI [19], Li 2023 [8],
Li 2025 [9], Degregori [10]) against their abstracts, each supports the sentence it is attached to. No fabricated or
mis-cited reference detected.
