# cutoffguard

Keep a deployed diagnostic test's false-positive rate (FPR) on target at a new site, using only what a screening
programme already observes: the verified outcomes (e.g. colonoscopy results) of people who tested positive.

- Finite-sample guarantee: expected FPR <= alpha for a fresh control from the same site, whatever the past referral
  cut-offs, attendance or result delays (unverified people are counted as possible false positives), given an upper
  bound `pi_max` on prevalence (Proposition S1 in the paper).
- High-confidence option (`delta`): P(FPR > alpha) <= delta instead of a bound on the expected FPR.
- `Recalibrator`: monthly updates with a liberal burn-in and a drift alarm.
- `GroupRecalibrator`: per-group FPR control (e.g. people with and without chronic disease).
- `prevalence_bounded_threshold`: label-free local cut-off from unlabelled scores and a prevalence bound (with the same
  high-confidence option) - sufficient at stable, well-sampled sites.
- `audit_sites`: realised FPR of a fixed cut-off per site with exact binomial tests.

```
pip install .
cutoffguard --history history.csv --alpha 0.10 --pi-max 0.05            # next month's cut-off
cutoffguard --history history.csv --group-col comorbidity                 # per-group cut-offs
```
`history.csv` columns: `month, score, verified, label[, group]`.
