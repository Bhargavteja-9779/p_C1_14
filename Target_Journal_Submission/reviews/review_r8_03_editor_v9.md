# Review round 8, report 03: handling editor (manuscript v9)

**Score:** 8/10  **Decision:** Minor revision (accept after minor changes; low desk-rejection risk)

Version 9 deals with most of the round-7 points. GA panel 2 now includes the "other sub-site" pair, where the burn-in did worse (0.057 to 0.078). The Fig. 3 title no longer overclaims. S14 and S15 are cited. The per-1,000 numbers are given (Table S15). Fig. 2 now reads "CAG-170". Highlight 2 is marked "post hoc".

I checked these against the source tables and figures, and they agree:
- the prediction intervals and I²;
- the Fig. 3B shares (0.135/0.135, 0.167/0.111, 0.37 for the sub-site transfers, 0.31/0.30 for other cohorts);
- the Fig. 3C FPR and sensitivity values;
- the S15 values (285 to 86 false positives per 1,000; PPV 1.6% to 2.6%);
- the number audit of v9 (174 numbers checked, 0 unmatched).

The title, highlights and GA match the evidence, and the limitations are candid. The ethics statement is adequate. Several placeholders remain (authors, contributions, COI, funding, AI statement, GitHub/Zenodo link). They are clearly marked, so I have not counted them.

## Concerns

1. **MINOR: the length leaves no room for changes.** The main text from "To the Editor" to the Conclusion runs to 2,964 words, close to the 3,000-word Letter limit. Any addition during revision will push it over. *Resolve:* cut about 100–150 words now. Candidates are the conformal-literature paragraph (L208–212) and the three-bullet "checks" block (L133–139), which could become one sentence plus Table S5. Also check whether iMeta counts the highlights and GA summary towards the limit.

2. **MINOR: `repro_full.sh` is out of date and has never been run.** It runs `make_figures_v7.py` rather than `make_figures_v8.py` and leaves out `r7_posthoc.py`, so Table S15 is not regenerated. It also audits `manuscript_v8.md` instead of v9. It clones a fixed working branch of a personal GitHub repository. The only reproduction log is still `logs/repro_fresh_clone_2026-11-24.log`, which covers 5 scripts and has no commit hash. *Resolve:* update the script list and the audit target, point the script at the archival tag or Zenodo record, run it once at the submission commit, and commit the log.

3. **MINOR: Table S15 mixes diseases.** The column `cancers_detected_per_1000` and the pooled PPV combine one CRC cohort with two T2D cohorts. "Cancers" is wrong for two of the three cohorts, and a T2D "screening PPV at 1% prevalence" means little clinically. *Resolve:* either report the CRC cohort alone (the only screening use case, as L260 itself states) or rename the column to "cases detected". Say in the text that the pooled figure is purely illustrative.

4. **MINOR: the GA does not show the sensitivity cost.** The GA summary says the burn-in "cost sensitivity", but neither GA panel shows this. *Resolve:* add a one-line note under panel 2 ("3 case–control cohorts: sensitivity 0.46 to 0.22").

5. **MINOR: the title's recommendation is broader than the evidence.** "Should be recalibrated at the site of use" reads as an endorsement of the burn-in. However, the paper says the burn-in fits only screening (L260–263) and does not reduce tail risk. *Resolve:* consider "...should be verified and recalibrated at the site of use". This also matches "local verification" at L268.

6. **MINOR: taxon typography in Fig. 2.** "sp." is set in italics (it should be roman), while Aeromonadales and Enterobacteriaceae are set in roman. *Resolve:* apply one convention throughout.

7. **MINOR: line hygiene.** L82, L216 and L254–255 are over-length and unwrapped in the source. The round-7 orphan clause has been merged into L192, but it still reads as a non-sequitur. *Resolve:* see the wording fixes below.

## Line-level wording fixes

1. L82: "More recent work reports" → "Recent work reports". Rewrap the line.
2. L192: delete "; augmentation was evaluated on the full set of locked populations". The point is already made at L187.
3. L216: "so the comparison shows how miscalibrated the training cut-off is, not that the burn-in is robust" → "so this comparison measures the training cut-off's miscalibration, not the burn-in's robustness".
4. L254: "Any cut-off that meets the 10% target pays this price" → "Any cut-off meeting the 10% target pays a similar price". Rewrap the line.
5. L255: "the positive predictive value, pooled over these three cohorts" → "the illustrative positive predictive value, pooled over one CRC and two T2D cohorts".
6. L299: "which is why sites should monitor it" → "so sites should keep monitoring it".
7. L268: "should not be printed on a label without local verification" → "should not be quoted without local verification".
8. Title: "should be recalibrated at the site of use" → "should be verified and recalibrated at the site of use".
