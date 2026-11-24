"""POST HOC P5: CRC-specific specificity audit across all 11 CRC cohorts. Development cohorts: leave-one-cohort-out scores
(models trained on the other 7 development cohorts; scores_dev.npz). Locked sites: frozen-run scores (trained on all 8).
The audit evaluates the fixed source cut-off only (no method choice), so development cohorts are valid audit sites.
Reports per-site realised FPR with exact (Clopper-Pearson) 95% CIs, a chi-square overdispersion test against
Binomial(n0, 0.10), and the between-site SD of the logit FPR (DerSimonian-Laird tau)."""
import sys, os, numpy as np, pandas as pd
from scipy import stats
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src.data import DEV_CRC, LOCKED_CRC
from src import calibrate as C
Zd = np.load(os.path.join(H, "dev", "scores_dev.npz"))
items = list(np.load(os.path.join(H, "final", "results", "scores.npz"), allow_pickle=True)["items"])
rows = []
for model in ["lasso", "rf"]:
    for site in DEV_CRC + LOCKED_CRC:
        if site in DEV_CRC:
            s_src, y_src, st, yt = (Zd[f"{model}|{site}|{k}"] for k in ["src", "ysrc", "tgt", "ytgt"]); role = "development (LOCO)"
        else:
            it = [i for i in items if i[0] == "CRC" and i[1] == site and i[2] == model][0]; s_src, y_src, st, yt = it[3], it[4], it[5], it[6]; role = "locked"
        t = C.source_threshold(s_src, y_src, 0.10); c = st[yt == 0]; k = int((c >= t).sum()); n = len(c)
        lo, hi = stats.beta.ppf(0.025, k, n - k + 1) if k > 0 else 0.0, stats.beta.ppf(0.975, k + 1, n - k) if k < n else 1.0
        rows.append(dict(model=model, site=site, role=role, n_controls=n, fp=k, fpr=k / n, ci_lo=lo, ci_hi=hi,
                         sens=(st[yt == 1] >= t).mean(), p_binom=stats.binomtest(k, n, 0.10).pvalue))
D = pd.DataFrame(rows); out = []
for model in ["lasso", "rf"]:
    q = D[D.model == model]
    chi = (((q.fp - 0.1 * q.n_controls) ** 2) / (q.n_controls * 0.09)).sum(); df = len(q)
    y_ = np.log((q.fp + 0.5) / (q.n_controls - q.fp + 0.5)); v = 1 / (q.fp + 0.5) + 1 / (q.n_controls - q.fp + 0.5); w = 1 / v
    Q = (w * (y_ - (w * y_).sum() / w.sum()) ** 2).sum(); tau2 = max(0, (Q - (df - 1)) / (w.sum() - (w ** 2).sum() / w.sum()))
    out.append(dict(model=model, sites=df, fpr_min=q.fpr.min(), fpr_max=q.fpr.max(), n_over_012=int((q.fpr > 0.12).sum()),
                    n_ci_excludes_010=int(((q.ci_lo > 0.10) | (q.ci_hi < 0.10)).sum()), chi2=chi, p_overdispersion=stats.chi2.sf(chi, df),
                    tau_logit=np.sqrt(tau2), I2=max(0, (Q - (df - 1)) / Q) if Q > 0 else 0))
O = pd.DataFrame(out)
D.to_csv(os.path.join(H, "addendum_results", "posthoc_crc_audit_sites.csv"), index=False); O.to_csv(os.path.join(H, "addendum_results", "posthoc_crc_audit_summary.csv"), index=False)
pd.set_option("display.width", 250); print(D.round(3).to_string()); print(O.round(4).to_string())
