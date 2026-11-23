"""DEV ONLY (8 development CRC cohorts). Round 3 of D6.
(A) real splits as in round 2; (B) semi-synthetic benchmark with KNOWN truth: each held-out cohort's real control and
case score distributions (Gaussian KDE of all its samples) are the ground truth; labelled controls and pools are
drawn from them and FPR/sensitivity are computed exactly. New methods: self-calibrated hybrid (hyb_sc_k), self-
calibrated label-free (lf_sc), GoF-gated hybrid with conformal fallback (hyb_gof_k)."""
import sys, os, numpy as np, pandas as pd, warnings
from scipy import stats
from joblib import Parallel, delayed
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from src.data import load, DEV_CRC
from src import calibrate as C
ALPHA, PRIOR, PIS = 0.10, (0.01, 10), (0.0, 0.05, 0.2, "nat")
R_REAL, R_SYN, K_REAL, K_SYN, N_POOL = 50, 100, (5, 10, 20), (5, 10, 20, 40), 60

class KDETruth:
    def __init__(self, x):
        self.x = x; self.h = stats.gaussian_kde(x).factor * x.std(ddof=1)
    def sample(self, n, rng): return rng.choice(self.x, n) + self.h * rng.standard_normal(n)
    def sf(self, t): return stats.norm.sf((t - self.x) / self.h).mean()

def thresholds(T, s_src, y_src, c, u, a_sc, a_lf, k):
    th = {}
    if c is None:
        t, _ = T.predictive(np.array([ALPHA, a_lf]), u=u, prior=PRIOR)
        th.update(source=C.source_threshold(s_src, y_src, ALPHA), local_q=C.local_quantile(s_src, y_src, ALPHA, u=u),
                  lf_prior=t[0], lf_sc=t[1])
        return th
    t, _ = T.predictive(np.array([ALPHA, a_sc[k]]), c=c, u=u, prior=PRIOR)
    conf = C.local_controls_conformal(ALPHA, c); p = T.gof_pvalue(c)
    th.update({f"conf_{k}": conf, f"hyb_prior_{k}": t[0], f"hyb_sc_{k}": t[1],
               f"hyb_gof_{k}": t[1] if p >= 0.05 else conf, f"_gofflag_{k}": float(p < 0.05)})
    return th

def run(model, s, d, g_src, seed):
    rng = np.random.default_rng(seed); s_src, y_src, st, yt = d["s_src"], d["y_src"], d["st"], d["yt"]
    T = C.PredTransport(s_src, y_src, seed=seed)
    a_sc = {k: C.self_calibrate(s_src, y_src, g_src, ALPHA, k=k, prior=PRIOR, seed=seed) for k in sorted(set(K_REAL + K_SYN))}
    a_lf = C.self_calibrate(s_src, y_src, g_src, ALPHA, k=0, prior=PRIOR, seed=seed)
    rows = []; info = dict(model=model, cohort=s, a_lf=a_lf, **{f"a_sc_{k}": v for k, v in a_sc.items()})
    # (A) real splits
    i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
    for r in range(R_REAL):
        p0, p1 = rng.permutation(i0), rng.permutation(i1)
        c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
        for pi in PIS:
            for k in K_REAL:
                pc = c0[k:]
                if len(pc) < 8: continue
                n1 = min(len(c1) if pi == "nat" else int(round(pi * len(pc) / (1 - pi))), len(c1))
                u = st[np.concatenate([pc, c1[:n1]])]
                th = thresholds(T, s_src, y_src, st[c0[:k]], u, a_sc, a_lf, k)
                if k == K_REAL[0]: th.update(thresholds(T, s_src, y_src, None, u, a_sc, a_lf, k))
                for m, t in th.items():
                    rows.append(dict(bench="real", model=model, cohort=s, rep=r, pi=str(pi), k=k, method=m,
                                     fpr=t if m.startswith("_") else (st[e0] >= t).mean(), sens=np.nan if m.startswith("_") else (st[e1] >= t).mean()))
    # (B) semi-synthetic with known truth
    K0, K1 = KDETruth(st[yt == 0]), KDETruth(st[yt == 1]); nat = (yt == 1).mean()
    for r in range(R_SYN):
        for pi in PIS:
            pv = nat if pi == "nat" else pi; n1 = int(round(pv * N_POOL / (1 - pv)))
            u = np.concatenate([K0.sample(N_POOL, rng), K1.sample(n1, rng)])
            th = thresholds(T, s_src, y_src, None, u, a_sc, a_lf, 0)
            for k in K_SYN: th.update(thresholds(T, s_src, y_src, K0.sample(k, rng), u, a_sc, a_lf, k))
            for m, t in th.items():
                rows.append(dict(bench="syn", model=model, cohort=s, rep=r, pi=str(pi), k=0, method=m,
                                 fpr=t if m.startswith("_") else K0.sf(t), sens=np.nan if m.startswith("_") else K1.sf(t)))
    print(model, s, "done", {k: round(v, 3) for k, v in info.items() if k.startswith("a_")}, flush=True)
    return rows, info

if __name__ == "__main__":
    X, y, g, M = load("CRC", DEV_CRC)
    jobs = []
    for m in ("lasso", "rf"):
        for s in DEV_CRC:
            d = dict(np.load(os.path.join(HERE, f"scores_{m}_{s}.npz"))); gs = g[g != s]; assert (d["y_src"] == y[g != s]).all()
            jobs.append((m, s, d, gs))
    out = Parallel(n_jobs=4)(delayed(run)(m, s, d, gs, 200 + i) for i, (m, s, d, gs) in enumerate(jobs))
    pd.DataFrame([r for o in out for r in o[0]]).to_csv(os.path.join(HERE, "explore_v3.csv.gz"), index=False)
    pd.DataFrame([o[1] for o in out]).to_csv(os.path.join(HERE, "explore_v3_selfcal.csv"), index=False)
