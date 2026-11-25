"""POST HOC (after plan v6 results): per-study FPR of the published GMWI2 cut-off among HEALTHY TRAINING samples,
computed only from the developers' own published scores (Chang 2024, Supplementary Data 5) - no re-implementation."""
import json, numpy as np, pandas as pd
from scipy import stats
S5 = pd.read_csv("inputs/gmwi2_SData5_published_scores.csv.gz"); S2 = pd.read_csv("inputs/gmwi2_SData2_training_samples.csv.gz")
S5 = S5.merge(S2[["Sample accession", "Geography (Country)"]], on="Sample accession", how="left")
H = S5[S5["Subject health status"] == "Healthy"]; st = "Author's last name (Publication year)"
g = H.groupby(st).agg(n=("GMWI2", "size"), k=("GMWI2", lambda x: int((x < 0).sum())), country=("Geography (Country)", "first")).reset_index()
g["fpr"] = g.k / g.n; g = g[g.n >= 20].sort_values("fpr")
def dl(k, n):
    y = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v; mu = (w * y).sum() / w.sum(); Q = (w * (y - mu) ** 2).sum(); df = len(y) - 1
    t2 = max(0, (Q - df) / (w.sum() - (w ** 2).sum() / w.sum())); return dict(tau=float(np.sqrt(t2)), I2=float(max(0, (Q - df) / Q)), Q_p=float(stats.chi2.sf(Q, df)))
a = float((H.GMWI2 < 0).mean())
out = dict(studies=len(g), people=int(g.n.sum()), pooled_fpr=a, fpr_range=[float(g.fpr.min()), float(g.fpr.max())], fpr_iqr=[float(g.fpr.quantile(.25)), float(g.fpr.quantile(.75))],
           out_of_band=float(((g.fpr < a / 2) | (g.fpr > 1.5 * a)).mean()), **dl(g.k.values, g.n.values),
           over_half=g.loc[g.fpr > .5, [st, "country", "n", "fpr"]].values.tolist())
g.to_csv("results/gmwi2_published_training_perstudy.csv", index=False); json.dump(out, open("results/gmwi2_published_training.json", "w"), indent=1)
print(json.dumps(out, indent=1)); print(g.to_string())
