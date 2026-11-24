# 2026-11-24 — RESULT (cycle 5: pre-registered replication, protocol_v5 Addendum A)
Script replicate_v5.py committed before running (commit "Addendum A replication script"), run once.
Replication set: 19 populations in the full de-duplicated set that are not in the strict set (15 EUNA, 4 other:
TZA, GHA, ETH, CHN).
- H5 (LASSO, primary): distance-to-training vs FPR rho > 0 in 10/14 tests, median rho 0.17, one-sided sign P = 0.090.
  Pre-stated rule needed >= 9/14 AND P < 0.05 -> INCONCLUSIVE (direction replicates, strength does not).
  RF (secondary): 11/14, P = 0.029.
- H6 (LASSO): non-EUNA median index 0.38 vs EUNA 0.13 (difference +0.25, same direction as exploratory),
  one-sided MW P = 0.30 with only 4 non-EUNA populations -> INCONCLUSIVE. RF: +0.06, P = 0.70.
LIMITATION: the replication set is small and mostly European by construction (strict exclusions were study-level, e.g.
hospital controls, antibiotics, mothers), so H6 had little power. The geography/distance story stays EXPLORATORY in the
paper; it must not be stated as a confirmed finding.
