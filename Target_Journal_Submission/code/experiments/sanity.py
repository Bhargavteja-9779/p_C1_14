"""Stage 5 sanity and leakage checks (CRC, all 10 cohorts, LOSO, LASSO + RF).
1) real labels; 2) shuffled training labels (expect AUROC ~0.5); 3) single-feature trivial baseline (F. nucleatum
abundance); 4) majority-class baseline; 5) cohort identity predictability from profiles (strength of site effects);
6) tiny-data: train on 2 cohorts only. Output: results/sanity.csv"""
import os, sys, warnings
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.data import load, DISEASES
from src.pipeline import Pipeline
warnings.filterwarnings("ignore")
X, y, g, M = load("CRC"); cols = X.columns; X = X.values.astype(float)
rows = []
for model in ("lasso", "rf"):
    for s in DISEASES["CRC"]["studies"]:
        tr, te = g != s, g == s
        a_real = roc_auc_score(y[te], Pipeline(model, seed=0).fit(X[tr], y[tr], g[tr]).score(X[te]))
        rng = np.random.default_rng(0); ysh = y.copy(); ysh[tr] = rng.permutation(y[tr])
        a_shuf = roc_auc_score(y[te], Pipeline(model, seed=0).fit(X[tr], ysh[tr], g[tr]).score(X[te]))
        tiny_tr = np.isin(g, [c for c in DISEASES["CRC"]["studies"] if c != s][:2])
        a_tiny = roc_auc_score(y[te], Pipeline(model, seed=0).fit(X[tiny_tr], y[tiny_tr], g[tiny_tr]).score(X[te]))
        rows.append(dict(model=model, target=s, auc_real=a_real, auc_shuffled=a_shuf, auc_train_2_cohorts=a_tiny))
fn = [i for i, c in enumerate(cols) if "Fusobacterium_nucleatum" in c][0]
for s in DISEASES["CRC"]["studies"]:
    te = g == s; rows.append(dict(model="F_nucleatum_only", target=s, auc_real=roc_auc_score(y[te], X[te, fn])))
    rows.append(dict(model="majority_class", target=s, auc_real=0.5))
r = pd.DataFrame(rows)
# cohort identity from controls only (site effect strength), 5-fold CV balanced accuracy
c0 = y == 0; L = np.log10(X[c0][:, (X[c0] > 0).mean(0) > 0.05] / 100 + 1e-5)
acc = cross_val_score(LogisticRegression(C=0.1, max_iter=3000, class_weight="balanced"), L, g[c0],
                      cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="balanced_accuracy").mean()
r.to_csv(os.path.join(os.path.dirname(__file__), "..", "results", "sanity.csv"), index=False)
print(r.groupby("model")[["auc_real", "auc_shuffled", "auc_train_2_cohorts"]].agg(["mean", "min", "max"]).round(3).to_string())
print("cohort identity from control profiles, balanced accuracy:", round(acc, 3), "chance:", round(1 / len(np.unique(g)), 3))
