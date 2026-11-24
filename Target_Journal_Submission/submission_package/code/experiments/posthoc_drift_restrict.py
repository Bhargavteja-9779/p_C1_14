"""POST HOC P4: (a) downward drift (-0.5 logit from month 7) at the locked sites; (b) primary endpoint restricted to sites
with >= 40 controls, aggregated to the cohort level (one unit per distinct cohort: mean over models/diseases), with
Wilcoxon over cohorts; (c) high-confidence variant (delta = 0.10) in the primary resampled setting."""
import sys, os, numpy as np, pandas as pd
from scipy import stats
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, "final")); sys.path.insert(0, os.path.join(H, ".."))
sys.argv = ["x", "--dryrun"]   # import helpers only; we pass items explicitly
import run_final as RF
from src import calibrate as C
items = list(np.load(os.path.join(H, "final", "results", "scores.npz"), allow_pickle=True)["items"])
rng = np.random.default_rng(11); rows = []; R = 60
for disease, site, model, s_src, y_src, st, yt in items:
    P0, P1 = st[yt == 0], st[yt == 1]; pi = 0.10 if disease == "adenoma" else 0.01
    for r in range(R):
        for o in RF.simulate(s_src, y_src, P0, P1, pi, rng, drift=-0.5, months=18):
            rows.append(dict(disease=disease, site=site, model=model, rep=r, **o))
d = pd.DataFrame(rows); d["per"] = pd.cut(d.month, [0, 6, 9, 12, 18], labels=["1-6", "7-9", "10-12", "13-18"])
print("(a) downward drift: mean FPR / sensitivity by period")
print(d.groupby(["per", "method"], observed=True).agg(fpr=("fpr", "mean"), sens=("sens", "mean")).round(3).unstack("method").to_string())
d.to_csv(os.path.join(H, "addendum_results", "posthoc_drift_down.csv.gz"), index=False)
# (b) restricted, cohort-level
S = pd.read_csv(os.path.join(H, "final", "results", "sequential.csv.gz")); S = S[(S.setting == "primary") & (S.month >= 7)]
n0 = {(i[0], i[1]): int((i[6] == 0).sum()) for i in items}
S["n0"] = [n0[(a, b)] for a, b in zip(S.disease, S.site)]; S["over"] = S.fpr > 0.12
big = S[S.n0 >= 40]; u = big.groupby(["site", "method"]).over.mean().unstack()
print("\n(b) sites with >= 40 controls:", sorted(big.site.unique()), "n cohorts =", len(u))
print(u[["source", "local_q", "contam", "vp", "oracle"]].round(3).to_string())
for comp in ["source", "local_q", "contam"]:
    dd = u.vp - u[comp]; w = stats.wilcoxon(u.vp, u[comp], alternative="less", zero_method="zsplit")
    print(f"vp - {comp}: mean {dd.mean():+.3f}, cohorts {len(dd)}, one-sided Wilcoxon p = {w.pvalue:.3g}")
print("mean FPR (>=40 controls):", big.groupby("method").fpr.mean().round(3).to_dict())
