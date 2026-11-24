# Review round 7, report 03: handling editor (manuscript v8)

**Score:** 8/10  **Decision:** Minor revision (accept after minor changes)

Version 8 fixes the two round-6 MAJORs. The graphical-abstract (GA) summary now describes the unlabelled burn-in, and GA panel 2 shows the same thing. The Fig. 1 legend now says "Grey band". Several smaller items are also fixed: the Fig. 3B random split is now labelled "11 pop.", the "sp." forms are corrected in Fig. 2, and the *Collinsella* label matches the text. The main text (L28–253) is 2,918 words and the paper has 3 main figures, so it fits the Letter format, though with little room to spare.

I checked the key numbers against the figures and the SI, and they agree. These include the prediction intervals and I² (Table S2), the IBD top-five Asian ranking (Table S1; the sixth-ranked population is also Chinese), the GA bars (0.078/0.033 and 0.096/0.081, Table S4), the Fig. 3B shares, and the Fig. 3C FPR and sensitivity values. The title, highlights and GA summary match the evidence. The limitations are candid. The ethics statement is adequate.

Several placeholders remain: authors, contributions, COI, funding, the AI statement and the GitHub/Zenodo link. They are clearly marked, so I have not counted them as concerns, but they must be completed. The desk-rejection risk is low.

## Concerns

1. **MINOR: GA panel 2 tells a softer story than the text.** The "other cohort, same country" bars show a small gain in mean error (0.096 to 0.081). The text instead reports that the burn-in was "no better" on tail risk (0.30 vs 0.31), and the 0.096/0.081 numbers appear only in Table S4. The panel also leaves out the cross-site failure, where the burn-in was *worse* (0.057 to 0.078, 37% of burn-ins above 0.15). The panel subtitle says "sensitivity falls", but nothing in the panel shows sensitivity. *Resolve:* add an "other sub-site" bar pair, or plot P(FPR > 0.15) as in Fig. 3B. Then either drop "sensitivity falls" from the subtitle or add a one-line note on it ("3 case–control cohorts: 0.46 to 0.22").

2. **MINOR: the Fig. 3 title overclaims.** "Only calibration at the site of use restores the FPR" conflicts with two results in panel B: the burn-in did not reduce tail risk, and it failed across sub-sites. *Resolve:* see wording fix 4.

3. **MINOR: SI cross-references are out of date.** L258 says "Tables S1–S13", but the SI contains Table S14, which holds the local-versus-country results by population and the Holm summary. The text never cites S14. *Resolve:* change "S1–S13" to "S1–S14" and cite S14 at L138 and L244.

4. **MINOR: Fig. 2 taxon labels are still inconsistent.** "Firmicutes bacterium CAG 170" has no hyphen, unlike "CAG-520" and "CAG-182". Aeromonadales and Enterobacteriaceae are set roman while genus names are italic. Under bacteriological convention, names at every rank are italicised. *Resolve:* hyphenate the CAG number and apply one italics rule throughout.

5. **MINOR: the reproduction log is unchanged since round 6.** `logs/repro_fresh_clone_2026-11-24.log` still reruns only 5 of the roughly 20 scripts. It starts from the existing `data_cache` instead of running `rebuild_cache.sh`, records no commit hash and contains no `audit_numbers.py` output. The README now correctly names v8 and `make_figures_v7.py`. *Resolve:* before submission, run the full pipeline in the README order from a clean clone at the submission commit (1db69a8 or later). Log the commit, the diffs against the committed results, and the audit output. Then mint the Zenodo DOI and cite it in the Data Availability statement.

6. **MINOR: clinical framing.** The paper gives PPV (1.6% to 2.6%) but not the absolute numbers: false positives (colonoscopies) per 1,000 people screened, at the training cut-off versus the burn-in. Clinical readers will look for these. *Resolve:* add them as one SI line.

7. **MINOR: the highlights are long.** Highlight 4 runs to about 55 words and contains a parenthetical. *Resolve:* check the iMeta highlight length limit, then shorten it (see wording fix 5).

8. **MINOR: reference details.** Ref. 9 (Cell 2026) has no volume or pages, and ref. 24 is an arXiv preprint. *Resolve:* complete the citation details and check every 2026 reference against its DOI.

## Line-level wording fixes

1. L36: "More recent work reports that CRC classifiers lose calibration" → "Recent work reports that CRC classifiers lose calibration". Also rewrap this over-length line.
2. L146: delete the orphaned sentence "Augmentation was evaluated on the full set of locked populations." It repeats L141.
3. L258: "Tables S1–S13 are generated" → "Tables S1–S14 are generated".
4. L344 (Fig. 3 title): "Only calibration at the site of use restores the FPR" → "Calibration on the site's own people restores the average FPR; borrowed references do not".
5. L22–24 (Highlight 4): → "Within a site, a label-free burn-in on 100 people cut the average FPR error by about half (post hoc), but not the risk of an FPR above 0.15. It failed across sites and roughly halved sensitivity."
6. L19 (Highlight 2): "non-westernised populations were over-flagged by the T2D LASSO test" → "… by the T2D LASSO test (post hoc)".
7. L222: "is not a fixed property" → "is not a fixed property of the test".
8. Fig. 2D label: "Firmicutes bacterium CAG 170" → "Firmicutes bacterium CAG-170".
