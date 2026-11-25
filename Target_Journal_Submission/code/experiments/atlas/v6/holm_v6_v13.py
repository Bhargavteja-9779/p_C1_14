"""Review round 10: Holm-adjusted P values over the plan-v6 tests that have a P value (G2, G3, G4), strict set, as
protocol_v6.md specifies. G4 bootstrap P is bounded by its resolution (2,000 draws -> < 0.0005). Writes results/holm_v6_v13.json."""
import json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); d = json.load(open(os.path.join(R, "gmwi2_results.json")))
p = {"G2": d["strict"]["G2"]["p"], "G3": d["strict"]["G3"]["p"], "G4": max(d["G4"]["p_boot_le0"], 1 / 2000)}
o = sorted(p, key=p.get); adj, run = {}, 0
for i, k in enumerate(o): run = max(run, min(1, (len(o) - i) * p[k])); adj[k] = run
json.dump(dict(raw=p, holm=adj, note="G4 raw P is an upper bound (0 of 2000 bootstrap draws <= 0)"), open(os.path.join(R, "holm_v6_v13.json"), "w"), indent=1); print(p, adj)
