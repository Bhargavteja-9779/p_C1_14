"""v4 shared loaders: de-duplicated data (P0) and strict healthy flag (P1)."""
import os, sys, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ATL = os.path.dirname(HERE)
sys.path.insert(0, ATL); sys.path.insert(0, os.path.join(ATL, "..", ".."))
from src.data import load as _load, CACHE, DISEASES, DEV_CRC, LOCKED_CRC
from atlas_run import load_controls, healthy_studies, META
from common import split
OUT = os.path.join(HERE, "results"); os.makedirs(OUT, exist_ok=True)
STRICT_DROP_STUDIES = ["VincentC_2016", "MetaCardis_2020_a", "FengQ_2015", "LoombaR_2017", "YuJ_2015", "ThomasAM_2018a",
    "BackhedF_2015", "YassourM_2018", "FerrettiP_2018", "ShaoY_2019", "TettAJ_2019_a", "TettAJ_2019_b", "TettAJ_2019_c",
    "RaymondF_2016", "HMP_2019_ibdmdb", "IjazUZ_2017", "ZellerG_2014", "VogtmannE_2016", "HanniganGD_2017", "CosteaPI_2017"]
MIN_N = 20

def excluded():
    p = os.path.join(OUT, "excluded_samples.txt")
    return set(open(p).read().split()) if os.path.exists(p) else set()

def dropped_studies():
    p = os.path.join(OUT, "dropped_studies.txt")
    return set(open(p).read().split()) if os.path.exists(p) else set()

def load(disease, studies=None):
    X, y, g, M = _load(disease, studies); k = ~X.index.isin(excluded())
    return X[k], y[k], g[k], M[k]

_c = {}
def controls(s):
    """De-duplicated adult healthy controls of study s (X, metadata with 'strict_person' column)."""
    if s not in _c:
        X, md = load_controls(s); k = ~X.index.isin(excluded()); X, md = X[k], md[k].copy()
        md["strict_person"] = ((md.disease == "healthy") & (md.antibiotics_current_use != "yes") & (md.pregnant != "yes")
                               & md.family_role.isna() & (md.get("lactating") != "yes")).values
        _c[s] = (X, md)
    return _c[s]

def populations(disease, strict):
    """Healthy populations usable for a classifier: not in its training set, not dropped, n >= MIN_N."""
    train = set(DISEASES[disease]["studies"]); out = []
    for s in healthy_studies():
        if s in train or s in dropped_studies() or not os.path.exists(os.path.join(CACHE, "ra", f"{s}.csv")): continue
        if strict and s in STRICT_DROP_STUDIES: continue
        X, md = controls(s); n = int(md.strict_person.sum()) if strict else len(md)
        if n >= MIN_N: out.append(s)
    return out
