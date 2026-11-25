"""Re-parse Europe PMC JATS XML: main-text words (stop at back-matter headings), figures, panels, headings."""
import json, re, sys, os
import xml.etree.ElementTree as ET
BACK = re.compile(r"^(AUTHOR CONTRIBUTION|ACKNOWLEDG|CONFLICT|FUNDING|ETHICS|AI STATEMENT|DATA AVAILABILITY|SUPPORTING INFORMATION|Supporting information|REFERENCES|Contributor|Associated Data)", re.I)
def txt(e): return " ".join("".join(e.itertext()).split()) if e is not None else ""
def parse(path):
    root = ET.parse(path).getroot()
    body = root.find(".//body")
    figs, caps = [], []
    for f in root.iter("fig"):
        lab = txt(f.find("label")); cap = txt(f.find("caption"))
        figs.append(lab); caps.append(cap)
    # strip figs/tables for word count
    for el in list(root.iter()):
        for ch in list(el):
            if ch.tag in ("fig", "table-wrap", "supplementary-material"): el.remove(ch)
    words = 0; heads = []; methods_words = 0
    to_editor = "to the editor" in txt(body)[:3000].lower()
    for s in list(body):
        t = txt(s.find("title")) if s.tag == "sec" else ""
        if t and BACK.match(t): continue
        if not t and re.search(r"fund|grant|foundation|supported by|program of china", txt(s), re.I): continue
        w = len(txt(s).split()) - len(t.split())
        if re.match(r"(MATERIALS AND )?METHODS|EXPERIMENTAL PROCEDURES", t, re.I): methods_words += w
        words += w
        if s.tag == "sec": heads.append((t, [txt(ss.find("title")) for ss in s.findall("sec")]))
    main = [(l, c) for l, c in zip(figs, caps) if re.match(r"^(Figure|FIGURE|Fig)\s*\d+$", l.strip())]
    panels = []
    for l, c in main:
        letters = set()
        for grp in re.findall(r"\(([A-Z](?:\s*[,–-]\s*[A-Z])*)\)", c):
            for a, b in re.findall(r"([A-Z])\s*[–-]\s*([A-Z])", grp):
                letters |= {chr(x) for x in range(ord(a), ord(b) + 1)}
            letters |= set(re.findall(r"[A-Z]", grp))
        letters |= set(re.findall(r"^([A-Z])\)|[.;]\s([A-Z])\)\s", c) and [])
        panels.append(max([ord(x) - 64 for x in letters], default=0))
    abs_ = txt(root.find(".//abstract"))
    kw = [txt(k) for k in root.iter("kwd")]
    refs = len(list(root.iter("ref")))
    hist = {d.get("date-type"): "-".join(txt(d.find(k)) for k in ("year", "month", "day")) for d in root.iter("date")}
    subj = [txt(s) for s in root.iter("subject")]
    return dict(jats_type=root.get("article-type"), to_editor=to_editor, subjects=subj, main_words=words, methods_words=methods_words,
                headings=heads, n_main_figs=len(main), fig_labels=[l for l, _ in main], panels=panels,
                captions=[c for _, c in main], other_figs=[l for l in figs if not re.match(r"^(Figure|FIGURE|Fig)\s*\d+$", l.strip())],
                n_refs=refs, history=hist, abstract=abs_, keywords=kw)
out = {}
for fn in sorted(os.listdir(sys.argv[1])):
    if fn.endswith(".xml"):
        try: out[fn[:-4]] = parse(os.path.join(sys.argv[1], fn))
        except Exception as e: print("ERR", fn, e)
json.dump(out, open(sys.argv[2], "w"), indent=1)
for k, v in out.items():
    print(k, v["jats_type"], v["subjects"][:1], v["to_editor"], v["main_words"], v["methods_words"], v["n_main_figs"], v["panels"], v["n_refs"], v["other_figs"][:3])
