"""Protocol addendum A1 (protocol_addendum_drugs.md). Usage: python3 addendum_drugs.py dev | confirm"""
import sys, os, numpy as np, pandas as pd, statsmodels.api as sm
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src.data import load, DEV_CRC, CACHE
from src.models import train_and_score, preprocess_fit, preprocess_apply, logit
from src import calibrate as C
MODE = sys.argv[1]; OUT = os.path.join(H, "addendum_results"); os.makedirs(OUT, exist_ok=True)
ORAL = ["Streptococcus", "Veillonella", "Fusobacterium", "Gemella", "Peptostreptococcus", "Parvimonas", "Porphyromonas",
        "Lactobacillus_salivarius", "Actinomyces", "Haemophilus", "Solobacterium", "Dialister_pneumosintes", "Rothia",
        "Prevotella_intermedia", "Prevotella_nigrescens", "Campylobacter", "Eikenella", "Granulicatella", "Atopobium", "Filifactor"]
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
X, y, g, M = load("CRC", DEV_CRC); cols = X.columns; idx = np.arange(len(y))
cohorts = ["VincentC_2016", "LeeKA_2022", "JieZ_2017"] if MODE == "dev" else ["MetaCardis_2020_a"]
rows, pos_rows = [], []
for model in ["lasso", "rf"]:
    s_src, y_src, _, m = train_and_score(X.values, y, g, idx, idx[:1], model, seed=2026)
    p = preprocess_fit(X.values); t = C.source_threshold(s_src, y_src, 0.10)
    feat = cols[p["keep"]]
    if model == "lasso":
        coef = m.coef_[0]; oral = np.array([any(o in f for o in ORAL) and c > 0 for f, c in zip(feat, coef)])
    for c in cohorts:
        a = pd.read_csv(os.path.join(CACHE, "ra", f"{c}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
        a = a.groupby(level=0).sum().T; md = meta.loc[meta.index.intersection(a.index)]
        md = md[(md.study_name == c) & (md.body_site == "stool") & md.age_category.isin(["adult", "senior"])]
        md = md.assign(_d=pd.to_numeric(md.get("days_from_first_collection"), errors="coerce").fillna(0)).sort_values("_d")
        md = md[~md.subject_id.duplicated()]
        Z = preprocess_apply(a.loc[md.index].reindex(columns=cols, fill_value=0).fillna(0).values, p)
        sc = logit(m.predict_proba(Z)[:, 1]); tr = md.treatment.fillna("")
        d = pd.DataFrame(dict(score=sc, pos=(sc >= t).astype(float), ppi=tr.str.contains("PPI").astype(float).values,
                              metformin=tr.str.contains("metformin").astype(float).values, statin=tr.str.contains("statin").astype(float).values,
                              aspirin=tr.str.contains(r"\basa\b").astype(float).values, betablocker=tr.str.contains("beta_block").astype(float).values,
                              age=pd.to_numeric(md.age, errors="coerce").values, BMI=pd.to_numeric(md.BMI, errors="coerce").values,
                              male=(md.gender == "male").astype(float).values, cond=md.study_condition.values), index=md.index)
        if model == "lasso": d["oral"] = Z[:, oral] @ coef[oral]
        covs = [k for k in ["age", "BMI"] if d[k].notna().mean() >= 0.8] + (["male"] if d.male.nunique() > 1 else [])
        drugs = [k for k in ["metformin", "statin", "aspirin", "betablocker"] if d[k].sum() >= 10 and k != "ppi"] if MODE == "confirm" else []
        conds = pd.get_dummies(d.cond, prefix="c", drop_first=True, dtype=float) if d.cond.nunique() > 1 else pd.DataFrame(index=d.index)
        dd = pd.concat([d, conds], axis=1).dropna(subset=covs)
        Xr = sm.add_constant(dd[["ppi"] + list(conds.columns) + covs + drugs].astype(float))
        for outcome in (["score", "oral"] if model == "lasso" else ["score"]):
            r = sm.OLS(dd[outcome], Xr).fit()
            for v in ["ppi"] + drugs:
                rows.append(dict(model=model, cohort=c, outcome=outcome, term=v, n=len(dd), n_ppi=int(dd.ppi.sum()), beta=r.params[v],
                                 lo=r.conf_int().loc[v, 0], hi=r.conf_int().loc[v, 1],
                                 p_one_sided=r.pvalues[v] / 2 if r.params[v] > 0 else 1 - r.pvalues[v] / 2, covs="+".join(covs + drugs)))
        if model == "lasso":   # mediation (descriptive): add oral component
            r2 = sm.OLS(dd.score, pd.concat([Xr, dd[["oral"]]], axis=1)).fit()
            rows.append(dict(model=model, cohort=c, outcome="score|oral", term="ppi", n=len(dd), n_ppi=int(dd.ppi.sum()), beta=r2.params["ppi"],
                             lo=r2.conf_int().loc["ppi", 0], hi=r2.conf_int().loc["ppi", 1], p_one_sided=np.nan, covs="+oral"))
        u, nu = dd[dd.ppi == 1].pos, dd[dd.ppi == 0].pos
        rng = np.random.default_rng(1); bs = [u.sample(frac=1, replace=True, random_state=b).mean() / max(nu.sample(frac=1, replace=True, random_state=b).mean(), 1e-9) for b in range(2000)]
        pos_rows.append(dict(model=model, cohort=c, n_ppi=len(u), n_no=len(nu), pos_ppi=u.mean(), pos_no=nu.mean(), rr=u.mean() / max(nu.mean(), 1e-9),
                             rr_lo=np.percentile(bs, 2.5), rr_hi=np.percentile(bs, 97.5)))
        if MODE == "confirm":   # positivity by PPI within each condition group
            for cond, q in dd.groupby("cond"):
                pos_rows.append(dict(model=model, cohort=c + ":" + cond, n_ppi=int(q.ppi.sum()), n_no=int((q.ppi == 0).sum()),
                                     pos_ppi=q[q.ppi == 1].pos.mean(), pos_no=q[q.ppi == 0].pos.mean(), rr=np.nan, rr_lo=np.nan, rr_hi=np.nan))
R = pd.DataFrame(rows); P = pd.DataFrame(pos_rows)
R.to_csv(os.path.join(OUT, f"{MODE}_regression.csv"), index=False); P.to_csv(os.path.join(OUT, f"{MODE}_positivity.csv"), index=False)
pd.set_option("display.width", 250); print(R.round(4).to_string()); print(P.round(3).to_string())
