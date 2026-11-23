"""DEV ONLY (8 development CRC cohorts). Round 2 of D6: hybrid (few labelled local controls + unlabelled pool) vs
baselines incl. STEP-3 additions (UPA alignment, free 2-component GMM). Scores cached in dev/scores_*.npz."""
import sys, os, numpy as np, pandas as pd, warnings
from joblib import Parallel, delayed
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from src.data import load, DEV_CRC
from src.models import train_and_score
from src import calibrate as C
ALPHA, R, KS, PIS, PRIOR = 0.10, 50, (5, 10, 20), (0.0, 0.05, 0.2, "nat"), (0.01, 10)

def scores(model, s, X, y, g):
    f = os.path.join(HERE, f"scores_{model}_{s}.npz")
    if not os.path.exists(f):
        te = g == s; s_src, y_src, st, _ = train_and_score(X, y, g, ~te, te, model)
        np.savez(f, s_src=s_src, y_src=y_src, st=st, yt=y[te])
    return dict(np.load(f))

def run(model, s, d, seed):
    rng = np.random.default_rng(seed); s_src, y_src, st, yt = d["s_src"], d["y_src"], d["st"], d["yt"]
    T = C.PredTransport(s_src, y_src, seed=seed); i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]; rows = []
    for r in range(R):
        p0, p1 = rng.permutation(i0), rng.permutation(i1)
        c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]; c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
        for pi in PIS:
            ev = lambda t: dict(fpr=(st[e0] >= t).mean(), sens=(st[e1] >= t).mean())
            base = dict(model=model, cohort=s, rep=r, pi=str(pi))
            for k in KS:
                lab = c0[:k]; pc = c0[k:]
                if len(pc) < 8: continue
                n1 = len(c1) if pi == "nat" else int(round(pi * len(pc) / (1 - pi))); n1 = min(n1, len(c1))
                u = st[np.concatenate([pc, c1[:n1]])]; c = st[lab]
                th = {}
                if k == KS[0]:  # label-free methods depend on the pool only; evaluate once per pool (pool for k=5)
                    th.update(source=C.source_threshold(s_src, y_src, ALPHA), local_q=C.local_quantile(s_src, y_src, ALPHA, u=u),
                              em=C.em_label_shift(s_src, y_src, ALPHA, u=u), upa=C.upa_align(s_src, y_src, ALPHA, u=u),
                              gmm2=C.gmm2(s_src, y_src, ALPHA, u=u), shift_v1=T.site_shift(ALPHA, u)[0],
                              lf_prior=T.predictive(ALPHA, u=u, prior=PRIOR)[0])
                th[f"conf_{k}"] = C.local_controls_conformal(ALPHA, c)
                th[f"ctrlq_{k}"] = C.local_controls_quantile(ALPHA, c)
                th[f"pctrl_{k}"] = T.predictive(ALPHA, c=c)[0]
                th[f"hyb_free_{k}"] = T.predictive(ALPHA, c=c, u=u)[0]
                th[f"hyb_prior_{k}"] = T.predictive(ALPHA, c=c, u=u, prior=PRIOR)[0]
                for m, t in th.items(): rows.append(dict(base, method=m, k=k, **ev(t)))
    print(model, s, "done", flush=True)
    return rows

if __name__ == "__main__":
    X, y, g, M = load("CRC", DEV_CRC); X = X.values
    jobs = [(m, s, scores(m, s, X, y, g)) for m in ("lasso", "rf") for s in DEV_CRC]
    out = Parallel(n_jobs=4)(delayed(run)(m, s, d, 100 + i) for i, (m, s, d) in enumerate(jobs))
    D = pd.DataFrame([r for o in out for r in o]); D.to_csv(os.path.join(HERE, "explore_v2.csv"), index=False)
    D["ae"] = (D.fpr - ALPHA).abs(); D["viol"] = D.fpr > ALPHA + 0.05
    print(D.groupby(["pi", "method"])[["fpr", "ae", "viol", "sens"]].mean().round(3).to_string())
