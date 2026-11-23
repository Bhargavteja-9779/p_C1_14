"""POST-HOC analyses added after review round 1 (not pre-registered). Output: post_review1.txt
A. Cohort characteristics (controls): country, platform, median reads, age, BMI.
B. Drivers of control-score shift: Spearman vs log read-depth ratio; within-platform/country checks.
C. MetaCardis restricted to 'healthy' controls: status-quo FPR and conformal n=20.
D. Percentile normalisation against controls (Gibbons 2018), target normalised against the same 20 local controls,
   then the training threshold (CRC external, LASSO + RF, R=50).
E. Positivity among Yachida adenoma carriers under status-quo vs conformal(n=20) CRC thresholds."""
import os, sys, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from src.data import load, DISEASES, DEV_CRC, LOCKED_CRC, CACHE
from src.models import train_and_score, make, preprocess_fit, preprocess_apply, logit
from src import calibrate as C
out = []; rng = np.random.default_rng(5); alpha = 0.10
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
# ---- A
rows = []
for dz in ["CRC", "IBD", "T2D"]:
    X, y, g, M = load(dz); M = M.assign(y=y)
    for s, q in M.groupby("study"):
        c = q[q.y == 0]
        rows.append(dict(task=dz, cohort=s, country=c.country.mode().iat[0], platform=c.sequencing_platform.mode().iat[0],
                         controls=len(c), cases=int(q.y.sum()), median_reads_M=round(pd.to_numeric(c.number_reads, errors="coerce").median() / 1e6, 1),
                         median_age=pd.to_numeric(c.age, errors="coerce").median(), median_BMI=round(pd.to_numeric(c.BMI, errors="coerce").median(), 1),
                         control_disease=",".join(f"{k}:{v}" for k, v in c.disease.value_counts().head(3).items())))
A = pd.DataFrame(rows); A.to_csv(os.path.join(HERE, "cohort_characteristics.csv"), index=False)
out += ["A. Cohort characteristics (controls)", A.to_string(index=False)]
# ---- B: control-score shift vs read depth ratio (target vs training controls)
info = pd.read_csv(os.path.join(HERE, "locked_cohorts.csv")); d = pd.read_csv(os.path.join(HERE, "locked_rows.csv.gz"))
fpr = d[(d.alpha == 0.1) & (d.method == "source")].groupby(["task", "cohort", "model"]).fpr.mean().reset_index()
B = []
for dz in ["CRC", "IBD", "T2D", "adenoma"]:
    X, y, g, M = load(dz); reads = pd.to_numeric(M.number_reads, errors="coerce").values
    for s in fpr[fpr.task == dz].cohort.unique():
        tr = np.isin(g, DEV_CRC) if dz == "CRC" else g != s
        for model in ["lasso", "rf"]:
            z = np.load(os.path.join(HERE, "scores", f"{dz}_{s}_{model}.npz"))
            B.append(dict(task=dz, cohort=s, model=model, shift=np.median(z["st"][z["yt"] == 0]) - np.median(z["s_src"][z["y_src"] == 0]),
                          log_depth_ratio=np.log10(np.nanmedian(reads[(g == s) & (y == 0)]) / np.nanmedian(reads[tr & (y == 0)])),
                          fpr=fpr[(fpr.task == dz) & (fpr.cohort == s) & (fpr.model == model)].fpr.iat[0]))
B = pd.DataFrame(B)
for v in ["shift", "fpr"]:
    r = stats.spearmanr(B.log_depth_ratio, B[v]); out.append(f"B. log10 depth ratio (target/training controls) vs {v}: rho={r.statistic:.2f} P={r.pvalue:.2g} (n={len(B)})")
r = stats.spearmanr(B.log_depth_ratio, (B.fpr - 0.1).abs()); out.append(f"B. log10 depth ratio vs |FPR-0.10|: rho={r.statistic:.2f} P={r.pvalue:.2g}")
# ---- C: MetaCardis healthy-only controls
X, y, g, M = load("T2D"); dis = M.disease.values
for model in ["lasso", "rf"]:
    z = np.load(os.path.join(HERE, "scores", f"T2D_MetaCardis_2020_a_{model}.npz")); st, yt = z["st"], z["yt"]; dm = dis[g == "MetaCardis_2020_a"]
    t = C.source_threshold(z["s_src"], z["y_src"], alpha)
    for grp in ["healthy", "MS", "IGT"]:
        c = st[(yt == 0) & (dm == grp)]; out.append(f"C. MetaCardis {model} controls={grp} (n={len(c)}): status-quo FPR={np.mean(c >= t):.3f}")
    h = np.where((yt == 0) & (dm == "healthy"))[0]; f = []
    for r_ in range(200):
        p = rng.permutation(h); tc = C.local_controls_conformal(alpha, st[p[:20]]); f.append(np.mean(st[p[len(p)//2:]] >= tc))
    out.append(f"C. MetaCardis {model} healthy-only conformal n=20: mean FPR={np.mean(f):.3f}, P(FPR>0.15)={np.mean(np.array(f) > 0.15):.3f}")
# ---- D + E: CRC external with dev-trained models
X, y, g, M = load("CRC"); Xv = X.values
Xa, ya, ga, Ma = load("adenoma", ["YachidaS_2019"])
ade = Xa.reindex(columns=X.columns, fill_value=0.0).values[ya == 1]
tr = np.isin(g, DEV_CRC)
def pct_norm(A, ref):  # percentile of each feature value within reference (control) samples
    return np.stack([(np.searchsorted(np.sort(ref[:, j]), A[:, j], side="right") / ref.shape[0]) for j in range(A.shape[1])], 1)
p = preprocess_fit(Xv[tr]); keep = p["keep"]
for model in ["lasso", "rf"]:
    # E: adenoma positivity
    te_y = g == "YachidaS_2019"
    s_src, y_src, st, m = train_and_score(Xv, y, g, tr, te_y, model)
    sa = logit(m.predict_proba(preprocess_apply(ade, p))[:, 1]); yt = y[te_y]; i0 = np.where(yt == 0)[0]
    t0 = C.source_threshold(s_src, y_src, alpha); pos_c = []
    for r_ in range(200):
        pp = rng.permutation(i0); pos_c.append(np.mean(sa >= C.local_controls_conformal(alpha, st[pp[:20]])))
    out.append(f"E. Yachida adenoma carriers (n={len(sa)}) {model}: positivity status-quo={np.mean(sa >= t0):.3f}, conformal n=20 mean={np.mean(pos_c):.3f}")
    # D: percentile normalisation
    Ptr = np.zeros((tr.sum(), keep.sum())); Xk = Xv[:, keep]; gi = g[tr]; yi = y[tr]; Xtr = Xk[tr]
    for s in np.unique(gi): Ptr[gi == s] = pct_norm(Xtr[gi == s], Xtr[(gi == s) & (yi == 0)])
    oof = np.zeros(len(yi))
    from sklearn.model_selection import GroupKFold
    for a, b in GroupKFold(len(np.unique(gi))).split(Ptr, yi, gi): oof[b] = make(model).fit(Ptr[a], yi[a]).predict_proba(Ptr[b])[:, 1]
    mm = make(model).fit(Ptr, yi); tP = C.source_threshold(logit(oof), yi, alpha)
    for s in LOCKED_CRC:
        Xs = Xk[g == s]; ys = y[g == s]; j0, j1 = np.where(ys == 0)[0], np.where(ys == 1)[0]; f, se = [], []
        for r_ in range(50):
            pp = rng.permutation(j0); cal, ev = pp[:20], pp[len(pp)//2:]
            sc = logit(mm.predict_proba(pct_norm(Xs, Xs[cal]))[:, 1]); f.append(np.mean(sc[ev] >= tP)); se.append(np.mean(sc[j1] >= tP))
        out.append(f"D. percentile-norm (20 local controls) + training threshold {model} {s}: mean FPR={np.mean(f):.3f} P(FPR>0.15)={np.mean(np.array(f)>0.15):.3f} sens={np.mean(se):.3f}")
txt = "\n".join(map(str, out)); open(os.path.join(HERE, "post_review1.txt"), "w").write(txt); print(txt)
