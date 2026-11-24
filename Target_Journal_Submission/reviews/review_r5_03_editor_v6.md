# Review round 5, report 03: handling editor (manuscript v6)

**Score:** 7.5/10  **Decision:** Minor revision. All ten round-4 concerns are addressed. Table S12 is cited, "S1–S12" is used, Fig. 3A is described as the five-population subset, the Fig. 2 legend covers opposite weights, Fig. 3B labels "2 studies", the limitations include processing and referral controls, data availability names accessions, and the README targets v6 and lists `r3_posthoc.py`, `make_figures_v5.py` and `make_graphical_abstract.py`. The main text (L29–251) has about 2,750 words and 3 figures, so it fits the Letter format. The ethics statement is adequate. The placeholders for authors, contributions, COI, funding, AI use and the GitHub/Zenodo link are clearly marked. They are not scientific concerns, but they must be completed before submission. I see no desk-rejection risk beyond those placeholders. The remaining issues concern how the headline items match the evidence.

## Concerns

1. **MAJOR: GA panel 2 mislabels the local bar and overstates the result.** The bar reads "100 local unlabelled people". Its source (Table S12, `local_perdraw_inband`) and the text (L138) both say "100 *labelled* local controls". Those draws are also random splits of the same population, which the text calls an implementation check (L166–167), not evidence of robustness. The panel title "Only local calibration fixes it … costs sensitivity" puts a case–control result (Fig. 3C) on a healthy-only panel. *Resolve:* relabel the bar "100 local controls (random draw)" and retitle the panel "Same-country reference vs local calibration (8 populations, 46 pairs)". Then either drop "costs sensitivity" from the panel title or give it its own caption line, citing Fig. 3C and the three cohorts.

2. **MAJOR: Highlight 4 says "when the case mix shifted".** The 57% comes from age/BMI/sex halves and accession order. Clinical readers will take "case mix" to mean disease prevalence, which is the separate Fig. 3C experiment. *Resolve:* "...cut the FPR error by 57% when the burn-in group differed from later patients in age, BMI, sex or sampling order (post hoc grouping; ...)".

3. **MINOR: the title still reads broader than the evidence.** The burn-in fits only screening settings (L208–210). For IBD and T2D, the paper recommends labelled local controls. *Resolve:* consider "...should be verified at the site of use". Alternatively, keep "recalibrated" and add one sentence to the GA summary saying that IBD and T2D tests would need labelled local controls.

4. **MINOR: Fig. 3C versus the text.** The strict burn-in's sensitivity (about 0.13–0.15) is plotted but never reported. *Resolve:* add it at L203.

5. **MINOR: Fig. 2 taxon labels** are not italicised and lack a period after "sp" ("Prevotella sp CAG 520"). One label is truncated ("Enterobacter cloacae compl"). *Resolve:* italicise genus and species names, write "sp.", and give the full name "complex".

6. **MINOR: Fig. 1 uses orange twice.** The non-westernised diamonds sit on an orange prediction-interval band and are hard to see for populations inside the band. *Resolve:* use a non-orange marker colour, or outline the diamonds.

7. **MINOR: the Highlights are dense for a clinical audience.** Highlight 4 has two parenthetical statistics. *Resolve:* keep one number per bullet and move the P-value bookkeeping to the main text.

8. **MINOR: the burn-in rule is unreadable in plain text.** The rule at L155 (the ceiling formula) has no worked example. *Resolve:* add one line, e.g. "N = 100, α = 0.10, π_max = 0.01 gives k = 91, i.e. the 91st lowest score".

9. **MINOR: reproducibility.** No fresh-clone run of `rebuild_cache.sh` plus the README run order is recorded. The script expects 61 cohort files. *Resolve:* record the date, commit and `audit_numbers.py` output for one clean run in the README. Archive the repository on Zenodo before submission.

## Line-level wording fixes

1. L23: "when the case mix shifted" → "when the burn-in group differed from later people in age, BMI, sex or sampling order".
2. L12: "recalibrating on about 100 unlabelled people from the same site" → "recalibrating on the first ~100 people tested at the same site (no labels needed)".
3. L36: "Two years later, the same group" → "In 2021, the same group".
4. L84: "Even with perfect calibration, small cohorts would put" → "Even if the cut-off were perfectly calibrated, sampling noise in small cohorts alone would put".
5. L138: "100 labelled local controls" → "100 local controls drawn at random (labels not needed in healthy cohorts)". This keeps the text consistent with the GA.
6. L203: "Sensitivity fell from 0.46 to 0.21–0.23." → "Sensitivity fell from 0.46 to 0.21–0.23 (burn-in) and about 0.13–0.15 (strict burn-in)."
7. L216: "is not a fixed property" → "is not a fixed property of the test".
8. L341 (Fig. 3 title): "Only calibration at the site of use restores the FPR" → "Calibration on people from the site of use restores the FPR; borrowed references do not".
