# Novelty elevation log (Stage 4)

## Starting scorecard (first run, re-scored honestly at start of RECHECK; 0-5 each)
| Item | Score | Evidence |
|---|---|---|
| Problem importance / real-world cost | 3 | CRC burden cited; threshold matters for colonoscopy load (FIT literature); no microbiome test is deployed yet -> forward-looking |
| Distance from prior work | 2 | first run had no novelty map; label-shift EM and indirect reference-interval methods are close |
| Strength of evidence | 1 | pilot only, 1 disease, 1 seed, and a duplicated cohort (ThomasAM_2019_c = Yachida subset) in the locked set |
| Insight beyond the method | 2 | "AUROC transfers but cut-off does not" - plausible, shown on 1 disease only |
| Practical capability | 2 | no tested fix yet |
| Rigour / reproducibility | 2 | no run_all, no seeds, leakage bug |
| **Total** | **12/30** | |

## Round 1 (written BEFORE dev results)
Weakest point: distance from prior work + evidence. Ideas generated (family):
1. Operating-point LOSO protocol + overdispersion test (new protocol/benchmark).
2. Site-factor analysis of drift: which measurable site properties (sequencing depth, country, age) predict FPR drift (analysis/insight).
3. Site-shift mixture model for label-free threshold re-estimation (new inference idea; cross-field analogue: indirect reference intervals).
4. Exact finite-sample rule for how many labelled local controls are needed (theory: conformal order statistic, Beta law) validated against real sites (theory + protocol).
5. Label-free drift alarm: predict the status-quo FPR error from unlabeled target scores before any label is collected (uncertainty / "knows when unsure").
6. Cohort-invariant representation: per-cohort feature standardisation with test-time re-standardisation (domain-adaptive training); CLR features (new representation).
Literature status: 3 and 4 have close analogues (Saerens EM; conformal prediction); 1, 2, 5 not found in microbiome literature so far (prior-art agent running - to update).

Hypotheses and falsifiers:
- H1 (alarm): across held-out sites, the label-free shift statistic d = median(target pool scores) - median(source OOF control scores)
  predicts the realised FPR of the status-quo threshold (Spearman rho >= 0.5). WRONG if rho < 0.3 or its 95% CI includes 0.
- H2 (label-free fix): M4 site-shift lowers mean |FPR - 0.10| vs M0 and vs M1 when the pool contains cases (pi = 0.1, 0.3).
  WRONG if M4 is not lower than M1 in paired site comparison.
- H3 (labelled-control rule): the exact Beta-binomial law predicts the observed distribution of realised FPR for the
  conformal threshold at real sites (observed P(FPR_eval > 0.15) within +-5 points of predicted). WRONG if it deviates more.
- H4 (representation): per-cohort standardisation (pcz) reduces FPR drift. WRONG if |FPR-alpha| is not lower than M0.
  Honesty note: a 3-split smoke test (1 seed) run to check the code had already shown pcz with a larger FPR error;
  H4 was therefore written after a glimpse of that smoke output.

## Round 1 results (dev CRC, 8 sites x 2 models x 10 seeds x 50 splits; RECHECK/stage5/dev/)
- Status quo M0: mean |FPR-0.10| = 0.102-0.108; site-mean FPR ranges 0.00-0.34; P(FPR>0.15) = 29-46% of splits.
  Evaluation-noise floor (oracle on the same halves) = 0.037.
- H2 FALSIFIED: our site-shift mixture (M4) is worse than M0 at pi=0 and 0.1 (LASSO +0.068, RF +0.136 at pi=0) and not
  better than local quantile at pi=0.3. Dropped as a contribution; kept as a reported negative result.
- Prediction alignment (Roschewitz 2023, M7) and per-site feature re-standardisation (M6) are WORSE than doing nothing
  (both implicitly assume the target class mix equals the source's ~50%; pools here have 0-30% cases).
- EM prior adjustment (M2) ~ no gain. Local quantile (M1) and known-prevalence subtraction (M3) small gains (~0.02).
- Few labelled local controls (M5, n=10/20): gain ~0.02-0.05, limited by n.
- H4 FALSIFIED (pcz worse).
- H1: label-free exceedance alarm (fraction of the unlabeled pool above the cut-off) ranks sites by realised FPR
  (Spearman 0.96-1.00 at site level, 8 sites) - but at pi=0 it is close to tautological; to be tested at pi>0 on locked sets.
- Side finding: site AUROC vs |FPR-alpha| Spearman -0.56 to -0.60 (n=8, weak evidence).
Ideas tried so far: 7 (M1, M2, M3, M4, M6, M7 label-free; M5 labelled).

## Round 2 (written BEFORE running)
Weakest point now: no method clearly beats the trivial local quantile; label-free mixture idea not new and does not work.
Ideas (family): (a) empirical-Bayes shrinkage of the local threshold toward the source threshold, with between-site
variance tau^2 learned from leave-one-cohort-out OOF thresholds of the TRAINING cohorts (hierarchical model / borrowing
multi-cohort structure); (b) exact finite-sample order-statistic rule for n labelled local controls (theory); (c) report
the noise floor and the n needed (protocol). Lit check: hierarchical shrinkage of site cut-offs not found in the 85-paper
map (closest: indirect reference intervals, conformal); conformal order statistics are textbook.
- H5: shrinkage (M8) applied to the unlabeled pool quantile lowers mean |FPR-0.10| vs BOTH M0 and M1 at pi=0
  (dev CRC, paired by site). WRONG if its mean is not lower than M1's.
- H6: shrinkage applied to n labelled controls beats raw conformal at n=10. WRONG if not lower.
