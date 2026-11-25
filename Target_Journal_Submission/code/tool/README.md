# fprcal — check and set a diagnostic test's false-positive rate at the site of use

Gut-microbiome disease classifiers are usually reported with one cut-off and one false-positive rate (FPR). Our atlas
(14 disease tests x 36 healthy populations, 20 countries) shows that the FPR at a fixed cut-off depends on the
population. `fprcal` gives a laboratory these commands:

| Command | What it does | Needs labels? |
|---|---|---|
| `fprcal atlas CRC` | How far this test's FPR moved across 32-36 healthy populations (pooled FPR, 95% prediction interval, most over-flagged populations) | no |
| `fprcal verify scores.txt --cutoff 1.3` | Exact binomial check of the stated FPR on local healthy people: EXCEEDS / CONSISTENT / INCONCLUSIVE | yes (healthy) |
| `fprcal cutoff scores.txt --pi-max 0.01` | Label-free cut-off from the first N people tested (k-th smallest score, k = ceil((N+1)(1-alpha(1-pi_max)))), with the exact law of the realised FPR | no |
| `fprcal plan` | Burn-in size table: mean, 95th percentile and P(FPR>0.15) of the realised FPR for each N; expected-FPR rule and PAC rule | no |
| `fprcal score abundances.csv --test CRC --out scores.csv` | Score samples with the 14 shipped LASSO atlas tests (coefficient tables). Input format below. **Research use only; not a diagnostic device.** | no |

### Input for `fprcal score`

The shipped models use **MetaPhlAn3 relative abundances (%) of all clades, kingdom to species (k__, p__, c__, o__, f__,
g__, s__), present in > 5% of training samples** — not species only. Higher ranks carry 8–86% of each test's total
|coefficient| weight (e.g. CRC 30%, fatty liver 86%).

- Best: the full MetaPhlAn3 / curatedMetagenomicData table with full clade strings, all ranks
  (`k__Bacteria|p__Fusobacteria|...|s__Fusobacterium_nucleatum`). cMD `relative_abundance` tables have clades as rows:
  use `--taxa-rows`.
- Species rows only, **with full lineage strings**: accepted; each missing higher rank is computed as the sum of the
  species below it (reproduces the MetaPhlAn3 rows to rounding error).
- Species names only (`s__Name`, no lineage): the higher-rank features cannot be computed. `score` stops with an error
  because these features carry more than `--max-missing` (default 0.05) of the |coefficient| weight.
  `--allow-missing` scores anyway (missing features set to their training mean, so they add nothing to the score) and
  prints a warning; such scores are biased and should not be used to set or check a cut-off.

Every output row reports `missing_weight` (share of the test's total |w| on features whose rank is absent from the input
or whose value is NaN) and, for a single test, `absent_weight` (share on clades of a rank that is present but not
detected in the table; counted as 0%, as MetaPhlAn omits undetected clades).

```bash
fprcal score LiJ_2017_relative_abundance.csv --taxa-rows --test CRC --out scores.csv   # cMD table, clades as rows
```

Guarantees (exchangeable healthy people, continuous scores): `--rule expected` gives E[FPR] <= alpha;
`--rule pac --delta 0.05` gives P(FPR > alpha) <= 0.05. Both hold if at most a share `pi_max` of the burn-in group has
the disease. They do **not** hold when the burn-in group comes from another site or another city: in our data the rule
then failed (see manuscript). Use the burn-in at the same site, then verify.

Install and test: `pip install -e . && python -m pytest -q tests` (numpy, scipy, pandas; Python >= 3.9).

Python:
```python
from fprcal import burnin_cutoff, verify_fpr, plan, atlas
r = burnin_cutoff(first_100_scores, alpha=0.10, pi_max=0.01); print(r)
print(verify_fpr(later_healthy_scores, r.cutoff))
atlas.lookup("IBD", "lasso")
```
Atlas data: `fprcal/data/*.csv`, copied from `experiments/atlas/v5/results/` (curatedMetagenomicData 2021-03-31,
MetaPhlAn3). Licence: MIT.
