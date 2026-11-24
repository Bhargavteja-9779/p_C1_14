"""POST HOC P8: why do some CRC sites exceed the target? For each of the 11 CRC sites (LASSO; development sites with their
leave-one-cohort-out model, locked sites with the model trained on all 8 development cohorts), decompose the shift of the
site's control scores relative to the source controls into species contributions (oral-origin taxa enriched, commensals
depleted, other), and relate the realised FPR to technical/population covariates of the controls (median sequencing depth,
Shannon diversity, extraction kit, country, age)."""
import sys, os, numpy as np, pandas as pd
from scipy import stats
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src.data import load, DEV_CRC, LOCKED_CRC
from src.models import preprocess_fit, preprocess_apply, make, logit
from src import calibrate as C
ORAL = ["Streptococcus", "Veillonella", "Fusobacterium", "Gemella", "Peptostreptococcus", "Parvimonas", "Porphyromonas",
        "Lactobacillus_salivarius", "Actinomyces", "Haemophilus", "Solobacterium", "Dialister_pneumosintes", "Rothia",
        "Prevotella_intermedia", "Prevotella_nigrescens", "Campylobacter", "Eikenella", "Granulicatella", "Atopobium", "Filifactor"]
X, y, g, M = load("CRC", DEV_CRC + LOCKED_CRC); cols = X.columns; Xv = X.values
au = pd.read_csv(os.path.join(H, "addendum_results", "posthoc_crc_audit_sites.csv")); au = au[au.model == "lasso"].set_index("site")
rows = []
for site in DEV_CRC + LOCKED_CRC:
    tr = np.isin(g, [s for s in DEV_CRC if s != site]); te = g == site
    p = preprocess_fit(Xv[tr]); Ztr, Zte = preprocess_apply(Xv[tr], p), preprocess_apply(Xv[te], p); feat = cols[p["keep"]]
    m = make("lasso").fit(Ztr, y[tr]); coef = m.coef_[0]
    oral = np.array([any(o in f for o in ORAL) and c > 0 for f, c in zip(feat, coef)])
    c_src = Ztr[y[tr] == 0].mean(0); c_site = Zte[y[te] == 0].mean(0); contrib = coef * (c_site - c_src)
    ra = Xv[te][y[te] == 0] / 100; ra = ra / ra.sum(1, keepdims=True)
    shannon = np.mean([-(r[r > 0] * np.log(r[r > 0])).sum() for r in ra])
    md = M[te][y[te] == 0]
    rows.append(dict(site=site, role="locked" if site in LOCKED_CRC else "development", fpr=au.loc[site, "fpr"],
                     shift_total=contrib.sum(), shift_oral=contrib[oral].sum(), shift_depletion=contrib[coef < 0].sum(),
                     shift_other=contrib[(coef > 0) & ~oral].sum(), shannon=shannon,
                     depth_M=np.median(pd.to_numeric(md.number_reads, errors="coerce")) / 1e6,
                     kit=str(md.DNA_extraction_kit.mode().iloc[0]) if md.DNA_extraction_kit.notna().any() else "NA",
                     country=str(md.country.mode().iloc[0]), age=pd.to_numeric(md.age, errors="coerce").median()))
D = pd.DataFrame(rows).sort_values("fpr", ascending=False)
D.to_csv(os.path.join(H, "addendum_results", "posthoc_site_explain.csv"), index=False)
pd.set_option("display.width", 250); print(D.round(3).to_string(index=False))
print("\nSpearman correlation with site FPR (11 sites):")
for v in ["shift_total", "shift_oral", "shift_depletion", "shift_other", "shannon", "depth_M", "age"]:
    r, pv = stats.spearmanr(D.fpr, D[v], nan_policy="omit"); print(f"  {v:16s} rho = {r:+.2f}  p = {pv:.3f}")
