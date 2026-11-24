# Review round 4, report 03: handling editor (manuscript v5)

**Score:** 7/10  **Decision:** Minor revision. Round-3 concerns are largely resolved. The title now says "should", the GA quotes 0–62% (LASSO), I² is given as a percentage, sensitivity is stated, a "Where this applies" section is added, and there is a README with pinned packages and committed, sha256-checked metadata. The main text is about 2,620 words with 3 figures, so it is within Letter limits. Author, COI, funding, AI-use and repository/DOI placeholders are clearly marked and are not counted as scientific concerns. They must be filled in before submission.

## Concerns

1. **MAJOR: the graphical abstract mixes population sets and mislabels one bar.** In `make_graphical_abstract.py`, panel 2 "other cohort, same country" plots the *neighbour-cohort burn-in* (`stress/neighbour/N100/BURN`). That is not the country-matched reference the text reports (46% vs 79% in band, Table S12). Panel 2's training/pooled bars use the `all_full` random set. Panel 3 uses the post hoc within-site set (13 populations). The two "training cut-off" bars therefore come from different populations, but they look comparable. *Resolve:* relabel the bar ("burn-in from another cohort, same country"), or plot the country reference itself. Plot all bars on one population set, or name the set and n under each panel.

2. **MAJOR: Highlight 4 and the GA omit the price.** "Cut the FPR error by about half, even when the case mix shifted" leaves out two facts. Sensitivity fell from 0.46 to 0.21–0.23, and "about half" is 57% (post hoc grouping) or 48% (pre-stated, not supported). *Resolve:* "…roughly halved the FPR error within sites (57%, post hoc grouping), held FPR at or below target with 1–10% patients at the cost of about half the sensitivity, and failed across sites."

3. **MAJOR: reproducibility documents lag v5.** The README run order ends with `make_figures_v4.py → figures_v4`. It omits `make_figures_v5.py`, `make_graphical_abstract.py` and `r3_posthoc.py`, which produces Table S12, the GA and the 57%/P = 0.0007 numbers. The audit command targets `manuscript_v4.md`. The SI points Figure S1 to `figures_v4/`. The docstring of `make_figures_v5.py` still says v4. *Resolve:* update the README run order and audit target, the SI paths and the script headers, and record one fresh-clone run.

4. **MINOR: Table S12 is never cited.** It holds the 57%, 12/13, P = 0.0007 and the country-reference comparison. L136 cites Table S9, and L246 says "Tables S1–S11". *Resolve:* cite S12 at L136 and L176, and change "S1–S11" to "S1–S12".

5. **MINOR: Figure 3A versus the text.** The figure shows 5 populations, with control augmentation at about 0.077. The text cites 7 populations, with augmentation at 0.064 versus burn-in 0.029. Readers will see a conflict. *Resolve:* say in the text that Fig. 3A uses the fixed 5-population set, or add the 7-population values to the legend.

6. **MINOR: Figure 3B layout.** The legend overprints the "other sub-site" error bar. The 2-population bar has a very wide, asymmetric CI. *Resolve:* move the legend and add "(2 studies)" to that bar.

7. **MINOR: Figure 2B shows *R. torques* in red** (more abundant, raises the CRC score), while panel C shows it in blue for IBD. This is consistent with fitted weights but will confuse readers. Add one legend sentence: "the same taxon can carry opposite weights in different models."

8. **MINOR: references are out of order.** [28] is cited (L215) before [27] (L217). Refs 8, 10 and 16 are 2026 papers; confirm the volume and article numbers against the citation audit.

9. **MINOR: Highlight 1 omits the model.** The intervals are LASSO intervals; RF IBD is 0.5–65%. Say "(LASSO)".

10. **MINOR: limitations.** Add the following: the healthy cohorts differ in collection and extraction protocols, which confound "population" with "site processing". The strict set excludes the clinical-referral controls that a real IBD/T2D test would see. Data availability should name the per-cohort accession sources (Table S1) as well as the repository.

## Line-level wording fixes

1. L16: "a cut-off set for a 10% false-positive rate (FPR)" → "a LASSO cut-off set for a 10% false-positive rate (FPR)".
2. L19: "Asian populations were over-flagged by the IBD test" → "the five populations most over-flagged by the IBD test were Asian".
3. L22–23: replace with the wording in concern 2.
4. L126: "(Table S3; S4)" → "(Tables S3 and S4)".
5. L136: "(post hoc; Table S9)" → "(post hoc; Table S12)".
6. L176: "(post hoc grouping; …P = 0.0007)" → add "; Table S12".
7. L166: "(Figure 3A, Table S4)" → "(Table S4; Figure 3A shows the fixed five-population subset)".
8. L182: "This rests on only two studies." → "This rests on two studies (five sub-sites)."
9. L213: "cannot be printed on a label" → "should not be printed on a label without local verification".
10. L246: "Tables S1–S11" → "Tables S1–S12".
