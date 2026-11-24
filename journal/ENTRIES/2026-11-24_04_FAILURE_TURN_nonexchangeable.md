# 2026-11-24 — RESULT / FAILURE / TURN (burn-in under non-random splits; P4-P6)
Files: v4/results/summary_v4.json, summary_v4_table.csv, deploy_v4_units.csv.
- v3 criterion after dedup is unchanged (locked populations with n >= 120 had no duplicates): BURN(N=100)
  P(FPR>0.15) 0.085, error -54% vs status quo, PAC P(FPR>0.10) 0.045. As the statistician said, the first and third
  numbers are fixed by N and M under random splits; they check the code, not the world. Only 7 distinct populations
  carry the N=100 result; population-cluster bootstrap of BURN - SRC error: -0.034 (95% CI -0.065 to -0.013),
  6 of 7 populations better, Wilcoxon on population means P = 0.031.
- HYPOTHESIS H-NX1 (stated before running): within-site non-random splits keep >= 50% error reduction and
  P(FPR>0.15) <= 0.20. RESULT: 48% reduction (0.039 vs 0.075), P(FPR>0.15) 0.158, 13 populations, 228 units.
  NOT SUPPORTED as pre-stated (misses 50% by 2 points).
  Inside that: age/BMI/sex halves -58% (N=100, 7 populations); accession order -56% (13 populations) - the rule
  survives case-mix change inside a site. Sub-sites of one study (MetaCardis Leipzig/Copenhagen/Paris, PREDICT UK/US):
  BURN is WORSE than doing nothing (+36%, P(FPR>0.15) 0.37 at N=100; only 2 studies, so weak evidence).
- H-NX2 (neighbouring cohort, same country): SUPPORTED - burn-in borrowed from another cohort keeps P(FPR>0.15) at 0.30
  and is no better than the status quo (P = 0.57, 9 populations).
- ALIGN (label-free ComBat-style feature alignment on the same 100 people): better than status quo (-35% to -47%) but
  worse than BURN in 7/7 locked and 10/11 strict populations (BURN - ALIGN -0.012, CI -0.017 to -0.007). Pre-stated: supported.
TURN: the honest statement is narrower than v3. The burn-in works when the calibration people come from the same site
that will use the test, even if case-mix drifts (age, sex, BMI, order). It does not transfer between sites - not even
between cities inside one study, not between cohorts of one country. "Population" in the title should be "site".
That is a cleaner, more useful clinical message: re-calibrate at each site, on its own first patients.
