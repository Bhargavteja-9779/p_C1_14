"""POST HOC (review r19): robust headline (share of classifier-population pairs outside 0.05-0.15 under refit and
fold-model scoring, strict set), unit-level H4 improvement share, full-set RF population variance share."""
import os, json, pandas as pd
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
p = pd.read_csv(os.path.join(R, "posthoc_r19_foldmodel_perpop.csv")); u = pd.read_csv(os.path.join(R, "v5_h4_units.csv"))
oob = lambda f: (f < .05) | (f > .15)
out = dict(pairs=int(len(p)), oob_refit_all=float(oob(p.fpr_refit).mean()), oob_fold_all=float(oob(p.fpr_fold).mean()),
           oob_refit={m: float(oob(g.fpr_refit).mean()) for m, g in p.groupby("model")}, oob_fold={m: float(oob(g.fpr_fold).mean()) for m, g in p.groupby("model")},
           gt015_refit_all=float((p.fpr_refit > .15).mean()), gt015_fold_all=float((p.fpr_fold > .15).mean()),
           h4_units=int(len(u)), h4_units_improved=float((u.burn < u.src).mean()),
           h2_full_rf_pop_share=json.load(open(os.path.join(R, "v5_summary.json")))["H2_full_rf"]["pop_share"])
json.dump(out, open(os.path.join(R, "posthoc_r19_numbers.json"), "w"), indent=1); print(out)
