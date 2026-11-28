# Analysis plan v7: a second published index (GMHI). Written 2026-11-28 BEFORE any GMHI score was computed.

## Why
Final editor check r14 (75/100): significance 7 vs P75 8 because 27 of the 28 atlas classifiers are research refits;
the audit of a released index (GMWI2) was rated the highest-relevance part. Test whether the GMWI2 findings hold for an
independent, earlier, widely used released index with a different algorithm.

## Test
Gut Microbiome Health Index (GMHI; Gupta et al. 2020, Nat Commun 11:4635), computed exactly as in the developers'
released script `GMHI.R` (repository jaeyunsung/GMHI_2020, cloned 2026-11-28; commit hash recorded in the results):
species-level relative abundances, unclassified/virus clades removed, renormalised to sum 1, values < 1e-5 set to 0;
7 health-prevalent (MH) and 43 health-scarce (MN) species; psi = (R / R') x Shannon(within group), R'_MH = 7,
R'_MN = 31; GMHI = log10((psi_MH + 1e-5) / (psi_MN + 1e-5)). Published decision rule: GMHI > 0 healthy, < 0
non-healthy. A false positive = a healthy adult with GMHI < 0. Ties at exactly 0 are reported separately.
The R script is not executed; it is re-implemented in Python (`run_gmhi.py`).

## QC gates (before any hypothesis is evaluated)
- Q1: on the developers' example (`species_relative_abundances.csv`), our GMHI equals `GMHI_output.csv` (max |diff| < 1e-6).
- Q2: on samples present both in curatedMetagenomicData (cMD, MetaPhlAn3) and in the developers' 4,347-sample profiles
  (MetaPhlAn2), matched by sample/run accession, Pearson r between the two GMHI values >= 0.80 (different MetaPhlAn
  versions and species names; MH/MN species missing from cMD are listed). If Q2 fails, H3-H6 are reported as an
  implementation mismatch and not interpreted; H1-H2 (developers' own profiles) stand.

## Stated (developer) FPR
alpha_GMHI = share of healthy samples (Phenotype == "Healthy") in the developers' 4,347-sample data with GMHI < 0,
computed with the published formula on the developers' own profiles.

## Data
Developers' data: healthy samples by study ("Study No."), studies with >= 20 healthy samples.
cMD: healthy adults, one per subject, de-duplicated, strict and full sets (v4 definitions, as for GMWI2), n >= 20.
A cMD population is "seen" if any of its sample or run accessions appears in the developers' metadata ("Sample
Accession or Sample ID"); otherwise "unseen". Primary: unseen strict populations; full set = sensitivity.
East Asian (fixed before seeing results): developers' "Geographical Region or Population" containing China, Chinese,
Japan, Japanese, Korea, Korean, Hong Kong or Taiwan; cMD country CHN, JPN, KOR, HKG, TWN.

## Hypotheses (each with falsifier)
- H1 heterogeneity in the developers' own healthy data: DerSimonian-Laird I^2 >= 0.5 on logit share flagged across
  studies. FALSIFIED if I^2 < 0.5.
- H2 East Asian excess in the developers' own healthy data (replication of the GMWI2 finding): share flagged higher in
  East Asian than in other studies (one-sided Mann-Whitney, P < 0.05). FALSIFIED if not; INCONCLUSIVE if < 3 East Asian
  studies.
- H3 heterogeneity in unseen cMD strict populations: I^2 >= 0.5 (INCONCLUSIVE if < 5 populations).
- H4 miscalibration beyond noise: share of unseen strict populations outside [alpha/2, 1.5 alpha] exceeds the exact
  binomial expectation under FPR = alpha by >= 20 percentage points, exact Poisson-binomial P < 0.05.
- H5 shared population effect: across cMD strict populations scored by both indices (n >= 20), the GMHI and GMWI2
  flag rates are positively rank-correlated (Spearman rho > 0, one-sided P < 0.05).
- H6 local fix: within-site burn-in, N = 100, target alpha_GMHI, designs as GMWI2 G4 (accession order; age and BMI
  halves), full set, n >= 120; mean |FPR - alpha_GMHI| lower than with the published cut-off, population-clustered
  bootstrap 95% CI of the difference excluding 0.
Holm correction over the P values of H2, H4, H5, H6 (H6: bootstrap P). Everything else is post hoc and labelled so.
