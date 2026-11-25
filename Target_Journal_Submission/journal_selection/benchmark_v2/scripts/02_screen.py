"""Keyword relevance screen of iMeta 2024-2026 works (title+abstract)."""
import json, re, sys
d = json.load(open(sys.argv[1]))
groups = {
 "ml": r"machine learning|deep learning|random forest|classifier|neural network|artificial intelligence|\bAI\b|predictive model|prediction model|XGBoost|LASSO",
 "diag": r"diagnos|biomarker|signature|non-invasive|noninvasive|screening|discriminat|AUC|area under",
 "multicohort": r"cross-cohort|multi-cohort|multicohort|meta-analysis|independent cohorts|external validation|validation cohort|cohorts|across studies|multiple cohorts|pooled",
 "atlas": r"atlas|catalog|catalogue|resource|database|compendium|landscape|web server|webserver|platform|repository",
 "batch": r"batch effect|reproducib|confound|heterogeneity|standardi|benchmark|generaliz|transferab|robust",
 "geo": r"countr|geograph|population|ethnic|global|worldwide|regions|nationwide|urbaniz|industrializ|lifestyle",
 "gut": r"gut microbio|fecal|faecal|stool|intestinal microbio|metagenom|16S",
 "disease": r"colorectal|inflammatory bowel|crohn|ulcerative|type 2 diabetes|\bT2D\b|cancer|obesity|cirrhosis|disease",
}
out = []
for w in d:
    if w["type"] not in ("article",): continue
    t = (w["title"] or "") + " " + (w["abstract"] or "")
    hits = {g: len(re.findall(p, t, flags=re.I)) for g, p in groups.items()}
    score = sum(min(v, 3) for v in hits.values()) + 2*min(hits["ml"],2) + 2*min(hits["multicohort"],2) + 2*min(hits["geo"],1)
    out.append((score, w["cited_by"], w["doi"], w["year"], w["title"], hits))
out.sort(key=lambda x: -x[0])
json.dump([dict(score=o[0], cited=o[1], doi=o[2], year=o[3], title=o[4], hits=o[5]) for o in out], open(sys.argv[2], "w"), indent=1)
for o in out[:110]:
    print(o[0], o[1], o[2], o[3], (o[4] or "")[:110])
