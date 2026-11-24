"""POST HOC P6: CRC-only deployment simulation over the 11 CRC sites (8 development LOCO + 3 locked), primary settings
(B = 100, 12 months, pi = 1%, R = 100). Development sites are optimistic for the verified-positive rule (it was designed
on them) and are reported separately."""
import sys, os, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "final")); sys.path.insert(0, os.path.join(H, ".."))
sys.argv = ["x", "--dryrun"]; import run_final as RF
from src.data import DEV_CRC, LOCKED_CRC
from src import calibrate as C
Zd = np.load(os.path.join(H, "dev", "scores_dev.npz")); items = list(np.load(os.path.join(H, "final", "results", "scores.npz"), allow_pickle=True)["items"])
rng = np.random.default_rng(21); rows = []
for model in ["lasso", "rf"]:
    for site in DEV_CRC + LOCKED_CRC:
        if site in DEV_CRC: s_src, y_src, st, yt = (Zd[f"{model}|{site}|{k}"] for k in ["src", "ysrc", "tgt", "ytgt"]); role = "development"
        else: it = [i for i in items if i[0] == "CRC" and i[1] == site and i[2] == model][0]; s_src, y_src, st, yt = it[3], it[4], it[5], it[6]; role = "locked"
        for r in range(100):
            for o in RF.simulate(s_src, y_src, st[yt == 0], st[yt == 1], 0.01, rng):
                rows.append(dict(model=model, site=site, role=role, rep=r, **o))
d = pd.DataFrame(rows); d.to_csv(os.path.join(H, "addendum_results", "posthoc_crc_deploy.csv.gz"), index=False)
d["over"] = d.fpr > 0.12; L = d[d.month >= 7]
print(L.groupby(["role", "method"]).agg(fpr=("fpr", "mean"), p_over=("over", "mean"), sens=("sens", "mean")).round(3).unstack("method").to_string())
print(L.groupby("method").agg(fpr=("fpr", "mean"), p_over=("over", "mean"), sens=("sens", "mean")).round(3).to_string())
