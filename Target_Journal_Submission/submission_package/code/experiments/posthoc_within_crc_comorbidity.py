"""POST HOC (after locked analysis and addendum): comorbidity inside CRC screening/colonoscopy cohorts.
Controls (colonoscopy-negative) and CRC cases carry comorbidity labels (disease field: T2D, hypertension, fatty_liver,
hypercholesterolemia) in FengQ_2015, ThomasAM_2018a (development; leave-one-cohort-out scores) and YuJ_2015 (locked
site; scores from the frozen final run). Question 1: are comorbid controls flagged more often than healthy controls at
the source 90%-specificity cut-off? Question 2: do comorbid CRC cases score higher (relevant to per-group sensitivity)?"""
import sys, os, numpy as np, pandas as pd, statsmodels.api as sm
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src.data import load, DEV_CRC, LOCKED_CRC
from src import calibrate as C
COM = ["T2D", "hypertension", "fatty_liver", "hypercholesterolemia"]
Zd = np.load(os.path.join(H, "dev", "scores_dev.npz"))
Xd, yd, gd, Md = load("CRC", DEV_CRC)
items = list(np.load(os.path.join(H, "final", "results", "scores.npz"), allow_pickle=True)["items"])
Xf, yf, gf, Mf = load("CRC", DEV_CRC + LOCKED_CRC)
rows = []
for model in ["lasso", "rf"]:
    for site in ["FengQ_2015", "ThomasAM_2018a", "YuJ_2015"]:
        if site in DEV_CRC:
            st = Zd[f"{model}|{site}|tgt"]; s_src, y_src = Zd[f"{model}|{site}|src"], Zd[f"{model}|{site}|ysrc"]; md = Md[gd == site]
        else:
            it = [i for i in items if i[0] == "CRC" and i[1] == site and i[2] == model][0]; s_src, y_src, st = it[3], it[4], it[5]; md = Mf[gf == site]
        t = C.source_threshold(s_src, y_src, 0.10)
        dis = md.disease.fillna("")
        rows.append(pd.DataFrame(dict(model=model, site=site, score=st, pos=(st >= t).astype(float), case=(md.study_condition == "CRC").astype(int).values,
                                      comorbid=dis.apply(lambda x: any(k in x for k in COM)).astype(int).values, disease=dis.values,
                                      age=pd.to_numeric(md.age, errors="coerce").values, BMI=pd.to_numeric(md.BMI, errors="coerce").values,
                                      male=(md.gender == "male").astype(float).values)))
D = pd.concat(rows, ignore_index=True)
D.to_csv(os.path.join(H, "addendum_results", "posthoc_within_crc.csv"), index=False)
print("counts\n", D[D.model == "lasso"].groupby(["site", "case", "comorbid"]).size().unstack().to_string())
out = []
for model in ["lasso", "rf"]:
    for grp, lab in [(0, "controls"), (1, "CRC cases")]:
        q = D[(D.model == model) & (D.case == grp)]
        print(f"\n{model} {lab}: positivity by comorbidity per site\n", q.groupby(["site", "comorbid"]).pos.agg(["mean", "size"]).round(3).unstack().to_string())
        qq = q.dropna(subset=["age", "BMI"]); Xr = pd.get_dummies(qq.site, drop_first=True, dtype=float)
        Xr = sm.add_constant(pd.concat([qq[["comorbid", "age", "BMI", "male"]], Xr], axis=1).astype(float))
        r = sm.OLS(qq.score, Xr).fit(); rl = sm.Logit(qq.pos, Xr).fit(disp=0)
        out.append(dict(model=model, group=lab, n=len(qq), n_comorbid=int(qq.comorbid.sum()), beta_score=r.params["comorbid"],
                        lo=r.conf_int().loc["comorbid", 0], hi=r.conf_int().loc["comorbid", 1], p=r.pvalues["comorbid"],
                        OR_pos=np.exp(rl.params["comorbid"]), OR_lo=np.exp(rl.conf_int().loc["comorbid", 0]), OR_hi=np.exp(rl.conf_int().loc["comorbid", 1]),
                        p_pos=rl.pvalues["comorbid"], pos_comorbid=qq[qq.comorbid == 1].pos.mean(), pos_healthy=qq[qq.comorbid == 0].pos.mean()))
O = pd.DataFrame(out); O.to_csv(os.path.join(H, "addendum_results", "posthoc_within_crc_summary.csv"), index=False)
pd.set_option("display.width", 250); print("\nPooled (site fixed effects; adjusted age, BMI, sex)\n", O.round(4).to_string())
