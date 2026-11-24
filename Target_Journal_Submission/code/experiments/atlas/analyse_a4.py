"""A4: between-cohort variance of control scores before/after individual covariates (linear mixed model on logit score),
plus GLMM-style latent ICC approximation for flags. Also cohort-level covariate R^2 (post hoc, descriptive)."""
import numpy as np, pandas as pd, statsmodels.formula.api as smf, warnings; warnings.filterwarnings("ignore")
r = pd.read_csv("results/atlas_rows.csv.gz"); C = pd.read_csv("results/atlas_covars.csv.gz").set_index("sample_id")
r = r[~r.study.str.startswith("TRAIN")].join(C, on="sample_id")
r["logdepth"] = np.log10(r.number_reads); r["male"] = (r.gender == "male").astype(float)
out = []
for (d, m), g in r.groupby(["disease", "model"]):
    g = g.dropna(subset=["age", "BMI", "gender"]); g = g[g.groupby("study").study.transform("size") >= 10]
    g = g.assign(z=(g.score - g.score.mean()) / g.score.std())
    f0 = smf.mixedlm("z ~ 1", g, groups=g.study).fit(); f1 = smf.mixedlm("z ~ age + male + BMI + logdepth + shannon + richness", g, groups=g.study).fit()
    icc = lambda f: float(f.cov_re.iloc[0, 0] / (f.cov_re.iloc[0, 0] + f.scale))
    out.append(dict(disease=d, model=m, n=len(g), cohorts=g.study.nunique(), icc_raw=icc(f0), icc_adj=icc(f1),
                    between_var_reduction=1 - f1.cov_re.iloc[0, 0] / f0.cov_re.iloc[0, 0],
                    **{f"b_{k}": f1.params[k] for k in ["age", "male", "BMI", "logdepth", "shannon", "richness"]},
                    **{f"p_{k}": f1.pvalues[k] for k in ["age", "male", "BMI", "logdepth", "shannon", "richness"]}))
o = pd.DataFrame(out); o.to_csv("results/a4_icc.csv", index=False); print(o.round(3).T.to_string())
