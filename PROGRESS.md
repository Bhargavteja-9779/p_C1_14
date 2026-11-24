# PROGRESS (resume file)

Any agent continuing this work: read this file first, then `git log`. Work happens on branch
`claude/sharp-meitner-guez1q` (session 3; fast-forwarded from `claude/zen-planck-p60lrt`; earlier: `claude/dreamy-clarke-rldxev`, same history up to 1777afd). All deliverables live in `Target_Journal_Submission/`.
Commit + push after every phase (auto-save).

## Environment notes
- 4 CPU, 15 GB RAM, no GPU. Python 3.13. ScienceDirect HTML blocked (403); Crossref, OpenAlex, arXiv, UCI, PhysioNet, Zenodo, HF reachable.

## Phase log
- [x] Phase -1: repo skeleton created (2026-11-23)
- [x] STEP 0: journal landscape + 72-day evidence
- [x] STEP 1: benchmark 25 papers, level profile, style notes
- [x] STEP 2: real-life problem discovery
- [x] STEP 3: novelty map + scorecard (2026-11-24; 76 verified rows)
- [x] Protocol pre-registration (code/experiments/protocol.md, 2026-11-24)
- [x] First working version (src/calibrate.py; dev rounds 1-4)
- [x] Novelty escalation loop (D6) rounds 1-4 (experiments/novelty_escalation_log.md); RF round 3 confirmation running
- [ ] Final experiments
- [~] Manuscript (draft v0.1 with placeholders; manuscript/manuscript.md)
- [ ] Reviews 1-11
- [ ] Final package

## Decisions (with reasons)
- 2026-11-23 STEP 0 (in progress): Measured received->accepted days from Crossref assertions (Springer/T&F/Wiley/IET) and
  PubMed history (Elsevier/OUP/biomed). ~95 hand-picked journals + automatic screen of 1378 non-Elsevier journals
  (OpenAlex 2yr citedness>4.5) + PubMed screen of Elsevier/IEEE journals. Raw files in journal_selection/raw/.
  Key finding: nearly no Q1 journal has p75<=72 for full research articles. Letters/short reports inflate speed.
  Research-only checks: Critical Care 66/85 (fail), iMeta research article 56/86 (fail), iMeta Letter 33/52 (pass),
  Ophthalmology & Therapy 52/70 (pass, but likely Q2 + clinical scope).
- 2026-11-23 STEP 0 DONE: iMeta (Wiley), Short Communication format (Letter median 33 d, P75 52 d; Research Article fails P75=86).
  See journal_selection/selected_journal.md.
- STEP 1 running (background agent writing journal_benchmark.csv + benchmark_raw_notes.md).
- STEP 2 lead topic: operating-point (decision threshold) transfer of gut-microbiome disease classifiers to new sites.
  Data: curatedMetagenomicData via ExperimentHub (fetch_cmd.py -> data_cache/ra/*.csv, data_cache/sampleMetadata.csv; not committed).
  Cohorts: CRC 11, IBD 4, T2D 4 (incl. MetaCardis 2022 release), adenoma 5.
  PILOT (code/pilot/pilot_threshold_transfer.py): LOSO over 11 CRC cohorts, threshold set for 90% specificity on training
  out-of-fold controls. Realised specificity per held-out cohort: LASSO 0.79-1.00, RF 0.72-1.00; overdispersion vs binomial
  chi2 p=0.004 (LASSO), p=2e-7 (RF). => threshold drift is real, not sampling noise. Mean AUC LASSO 0.78, RF 0.82.
- STEP 3 running (background agent writing novelty_map.csv + novelty_search_log.md).

## Session 2 (2026-11-24) resume notes
- Container was fresh: data_cache/ rebuilt. Metadata = curatedMetagenomicData `devel` data/sampleMetadata.rda
  (raw.githubusercontent.com; 22,588 x 141). ExperimentHub sqlite -> /tmp/claude-0/eh/eh.sqlite3.
  Rebuild: `pip install scikit-learn scipy pandas pyreadr matplotlib`; then in data_cache/: `python3 ../fetch_cmd.py <studies>`
  (MetaCardis via title `2022-10-19.MetaCardis_2020_a.relative_abundance`).
- Round 1 dev exploration (code/experiments/dev/explore_v1.py) re-run (its log was empty in the commit).
- STEP 3 result: no prior unlabeled threshold adaptation for microbiome classifiers, BUT the estimator (affine score
  calibration fitted to unlabeled 2-component score mixture) exists in speaker verification (Brummer & Garcia-Romero 2014).
  Close 2026 work: SACSIM (Biometrics; covariate-based NP adaptation), CRC-TrustBench (Front Microbiol; benchmark only),
  Bao 2026 Zenodo deposit (threshold transportability, needs labels; manuscript to re-check before submission).
  Scorecard: problem 3, method 2, evaluation 4, practical 4. => D6 direction: identifiability check / abstain, finite-sample
  FPR bound, hybrid unlabeled + few labelled controls; add baselines: per-site feature standardisation, MLLS-BCTS, DyS/HDy,
  2-Gaussian unsupervised calibration.

## Session 3 (2026-11-24 late) resume notes
- Fast-forwarded `claude/sharp-meitner-guez1q` to zen-planck a8509cb. data_cache rebuilt (19 cohorts) with the commands above.
- Smoke test passed. LOCKED final test launched once for lasso and rf (code/experiments/final/run_final.py, R=200).
  Next: analyze_final.py -> make_figures.py -> fill [[...]] in manuscript + SI -> reviews.
