"""FINAL locked-cohort analysis (protocol.md). Refuses to run unless protocol.md contains 'FROZEN: yes'.
Usage: python3 run_final.py            -> locked analysis, writes experiments/final/results/
       python3 run_final.py --dryrun   -> same pipeline on DEV CRC cohorts only (code check; no locked data)"""
import sys, os, re, json, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", ".."))
from src.data import load, DISEASES, DEV_CRC, LOCKED_CRC
from src.models import train_and_score
from src import calibrate as C

DRY = "--dryrun" in sys.argv
if not DRY and not re.search(r"^FROZEN: yes\s*$", open(os.path.join(HERE, "..", "protocol.md")).read(), re.M):
    sys.exit("protocol.md is not frozen - refusing to touch locked cohorts")
OUT = os.path.join(HERE, "dryrun" if DRY else "results"); os.makedirs(OUT, exist_ok=True)
SEED = 2026; R = 20 if DRY else 200; T = 12; MODELS = ["lasso", "rf"]

def site_scores():
    """Return list of (disease, site, model, s_src, y_src, s_tgt, y_tgt). Cached."""
    f = os.path.join(OUT, "scores.npz")
    if os.path.exists(f):
        Z = np.load(f, allow_pickle=True); return list(Z["items"])
    items = []
    if DRY:
        tasks = [("CRC", DEV_CRC[:6], DEV_CRC[6:])]
    else:
        tasks = [("CRC", DEV_CRC, LOCKED_CRC)] + [(d, None, None) for d in ["IBD", "T2D", "adenoma"]]
    for disease, train, test in tasks:
        studies = (train + test) if train else DISEASES[disease]["studies"]
        X, y, g, M = load(disease, studies); X = X.values
        sites = test if train else studies
        for site in sites:
            te = g == site; tr = np.isin(g, train) if train else ~te
            for model in MODELS:
                s_src, y_src, st, _ = train_and_score(X, y, g, tr, te, model, seed=SEED)
                items.append((disease, site, model, s_src, y_src, st, y[te])); print(disease, site, model, flush=True)
    np.savez(f, items=np.array(items, dtype=object)); return items

def simulate(s_src, y_src, P0, P1, pi, rng, alpha=0.10, pim=None, B=100, delay=0, burn=2, smooth=False,
             adh=1.0, miss=0.0, drift=0.0, months=None):
    """One deployment stream. smooth: KDE-smoothed site population; adh: colonoscopy attendance; miss: share of
    cancers missed at colonoscopy (observed as control); drift: logit shift of all scores from month 7."""
    T_ = months or T; pim = max(0.05, pi) if pim is None else pim
    bw = lambda P: 1.06 * P.std() * len(P) ** -0.2
    draw = lambda P, n: rng.choice(P, n) + (rng.normal(0, bw(P), n) if smooth else 0)
    Q0, Q1 = (draw(P0, 20000), draw(P1, 20000)) if smooth else (P0, P1)
    t_src = C.source_threshold(s_src, y_src, alpha)
    rec = C.SequentialRecalibrator(s_src, y_src, alpha, pim, burn=burn, delay=delay)
    th = dict(source=t_src, local_q=t_src, contam=t_src, oracle=np.quantile(Q0, 1 - alpha), vp=rec.t)
    U, out = [], []
    for month in range(1, T_ + 1):
        sh = drift if month > 6 else 0.0
        if sh: th["oracle"] = np.quantile(Q0 + sh, 1 - alpha)
        y_new = (rng.random(B) < pi).astype(int); u_new = np.where(y_new == 1, draw(P1, B), draw(P0, B)) + sh
        for k, t in th.items():
            out.append(dict(month=month, method=k, fpr=((Q0 + sh) >= t).mean(), sens=((Q1 + sh) >= t).mean(),
                            refer=(u_new >= t).mean()))
        lab_obs = np.where((y_new == 1) & (rng.random(B) < miss), 0, y_new)
        th["vp"] = rec.update(u_new, lab_obs, rng.random(B) < adh)
        U.extend(u_new); u = np.array(U)
        th["local_q"] = np.quantile(u, 1 - alpha); th["contam"] = C.contam_quantile(u, alpha, pim)
    return out

def oneshot(s_src, y_src, st, yt, rng, alpha=0.10, reps=None):
    reps = reps or R; i0, i1 = np.where(yt == 0)[0], np.where(yt == 1)[0]; out = []
    for r in range(reps):
        p0, p1 = rng.permutation(i0), rng.permutation(i1); h = len(p0) // 2; pool0, e0 = p0[:h], p0[h:]
        h1 = len(p1) // 2; pc, e1 = p1[:h1], p1[h1:]
        for pi in [0.0, 0.05, 0.10]:
            n1 = min(rng.binomial(h, pi / (1 - pi)) if pi > 0 else 0, h1); idx = np.concatenate([pool0, pc[:n1]])
            u, lab = st[idx], yt[idx]; pim = max(0.05, pi)
            th = dict(source=C.source_threshold(s_src, y_src, alpha), local_q=np.quantile(u, 1 - alpha),
                      em=C.em_label_shift(s_src, y_src, alpha, u=u), contam=C.contam_quantile(u, alpha, pim),
                      conf20=C.local_controls_conformal(alpha, st[pool0[:20]]) if h >= 20 else np.nan,
                      vp=C.verified_positive(u, lab, alpha, pim, C.contam_quantile(u, 2 * alpha, pim))[0])
            for k, t in th.items():
                out.append(dict(rep=r, pi=pi, method=k, fpr=(st[e0] >= t).mean(), sens=(st[e1] >= t).mean()))
    return out

if __name__ == "__main__":
    items = site_scores(); rng = np.random.default_rng(SEED)
    SETTINGS = [("primary", {})] + [(f"alpha{a}", dict(alpha=a)) for a in (0.05, 0.20)] + \
               [("pimax_miss", dict(pim=0.05)), ("delay1", dict(delay=1)), ("B50", dict(B=50)), ("B200", dict(B=200)),
                ("burn3", dict(burn=3)), ("smooth", dict(smooth=True)), ("adherence70", dict(adh=0.7)),
                ("miss5", dict(miss=0.05)), ("drift", dict(drift=0.5, months=18)),
                ("combined", dict(smooth=True, adh=0.7, miss=0.05, delay=1, drift=0.5, months=18))]
    rows, rows1 = [], []
    for disease, site, model, s_src, y_src, st, yt in items:
        P0, P1 = st[yt == 0], st[yt == 1]
        pis = [0.10, 0.30] if disease == "adenoma" else [0.01, 0.05, 0.10]
        for name, kw in SETTINGS:
            for pi in (pis if name != "pimax_miss" else [0.10]):
                for r in range(R):
                    for o in simulate(s_src, y_src, P0, P1, pi, rng, **kw):
                        rows.append(dict(setting=name, disease=disease, site=site, model=model, pi=pi, rep=r,
                                         alpha=kw.get("alpha", 0.10), **o))
        for o in oneshot(s_src, y_src, st, yt, rng):
            rows1.append(dict(disease=disease, site=site, model=model, **o))
        print("done", disease, site, model, flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "sequential.csv.gz"), index=False)
    pd.DataFrame(rows1).to_csv(os.path.join(OUT, "oneshot.csv.gz"), index=False)
    json.dump(dict(seed=SEED, R=R, T=T, dry=DRY), open(os.path.join(OUT, "run_info.json"), "w"))
