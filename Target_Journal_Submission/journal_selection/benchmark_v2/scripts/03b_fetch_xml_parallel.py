"""Parallel fetch of Europe PMC fullTextXML for candidates (PMCID from OpenAlex); plus Europe PMC pubType. Data only."""
import json, sys, os, time, requests
from concurrent.futures import ThreadPoolExecutor
cands = [l.strip() for l in open(sys.argv[1]) if l.strip()]
rawdir = sys.argv[2]; oa = {w["doi"]: w for w in json.load(open(sys.argv[3]))}; meta_out = sys.argv[4]
E = "https://www.ebi.ac.uk/europepmc/webservices/rest"
def get(url, **kw):
    for a in range(6):
        try:
            r = requests.get(url, timeout=60, **kw)
            if r.status_code == 200: return r
        except Exception: pass
        time.sleep(2 + 3 * a)
    return None
def work(c):
    w = oa["10.1002/" + c]; pmc = (w.get("pmcid") or "").rsplit("/", 1)[-1]
    if pmc and not pmc.upper().startswith("PMC"): pmc = "PMC" + pmc
    m = {"key": c, "pmcid": pmc or None}
    r = get(E + "/search", params={"query": f'DOI:"10.1002/{c}"', "format": "json", "resultType": "core"})
    if r is not None:
        h = (r.json().get("resultList", {}).get("result") or [{}])[0]
        m.update(pmid=h.get("pmid"), pmcid=h.get("pmcid") or m["pmcid"], pubtypes=h.get("pubTypeList", {}).get("pubType"))
    p = os.path.join(rawdir, c + ".xml")
    if m["pmcid"] and not os.path.exists(p):
        x = get(f"{E}/{m['pmcid']}/fullTextXML")
        if x is not None and x.text.lstrip().startswith("<"): open(p, "w").write(x.text)
    m["has_xml"] = os.path.exists(p); print(c, m["pmcid"], m["has_xml"], flush=True); return m
with ThreadPoolExecutor(6) as ex: res = list(ex.map(work, cands))
json.dump(res, open(meta_out, "w"), indent=1)
