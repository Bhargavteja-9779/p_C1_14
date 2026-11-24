# 2026-11-24 — RESULT (cycle 5: tool + verification power, POST HOC descriptive)
ATTEMPT: packaged the method as `fprcal` (code/tool): burn-in cut-off (expected / PAC), exact Beta law of the realised
FPR, exact binomial verification of a stated FPR, planning table, atlas lookup (14 tests x 2 models x 32-36 strict
populations). 11 unit tests pass, including Monte-Carlo checks of both guarantees and the contamination bound.
OBSERVATION (planning table, analytic): with N = 100 the expected-FPR rule has P(FPR>0.15) = 0.055 and 95th percentile
0.152; N = 200 -> 0.015. The PAC rule at N = 100 has mean FPR 0.050 (costs sensitivity).
RESULT (verify_power_v5.py, observed FPR treated as truth): 218/489 LASSO test-population units (45%) have FPR > 0.15.
Verifying on n = 100 local healthy people (one-sided exact test of FPR <= 0.15 at 0.05) detects them with mean power
0.72 (0.98 for FPR > 0.25); worst false-alarm probability for in-range units 0.033. n = 50: 0.61 / 0.91.
DEAD END (again): DEBIAS-M install from GitHub denied by the permission system; torch (CPU) did install. Stays
BLOCKED ON USER.
TURN: message for readers becomes "verify, then recalibrate locally" with a ready tool and sample-size numbers.
