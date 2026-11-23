"""DEV ONLY. Round 9: which species make the CRC test fire in chronic disease, and can a specificity-constrained
signature remove the excess without losing CRC accuracy?
(1) LASSO CRC model on 8 DEV CRC cohorts; per comorbidity cohort, decompose the score difference condition - own
    controls into species contributions: coef_j * (mean z_j | condition - mean z_j | control).
(2) 'Shared-dysbiosis' species = CRC-model species whose shift has the same sign as their CRC coefficient in >= K of
    the comorbidity cohorts (estimated in DEV comorbidity cohorts, leave-one-cohort-out when evaluating).
(3) Specificity-constrained model: retrain excluding shared-dysbiosis species. Evaluate CRC AUC (LOCO over DEV CRC
    cohorts) and positivity ratio in the held-out comorbidity cohort."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC, CACHE
from src.models import preprocess_fit, preprocess_apply, make, logit
from sklearn.metrics import roc_auc_score
COH = {"JieZ_2017": "ACVD", "QinN_2014": "cirrhosis", "LiJ_2017": "hypertension", "LoombaR_2017": "fatty_liver",
       "NagySzakalD_2017": "ME/CFS", "XieH_2016": "asthma", "ZhuF_2020": "schizophrenia"}
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
X, y, g, M = load("CRC", DEV_CRC); cols = X.columns
def cohort(c):
    a = pd.read_csv(os.path.join(CACHE, "ra", f"{c}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
    a = a.groupby(level=0).sum().T; md = meta.loc[meta.index.intersection(a.index)]
    md = md[(md.study_name == c) & (md.body_site == "stool") & md.study_condition.isin(["control", COH[c]])]
    md = md[~md.subject_id.duplicated()]
    return a.loc[md.index].reindex(columns=cols, fill_value=0).fillna(0).values, (md.study_condition != "control").values.astype(int)
CO = {c: cohort(c) for c in COH}
# (1) decomposition with the full model
p = preprocess_fit(X.values); Z = preprocess_apply(X.values, p); feat = cols[p["keep"]]
m = make("lasso").fit(Z, y); coef = pd.Series(m.coef_[0], index=feat)
print("non-zero CRC species:", (coef != 0).sum())
contrib = {}
for c, (A, d) in CO.items():
    Za = preprocess_apply(A, p); contrib[c] = pd.Series(coef.values * (Za[d == 1].mean(0) - Za[d == 0].mean(0)), index=feat)
Ct = pd.DataFrame(contrib); Ct = Ct[(coef != 0).values]
Ct["n_pos"] = (Ct[list(COH)] > 0).sum(1); Ct["coef"] = coef[Ct.index]; Ct["total"] = Ct[list(COH)].sum(1)
print("\nScore gap (condition - control) explained by CRC species, sum of contributions:\n", Ct[list(COH)].sum().round(2).to_string())
print("\nTop 15 species driving false alarms (sum over 7 conditions):\n", Ct.sort_values("total", ascending=False).head(15)[["coef", "n_pos", "total"] + list(COH)].round(3).to_string())
Ct.to_csv(os.path.join(os.path.dirname(__file__), "explore_v9_contrib.csv"))
# (2)-(3) specificity-constrained signature, leave-one-comorbidity-cohort-out
def shared_species(exclude, K):
    s = []
    for c, (A, d) in CO.items():
        if c == exclude: continue
        Za = preprocess_apply(A, p); s.append(np.sign(coef.values) * (Za[d == 1].mean(0) - Za[d == 0].mean(0)) > 0.2)
    return feat[(np.sum(s, 0) >= K) & (coef.values != 0)]
rows = []
for K in [None, 4, 3, 2]:
    for c, (A, d) in CO.items():
        drop = set() if K is None else set(shared_species(c, K))
        keepcols = [j for j, f in enumerate(cols) if f not in drop]
        Xk = X.values[:, keepcols]; Ak = A[:, keepcols]
        # CRC LOCO AUC on DEV CRC cohorts (thresholds from LOCO controls)
        aucs = []
        for s in DEV_CRC:
            te = g == s; pp = preprocess_fit(Xk[~te]); mm = make("lasso").fit(preprocess_apply(Xk[~te], pp), y[~te])
            aucs.append(roc_auc_score(y[te], mm.predict_proba(preprocess_apply(Xk[te], pp))[:, 1]))
        pp = preprocess_fit(Xk); mm = make("lasso").fit(preprocess_apply(Xk, pp), y)
        oof = np.zeros(len(y))
        for s in DEV_CRC:
            te = g == s; p2 = preprocess_fit(Xk[~te]); m2 = make("lasso").fit(preprocess_apply(Xk[~te], p2), y[~te])
            oof[te] = logit(m2.predict_proba(preprocess_apply(Xk[te], p2))[:, 1])
        t = np.quantile(oof[y == 0], 0.9); sc = logit(mm.predict_proba(preprocess_apply(Ak, pp))[:, 1])
        sens = (oof[y == 1] >= t).mean()
        rows.append(dict(K=str(K), heldout=c, n_drop=len(drop), crc_auc=np.mean(aucs), crc_sens_oof=sens,
                         pos_dis=(sc[d == 1] >= t).mean(), pos_ctrl=(sc[d == 0] >= t).mean()))
    print("K", K, "done", flush=True)
R = pd.DataFrame(rows); R["ratio"] = R.pos_dis / R.pos_ctrl.clip(lower=1e-3)
R.to_csv(os.path.join(os.path.dirname(__file__), "explore_v9_constrained.csv"), index=False)
print(R.round(3).to_string())
print(R.groupby("K")[["n_drop", "crc_auc", "crc_sens_oof", "pos_dis", "pos_ctrl"]].mean().round(3).to_string())
