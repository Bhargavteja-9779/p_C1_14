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
| `fprcal score abundances.csv --test CRC --out scores.csv` | Score samples with the 14 shipped LASSO atlas tests (coefficient tables). Input: CSV, rows = samples, columns = MetaPhlAn3 species names as in curatedMetagenomicData (e.g. `s__Fusobacterium_nucleatum`), values = relative abundance in % (use `--taxa-rows` if taxa are rows). **Research use only; not a diagnostic device.** | no |

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
