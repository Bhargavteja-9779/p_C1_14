import os, sys, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v4"))
from common_v4 import controls, populations, CACHE, MIN_N, DISEASES
sys.path.insert(0, os.path.join(HERE, "..", "v5")); import atlas_v5 as A5
from src.pipeline import _log, logit
OUT = os.path.join(HERE, "results"); A = 0.10; META = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
TESTS = {k: A5.TESTS[k] for k in ["CRC", "adenoma", "IBD", "T2D", "IGT"]}
def country(ids): return META.loc[ids, "country"].fillna("NA").values
def weights(y, g, ids):
    c = country(ids); key = pd.Series([f"{a}|{b}" for a, b in zip(c, y)]); w = 1.0 / key.map(key.value_counts()).values
    cw = pd.Series(c); w = w / pd.Series(c).map(cw.value_counts()).values * len(w)  # down-weight big countries
    return w / w.mean()
def fit(X, y, g, ids, balanced):
    keep = (X > 0).mean(0) > 0.05; L = _log(X, keep); mu, sd = L.mean(0), L.std(0) + 1e-6; Z = (L - mu) / sd
    w = weights(y, g, ids) if balanced else np.ones(len(y))
    oof = np.zeros(len(y)); aucs = []
    for a, b in GroupKFold(len(np.unique(g))).split(Z, y, g):
        m = LogisticRegression(C=0.1, penalty="l1", solver="liblinear", class_weight="balanced", max_iter=2000).fit(Z[a], y[a], sample_weight=w[a])
        oof[b] = m.predict_proba(Z[b])[:, 1]
        if len(np.unique(y[b])) == 2: aucs.append(roc_auc_score(y[b], oof[b]))
    m = LogisticRegression(C=0.1, penalty="l1", solver="liblinear", class_weight="balanced", max_iter=2000).fit(Z, y, sample_weight=w)
    oofl = logit(oof); t = np.quantile(oofl[(y == 0)], 1 - A) if not balanced else np.quantile(np.repeat(oofl[y == 0], 1), 1 - A)
    # weighted quantile for balanced cut-off
    if balanced:
        s = oofl[y == 0]; ww = w[y == 0]; o = np.argsort(s); cs = np.cumsum(ww[o]) / ww.sum(); t = s[o][np.searchsorted(cs, 1 - A)]
    return dict(keep=keep, mu=mu, sd=sd, m=m, t=float(t), auc=float(np.mean(aucs)))
def dl_tau(k, n):
    y = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v; mu = (w * y).sum() / w.sum(); Q = (w * (y - mu) ** 2).sum()
    return float(np.sqrt(max(0, (Q - len(y) + 1) / (w.sum() - (w ** 2).sum() / w.sum()))))
rows = []
for t, (case, studies) in TESTS.items():
    X, y, g, M = A5.load_cc(case, studies); X = X; ids = X.index
    from common_v4 import healthy_studies, dropped_studies, STRICT_DROP_STUDIES
    P = [z for z in healthy_studies() if z not in set(studies) and z not in dropped_studies() and z not in STRICT_DROP_STUDIES
         and os.path.exists(os.path.join(CACHE, "ra", f"{z}.csv"))]
    mods = {bal: fit(X.values, y, g, ids, bal) for bal in [False, True]}
    for s in P:
        Xc, md = controls(s); Xc = Xc[md.strict_person.values]
        if len(Xc) < MIN_N: continue
        for bal, mo in [("naive", mods[False]), ("balanced", mods[True])]:
            Z = (_log(Xc.reindex(columns=X.columns, fill_value=0).fillna(0).values, mo["keep"]) - mo["mu"]) / mo["sd"]
            sc = logit(mo["m"].predict_proba(Z)[:, 1]); rows.append(dict(test=t, arm=bal, pop=s, n=len(sc), k=int((sc >= mo["t"]).sum()), fpr=float(np.mean(sc >= mo["t"])), auc=mo["auc"]))
    print(t, "naive AUC %.3f balanced AUC %.3f" % (mods[False]["auc"], mods[True]["auc"]), flush=True)
R = pd.DataFrame(rows); R.to_csv(os.path.join(OUT, "v6c_rows.csv"), index=False)
res = {}
for arm in ["naive", "balanced"]:
    d = R[R.arm == arm]; taus = []; oob = []
    for t, gg in d.groupby("test"):
        if len(gg) >= 3: taus.append(dl_tau(gg.k.values, gg.n.values)); oob.append(float(((gg.fpr < .05) | (gg.fpr > .15)).mean()))
    res[arm] = dict(mean_tau=float(np.mean(taus)), mean_oob=float(np.mean(oob)), mean_auc=float(d.groupby("test").auc.first().mean()))
# clustered bootstrap on tau difference
rng = np.random.default_rng(5); pops = R["pop"].unique(); db = []
for _ in range(2000):
    pick = set(rng.choice(pops, len(pops))); Rb = R[R["pop"].isin(pick)]
    tn = [dl_tau(gg.k.values, gg.n.values) for t, gg in Rb[Rb.arm == "naive"].groupby("test") if len(gg) >= 3]
    tb = [dl_tau(gg.k.values, gg.n.values) for t, gg in Rb[Rb.arm == "balanced"].groupby("test") if len(gg) >= 3]
    if tn and tb: db.append(np.mean(tb) - np.mean(tn))
res["C1"] = dict(tau_naive=res["naive"]["mean_tau"], tau_balanced=res["balanced"]["mean_tau"], diff=res["balanced"]["mean_tau"] - res["naive"]["mean_tau"],
                 ci95=[float(np.percentile(db, 2.5)), float(np.percentile(db, 97.5))], supported=res["balanced"]["mean_tau"] < res["naive"]["mean_tau"])
res["C2"] = dict(oob_naive=res["naive"]["mean_oob"], oob_balanced=res["balanced"]["mean_oob"], supported=res["balanced"]["mean_oob"] < res["naive"]["mean_oob"])
res["C3"] = dict(auc_naive=res["naive"]["mean_auc"], auc_balanced=res["balanced"]["mean_auc"], drop=res["naive"]["mean_auc"] - res["balanced"]["mean_auc"], supported=(res["naive"]["mean_auc"] - res["balanced"]["mean_auc"]) <= 0.03)
json.dump(res, open(os.path.join(OUT, "v6c_results.json"), "w"), indent=1); print(json.dumps(res, indent=1))
