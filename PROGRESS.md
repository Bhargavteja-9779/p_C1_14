# PROGRESS (resume file)

Any agent continuing this work: read this file first, then `git log`. Work happens on branch
`claude/hopeful-carson-p4zvqk` (earlier: `claude/dreamy-clarke-rldxev`). All deliverables live in `Target_Journal_Submission/`.
Commit + push after every phase (auto-save).

## Environment notes
- data_cache/ is NOT committed. Rebuild: download https://experimenthub.bioconductor.org/metadata/experimenthub.sqlite3 to
  /tmp/claude-0/eh/eh.sqlite3; sampleMetadata.rda from raw.githubusercontent.com/waldronlab/curatedMetagenomicData/master/data/
  -> data_cache/sampleMetadata.csv (pyreadr); then `cd data_cache && python3 ../fetch_cmd.py <studies>` (MetaCardis: pass
  `2022-10-19.MetaCardis_2020_a.relative_abundance`). Takes ~3 min.
- 4 CPU, 15 GB RAM, no GPU. Python 3.13. ScienceDirect HTML blocked (403); Crossref, OpenAlex, arXiv, UCI, PhysioNet, Zenodo, HF reachable.

## Phase log
- [x] Phase -1: repo skeleton created (2026-11-23)
- [x] STEP 0: journal landscape + 72-day evidence
- [x] STEP 1: benchmark 25 papers, level profile, style notes
- [x] STEP 2: real-life problem discovery
- [ ] STEP 3: novelty map + scorecard
- [ ] Protocol pre-registration
- [ ] First working version
- [ ] Novelty escalation loop (D6)
- [ ] Final experiments
- [ ] Manuscript
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
- STEP 1 DONE (journal_benchmark.csv, level profile, style notes).
- STEP 2 lead topic: operating-point (decision threshold) transfer of gut-microbiome disease classifiers to new sites.
  Data: curatedMetagenomicData via ExperimentHub (fetch_cmd.py -> data_cache/ra/*.csv, data_cache/sampleMetadata.csv; not committed).
  Cohorts: CRC 11, IBD 4, T2D 4 (incl. MetaCardis 2022 release), adenoma 5.
  PILOT (code/pilot/pilot_threshold_transfer.py): LOSO over 11 CRC cohorts, threshold set for 90% specificity on training
  out-of-fold controls. Realised specificity per held-out cohort: LASSO 0.79-1.00, RF 0.72-1.00; overdispersion vs binomial
  chi2 p=0.004 (LASSO), p=2e-7 (RF). => threshold drift is real, not sampling noise. Mean AUC LASSO 0.78, RF 0.82.
- STEP 3 running (background agent writing novelty_map.csv + novelty_search_log.md).
- 2026-11-23 (session 2): container reset; data cache rebuilt; STEP 3 novelty search re-run (previous run never committed);
  dev round 1 (code/experiments/dev/explore_v1.py) running on the 8 DEV CRC cohorts only.
- 2026-11-23 AUTHOR DECISIONS (fixed, do not change): code available on request; no funding; no competing interests.
  Wording in Target_Journal_Submission/manuscript/back_matter.md — use verbatim.
