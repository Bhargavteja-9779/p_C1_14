"""Plan v6b: NAIVE vs case-mix BALANCED GMWI2-recipe classifiers, leave-one-study-out on cMD."""
import os, sys, json, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from scipy import stats, sparse
from multiprocessing import Pool
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v4"))
from common_v4 import excluded, CACHE
OUT = os.path.join(HERE, "results")
DIS = {"IBD", "T2D", "CRC", "IGT", "CAD", "ACVD", "adenoma", "cirrhosis", "hypertension", "HF", "AS", "schizophrenia", "fatty_liver",
       "ME/CFS", "migraine", "PD", "T1D", "melanoma", "BD", "asthma"}
EA = {"CHN", "JPN", "KOR"}
M = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
def build():
    mats, metas = [], []; ex = excluded()
    for f in sorted(os.listdir(os.path.join(CACHE, "ra"))):
        s = f[:-4]; raw = pd.read_csv(os.path.join(CACHE, "ra", f), index_col=0)
        md = M.loc[M.index.intersection(raw.columns)]; md = md[(md.study_name == s) & (md.body_site == "stool") & md.age_category.isin(["adult", "senior"])]
        lab = np.where((md.study_condition == "control") & (md.disease == "healthy"), 1, np.where(md.study_condition.isin(DIS), 0, -1))
        md = md.assign(healthy=lab)[lab >= 0]
        md = md.assign(_d=pd.to_numeric(md.get("days_from_first_collection"), errors="coerce").fillna(0)).sort_values("_d"); md = md[~md.subject_id.duplicated()]
        md = md[~md.index.isin(ex)]
        if not len(md): continue
        mats.append((raw[md.index] / 100 > 1e-5)); metas.append(md[["study_name", "country", "healthy"]])
    X = pd.concat(mats, axis=1).fillna(False).astype(bool).T; Mt = pd.concat(metas)
    return X.loc[Mt.index], Mt
def fit(args):
    s, mode = args
    tr = Mt.study_name.values != s; Xtr, ytr = X[tr], y[tr]
    keep = np.asarray(Xtr.mean(0)).ravel() >= 0.01
    if mode == "balanced":
        key = pd.Series(list(zip(Mt.country.values[tr], ytr))); w = 1.0 / key.map(key.value_counts()).values; w = w * len(w) / w.sum()
    else: w = None
    m = LogisticRegression(penalty="l1", C=0.03, solver="liblinear", class_weight="balanced", max_iter=2000).fit(Xtr[:, keep], ytr, sample_weight=w)
    te = ~tr; d = m.decision_function(X[te][:, keep])
    return s, mode, np.where(te)[0], d
if __name__ == "__main__":
    Xdf, Mt = build(); X = sparse.csr_matrix(Xdf.values.astype(np.float32)); y = Mt.healthy.values.astype(int)
    print("samples", X.shape, "healthy", y.sum(), "studies", Mt.study_name.nunique(), flush=True)
    jobs = [(s, m) for s in Mt.study_name.unique() for m in ["naive", "balanced"]]
    with Pool(4) as P: res = P.map(fit, jobs)
    D = {m: np.full(len(y), np.nan) for m in ["naive", "balanced"]}
    for s, m, idx, d in res: D[m][idx] = d
    R = Mt.assign(naive=D["naive"], balanced=D["balanced"]); R.to_csv(os.path.join(OUT, "v6b_loso_scores.csv.gz"))
    print("done", flush=True)
