"""P2 heterogeneity, P3 covariates (as specified + extended), P7 fold-model scoring. Reads results/atlas_rows_v4.csv.gz."""
import os, json, numpy as np, pandas as pd, statsmodels.formula.api as smf, warnings; warnings.filterwarnings("ignore")
from scipy import stats
from common_v4 import *
A = 0.10
r = pd.read_csv(os.path.join(OUT, "atlas_rows_v4.csv.gz")); H = r[~r.study.str.startswith("TRAIN")].copy()
def subset(strict):
    if not strict: return H
    h = H[(H.strict_person == True) & ~H.study.isin(STRICT_DROP_STUDIES)]
    return h[h.groupby(["disease", "model", "study"]).study.transform("size") >= MIN_N]
def dl(k, n):
    y = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v
    mu = np.sum(w * y) / w.sum(); Q = np.sum(w * (y - mu) ** 2); df = len(y) - 1
    tau2 = max(0, (Q - df) / (w.sum() - (w ** 2).sum() / w.sum())); ws = 1 / (v + tau2); mus = np.sum(ws * y) / ws.sum(); se = ws.sum() ** -.5
    t = stats.t.ppf(.975, len(y) - 2); ex = lambda x: 1 / (1 + np.exp(-x))
    return dict(pooled=ex(mus), tau=np.sqrt(tau2), I2=max(0, (Q - df) / Q) if Q > 0 else 0, Q=Q, Q_p=stats.chi2.sf(Q, df),
                pi_lo=ex(mus - t * np.sqrt(tau2 + se ** 2)), pi_hi=ex(mus + t * np.sqrt(tau2 + se ** 2)))
def exp_oob(n):  # P(Binom(n,.1)/n outside [.05,.15]) under perfect calibration
    k = np.arange(n + 1); f = k / n; return stats.binom.pmf(k, n, A)[(f < .05) | (f > .15)].sum()
het, per = [], []
for strict in [True, False]:
    for (d, m), g in subset(strict).groupby(["disease", "model"]):
        c = g.groupby("study").agg(n=("flag", "size"), k=("flag", "sum"), kf=("flag_folds", "sum")).reset_index(); c["fpr"] = c.k / c.n
        c["fpr_folds"] = c.kf / c.n; c = c.assign(disease=d, model=m, strict=strict); per.append(c)
        oob = ((c.fpr < .05) | (c.fpr > .15)).mean(); e = np.mean([exp_oob(n) for n in c.n]); big = c[c.n >= 100]
        het.append(dict(strict=strict, disease=d, model=m, populations=len(c), people=int(c.n.sum()), **dl(c.k.values, c.n.values),
                        fpr_min=c.fpr.min(), fpr_max=c.fpr.max(), p10=c.fpr.quantile(.1), p90=c.fpr.quantile(.9),
                        n100_pops=len(big), n100_min=big.fpr.min(), n100_max=big.fpr.max(), n100_oob=((big.fpr < .05) | (big.fpr > .15)).mean(),
                        oob_obs=oob, oob_exp=e, oob_excess=oob - e, pooled_raw=c.k.sum() / c.n.sum(),
                        pooled_raw_folds=c.kf.sum() / c.n.sum(), max_abs_fpr_change_folds=(c.fpr_folds - c.fpr).abs().max(),
                        mean_score_shift_folds=float((g.score_folds - g.score).mean())))
het = pd.DataFrame(het); pd.concat(per).to_csv(os.path.join(OUT, "atlas_perpop_v4.csv"), index=False); het.to_csv(os.path.join(OUT, "heterogeneity_v4.csv"), index=False)
pd.set_option("display.width", 250); print(het.round(3).to_string())
# training-cohort OOF control FPR (reference)
T = r[r.study.str.startswith("TRAIN")].groupby(["disease", "model"]).flag.mean(); print("TRAIN OOF FPR\n", T.round(3).to_string())
# P3 covariates
ids = set(H.sample_id); cov = []
for s in H.study.unique():
    Xc, md = controls(s); P = Xc.values / np.maximum(Xc.values.sum(1, keepdims=True), 1e-12)
    cov.append(pd.DataFrame(dict(shannon=-(np.where(P > 0, P * np.log(np.where(P > 0, P, 1)), 0)).sum(1), richness=(P > 0).sum(1)), index=Xc.index))
C = pd.concat(cov); C = C[~C.index.duplicated()].join(META[["age", "gender", "BMI", "number_reads"]])
out = []
for strict in [True, False]:
    for (d, m), g in subset(strict).groupby(["disease", "model"]):
        g = g.join(C, on="sample_id"); g["logdepth"] = np.log10(g.number_reads); g["male"] = (g.gender == "male").astype(float)
        avail = g.study.nunique(); g = g.dropna(subset=["age", "BMI", "gender", "logdepth"]); g = g[g.groupby("study").study.transform("size") >= 10]
        g = g.assign(z=(g.score - g.score.mean()) / g.score.std())
        f0 = smf.mixedlm("z ~ 1", g, groups=g.study).fit(); icc = lambda f: float(f.cov_re.iloc[0, 0] / (f.cov_re.iloc[0, 0] + f.scale))
        row = dict(strict=strict, disease=d, model=m, people=len(g), pops_used=g.study.nunique(), pops_available=avail, icc_raw=icc(f0))
        for tag, fml in [("spec", "z ~ age + male + BMI + logdepth"), ("ext", "z ~ age + male + BMI + logdepth + shannon + richness")]:
            f1 = smf.mixedlm(fml, g, groups=g.study).fit()
            row.update({f"icc_{tag}": icc(f1), f"between_var_change_{tag}": f1.cov_re.iloc[0, 0] / f0.cov_re.iloc[0, 0] - 1,
                        **{f"p_{tag}_{k}": f1.pvalues[k] for k in ["age", "male", "BMI", "logdepth"]}})
        out.append(row)
o = pd.DataFrame(out); o.to_csv(os.path.join(OUT, "covariates_v4.csv"), index=False); print(o.round(3).T.to_string())
