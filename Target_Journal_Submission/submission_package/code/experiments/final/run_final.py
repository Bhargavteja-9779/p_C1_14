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


# ---------------- Part B and C (comorbidity) ----------------
def comorbidity_parts():
    import statsmodels.api as sm
    from src.data import CACHE
    from src.models import preprocess_fit, preprocess_apply, logit
    meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
    X, y, g, M = load("CRC", DEV_CRC); cols = X.columns; idx = np.arange(len(y))
    cohorts = ["JieZ_2017", "QinN_2014"] if DRY else ["MetaCardis_2020_a", "QinJ_2012", "KarlssonFH_2013", "NielsenHB_2014",
                                                      "HallAB_2017", "IjazUZ_2017", "HMP_2019_ibdmdb"]
    rowsB, fits, scored = [], [], {}
    for model in MODELS:
        s_src, y_src, _, m = train_and_score(X.values, y, g, idx, idx[:1], model, seed=SEED)
        p = preprocess_fit(X.values); t = C.source_threshold(s_src, y_src, 0.10)
        for c in cohorts:
            a = pd.read_csv(os.path.join(CACHE, "ra", f"{c}.csv"), index_col=0); a.index = [i.split("|")[-1] for i in a.index]
            a = a.groupby(level=0).sum().T; md = meta.loc[meta.index.intersection(a.index)]
            md = md[(md.study_name == c) & (md.body_site == "stool") & md.age_category.isin(["adult", "senior"])]
            md = md.assign(_d=pd.to_numeric(md.get("days_from_first_collection"), errors="coerce").fillna(0)).sort_values("_d")
            md = md[~md.subject_id.duplicated()]
            sc = logit(m.predict_proba(preprocess_apply(a.loc[md.index].reindex(columns=cols, fill_value=0).fillna(0).values, p))[:, 1])
            md = md.assign(score=sc, pos=sc >= t); scored[(model, c)] = (md, s_src, y_src)
            ctrl = md[md.study_condition == "control"]
            for cond in [k for k in md.study_condition.unique() if k != "control" and (md.study_condition == k).sum() >= 10]:
                grp = md[md.study_condition == cond]
                boot = [grp.pos.sample(frac=1, replace=True, random_state=b).mean() / max(ctrl.pos.sample(frac=1, replace=True, random_state=b).mean(), 1e-9) for b in range(1000)]
                rowsB.append(dict(model=model, cohort=c, condition=cond, n=len(grp), n_ctrl=len(ctrl), pos=grp.pos.mean(),
                                  pos_ctrl=ctrl.pos.mean(), ratio=grp.pos.mean() / max(ctrl.pos.mean(), 1e-9),
                                  ratio_lo=np.percentile(boot, 2.5), ratio_hi=np.percentile(boot, 97.5)))
                d = pd.concat([grp, ctrl])[["score", "study_condition", "age", "BMI", "gender"]].copy()
                d["dis"] = (d.study_condition == cond).astype(float); d["male"] = (d.gender == "male").astype(float)
                covs = [k for k in ["age", "BMI", "male"] if d[k].notna().mean() > 0.8 and d[k].nunique() > 1]
                d = d.dropna(subset=covs)
                for spec, cv in [("crude", []), ("adjusted", covs)]:
                    r = sm.OLS(d.score, sm.add_constant(d[["dis"] + cv].astype(float))).fit()
                    fits.append(dict(model=model, cohort=c, condition=cond, spec=spec, covs="+".join(cv), n=len(d),
                                     beta=r.params["dis"], lo=r.conf_int().loc["dis", 0], hi=r.conf_int().loc["dis", 1],
                                     p_one_sided=r.pvalues["dis"] / 2 if r.params["dis"] > 0 else 1 - r.pvalues["dis"] / 2))
    F = pd.DataFrame(fits)
    adj = F[F.spec == "adjusted"].copy()
    for model in MODELS:   # Holm correction within model
        q = adj[adj.model == model].sort_values("p_one_sided"); k = len(q)
        holm = np.minimum(1, np.maximum.accumulate([(k - i) * pv for i, pv in enumerate(q.p_one_sided)]))
        adj.loc[q.index, "p_holm"] = holm
    pd.DataFrame(rowsB).to_csv(os.path.join(OUT, "partB_positivity.csv"), index=False)
    F.to_csv(os.path.join(OUT, "partB_regression.csv"), index=False); adj.to_csv(os.path.join(OUT, "partB_adjusted_holm.csv"), index=False)
    # Part C
    site = "JieZ_2017" if DRY else "MetaCardis_2020_a"
    shares = {"ACVD": 0.20} if DRY else {"CAD": 0.10, "T2D": 0.15, "HF": 0.03, "IGT": 0.15}
    rng = np.random.default_rng(SEED + 1); rowsC = []; B, TT = 200, 18
    for model in MODELS:
        md, s_src, y_src = scored[(model, site)]; case_sc = s_src[y_src == 1]
        pops = {"control": md[md.study_condition == "control"].score.values}
        pops.update({k: md[md.study_condition == k].score.values for k in shares})
        names = list(pops); w = np.array([1 - sum(shares.values())] + [shares[k] for k in shares])
        for r in range(R):
            pooled = C.SequentialRecalibrator(s_src, y_src, 0.10, 0.05)
            grp = {k: C.SequentialRecalibrator(s_src, y_src, 0.10, 0.05) for k in names}; t_src = C.source_threshold(s_src, y_src, 0.10)
            for month in range(1, TT + 1):
                for meth in ["source", "pooled", "group"]:
                    for k in names:
                        t = t_src if meth == "source" else pooled.t if meth == "pooled" else grp[k].t
                        rowsC.append(dict(model=model, rep=r, month=month, method=meth, group=k, share=w[names.index(k)],
                                          fpr=(pops[k] >= t).mean(), sens_proxy=(case_sc >= t).mean()))
                gi = rng.choice(len(names), B, p=w); yc = rng.random(B) < 0.01
                u = np.array([rng.choice(case_sc) if yc[i] else rng.choice(pops[names[gi[i]]]) for i in range(B)])
                pooled.update(u, yc.astype(int))
                for j, k in enumerate(names):
                    sel = gi == j
                    if sel.any(): grp[k].update(u[sel], yc[sel].astype(int))
    pd.DataFrame(rowsC).to_csv(os.path.join(OUT, "partC_groupcal.csv.gz"), index=False)

if __name__ == "__main__":
    comorbidity_parts(); print("parts B/C done")
