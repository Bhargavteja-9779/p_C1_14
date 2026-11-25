# Editor report — iMeta Letter (manuscript_v12)

**Recommendation:** Minor revision
**Editor score:** 8/10
**Desk-rejection risk:** Low. Format fits a Letter (main text ~2,200 words; 3 figures; graphical-abstract summary ~125 words). Ethics and data-availability statements present; author/ack/COI/funding/AI and the GitHub–Zenodo URL are clearly marked placeholders (noted, not counted). Tool tests pass (11/11).

## Summary
A well-scoped, rigorously reported Letter. The claim — a microbiome classifier's false-positive rate is a joint property of test and population, and geographically unbalanced pooled training can encode a region's normal flora as a disease signal — is supported by the figures and SI. Pre-specified plans with falsification criteria, reported failed hypotheses, effect sizes with CIs, and a released tool make this unusually reproducible for the genre. Title, summary and headings match the evidence; I found no misstated results.

## MAJOR concerns
None. No desk-rejection risk and no result is overstated relative to the data.

## MINOR concerns
1. **Summary conflates two quantities.** The abstract's "cut the FPR error by 62–79%" pools the 28-classifier within-site result (62%) with the single GMWI2 result (79%, line 134–135). Rephrase so a reader sees these are two analyses, not one range. *Resolution:* "…by 62% across 28 classifiers, and by 79% for GMWI2."
2. **Figure 3C hypothesis labelling.** Panel C caption states H₀: FPR ≤ 0.15, but text (line 146) frames the headline as detecting "a true FPR above 0.25 with probability 0.98," and the panel plots both 0.15 and 0.25 curves. State one primary hypothesis in text and caption and mark the other as secondary. *Resolution:* align caption wording to line 146.
3. **Reference numbering is not in citation order.** GMWI2 [22] and [23] are first cited at lines 33 and 91, before [13]–[21]. iMeta numbers by order of appearance. *Resolution:* renumber, or confirm the journal's style permits grouped numbering.
4. **Burn-in deployment proxy.** The within-site recalibration is evaluated on a non-random split of the *same* cohort, not prospectively; the across-site failure is disclosed (line 138–140), but a clinical reader may miss that no truly prospective test was run. *Resolution:* one sentence in the site section stating the evaluation is retrospective within-cohort and that prospective validation is the next step.
5. **Sensitivity cost framing.** The recalibration's sensitivity drop (0.46 → 0.21–0.23 with 1–10% contamination) is in SI and the limits; given the clinical audience, surface it once in the main text where the fix is recommended, so the screening-vs-symptomatic caveat is unmissable. *Resolution:* add a clause at line 143.
6. **"Population" conflates biology and batch.** Acknowledged in limits (line 161), but the central claim leans on it; keep the GMWI2 case-mix result foregrounded as the strongest evidence that the effect is not purely technical.
7. **I² reporting.** I² values are given without CIs in several places (lines 49, 74, 81). Add interval or n so readers can judge precision. *Resolution:* cite Table S2 columns.
8. **Figure 1D null result.** "AUROC did not predict spread" (ρ = −0.06) is a key message but easy to under-read at panel size; consider a one-line annotation of the take-home on the panel.

## Line-level fixes (≤8)
- L13 / L48: harmonise units — "0% to 77%" (summary) vs "0 to 0.77" (text); use one convention throughout.
- L33: define GMWI2 at first mention before the citation jump; reorder refs (see Minor 3).
- L50: "15–16% of populations outside 0.05–0.15" — state this is the sampling-noise expectation inline.
- L71: "we take this as the stated FPR" — clarify 20.8% is the developers' training FPR, not an independent target.
- L107: "beyond our pre-stated margin of 0.03, so that hypothesis failed" — good; add the pre-registered margin's location (plan v6b).
- L112: "(66% to 82%)" — specify this is the 0.05–0.15 out-of-band share.
- L146: "probability 0.98" — add n (=100) inline to match Figure 3C.
- L207: ensure the Zenodo DOI and GitHub URL are live before production; flag as the only blocking placeholder for reproducibility.

**Bottom line:** Accept after minor revision. The science, scale (6,525–8,160 healthy people, 36–55 populations, 20 countries, 28 classifiers), and openness are strong; fixes are editorial and clarifying, not substantive.
