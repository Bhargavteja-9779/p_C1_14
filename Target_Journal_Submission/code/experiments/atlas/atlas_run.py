"""Protocol v3: healthy-population false-positive atlas. Writes results/atlas_rows.csv.gz and atlas_coefs.csv."""
import os, sys, numpy as np, pandas as pd
from multiprocessing import Pool
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, CACHE, DISEASES, _near_dup_mask
from src.pipeline import Pipeline
OUT = os.path.join(os.path.dirname(__file__), "results"); os.makedirs(OUT, exist_ok=True)
ALPHA = 0.10
META = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")

def healthy_studies():
    m = META[(META.body_site == "stool") & (META.study_condition == "control") & META.age_category.isin(["adult", "senior"])]
    n = m.groupby("study_name").size(); return sorted(n[n >= 20].index)

def load_controls(s):
    a = pd.read_csv(os.path.join(CACHE, "ra", f"{s}.csv"), index_col=0)
    a.index = [i.split("|")[-1] for i in a.index]; a = a.groupby(level=0).sum().T
    md = META.loc[META.index.intersection(a.index)]
    md = md[(md.study_name == s) & (md.body_site == "stool") & (md.study_condition == "control") & md.age_category.isin(["adult", "senior"])]
    md = md.assign(_d=pd.to_numeric(md.get("days_from_first_collection"), errors="coerce").fillna(0)).sort_values("_d")
    md = md[~md.subject_id.duplicated()]
    X = a.loc[md.index].fillna(0.0); d = _near_dup_mask(X.values)
    return X[~d], md[~d]

def job(args):
    disease, model = args
    X, y, g, M = load(disease)
    p = Pipeline(model).fit(X.values, y, g)
    t = float(np.quantile(p.oof[y == 0], 1 - ALPHA))
    train_st = set(DISEASES[disease]["studies"]) | ({"ThomasAM_2019_c"} if disease == "CRC" else set())
    rows = []
    for s in healthy_studies():
        if s in train_st or not os.path.exists(os.path.join(CACHE, "ra", f"{s}.csv")): continue
        Xc, md = load_controls(s)
        Xa = Xc.reindex(columns=X.columns, fill_value=0.0).fillna(0.0).values
        sc = p.score(Xa)
        rows.append(pd.DataFrame(dict(disease=disease, model=model, study=s, sample_id=md.index, score=sc, thr=t,
                                      flag=(sc >= t).astype(int), frac_features_present=(Xa > 0).sum(1) / max(1, (Xc.values > 0).sum(1).mean()))))
    # training cohorts' own LOSO OOF control FPR (reference)
    for c in np.unique(g):
        i = (g == c) & (y == 0)
        rows.append(pd.DataFrame(dict(disease=disease, model=model, study="TRAIN:" + c, sample_id=M.index[i], score=p.oof[i], thr=t,
                                      flag=(p.oof[i] >= t).astype(int), frac_features_present=np.nan)))
    coefs = None
    if model == "lasso":
        keep_cols = X.columns[p.keep]
        coefs = pd.DataFrame(dict(disease=disease, taxon=keep_cols, w=p.m.coef_[0], mu=p.mu, sd=p.sd))
    print(disease, model, "done", flush=True)
    return pd.concat(rows), coefs

if __name__ == "__main__":
    jobs = [(d, m) for d in ["CRC", "IBD", "T2D"] for m in ["lasso", "rf"]]
    with Pool(4) as pool: res = pool.map(job, jobs)
    pd.concat([r[0] for r in res]).to_csv(os.path.join(OUT, "atlas_rows.csv.gz"), index=False)
    pd.concat([r[1] for r in res if r[1] is not None]).to_csv(os.path.join(OUT, "atlas_coefs.csv"), index=False)
