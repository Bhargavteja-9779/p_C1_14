"""Atlas of realised FPRs: 14 disease tests x 2 models (LASSO, random forest) x up to 36 strict healthy populations
(curatedMetagenomicData 2021-03-31; cut-off = 90th percentile of training-control out-of-fold scores, target FPR 0.10).
Shipped data are the result files of experiments/atlas/v5 (analyse_v5.py)."""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
_D = os.path.join(os.path.dirname(__file__), "data")


def populations() -> pd.DataFrame:
    """One row per test x model x population: n healthy people, k flagged, FPR, country, non-westernised flag."""
    return pd.read_csv(os.path.join(_D, "atlas_perpop_strict_v5.csv"))


def heterogeneity() -> pd.DataFrame:
    """One row per test x model: random-effects pooled FPR, tau (logit), I2, 95% prediction interval, share of
    populations outside 0.05-0.15, AUROC (leave-one-cohort-out on training data)."""
    return pd.read_csv(os.path.join(_D, "atlas_heterogeneity_strict_v5.csv"))


def tests() -> list[str]:
    return sorted(heterogeneity().test.unique())


def lookup(test: str, model: str = "lasso") -> dict:
    """What a new site should expect for this test: pooled FPR, 95% prediction interval, observed range."""
    h = heterogeneity(); r = h[(h.test.str.lower() == test.lower()) & (h.model == model)]
    if r.empty: raise KeyError(f"unknown test/model {test}/{model}; tests: {', '.join(tests())}")
    r = r.iloc[0]; p = populations(); p = p[(p.test == r.test) & (p.model == model)].sort_values("fpr")
    return dict(test=r.test, model=model, populations=int(r.populations), people=int(r.people), auroc=float(r.auroc),
                pooled_fpr=float(r.pooled), I2=float(r.I2), tau_logit=float(r.tau), pi95=(float(r.pi_lo), float(r.pi_hi)),
                share_outside_005_015=float(r.oob), lowest=p.head(3)[["study", "country", "n", "fpr"]].to_dict("records"),
                highest=p.tail(3)[::-1][["study", "country", "n", "fpr"]].to_dict("records"))


def position(test: str, model: str, local_fpr: float) -> float:
    """Percentile of a site's measured FPR among atlas populations for this test (0 = lowest, 1 = highest)."""
    p = populations(); p = p[(p.test.str.lower() == test.lower()) & (p.model == model)]
    return float((p.fpr < local_fpr).mean() + 0.5 * (p.fpr == local_fpr).mean())
