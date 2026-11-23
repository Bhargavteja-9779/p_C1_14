# PROGRESS (resume file)

Any agent continuing this work: read this file first, then `git log`. Work happened on branch
`claude/dreamy-clarke-rldxev` up to commit 1777afd; from 2026-11-23 (session 2) work continues on
`claude/affectionate-euler-dyczzb`. All deliverables live in `Target_Journal_Submission/`.
Commit + push after every phase (auto-save).

## Environment notes
- 4 CPU, 15 GB RAM, no GPU. Python 3.13. ScienceDirect HTML blocked (403); Crossref, OpenAlex, arXiv, UCI, PhysioNet, Zenodo, HF reachable.

## Rebuilding the environment (fresh container)
1. `pip install scikit-learn pandas pyreadr scipy matplotlib`
2. `curl -L -o /tmp/claude-0/eh/eh.sqlite3 https://experimenthub.bioconductor.org/metadata/experimenthub.sqlite3`
3. sampleMetadata: `curl -L https://raw.githubusercontent.com/waldronlab/curatedMetagenomicData/devel/data/sampleMetadata.rda`
   -> pyreadr -> `data_cache/sampleMetadata.csv` (22588 x 141).
4. `cd data_cache && python3 ../Target_Journal_Submission/code/scripts/fetch_cmd.py <studies>` (MetaCardis via
   `2022-10-19.MetaCardis_2020_a.relative_abundance`). Takes ~3 min.

## Phase log
- [x] Phase -1: repo skeleton created (2026-11-23)
- [x] STEP 0: journal landscape + 72-day evidence
- [x] STEP 1: benchmark 25 papers, level profile, style notes
- [x] STEP 2: real-life problem discovery
- [x] STEP 3: novelty map + scorecard (journal_selection/novelty_map.csv, 75 items; novelty_search_log.md)
- [x] Data lock (code/experiments/data_lock.md)
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
- STEP 1 running (background agent writing journal_benchmark.csv + benchmark_raw_notes.md).
- STEP 2 lead topic: operating-point (decision threshold) transfer of gut-microbiome disease classifiers to new sites.
  Data: curatedMetagenomicData via ExperimentHub (fetch_cmd.py -> data_cache/ra/*.csv, data_cache/sampleMetadata.csv; not committed).
  Cohorts: CRC 11, IBD 4, T2D 4 (incl. MetaCardis 2022 release), adenoma 5.
  PILOT (code/pilot/pilot_threshold_transfer.py): LOSO over 11 CRC cohorts, threshold set for 90% specificity on training
  out-of-fold controls. Realised specificity per held-out cohort: LASSO 0.79-1.00, RF 0.72-1.00; overdispersion vs binomial
  chi2 p=0.004 (LASSO), p=2e-7 (RF). => threshold drift is real, not sampling noise. Mean AUC LASSO 0.78, RF 0.82.
- STEP 3 running (background agent writing novelty_map.csv + novelty_search_log.md).
- 2026-11-23 (session 2) STEP 3 DONE. Closest prior art: SACSIM (Qiu et al. 2026 Biometrics, NP rule adapted with
  unlabeled target), Zhang et al. 2013 ICML (target+conditional shift, location-scale), MLLS/Saerens, Godau 2023/2025
  (prevalence-shift threshold re-setting, imaging), CaDC 2023 (sepsis), Tong 2018 NP umbrella (= our conformal baseline).
  No systematic microbiome threshold-drift report found -> framing novelty 4/5; site-shift mixture 2.5/5 as a method.
- DEV round 1: label-free site-shift v1 fails at low prevalence. Round 2: location-scale transport from few controls
  fails; conformal local-control threshold is the only one on target in every cohort, but P(FPR>0.15) ~ 0.2.
  See code/experiments/novelty_escalation_log.md.
- Round 3 direction: guarantees that matter per deployment (high-probability, not in-expectation) - (i) PAC/
  training-conditional local-control threshold, (ii) label-free contamination-bounded quantile of the unlabeled pool
  using only an upper bound on prevalence (known in screening), with DKW correction; (iii) hybrid.
