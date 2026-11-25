# Source data for the figures of manuscript v15

Every panel of the v15 figures is drawn only from the files in this folder (byte-identical copies of the repository
files the scripts read). Scripts are in `Target_Journal_Submission/code/experiments/atlas/` (paths below are relative
to it). Supersedes `source_data_v12/` (v15 changed Fig 2B to the strict set, split old Fig 3 into Fig 3 and Fig S1, and
added the graphical abstract).

**Check:** `python Target_Journal_Submission/manuscript/source_data_v16/rebuild_figures.py` copies the unchanged v15
scripts into a temporary mirror of the repository that contains only these files (plus the fprcal package code), runs
them and compares the PNGs with `manuscript/figures_v15/` and `manuscript/graphical_abstract/`. Result (2026-11-25,
environment.yml): all five PNGs pixel-identical; 12 s.

## Figure / panel → script → input files

| Figure | Panel | Script | Input file(s) (folder in this directory) | Produced by (upstream) |
|---|---|---|---|---|
| Figure 1 | A map: false-alarm index of 36 populations | v5/make_fig_atlas_v15.py | figure1/v5_popindex_strict_lasso.csv; figure1/atlas_perpop_strict_v5.csv (country, lifestyle); figure1/v5_perpop_strict.csv (n); figure1/ne_110m_admin_0_countries.zip (Natural Earth 1:110m, public domain; sha256 in .sha256) | v5/analyse_v5.py; fprcal package data (`code/tool/fprcal/data/`) |
| Figure 1 | B heatmap: realised FPR, 14 LASSO tests × 36 populations | v5/make_fig_atlas_v15.py | figure1/v5_perpop_strict.csv; figure1/v5_het_strict.csv (row order: ascending τ); figure1/v5_popindex_strict_lasso.csv (column order); figure1/atlas_perpop_strict_v5.csv (labels) | v5/atlas_v5.py → v5/analyse_v5.py |
| Figure 1 | C 95% prediction intervals, LASSO and RF | v5/make_fig_atlas_v15.py | figure1/v5_het_strict.csv | v5/analyse_v5.py |
| Figure 1 | D AUROC vs τ | v5/make_fig_atlas_v15.py | figure1/v5_het_strict.csv (Spearman ρ computed in the script) | v5/analyse_v5.py |
| Figure 2 | A GMWI2 training studies (published scores) | v6/make_fig_gmwi2_v15.py | figure2/gmwi2_published_training_perstudy.csv; figure2/gmwi2_results.json (training FPR, `alpha_gmwi2`) | v6/posthoc_published_scores.py; v6/run_gmwi2.py |
| Figure 2 | B 15 unseen strict populations | v6/make_fig_gmwi2_v15.py | figure2/gmwi2_perpop_strict.csv (rows with `seen == False`); figure2/sampleMetadata.csv.gz (country; same file as `data/sampleMetadata.csv.gz`, sha256 of the unzipped CSV in sampleMetadata.sha256); figure2/gmwi2_results.json | v6/run_gmwi2.py |
| Figure 2 | C taxa behind the East Asian gap | v6/make_fig_gmwi2_v15.py | figure2/gmwi2_eastasia_taxa.csv (first 8 rows) | v6/posthoc_eastasia.py |
| Figure 2 | D country × label reweighting | v6/make_fig_gmwi2_v15.py | figure2/v6b_perstudy_naive.csv; figure2/v6b_perstudy_balanced.csv; figure2/v6b_results.json; figure2/gmwi2_results.json | v6/run_v6b.py → v6/analyse_v6b.py |
| Figure 3 | A within-site burn-in vs training cut-off, 28 classifiers | v5/make_fig_site_v15.py | figure3/v5_h4_units.csv | v5/analyse_v5.py (H4) |
| Figure 3 | B sensitivity price (contaminated burn-in) | v5/make_fig_site_v15.py | figure3/deploy_v4_cc_summary.csv (N = 100, π = π_max > 0) | v4/deploy_v4.py → v4/summarise_v4.py |
| Figure S1 | A exact risk of a high FPR vs burn-in size | v5/make_fig_site_v15.py | none: computed by `fprcal.fpr_law`, `k_expected`, `k_pac` (code/tool/fprcal/core.py) | — |
| Figure S1 | B power of local verification | v5/make_fig_site_v15.py | figureS1/verify_power_v5.csv (LASSO rows) | v5/verify_power_v5.py |
| Graphical abstract | 1 FPR per test, populations ≥ 100 people | make_graphical_abstract_v15.py | graphical_abstract/v5_perpop_strict.csv | v5/analyse_v5.py |
| Graphical abstract | 2 GMWI2 training studies, East Asian vs other | make_graphical_abstract_v15.py | graphical_abstract/gmwi2_published_training_perstudy.csv | v6/posthoc_published_scores.py |
| Graphical abstract | 3 burn-in vs training cut-off | make_graphical_abstract_v15.py | graphical_abstract/v5_h4_units.csv | v5/analyse_v5.py |

Notes
- `make_fig_site_v15.py` draws Figure 3 and Figure S1 in one run, so it needs the files of both `figure3/` and `figureS1/`.
- Graphical-abstract files are identical copies of the Figure 1/2/3 files of the same name.
- Figure 1 needs `geopandas` (pinned in requirements.txt / environment.yml).
- Outputs: `manuscript/figures_v15/figure1_atlas.*`, `figure2_published_test.*`, `figure3_site.*`,
  `figureS1_site_methods.*`; `manuscript/graphical_abstract/graphical_abstract_v15.*`.
- If the v16 figure scripts (`v6/make_fig_gmwi2_v16.py`, `make_graphical_abstract_v16.py`, in progress) replace the v15
  ones, re-check this table; as of 2026-11-25 both read the same files as their v15 counterparts.

## v16 changes (same inputs)
Manuscript v16 redraws two items with layout changes only; they read exactly the input files listed above:
- Figure 2 (band 0.10–0.31 shaded in panel B; italic taxon names in C): `v6/make_fig_gmwi2_v16.py` →
  `manuscript/figures_v16/figure2_published_test.{png,pdf}`.
- Graphical abstract (no overlapping labels): `make_graphical_abstract_v16.py` →
  `manuscript/graphical_abstract/graphical_abstract_v16.{png,pdf}`.
Figures 1, 3 and S1 are unchanged from v15 (copied to `manuscript/figures_v16/`).
