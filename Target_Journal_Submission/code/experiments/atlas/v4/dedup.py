"""P0: global cross-cohort duplicate detection (profiles only). Writes results/duplicates.csv, excluded_samples.txt, dropped_studies.txt."""
import os, numpy as np, pandas as pd
from common_v4 import *
from common_v4 import _load
assert not os.path.exists(os.path.join(OUT, "excluded_samples.txt")), "already run (idempotent guard)"
Xs, lab = [], []
for s in healthy_studies():
    if not os.path.exists(os.path.join(CACHE, "ra", f"{s}.csv")): continue
    X, md = load_controls(s); Xs.append(X); lab += [("H", s, i) for i in X.index]
for d in ["CRC", "IBD", "T2D"]:
    X, y, g, M = _load(d); Xs.append(X); lab += [("T" + d, gg, i) for gg, i in zip(g, X.index)]
lab = pd.DataFrame(lab, columns=["kind", "study", "sample"])
A = pd.concat(Xs).fillna(0.0).values.astype(np.float32)
A = A / (A.sum(1, keepdims=True) + 1e-12); L = np.log10(A + 1e-5); L -= L.mean(1, keepdims=True); L /= np.linalg.norm(L, axis=1, keepdims=True)
hits = []
for i0 in range(0, len(L), 2000):
    C = L[i0:i0 + 2000] @ L.T; ii, jj = np.where(C > 0.99)
    for a, b in zip(ii + i0, jj):
        if a < b and lab.study[a] != lab.study[b] and lab["sample"][a] != lab["sample"][b]: hits.append((a, b, C[a - i0, b]))
h = pd.DataFrame(hits, columns=["a", "b", "r"])
cc = set(s for d in ["CRC", "IBD", "T2D"] for s in DISEASES[d]["studies"])
size = lab.groupby("study").size()
rem = []
for a, b, r in h.itertuples(index=False):
    sa, sb = lab.study[a], lab.study[b]
    if (sa in cc) != (sb in cc): loser = b if sa in cc else a           # rule (i)
    elif sa in cc and sb in cc: loser = None                            # both case-control: report only
    else: loser = a if size[sa] < size[sb] else b                       # rule (ii)
    rem.append(None if loser is None else lab["sample"][loser])
h["sa"], h["sb"] = lab.study.values[h.a], lab.study.values[h.b]
h["ida"], h["idb"] = lab["sample"].values[h.a], lab["sample"].values[h.b]; h["removed"] = rem
h.drop(columns=["a", "b"]).to_csv(os.path.join(OUT, "duplicates.csv"), index=False)
ex = set(x for x in rem if x)
hs = lab[lab.kind == "H"].drop_duplicates("sample")
frac = hs.assign(x=hs["sample"].isin(ex)).groupby("study").x.mean()
drop = sorted(frac[frac >= 0.5].index)
open(os.path.join(OUT, "excluded_samples.txt"), "w").write("\n".join(sorted(ex)))
open(os.path.join(OUT, "dropped_studies.txt"), "w").write("\n".join(drop))
print(h.groupby(["sa", "sb"]).agg(pairs=("r", "size"), removed=("removed", lambda x: x.notna().sum())).to_string())
print("excluded samples:", len(ex), "dropped studies:", drop)
print(frac[frac > 0].round(3).to_string())
