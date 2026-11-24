# Review round 6, report 03: handling editor (manuscript v7)

**Score:** 7.5/10  **Decision:** Minor revision

Most round-5 items are fixed. Highlight 4 no longer says "case mix", the strict burn-in sensitivity (0.13–0.15) is now reported, the worked example is correct (k = ⌈101 × 0.901⌉ = 92), and the GA bar now matches Table S12 ("labelled local controls"). The story is clear and the limitations are candid. The ethics statement is adequate. The placeholders for authors, contributions, COI, funding, AI use and the GitHub/Zenodo link are clearly marked. They are not scientific concerns, but they must be completed before submission. Desk-rejection risk is low, with two exceptions: the length (concern 3) and the GA–text mismatch (concern 1).

## Concerns

1. **MAJOR: the GA summary contradicts GA panel 2.** The summary (L12–13) says "recalibrating on about 100 *unlabelled* people … brought it close to target, at the cost of about half the sensitivity". Panel 2 shows "100 *labelled* local controls" (random draws, 8 populations, post hoc). Readers see the picture and the sentence together. The halved sensitivity comes from three case–control cohorts (Fig. 3C), not from this panel. *Resolve:* rewrite the last GA sentence to match panel 2 ("100 local controls (random draws) put 79% of pairs in band, versus 46% for same-country cut-offs"). Then add one clause: "label-free burn-in worked within sites, failed across sites, and in 3 cohorts halved sensitivity". Alternatively, replace panel 2 with Fig. 3B's within-site versus cross-site contrast, which is the paper's actual message.

2. **MAJOR: the Fig. 1 legend does not match the figure.** The legend says "Orange band: 95% random-effects prediction interval". In the figure that band is grey; orange is used only for the non-westernised diamonds. *Resolve:* change the legend to "Grey band". This also settles round-5 item 6.

3. **MINOR (format risk): length.** The main text (L30–262, including headings and the table) is about 2,940 words, right at the 3,000 limit. Any added text will push it over. *Resolve:* trim the redundant Holm bullet list (L245–256) to one sentence that cites Table S10. Compress the introduction's literature run (L39–46).

4. **MINOR: Fig. 2 labels are still unfixed** (round-5 item 5). They read "Prevotella sp CAG 520" and "Roseburia sp CAG 182". The text says "*Collinsella massiliensis*" but the panel says "[Collinsella] massiliensis". The text says "*Catenibacterium*" but the panel says "Catenibacterium mitsuokai". Higher-rank names (Enterobacteriaceae, Aeromonadales) are set roman while genera are italic, which is inconsistent. *Resolve:* write "sp.", match the text to the panel labels, and italicise only genus and species names.

5. **MINOR: the random-split counts differ.** Fig. 3B labels the random split "13 pop." The text (L176) gives 7 locked and 11 strict-set populations at N = 100. *Resolve:* state in the Fig. 3B legend that the random split uses the same 13 populations as the accession-order design, or align the counts.

6. **MINOR: Highlights are still dense.** Highlight 4 still carries two parenthetical statistics. *Resolve:* move "(post hoc grouping; pre-stated pooled test 48% …)" to the main text and keep the 57% with the word "post hoc".

7. **MINOR: the fresh-clone reproduction is partial.** `logs/repro_fresh_clone_2026-11-24.log` covers 5 of roughly 15 scripts. It uses a pre-existing `data_cache` rather than a run of `rebuild_cache.sh` from scratch. It records no commit hash. It includes no `audit_numbers.py` output. Augmentation, taxa, the r3/r5 post hoc analyses, the figures and the SI tables were not regenerated. The README heading still reads "manuscript v4". *Resolve:* rerun from a clean clone at commit d294fec, starting with `rebuild_cache.sh` and following the full README order through `audit_numbers.py`. Log the commit, date and diff summary. Update the README heading. Mint the Zenodo DOI.

8. **MINOR: clinical framing.** The paper states that PPV rose from 1.6% to 2.6% (L212). Clinical readers would also want the absolute numbers: how many colonoscopies per 1,000 people screened at the training cut-off versus the burn-in. *Resolve:* add one SI line. It need not go in the main text, because of the word limit.

## Line-level wording fixes

1. L12–13: "recalibrating on about 100 unlabelled people from the same site brought it close to target" → "a label-free burn-in on the first ~100 people at the same site brought it close to target within that site, but not across sites".
2. L340–341 (Fig. 1 legend): "Orange band: 95% random-effects prediction interval" → "Grey band: 95% random-effects prediction interval".
3. L39: "More recent work reports that CRC classifiers lose calibration" → "Recent work reports that CRC classifiers lose calibration" (the line is also over-length; rewrap it).
4. L151: "Augmentation was evaluated on the full set of locked populations." The sentence is orphaned mid-paragraph. Move it to L146 or delete it.
5. L211: split the over-long line at "This is the cost of making the stated FPR true."
6. L224: "is not a fixed property" → "is not a fixed property of the test".
7. L353 (Fig. 3 title): "Only calibration at the site of use restores the FPR" → "Calibration on people from the site of use restores the FPR; borrowed references do not".
8. L362: "Other sub-site: another city or country of the same study." → "Other sub-site: another city or country of the same study (2 studies, 5 sub-sites)."
