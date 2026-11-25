"""POST HOC (review round 11, M1/M4/M5): does the v6b gap reduction come from label balance WITHIN country, or from
equalising countries? v6b's pre-specified weight 1/n(country,label) also gives every country x label cell equal total
weight. Here: 'within' weight = n_country / (L_country * n_country,label): healthy and non-healthy share each country's
ORIGINAL total weight equally (L = number of labels present). Same data, LOSO, model and cut-off as run_v6b.py.
Also: absolute gap with corrected study-clustered CI, and FPR-scale spread (MAD) for all arms.
Writes results/v6b_withincountry_scores.csv.gz and results/posthoc_v6b_withincountry.json."""
import os, sys, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import sparse
from multiprocessing import Pool
from sklearn.linear_model import LogisticRegression
import run_v6b as RB
OUT = RB.OUT; EA = RB.EA
def fit(s):
    tr = Mt.study_name.values != s; Xtr, ytr = X[tr], y[tr]; keep = np.asarray(Xtr.mean(0)).ravel() >= 0.01
    c = pd.Series(Mt.country.fillna("NA").values[tr]); key = c + "|" + pd.Series(ytr).astype(str)
    nc = c.map(c.value_counts()).values; ncl = key.map(key.value_counts()).values; L = c.map(pd.Series(ytr).groupby(c).nunique()).values
    w = nc / (L * ncl); w = w * len(w) / w.sum()
    m = LogisticRegression(penalty="l1", C=0.03, solver="liblinear", class_weight="balanced", max_iter=2000).fit(Xtr[:, keep], ytr, sample_weight=w)
    te = ~tr; return np.where(te)[0], m.decision_function(X[te][:, keep])
if __name__ == "__main__":
    f = os.path.join(OUT, "v6b_withincountry_scores.csv.gz")
    if not os.path.exists(f):
        Xdf, Mt0 = RB.build(); globals().update(Mt=Mt0, X=sparse.csr_matrix(Xdf.values.astype(np.float32)), y=Mt0.healthy.values.astype(int))
        with Pool(4) as P: res = P.map(fit, list(Mt.study_name.unique()))
        d = np.full(len(y), np.nan)
        for idx, v in res: d[idx] = v
        old = pd.read_csv(os.path.join(OUT, "v6b_loso_scores.csv.gz"), index_col=0); assert (old.index == Mt.index).all()
        old.assign(within=d).to_csv(f)
    R = pd.read_csv(f, index_col=0)
    def per(R, arm):
        H = R[R.healthy == 1]; g = H.assign(k=(H[arm] < 0).astype(int)).groupby("study_name").agg(n=("k", "size"), k=("k", "sum"), country=("country", "first"))
        g = g[g.n >= 20]; g["fpr"] = g.k / g.n; g["ea"] = g.country.isin(EA); return g
    def gap(g): return float(g[g.ea].fpr.median() - g[~g.ea].fpr.median())
    o = {}
    for arm in ["naive", "balanced", "within"]:
        g = per(R, arm); f_ = g.fpr.values
        o[arm] = dict(gap=gap(g), ea_median=float(g[g.ea].fpr.median()), other_median=float(g[~g.ea].fpr.median()), pooled_fpr=float((R[R.healthy == 1][arm] < 0).mean()),
                      mad_fpr=float(np.median(np.abs(f_ - np.median(f_)))), studies=len(g))
    for arm in ["balanced", "within"]: o[arm]["rel_reduction"] = 1 - o[arm]["gap"] / o["naive"]["gap"]; o[arm]["abs_reduction"] = o["naive"]["gap"] - o[arm]["gap"]
    st = R.study_name.unique(); S = {s: R[R.study_name == s] for s in st}; rng = np.random.default_rng(11); B = {"balanced": [], "within": []}
    for i in range(2000):
        D = pd.concat([S[s].assign(study_name=f"{s}#{j}") for j, s in enumerate(rng.choice(st, len(st)))])
        try:
            gn = gap(per(D, "naive"))
            for arm in B: B[arm].append(gn - gap(per(D, arm)))
        except Exception: pass
    for arm in B: o[arm]["abs_reduction_ci95"] = [float(np.nanpercentile(B[arm], 2.5)), float(np.nanpercentile(B[arm], 97.5))]
    json.dump(o, open(os.path.join(OUT, "posthoc_v6b_withincountry.json"), "w"), indent=1); print(json.dumps(o, indent=1))
