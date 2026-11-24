"""P6 atlas re-run on de-duplicated data (+P7 fold-model scores). Writes results/atlas_rows_v4.csv.gz, atlas_coefs_v4.csv."""
import os, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from multiprocessing import Pool
from common_v4 import *
from src.pipeline import Pipeline, make, logit, _log
from sklearn.model_selection import GroupKFold
ALPHA = 0.10
class PipeF(Pipeline):
    """Same fit as Pipeline; additionally keeps the inner LOCO fold models for P7 (no change to OOF scores or refit)."""
    def fit(self, X, y, g):
        super().fit(X, y, g); Z = (_log(X, self.keep) - self.mu) / self.sd
        self.folds = [make(self.model, self.seed).fit(Z[a], y[a]) for a, b in GroupKFold(len(np.unique(g))).split(Z, y, g)]
        return self
    def score_folds(self, Xt):
        Z = (_log(Xt, self.keep) - self.mu) / self.sd
        return np.mean([logit(m.predict_proba(Z)[:, 1]) for m in self.folds], 0)
def job(a):
    disease, model = a
    X, y, g, M = load(disease); p = PipeF(model).fit(X.values, y, g)
    t = float(np.quantile(p.oof[y == 0], 1 - ALPHA)); rows = []
    for s in populations(disease, strict=False):
        Xc, md = controls(s); Xa = Xc.reindex(columns=X.columns, fill_value=0.0).fillna(0.0).values
        sc, sf = p.score(Xa), p.score_folds(Xa)
        rows.append(pd.DataFrame(dict(disease=disease, model=model, study=s, sample_id=md.index, strict_person=md.strict_person.values,
                                      score=sc, score_folds=sf, thr=t, flag=(sc >= t).astype(int), flag_folds=(sf >= t).astype(int))))
    for c in np.unique(g):
        i = (g == c) & (y == 0)
        rows.append(pd.DataFrame(dict(disease=disease, model=model, study="TRAIN:" + c, sample_id=M.index[i], strict_person=np.nan,
                                      score=p.oof[i], score_folds=p.oof[i], thr=t, flag=(p.oof[i] >= t).astype(int), flag_folds=(p.oof[i] >= t).astype(int))))
    coefs = pd.DataFrame(dict(disease=disease, taxon=X.columns[p.keep], w=p.m.coef_[0], mu=p.mu, sd=p.sd)) if model == "lasso" else None
    print(disease, model, "done", flush=True); return pd.concat(rows), coefs
if __name__ == "__main__":
    f = os.path.join(OUT, "atlas_rows_v4.csv.gz"); assert not os.path.exists(f), "already run"
    with Pool(4) as P: res = P.map(job, [(d, m) for d in ["CRC", "IBD", "T2D"] for m in ["lasso", "rf"]])
    pd.concat([r[0] for r in res]).to_csv(f, index=False)
    pd.concat([r[1] for r in res if r[1] is not None]).to_csv(os.path.join(OUT, "atlas_coefs_v4.csv"), index=False)
