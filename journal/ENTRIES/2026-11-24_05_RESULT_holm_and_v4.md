# 2026-11-24 — RESULT / LIMITATION (multiplicity, augmentation after dedup, manuscript v4)
- Control augmentation after dedup: no overall gain (0.078 vs 0.087, P = 0.58). SURPRISE: it still fixes the Indian
  cohort GuptaA for IBD LASSO (0.62 -> 0.03) after removing the 30 shared people - the remaining DhakanDB people are
  Indian too. So augmentation works when the pool happens to contain the same population. Same lesson as the burn-in:
  local information is what fixes it.
- Burn-in vs augmentation is no longer "P = 0.0004": by population it is 4/7 better, P = 0.22 (v3 counted repeated
  populations as independent - my error, caught by the statistician).
- Holm over all 11 reported P values: three survive (strict BURN vs SRC 0.0098, within-site non-random BURN vs SRC
  0.022, post hoc T2D non-westernised 0.0035). The 7-population locked comparisons do not (0.13-0.19).
- Manuscript v4 written: title now says "must be recalibrated at each site". Audit: 161/161 numbers trace to result files.
LIMITATION: the method itself is not new (conformal / NP / reference-interval adaptation); the contribution is the
measurement (scale, I2, mechanism) and the evidence about WHERE calibration data must come from.
