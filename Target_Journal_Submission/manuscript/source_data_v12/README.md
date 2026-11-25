# Source data for the figures of manuscript v12

Every panel is drawn only from these files. The scripts that draw them are in `code/experiments/atlas/`.

| Figure | Script | Files |
|---|---|---|
| Figure 1 (atlas; reused from v11) | v5/make_fig_atlas_v11.py | figure1/: atlas_perpop_strict_v5.csv (population metadata, from the fprcal package data), v5_perpop_strict.csv (FPR per classifier × population), v5_het_strict.csv (I², τ, prediction intervals), v5_popindex_strict_lasso.csv (false-alarm index), tests_v5.csv (AUROC) |
| Figure 2 (GMWI2 audit, mechanism) | v6/make_fig_gmwi2_v12.py | figure2/: gmwi2_published_training_perstudy.csv (A), gmwi2_perpop_full.csv (B), gmwi2_eastasia_taxa.csv (C), v6b_perstudy_naive/balanced.csv and v6b_results.json (D), gmwi2_results.json, counts_v12.json |
| Figure 3 (what a site can do) | v5/make_fig_deploy_v11.py | figure3/: v5_h4_units.csv (within-site burn-in), verify_power_v5.csv (verification power), deploy_v4_cc_summary.csv (contaminated burn-in) |

Figure 2 also reads `data_cache/sampleMetadata.csv` for country labels. The exact copy of that file is deposited as
`data/sampleMetadata.csv.gz`.
