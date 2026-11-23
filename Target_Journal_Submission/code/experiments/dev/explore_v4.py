"""DEV ONLY. Round 4 of D6: robustness of the candidate (hyb_sc_k) on the semi-synthetic known-truth benchmark built
from the 8 dev cohorts: target FPR alpha in {0.05, 0.10, 0.20}; third classifier (hist. gradient boosting);
misspecified prevalence prior (prior mean 0.001 / 0.01 / 0.05 / 0.20 vs pool prevalence 0 / 0.01 / 0.05 / 0.20)."""
import sys, os, numpy as np, pandas as pd, warnings
from joblib import Parallel, delayed
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..")); sys.path.insert(0, HERE)
from src.data import load, DEV_CRC
from src import calibrate as C
from explore_v2 import scores
from explore_v3 import KDETruth
R, KS, PIS, N_POOL = 30, (5, 10, 20), (0.0, 0.01, 0.05, 0.2), 60
CONFIGS = [(0.05, 0.01), (0.10, 0.01), (0.20, 0.01), (0.10, 0.001), (0.10, 0.05), (0.10, 0.20)]  # (alpha, prior mean)

def run(model, s, d, g_src, seed):
    rng = np.random.default_rng(seed); s_src, y_src, st, yt = d["s_src"], d["y_src"], d["st"], d["yt"]
    T = C.PredTransport(s_src, y_src, seed=seed); K0, K1 = KDETruth(st[yt == 0]), KDETruth(st[yt == 1])
    cal = {}
    for al, pm in CONFIGS:
        for k in (0,) + KS: cal[al, pm, k] = C.self_calibrate(s_src, y_src, g_src, al, k=k, prior=(pm, 10), seed=seed)
    rows = []
    for r in range(R):
        for pi in PIS:
            n1 = int(round(pi * N_POOL / (1 - pi))); u = np.concatenate([K0.sample(N_POOL, rng), K1.sample(n1, rng)])
            cs = {k: K0.sample(k, rng) for k in KS}
            for al, pm in CONFIGS:
                th = {}
                if pm == 0.01:
                    th.update(source=C.source_threshold(s_src, y_src, al), local_q=C.local_quantile(s_src, y_src, al, u=u))
                    for k in KS: th[f"conf_{k}"] = C.local_controls_conformal(al, cs[k])
                th["lf_sc"] = T.predictive(cal[al, pm, 0], u=u, prior=(pm, 10))[0]
                for k in KS: th[f"hyb_sc_{k}"] = T.predictive(cal[al, pm, k], c=cs[k], u=u, prior=(pm, 10))[0]
                for m, t in th.items():
                    rows.append(dict(model=model, cohort=s, rep=r, pi=pi, alpha=al, prior=pm, method=m, fpr=K0.sf(t), sens=K1.sf(t)))
    print(model, s, "done", flush=True); return rows

if __name__ == "__main__":
    X, y, g, M = load("CRC", DEV_CRC); Xv = X.values; jobs = []
    for m in ("lasso", "rf", "hgb"):
        for s in DEV_CRC:
            d = scores(m, s, Xv, y, g); jobs.append((m, s, d, g[g != s]))
    out = Parallel(n_jobs=4)(delayed(run)(m, s, d, gs, 300 + i) for i, (m, s, d, gs) in enumerate(jobs))
    pd.DataFrame([r for o in out for r in o]).to_csv(os.path.join(HERE, "explore_v4.csv.gz"), index=False)
