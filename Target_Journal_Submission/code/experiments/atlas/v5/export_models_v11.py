"""Export the 14 LASSO tests of the atlas as plain tables for fprcal (no pickles): per test, taxon, mu, sd, weight, plus
intercept and the training cut-off. Refits with the same deterministic pipeline as atlas_v5.py and checks that exported
scoring reproduces atlas_rows_v5 scores. Writes ../../../tool/fprcal/data/models_lasso_v5.csv, models_lasso_v5_meta.csv."""
import os, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from common_v5 import *
import atlas_v5 as A5
from src.pipeline import Pipeline
D = os.path.join(HERE5, "..", "..", "..", "tool", "fprcal", "data"); rows = pd.read_csv(os.path.join(OUT5, "atlas_rows_v5.csv.gz"))
coef, meta, worst = [], [], 0
for t, (case, studies) in A5.TESTS.items():
    X, y, g, M = A5.load_cc(case, studies); p = Pipeline("lasso").fit(X.values, y, g); thr = float(np.quantile(p.oof[y == 0], 1 - A))
    cols = X.columns[p.keep]; c = pd.DataFrame(dict(test=t, taxon=cols, mu=p.mu, sd=p.sd, w=p.m.coef_[0])); coef.append(c)
    meta.append(dict(test=t, intercept=float(p.m.intercept_[0]), cutoff=thr, target_fpr=A, training_cohorts=";".join(studies), n_taxa=len(cols), n_nonzero=int((c.w != 0).sum())))
    r = rows[(rows.test == t) & (rows.model == "lasso")]; assert abs(r.thr.iloc[0] - thr) < 1e-9, t
    s = r.study.iloc[0]; Xc, md = controls(s); Xc = Xc.reindex(columns=X.columns, fill_value=0.0).fillna(0.0)
    z = (np.log10(Xc[cols].values / 100 + 1e-5) - c.mu.values) / c.sd.values; sc = np.clip(z @ c.w.values + meta[-1]["intercept"], -9.21024, 9.21024)
    ref = r[r.study == s].set_index("sample_id").score.reindex(md.index).values; worst = max(worst, float(np.nanmax(np.abs(sc - ref)))); print(t, s, worst, flush=True)
pd.concat(coef).to_csv(os.path.join(D, "models_lasso_v5.csv"), index=False); pd.DataFrame(meta).to_csv(os.path.join(D, "models_lasso_v5_meta.csv"), index=False)
print("max |exported - atlas| score difference:", worst); assert worst < 1e-4
