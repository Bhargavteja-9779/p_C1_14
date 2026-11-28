"""POST HOC deviation from plan v7 (found in review round 15): the plan's accession matching between the developers'
metadata (BioSample accessions) and curatedMetagenomicData (sample names / run accessions) matched only 2 studies.
Here samples are matched through the developers' sample titles and subject IDs as well. Outputs: corrected Q2 (the
plan's gate, r >= 0.80), the profiler-version shift per study (same samples, developers' MetaPhlAn2 vs cMD MetaPhlAn3
profiles), corrected seen/unseen counts, and exact-zero (tie) counts per population."""
import os, json, numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); IN = os.path.join(HERE, "inputs"); OUT = os.path.join(HERE, "results")
src = open(os.path.join(HERE, "run_gmhi.py")).read(); ns = {"__file__": os.path.join(HERE, "run_gmhi.py")}
exec(compile(src.split("# ---------------- Q1")[0], "run_gmhi_head", "exec"), ns); gmhi = ns["gmhi"]
M = pd.read_csv(os.path.join(IN, "Final_metadata_4347.csv.gz"), header=None, index_col=0, low_memory=False).T.reset_index(drop=True)
sp = [c for c in M.columns if str(c).startswith("s__")]; M["g"] = gmhi(M[sp].apply(pd.to_numeric, errors="coerce").fillna(0).T).values
key = {}
for c in ["Sample Accession or Sample ID", "Sample title (ENA/SRA)", "Sample title (Paper)", "Subject Id (If available)"]:
    for v, g in zip(M[c].astype(str).str.strip(), M.g):
        if v != "nan": key.setdefault(v, g)
R = pd.read_csv(os.path.join(OUT, "gmhi_rows.csv.gz")); R["dev_g"] = [key.get(str(s), np.nan) for s in R.sample_id]
q = R.dropna(subset=["dev_g"]); qc = q.assign(a=q.gmhi - q.groupby("study").gmhi.transform("mean"), b=q.dev_g - q.groupby("study").dev_g.transform("mean"))
res = dict(n_overlap=int(len(q)), studies=int(q.study.nunique()), pearson=float(np.corrcoef(q.gmhi, q.dev_g)[0, 1]),
           within_study_pearson=float(np.corrcoef(qc.a, qc.b)[0, 1]), flag_dev_profiles=float((q.dev_g < 0).mean()), flag_cmd_profiles=float((q.gmhi < 0).mean()))
res["Q2_pass"] = res["pearson"] >= 0.80
g = q.groupby("study").agg(n=("gmhi", "size"), flag_dev=("dev_g", lambda v: float((v < 0).mean())), flag_cmd=("gmhi", lambda v: float((v < 0).mean())), country=("country", "first")).reset_index()
g = g[g.n >= 20]; g["shift"] = g.flag_cmd - g.flag_dev; g.to_csv(os.path.join(OUT, "gmhi_profiler_shift_perstudy.csv"), index=False)
res["shift_studies"] = int(len(g)); res["shift_range"] = [float(g["shift"].min()), float(g["shift"].max())]
res["rank_spearman_dev_vs_cmd"] = float(stats.spearmanr(g.flag_dev, g.flag_cmd)[0])
S = R[R.strict_person & R.strict_study]
P = S.groupby("study").agg(n=("flag", "size"), seen=("dev_g", lambda v: bool(v.notna().any())), ties=("tie", "sum")).reset_index(); P = P[P.n >= 20]
res["strict_pops"] = int(len(P)); res["strict_unseen_corrected"] = int((~P.seen).sum()); res["strict_ties_total"] = int(P.ties.sum())
res["ties_top"] = P.sort_values("ties", ascending=False).head(4)[["study", "ties", "n"]].values.tolist()
json.dump(res, open(os.path.join(OUT, "posthoc_gmhi_matching.json"), "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str))
