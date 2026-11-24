# Review round 3, report 03: editor, clarity and reproducibility (manuscript v4)

**Score:** 5/10  **Decision:** Major revision. The science is now cleanly scoped. The submission package is not ready, and the headline wording still claims more than the corrected statistics show.

## Concerns

1. **MAJOR: the Supporting Information is stale.** `supporting_information.md` still describes the v3 analysis (adenoma task, Tables S6/S9–S11, `screening_pool_sim.py`). It has no strict set, no burn-in rule, no de-duplication and no S5 "first version". The main text sends all methods to the SI ("Full methods … are in the Supporting Information") and cites Table S3 and S5. A desk editor would return the paper as it stands. *Resolve:* write SI v4 (methods, Table S1 cohorts, the strict-set flow diagram with counts, the Holm table, D1–D4) and check every cross-reference.

2. **MAJOR: the title, abstract and bullet 3 overstate the burn-in result.** The bullet says the burn-in "halves the error". The text reports 48% against a pre-stated 50% threshold, and says this hypothesis is "not supported as written". The locked seven-population comparisons do not survive Holm correction (0.19, 0.13). Burn-in versus augmentation gives P = 0.22. "Must be recalibrated at each site" is a recommendation, not a finding. *Resolve:* use "should" or "need to be checked" in the title, change bullet 3 to "roughly halved (48%)", and add "in seven held-out populations" wherever the locked result is cited.

3. **MAJOR: "0% to 76%" in the graphical abstract.** The 76% figure is GuptaA_2019 under IBD RF, with n = 29 (atlas_perpop_v4.csv). It appears only in Figure S1. The main-text range for populations of at least 100 people is 0.4–61%. *Resolve:* quote the main-figure LASSO range, or say "up to 62% (LASSO) and 76% (RF; n = 29)".

4. **MAJOR: the clinical framing of the burn-in.** In the contaminated burn-in, sensitivity fell from 0.46 to 0.21–0.23. Clinical readers will see the main cost as halved sensitivity, not as a restored FPR. The rule also needs a known π_max and a mostly healthy stream of people. That fits CRC screening, but not IBD or T2D tests used on symptomatic or referred patients, where prevalence is high. *Resolve:* add a short paragraph that names the settings where the rule applies and where it does not, and state the sensitivity trade-off in the abstract.

5. **MAJOR: no outside reproducibility.** HANDOFF records G9 as "unknown, no fresh-clone test". There is no README for `v4/` and no run order for its 13 scripts. `rebuild_cache.sh`:
   - pulls `sampleMetadata.rda` from the moving *devel* branch, not the 2021-03-31 release the paper cites;
   - pins only scikit-learn;
   - hides fetch failures with `|| true`;
   - hard-codes `/tmp/claude-0`.

   The HANDOFF rerun command points to v3 `atlas_run.py`. *Resolve:* add `code/experiments/atlas/v4/README.md` with run order, inputs and outputs. Pin all packages and the metadata commit, make fetch failures fatal, and run a fresh-clone test before deposit (GitHub + Zenodo DOI).

6. **MAJOR: declarations are placeholders.** Authors, contributions, COI, funding, the AI statement, and the repository URL and DOI are all missing. iMeta also requires Highlights (3–5 bullets) and a graphical abstract image; neither is supplied. *Resolve:* complete all of these. Add 2–3 sentences to the ethics statement on the original studies' consent and the terms of public data use.

7. **MINOR: citation gaps.** Ref. 12 (Vujkovic-Cvijin) is listed but never cited. Figure 3A is never cited in the text, and Tables S1/S2 are not cited (Table S3 is cited first). *Resolve:* cite ref. 12 where covariates are discussed, or drop it. Cite Fig. 3A in the burn-in random-split paragraph.

8. **MINOR: Figure 3 uses internal code labels.** The panels say SRC, ATLAS, BURN, BURN-PAC and ALIGN, but the legend uses colour names. In 3A the legend overprints the BURN line. In 3B the y-axis reads "P(FPR > 0.15), N = 100". *Resolve:* use plain labels ("training cut-off", "pooled reference", "burn-in", "strict burn-in", "feature alignment"), move the legend, and give n populations per bar in 3B.

9. **MINOR: Figure 2 uses study codes.** Panel titles show study codes (LokmerA, GuptaA, BritoIL), but the text names countries. The colour key ("raises score") differs from the legend's sign convention, and *Ruminococcus torques* as a "health marker" will surprise IBD readers. *Resolve:* title the panels with country and lifestyle, use one sign convention, and comment briefly on *R. torques*.

10. **MINOR: structure.** The section titled "What we measured, and what a first review changed" puts internal review history into the main text. The 11 Holm-adjusted P values sit in Limitations. *Resolve:* move the revision history to the SI. Keep a two-sentence data-quality statement in the main text. Put the Holm results in a small SI table and refer to it.

11. **MINOR: I² notation.** I² is given as a proportion (0.70–0.95). Clinical readers expect a percentage (70–95%). *Resolve:* change it in the text, Figure 1 titles and the abstract.

## Line-level wording fixes

1. L1: "…and must be recalibrated at each site" → "…and should be recalibrated at the site of use".
2. L9: "flagged anywhere from 0% to 76%" → "flagged 0% to 62% (LASSO)".
3. L10: "(I² 0.70–0.95)" → "(I² 70–95%)".
4. L12–13: "This held when the case mix shifted" → "It stayed at or below target with 1–10% patients in the burn-in group, at the cost of sensitivity".
5. L38: "halves the error" → "cut the error by about half (48%)".
6. L44: rename the heading to "DATA AND DESIGN".
7. L65: "close to or below target" → "within 0.04 of target", since IBD and T2D LASSO were 0.12–0.13.
8. L124: "added after our literature search" → "not pre-specified; added after round-1 review".
9. L176: "Neither test is close to a screening tool on its own" → "Neither classifier is a usable screening test on its own".
10. L207–208: "restores it. Borrowed references do not." → "brought it close to target in the cohorts we could test; references borrowed from other cohorts did not".
