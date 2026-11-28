# Statistical review, round 15 (r15_01): manuscript v17 (iMeta Letter)

**Reviewer focus:** the new GMHI audit (plan v7), plus spot checks of headline numbers against `v5/results` and `v6/results`.
**Files read:** `submission_final_v17/manuscript_v17.md`, `supporting_information_v17.md`, `code/experiments/atlas/v7/*` (protocol, `run_gmhi.py`, `posthoc_gmhi_names.py`, `inputs/GMHI.R`, all `results/*`), and selected v5/v6 result files.
**My own recomputations:** scripts in `/tmp/claude-0/r15_stats/` (`q2_titles.py`, `miss.py`). No repository file other than this review was changed.

**Score: 6/10**
**Recommendation: major revision.** The GMHI section needs work before submission. The rest of the manuscript checks out numerically.

---

## Summary

The re-implementation of GMHI is correct. The developers'-data results (H1, H2) are reproducible and correctly reported. The cMD part of the audit is a different matter. Its QC gate Q2, its "seen/unseen" split and its handling of zero scores all have problems. When I fixed the sample matching, the pre-specified Q2 gate **fails**: r = 0.795 against a criterion of ≥ 0.80. Under the plan's own rule, H3–H6 should then be reported as an implementation mismatch, yet the main text uses H5 (ρ = 0.70 with GMWI2) and H6 (−79%) as findings. The profiler-version caveat says the shift is 70% → 85%. In fact it is larger and depends strongly on the population (pooled 23% → 43%; per-study shifts of 0 to +74 points). The graphical-abstract summary still contains a stale, duplicated sentence from v16.

## Verified as correct

- **Plan timing.** `8b70d70` (plan and developer inputs, 03:32:30) comes before `32a7351` (code and results, 03:35:16) and `cbfa2b5` (manuscript, 03:37:50). The plan commit contains no score files or GMHI code. The usual caveat applies: git timestamps are set by the author, so pre-specification is self-certified rather than externally registered (see Minor 7).
- **GMHI re-implementation, line by line against `GMHI.R`.** All steps match:
  - Unclassified/virus removal: R's `contains()` ignores case and Python's `in` does not, but I checked that no species name in either the developers' or the cMD data differs by case, so this has no effect.
  - Column renormalisation, then `< 1e-5 → 0`.
  - Selection of the MH and MN species.
  - Shannon index over present species, using whole-profile proportions as in R.
  - R/7 and R/31, then `log10((ψMH+1e-5)/(ψMN+1e-5))`.
  - Q1: max |diff| = 4.9e-15. Confirmed.
- **Developers' data.** 4,347 profiles, each summing exactly to 100; no NaNs were coerced. α_GMHI = 0.236 (2,636 healthy, 20 ties counted as not flagged; disclosed). H1: 21 studies, I² = 0.962, range 0.030–0.897. H2: I recomputed the medians by hand, 0.673 (8 East Asian studies) vs 0.205 (13 others); one-sided Mann–Whitney P = 0.00067. The test is one-sided as the plan specified.
- **Holm.** Order H6 (0) < H4 < H5 < H2. Adjusted H2 = 0.00067 × 1, which is correct, so "one-sided P = 0.0007, Holm-adjusted" is right. H6's bootstrap P = 0 is correctly reported in the SI as P < 0.0002.
- **Other headline numbers match their result files:**
  - 36 strict populations and 6,525 people (and 55/8,160 in the full set).
  - 489 LASSO pairs: 45% with FPR > 0.15 and 24% with FPR < 0.05.
  - Populations with n ≥ 100: FPR range 0–0.873 (HF RF, LiuW_2016); LASSO maximum 0.770.
  - I² median 0.94, range 0.64–0.97; full set 28/28.
  - Share outside band: 15–16% expected vs 50–97% observed.
  - Burn-in −62% over 646 units.
  - GMWI2:
    - α = 0.208.
    - 44 studies, I² = 0.96. East Asian 0.64 (13 studies) vs others 0.12, two-sided P = 5.3e-7. The test is two-sided, as the text says.
    - 15 unseen populations, 1,914 people, r = 0.991. 12/15 outside the band vs 9% expected, Holm P = 1.8e-12.
    - East Asian 0.38 vs 0.06, P = 0.020; full set P = 0.065. Seen-vs-unseen P = 0.72.
    - G4: 0.21 → 0.04, −79%, CI 64–85%.
    - Case mix 1,574/2,522 vs 1,097/5,547.

---

## MAJOR issues

### M1. The "seen/unseen" accession matching fails silently, and Q2 rests on 2 of about 19 overlapping studies
**Where:** `run_gmhi.py` lines 55–67; SI S7 QC paragraph; SI table rows H3/H4; main text "on 101 samples profiled with both versions".

**What is wrong.** The developers' column "Sample Accession or Sample ID" holds BioSample accessions (SAMEA…/SAMN…). cMD `sample_id` holds study sample names, and cMD `NCBI_accession` holds run accessions (ERR/SRR). The two sets meet only in JieZ_2017 and YassourM_2016, the two cMD studies whose `sample_id` happens to be a BioSample accession. As a result:
- Many GMHI training studies are classified as "unseen". Examples from the developers' metadata: Schirmer 2016, Zeevi 2015, Le Chatelier 2013, Qin 2012, Qin 2014, HMP, Li 2017, Obregon-Tito, Rampelli, Liu 2016 (LiuW_2016, a strict population), Nielsen, Zeller, Vogtmann, Backhed and Feng.
- I matched cMD `sample_id` against the developers' "Sample title (ENA/SRA)", "Sample title (Paper)" and "Subject Id". This identifies at least 10 of the 34 "unseen" strict populations as GMHI training populations, which leaves ≤ 24 unseen. LiuW_2016 and Nielsen are probably also seen, though my match did not catch them.
- So the H3/H4 rows of the SI ("34 unseen populations") are wrong as labelled.

**Fix.** Match through the developers' sample titles or subject IDs, or map BioSample to run accessions through ENA. Then redo the seen/unseen split, Q2 and H3/H4, and record this as a deviation from the plan's operational definition.

### M2. Under correct matching, the pre-specified Q2 gate fails, so H5 and H6 should not be interpreted under the plan
**Where:** main text GMHI paragraph (ρ = 0.70) and burn-in paragraph (GMHI 0.26 → 0.05, −79%); SI S7 table rows H5/H6; Figure S2B and S2C.

**What I found.** On the 2,190 samples matched by title across 19 studies:

| Measure | Value |
|---|---|
| Pooled Pearson r | **0.795** (criterion ≥ 0.80; **fails**) |
| Spearman | 0.80 |
| Within-study (centred) r | 0.71 |
| Within-study r, JieZ_2017 and YassourM_2016 (the authors' own 101 samples) | 0.73 and 0.72 |

The reported r = 0.803 on 101 samples comes partly from the mean difference between the two clusters. With n = 101 its 95% CI (about 0.72–0.86) easily includes values below 0.80, so even as reported, "passed narrowly" is not a robust pass.

The plan says: "If Q2 fails, H3–H6 are reported as an implementation mismatch and not interpreted; H1–H2 stand."

**Fix.** Repeat Q2 on the full matched overlap. If it fails, as I find, keep H1–H2 in the main text and move H5/H6 to "not interpretable per plan", or at most post hoc. In that case remove "GMHI from 0.26 to 0.05 (−79%)", the ρ = 0.70 sentence and Figure S2B/C from the confirmatory narrative.

### M3. The profiler-version shift is understated and is not uniform across populations
**Where:** main text ("raised the share flagged from 70% to 85%"); SI S7; `posthoc_gmhi_names.py`.

**What I found.** On the 2,190 matched samples, the flag rate is 23% with the developers' MetaPhlAn2 profiles and 43% with cMD MetaPhlAn3 profiles: +20 points, not +15. More importantly, the shift varies by study (studies with n ≥ 20):

| Study | Flag rate, developers' profiles → cMD profiles |
|---|---|
| Obregon-Tito | 66% → 66% (no shift) |
| Schirmer | 10% → 15% |
| Zeevi | 9% → 32% |
| Li 2017 | 31% → 86% |
| Qin 2014 | 41% → 94% |
| Raymond | 17% → 91% |

Across these 12 studies, Spearman ρ between the cMD and developer flag rates is only 0.69. The profiler artefact therefore changes the ranking of populations, not only the level. Two claims rest on the assumption that it does not:
- The main-text reading that "the level … is not interpretable" while the cross-population correlation with GMWI2 is.
- The post hoc "ranking unchanged" (ρ = 0.996). This only tests renaming 4 MN species. It cannot address the 4 missing MH species, which are the main source of the shift.

**Fix.** Report the shift on the full overlap, per study. Remove or qualify "ranking unchanged". State that the cMD GMHI is a reduced index (3/7 MH and 30/43 MN species) whose bias depends on the population.

### M4. Zero scores (no MH and no MN species detected) are silently counted as "healthy"; the plan required separate reporting
**Where:** `run_gmhi.py` line 68 (`flag = sc < 0`); `gmhi_results.json` (cMD ties not reported); SI S7 (only the 20 developer-data ties are mentioned).

**What I found.**
- 139 strict and 172 full cMD samples have GMHI exactly 0.
- They cluster in non-industrialised populations, where the 3 surviving MH species (bifidobacteria) are rare:

| Population | Ties | FPR as reported | FPR with ties flagged |
|---|---|---|---|
| SmitsSA_2017 (Hadza) | 29/31 | 0.06 | 1.00 |
| RampelliS_2015 | 16/33 | 0.27 | 0.76 |
| PasolliE_2019 | 17/111 | 0.61 | 0.77 |
| RubelMA_2020 | 17/76 | 0.58 | 0.80 |

- This drives H5. GMWI2 also rates rural African populations as healthy. The 36-population ρ falls from **0.70 to 0.44** if ties are flagged, and to **0.46** if ties are excluded (both P < 0.01, but much weaker).
- A minor asymmetry in H6: the status-quo rule (`neg > 0`) never flags ties, while the burn-in rule (`neg >= tb`) can. The effect is negligible here (≤ 4.5% ties in H6 populations).

**Fix.** Report cMD ties per population as the plan requires. Give H5 (and H3/H4) with ties flagged, excluded and not flagged. Do not present ρ = 0.70 without this sensitivity analysis.

### M5. The graphical-abstract summary contains a stale, contradictory sentence
**Where:** manuscript top: "A published gut-health index labelled 64% of healthy people in its own East Asian training studies as non-healthy, against 12% elsewhere…"

**What is wrong.** This is the v16 GMWI2-only sentence. It sits directly after the new sentence on two indices. It also says "64%/12%", which are medians across studies, as if they were pooled shares.

**Fix.** Delete the sentence, or merge it with the new one, e.g. "median 64% vs 12% (GMWI2) and 67% vs 21% (GMHI) of studies…". Also check highlights and the cover letter for the same leftover.

---

## MINOR issues

1. **Missing-species list computed from one study only.** `run_gmhi.py` line 63 computes "missing species" from the first study only (AsnicarF_2021). The JSON therefore lists 15 MN species missing, while the SI says 13 are missing "in any of the 61 studies". I confirm that 13 is correct across all studies (Atopobium parvulum and Granulicatella adiacens do occur elsewhere). *Fix:* compute the union across studies and correct the JSON field.
2. **Not interpreting H4 is a post hoc deviation and should be called one.** Q2 "passed" as reported, so by the plan H4 should have been interpreted. *Fix:* in the SI table, label it "deviation from plan v7: not interpreted because…". Apply the same logic consistently to H5/H6, which carry the same confound (see M2–M4).
3. **The GMHI H6 gain is partly built in.** The status-quo error is inflated by the profiler artefact, and any local quantile rule removes a level offset. "Which also removed the shift caused by the profiling software" is true, but it means the −79% is not comparable to GMWI2's −79%. *Fix:* say so, and give the CI in the main text (−0.39 to −0.13), as is done for GMWI2. H6 populations also include GMHI training populations (JieZ_2017, QinJ_2012, Zeevi, Schirmer, Le Chatelier), which is acceptable for a within-site test but should be noted.
4. **H2 is in-sample.** It uses the data from which the MH/MN species were selected. The text's "in the developers' own data" is accurate, but "replication of the GMWI2 finding" should be worded as consistency within the training data. The cMD East Asian contrast (0.84 vs 0.41 unseen strict) is now uninterpretable because of M1/M3 and is rightly not used in the main text.
5. **East Asian word list.** The pre-specified list classes "Liu (2016) Mongolian Population" (S-8; FPR 0.075) as non-East-Asian. That is defensible as written, but it should be noted, because many Mongolian participants live in Inner Mongolia, China. Report H2 with S-8 reclassified as a sensitivity check (H2 would remain significant).
6. **Pearson is a fragile QC metric for GMHI.** GMHI is a log ratio with a floor near −5 when ψ = 0. Report Spearman and within-study agreement alongside it, and the sign agreement for the full overlap (78% on 2,190 samples vs 85% reported).
7. **Pre-specification rests only on git timestamps.** The plan, results and manuscript were committed within 5 minutes of each other, and git timestamps are set by the author. *Fix:* say in S5/S7 that pre-specification rests on repository timestamps only, and deposit the plan with a trusted timestamp (Zenodo/OSF) at submission.
8. **SI reference.** SI line 4 says "Tables S1–S25" are in the Supporting Tables file, but the package contains `si_tables_v16.md`. Rename it or regenerate it as v17 so that the file names match.

---

## Bottom line

The GMWI2 audit and the atlas numbers are solid and match the result files. The GMHI addition is useful only for H1–H2, which are correct. The cMD half (Q2, H3–H6) rests on a sample-matching failure, and corrected matching fails the plan's own QC gate. The profiler shift is understated and differs by population, and zero scores are handled in a way that drives the headline correlation with GMWI2. Fix M1–M5 before submission. The quickest fix is to keep GMHI to H1–H2 in the main text and report the rest as an implementation mismatch under the plan.
