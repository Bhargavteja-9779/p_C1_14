"""POST-HOC (added after review round 1). Label-free threshold from an unlabelled pool of the first N screened people
at screening-like prevalence pi: pool = N draws (with replacement) from the cohort's calibration-half controls,
each replaced by a case with probability pi. Threshold = (1-alpha) quantile of pool; FPR on evaluation-half controls.
Compared with conformal on 20 labelled controls. All 16 held-out cohorts x 2 models, alpha=0.10, R=200."""
import os, glob, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); rng = np.random.default_rng(11); alpha = 0.10; rows = []
for f in sorted(glob.glob(os.path.join(HERE, "scores", "*.npz"))):
    task, model = os.path.basename(f).split("_")[0], os.path.basename(f)[:-4].split("_")[-1]
    cohort = "_".join(os.path.basename(f)[:-4].split("_")[1:-1]); z = np.load(f); st, yt = z["st"], z["yt"]
    i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
    for r in range(200):
        p = rng.permutation(i0); cal, ev = p[: len(p) // 2], p[len(p) // 2:]
        for pi in [0.005, 0.01, 0.05]:
            for N in [100, 300, 1000]:
                is_case = rng.random(N) < pi
                pool = np.where(is_case, st[rng.choice(i1, N)], st[rng.choice(cal, N)])
                t = np.quantile(pool, 1 - alpha)
                rows.append(dict(task=task, cohort=cohort, model=model, pi=pi, N=N, fpr=(st[ev] >= t).mean(), sens=(st[i1] >= t).mean()))
d = pd.DataFrame(rows); d.to_csv(os.path.join(HERE, "screening_pool_rows.csv.gz"), index=False)
cm = d.groupby(["pi", "N", "task", "cohort", "model"]).fpr.mean().reset_index()
s = cm.groupby(["pi", "N"]).fpr.agg(["mean", "min", "max", "std"]).join(d.groupby(["pi", "N"]).agg(p_gt_015=("fpr", lambda x: (x > 0.15).mean()), sens=("sens", "mean")))
txt = "Cohort-mean FPR across 32 cohort x model pairs, and per-draw P(FPR>0.15):\n" + s.round(3).to_string()
open(os.path.join(HERE, "screening_pool_sim.txt"), "w").write(txt); print(txt)
