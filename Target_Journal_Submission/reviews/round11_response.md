# Response to review round 11 (manuscript v13 -> v14)

## Statistics (6/10, major)
M1 ACCEPTED, verified independently (posthoc_v6b_withincountry.py): the pre-specified weight 1/n(country,label) equalises
every country x label group; label balance within countries alone, keeping each country's share, removed 37% of the gap
(0.19, CI −0.04 to 0.31) vs 88% (0.46, CI 0.18–0.58). Text now says reweighting acts through both within-country case
mix and the overall geographic make-up; title and conclusion no longer claim a general mechanism.
M2 ACCEPTED, verified in code (weights() divides by country size twice). v6c removed from the main text; SI S6.6 explains.
M3 ACCEPTED: H2 failure stated; RF shares given; sampling noise separated (h2_sampling_v13.py: LASSO noise 14%, pair 48%;
RF classifier 46%, pair 25%).
M4 ACCEPTED: tau claim for v6b removed; FPR-scale MAD reported (0.13 both arms); European studies flagged more often noted.
M5 ACCEPTED: absolute gap reduction with CI reported; 88% no longer in the graphical-abstract summary.
Minor: H4/G4 population set stated (>= 120 people, full set); sensitivity price decomposed (FPR correction vs
contamination 0.02–0.04; 3 cohorts); verification power described as an atlas average, lower at exactly 0.25; new
low-scoring-patient contamination unit test (passes); Holm note corrected to 5,000 draws (G4 Holm < 0.0004); GMWI2
in-training analysis labelled post hoc; taxa reordered by contribution incl. Clostridium sp. CAG_167, top five = 39%
(numbers_v14.py); Fig 2B title and Fig 2D labels corrected (figures_v14); Fig 3 legend panel D added; SI 5,514/5,547;
"62%" is a median (stated).
## Novelty (8/10, minor)
MAJOR 1 ACCEPTED: Li M 2023, Li P 2025 (Gut Microbes) and Degregori 2026 (iMeta) cited (DOIs verified on Crossref; the
reviewer's author initials were corrected); "has not been measured" softened. MINOR 1: GMHI (Gupta 2020) cited.
MINOR 2: Saerens 2002 cited. MINOR 3 (2026 preprint): not added. MINOR 4: no "first" claims.
## Editor (8/10, minor)
MAJOR 1 (repository/Zenodo): BLOCKED ON AUTHORS. MAJOR 2: title tempered; balancing framed as a training-data check.
MAJOR 3: clinical boundary stated in summary and site section (screening only; retrospective; sensitivity cost).
