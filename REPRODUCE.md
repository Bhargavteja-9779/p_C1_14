# Reproducing the submitted manuscript (v22; package `Target_Journal_Submission/submission_final_v22/`) (FPR atlas, GMWI2 audit, site burn-in, fprcal)

Everything runs on CPU (4 cores used where parallel); no GPU. Paths below are relative to the repository root unless a
step says `cd`. Result scripts write to their own `results/` folder; several refuse to run if their output already
exists (`atlas_v4.py`, `atlas_v5.py`, `deploy_v4.py`, `dedup.py`, `control_augmentation_v4.py`, `replicate_v5.py`,
`numbers_v11.py`), so to regenerate from scratch move `results/` aside first and compare afterwards (see
`scripts/repro_full.sh` for the v4 version of that check).

Run times: measured in the full fresh-clone rerun (`logs/repro_full_2026-11-24.log`) or in this session where given;
"not logged" means the step was run but its wall time was not recorded (all jobs take minutes on CPU).

## 0. Environment (≈5 min)

```bash
conda env create -f environment.yml && conda activate fprcal-atlas     # Python 3.13 + pinned packages + fprcal (editable)
# or: python3.13 -m venv .venv && . .venv/bin/activate && pip install -r Target_Journal_Submission/code/requirements.txt \
#     && pip install pytest==9.1.1 -e Target_Journal_Submission/code/tool
```
Reported runs: Python 3.13.18, scikit-learn 1.9.1, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0,
matplotlib 3.11.2, geopandas 1.2.0 (Figure 1 map only). Random seeds are fixed or derived from names (crc32), so reruns
give identical numbers.

## 1. Data: curatedMetagenomicData (≈3–5 min, ~1 GB)

```bash
scripts/rebuild_cache.sh                 # -> data_cache/ (not in git)
export CMD_CACHE=$PWD/data_cache
ls data_cache/ra | wc -l                 # must be 61
```
- `sampleMetadata.csv` is the committed copy `data/sampleMetadata.csv.gz` (decompressed to `data_cache/sampleMetadata.csv`; the sha256 in `data/sampleMetadata.sha256` is of the decompressed CSV).
- Relative-abundance tables (MetaPhlAn3; full clade strings, all ranks, as row names) are downloaded from Bioconductor
  ExperimentHub, release 2021-03-31 (MetaCardis_2020_a: 2022-10-19), by `Target_Journal_Submission/code/scripts/fetch_cmd.py`
  (study list: CRC/IBD/T2D case–control cohorts + `Target_Journal_Submission/code/experiments/atlas/healthy_studies.txt`).
  BedarfJR_2017 and PehrssonE_2016 are not in that release and are skipped by design.
- `fetch_cmd.py` at the repository root is the original copy of the downloader (hard-coded ExperimentHub index path);
  use the version under `code/scripts/` via `rebuild_cache.sh`.
- **Check the count.** The atlas and GMWI2 scripts skip any study whose table is missing without stopping, so an
  incomplete cache silently gives different numbers.

## 2. De-duplication and the v4 deployment simulation (≈8 min)

```bash
cd Target_Journal_Submission/code/experiments/atlas/v4
python dedup.py            # 13 s   duplicates.csv, excluded_samples.txt, dropped_studies.txt (used by v5 and v6)
python deploy_v4.py        # 434 s  contaminated burn-in simulation (Figure 3B)
python summarise_v4.py     # 8 s    deploy_v4_cc_summary.csv
```
The rest of the v4 pipeline (earlier manuscript versions) is in `v4/README.md`.

## 3. Atlas: 14 tests × LASSO/RF × 36 strict healthy populations (v5)

```bash
cd Target_Journal_Submission/code/experiments/atlas/v5
python atlas_v5.py         # not logged (v4 analogue: 113 s, 4 processes)  atlas_rows_v5.csv.gz, tests_v5.csv, coefs_v5.csv
python analyse_v5.py       # not logged  v5_perpop_*, v5_het_*, v5_popindex_*, v5_h4_units.csv (within-site burn-in), v5_summary.json
python verify_power_v5.py  # not logged  verify_power_v5.csv/.json (Figure S1B)
python explore_v5.py; python replicate_v5.py; python genus_axis_v5.py           # exploratory / replication (SI)
python h4_cluster_ci_v11.py; python h2_sampling_v13.py; python numbers_v11.py   # post hoc numbers quoted in the text
python export_models_v11.py  # refits the 14 LASSO tests, writes code/tool/fprcal/data/models_lasso_v5*.csv, asserts scores = atlas
```
Model features: MetaPhlAn3 relative abundances of all clades (kingdom to species) present in > 5% of training samples
(`v5/common_v5.py`; clade strings reduced to their last level).

## 4. GMWI2 audit (v6; run from the v6 folder, scripts use relative paths)

```bash
cd Target_Journal_Submission/code/experiments/atlas/v6
# optional: python extract_gmwi2.py <gmwi2 model file>  (coefficients already committed: gmwi2_coefficients.json)
python run_gmwi2.py                    # gmwi2_rows.csv.gz, gmwi2_perpop_{full,strict}.csv, gmwi2_results.json
python posthoc_published_scores.py     # gmwi2_published_training_perstudy.csv (developers' published scores, inputs/)
python posthoc_eastasia.py             # gmwi2_eastasia_taxa.csv, gmwi2_eastasia.json
python posthoc_casemix.py
python run_v6b.py && python analyse_v6b.py     # country × label reweighting: v6b_loso_scores, v6b_perstudy_*, v6b_results.json
python posthoc_v6b_within.py; python posthoc_v6b_withincountry.py
python run_v6c.py; python corrected_boot_v13.py; python holm_v6_v13.py
python counts_v12.py; python numbers_v14.py; python posthoc_eastasia_strict_v15.py
```
GMHI audit (plan v7) and the post hoc checks added after the final reviews:
```bash
cd ../v7 && python run_gmhi.py && python posthoc_gmhi_matching.py && python posthoc_gmhi_names.py \
  && python posthoc_gmhi_gmwi2_overlap.py && python posthoc_r16_sensitivity.py && python make_fig_gmhi_v17.py
cd ../v5 && python posthoc_r17_numbers.py && python posthoc_r18_checks.py
python posthoc_r19_foldmodel.py && python posthoc_r19_numbers.py   # mean-logit fold-model check, ~25 min on 4 CPUs (needs data_cache)
python posthoc_r20_perfold.py && python posthoc_r20_numbers.py    # per-fold flag check (S2.3), ~25 min
```
`v7/results/README.md` lists which v7 output fields are superseded.
Run times: not logged (each minutes on CPU). Inputs from Chang et al. 2024 are in `v6/inputs/` (see `SOURCE.md`).

## 5. Figures (12 s)

```bash
cd Target_Journal_Submission/code/experiments/atlas
python v5/make_fig_atlas_v21.py         # Figure 1 (v21: panel D)  -> manuscript/figures_v21/
python v6/make_fig_gmwi2_v21.py         # Figure 2 (v21: top-five taxa marked, panel D legend)
python v5/make_fig_site_v22.py          # Figure 3 and Figure S1 (v22 wording)
python v7/make_fig_gmhi_v17.py          # Figure S2 (GMHI)
python make_graphical_abstract_v22.py   # graphical abstract (v22)
```
The v22 package `figures/` folder holds the exact files submitted. `python scripts/check_figures_v22.py` reruns every figure script and compares each
PNG pixel by pixel with the package copy (2026-11-28: 6/6 identical; `logs/check_figures_v22.txt`). The pixel-identical rebuild below covers the v16
figures; Figures 1 and 2 (v21), Figure 3 (v17), Figure S2 and the graphical abstract are regenerated by the scripts above.
Outputs: `Target_Journal_Submission/manuscript/figures_v15/` (Figures 1, 3, S1; identical copies in `figures_v16/`), `figures_v16/` (Figure 2) and `.../graphical_abstract/`. Panel → script → input
file table and copies of every input: `Target_Journal_Submission/manuscript/source_data_v16/README.md`. To redraw from
those copies only, without touching the repository, and compare pixel by pixel with the published PNGs:
```bash
python Target_Journal_Submission/manuscript/source_data_v16/rebuild_figures.py    # 2026-11-25: 5/5 identical
```

## 6. Number audit (<1 min)

```bash
A=Target_Journal_Submission/code/experiments/atlas
python scripts/audit_numbers.py Target_Journal_Submission/submission_final_v22/manuscript_v22.md \
  $A/v4/results $A/results $A/v5/results $A/v6/results $A/v7/results $A/v3 Target_Journal_Submission/journal_selection
```
Last recorded result: `logs/audit_manuscript_v22.md.txt` (0 unmatched). The check is lenient: a number passes if any
result value rounds to it.

## 7. fprcal tests (≈40 s)

```bash
cd Target_Journal_Submission/code/tool && pip install -e . && python -m pytest -q tests     # 19 passed
```
The `score` tests use `tests/data/cmd_ZellerG_2014_6samples.csv` (6 healthy samples, cMD format) and check that the
scores equal the atlas scores (`atlas_rows_v5.csv.gz`).

## Author actions not covered here
GitHub URL, Zenodo DOI and the tagged fprcal v0.1.0 release.
