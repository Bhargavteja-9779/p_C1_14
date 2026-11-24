#!/usr/bin/env bash
# Full reproducibility check: fresh clone of the pushed branch, all v4 result scripts in README order with results/
# moved aside, then comparison of every regenerated CSV/JSON with the committed copy, and the number audit.
# usage: scripts/repro_full.sh WORKDIR [CMD_CACHE]
set -euo pipefail
W="$1"; export CMD_CACHE="${2:-$(cd "$(dirname "$0")/.." && pwd)/data_cache}"
rm -rf "$W/clone"; git clone -q -b claude/trusting-mayer-1ipvjz https://github.com/Bhargavteja-9779/p_C1_14.git "$W/clone"
cd "$W/clone"; echo "commit $(git rev-parse HEAD)"; echo "python $(python3 --version 2>&1)"
cd Target_Journal_Submission/code/experiments/atlas/v4; mkdir ref; mv results/* ref/
for s in dedup.py atlas_v4.py analyse_atlas_v4.py hypotheses_v4.py taxa_v4.py deploy_v4.py summarise_v4.py \
         control_augmentation_v4.py h2h_v4.py holm_v4.py counts_v4.py r3_posthoc.py neardup_check.py dedup095_sensitivity.py \
         holm_v5.py r6_posthoc.py r7_posthoc.py make_figures_v8.py make_graphical_abstract.py make_si_v4.py; do
  t0=$(date +%s); python3 -W ignore "$s" > /dev/null; echo "ran $s ($(( $(date +%s) - t0 )) s)"; done
python3 - <<'PY'
import os, json, pandas as pd, numpy as np
bad = 0
for f in sorted(os.listdir("ref")):
    a, b = os.path.join("results", f), os.path.join("ref", f)
    if not os.path.exists(a): print("MISSING", f); bad += 1; continue
    if f.endswith((".csv", ".csv.gz")):
        x, y = pd.read_csv(a), pd.read_csv(b)
        same = x.shape == y.shape and all((x[c].equals(y[c]) or (pd.api.types.is_numeric_dtype(x[c]) and np.allclose(x[c].fillna(-9), y[c].fillna(-9), atol=1e-9))) for c in x.columns)
    elif f.endswith(".json"): same = json.load(open(a)) == json.load(open(b))
    else: same = open(a).read() == open(b).read()
    print(("same     " if same else "DIFFERENT"), f); bad += (not same)
print("files differing:", bad)
PY
cd "$W/clone" && python3 scripts/audit_numbers.py Target_Journal_Submission/manuscript/manuscript_v9.md | head -2
