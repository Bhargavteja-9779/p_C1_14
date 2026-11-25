"""Resume an interrupted locked run (container restart) WITHOUT re-running finished cohorts.

The only global randomness in run_final.py is rng = default_rng(2026), consumed by two permutations per replicate
(controls, cases). Model fitting is seeded (random_state=0). Replaying those permutations for the finished cohorts
(sizes n0/n1 from the run log) restores the exact rng state, so the remaining cohorts get the same splits an
uninterrupted run would have used. Usage: python resume_final.py <model>
"""
import os, re, sys, runpy
import numpy as np, pandas as pd

H = os.path.dirname(os.path.abspath(__file__)); model = sys.argv[1]
csv, log = os.path.join(H, f"final_{model}.csv"), os.path.join(H, f"final_{model}.log")
done = [re.split(r"\s+", l.strip()) for l in open(log) if l.startswith(model + " ")]
done = [(p[1], p[2], int(p[6]), int(p[8])) for p in done]  # disease, cohort, n0, n1
prev = pd.read_csv(csv)
assert len(prev.groupby(["disease", "cohort"])) == len(done), "CSV and log disagree"
R = 200
src = open(os.path.join(H, "run_final.py")).read()
# 1) rng replay for finished cohorts; 2) skip them in the task loop; 3) start rows from the saved CSV
replay = ("rng = np.random.default_rng(2026)\n"
          f"for _n0, _n1 in {[(a, b) for _, _, a, b in done]}:\n"
          f"    for _r in range({R}): rng.permutation(np.arange(_n0)); rng.permutation(np.arange(_n1))\n")
src = src.replace('rng = np.random.default_rng(2026)', 'rng = None', 1)
src = src.replace("rows = []\n", replay + "import pandas as _pd\nrows = _pd.read_csv(%r).to_dict('records')\n" % csv
                  + "DONE = %r\n" % {(d, c) for d, c, _, _ in done}, 1)
src = src.replace("for dis, s, X, y, g, tr, te in tasks():\n",
                  "for dis, s, X, y, g, tr, te in tasks():\n    if (dis, s) in DONE: continue\n", 1)
assert src.count("DONE") == 2 and "rng = None" in src
sys.argv = ["run_final.py", model]
exec(compile(src, os.path.join(H, "run_final.py"), "exec"), {"__name__": "__main__", "__file__": os.path.join(H, "run_final.py")})
