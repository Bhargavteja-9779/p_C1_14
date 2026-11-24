"""Supporting Information tables S1-S4 (markdown)."""
import os, sys, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(H, ".."))
from src.data import load, DISEASES, DEV_CRC, LOCKED_CRC, CACHE
E = os.path.join(H, "..", "experiments"); R = os.path.join(E, "final", "results"); DV = os.path.join(E, "dev")
out = []
# S1 cohorts
meta = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False)
rows = []
for d in ["CRC", "IBD", "T2D", "adenoma"]:
    X, y, g, M = load(d)
    for s in DISEASES[d]["studies"]:
        role = ("Development" if s in DEV_CRC else "Locked test") if d == "CRC" else ("Locked test (partly independent)" if d == "adenoma" else "Locked test")
        rows.append(dict(Analysis=f"{d} vs control", Cohort=s, Cases=int(y[g == s].sum()), Controls=int((y[g == s] == 0).sum()), Role=role))
COM = {"JieZ_2017": "ACVD", "QinN_2014": "cirrhosis", "LiJ_2017": "hypertension, pre-hypertension", "LoombaR_2017": "fatty liver, cirrhosis",
       "NagySzakalD_2017": "ME/CFS", "XieH_2016": "asthma, migraine", "ZhuF_2020": "schizophrenia", "ChengpingW_2017": "ankylosing spondylitis",
       "LiJ_2014": "T2D, IBD, T1D", "VilaAV_2018": "IBD", "HMP_2019_t2d": "IGT, T2D"}
for c, cond in COM.items():
    q = meta[(meta.study_name == c) & (meta.body_site == "stool")].drop_duplicates("subject_id")
    rows.append(dict(Analysis="Comorbidity (other conditions)", Cohort=c, Cases=int((q.study_condition != "control").sum()),
                     Controls=int((q.study_condition == "control").sum()), Role=f"Development ({cond})"))
for c in ["MetaCardis_2020_a", "QinJ_2012", "KarlssonFH_2013", "NielsenHB_2014", "HallAB_2017", "IjazUZ_2017", "HMP_2019_ibdmdb"]:
    rows.append(dict(Analysis="Comorbidity (other conditions)", Cohort=c, Cases="see Table S3", Controls="see Table S3", Role="Locked test"))
out.append("## Table S1. Cohorts, sample sizes (one sample per subject) and roles\n\n" + pd.DataFrame(rows).to_markdown(index=False))
# S2 sensitivity analyses
S = pd.read_csv(os.path.join(R, "sequential.csv.gz")); S["over"] = S.fpr > S.alpha + 0.02; L = S[S.month >= 7]
t = L.groupby(["setting", "method"]).agg(FPR=("fpr", "mean"), P_over=("over", "mean"), Sens=("sens", "mean")).round(3)
t = t.unstack("method"); t.columns = [f"{a} {b}" for a, b in t.columns]
cols = [f"{m} {b}" for m in ["FPR", "P_over", "Sens"] for b in ["source", "local_q", "contam", "vp", "oracle"]]
out.append("## Table S2. Primary and pre-specified sensitivity analyses (locked sites, months 7-12 [7-18 for drift settings]; "
           "mean true FPR, share of site-months with FPR > alpha + 0.02, mean sensitivity). vp = verified-positive recalibration (proposed).\n\n"
           + t[[c for c in cols if c in t.columns]].reset_index().to_markdown(index=False))
d = S[S.setting == "primary"].groupby(["disease", "pi", "method"]).agg(FPR=("fpr", "mean")).round(3).unstack("method").reset_index()
d.columns = [c if isinstance(c, str) else (c[1] or c[0]) for c in d.columns]
out.append("### Table S2b. Primary setting by disease and prevalence (mean true FPR, months 7-12)\n\n" + d.to_markdown(index=False))
# S3 Part B
pB = pd.read_csv(os.path.join(R, "partB_positivity.csv")).round(3); aB = pd.read_csv(os.path.join(R, "partB_adjusted_holm.csv")).round(4)
pB["ratio (95% CI)"] = pB.apply(lambda r: f"{r.ratio:.2f} ({r.ratio_lo:.2f}-{min(r.ratio_hi, 999):.2f})" if r.pos_ctrl > 0 else "n/a (no control positives)", axis=1)
out.append("## Table S3. Locked comorbidity confirmation: CRC-test positivity vs the same cohort's controls\n\n" +
           pB[["model", "cohort", "condition", "n", "n_ctrl", "pos", "pos_ctrl", "ratio (95% CI)"]].to_markdown(index=False))
out.append("### Table S3b. Adjusted CRC-score difference (logit), one-sided p, Holm-adjusted within model\n\n" +
           aB[["model", "cohort", "condition", "covs", "n", "beta", "lo", "hi", "p_one_sided", "p_holm"]].to_markdown(index=False))
dv = pd.read_csv(os.path.join(DV, "explore_v7b_fits.csv")).round(3)
out.append("### Table S3c. Development cohorts: crude and adjusted CRC-score difference (LASSO)\n\n" + dv.to_markdown(index=False))
# S4 constrained signature
cs = pd.read_csv(os.path.join(DV, "explore_v9_constrained.csv")).round(3)
out.append("## Table S4. Specificity-constrained signatures (exploratory, development). K = minimum number of other conditions sharing a "
           "species' shift for it to be removed (None = full model).\n\n" +
           cs.groupby("K")[["n_drop", "crc_auc", "crc_sens_oof", "pos_dis", "pos_ctrl"]].mean().round(3).reset_index().to_markdown(index=False))
ct = pd.read_csv(os.path.join(DV, "explore_v9_contrib.csv"), index_col=0).sort_values("total", ascending=False).head(20).round(3)
out.append("### Table S4b. Top 20 species contributing to the CRC-score gap across seven development conditions\n\n" + ct.reset_index().rename(columns={"index": "species"}).to_markdown(index=False))
pC = pd.read_csv(os.path.join(R, "partC_groupcal.csv.gz")); q = pC[pC.month >= 7].assign(over=lambda x: x.fpr > 0.12)
tc = q.groupby(["model", "group", "method"]).agg(FPR=("fpr", "mean"), P_over=("over", "mean"), Sens_proxy=("sens_proxy", "mean")).round(3).reset_index()
out.append("## Table S5. Group-conditional recalibration at the locked MetaCardis site (months 7-18)\n\n" + tc.to_markdown(index=False))
AD = os.path.join(E, "addendum_results")
for f, title in [("dev_regression.csv", "Table S6a. Medication addendum, development check (PPI; direction only)"),
                 ("confirm_regression.csv", "Table S6b. Medication addendum, MetaCardis (pre-specified H5/H6; other drugs secondary)"),
                 ("confirm_positivity.csv", "Table S6c. Test positivity by PPI use, MetaCardis (overall and within condition group)"),
                 ("metformin_within_T2D.csv", "Table S6d. Exploratory: metformin users vs non-users within type 2 diabetes")]:
    out.append(f"## {title}\n\n" + pd.read_csv(os.path.join(AD, f)).round(4).to_markdown(index=False))
open(os.path.join(H, "..", "..", "manuscript", "SI_tables.md"), "w").write("# Supporting Information — Tables\n\n" + "\n\n".join(out) + "\n")
print("ok")
