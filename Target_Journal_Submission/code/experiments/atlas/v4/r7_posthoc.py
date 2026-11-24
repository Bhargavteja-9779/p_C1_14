"""POST HOC (review round 7): false positives and detected cases per 1,000 screened at 1% prevalence, from the pooled
locked case-control sensitivity/FPR at N = 100 (pi = pi_max = 0.01). Writes results/r7_per1000.csv."""
import os, pandas as pd
from common_v4 import OUT
p = pd.read_csv(os.path.join(OUT, "ppv_v4.csv")); p = p[(p.pi == 0.01) & (p.pimax == 0.01) & (p.prev == 0.01)]
p = p.assign(false_positives_per_1000=(p.fpr * 990).round(1), cases_detected_per_1000=(p.sens * 10).round(2))[["method", "sens", "fpr", "ppv", "false_positives_per_1000", "cases_detected_per_1000"]]
p.to_csv(os.path.join(OUT, "r7_per1000.csv"), index=False); print(p.round(4).to_string())
