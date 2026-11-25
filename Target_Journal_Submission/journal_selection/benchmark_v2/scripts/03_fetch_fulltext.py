"""For each candidate DOI: Europe PMC metadata + fullTextXML; parse structure stats. Downloaded XML is data only."""
import json, re, sys, time, os, requests
import xml.etree.ElementTree as ET
cands = [l.strip() for l in open(sys.argv[1]) if l.strip()]
rawdir = sys.argv[2]; out = sys.argv[3]
oa = {w["doi"]: w for w in json.load(open(sys.argv[4]))}
os.makedirs(rawdir, exist_ok=True)
E = "https://www.ebi.ac.uk/europepmc/webservices/rest"
def txt(el): return " ".join("".join(el.itertext()).split()) if el is not None else ""
res = []
for c in cands:
    doi = "10.1002/" + c
    rec = {"doi": doi, "title": oa.get(doi, {}).get("title"), "year": oa.get(doi, {}).get("year"),
           "cited_by_openalex": oa.get(doi, {}).get("cited_by"), "abstract_openalex": oa.get(doi, {}).get("abstract")}
    hits = []
    for attempt in range(5):
        try:
            r = requests.get(E + "/search", params={"query": f'DOI:"{doi}"', "format": "json", "resultType": "core"}, timeout=60)
            hits = r.json().get("resultList", {}).get("result", []); break
        except Exception as e:
            print("retry", c, r.status_code, file=sys.stderr); time.sleep(3)
    if hits:
        h = hits[0]
        rec.update(pmid=h.get("pmid"), pmcid=h.get("pmcid"), epmc_pubtypes=h.get("pubTypeList", {}).get("pubType"),
                   epmc_abstract=re.sub("<[^>]+>", " ", h.get("abstractText") or ""))
    xml_path = os.path.join(rawdir, c + ".xml")
    if rec.get("pmcid") and not os.path.exists(xml_path):
        x = requests.get(f"{E}/{rec['pmcid']}/fullTextXML", timeout=90)
        if x.status_code == 200 and x.text.startswith("<"):
            open(xml_path, "w").write(x.text)
        time.sleep(0.3)
    if os.path.exists(xml_path):
        root = ET.parse(xml_path).getroot()
        rec["jats_article_type"] = root.get("article-type")
        cats = [txt(s) for s in root.iter("subject")]
        rec["subjects"] = cats
        body = root.find(".//body")
        figs = [f for f in body.iter("fig")] if body is not None else []
        caps = [txt(f.find("caption")) for f in figs]
        rec["n_main_figs"] = len(figs)
        rec["fig_captions"] = caps
        rec["n_panels_est"] = [len(set(re.findall(r"\(([A-Z])\)", cp))) or len(set(re.findall(r"\b([A-Z])\)", cp))) for cp in caps]
        rec["n_tables"] = len(list(body.iter("table-wrap"))) if body is not None else 0
        # body words excluding figure captions/tables
        if body is not None:
            for f in list(body.iter()):
                for ch in list(f):
                    if ch.tag in ("fig", "table-wrap"): f.remove(ch)
            rec["body_words"] = len(txt(body).split())
            rec["sections"] = [txt(s.find("title")) for s in body.findall("sec")]
            rec["subsections"] = [[txt(ss.find("title")) for ss in s.findall("sec")] for s in body.findall("sec")]
            rec["body_text"] = txt(body)
        rec["n_refs"] = len(list(root.iter("ref")))
        back = root.find(".//back"); bt = txt(back) if back is not None else ""
        rec["urls"] = sorted(set(re.findall(r"https?://[^\s,;)]+", txt(root))))[:40]
        rec["abstract_jats"] = txt(root.find(".//abstract"))
        hist = {}
        for d in root.iter("date"):
            hist[d.get("date-type")] = "-".join(txt(d.find(k)) for k in ("year", "month", "day"))
        rec["history"] = hist
    res.append(rec); time.sleep(0.2)
    print(c, rec.get("pmcid"), rec.get("jats_article_type"), rec.get("n_main_figs"), rec.get("body_words"), flush=True)
json.dump(res, open(out, "w"), indent=1)
