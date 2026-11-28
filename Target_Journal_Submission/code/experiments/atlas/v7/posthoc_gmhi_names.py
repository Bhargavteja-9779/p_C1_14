"""POST HOC (after run_gmhi.py): sensitivity of the cMD GMHI scores to MetaPhlAn2 -> MetaPhlAn3 species renames.
Four health-scarce species have a clear MetaPhlAn3 name; none of the four missing health-prevalent species exists in
MetaPhlAn3. Reports Q2 agreement and unseen strict flag rates with the renames applied."""
import os, sys, json, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import importlib.util
RENAME = {"s__Hungatella_hathewayi": "s__Clostridium_hathewayi", "s__Erysipelatoclostridium_ramosum": "s__Clostridium_ramosum",
          "s__Streptococcus_anginosus_group": "s__Streptococcus_anginosus", "s__Streptococcus_mitis": "s__Streptococcus_mitis_oralis_pneumoniae"}
src = open(os.path.join(HERE, "run_gmhi.py")).read().split("# ---------------- Q1")[0]
ns = {"__file__": os.path.join(HERE, "run_gmhi.py")}; exec(compile(src, "run_gmhi_head", "exec"), ns); gmhi = ns["gmhi"]
sys.path.insert(0, os.path.join(HERE, "..", "v4")); from common_v4 import controls, CACHE
R = pd.read_csv(os.path.join(HERE, "results", "gmhi_rows.csv.gz"))
new = []
for s, x in R.groupby("study", sort=False):
    raw = pd.read_csv(os.path.join(CACHE, "ra", f"{s}.csv"), index_col=0)[list(x.sample_id)]
    raw.index = [i.split("|")[-1] for i in raw.index]; raw = raw[[i.startswith("s__") for i in raw.index]]
    raw.index = [RENAME.get(i, i) for i in raw.index]; raw = raw.groupby(level=0).sum()
    new.append(pd.Series(gmhi(raw).values, index=x.index))
R["gmhi_renamed"] = pd.concat(new).reindex(R.index)
q = R.dropna(subset=["dev_gmhi"])
S = R[R.strict_person & R.strict_study]; P = S.groupby("study").agg(n=("flag", "size"), seen=("in_gmhi_training", "any"),
       fpr=("gmhi", lambda v: float((v < 0).mean())), fpr_renamed=("gmhi_renamed", lambda v: float((v < 0).mean()))).reset_index()
U = P[(~P.seen) & (P.n >= 20)]
out = dict(q2_pearson_renamed=float(np.corrcoef(q.gmhi_renamed, q.dev_gmhi)[0, 1]), q2_pearson_original=float(np.corrcoef(q.gmhi, q.dev_gmhi)[0, 1]),
           unseen_strict_median_fpr_original=float(U.fpr.median()), unseen_strict_median_fpr_renamed=float(U.fpr_renamed.median()),
           dev_overlap_flag_rate_dev_profiles=float((q.dev_gmhi < 0).mean()), dev_overlap_flag_rate_cmd_profiles=float((q.gmhi < 0).mean()),
           spearman_original_vs_renamed=float(U[["fpr", "fpr_renamed"]].corr("spearman").iloc[0, 1]))
json.dump(out, open(os.path.join(HERE, "results", "posthoc_gmhi_names.json"), "w"), indent=1); print(out)
