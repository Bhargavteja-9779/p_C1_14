"""POST HOC (review round 5): distribution of the maximum cross-cohort log-profile correlation per sample, to see whether
near-duplicates exist below r = 0.99. Writes results/neardup_check.csv (pairs with r > 0.90) and prints a histogram."""
import os, numpy as np, pandas as pd
from common_v4 import *
from common_v4 import _load
Xs, lab = [], []
for s in healthy_studies():
    if not os.path.exists(os.path.join(CACHE, "ra", f"{s}.csv")) or s in dropped_studies(): continue
    X, md = controls(s); Xs.append(X); lab += [("H", s, i) for i in X.index]
for d in ["CRC", "IBD", "T2D"]:
    X, y, g, M = load(d); Xs.append(X); lab += [("T" + d, gg, i) for gg, i in zip(g, X.index)]
lab = pd.DataFrame(lab, columns=["kind", "study", "sample"])
A = pd.concat(Xs).fillna(0.0).values.astype(np.float32)
A = A / (A.sum(1, keepdims=True) + 1e-12); L = np.log10(A + 1e-5); L -= L.mean(1, keepdims=True); L /= np.linalg.norm(L, axis=1, keepdims=True)
st = lab.study.values; mx = np.zeros(len(L)); hits = []
for i0 in range(0, len(L), 2000):
    C = L[i0:i0 + 2000] @ L.T
    for k in range(C.shape[0]):
        row = C[k].copy(); row[st == st[i0 + k]] = -1; row[lab["sample"].values == lab["sample"].values[i0 + k]] = -1
        j = int(row.argmax()); mx[i0 + k] = row[j]
        if row[j] > 0.90 and i0 + k < j: hits.append((lab.study[i0 + k], lab["sample"][i0 + k], st[j], lab["sample"][j], row[j]))
print(np.histogram(mx, bins=[0, .6, .7, .8, .85, .9, .93, .95, .97, .99, 1.0]))
h = pd.DataFrame(hits, columns=["sa", "ida", "sb", "idb", "r"]); h.to_csv(os.path.join(OUT, "neardup_check.csv"), index=False)
print(h.groupby(["sa", "sb"]).r.agg(["size", "min", "max"]).to_string())
