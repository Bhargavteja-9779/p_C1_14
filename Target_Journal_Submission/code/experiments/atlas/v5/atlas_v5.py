"""v5 atlas: 14 diseases x {LASSO, RF}. Writes results/atlas_rows_v5.csv.gz, tests_v5.csv (AUROC, n), coefs_v5.csv."""
import os, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from multiprocessing import Pool
from sklearn.metrics import roc_auc_score
from common_v5 import *
from src.data import _near_dup_mask
from src.pipeline import Pipeline
TESTS = {"CRC": ("CRC", DISEASES["CRC"]["studies"]), "adenoma": ("adenoma", DISEASES["adenoma"]["studies"]),
         "IBD": ("IBD", DISEASES["IBD"]["studies"]), "T2D": ("T2D", DISEASES["T2D"]["studies"]),
         "IGT": ("IGT", ["HMP_2019_t2d", "KarlssonFH_2013", "MetaCardis_2020_a"]), "CAD": ("CAD", ["MetaCardis_2020_a"]),
         "HF": ("HF", ["MetaCardis_2020_a"]), "ACVD": ("ACVD", ["JieZ_2017"]), "cirrhosis": ("cirrhosis", ["QinN_2014"]),
         "hypertension": ("hypertension", ["LiJ_2017"]), "schizophrenia": ("schizophrenia", ["ZhuF_2020"]),
         "ME/CFS": ("ME/CFS", ["NagySzakalD_2017"]), "migraine": ("migraine", ["XieH_2016"]), "fatty_liver": ("fatty_liver", ["LoombaR_2017"])}
EXC = excluded()
def load_cc(case, studies):
    Xs, Ms = [], []
    for s in studies:
        a = pd.read_csv(os.path.join(CACHE, "ra", f"{s}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]; a = a.groupby(level=0).sum().T
        md = META.loc[META.index.intersection(a.index)]; md = md[(md.study_name == s) & (md.body_site == "stool") & md.study_condition.isin([case, "control"])]
        md = md[md.age_category.isin(["adult", "senior"]) | (md.study_condition == case)]
        md = md.assign(_d=pd.to_numeric(md.get("days_from_first_collection"), errors="coerce").fillna(0)).sort_values("_d"); md = md[~md.subject_id.duplicated()]
        Xs.append(a.loc[md.index]); Ms.append(md.assign(study=s))
    X = pd.concat(Xs).fillna(0.0); M = pd.concat(Ms); k = ~X.index.isin(EXC); X, M = X[k], M[k]
    d = _near_dup_mask(X.values); X, M = X[~d], M[~d]
    return X, (M.study_condition == case).astype(int).values, M.study.values, M
def job(a):
    name, model = a; case, studies = TESTS[name]; X, y, g, M = load_cc(case, studies)
    p = Pipeline(model).fit(X.values, y, g); t = float(np.quantile(p.oof[y == 0], 1 - A)); rows = []
    info = dict(test=name, model=model, n_cases=int(y.sum()), n_controls=int((y == 0).sum()), cohorts=len(set(studies)), auroc=roc_auc_score(y, p.oof),
                train_fpr=float(np.mean(p.oof[y == 0] >= t)), train_sens=float(np.mean(p.oof[y == 1] >= t)))
    for s in healthy_studies():
        if s in studies or s in dropped_studies() or not os.path.exists(os.path.join(CACHE, "ra", f"{s}.csv")): continue
        Xc, md = controls(s)
        if len(Xc) < MIN_N: continue
        sc = p.score(Xc.reindex(columns=X.columns, fill_value=0.0).fillna(0.0).values)
        rows.append(pd.DataFrame(dict(test=name, model=model, study=s, sample_id=md.index, strict_person=md.strict_person.values, score=sc, thr=t, flag=(sc >= t).astype(int))))
    coefs = pd.DataFrame(dict(test=name, taxon=X.columns[p.keep], w=p.m.coef_[0], mu=p.mu, sd=p.sd)) if model == "lasso" else None
    print(name, model, round(info["auroc"], 3), flush=True); return pd.concat(rows), coefs, info
if __name__ == "__main__":
    f = os.path.join(OUT5, "atlas_rows_v5.csv.gz"); assert not os.path.exists(f), "already run"
    with Pool(4) as P: res = P.map(job, [(n, m) for n in TESTS for m in ["lasso", "rf"]])
    pd.concat([r[0] for r in res]).to_csv(f, index=False)
    pd.concat([r[1] for r in res if r[1] is not None]).to_csv(os.path.join(OUT5, "coefs_v5.csv"), index=False)
    pd.DataFrame([r[2] for r in res]).to_csv(os.path.join(OUT5, "tests_v5.csv"), index=False)
    print(pd.DataFrame([r[2] for r in res]).round(3).to_string())
