"""Measure received->accepted days from PubMed <History> dates (PubStatus received/accepted).
Random sample of journal articles with publication date in window. Appends to CSV."""
import sys, json, random, time, urllib.request, urllib.parse, csv, statistics, datetime as dt
import xml.etree.ElementTree as ET
E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r: return r.read()
        except Exception: time.sleep(2 + 2*i)
    return b""
def sample_ids(journal_term, n, seed=0):
    term = f'{journal_term} AND ("2025/06/01"[dp] : "2026/11/22"[dp]) AND journal article[pt] NOT review[pt] NOT editorial[pt] NOT erratum[pt] NOT letter[pt] NOT comment[pt] NOT "systematic review"[pt] NOT "meta-analysis"[pt] NOT "practice guideline"[pt] NOT "consensus development conference"[pt]'
    x = ET.fromstring(get(E + "esearch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "term": term, "retmax": 5000})))
    ids = [i.text for i in x.findall(".//Id")]
    random.Random(seed).shuffle(ids); return ids[:n], len(ids)
def dates(ids):
    out = []
    for k in range(0, len(ids), 100):
        x = ET.fromstring(get(E + "efetch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids[k:k+100]), "retmode": "xml"})))
        for art in x.findall(".//PubmedArticle"):
            h = {}
            for d in art.findall(".//History/PubMedPubDate"):
                try: h[d.get("PubStatus")] = dt.date(int(d.findtext("Year")), int(d.findtext("Month")), int(d.findtext("Day")))
                except Exception: pass
            if "received" in h and "accepted" in h and h["accepted"] >= h["received"]:
                doi = next((a.text for a in art.findall(".//ArticleId") if a.get("IdType") == "doi"), "")
                out.append(dict(title=(art.findtext(".//ArticleTitle") or "")[:200], doi=doi, received=h["received"].isoformat(),
                                accepted=h["accepted"].isoformat(), days=(h["accepted"] - h["received"]).days))
        time.sleep(0.4)
    return out
if __name__ == "__main__":
    cands = json.loads(sys.argv[1]); outcsv = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 120
    rows = []
    for name, term in cands.items():
        ids, tot = sample_ids(term, n); rs = dates(ids)
        for r in rs: r["journal"] = name
        rows += rs; ds = sorted(r["days"] for r in rs)
        if ds:
            print(f"{name:45s} pool={tot:5d} n={len(ds):3d} median={statistics.median(ds):6.1f} p75={ds[int(round(0.75*(len(ds)-1)))]:4d} max={ds[-1]:4d}", flush=True)
        else: print(f"{name:45s} pool={tot} no dates", flush=True)
    with open(outcsv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["journal","title","doi","received","accepted","days"]); w.writeheader(); w.writerows(rows)
