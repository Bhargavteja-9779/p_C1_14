# Analysis plan v6 — external, published test (GMWI2). Written 2026-11-25 BEFORE any GMWI2 score was computed on our data.

## Why (novelty escalation, cycle 6)
Blind scorecard r9: significance 7 vs P75 8 because "the 28 classifiers are the authors' research models, not tests in
use". Self-score novelty 17/25 (differentiation and significance weakest). The decisive test: does a PUBLISHED,
externally trained, released microbiome classifier with a fixed published cut-off show the same population-dependent
false-positive rate in healthy people it never saw?

## Test
Gut Microbiome Wellness Index 2 (GMWI2; Chang et al. 2024, Nat Commun 15:7447; MIT licence; bioconda gmwi2 1.6).
L1 logistic regression on presence (relative abundance > 1e-5) of MetaPhlAn3 clades at all ranks; 95 non-zero
coefficients; published cut-off: GMWI2 > 0 = "healthy", < 0 = "non-healthy". Coefficients extracted from the released
model file with a whitelisted unpickler (extract_gmwi2.py) and cross-checked against Supplementary Data 3 (must match).
A "false positive" = a healthy adult with GMWI2 < 0 (flagged non-healthy). Ties at exactly 0 are reported separately.

## Stated (developer) FPR
alpha_GMWI2 = share of the 5,547-ish healthy training samples of Chang et al. with published GMWI2 < 0 (Supplementary
Data 5; computed from their file, not from our profiles).

## Data
Healthy adults, one per subject, de-duplicated (v4 rules), strict and full population sets (v4 definitions).
Training overlap: a sample is "GMWI2-training" if its sample accession or any run accession (NCBI_accession) appears in
Supplementary Data 2. A population is "unseen" if NONE of its samples are GMWI2-training. Primary analysis: unseen
populations, n >= 20 (strict set); full set = sensitivity. Seen populations (in-sample for GMWI2) are reported separately.

## QC gate (before any hypothesis is evaluated)
On samples present in both cMD and Supplementary Data 5, Pearson r between our GMWI2 and the published GMWI2 must be
>= 0.90 (different MetaPhlAn3 runs). If it fails, the analysis is reported as an implementation mismatch and stops.

## Hypotheses (each with falsifier)
- G1 heterogeneity: DerSimonian–Laird on logit FPR across unseen strict populations gives I^2 >= 0.5.
  FALSIFIED if I^2 < 0.5 (or fewer than 5 unseen populations -> INCONCLUSIVE).
- G2 miscalibration beyond noise: the share of unseen populations whose FPR lies outside [alpha/2, 1.5 alpha] exceeds the
  binomial expectation under FPR = alpha (exact, per population sizes) by >= 20 percentage points.
- G3 optimism of in-sample validation: mean FPR of seen populations (n >= 20) < mean FPR of unseen populations
  (one-sided Mann–Whitney, P < 0.05). FALSIFIED if not.
- G4 local fix: within-site burn-in with N = 100 (v5 H4 design: first 100 by accession order; age/BMI halves) and target
  alpha_GMWI2 lowers mean |FPR - alpha_GMWI2| vs the published cut-off, averaged over eligible populations (all
  populations with n >= 120, seen or unseen), with a population-clustered bootstrap 95% CI excluding 0.
Holm correction over G1-G4 P values where a P value exists (G2: exact Poisson-binomial test; G3: MW; G4: bootstrap).
