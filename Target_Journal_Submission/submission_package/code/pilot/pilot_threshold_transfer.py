import pandas as pd, numpy as np, glob
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score
m = pd.read_csv("sampleMetadata.csv", low_memory=False).set_index("sample_id")
studies = ["FengQ_2015","GuptaA_2019","HanniganGD_2017","ThomasAM_2018a","ThomasAM_2018b","ThomasAM_2019_c","VogtmannE_2016","WirbelJ_2018","YachidaS_2019","YuJ_2015","ZellerG_2014"]
X = []; meta = []
for s in studies:
    a = pd.read_csv(f"ra/{s}.csv", index_col=0)
    a.index = [i.split("|")[-1] for i in a.index]
    a = a.T; md = m.loc[a.index]
    keep = md.study_condition.isin(["CRC", "control"]).values
    X.append(a[keep]); meta.append(md[keep].assign(study=s))
X = pd.concat(X).fillna(0); meta = pd.concat(meta)
y = (meta.study_condition == "CRC").astype(int).values
L = np.log10(X.values / 100 + 1e-5)
print(X.shape, y.mean())
rows = []
for s in studies:
    te = (meta.study == s).values; tr = ~te
    prev = (X.values[tr] > 0).mean(0) > 0.05
    Ltr, Lte = L[tr][:, prev], L[te][:, prev]
    mu, sd = Ltr.mean(0), Ltr.std(0) + 1e-6
    for name, clf in [("LASSO-LR", LogisticRegression(penalty="l1", C=0.1, solver="liblinear", class_weight="balanced")),
                      ("RF", RandomForestClassifier(500, n_jobs=4, random_state=0, min_samples_leaf=2))]:
        Ztr, Zte = (Ltr - mu) / sd, (Lte - mu) / sd
        oof = cross_val_predict(clf, Ztr, y[tr], cv=StratifiedKFold(5, shuffle=True, random_state=0), method="predict_proba")[:, 1]
        thr = np.quantile(oof[y[tr] == 0], 0.90)  # 90% spec on training controls (out-of-fold)
        clf.fit(Ztr, y[tr]); p = clf.predict_proba(Zte)[:, 1]
        yt = y[te]
        oracle = np.quantile(p[yt == 0], 0.90)
        rows.append(dict(study=s, model=name, auc=roc_auc_score(yt, p), spec=(p[yt == 0] < thr).mean(), sens=(p[yt == 1] >= thr).mean(),
                         sens_oracle=(p[yt == 1] >= oracle).mean()))
r = pd.DataFrame(rows); print(r.round(3).to_string())
print(r.groupby("model")[["auc", "spec", "sens", "sens_oracle"]].agg(["mean", "min", "max"]).round(3))
from scipy import stats
print("\n== overdispersion of realised FPR vs binomial(alpha=0.1) ==")
for name in ["LASSO-LR","RF"]:
    rr = r[r.model==name]; chi=0; out=[]
    for _,q in rr.iterrows():
        n0 = int(((meta.study==q.study)&(y==0)).sum()); fp = round((1-q.spec)*n0)
        chi += (fp-0.1*n0)**2/(n0*0.1*0.9); out.append((q.study[:10], n0, fp, round(stats.binomtest(fp,n0,0.1).pvalue,4)))
    print(name, "chi2=",round(chi,1),"df=",len(rr),"p=",stats.chi2.sf(chi,len(rr)), out)
