# RECHECK PROGRESS
Finding at start: the first run stopped after journal selection, pilot and a data lock (no manuscript, no novelty map,
no full experiments). This run re-verifies what exists and completes the study.

- [x] Stage 1 journal re-verification -> KEEP iMeta Letter (stage1/stage1_journal_recheck.md)
- [x] Stage 2 problem story (stage2/problem_story.md) - reframed: label-free mixture is not new (other fields)
- [x] Stage 3 prior art: 85-paper novelty_map.csv; close calls Roschewitz 2023, lab-medicine indirect RIs, speaker-verification unsupervised calibration, CRC-TrustBench 2026, SACSIM 2026
- [ ] Stage 4 novelty elevation: round 1 done (H2, H4 falsified); round 2 (EB shrinkage) running
- [ ] Stage 5 experiments
- [ ] Stage 6 citations/claims
- [ ] Stage 7 manuscript
- [ ] Stage 8 reviews R1-R6
- [ ] Stage 9 audit
- [ ] Stage 10 final report

## Bugs found so far
1. ThomasAM_2019_c = 80 duplicated YachidaS_2019 samples (cross-cohort leakage in first-run locked set; RF AUROC 1.000).
2. fetch_cmd.py: MetaCardis title missing '.relative_abundance' -> cohort silently missing.
3. deploy_sim seeding used Python hash() (non-reproducible across processes) -> crc32.
4. First-run APC out of date (5,500 -> 4,960 USD); P75 52 -> 51.5.

## RESUME HERE (saved 2026-11-23, session paused by user)
- Branch: claude/quirky-mayer-0g4bp1. Data are NOT in git: re-create with
  `mkdir data_cache && cd data_cache` + download sampleMetadata.rda from
  raw.githubusercontent.com/waldronlab/curatedMetagenomicData/devel/data/sampleMetadata.rda -> sampleMetadata.csv (pyreadr),
  ExperimentHub sqlite to /tmp/claude-0/eh/eh.sqlite3, then `python fetch_cmd.py <studies>`
  (MetaCardis needs title `2022-10-19.MetaCardis_2020_a.relative_abundance`). Set CMD_CACHE=<repo>/data_cache.
- Large result CSVs (results/*.csv.gz) are gitignored: re-run
  `python experiments/deploy_sim.py --set dev --seeds 10 --reps 50 --out results/deploy_dev.csv.gz` (~16 min, 4 CPU).
- Round 2 (M8 empirical-Bayes shrinkage, H5/H6 in novelty_elevation_log.md) was running when paused; result not seen.
  Re-run: `--set dev --modes global --out results/deploy_dev_r2.csv.gz`, then `python experiments/analyze.py`.
- Next: decide final method list from dev -> run `--set locked` ONCE -> sanity.py -> figures -> manuscript (iMeta Letter,
  ~2,100 words, 2 figures) -> reviews R1-R6 -> audit -> final report.
- Planned framing (from evidence so far): finding (cut-off does not transfer across cohorts, overdispersed) + negative
  result (label-free fixes from ML/imaging fail or hurt) + practical rule (local controls, exact Beta law; ~75 known
  negatives keep P(FPR>0.15) <= 5.4%). The label-free mixture (M4) is NOT novel and did not work.
