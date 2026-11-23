"""DEV ONLY. Round 6: realism stress tests for sequential verified-positive recalibration.
Scenarios: smoothed site population (KDE instead of <= 65 discrete scores); colonoscopy adherence 70%;
colonoscopy misses 5% of cancers (labelled control); 1-month follow-up delay; temporal drift (+0.5 logit shift of all
scores from month 7, e.g. new kit lot / lab protocol); combined. Variants: cumulative pool vs 6-month sliding window."""
import sys, os, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import DEV_CRC
from src import calibrate as C
from scipy import stats
D = os.path.dirname(__file__); Z = np.load(os.path.join(D, "scores_dev.npz"))
alpha = 0.10; R = 60; B = 100; T = 18; rng = np.random.default_rng(6)
SCEN = dict(base={}, smooth=dict(smooth=True), adherence70=dict(adh=0.7), miss5=dict(miss=0.05), delay1=dict(delay=1),
            drift=dict(drift=0.5), combined=dict(smooth=True, adh=0.7, miss=0.05, delay=1, drift=0.5))
def sampler(P, smooth, n):
    x = rng.choice(P, n)
    return x + rng.normal(0, 1.06 * P.std() * len(P) ** -0.2, n) if smooth else x
rows = []
for model in ["lasso", "rf"]:
    for s in DEV_CRC:
        s_src, y_src, st, yt = (Z[f"{model}|{s}|{k}"] for k in ["src", "ysrc", "tgt", "ytgt"])
        P0, P1 = st[yt == 0], st[yt == 1]
        for name, sc in SCEN.items():
            sm, adh, miss, delay, drift = sc.get("smooth", False), sc.get("adh", 1.0), sc.get("miss", 0.0), sc.get("delay", 0), sc.get("drift", 0.0)
            # true population: large sample (smoothed or empirical) for exact-ish FPR
            Q0, Q1 = (sampler(P0, True, 20000), sampler(P1, True, 20000)) if sm else (P0, P1)
            for pi in [0.01, 0.05]:
                pim = 0.05
                for r in range(R):
                    U, L, TAU, MON = [], [], [], []
                    t_src = C.source_threshold(s_src, y_src, alpha)
                    th = dict(source=t_src, local_q=t_src, vp=np.quantile(s_src[y_src == 0], 1 - 2 * alpha))
                    th["vp_win6"] = th["vp"]; th["lq_win6"] = t_src; th["vp_alarm"] = th["vp"]; start = 0; alarms = 0
                    for month in range(1, T + 1):
                        sh = drift if month > 6 else 0.0
                        y_new = (rng.random(B) < pi).astype(int)
                        u_new = np.where(y_new == 1, sampler(P1, sm, B), sampler(P0, sm, B)) + sh
                        for k, t in th.items():
                            rows.append(dict(model=model, cohort=s, scen=name, pi=pi, rep=r, month=month, method=k,
                                             fpr=((Q0 + sh) >= t).mean(), sens=((Q1 + sh) >= t).mean(), refer=(u_new >= t).mean()))
                        att = rng.random(B) < adh                          # attends colonoscopy if referred
                        lab_obs = np.where((y_new == 1) & (rng.random(B) < miss), 0, y_new)   # missed cancers look like controls
                        for key in ["vp", "vp_win6"]:
                            pass
                        TAU.append(dict(vp=np.where(att, th["vp"], np.inf), vp_win6=np.where(att, th["vp_win6"], np.inf),
                                        vp_alarm=np.where(att, th["vp_alarm"], np.inf)))
                        U.append(u_new); L.append(lab_obs); MON.append(month)
                        for key, win in [("vp", T), ("vp_win6", 6)]:
                            lo = max(0, len(U) - win); hi = len(U)
                            u = np.concatenate(U[lo:hi]); lab = np.concatenate(L[lo:hi])
                            tau = np.concatenate([TAU[i][key] if i < hi - delay else np.full(B, np.inf) for i in range(lo, hi)])
                            th[key] = C.verified_positive_seq(u, tau, lab, alpha, pim)
                        # alarm: month whose labels just arrived; exact verified FP count vs Binomial(m0, alpha)
                        j = len(U) - 1 - delay
                        if j >= start + 1:
                            ver = U[j] >= TAU[j]["vp_alarm"]; fp = int((ver & (L[j] == 0)).sum()); m0 = B - int(np.floor(pim * B))
                            if stats.binom.sf(fp - 1, m0, alpha) < 0.01: start = j; alarms += 1
                        lo = start; hi = len(U)
                        u = np.concatenate(U[lo:hi]); lab = np.concatenate(L[lo:hi])
                        tau = np.concatenate([TAU[i]["vp_alarm"] if i < hi - delay else np.full(B, np.inf) for i in range(lo, hi)])
                        th["vp_alarm"] = C.verified_positive_seq(u, tau, lab, alpha, pim)
                        th["local_q"] = np.quantile(np.concatenate(U), 1 - alpha)
                        th["lq_win6"] = np.quantile(np.concatenate(U[-6:]), 1 - alpha)
d = pd.DataFrame(rows); d.to_csv(os.path.join(D, "explore_v6.csv.gz"), index=False)
d["over"] = d.fpr > 0.12
for per, (lo, hi) in dict(m4_6=(4, 6), m7_9_after_drift=(7, 9), m10_12=(10, 12), m13_18=(13, 18)).items():
    q = d[d.month.between(lo, hi)]
    print(f"\n=== {per} ===\n", q.groupby(["scen", "pi", "method"]).agg(fpr=("fpr", "mean"), p_over=("over", "mean"),
          sens=("sens", "mean")).round(3).unstack("method").to_string())
