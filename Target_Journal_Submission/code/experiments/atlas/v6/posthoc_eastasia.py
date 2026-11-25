"""POST HOC (exploratory): East Asian vs other healthy studies under the published GMWI2 cut-off, (a) developers' own
published training scores, (b) our unseen cMD populations; taxon decomposition of the score gap on cMD profiles."""
import json, os, sys, numpy as np, pandas as pd
from scipy import stats
EA = {"China", "Japan", "South Korea", "Hong Kong", "Taiwan", "CHN", "JPN", "KOR"}
g = pd.read_csv("results/gmwi2_published_training_perstudy.csv"); g["ea"] = g.country.isin(EA)
out = dict(published_training=dict(ea_studies=int(g.ea.sum()), other_studies=int((~g.ea).sum()), ea_median=float(g[g.ea].fpr.median()), other_median=float(g[~g.ea].fpr.median()),
           ea_range=[float(g[g.ea].fpr.min()), float(g[g.ea].fpr.max())], other_range=[float(g[~g.ea].fpr.min()), float(g[~g.ea].fpr.max())],
           mw_p=float(stats.mannwhitneyu(g[g.ea].fpr, g[~g.ea].fpr, alternative="two-sided").pvalue),
           ea_people=int(g[g.ea].n.sum()), ea_flagged=int(g[g.ea].k.sum())))
R = pd.read_csv("results/gmwi2_rows.csv.gz"); META = pd.read_csv("/home/user/p_C1_14/data_cache/sampleMetadata.csv", low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
R["country"] = META.loc[R.sample_id, "country"].values; R["ea"] = R.country.isin(EA)
P = R.groupby("study").agg(n=("flag", "size"), fpr=("flag", "mean"), seen=("in_gmwi2_training", "any"), ea=("ea", "first"), country=("country", "first")).reset_index(); P = P[P.n >= 20]
U = P[~P.seen]
out["cmd_unseen"] = dict(ea=U[U.ea][["study", "country", "n", "fpr"]].values.tolist(), other_median=float(U[~U.ea].fpr.median()), ea_median=float(U[U.ea].fpr.median()) if U.ea.any() else None,
                         mw_p=float(stats.mannwhitneyu(U[U.ea].fpr, U[~U.ea].fpr, alternative="greater").pvalue) if U.ea.sum() >= 2 else None)
# taxon decomposition on cMD profiles (all healthy samples, seen+unseen): w_j * (presence_EA - presence_other)
J = json.load(open("gmwi2_coefficients.json")); F, W = J["features"], np.array(J["coef"]); pres = []
for s, x in R.groupby("study"):
    raw = pd.read_csv(f"/home/user/p_C1_14/data_cache/ra/{s}.csv", index_col=0)[list(x.sample_id)]
    pres.append(pd.DataFrame(((raw.reindex(F).fillna(0).values / 100) > 1e-5).T, index=x.sample_id, columns=F))
Pm = pd.concat(pres).loc[R.sample_id]; ea = R.ea.values
# population-balanced presence: mean over populations of within-population presence
pops = R.study.values
def balanced(mask):
    return pd.DataFrame(Pm.values[mask], index=pops[mask]).groupby(level=0).mean().mean(0).values
d = balanced(ea) - balanced(~ea); c = W * d
T = pd.DataFrame(dict(taxon=[f.split("|")[-1] for f in F], rank=[f.split("|")[-1][:1] for f in F], w=W, presence_ea=balanced(ea), presence_other=balanced(~ea), contrib=c)).sort_values("contrib")
T.to_csv("results/gmwi2_eastasia_taxa.csv", index=False)
out["decomposition"] = dict(score_gap_total=float(c.sum()), top_negative=T.head(10)[["taxon", "w", "presence_ea", "presence_other", "contrib"]].round(3).values.tolist(),
                            share_top5_of_negative=float(T.contrib.head(5).sum() / T.contrib[T.contrib < 0].sum()))
json.dump(out, open("results/gmwi2_eastasia.json", "w"), indent=1); print(json.dumps(out, indent=1))
