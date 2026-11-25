import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, GroupKFold

def preprocess_fit(Xtr, prev_min=0.05):
    keep = (Xtr > 0).mean(0) > prev_min
    L = np.log10(Xtr[:, keep] / 100 + 1e-5); mu, sd = L.mean(0), L.std(0) + 1e-6
    return dict(keep=keep, mu=mu, sd=sd)

def preprocess_apply(X, p):
    return (np.log10(X[:, p["keep"]] / 100 + 1e-5) - p["mu"]) / p["sd"]

def make(name, seed=0):
    if name == "lasso": return LogisticRegression(l1_ratio=1, C=0.1, solver="liblinear", class_weight="balanced", random_state=seed)
    if name == "rf": return RandomForestClassifier(500, min_samples_leaf=2, n_jobs=4, random_state=seed, class_weight="balanced_subsample")
    raise ValueError(name)

def logit(p): p = np.clip(p, 1e-4, 1 - 1e-4); return np.log(p / (1 - p))

def train_and_score(X, y, groups, tr, te, name, seed=0):
    """Fit preprocessing+model on tr; return source out-of-fold scores (leave-one-cohort-out inside tr when >=3 cohorts)
    and target scores. Scores on logit scale."""
    p = preprocess_fit(X[tr]); Ztr, Zte = preprocess_apply(X[tr], p), preprocess_apply(X[te], p)
    ytr, gtr = y[tr], groups[tr]
    oof = np.zeros(len(ytr)); ug = np.unique(gtr)
    folds = GroupKFold(len(ug)).split(Ztr, ytr, gtr) if len(ug) >= 3 else StratifiedKFold(5, shuffle=True, random_state=seed).split(Ztr, ytr)
    for a, b in folds:
        m = make(name, seed).fit(Ztr[a], ytr[a]); oof[b] = m.predict_proba(Ztr[b])[:, 1]
    m = make(name, seed).fit(Ztr, ytr)
    return logit(oof), ytr, logit(m.predict_proba(Zte)[:, 1]), m

def train_and_score_featstd(X, y, groups, tr, te, name, seed=0, ref="all"):
    """Baseline: per-site unlabeled feature standardisation (Zheng 2026-style). Each training cohort standardised with
    its own mean/sd. Returns source OOF logit scores, labels, and a scorer f(idx_pool, idx_score) that standardises the
    target with the mean/sd of the UNLABELED POOL rows only (same pool as the score-based methods) and scores idx_score."""
    p = preprocess_fit(X[tr]); keep = p["keep"]
    L = np.log10(X[:, keep] / 100 + 1e-5); Z = np.zeros_like(L)
    for gname in np.unique(groups[tr]):
        i = (groups == gname) & tr
        j = i & (y == 0) if ref == "controls" else i  # ref="controls" (post-hoc, review r2): standardise on controls only
        Z[i] = (L[i] - L[j].mean(0)) / (L[j].std(0) + 1e-6)
    Ztr, ytr, gtr = Z[tr], y[tr], groups[tr]
    oof = np.zeros(len(ytr))
    for a, b in GroupKFold(len(np.unique(gtr))).split(Ztr, ytr, gtr):
        oof[b] = make(name, seed).fit(Ztr[a], ytr[a]).predict_proba(Ztr[b])[:, 1]
    m = make(name, seed).fit(Ztr, ytr); Lte = L[te]
    def scorer(pool, idx):
        mu, sd = Lte[pool].mean(0), Lte[pool].std(0) + 1e-6
        return logit(m.predict_proba((Lte[idx] - mu) / sd)[:, 1])
    return logit(oof), ytr, scorer
