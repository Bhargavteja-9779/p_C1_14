"""Endpoints and tests from protocol.md section 6-7. Usage: python3 analyze_final.py [results|dryrun]"""
import sys, os, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "results")
S = pd.read_csv(os.path.join(D, "sequential.csv.gz")); O = pd.read_csv(os.path.join(D, "oneshot.csv.gz"))
rng = np.random.default_rng(2026); out = []
def p(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

late = S[S.month >= 7].copy(); late["over"] = late.fpr > late.alpha + 0.02; late["abs_err"] = (late.fpr - late.alpha).abs()
S["fp1000"] = 1000 * (1 - S.pi) * S.fpr; S["miss1000"] = 1000 * S.pi * (1 - S.sens)

for setting in S.setting.unique():
    q = late[late.setting == setting]
    tab = q.groupby(["disease", "pi", "method"]).agg(p_over=("over", "mean"), abs_err=("abs_err", "mean"),
                                                     fpr=("fpr", "mean"), sens=("sens", "mean")).round(3)
    p(f"\n##### setting = {setting} (months 7-12)\n" + tab.unstack("method").to_string())
for setting in ["drift", "combined"]:
    q = S[(S.setting == setting)].copy(); q["over"] = q.fpr > q.alpha + 0.02
    q["period"] = pd.cut(q.month, [0, 6, 9, 12, 18], labels=["1-6", "7-9", "10-12", "13-18"])
    p(f"\n##### {setting}: by period (mean FPR / P(FPR>alpha+0.02))\n" +
      q.groupby(["disease", "period", "method"], observed=True).agg(fpr=("fpr", "mean"), p_over=("over", "mean")).round(3).unstack("method").to_string())
prim = late[late.setting == "primary"]
p("\n##### harms per 1,000 screened, primary, 12-month average\n" +
  S[S.setting == "primary"].groupby(["disease", "model", "pi", "method"])[["fp1000", "miss1000"]].mean().round(2).unstack("method").to_string())
p("\n##### burn-in (month 1) referral rate, primary\n" +
  S[(S.setting == "primary") & (S.month == 1)].groupby(["disease", "method"]).refer.mean().round(3).unstack().to_string())

# H1: paired over site x model, per disease and pooled; endpoint averaged over pi and reps
unit = prim.groupby(["disease", "site", "model", "method"]).over.mean().unstack("method")
def boot_diff(u, a, b, n=2000):
    sites = u.index.get_level_values("site").unique(); diffs = []
    for _ in range(n):
        pick = rng.choice(sites, len(sites)); diffs.append(np.mean([(u.xs(s, level="site")[a] - u.xs(s, level="site")[b]).mean() for s in pick]))
    return np.percentile(diffs, [2.5, 97.5])
for grp, u in [("pooled", unit)] + [(d, unit.xs(d, level="disease", drop_level=False)) for d in unit.index.get_level_values("disease").unique()]:
    for comp in ["source", "local_q", "contam"]:
        d = u["vp"] - u[comp]
        w = stats.wilcoxon(u["vp"], u[comp], alternative="less", zero_method="zsplit") if len(d) > 1 and (d != 0).any() else None
        ci = boot_diff(u, "vp", comp)
        p(f"H1 {grp}: vp - {comp}: mean diff {d.mean():+.3f} (95% CI {ci[0]:+.3f}, {ci[1]:+.3f}); n={len(d)}; "
          f"Wilcoxon one-sided p={w.pvalue:.4g}" if w else f"H1 {grp}: vp - {comp}: no variation")
# H2: sensitivity non-inferiority vs oracle
us = prim.groupby(["disease", "site", "model", "method"]).sens.mean().unstack("method")
ci = boot_diff(us, "vp", "oracle")
p(f"H2 pooled: sens(vp) - sens(oracle) = {(us.vp - us.oracle).mean():+.3f}, 95% CI ({ci[0]:+.3f}, {ci[1]:+.3f}); "
  f"non-inferior at -0.05: {ci[0] > -0.05}")
p("\n##### one-shot analysis (mean FPR / sens)\n" + O.groupby(["disease", "pi", "method"])[["fpr", "sens"]].mean().round(3).unstack("method").to_string())
p("\n##### per-site primary endpoint (vp vs source vs local_q)\n" + unit[["source", "local_q", "contam", "vp", "oracle"]].round(3).to_string())
open(os.path.join(D, "summary.txt"), "w").write("\n".join(out))

# ---------------- Part B / C ----------------
if os.path.exists(os.path.join(D, "partB_positivity.csv")):
    pB = pd.read_csv(os.path.join(D, "partB_positivity.csv")); aB = pd.read_csv(os.path.join(D, "partB_adjusted_holm.csv"))
    p("\n##### Part B positivity vs own controls\n" + pB.round(3).to_string())
    p("\n##### Part B adjusted coefficients (H3; Holm within model)\n" + aB.round(4).to_string())
    pC = pd.read_csv(os.path.join(D, "partC_groupcal.csv.gz")); q = pC[pC.month >= 7].assign(over=lambda x: x.fpr > 0.12)
    p("\n##### Part C months 7-18: FPR / P(FPR>0.12) / sensitivity proxy per group\n" +
      q.groupby(["model", "group", "method"]).agg(fpr=("fpr", "mean"), p_over=("over", "mean"), sens=("sens_proxy", "mean")).round(3).unstack("method").to_string())
    ov = q.assign(wf=q.fpr * q.share).groupby(["model", "method", "rep", "month"]).wf.sum().groupby(["model", "method"]).mean()
    p("\n##### Part C overall FPR\n" + ov.round(3).to_string())
    open(os.path.join(D, "summary.txt"), "w").write("\n".join(out))
