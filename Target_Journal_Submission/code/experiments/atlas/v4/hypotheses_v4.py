"""Pre-specified atlas hypotheses A1, A2, A3, A5 (protocol_atlas.md) re-tested on de-duplicated data, full and strict sets.
A5 as specified: local labelled controls n=100 (conformal) in band in >=90% of cohorts; country-matched external reference
(pooled scores of the other cohorts of the same country) not."""
import os, numpy as np, pandas as pd
from scipy import stats
from common_v4 import *
A = 0.10; rng = np.random.default_rng(20261124)
r = pd.read_csv(os.path.join(OUT, "atlas_rows_v4.csv.gz")); H = r[~r.study.str.startswith("TRAIN")]
ctry = META.groupby("study_name").country.agg(lambda x: x.mode().iloc[0]); nw = META.groupby("study_name").non_westernized.agg(lambda x: (x == "yes").mean() > .5)
def sub(strict):
    if not strict: return H
    h = H[(H.strict_person == True) & ~H.study.isin(STRICT_DROP_STUDIES)]; return h[h.groupby(["disease", "model", "study"]).study.transform("size") >= MIN_N]
out = []
for strict in [True, False]:
    h = sub(strict); f = h.groupby(["disease", "model", "study"]).flag.agg(["mean", "size", "sum"]).reset_index()
    for m in ["lasso", "rf"]:
        F = f[f.model == m].pivot(index="study", columns="disease", values="mean")
        # A1 chi-square vs binomial(0.10) for CRC (as specified)
        c = f[(f.model == m) & (f.disease == "CRC")]; chi = (((c["sum"] - c["size"] * A) ** 2) / (c["size"] * A * (1 - A))).sum()
        out.append(dict(strict=strict, model=m, test="A1_CRC_chi2", value=chi, p=stats.chi2.sf(chi, len(c)), n=len(c)))
        for other in ["IBD", "T2D"]:   # A2
            x = F[["CRC", other]].dropna(); rho = stats.spearmanr(x.CRC, x[other])[0]
            bs = [stats.spearmanr(*x.iloc[rng.integers(0, len(x), len(x))].T.values)[0] for _ in range(2000)]
            out.append(dict(strict=strict, model=m, test=f"A2_rho_CRC_{other}", value=rho, lo=np.nanpercentile(bs, 2.5), hi=np.nanpercentile(bs, 97.5), n=len(x)))
        for dz in ["CRC", "IBD", "T2D"]:  # A3 (specified for CRC; IBD/T2D post hoc)
            c = f[(f.model == m) & (f.disease == dz)].assign(nw=lambda d: d.study.map(nw)); a, b = c[c.nw]["mean"], c[~c.nw]["mean"]
            out.append(dict(strict=strict, model=m, test=f"A3_{dz}_nonwest_minus_west" + ("" if dz == "CRC" else "_posthoc"), value=a.median() - b.median(),
                            p=stats.mannwhitneyu(a, b, alternative="greater").pvalue, n=f"{len(a)} vs {len(b)}"))
        # A5
        for dz in ["CRC", "IBD", "T2D"]:
            g = h[(h.model == m) & (h.disease == dz)]; S = {s: x.score.values for s, x in g.groupby("study")}
            inb_loc, inb_ctry, n_ctry = [], [], 0
            for s, x in S.items():
                if len(x) >= 120:
                    fp = []
                    for _ in range(200):
                        p = rng.permutation(len(x)); t = np.sort(x[p[:100]])[int(np.ceil(101 * .9)) - 1]; fp.append(np.mean(x[p[100:]] >= t))
                    inb_loc.append(.05 <= np.mean(fp) <= .15)
                same = [o for o in S if o != s and ctry[o] == ctry[s]]
                if same:
                    t = np.quantile(np.concatenate([S[o] for o in same]), 1 - A); v = np.mean(x >= t); inb_ctry.append(.05 <= v <= .15); n_ctry += 1
            out.append(dict(strict=strict, model=m, test=f"A5_{dz}_local100_inband_share", value=np.mean(inb_loc), n=len(inb_loc)))
            out.append(dict(strict=strict, model=m, test=f"A5_{dz}_country_ref_inband_share", value=np.mean(inb_ctry) if inb_ctry else np.nan, n=n_ctry))
o = pd.DataFrame(out); o.to_csv(os.path.join(OUT, "hypotheses_v4.csv"), index=False); pd.set_option("display.width", 200); print(o.round(4).to_string())
