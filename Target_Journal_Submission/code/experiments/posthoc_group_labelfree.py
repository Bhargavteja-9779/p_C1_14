"""POST HOC P7: does the label-free prevalence-bounded rule, run within recorded groups, equalise false-positive rates at
MetaCardis as well as the verified-positive rule? Same simulation as Part C (B = 200/month, 18 months, 1% CRC cases from
development out-of-fold case scores), R = 100."""
import sys, os, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src.data import load, DEV_CRC, CACHE
from src.models import train_and_score, preprocess_fit, preprocess_apply, logit
from src import calibrate as C
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
X, y, g, M = load("CRC", DEV_CRC); cols = X.columns; idx = np.arange(len(y)); rows = []
shares = {"CAD": 0.10, "T2D": 0.15, "HF": 0.03, "IGT": 0.15}; rng = np.random.default_rng(31)
for model in ["lasso", "rf"]:
    s_src, y_src, _, m = train_and_score(X.values, y, g, idx, idx[:1], model, seed=2026); p = preprocess_fit(X.values); case_sc = s_src[y_src == 1]
    c = "MetaCardis_2020_a"; a = pd.read_csv(os.path.join(CACHE, "ra", f"{c}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
    a = a.groupby(level=0).sum().T; md = meta.loc[meta.index.intersection(a.index)]
    md = md[(md.study_name == c) & (md.body_site == "stool") & md.age_category.isin(["adult", "senior"])]; md = md[~md.subject_id.duplicated()]
    sc = logit(m.predict_proba(preprocess_apply(a.loc[md.index].reindex(columns=cols, fill_value=0).fillna(0).values, p))[:, 1])
    pops = {"control": sc[md.study_condition.values == "control"]}; pops.update({k: sc[md.study_condition.values == k] for k in shares})
    names = list(pops); w = np.array([1 - sum(shares.values())] + [shares[k] for k in shares])
    for r in range(100):
        U = {k: [] for k in names}; t_src = C.source_threshold(s_src, y_src, 0.10)
        vp = {k: C.SequentialRecalibrator(s_src, y_src, 0.10, 0.05) for k in names}
        for month in range(1, 19):
            for k in names:
                tl = C.contam_quantile(np.concatenate(U[k]), 0.10, 0.05) if U[k] else t_src
                for meth, t in [("labelfree_group", tl), ("vp_group", vp[k].t)]:
                    rows.append(dict(model=model, rep=r, month=month, group=k, method=meth, fpr=(pops[k] >= t).mean(), sens=(case_sc >= t).mean()))
            gi = rng.choice(len(names), 200, p=w); yc = rng.random(200) < 0.01
            u = np.array([rng.choice(case_sc) if yc[i] else rng.choice(pops[names[gi[i]]]) for i in range(200)])
            for j, k in enumerate(names):
                sel = gi == j
                if sel.any(): U[k].append(u[sel]); vp[k].update(u[sel], yc[sel].astype(int))
d = pd.DataFrame(rows); d.to_csv(os.path.join(H, "addendum_results", "posthoc_group_labelfree.csv.gz"), index=False)
q = d[d.month >= 7].assign(over=lambda x: x.fpr > 0.12)
print(q.groupby(["model", "group", "method"]).agg(fpr=("fpr", "mean"), p=("over", "mean"), sens=("sens", "mean")).round(3).unstack("method").to_string())
