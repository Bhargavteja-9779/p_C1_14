"""The 14 LASSO disease tests of the atlas, shipped as plain coefficient tables (refit by
experiments/atlas/v5/export_models_v11.py; exported scores match the atlas scores to 1e-13).

Features: MetaPhlAn3 relative abundances (%) of ALL clades, kingdom to species (k__, p__, c__, o__, f__, g__, s__),
present in > 5% of training samples, each named by its last level (e.g. g__Blautia, s__Fusobacterium_nucleatum). The
models are NOT species-only: higher ranks carry 8-86% of each test's total |coefficient| weight.

Input: one row per sample, one column per clade (relative abundance in %). Best input is the full MetaPhlAn3 /
curatedMetagenomicData table with full clade strings (k__Bacteria|p__...|...|s__Name), all ranks. If only the
species-level rows are given but with full lineage strings, every higher rank that is not in the table is computed by
summing the species below it (this reproduces the MetaPhlAn3 higher-rank rows to rounding error).

Missing vs absent features. A model feature at a rank that appears in the input (e.g. a species when other species are
given) but has no column was not detected and counts as 0 % (MetaPhlAn and cMD omit undetected clades); its |w| share is
reported as `absent_weight`. A feature at a rank that does not appear in the input at all (e.g. genera when a
species-only table without lineage strings is given), or whose value is NaN, is *missing*: its value is unknown. Per
sample, `missing_weight` = sum of |w| over missing features / sum of |w| over all model features. If it exceeds
`max_missing` (default 0.05), `score` raises MissingFeaturesError unless `allow_missing=True`; then missing features are
set to their training mean (they contribute 0 to the score) and a warning is issued.

Score = intercept + sum_j w_j * (log10(x_j/100 + 1e-5) - mu_j) / sd_j, on the logit scale, clipped to +-9.21.
Research use only: these are atlas classifiers, not validated diagnostics; their AUROC ranges from 0.54 to 0.94."""
from __future__ import annotations
import os
import warnings
import numpy as np
import pandas as pd
_D = os.path.join(os.path.dirname(__file__), "data")
RANKS = ("k", "p", "c", "o", "f", "g", "s", "t")


class MissingFeaturesError(ValueError):
    """The input lacks model features that carry more than the allowed share of |coefficient| weight."""


def _coef(): return pd.read_csv(os.path.join(_D, "models_lasso_v5.csv"))


def meta() -> pd.DataFrame:
    """Per test: intercept, training cut-off (targets FPR 0.10 on training controls), training cohorts, AUROC."""
    m = pd.read_csv(os.path.join(_D, "models_lasso_v5_meta.csv"))
    h = pd.read_csv(os.path.join(_D, "atlas_heterogeneity_strict_v5.csv")); h = h[h.model == "lasso"][["test", "auroc"]]
    return m.merge(h, on="test", how="left")


def _rank(name: str) -> str | None:
    r = name.split("__", 1)[0] if "__" in name else None
    return r if r in RANKS else None


def to_clades(abund: pd.DataFrame) -> pd.DataFrame:
    """Columns -> last-level clade names (as in the atlas), after filling in higher ranks from lineage strings.

    Full clade strings (k__..|..|s__..) are reduced to their last level. Any ancestor clade that is not itself a column
    is computed as the sum of the leaf columns (columns with no descendants in the table) below it. Duplicated last-level
    names are summed, as in atlas_v5.py."""
    A = abund.copy(); A.columns = [str(c).strip() for c in A.columns]
    cols = list(A.columns); present = set(cols)
    full = [c for c in cols if "|" in c]
    if full:
        ancestors = {"|".join(c.split("|")[:i]) for c in full for i in range(1, c.count("|") + 1)}
        add: dict[str, pd.Series] = {}
        for c in full:
            if c in ancestors: continue                                   # not a leaf: its descendants are in the table
            parts = c.split("|")
            for i in range(1, len(parts)):
                p = "|".join(parts[:i])
                if p not in present: add[p] = add[p] + A[c] if p in add else A[c].copy()
        if add: A = pd.concat([A, pd.DataFrame(add, index=A.index)], axis=1)
    A.columns = [c.split("|")[-1] for c in A.columns]
    return A.T.groupby(level=0).sum(min_count=1).T


def _prepare(abund, c):
    """Feature matrix in model order, plus per-sample missing and absent |w| shares."""
    A = to_clades(abund)
    ranks = {_rank(x) for x in A.columns} - {None}
    a = np.abs(c.w.values); tot = a.sum()
    in_cols = c.taxon.isin(A.columns).values
    rank_seen = np.array([_rank(t) in ranks for t in c.taxon])
    X = A.reindex(columns=c.taxon).astype(float).values                 # NaN where column absent
    nan = np.isnan(X)
    missing = (~rank_seen)[None, :] | (in_cols[None, :] & nan)          # rank not given at all, or NaN value
    absent = (rank_seen & ~in_cols)[None, :] & np.ones_like(nan)        # rank given, clade not detected -> 0 %
    X = np.where(absent, 0.0, X)
    return X, missing, missing @ a / tot, absent @ a / tot


def score(abund: pd.DataFrame, test: str, max_missing: float = 0.05, allow_missing: bool = False) -> pd.Series:
    """Logit-scale score of each sample (row) for one test.

    attrs: cutoff, missing_weight (per sample), absent_weight (per sample), missing_taxa (model features missing in
    at least one sample). Raises MissingFeaturesError if any sample's missing_weight > max_missing and not allow_missing."""
    c = _coef(); c = c[c.test.str.lower() == test.lower()]
    if c.empty: raise KeyError(f"unknown test {test}; tests: {', '.join(meta().test)}")
    m = meta().set_index("test").loc[c.test.iloc[0]]
    X, miss, mw, aw = _prepare(abund, c)
    names = c.taxon.values[miss.any(axis=0)].tolist()
    if (mw > max_missing).any():
        msg = (f"{m.name}: model features carrying up to {mw.max():.1%} of the total |coefficient| weight are missing from "
               f"the input (limit {max_missing:.0%}; {len(names)} features, e.g. {', '.join(names[:5])}). The models use "
               f"MetaPhlAn3 clades of every rank (kingdom to species): give the full clade table (k__...|...|s__... strings, "
               f"all ranks, as in curatedMetagenomicData) or species rows with full lineage strings.")
        if not allow_missing: raise MissingFeaturesError(msg + " Use allow_missing=True (--allow-missing) to score anyway.")
        warnings.warn(msg + " Scoring anyway (allow_missing): missing features set to their training mean; scores are biased.",
                      stacklevel=2)
    z = (np.log10(np.where(miss, 0.0, X) / 100 + 1e-5) - c.mu.values) / c.sd.values
    z = np.where(miss, 0.0, z)                                          # missing -> training mean (contributes 0)
    s = pd.Series(np.clip(z @ c.w.values + m.intercept, -9.21024, 9.21024), index=abund.index, name=f"score_{m.name}")
    s.attrs.update(missing_taxa=names, cutoff=float(m.cutoff),
                   missing_weight=pd.Series(mw, index=abund.index), absent_weight=pd.Series(aw, index=abund.index))
    return s


def score_all(abund: pd.DataFrame, max_missing: float = 0.05, allow_missing: bool = False) -> pd.DataFrame:
    """Scores, flags (score >= training cut-off) and missing-weight shares for all 14 tests."""
    out = {}
    for t in meta().test:
        s = score(abund, t, max_missing, allow_missing)
        out[f"{t}_score"] = s.values; out[f"{t}_flag"] = (s.values >= s.attrs["cutoff"]).astype(int)
        out[f"{t}_missing_weight"] = s.attrs["missing_weight"].values
    return pd.DataFrame(out, index=abund.index)
