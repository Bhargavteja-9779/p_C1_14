# HANDOFF — read this first

**Branch:** `claude/bold-clarke-qsp9pf` (2026-11-28: fast-forwarded onto `claude/sharp-meitner-guez1q`, the most recent line, v17; bold-clarke's own earlier commits were already ancestors). Earlier lines: sharp-meitner <- zen-planck <- festive-cori <- trusting-mayer <- beautiful-goldberg.
**Cycle:** 5 of 12 · **Pivots used:** 1 of 3 · **Phase:** final package v22 (USER_DIRECTIVES rule 3: 9/10 dimensions >= P75; clarity borderline)

## NEXT ACTION
Package ready: Target_Journal_Submission/submission_final_v22/ (see FINAL_REPORT.md). G10 met (blind panels r19 7/8/7
and r20 7.5/8/7, all minor). Only open quality item: clarity scored 7/8/6 vs P75 7.25 in r20; v22 cut main-text
numerals to 134 but was not re-scored. Optional next step: one blind editor check of v22 for clarity. Open technical
items (not required): Fig 1A marker overlap, single build entry point, fail-hard on missing studies.
BLOCKED ON USER (author-only): author list/affiliations, CRediT, COI, funding, AI-use statement (must mention simulated
review rounds named in plans v6/v7), public repo + Zenodo DOI + tagged fprcal release, right of reply to GMWI2 and GMHI
developers, suggested reviewers, iMeta guideline check, Poyet 2026 full-text check.

## One-line summary
- **Journal:** iMeta (Wiley), Short Communication; Letter received→accepted median 33 d / P75 52 d (n=67, verified via PubMed). JIF/quartile Q1 per secondary sources only (JCR not reachable: UNVERIFIED). Fallback: Frontiers in Microbiology (59/79 d).
- **Topic:** gut-microbiome disease classifiers (CRC/IBD/T2D) have a false-positive rate that depends on the population they are used in.
- **Hypothesis:** FPR at a fixed cut-off varies far beyond sampling noise across healthy populations (cohort-level effect), and a label-free burn-in self-calibration on ~100 local people restores the target FPR where fixes based on other cohorts do not.

## What is running
Nothing. (No GPU; everything is CPU, minutes per job.)

## Compute
Cycle 4: ~0.5 h CPU wall-clock of 15 h (dedup 1 min, atlas 2 min, deploy ~6 min, augmentation ~12 min). Global: earlier cycles not logged (UNVERIFIED, all CPU, small). Ceiling 120 h.

## Gate status (honest)
| Gate | Status | Evidence / gap |
|---|---|---|
| G1 journal | partial | iMeta Letter passes the 72-day rule; JCR quartile not verified first-hand |
| G2 prior art | pass (to re-check) | RECHECK/stage3 novelty_map.csv (85 records) + journal_selection/novelty_map.csv (50) |
| G3 novelty ≥20/25 | unknown | self-score 24/30 (old scale); editor: "burn-in rule = adaptation, not a methods advance" |
| G4 baselines | partial | status quo, control augmentation, pooled/country/matched references, ComBat-style ALIGN; no MMUPHin/DEBIAS-M |
| G5 confirmation win | partial | burn-in beats status quo: strict set 11/11 populations, Holm P=0.0098; within-site non-random Holm P=0.022; but pre-stated H-NX1 (≥50%) missed (48%); 7-population locked tests not Holm-significant |
| G6 ablation | n/a / partial | burn-in vs PAC vs augmentation |
| G7 generalization | partial | 3 diseases × 2 models × ~60 populations; needs strict subset + non-random splits |
| G8 leakage | pass | global dedup v4/dedup.py (119 samples removed) |
| G9 reproducibility | pass | full fresh-clone rerun, 30/30 result files identical (logs/repro_full_2026-11-24.log) |
| G10 review | in progress | r3: 7/6/5; r4: 7/8/incomplete; r5: stats 7 minor, novelty 8 minor, editor 7.5 minor (MAJOR wording items fixed) -> v7; r6: 7/8/7.5 minor (3 MAJOR, fixed in v8); r7: 8/8/8 minor, NO MAJOR (1st clean) -> v9; r8: 7/8/8 minor, NO MAJOR (2nd clean) -> G10 met -> v10 |
| G11 number audit | pass (lenient) | scripts/audit_numbers.py: 161/161 numbers of v4 match a result value (lenient: any value in results dirs) |

## Last decisions / failures
See state/decisions.md and journal/ENTRIES/. Failures so far (cycle 3, DEV): healthy-context residual, pooled atlas
reference, composition-matched reference all falsified; control augmentation gave no gain (locked, P=0.69).

## Commands
- Status: `python3 scripts/status.py`
- Rebuild data (fresh container, ~3 min): `scripts/rebuild_cache.sh`
- Reproduce v4: see Target_Journal_Submission/code/experiments/atlas/v4/README.md (run order)
- Supervisor (local machine only): start `nohup scripts/supervisor.sh &`; stop `touch state/STOP`; logs `logs/supervisor.log`.
  Remove autostart: nothing installed (cloud container is ephemeral).
- Move account: everything is pushed to GitHub; in the new session paste BOOTSTRAP_PROMPT.txt.

## Known problems
- ScienceDirect HTML blocked (403); Crossref/OpenAlex/PubMed/arXiv reachable.
- Do NOT re-run `deploy_eval.py` for the original v3 locked analysis; the corrected re-analysis has its own script (R2.4+).
- data_cache/ is not in git.

## File map
- Persistence: HANDOFF.md, MASTER_PROMPT.md, BOOTSTRAP_PROMPT.txt, state/, journal/ENTRIES/, scripts/
- Older resume notes: PROGRESS.md (sessions 1-3)
- Journal selection: Target_Journal_Submission/journal_selection/
- Prior art: RECHECK/stage3/, Target_Journal_Submission/journal_selection/novelty_map.csv
- Code: Target_Journal_Submission/code/{src,experiments/atlas}
- Manuscript v3: Target_Journal_Submission/manuscript/manuscript_v3.md, figures_v3/
- Reviews: Target_Journal_Submission/reviews/ (round 1, round 2 reports)
