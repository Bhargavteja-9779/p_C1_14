"""POST HOC (review round 15, novelty M2): how independent is the GMHI replication of the GMWI2 finding?
Counts the GMHI healthy training samples (BioSample accessions) that are also GMWI2 training samples, per study, and
repeats H2 on GMHI studies whose samples are not in GMWI2's training data."""
import os, json, numpy as np, pandas as pd
from scipy import stats
H = os.path.dirname(os.path.abspath(__file__))
M = pd.read_csv(os.path.join(H, "inputs", "Final_metadata_4347.csv.gz"), header=None, index_col=0, low_memory=False).T
S2 = pd.read_csv(os.path.join(H, "..", "v6", "inputs", "gmwi2_SData2_training_samples.csv.gz"))
gw = set(S2["Sample accession"].astype(str)) | set(S2["RunID"].astype(str))
M = M[M.Phenotype == "Healthy"]; M["in_gmwi2"] = M["Sample Accession or Sample ID"].astype(str).str.strip().isin(gw)
M["study_no"] = M["Study No. (From VG sheet (V-*) from SB sheet (S-*))"]
st = pd.read_csv(os.path.join(H, "results", "gmhi_dev_perstudy.csv"))
ov = M.groupby("study_no").in_gmwi2.mean().rename("share_in_gmwi2"); st = st.merge(ov, left_on="study_no", right_index=True, how="left")
ind = st[st.share_in_gmwi2 < 0.5]
e, o = ind[ind.ea].fpr, ind[~ind.ea].fpr
res = dict(healthy_samples=int(len(M)), share_samples_in_gmwi2=float(M.in_gmwi2.mean()), studies=int(len(st)),
           studies_mostly_in_gmwi2=int((st.share_in_gmwi2 >= 0.5).sum()), independent_studies=int(len(ind)), independent_ea=int(len(e)), independent_other=int(len(o)),
           independent_median_ea=float(e.median()) if len(e) else None, independent_median_other=float(o.median()) if len(o) else None,
           independent_p_one_sided=float(stats.mannwhitneyu(e, o, alternative="greater").pvalue) if len(e) >= 2 and len(o) >= 2 else None)
st.to_csv(os.path.join(H, "results", "gmhi_dev_perstudy_overlap.csv"), index=False)
json.dump(res, open(os.path.join(H, "results", "posthoc_gmhi_gmwi2_overlap.json"), "w"), indent=1); print(json.dumps(res, indent=1))
print(st[["study_no", "author", "ea", "fpr", "share_in_gmwi2"]].to_string())
