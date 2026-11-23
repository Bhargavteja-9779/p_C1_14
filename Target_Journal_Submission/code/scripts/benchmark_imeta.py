"""Helper for iMeta journal benchmark: fetch PubMed records, screen, fetch Europe PMC full text, extract metrics.
Open APIs only (NCBI E-utilities, Europe PMC REST, Crossref)."""
import json, re, sys, time, os, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
OUT = os.environ.get("BENCH_DIR", "/tmp/claude-0/bench")
UA = {"User-Agent": "imeta-benchmark-script/0.1 (python urllib)"}

def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:
            time.sleep(2 + 2 * i); err = e
    raise err

def pubmed_ids():
    q = urllib.parse.quote('"Imeta"[ta] AND 2024:2026[dp]')
    j = json.loads(get(f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={q}&retmax=5000&retmode=json"))
    return j["esearchresult"]["idlist"]

def pubmed_fetch(ids):
    recs = []
    for i in range(0, len(ids), 150):
        x = get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=" + ",".join(ids[i:i+150]))
        root = ET.fromstring(x)
        for a in root.findall(".//PubmedArticle"):
            g = lambda p: "".join(a.find(p).itertext()) if a.find(p) is not None else ""
            ab = " ".join((("[" + e.get("Label") + "] ") if e.get("Label") else "") + "".join(e.itertext()) for e in a.findall(".//Abstract/AbstractText"))
            ids_ = {e.get("IdType"): e.text for e in a.findall(".//PubmedData/ArticleIdList/ArticleId")}
            recs.append(dict(pmid=g(".//PMID"), title=g(".//ArticleTitle"), abstract=ab,
                             year=g(".//JournalIssue/PubDate/Year") or g(".//ArticleDate/Year"),
                             pubtypes=[e.text for e in a.findall(".//PublicationType")],
                             doi=ids_.get("doi", ""), pmcid=ids_.get("pmc", "")))
        time.sleep(0.4)
    return recs

def fulltext(pmcid):
    p = f"{OUT}/xml/{pmcid}.xml"
    if os.path.exists(p) and os.path.getsize(p) > 1000:
        return open(p, "rb").read()
    x = get(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML")
    os.makedirs(f"{OUT}/xml", exist_ok=True); open(p, "wb").write(x); time.sleep(0.3)
    return x

def crossref(doi):
    j = json.loads(get("https://api.crossref.org/works/" + urllib.parse.quote(doi)))
    return {a.get("name"): a.get("value") for a in j["message"].get("assertion", [])}

def metrics(xml):
    root = ET.fromstring(xml)
    body = root.find(".//body")
    # body text excluding figure/table captions
    def txt(e, skip=("fig", "table-wrap", "supplementary-material")):
        s = (e.text or "") if e.tag not in skip else ""
        for c in e:
            if c.tag not in skip: s += txt(c, skip)
            s += c.tail or ""
        return s
    btxt = txt(body) if body is not None else ""
    secs = [ "".join(s.find("title").itertext()) for s in body.findall("sec") if s.find("title") is not None] if body is not None else []
    figs = root.findall(".//body//fig") or root.findall(".//fig")
    das = ""
    for s in root.iter("sec"):
        t = s.find("title")
        if t is not None and re.search(r"data availab|code availab", "".join(t.itertext()), re.I):
            das += " ".join(s.itertext())
    for n in root.iter("notes"):
        if re.search(r"availab", " ".join(n.itertext())[:200], re.I): das += " " + " ".join(n.itertext())
    abst = root.find(".//front//abstract")
    return dict(words=len(btxt.split()), sections=secs, n_fig=len([f for f in figs if not re.search(r"graphical|toc", (f.get("id") or ""), re.I)]),
                n_tab=len(root.findall(".//body//table-wrap")), n_ref=len(root.findall(".//ref-list/ref")),
                das=re.sub(r"\s+", " ", das)[:1500], urls=sorted(set(re.findall(r"https?://(?:github|gitee|zenodo|figshare|gitlab)[^\s\"<>)\]]+", " ".join(root.itertext())))),
                abstracts=[(a.get("abstract-type") or "main", re.sub(r"\s+", " ", " ".join(a.itertext()))[:300]) for a in root.findall(".//front//abstract")],
                body=btxt)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "pubmed":
        r = pubmed_fetch(pubmed_ids()); json.dump(r, open(f"{OUT}/pubmed.json", "w"), indent=1); print(len(r))
    elif cmd == "ft":
        for pm in sys.argv[2:]:
            m = metrics(fulltext(pm)); body = m.pop("body")
            open(f"{OUT}/xml/{pm}.body.txt", "w").write(body)
            print(pm, json.dumps(m, ensure_ascii=False))
    elif cmd == "crossref":
        print(crossref(sys.argv[2]))

BACK = re.compile(r"author contrib|conflict of interest|ethics|acknowledg|supporting information|data availab|code availab|^references|associated data|contributor information|ai statement|funding|declaration|consent", re.I)

def metrics2(xml):
    """Main-text word count (approximate): body text, excluding figure/table captions and back-matter sections."""
    root = ET.fromstring(xml)
    body = root.find(".//body")
    def txt(e):
        s = e.text or ""
        for c in e:
            if c.tag not in ("fig", "table-wrap", "supplementary-material"):
                s += txt(c)
            s += c.tail or ""
        return s
    words, secs, sub = 0, [], {}
    if body is not None:
        # text directly in body (before first sec) = intro paragraphs
        for c in body:
            t = "".join(c.find("title").itertext()).strip() if c.tag == "sec" and c.find("title") is not None else ""
            if c.tag == "sec":
                secs.append(t)
                sub[t] = ["".join(s.find("title").itertext()).strip() for s in c.findall("sec") if s.find("title") is not None]
            if c.tag == "sec" and BACK.search(t):
                continue
            if c.tag in ("fig", "table-wrap", "supplementary-material"):
                continue
            words += len(txt(c).split())
    kw = [ "".join(k.itertext()) for k in root.findall(".//kwd")]
    abst = [(a.get("abstract-type") or "main", [ "".join(t.itertext()) for t in a.findall(".//title")], len(" ".join(a.itertext()).split())) for a in root.findall(".//front//abstract")]
    hist = {d.get("date-type"): "-".join(filter(None, [ (d.findtext("year") or ""), (d.findtext("month") or ""), (d.findtext("day") or "")])) for d in root.findall(".//front//history/date")}
    caps = [re.sub(r"\s+", " ", " ".join(f.find("caption").itertext()))[:160] for f in root.findall(".//fig") if f.find("caption") is not None]
    return dict(main_words=words, top_sections=secs, subsections=sub, keywords=kw, abstracts=abst, history=hist, fig_captions=caps,
                n_fig=len(root.findall(".//body//fig")), n_tab=len(root.findall(".//body//table-wrap")), n_ref=len(root.findall(".//ref-list/ref")))

if __name__ == "__main__" and sys.argv[1] == "ft2":
    for pm in sys.argv[2:]:
        print(pm, json.dumps(metrics2(fulltext(pm)), ensure_ascii=False))
