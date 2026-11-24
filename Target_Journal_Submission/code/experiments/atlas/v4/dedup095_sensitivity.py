"""POST HOC sensitivity (review round 5): de-duplicate at r > 0.95 (same rules as P0) and re-check (a) strict-set
heterogeneity, (b) control augmentation for the IBD/T2D tests on GuptaA_2019 and overall. Writes results/dedup095_sensitivity.json."""
import os, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import stats
from common_v4 import *
from src.pipeline import Pipeline
TH = 0.95; A = 0.10; dev, lock = split()
Xs, lab = [], []
for s in healthy_studies():
    if not os.path.exists(os.path.join(CACHE, "ra", f"{s}.csv")) or s in dropped_studies(): continue
    X, md = controls(s); Xs.append(X); lab += [("H", s, i) for i in X.index]
for d in ["CRC", "IBD", "T2D"]:
    X, y, g, M = load(d); Xs.append(X); lab += [("T", gg, i) for gg, i in zip(g, X.index)]
lab = pd.DataFrame(lab, columns=["kind", "study", "sample"]).reset_index(drop=True)
Af = pd.concat(Xs).fillna(0.0).values.astype(np.float32)
Af = Af / (Af.sum(1, keepdims=True) + 1e-12); L = np.log10(Af + 1e-5); L -= L.mean(1, keepdims=True); L /= np.linalg.norm(L, axis=1, keepdims=True)
cc = set(s for d in ["CRC", "IBD", "T2D"] for s in DISEASES[d]["studies"]); size = lab.groupby("study").size(); rem = set(); pairs = []
for i0 in range(0, len(L), 2000):
    C = L[i0:i0 + 2000] @ L.T; ii, jj = np.where(C > TH)
    for a, b in zip(ii + i0, jj):
        sa, sb = lab.study[a], lab.study[b]
        if a >= b or sa == sb or lab["sample"][a] == lab["sample"][b]: continue
        if (sa in cc) != (sb in cc): loser = b if sa in cc else a
        elif sa in cc and sb in cc: continue
        else: loser = a if size[sa] < size[sb] else b
        rem.add(lab["sample"][loser]); pairs.append((sa, sb))
out = dict(threshold=TH, extra_removed=len(rem), pairs=pd.Series([f"{a}~{b}" for a, b in pairs]).value_counts().to_dict())
r = pd.read_csv(os.path.join(OUT, "atlas_rows_v4.csv.gz")); H = r[~r.study.str.startswith("TRAIN") & ~r.sample_id.isin(rem)]
H = H[(H.strict_person == True) & ~H.study.isin(STRICT_DROP_STUDIES)]; H = H[H.groupby(["disease", "model", "study"]).study.transform("size") >= MIN_N]
def dl(k, n):
    y = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v; mu = (w * y).sum() / w.sum(); Q = (w * (y - mu) ** 2).sum(); df = len(y) - 1
    t2 = max(0, (Q - df) / (w.sum() - (w ** 2).sum() / w.sum())); ws = 1 / (v + t2); m2 = (ws * y).sum() / ws.sum(); se = ws.sum() ** -.5; t = stats.t.ppf(.975, len(y) - 2); ex = lambda x: 1 / (1 + np.exp(-x))
    return dict(I2=max(0, (Q - df) / Q), pi_lo=ex(m2 - t * np.sqrt(t2 + se ** 2)), pi_hi=ex(m2 + t * np.sqrt(t2 + se ** 2)))
out["heterogeneity_strict"] = {f"{d}_{m}": dict(populations=g.study.nunique(), **dl(g.groupby("study").flag.sum().values, g.groupby("study").flag.size().values))
                               for (d, m), g in H.groupby(["disease", "model"])}
aug = []
for d in ["IBD", "T2D"]:
    X, y, g, M = load(d); train = set(DISEASES[d]["studies"]); Xs2, ys, gs = [X], [y], [g]
    for s in dev:
        if s in train or s in dropped_studies() or not os.path.exists(os.path.join(CACHE, "ra", f"{s}.csv")): continue
        Xc, md = controls(s); k = ~Xc.index.isin(rem); Xs2.append(Xc[k]); ys.append(np.zeros(k.sum(), int)); gs.append(np.array([s] * k.sum()))
    XA = pd.concat(Xs2).fillna(0.0); yA, gA = np.concatenate(ys), np.concatenate(gs)
    for m in ["lasso", "rf"]:
        for flag in [False, True]:
            k = np.ones(len(yA), bool) if flag else np.isin(gA, list(train))
            p = Pipeline(m).fit(XA.values[k], yA[k], gA[k]); t = np.quantile(p.oof[p.y == 0], 1 - A)
            for s in [x for x in populations(d, strict=False) if x in lock]:
                Xc, md = controls(s); Xc = Xc[~Xc.index.isin(rem)]; sc = p.score(Xc.reindex(columns=XA.columns, fill_value=0).fillna(0).values)
                aug.append(dict(disease=d, model=m, aug=flag, pop=s, fpr=float(np.mean(sc >= t))))
a = pd.DataFrame(aug); a["err"] = (a.fpr - A).abs()
out["augmentation_IBD_T2D_mean_abs_err"] = a.groupby(["disease", "model", "aug"]).err.mean().round(4).to_dict().__repr__()
out["GuptaA"] = a[a["pop"] == "GuptaA_2019"].round(3).to_dict("records")
json.dump(out, open(os.path.join(OUT, "dedup095_sensitivity.json"), "w"), indent=1, default=float); print(json.dumps(out, indent=1, default=float))
