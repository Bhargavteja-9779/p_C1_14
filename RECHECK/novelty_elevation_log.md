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
