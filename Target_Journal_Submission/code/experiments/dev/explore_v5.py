"""DEV ONLY. Round 5: sequential deployment simulation. Each held-out cohort = the site's population (true FPR/sens
computed exactly on all its controls/cases). Monthly batches of B tests drawn with replacement at prevalence pi."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import DEV_CRC
from src import calibrate as C
D = os.path.dirname(__file__); Z = np.load(os.path.join(D, "scores_dev.npz"))
alpha = 0.10; R = 100; B = 100; T = 12; rng = np.random.default_rng(5); rows = []
for model in ["lasso", "rf"]:
    for s in DEV_CRC:
        s_src, y_src, st, yt = (Z[f"{model}|{s}|{k}"] for k in ["src", "ysrc", "tgt", "ytgt"])
        P0, P1 = st[yt == 0], st[yt == 1]
        tfpr = lambda t: (P0 >= t).mean(); tsens = lambda t: (P1 >= t).mean()
        t_src = C.source_threshold(s_src, y_src, alpha); t_burn = np.quantile(s_src[y_src == 0], 1 - 3 * alpha); t_burn2 = np.quantile(s_src[y_src == 0], 1 - 2 * alpha)
        t_oracle = np.quantile(P0, 1 - alpha)
        for pi in [0.01, 0.05, 0.10]:
            pim = max(0.05, pi)
            for r in range(R):
                U = []; L = []; TAU = {k: [] for k in ["vp", "vp2"]}
                th = dict(source=t_src, local_q=t_src, contam=t_src, vp=t_burn, vp2=t_burn2, oracle=t_oracle)
                for month in range(T):
                    y_new = (rng.random(B) < pi).astype(int)
                    u_new = np.where(y_new == 1, rng.choice(P1, B), rng.choice(P0, B))
                    for k, t in th.items():
                        rows.append(dict(model=model, cohort=s, pi=pi, rep=r, month=month + 1, method=k,
                                         fpr=tfpr(t), sens=tsens(t), refer=(u_new >= t).mean()))
                    TAU["vp"].extend([th["vp"]] * B); TAU["vp2"].extend([th["vp2"]] * B); U.extend(u_new); L.extend(y_new)
                    u, lab = np.array(U), np.array(L)
                    th["local_q"] = np.quantile(u, 1 - alpha)
                    th["contam"] = C.contam_quantile(u, alpha, pim)
                    th["vp"] = C.verified_positive_seq(u, np.array(TAU["vp"]), lab, alpha, pim)
                    th["vp2"] = C.verified_positive_seq(u, np.array(TAU["vp2"]), lab, alpha, pim)
d = pd.DataFrame(rows); d.to_csv(os.path.join(D, "explore_v5.csv.gz"), index=False)
d["over12"] = d.fpr > 0.12
for mo in [[1], [2, 3], [4, 6], [7, 12]]:
    q = d[d.month.between(mo[0], mo[-1])]
    print(f"\n=== months {mo[0]}-{mo[-1]} ===")
    print(q.groupby(["model", "pi", "method"]).agg(fpr=("fpr", "mean"), p_over12=("over12", "mean"), sens=("sens", "mean"),
                                                    refer=("refer", "mean")).round(3).unstack("method").to_string())
# harms per 1000 screened over the 12 months (lasso, pi=0.01): extra referrals of controls and missed cases vs oracle
d["fp_per1000"] = 1000 * (1 - d.pi) * d.fpr; d["missed_per1000"] = 1000 * d.pi * (1 - d.sens)
h = d.groupby(["model", "pi", "method"])[["fp_per1000", "missed_per1000"]].mean()
print("\n=== harms per 1,000 screened (12-month average) ===\n", h.round(2).unstack("method").to_string())
print("\nper-cohort months 4-12 mean FPR (lasso, pi=0.05)\n",
      d[(d.model == "lasso") & (d.pi == 0.05) & (d.month >= 4)].groupby(["cohort", "method"]).fpr.mean().unstack().round(3).to_string())
