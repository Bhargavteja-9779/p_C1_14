# HANDOFF — read this first

**Branch:** `claude/trusting-mayer-1ipvjz` (contains `claude/beautiful-goldberg-37nqmw` cycle-6 work, merged 2026-11-25; parallel duplicate files kept with suffix `_alt_trusting`).
**Cycle:** 5 of 12 · **Pivots used:** 1 of 3 · **Phase:** cycle 5 — upgrade after rejection (USER_DIRECTIVES.md)

## NEXT ACTION
CYCLE 6 (2026-11-25): added an EXTERNAL PUBLISHED-TEST audit + mechanism, the biggest novelty lift so far.
Done: plan v6/v6b (committed before running); GMWI2 coefficients extracted (whitelisted unpickler) = SData3; QC r=0.99;
G1,G2,G4 supported, G3 falsified; developers' own scores flag 0-84% of healthy TRAINING samples by study (I2 0.96), East
Asian median 0.64 vs 0.12 (P=5e-7); case-mix OR 6.7; v6b retrain: country-balancing removes 88% of the gap (B1,B2,B4
supported; B3 AUROC -0.040 failed by 0.01); within-study AUROC -0.020 (post hoc). Figure 2 v12 (figures_v12/
figure2_published_test). manuscript_v12.md drafted (~3,400 words = OVER the Letter band; 3 figures).
NEXT: (1) TRIM v12 to <=2,500 words OR move GMWI2 variance-decomposition detail to SI and keep Letter; decide Letter vs
Research Article (iMeta allows both; 3 figs + mechanism may suit a short Research Article). (2) Rebuild SI as ONE v12
document (round-9 editor MAJOR 1): S1 data/populations, S2 robustness, S3 taxa, S4 earlier CRC/IBD/T2D + cross-site
burn-in, S5 plans/deviations, S6 GMWI2 audit + case-mix (plans v6/v6b, QC, G1-G4, B1-B4), Tables S1-S20. (3) numbers_v12
audit script over every in-text number. (4) fill repo URL/Zenodo/back matter (needs user). (5) review round 10 (3 fresh
reviewers + blind scorecard) on v12; target significance 8+ (dim 1) now that a deployed test is included. (6) DEBIAS-M
still blocked (install denied). Figures 1 and 3 are reused from v11 (figure1_atlas, figure2_site->figure3_site).

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
