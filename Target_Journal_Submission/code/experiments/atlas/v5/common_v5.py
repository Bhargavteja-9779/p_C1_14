"""v5 shared code: geography-stable feature penalisation (GSP). Reuses v4 de-duplicated loaders."""
import os, sys, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "v4"))
from common_v4 import *                      # load, controls, populations, split, STRICT_DROP_STUDIES, DISEASES, ...
from src.pipeline import make, logit, _log
from sklearn.model_selection import GroupKFold
OUT5 = os.path.join(HERE, "results"); os.makedirs(OUT5, exist_ok=True)
A = 0.10

def feature_icc(L_list):
    """Between-population share of variance per feature (one-way random-effects ICC, moment estimator), from a list of
    per-population matrices of log-abundance (same columns)."""
    k = len(L_list); n = np.array([len(x) for x in L_list]); N = n.sum()
    means = np.array([x.mean(0) for x in L_list]); grand = np.concatenate(L_list).mean(0)
    msb = (n[:, None] * (means - grand) ** 2).sum(0) / (k - 1)
    msw = sum(((x - x.mean(0)) ** 2).sum(0) for x in L_list) / (N - k)
    n0 = (N - (n ** 2).sum() / N) / (k - 1)
    s2b = np.maximum((msb - msw) / n0, 0)
    return s2b / (s2b + msw + 1e-12)

class GSP:
    """Classifier on z-scored log features, column j multiplied by s_j = (1 - icc_j)^gamma (LASSO: higher effective
    penalty for population-variable taxa); for RF, features with icc above the drop quantile are removed."""
    def __init__(self, model, icc=None, gamma=0.0, drop_q=None, seed=0):
        self.model, self.icc, self.gamma, self.drop_q, self.seed = model, icc, gamma, drop_q, seed
    def _Z(self, X):
        Z = (_log(X, self.keep) - self.mu) / self.sd
        return Z[:, self.use] * self.s[self.use]
    def fit(self, X, y, g):
        self.keep = (X > 0).mean(0) > 0.05
        L = _log(X, self.keep); self.mu, self.sd = L.mean(0), L.std(0) + 1e-6
        icc = np.zeros(self.keep.sum()) if self.icc is None else self.icc[self.keep]
        self.s = (1 - icc) ** self.gamma; self.use = np.ones(len(icc), bool)
        if self.drop_q is not None: self.use = icc <= np.quantile(icc, self.drop_q)
        Z = self._Z(X); oof = np.zeros(len(y))
        for a, b in GroupKFold(len(np.unique(g))).split(Z, y, g):
            oof[b] = make(self.model, self.seed).fit(Z[a], y[a]).predict_proba(Z[b])[:, 1]
        self.m = make(self.model, self.seed).fit(Z, y); self.oof = logit(oof); self.y, self.g = y, g
        self.t = float(np.quantile(self.oof[y == 0], 1 - A)); return self
    def score(self, X): return logit(self.m.predict_proba(self._Z(X))[:, 1])
