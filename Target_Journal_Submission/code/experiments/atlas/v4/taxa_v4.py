"""P8: LASSO taxon decomposition of population score shifts (strict set). shift_s = sum_j w_j (mean z_j in s - mean z_j in training controls)."""
import os, numpy as np, pandas as pd
from common_v4 import *
from src.pipeline import _log
ORAL = ["Porphyromonas", "Peptostreptococcus", "Parvimonas", "Fusobacterium", "Dialister", "Gemella", "Streptococcus", "Veillonella",
        "Actinomyces", "Rothia", "Haemophilus", "Solobacterium", "Filifactor", "Eikenella", "Neisseria", "Atopobium", "Selenomonas",
        "Leptotrichia", "Capnocytophaga", "Granulicatella", "Aggregatibacter", "Lachnoanaerobaculum", "Oribacterium", "Mogibacterium"]
co = pd.read_csv(os.path.join(OUT, "atlas_coefs_v4.csv")); per = pd.read_csv(os.path.join(OUT, "atlas_perpop_v4.csv"))
out, top = [], []
for d in ["CRC", "IBD", "T2D"]:
    c = co[co.disease == d].reset_index(drop=True); X, y, g, M = load(d)
    Xk = X.reindex(columns=c.taxon, fill_value=0).fillna(0).values; z0 = ((np.log10(Xk[y == 0] / 100 + 1e-5) - c.mu.values) / c.sd.values).mean(0)
    oral = c.taxon.str.replace(r"^[a-z]__\[?", "", regex=True).str.split(r"[_\]]").str[0].isin(ORAL).values
    pp = per[(per.disease == d) & (per.model == "lasso") & per.strict].sort_values("fpr", ascending=False)
    for s in pp.study:
        Xc, md = controls(s); Xc = Xc[md.strict_person.values]
        z = ((np.log10(Xc.reindex(columns=c.taxon, fill_value=0).fillna(0).values / 100 + 1e-5) - c.mu.values) / c.sd.values).mean(0)
        contrib = c.w.values * (z - z0); tot = contrib.sum()
        out.append(dict(disease=d, study=s, fpr=pp.set_index("study").fpr[s], shift=tot, pos_shift=contrib[contrib > 0].sum(),
                        oral_contrib=contrib[oral].sum(), oral_share_of_positive=contrib[oral & (contrib > 0)].sum() / max(contrib[contrib > 0].sum(), 1e-9)))
        if s in list(pp.study[:3]):
            o = np.argsort(-contrib)[:8]
            top += [dict(disease=d, study=s, rank=i + 1, taxon=c.taxon[j], w=c.w[j], dz=(z - z0)[j], contrib=contrib[j], oral=oral[j]) for i, j in enumerate(o)]
o = pd.DataFrame(out); o.to_csv(os.path.join(OUT, "taxa_shift_v4.csv"), index=False); pd.DataFrame(top).to_csv(os.path.join(OUT, "taxa_top_v4.csv"), index=False)
from scipy.stats import spearmanr
for d, gg in o.groupby("disease"): print(d, "rho(shift, FPR)=%.2f" % spearmanr(gg["shift"], gg.fpr)[0], "rho(oral, FPR)=%.2f" % spearmanr(gg.oral_contrib, gg.fpr)[0])
pd.set_option("display.width", 200); print(pd.DataFrame(top).round(3).to_string())
