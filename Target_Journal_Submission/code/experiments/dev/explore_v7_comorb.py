"""DEV ONLY. Round 7 (exploratory): do CRC microbiome classifiers flag non-cancer conditions more often?
CRC model trained on the 8 DEV CRC cohorts; threshold = source 90% specificity. Scored on non-locked cohorts with
other conditions; positivity compared WITHIN cohort (condition vs that cohort's own controls) to separate
condition effects from site effects. Locked cohorts (MetaCardis, QinJ, KarlssonFH, IBD/T2D/CRC test) not used."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC, CACHE
from src.models import preprocess_fit, preprocess_apply, make, logit, train_and_score
from scipy import stats
COHORTS = ["JieZ_2017", "QinN_2014", "LiJ_2017", "ChengpingW_2017", "ZhuF_2020", "LoombaR_2017", "LiJ_2014",
           "VilaAV_2018", "HMP_2019_t2d", "NagySzakalD_2017", "XieH_2016"]
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
X, y, g, M = load("CRC", DEV_CRC); cols = X.columns
rows = []
for model in ["lasso", "rf"]:
    Xv = X.values; idx = np.arange(len(y))
    s_src, y_src, _, m = train_and_score(Xv, y, g, idx, idx[:1], model)
    t = np.quantile(s_src[y_src == 0], 0.90)
    p = preprocess_fit(Xv)
    for c in COHORTS:
        a = pd.read_csv(os.path.join(CACHE, "ra", f"{c}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
        a = a.groupby(level=0).sum().T; md = meta.loc[meta.index.intersection(a.index)]
        md = md[(md.study_name == c) & (md.body_site == "stool") & md.age_category.isin(["adult", "senior"])]
        md = md.assign(_d=pd.to_numeric(md.get("days_from_first_collection"), errors="coerce").fillna(0)).sort_values("_d")
        md = md[~md.subject_id.duplicated()]
        A = a.loc[md.index].reindex(columns=cols, fill_value=0.0).fillna(0.0).values
        sc = logit(m.predict_proba(preprocess_apply(A, p))[:, 1])
        for cond, q in md.assign(score=sc, pos=sc >= t).groupby("study_condition"):
            rows.append(dict(model=model, cohort=c, condition=cond, n=len(q), pos_rate=q.pos.mean(), med_score=q.score.median()))
        # medication within cohort (if annotated)
        tr = md.treatment.fillna("NA").str.contains("metformin")
        if tr.sum() >= 10:
            rows.append(dict(model=model, cohort=c, condition="metformin_users", n=int(tr.sum()), pos_rate=(sc[tr.values] >= t).mean(), med_score=np.median(sc[tr.values])))
d = pd.DataFrame(rows)
ctrl = d[d.condition == "control"].set_index(["model", "cohort"]).pos_rate.rename("ctrl_rate")
d = d.join(ctrl, on=["model", "cohort"]); d["ratio"] = d.pos_rate / d.ctrl_rate
print(d.round(3).to_string()); d.to_csv(os.path.join(os.path.dirname(__file__), "explore_v7_comorb.csv"), index=False)
