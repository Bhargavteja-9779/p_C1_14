"""POST HOC P2: MetaCardis condition effects on the CRC-test score adjusted for medications, and species-level
decomposition of the heart-failure and T2D score gaps in the locked cohort (LASSO)."""
import sys, os, numpy as np, pandas as pd, statsmodels.api as sm
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src.data import load, DEV_CRC, CACHE
from src.models import train_and_score, preprocess_fit, preprocess_apply, logit
from src import calibrate as C
ORAL = ["Streptococcus", "Veillonella", "Fusobacterium", "Gemella", "Peptostreptococcus", "Parvimonas", "Porphyromonas",
        "Lactobacillus_salivarius", "Actinomyces", "Haemophilus", "Solobacterium", "Dialister_pneumosintes", "Rothia",
        "Prevotella_intermedia", "Prevotella_nigrescens", "Campylobacter", "Eikenella", "Granulicatella", "Atopobium", "Filifactor"]
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
X, y, g, M = load("CRC", DEV_CRC); cols = X.columns; idx = np.arange(len(y)); rows, dec = [], []
for model in ["lasso", "rf"]:
    s_src, y_src, _, m = train_and_score(X.values, y, g, idx, idx[:1], model, seed=2026)
    p = preprocess_fit(X.values); t = C.source_threshold(s_src, y_src, 0.10); feat = cols[p["keep"]]
    c = "MetaCardis_2020_a"
    a = pd.read_csv(os.path.join(CACHE, "ra", f"{c}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
    a = a.groupby(level=0).sum().T; md = meta.loc[meta.index.intersection(a.index)]
    md = md[(md.study_name == c) & (md.body_site == "stool") & md.age_category.isin(["adult", "senior"])]
    md = md[~md.subject_id.duplicated()]
    Z = preprocess_apply(a.loc[md.index].reindex(columns=cols, fill_value=0).fillna(0).values, p)
    sc = logit(m.predict_proba(Z)[:, 1]); tr = md.treatment.fillna("")
    d = pd.DataFrame(dict(score=sc, pos=(sc >= t).astype(float), cond=md.study_condition.values, male=(md.gender == "male").astype(float).values,
                          ppi=tr.str.contains("PPI").astype(float).values, metformin=tr.str.contains("metformin").astype(float).values,
                          statin=tr.str.contains("statin").astype(float).values, aspirin=tr.str.contains(r"\basa\b").astype(float).values,
                          betablocker=tr.str.contains("beta_block").astype(float).values,
                          age=pd.to_numeric(md.age, errors="coerce").values, BMI=pd.to_numeric(md.BMI, errors="coerce").values))
    print(model, "age recorded", round(d.age.notna().mean(), 3), "BMI recorded", round(d.BMI.notna().mean(), 3))
    D = pd.get_dummies(d.cond, dtype=float).drop(columns="control")
    for spec, cv in [("sex", ["male"]), ("sex+drugs", ["male", "ppi", "metformin", "statin", "aspirin", "betablocker"])]:
        r = sm.OLS(d.score, sm.add_constant(pd.concat([D, d[cv]], axis=1))).fit()
        for k in D.columns:
            rows.append(dict(model=model, spec=spec, condition=k, beta=r.params[k], lo=r.conf_int().loc[k, 0], hi=r.conf_int().loc[k, 1], p=r.pvalues[k]))
    sub = d.dropna(subset=["age", "BMI"])   # complete-case sensitivity with age/BMI
    if len(sub) > 200:
        Ds = pd.get_dummies(sub.cond, dtype=float).drop(columns="control")
        r = sm.OLS(sub.score, sm.add_constant(pd.concat([Ds, sub[["male", "age", "BMI", "ppi", "metformin", "statin", "aspirin", "betablocker"]]], axis=1))).fit()
        for k in Ds.columns:
            rows.append(dict(model=model, spec=f"complete-case age+BMI+sex+drugs (n={len(sub)})", condition=k, beta=r.params[k],
                             lo=r.conf_int().loc[k, 0], hi=r.conf_int().loc[k, 1], p=r.pvalues[k]))
    if model == "lasso":
        coef = m.coef_[0]; oral = np.array([any(o in f for o in ORAL) and cc > 0 for f, cc in zip(feat, coef)])
        ctrl = d.cond.values == "control"
        for k in ["HF", "T2D", "CAD", "IGT"]:
            gi = d.cond.values == k; contrib = coef * (Z[gi].mean(0) - Z[ctrl].mean(0))
            dec.append(dict(condition=k, total=contrib.sum(), oral=contrib[oral].sum(), depletion=contrib[coef < 0].sum(),
                            other=contrib[(coef > 0) & ~oral].sum()))
        for k, lab in [("metformin", "metformin users vs non-users (T2D)")]:
            gi = (d.cond.values == "T2D"); mu = gi & (d.metformin.values == 1); nu = gi & (d.metformin.values == 0)
            contrib = coef * (Z[mu].mean(0) - Z[nu].mean(0))
            dec.append(dict(condition=lab, total=contrib.sum(), oral=contrib[oral].sum(), depletion=contrib[coef < 0].sum(), other=contrib[(coef > 0) & ~oral].sum()))
R = pd.DataFrame(rows); Dc = pd.DataFrame(dec)
R.to_csv(os.path.join(H, "addendum_results", "posthoc_metacardis_drugadjusted.csv"), index=False)
Dc.to_csv(os.path.join(H, "addendum_results", "posthoc_metacardis_decomposition.csv"), index=False)
pd.set_option("display.width", 250); print(R.round(4).to_string()); print(Dc.round(3).to_string())
