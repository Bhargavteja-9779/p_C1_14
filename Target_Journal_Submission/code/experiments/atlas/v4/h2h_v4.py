"""Head-to-head on LOCKED healthy populations: burn-in (random design) vs control augmentation (Wirbel 2021), de-duplicated.
Unit = disease x model x population; inference by population (cluster bootstrap, Wilcoxon on population means)."""
import os, json, numpy as np, pandas as pd
from scipy import stats
from common_v4 import *
A = 0.10; rng = np.random.default_rng(11); dev, lock = split()
u = pd.read_csv(os.path.join(OUT, "deploy_v4_units.csv")); u = u[(u.design == "random") & u.pop_eval.isin(lock)]
ca = pd.read_csv(os.path.join(OUT, "control_augmentation_v4.csv")); ca["err"] = (ca.fpr - A).abs()
aug = ca[ca.aug].rename(columns={"pop": "pop_eval", "err": "aug_err", "fpr": "aug_fpr"})[["disease", "model", "pop_eval", "aug_err", "aug_fpr", "n"]]
noaug = ca[~ca.aug].rename(columns={"pop": "pop_eval", "err": "src_err"})[["disease", "model", "pop_eval", "src_err"]]
out = {}
hh = aug.merge(noaug, on=["disease", "model", "pop_eval"])
out["aug_vs_noaug_all_locked"] = dict(units=len(hh), pops=hh.pop_eval.nunique(), aug_mad=hh.aug_err.mean(), src_mad=hh.src_err.mean(),
                                      wilcoxon_pop_p=float(stats.wilcoxon(hh.groupby("pop_eval").apply(lambda d: (d.aug_err - d.src_err).mean())).pvalue))
for N in [50, 100]:
    b = u[(u.N == N) & (u.method == "BURN")][["disease", "model", "pop_eval", "mad"]]
    h = b.merge(hh, on=["disease", "model", "pop_eval"]); h["diff"] = h["mad"] - h.aug_err
    pp = h.groupby("pop_eval")["diff"].mean(); k = len(pp); g = h.groupby("pop_eval")["diff"].agg(["sum", "size"])
    bs = [g["sum"].values[i].sum() / g["size"].values[i].sum() for i in (rng.integers(0, k, k) for _ in range(2000))]
    out[f"burn_vs_aug_N{N}"] = dict(units=len(h), pops=k, burn_mad=h["mad"].mean(), aug_mad=h.aug_err.mean(), diff=h["diff"].mean(),
                                    lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)), units_burn_better=int((h["diff"] < 0).sum()),
                                    pops_burn_better=int((pp < 0).sum()), wilcoxon_pop_p=float(stats.wilcoxon(pp).pvalue) if k > 5 else None)
json.dump(out, open(os.path.join(OUT, "h2h_v4.json"), "w"), indent=1, default=float)
for k_, v in out.items(): print(k_, {a: round(b, 4) if isinstance(b, float) else b for a, b in v.items()})
print(ca.groupby(["disease", "model", "aug"]).agg(pops=("pop", "size"), mad=("err", "mean"), mx=("fpr", "max")).round(3).to_string())
