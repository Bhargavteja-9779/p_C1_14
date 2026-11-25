"""Review round 10 corrections (POST HOC; original result files are kept unchanged):
(1) v6c: correct population-clustered bootstrap (resampling WITH duplicates; run_v6c.py used set(), a ~63% subsample).
(2) v6c: level-free heterogeneity check: per-test median absolute deviation and SD of FPR on the probability scale,
    plus median FPR per arm (logit tau shrinks mechanically when FPRs move from ~0 towards 0.5).
(3) v6b: correct study-clustered bootstrap (each draw relabelled as its own cluster; analyse_v6b.py merged duplicates).
Writes results/corrected_boot_v13.json."""
import json, numpy as np, pandas as pd, importlib.util, os
H = os.path.dirname(os.path.abspath(__file__)); os.chdir(H); out = {}
def dl_tau(k, n):
    y = np.log((k + .5) / (n - k + .5)); v = 1 / (k + .5) + 1 / (n - k + .5); w = 1 / v; mu = (w * y).sum() / w.sum(); Q = (w * (y - mu) ** 2).sum()
    return float(np.sqrt(max(0, (Q - len(y) + 1) / (w.sum() - (w ** 2).sum() / w.sum()))))
# (1)+(2) v6c
R = pd.read_csv("results/v6c_rows.csv"); pops = R["pop"].unique(); G = {p: R[R["pop"] == p] for p in pops}
def mtau(D, arm): return np.mean([dl_tau(g.k.values, g.n.values) for _, g in D[D.arm == arm].groupby("test") if len(g) >= 3])
rng = np.random.default_rng(5); db = []
for i in range(2000):
    D = pd.concat([G[p].assign(pop=f"{p}#{j}") for j, p in enumerate(rng.choice(pops, len(pops)))]); db.append(mtau(D, "balanced") - mtau(D, "naive"))
per = []
for (t, arm), g in R.groupby(["test", "arm"]):
    f = g.fpr.values; per.append(dict(test=t, arm=arm, median_fpr=float(np.median(f)), mad_fpr=float(np.median(np.abs(f - np.median(f)))), sd_fpr=float(f.std(ddof=1)),
                                       tau=dl_tau(g.k.values, g.n.values), mean_abs_err=float(np.abs(f - .10).mean())))
P = pd.DataFrame(per); w = P.pivot(index="test", columns="arm")
out["v6c"] = dict(diff=float(mtau(R, "balanced") - mtau(R, "naive")), ci95_corrected=[float(np.percentile(db, 2.5)), float(np.percentile(db, 97.5))],
                  per_test=P.round(4).to_dict("records"),
                  tests_tau_lower=int((w.tau.balanced < w.tau.naive).sum()), tests_mad_lower=int((w.mad_fpr.balanced < w.mad_fpr.naive).sum()),
                  tests_sd_lower=int((w.sd_fpr.balanced < w.sd_fpr.naive).sum()), tests_abs_err_lower=int((w.mean_abs_err.balanced < w.mean_abs_err.naive).sum()),
                  mean_mad=dict(naive=float(w.mad_fpr.naive.mean()), balanced=float(w.mad_fpr.balanced.mean())),
                  mean_abs_err=dict(naive=float(w.mean_abs_err.naive.mean()), balanced=float(w.mean_abs_err.balanced.mean())))
# (3) v6b
spec = importlib.util.spec_from_file_location("a6b", "analyse_v6b.py"); src = open("analyse_v6b.py").read().split("o = summ(R)")[0]
ns = {}; exec(src, ns); summ, R6 = ns["summ"], ns["R"]
o = summ(R6); base = 1 - o["balanced"]["gap"] / o["naive"]["gap"]; st = R6.study_name.unique(); S = {s: R6[R6.study_name == s] for s in st}
rng = np.random.default_rng(11); bg, ba = [], []
for i in range(2000):
    D = pd.concat([S[s].assign(study_name=f"{s}#{j}") for j, s in enumerate(rng.choice(st, len(st)))])
    try:
        sb = summ(D); bg.append(1 - sb["balanced"]["gap"] / sb["naive"]["gap"]); ba.append(sb["balanced"]["auroc"] - sb["naive"]["auroc"])
    except Exception: pass
out["v6b"] = dict(rel_gap_reduction=float(base), ci95_corrected=[float(np.nanpercentile(bg, 2.5)), float(np.nanpercentile(bg, 97.5))],
                  share_draws_below_050=float(np.mean(np.array(bg) < .5)), auroc_diff_ci95_corrected=[float(np.percentile(ba, 2.5)), float(np.percentile(ba, 97.5))], draws=len(bg))
json.dump(out, open("results/corrected_boot_v13.json", "w"), indent=1)
print(json.dumps({k: {a: b for a, b in v.items() if a != "per_test"} for k, v in out.items()}, indent=1)); print(P.round(3).to_string())
