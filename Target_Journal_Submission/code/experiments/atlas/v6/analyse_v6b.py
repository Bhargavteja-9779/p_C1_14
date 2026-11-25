import json, numpy as np, pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score
R = pd.read_csv("results/v6b_loso_scores.csv.gz", index_col=0); EA = {"CHN", "JPN", "KOR"}
def dl_tau(k, n):
    yv = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v; mu = (w * yv).sum() / w.sum(); Q = (w * (yv - mu) ** 2).sum()
    return float(np.sqrt(max(0, (Q - len(yv) + 1) / (w.sum() - (w ** 2).sum() / w.sum())))), float(max(0, (Q - len(yv) + 1) / Q))
def summ(R):
    H = R[R.healthy == 1]; o = {}
    for m in ["naive", "balanced"]:
        g = H.assign(f=(H[m] < 0).astype(int)).groupby("study_name").agg(n=("f", "size"), k=("f", "sum"), country=("country", "first")).reset_index(); g = g[g.n >= 20]
        g["fpr"] = g.k / g.n; g["ea"] = g.country.isin(EA)
        tau, I2 = dl_tau(g.k.values, g.n.values)
        o[m] = dict(gap=float(g[g.ea].fpr.median() - g[~g.ea].fpr.median()), ea_median=float(g[g.ea].fpr.median()), other_median=float(g[~g.ea].fpr.median()),
                    tau=tau, I2=I2, auroc=float(roc_auc_score(R.healthy, R[m])), pooled_fpr=float((H[m] < 0).mean()),
                    sens_nonhealthy=float((R[R.healthy == 0][m] < 0).mean()), studies=len(g), ea_studies=int(g.ea.sum()))
        o[m + "_perstudy"] = g
    return o
o = summ(R)
for m in ["naive", "balanced"]: o.pop(m + "_perstudy").to_csv(f"results/v6b_perstudy_{m}.csv", index=False)
# study-clustered bootstrap
rng = np.random.default_rng(11); st = R.study_name.unique(); bg, ba = [], []
for b in range(2000):
    pick = rng.choice(st, len(st)); Rb = pd.concat([R[R.study_name == s] for s in pick])
    try:
        sb = summ(Rb); bg.append((sb["naive"]["gap"] - sb["balanced"]["gap"]) / sb["naive"]["gap"]); ba.append(sb["balanced"]["auroc"] - sb["naive"]["auroc"])
    except Exception: pass
res = dict(naive=o["naive"], balanced=o["balanced"],
           B1=dict(gap_naive=o["naive"]["gap"], supported=o["naive"]["gap"] >= 0.15),
           B2=dict(rel_gap_reduction=1 - o["balanced"]["gap"] / o["naive"]["gap"], ci95=[float(np.nanpercentile(bg, 2.5)), float(np.nanpercentile(bg, 97.5))], supported=(1 - o["balanced"]["gap"] / o["naive"]["gap"]) >= 0.5),
           B3=dict(auroc_diff=o["balanced"]["auroc"] - o["naive"]["auroc"], ci95=[float(np.percentile(ba, 2.5)), float(np.percentile(ba, 97.5))], supported=(o["balanced"]["auroc"] - o["naive"]["auroc"]) >= -0.03),
           B4=dict(tau_naive=o["naive"]["tau"], tau_balanced=o["balanced"]["tau"], supported=o["balanced"]["tau"] < o["naive"]["tau"]), boot_n=len(bg))
json.dump(res, open("results/v6b_results.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float))
