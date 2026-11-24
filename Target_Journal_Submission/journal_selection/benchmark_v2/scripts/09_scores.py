"""Write benchmark_scores.csv (judgement scores, 1-10, from retrieved abstract/full-text evidence) and per-dimension percentiles."""
import csv, statistics, sys
D = ["significance", "scale_breadth", "novelty", "rigor_statistics", "external_generalization", "resource_tool_value",
     "figure_visual_story", "clarity_framing", "reproducibility_openness", "actionable_insight_mechanism"]
S = {  # doi suffix: scores in order of D, evidence note
 "imt2.212":   ([7,5,6,6,8,3,7,8,5,6], "8 cohorts/5 countries/341 samples; RF+repeated CV, cohort-transfer matrix, LODO, case-only validation; accessions only, no code link"),
 "imt2.70123": ([8,6,7,7,7,3,7,7,5,7], "196 new metagenomes + 2 external anti-PD-1 cohorts; PERMANOVA, permutation, BH; clinical metadata restricted"),
 "imt2.70192": ([8,9,8,6,6,8,7,9,9,8], "2,896 studies/~720k samples; tier tool + curated data on GitHub; regression + bootstrap CI; policy call"),
 "imt2.70088": ([8,8,6,7,7,5,7,8,6,7], "6,423 women/18 provinces; FDR, PERMANOVA, GAM; score validated in 13 external datasets and prospectively"),
 "imt2.268":   ([7,8,7,8,7,3,6,6,7,5], "~7,000 people/14 regions; per-region networks + random-effects meta-analysis, heterogeneity, replication, FDR"),
 "imt2.169":   ([7,8,6,6,6,3,7,6,7,5], "4,132 metagenomes/19 cohorts/6 countries; uniform reprocessing; RF age model; map panel"),
 "imt2.70004": ([7,8,8,6,5,8,7,6,8,7], "161 diseases/32 fibres; new BHWA algorithm; mDiFiBank site + Code Ocean; mouse validation"),
 "imt2.70008": ([7,8,7,6,5,3,6,7,7,6], "1,605 stool + 1,035 environmental metagenomes; PERMANOVA/Wilcoxon/FDR; GSA + GitHub"),
 "imt2.70011": ([8,7,6,6,8,9,7,6,8,8], "1,242 ICB patients multi-cohort + in-house cohort; R package + web tool; CRISPR + CEP55 wet-lab"),
 "imt2.70079": ([8,6,6,8,5,2,7,7,5,6], "548 + 52 recovery cohort; q-values, confounder & mediation analysis, SHAP; single centre"),
 "imt2.183":   ([8,8,7,9,7,2,5,7,4,6], "7,834 people/5 cohorts; HR with 95% CI, GWAS, MR; data on request"),
 "imt2.70090": ([7,5,7,6,7,2,7,6,5,6], "185 tissues; 2 external datasets (AUROC 0.920/0.735 reported); multi-kingdom + proteomics"),
}
B = sys.argv[1]
with open(f"{B}/benchmark_scores.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["doi"] + D + ["total", "evidence"])
    for k, (sc, ev) in S.items(): w.writerow(["10.1002/" + k] + sc + [sum(sc), ev])
def pct(xs, q):  # linear interpolation (numpy default)
    xs = sorted(xs); i = (len(xs) - 1) * q; lo = int(i); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)
for j, d in enumerate(D):
    col = [v[0][j] for v in S.values()]
    print(f"{d}: median {pct(col,.5):.1f}  P75 {pct(col,.75):.2f}  max {max(col)}")
tot = [sum(v[0]) for v in S.values()]; print("total: median", pct(tot,.5), "P75", pct(tot,.75))
