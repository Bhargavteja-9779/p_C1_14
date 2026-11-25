"""The 14 LASSO disease tests of the atlas, shipped as plain coefficient tables (refit by
experiments/atlas/v5/export_models_v11.py; exported scores match the atlas scores to 1e-13).

Input: species relative abundances in percent (MetaPhlAn3-style), one row per sample, one column per taxon. Column names
may be full clade strings (k__...|s__Name) or the last level only (s__Name). Missing taxa count as 0.
Score = intercept + sum_j w_j * (log10(x_j/100 + 1e-5) - mu_j) / sd_j, on the logit scale, clipped to +-9.21.
Research use only: these are atlas classifiers, not validated diagnostics; their AUROC ranges from 0.54 to 0.94."""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
_D = os.path.join(os.path.dirname(__file__), "data")


def _coef(): return pd.read_csv(os.path.join(_D, "models_lasso_v5.csv"))


def meta() -> pd.DataFrame:
    """Per test: intercept, training cut-off (targets FPR 0.10 on training controls), training cohorts, AUROC."""
    m = pd.read_csv(os.path.join(_D, "models_lasso_v5_meta.csv"))
    h = pd.read_csv(os.path.join(_D, "atlas_heterogeneity_strict_v5.csv")); h = h[h.model == "lasso"][["test", "auroc"]]
    return m.merge(h, on="test", how="left")


def _norm(cols): return [str(c).split("|")[-1] for c in cols]


def score(abund: pd.DataFrame, test: str) -> pd.Series:
    """Logit-scale score of each sample (row) for one test."""
    c = _coef(); c = c[c.test.str.lower() == test.lower()]
    if c.empty: raise KeyError(f"unknown test {test}; tests: {', '.join(meta().test)}")
    m = meta().set_index("test").loc[c.test.iloc[0]]
    A = abund.copy(); A.columns = _norm(A.columns); A = A.T.groupby(level=0).sum().T
    missing = [t for t in c.taxon if t not in A.columns]
    X = A.reindex(columns=c.taxon, fill_value=0.0).fillna(0.0).astype(float).values
    z = (np.log10(X / 100 + 1e-5) - c.mu.values) / c.sd.values
    s = pd.Series(np.clip(z @ c.w.values + m.intercept, -9.21024, 9.21024), index=abund.index, name=f"score_{m.name}")
    s.attrs["missing_taxa"] = missing; s.attrs["cutoff"] = float(m.cutoff)
    return s


def score_all(abund: pd.DataFrame) -> pd.DataFrame:
    """Scores and flags (score >= training cut-off) for all 14 tests."""
    out = {}
    for t in meta().test:
        s = score(abund, t); out[f"{t}_score"] = s.values; out[f"{t}_flag"] = (s.values >= s.attrs["cutoff"]).astype(int)
    return pd.DataFrame(out, index=abund.index)
