"""EXPLORATORY (post hoc, after addendum A1 results): metformin and the CRC-test score.
(1) Replication within T2D in a non-locked cohort (LiJ_2014) and within T2D in MetaCardis.
(2) Species decomposition of the metformin effect in MetaCardis (LASSO): coef x (mean z | metformin - mean z | no),
    among T2D patients."""
import sys, os, numpy as np, pandas as pd, statsmodels.api as sm
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src.data import load, DEV_CRC, CACHE
from src.models import train_and_score, preprocess_fit, preprocess_apply, logit
from src import calibrate as C
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
X, y, g, M = load("CRC", DEV_CRC); cols = X.columns; idx = np.arange(len(y)); rows = []
for model in ["lasso", "rf"]:
    s_src, y_src, _, m = train_and_score(X.values, y, g, idx, idx[:1], model, seed=2026)
    p = preprocess_fit(X.values); t = C.source_threshold(s_src, y_src, 0.10); feat = cols[p["keep"]]
    for c in ["LiJ_2014", "MetaCardis_2020_a", "QinJ_2012", "KarlssonFH_2013"]:
        a = pd.read_csv(os.path.join(CACHE, "ra", f"{c}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
        a = a.groupby(level=0).sum().T; md = meta.loc[meta.index.intersection(a.index)]
        md = md[(md.study_name == c) & (md.body_site == "stool") & (md.study_condition == "T2D")]
        md = md[~md.subject_id.duplicated()]
        Z = preprocess_apply(a.loc[md.index].reindex(columns=cols, fill_value=0).fillna(0).values, p)
        sc = logit(m.predict_proba(Z)[:, 1]); met = md.treatment.fillna("").str.contains("metformin").values
        if met.sum() < 5 or (~met).sum() < 5: print(c, "too few", met.sum(), (~met).sum()); continue
        d = pd.DataFrame(dict(score=sc, met=met.astype(float), male=(md.gender == "male").astype(float).values,
                              age=pd.to_numeric(md.age, errors="coerce").values, BMI=pd.to_numeric(md.BMI, errors="coerce").values))
        covs = [k for k in ["age", "BMI"] if d[k].notna().mean() >= 0.8] + (["male"] if d.male.nunique() > 1 else [])
        d = d.dropna(subset=covs); r = sm.OLS(d.score, sm.add_constant(d[["met"] + covs])).fit()
        rows.append(dict(model=model, cohort=c, n_met=int(d.met.sum()), n_no=int((d.met == 0).sum()), beta=r.params["met"],
                         lo=r.conf_int().loc["met", 0], hi=r.conf_int().loc["met", 1], p=r.pvalues["met"],
                         pos_met=(sc[met] >= t).mean(), pos_no=(sc[~met] >= t).mean(), covs="+".join(covs)))
        if model == "lasso" and c == "MetaCardis_2020_a":
            coef = m.coef_[0]; contrib = pd.Series(coef * (Z[met].mean(0) - Z[~met].mean(0)), index=feat)
            top = contrib[coef != 0].sort_values(ascending=False)
            print("\nTop species driving the metformin effect (T2D, MetaCardis):\n", top.head(10).round(3).to_string())
            print("sum of contributions:", round(contrib.sum(), 3))
            top.to_csv(os.path.join(H, "addendum_results", "metformin_species_contrib.csv"))
R = pd.DataFrame(rows); R.to_csv(os.path.join(H, "addendum_results", "metformin_within_T2D.csv"), index=False)
pd.set_option("display.width", 250); print(R.round(4).to_string())
