"""DEV ONLY. Round 4 of D6 log: guaranteed thresholds.
(A) within-cohort: unlabelled pool (case share pi) -> robust_pool (P(FPR>a)<=delta for pi<=pi_max), robust_pool_mean,
    vs conformal/tolerance from labelled controls, local quantile, source.
(B) cross-study stress test (exchangeability violated): pool from cohort A, evaluate on cohort B of the SAME country
    (ThomasAM_2018a<->ThomasAM_2018b, Italy; ZellerG_2014<->WirbelJ_2018, Germany/France) and of different countries.
Usage: python explore_v4.py <model> [R]"""
import sys, os, numpy as np, pandas as pd, warnings, itertools
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, DEV_CRC
from src.models import train_and_score
from src import calibrate as C
model = sys.argv[1]; R = int(sys.argv[2]) if len(sys.argv) > 2 else 100
alpha, delta = 0.10, 0.10; rng = np.random.default_rng(4)
X, y, g, M = load("CRC", DEV_CRC); X = X.values
rows = []
for s in DEV_CRC:
    te = g == s; tr = ~te
    s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model)
    yt = y[te]; i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
    for r in range(R):
        p0, p1 = rng.permutation(i0), rng.permutation(i1)
        c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
        for pi in [0.0, 0.05, 0.2]:
            n1 = int(round(pi * len(c0) / (1 - pi))); u = st[np.concatenate([c0, c1[:n1]])]
            ths = dict(source=C.source_threshold(s_src, y_src, alpha), local_q=C.local_quantile(s_src, y_src, alpha, u=u),
                       rpool05=C.robust_pool(s_src, y_src, alpha, u=u, delta=delta, pi_max=0.05),
                       rpool20=C.robust_pool(s_src, y_src, alpha, u=u, delta=delta, pi_max=0.20),
                       rpoolmean05=C.robust_pool_mean(s_src, y_src, alpha, u=u, pi_max=0.05),
                       ctrl10=C.local_controls_conformal(alpha, st[c0[:10]]),
                       tol_ctrl_all=C.controls_tolerance(alpha, st[c0], delta))
            for k, t in ths.items():
                rows.append(dict(part="A", model=model, cohort=s, rep=r, pi=str(pi), method=k, n_pool=len(u),
                                 fpr=(st[e0] >= t).mean(), sens=(st[e1] >= t).mean(), abstain=np.isinf(t)))
    print(model, s, "A done", flush=True)
# (B) cross-study: train on the 6 other dev cohorts, pool = all controls of A (+ cases at share pi), evaluate on B
pairs = [("ThomasAM_2018a", "ThomasAM_2018b"), ("ZellerG_2014", "WirbelJ_2018"), ("FengQ_2015", "WirbelJ_2018"),
         ("VogtmannE_2016", "HanniganGD_2017"), ("GuptaA_2019", "ZellerG_2014")]
for a, b in pairs:
    for A_, B_ in [(a, b), (b, a)]:
        te = (g == A_) | (g == B_); tr = ~te
        s_src, y_src, st_all, _ = train_and_score(X, y, g, tr, te, model)
        ga, yy = g[te], y[te]; sa0 = st_all[(ga == A_) & (yy == 0)]; sa1 = st_all[(ga == A_) & (yy == 1)]
        sb0 = st_all[(ga == B_) & (yy == 0)]; sb1 = st_all[(ga == B_) & (yy == 1)]
        for r in range(R):
            for pi in [0.0, 0.05]:
                n1 = int(round(pi * len(sa0) / (1 - pi))); u = np.concatenate([sa0, rng.choice(sa1, n1, replace=False)])
                ths = dict(source=C.source_threshold(s_src, y_src, alpha), local_q=C.local_quantile(s_src, y_src, alpha, u=u),
                           rpool05=C.robust_pool(s_src, y_src, alpha, u=u, delta=delta, pi_max=0.05))
                for k, t in ths.items():
                    rows.append(dict(part="B", model=model, cohort=f"{A_}->{B_}", rep=r, pi=str(pi), method=k, n_pool=len(u),
                                     fpr=(sb0 >= t).mean(), sens=(sb1 >= t).mean(), abstain=np.isinf(t)))
                if pi == 0.0: break  # pool fixed when pi=0 -> one replicate is enough
    print(model, a, b, "B done", flush=True)
d = pd.DataFrame(rows); d.to_csv(os.path.join(os.path.dirname(__file__), f"explore_v4_{model}.csv"), index=False)
d["viol"] = d.fpr > alpha; d["abs_err"] = (d.fpr - alpha).abs()
A = d[d.part == "A"]
print(A.groupby(["pi", "method"])[["fpr", "viol", "abs_err", "sens", "abstain"]].mean().round(3).to_string())
print("NOTE: viol on the evaluation half includes eval sampling noise; the guarantee is on the population FPR.")
B = d[d.part == "B"].drop_duplicates(["cohort", "pi", "method", "rep"])
print(B.groupby(["cohort", "pi", "method"])[["fpr", "sens"]].mean().round(3).unstack("method").to_string())
