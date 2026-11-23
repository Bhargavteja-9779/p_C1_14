"""POST-HOC robustness (not pre-registered; added after review round 1).
Local controls drawn from a DIFFERENT centre/cohort than the deployment site, vs same-site controls.
(a) MetaCardis (T2D LOSO model trained on the other T2D cohorts): calibrate on 20 controls of centre A, evaluate FPR on controls of centre B.
(b) External CRC (one model trained on the 8 dev cohorts): calibrate on 20 controls of cohort A, evaluate FPR in cohort B."""
import os, sys, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from src.data import load
from src import calibrate as C
R, n, alpha = 200, 20, 0.10; rng = np.random.default_rng(7); rows = []
def run(label, groups, cal_scores, ev_scores_full, same):
    for r in range(R):
        if same:  # same-site: half split, as in the main analysis
            p = rng.permutation(len(ev_scores_full)); cal = ev_scores_full[p[: len(p) // 2][:n]]; ev = ev_scores_full[p[len(p) // 2:]]
        else:
            cal = rng.choice(cal_scores, n, replace=False); ev = ev_scores_full
        t = C.local_controls_conformal(alpha, cal); rows.append(dict(**groups, rep=r, fpr=(ev >= t).mean()))
# (a) MetaCardis centres
X, y, g, M = load("T2D"); loc = M.location.values[g == "MetaCardis_2020_a"]
for model in ["lasso", "rf"]:
    z = np.load(os.path.join(HERE, "scores", f"T2D_MetaCardis_2020_a_{model}.npz")); st, yt = z["st"], z["yt"]
    for A in ["Copenhagen", "Leipzig", "Paris"]:
        for B in ["Copenhagen", "Leipzig", "Paris"]:
            cA, cB = st[(yt == 0) & (loc == A)], st[(yt == 0) & (loc == B)]
            run("metacardis", dict(setting="MetaCardis centres", model=model, cal=A, deploy=B), cA, cB, A == B)
# (b) external CRC cohorts
for model in ["lasso", "rf"]:
    S = {s: np.load(os.path.join(HERE, "scores", f"CRC_{s}_{model}.npz")) for s in ["YachidaS_2019", "YuJ_2015", "ThomasAM_2019_c"]}
    for A in S:
        for B in S:
            cA = S[A]["st"][S[A]["yt"] == 0]; cB = S[B]["st"][S[B]["yt"] == 0]
            run("crc", dict(setting="External CRC cohorts", model=model, cal=A, deploy=B), cA, cB, A == B)
d = pd.DataFrame(rows); d.to_csv(os.path.join(HERE, "mismatch_rows.csv.gz"), index=False)
s = d.groupby(["setting", "model", "cal", "deploy"]).agg(mean_fpr=("fpr", "mean"), p_gt_015=("fpr", lambda x: (x > 0.15).mean())).reset_index()
s["same_site"] = s.cal == s.deploy
txt = s.round(3).to_string(index=False) + "\n\nSummary (mean over pairs):\n" + s.groupby(["setting", "same_site"])[["mean_fpr", "p_gt_015"]].agg(["mean", "min", "max"]).round(3).to_string()
open(os.path.join(HERE, "mismatch_analysis.txt"), "w").write(txt); print(txt)
