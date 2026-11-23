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
