"""DEV ONLY. Round 8: comorbidity-conditional (Mondrian) sequential recalibration.
Each comorbidity cohort = a site whose screened population mixes healthy controls and people with a chronic condition
(share w, realistic for screening age) plus CRC cases at 1% (OOF CRC case scores; sensitivity proxy).
Methods: source threshold; pooled SequentialRecalibrator; group-conditional SequentialRecalibrator (one per
comorbidity group, comorbidity known from records). Endpoint: per-group FPR, months 7-18."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC, CACHE
from src.models import preprocess_fit, preprocess_apply, make, logit, train_and_score
from src import calibrate as C
SITES = {"JieZ_2017": ("ACVD", 0.20), "QinN_2014": ("cirrhosis", 0.05), "LiJ_2017": ("hypertension", 0.40),
         "LoombaR_2017": ("fatty_liver", 0.25), "NagySzakalD_2017": ("ME/CFS", 0.05)}
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
X, y, g, M = load("CRC", DEV_CRC); cols = X.columns
alpha, pi, B, T, R = 0.10, 0.01, 200, 18, 100; rng = np.random.default_rng(8); rows = []
for model in ["lasso", "rf"]:
    idx = np.arange(len(y)); s_src, y_src, _, m = train_and_score(X.values, y, g, idx, idx[:1], model)
    p = preprocess_fit(X.values); case_sc = s_src[y_src == 1]
    for c, (cond, w) in SITES.items():
        a = pd.read_csv(os.path.join(CACHE, "ra", f"{c}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
        a = a.groupby(level=0).sum().T; md = meta.loc[meta.index.intersection(a.index)]
        md = md[(md.study_name == c) & (md.body_site == "stool") & md.study_condition.isin(["control", cond])]
        md = md[~md.subject_id.duplicated()]
        sc = logit(m.predict_proba(preprocess_apply(a.loc[md.index].reindex(columns=cols, fill_value=0).fillna(0).values, p))[:, 1])
        H, Cm = sc[(md.study_condition == "control").values], sc[(md.study_condition == cond).values]
        for r in range(R):
            pooled = C.SequentialRecalibrator(s_src, y_src, alpha, 0.05)
            grp = {0: C.SequentialRecalibrator(s_src, y_src, alpha, 0.05), 1: C.SequentialRecalibrator(s_src, y_src, alpha, 0.05)}
            t_src = C.source_threshold(s_src, y_src, alpha)
            for month in range(1, T + 1):
                th = dict(source=(t_src, t_src), pooled=(pooled.t, pooled.t), group=(grp[0].t, grp[1].t))
                for k, (t0, t1) in th.items():
                    rows.append(dict(model=model, site=c, cond=cond, rep=r, month=month, method=k,
                                     fpr_healthy=(H >= t0).mean(), fpr_comorb=(Cm >= t1).mean(),
                                     sens_healthy=(case_sc >= t0).mean(), sens_comorb=(case_sc >= t1).mean(),
                                     fpr_overall=(1 - w) * (H >= t0).mean() + w * (Cm >= t1).mean()))
                ycase = rng.random(B) < pi; com = rng.random(B) < w
                u = np.where(ycase, rng.choice(case_sc, B), np.where(com, rng.choice(Cm, B), rng.choice(H, B)))
                lab = ycase.astype(int)
                pooled.update(u, lab)
                for k in (0, 1):
                    sel = com == bool(k); grp[k].update(u[sel], lab[sel])
d = pd.DataFrame(rows); d.to_csv(os.path.join(os.path.dirname(__file__), "explore_v8_groupcal.csv.gz"), index=False)
q = d[d.month >= 7]
q = q.assign(o_h=q.fpr_healthy > 0.12, o_c=q.fpr_comorb > 0.12)
print(q.groupby(["model", "site", "method"]).agg(fpr_h=("fpr_healthy", "mean"), fpr_c=("fpr_comorb", "mean"),
      over_c=("o_c", "mean"), fpr_all=("fpr_overall", "mean"), sens_h=("sens_healthy", "mean"), sens_c=("sens_comorb", "mean")).round(3).to_string())
