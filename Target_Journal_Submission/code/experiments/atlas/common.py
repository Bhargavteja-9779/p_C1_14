import os, sys, re, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from src.data import load, CACHE, DISEASES, DEV_CRC, LOCKED_CRC
from atlas_run import load_controls
HERE = os.path.dirname(os.path.abspath(__file__))
def split():
    t = open(os.path.join(HERE, "atlas_split.md")).read()
    dev = re.search(r"DEV: (.*)", t).group(1).split(", "); lock = re.search(r"LOCKED: (.*)", t).group(1).split(", ")
    return dev, lock
_cache = {}
def healthy(s):
    if s not in _cache: _cache[s] = load_controls(s)
    return _cache[s]
