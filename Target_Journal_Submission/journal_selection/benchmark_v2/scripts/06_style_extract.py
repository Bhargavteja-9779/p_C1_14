"""Print style features for deep-read papers: headings, intro opening, limitations, caption keywords, abstract types, stats terms."""
import json, re, sys
import xml.etree.ElementTree as ET
P = json.load(open(sys.argv[2])); A = json.load(open(sys.argv[3]))
def txt(e): return " ".join("".join(e.itertext()).split()) if e is not None else ""
for k in sys.argv[4:]:
    root = ET.parse(f"{sys.argv[1]}/{k}.xml").getroot(); v = P[k]
    abs_types = [(a.get("abstract-type"), len(txt(a).split())) for a in root.iter("abstract")]
    body = txt(root.find(".//body"))
    print("=" * 10, k, v["jats_type"], "words", v["main_words"], "methods", v["methods_words"], "figs", v["n_main_figs"], "panels", v["panels"], "refs", v["n_refs"])
    print("abstracts:", abs_types)
    print("title:", txt(root.find(".//article-title")))
    for h, sub in v["headings"]: print("  H:", h[:120], "|", "; ".join(x[:90] for x in sub)[:600])
    i = body.lower().find("to the editor"); start = i if i >= 0 else 0
    print("OPEN:", body[start:start + 700])
    print("LIM:", " || ".join(x[:260] for x in A[k]["limitation_sents"][:5]))
    for j, c in enumerate(v["captions"]):
        kws = [w for w in ["schematic", "workflow", "overview", "flowchart", "map", "heatmap", "heat map", "forest", "ROC", "AUC", "PCoA", "network", "Sankey", "violin", "box", "study design", "geograph"] if re.search(r"\b" + w, c, re.I)]
        print(f"  Fig{j+1} [{v['panels'][j] or 1} panels] {c[:160]} -> {kws}")
    stats = {w: len(re.findall(w, body)) for w in ["95% CI", "FDR", "q <", "p <", "P <", "Wilcoxon", "PERMANOVA", "AUROC", "AUC", "random forest", "LASSO", "cross-validation", "leave-one", "meta-analysis", "SHAP", "permutation", "bootstrap", "Benjamini"]}
    print("STATS:", {a: b for a, b in stats.items() if b})
