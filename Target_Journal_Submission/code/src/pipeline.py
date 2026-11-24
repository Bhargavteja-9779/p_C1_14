"""Training pipelines. 'global': z-score features with pooled training statistics (standard).
'pcz': z-score every cohort with its own statistics; at a new site, z-score with the unlabeled deployment pool
(test-time feature re-standardisation, a common batch-effect fix)."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, StratifiedKFold


def make(name, seed=0):
    if name == "lasso":
        return LogisticRegression(l1_ratio=1, C=0.1, solver="liblinear", class_weight="balanced", random_state=seed)
    if name == "rf":
        return RandomForestClassifier(500, min_samples_leaf=2, n_jobs=1, random_state=seed,
                                      class_weight="balanced_subsample")
    raise ValueError(name)


def logit(p):
    p = np.clip(p, 1e-4, 1 - 1e-4); return np.log(p / (1 - p))


def _log(X, keep):
    return np.log10(X[:, keep] / 100 + 1e-5)


def _zs(L, ref=None):
    ref = L if ref is None else ref; return (L - ref.mean(0)) / (ref.std(0) + 1e-6)


class Pipeline:
    def __init__(self, model, mode="global", seed=0):
        self.model, self.mode, self.seed = model, mode, seed

    def _design(self, L, g):
        if self.mode == "global": return (L - self.mu) / self.sd
        Z = np.empty_like(L)
        for c in np.unique(g): Z[g == c] = _zs(L[g == c])
        return Z

    def fit(self, X, y, g):
        self.keep = (X > 0).mean(0) > 0.05
        L = _log(X, self.keep); self.mu, self.sd = L.mean(0), L.std(0) + 1e-6
        Z = self._design(L, g)
        ug = np.unique(g); oof = np.zeros(len(y))
        folds = (GroupKFold(len(ug)).split(Z, y, g) if len(ug) >= 3
                 else StratifiedKFold(5, shuffle=True, random_state=self.seed).split(Z, y))
        for a, b in folds:  # inner leave-one-cohort-out; preprocessing statistics are from the full training set
            oof[b] = make(self.model, self.seed).fit(Z[a], y[a]).predict_proba(Z[b])[:, 1]
        self.m = make(self.model, self.seed).fit(Z, y)
        self.oof, self.y, self.g = logit(oof), y, g
        return self

    def score(self, Xt, pool_idx=None):
        L = _log(Xt, self.keep)
        Z = (L - self.mu) / self.sd if self.mode == "global" else _zs(L, L[pool_idx])
        return logit(self.m.predict_proba(Z)[:, 1])
