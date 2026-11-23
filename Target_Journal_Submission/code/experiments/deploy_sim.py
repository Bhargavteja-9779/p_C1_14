"""Deployment simulation of operating-point transfer (protocol v2, RECHECK/stage5/protocol_v2_preregistered.md).

usage: python deploy_sim.py --set dev|locked|all --seeds 10 --reps 50 --out results/deploy_<set>.csv.gz
"""
import argparse, os, sys, time, warnings, zlib
import numpy as np, pandas as pd
from joblib import Parallel, delayed
from sklearn.metrics import roc_auc_score
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.data import load, DISEASES, DEV_CRC, LOCKED_CRC
from src.pipeline import Pipeline
from src import thresholds as T

ALPHA = 0.10
PIS = (0.0, 0.10, 0.30)
N_CONF = (10, 20)


def tasks(which):
    """(disease, train cohorts, target cohort) triples."""
    out = []
    if which in ("dev", "all"):
        out += [("CRC", [c for c in DEV_CRC if c != t], t) for t in DEV_CRC]
    if which in ("locked", "all"):
        out += [("CRC", list(DEV_CRC), t) for t in LOCKED_CRC]
        for d in ("IBD", "T2D", "adenoma"):
            st = DISEASES[d]["studies"]; out += [(d, [c for c in st if c != t], t) for t in st]
    return out


_CACHE = {}
def _data(d):
    if d not in _CACHE:
        X, y, g, M = load(d); _CACHE[d] = (X.values.astype(float), y, g, M.index.values)
    return _CACHE[d]


def run_job(disease, train, target, model, mode, seed, reps):
    warnings.filterwarnings("ignore")
    X, y, g, ids = _data(disease)
    tr, te = np.isin(g, train), g == target
    P = Pipeline(model, mode, seed).fit(X[tr], y[tr], g[tr])
    s_src, y_src = P.oof, P.y
    dens = (T._Dens(s_src[y_src == 0]), T._Dens(s_src[y_src == 1]))
    Xt, yt = X[te], y[te]
    st_full = P.score(Xt, pool_idx=np.arange(len(yt)))
    auc = roc_auc_score(yt, st_full)
    rng = np.random.default_rng(10_000 * seed + zlib.crc32(target.encode()) % 10_000)
    i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]
    rows = []
    for r in range(reps):
        p0, p1 = rng.permutation(i0), rng.permutation(i1)
        c0, e0 = p0[: len(p0) // 2], p0[len(p0) // 2:]
        c1, e1 = p1[: len(p1) // 2], p1[len(p1) // 2:]
        for pi in PIS:
            n1 = min(len(c1), int(round(pi * len(c0) / (1 - pi))))
            pool = np.concatenate([c0, c1[:n1]]); pi_act = n1 / len(pool)
            st = P.score(Xt, pool_idx=pool) if mode == "pcz" else st_full
            u = st[pool]
            th = {"M0_source": T.source(s_src, y_src, ALPHA)}
            # label-free alarm: estimated realised FPR of the status-quo threshold, from the unlabeled pool only
            above = float(np.mean(u >= th["M0_source"]))
            sens_src = float(np.mean(s_src[y_src == 1] >= th["M0_source"]))
            alarm_naive = above
            if mode == "global":
                th["M1_local_quantile"] = T.local_quantile(s_src, y_src, ALPHA, u)
                th["M2_em_prior"], pi_em = T.em_prior(s_src, y_src, ALPHA, u, dens=dens, return_pi=True)
                alarm_mix = float(np.clip((above - pi_em * sens_src) / max(1 - pi_em, 1e-6), 0, 1))
                th["M3_known_prev"] = T.known_prev(s_src, y_src, ALPHA, u, pi_act)
                th["M7_pred_alignment"] = T.prediction_alignment(s_src, y_src, ALPHA, u)
                th["M4_site_shift"], par = T.site_shift(s_src, y_src, ALPHA, u, dens=dens, return_params=True)
                for n in N_CONF:
                    if pi == 0.0 and n <= len(c0):  # labelled controls drawn from the pool controls
                        th[f"M5_conformal_n{n}"] = T.conformal_controls(ALPHA, st[c0[:n]])
                th["Oracle"] = float(np.quantile(st[e0], 1 - ALPHA))
            for k, t in th.items():
                rows.append((disease, target, model, mode, seed, r, pi, pi_act, k, t,
                             float((st[e0] >= t).mean()), float((st[e1] >= t).mean()), len(e0), len(e1), auc,
                             pi_em if mode == "global" else np.nan, par["b"] if mode == "global" else np.nan,
                             alarm_naive, alarm_mix if mode == "global" else np.nan, len(pool)))
    return rows


COLS = ["disease", "target", "model", "mode", "seed", "rep", "pi", "pi_actual", "method", "threshold", "fpr", "sens",
        "n0_eval", "n1_eval", "auc", "em_pi_hat", "shift_b",
        "alarm_naive", "alarm_mix", "pool_n"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="dev"); ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--reps", type=int, default=50); ap.add_argument("--out", required=True)
    ap.add_argument("--models", default="lasso,rf"); ap.add_argument("--modes", default="global,pcz")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args(); t0 = time.time()
    jobs = [(d, tr, tg, m, mo, s) for (d, tr, tg) in tasks(a.set) for m in a.models.split(",")
            for mo in a.modes.split(",") for s in range(a.seeds)]
    print(len(jobs), "jobs", flush=True)
    res = Parallel(n_jobs=a.jobs, verbose=5)(delayed(run_job)(*j, a.reps) for j in jobs)
    df = pd.DataFrame([r for rr in res for r in rr], columns=COLS)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True); df.to_csv(a.out, index=False)
    print("done", df.shape, round(time.time() - t0), "s")
