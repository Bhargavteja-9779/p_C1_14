# HANDOFF — read this first

**Branch:** `claude/trusting-mayer-1ipvjz` (contains the full history of `claude/beautiful-goldberg-37nqmw`).
**Cycle:** 4 of 12 · **Pivots used:** 1 of 3 · **Phase:** review round 3 on manuscript v4

## NEXT ACTION
Review round 3 on manuscript v4 (Target_Journal_Submission/manuscript/manuscript_v4.md). Reports go to
Target_Journal_Submission/reviews/review_r3_0{1,2,3}_*.md. If they are missing (session died), relaunch three fresh
reviewers (statistics, novelty/prior art with web search, editor/clarity/reproducibility). Then triage into
reviews/round3_response.md, fix, and run round 4. Also pending: SI v4 tables (make_si_v4.py), flow diagram, workflow schematic.

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
| G9 reproducibility | unknown | no fresh-clone test yet |
| G10 review | fail | round 2: editor borderline, statistics MAJOR |
| G11 number audit | pass (lenient) | scripts/audit_numbers.py: 161/161 numbers of v4 match a result value (lenient: any value in results dirs) |

## Last decisions / failures
See state/decisions.md and journal/ENTRIES/. Failures so far (cycle 3, DEV): healthy-context residual, pooled atlas
reference, composition-matched reference all falsified; control augmentation gave no gain (locked, P=0.69).

## Commands
- Status: `python3 scripts/status.py`
- Rebuild data (fresh container, ~3 min): `scripts/rebuild_cache.sh`
- Atlas rerun: `cd Target_Journal_Submission/code/experiments/atlas && CMD_CACHE=$PWD/../../../../data_cache python3 -W ignore atlas_run.py`
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
