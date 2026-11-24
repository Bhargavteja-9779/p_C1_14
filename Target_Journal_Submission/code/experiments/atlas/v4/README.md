# v4 analysis (manuscript v4) — how to reproduce

Plan written before running: `protocol_v4.md` (deviations D1–D4 at its end). All outputs land in `results/`.
Every script that writes results refuses to run if its output already exists, so committed results are never
overwritten. To reproduce from scratch, move `results/` aside first.

## 1. Data (≈5 min, ~1 GB)
From the repository root:
```
scripts/rebuild_cache.sh            # pinned packages, committed metadata (sha256-checked), ExperimentHub 2021-03-31 tables
export CMD_CACHE=$PWD/data_cache
```

## 2. Run order (from this directory; 4 CPUs, ~25 min total, no GPU)
| step | script | writes | time |
|---|---|---|---|
| P0 de-duplication | `dedup.py` | duplicates.csv, excluded_samples.txt, dropped_studies.txt | 1 min |
| P2/P7 atlas | `atlas_v4.py` | atlas_rows_v4.csv.gz, atlas_coefs_v4.csv | 2 min |
| P2/P3 statistics | `analyse_atlas_v4.py` | heterogeneity_v4.csv, covariates_v4.csv, atlas_perpop_v4.csv | 1 min |
| A1–A5 | `hypotheses_v4.py` | hypotheses_v4.csv | 1 min |
| P8 taxa | `taxa_v4.py` | taxa_shift_v4.csv, taxa_top_v4.csv | <1 min |
| P4–P6 burn-in | `deploy_v4.py` | deploy_v4_healthy.csv.gz, deploy_v4_cc.csv.gz | 6 min |
| summaries | `summarise_v4.py` | summary_v4.json, summary_v4_table.csv, deploy_v4_units.csv, deploy_v4_cc_summary.csv, ppv_v4.csv | 1 min |
| augmentation | `control_augmentation_v4.py` then `h2h_v4.py` | control_augmentation_v4.csv, h2h_v4.json | 12 min |
| multiplicity | `holm_v4.py` | holm_v4.csv | <1 s |
| counts | `counts_v4.py` | counts_v4.json | <1 min |
| figures | `make_figures_v4.py` | ../../../../manuscript/figures_v4/ | <1 min |
| SI tables | `make_si_v4.py` | ../../../../manuscript/si_tables_v4.md | <1 min |

Then from the repository root: `python3 scripts/audit_numbers.py Target_Journal_Submission/manuscript/manuscript_v4.md`
checks that every number in the manuscript matches a value in the result files.

## Software
Python 3.13; package versions pinned in `Target_Journal_Submission/code/requirements.txt`. Random seeds are derived
from names (crc32 of disease/model/population), so reruns give identical numbers.
