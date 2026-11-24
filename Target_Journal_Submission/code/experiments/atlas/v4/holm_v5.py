"""Holm over 12 population-level P values (holm_v4 family + post hoc within-site burn-in test). Writes results/holm_v5.csv."""
import os, json, pandas as pd
from common_v4 import OUT
d = pd.read_csv(os.path.join(OUT, "holm_v4.csv"))[["test", "p"]]
d.loc[d.test == "BURN-SRC NX1 pooled N100", "test"] = "BURN-SRC pre-stated pooled non-random (incl. cross-site) N100"
d.loc[d.test == "BURN-SRC strict N100", "test"] = "BURN-SRC strict N100 random split (training cut-off miscalibration)"
d = pd.concat([d, pd.DataFrame([dict(test="BURN-SRC within-site non-random N100 (post hoc grouping)", p=json.load(open(os.path.join(OUT, "r3_posthoc.json")))["within_site_N100"]["wilcoxon_pop_p"])])])
d = d.sort_values("p").reset_index(drop=True); m = len(d); d["holm"] = (d.p * (m - d.index)).cummax().clip(upper=1)
d.to_csv(os.path.join(OUT, "holm_v5.csv"), index=False); print(d.round(4).to_string())
import numpy as np
for N, pm in [(100, 0.01), (100, 0.0), (50, 0.01)]: print("k example", N, pm, int(np.ceil((N + 1) * (1 - 0.10 * (1 - pm)))))
