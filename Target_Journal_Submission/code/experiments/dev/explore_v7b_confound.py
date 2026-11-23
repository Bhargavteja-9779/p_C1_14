"""DEV ONLY. Round 7b: is excess CRC-test positivity in chronic conditions explained by age / BMI / sex?
Within-cohort logistic regression: positive ~ condition + age + BMI + sex (cohort controls as reference).
Also: does multi-condition 'control augmentation' (Thomas 2019) remove it? (train CRC model with extra non-CRC
disease samples labelled negative, using leave-one-cohort-out over the comorbidity cohorts)."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC, CACHE
from src.models import preprocess_fit, preprocess_apply, make, logit
import statsmodels.api as sm
COH = {"JieZ_2017": "ACVD", "QinN_2014": "cirrhosis", "LiJ_2017": "hypertension", "LoombaR_2017": "fatty_liver",
       "NagySzakalD_2017": "ME/CFS", "XieH_2016": "asthma", "ZhuF_2020": "schizophrenia"}
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
def cohort(c):
    a = pd.read_csv(os.path.join(CACHE, "ra", f"{c}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
    a = a.groupby(level=0).sum().T; md = meta.loc[meta.index.intersection(a.index)]
    md = md[(md.study_name == c) & (md.body_site == "stool") & md.age_category.isin(["adult", "senior"])]
    md = md[md.study_condition.isin(["control", COH[c]])]
    md = md.assign(_d=pd.to_numeric(md.get("days_from_first_collection"), errors="coerce").fillna(0)).sort_values("_d")
    md = md[~md.subject_id.duplicated()]; return a.loc[md.index], md
X, y, g, M = load("CRC", DEV_CRC); cols = X.columns
C = {c: cohort(c) for c in COH}
rows, fits = [], []
for model in ["lasso"]:
    for aug in [False, True]:
        for c in COH:
            Xtr, ytr = X.values, y.copy()
            if aug:   # add all OTHER comorbidity cohorts' samples as negatives
                extra = [C[o][0].reindex(columns=cols, fill_value=0).fillna(0).values for o in COH if o != c]
                Xtr = np.vstack([Xtr] + extra); ytr = np.concatenate([ytr, np.zeros(sum(len(e) for e in extra), int)])
            p = preprocess_fit(Xtr); m = make(model).fit(preprocess_apply(Xtr, p), ytr)
            s0 = logit(m.predict_proba(preprocess_apply(X.values[y == 0], p))[:, 1]); t = np.quantile(s0, 0.90)  # in-sample CRC ctrl (approx.)
            A, md = C[c]; sc = logit(m.predict_proba(preprocess_apply(A.reindex(columns=cols, fill_value=0).fillna(0).values, p))[:, 1])
            md = md.assign(score=sc, pos=(sc >= t).astype(int), dis=(md.study_condition != "control").astype(int))
            for cond, q in md.groupby("dis"):
                rows.append(dict(model=model, aug=aug, cohort=c, group="disease" if cond else "control", n=len(q), pos=q.pos.mean()))
            if not aug:
                d = md[["score", "dis", "age", "BMI", "gender"]].copy(); d["male"] = (d.gender == "male").astype(float)
                covs = [k for k in ["age", "BMI", "male"] if d[k].notna().mean() > 0.8 and d[k].nunique() > 1]
                d = d.dropna(subset=covs)
                for spec, cv in [("crude", []), ("adjusted", covs)]:
                    r = sm.OLS(d.score, sm.add_constant(d[["dis"] + cv].astype(float))).fit()
                    fits.append(dict(cohort=c, spec=spec, covs="+".join(cv), n=len(d), beta_dis=r.params["dis"],
                                     ci_lo=r.conf_int().loc["dis", 0], ci_hi=r.conf_int().loc["dis", 1], p=r.pvalues["dis"]))
r = pd.DataFrame(rows).pivot_table(index=["cohort", "group"], columns="aug", values="pos")
print("Positivity at 90%-spec threshold, without / with control augmentation\n", r.round(3).to_string())
print("\nScore difference (logit) disease - control, crude vs adjusted for age/BMI/sex\n", pd.DataFrame(fits).round(3).to_string())
