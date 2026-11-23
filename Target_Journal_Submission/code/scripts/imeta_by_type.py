"""Per-article received/accepted dates for iMeta from PubMed, labelled by PubMed publication type
(iMeta 'Letter' = Short Communication format). Window: articles with publication date 2025-06-01..2026-11-22."""
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, datetime as dt, csv, sys
E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
term = '"Imeta"[ta] AND ("2025/06/01"[dp] : "2026/11/22"[dp])'
ids = [i.text for i in ET.fromstring(urllib.request.urlopen(E + "esearch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "term": term, "retmax": 2000})).read()).findall(".//Id")]
rows = []
for k in range(0, len(ids), 150):
    x = ET.fromstring(urllib.request.urlopen(E + "efetch.fcgi?" + urllib.parse.urlencode({"db": "pubmed", "id": ",".join(ids[k:k+150]), "retmode": "xml"})).read())
    for a in x.findall(".//PubmedArticle"):
        pts = [p.text for p in a.findall(".//PublicationType")]
        typ = "Letter/ShortCommunication" if "Letter" in pts else "Review" if "Review" in pts else "Editorial" if "Editorial" in pts else "Erratum" if "Published Erratum" in pts else "ResearchArticle"
        h = {}
        for d in a.findall(".//History/PubMedPubDate"):
            try: h[d.get("PubStatus")] = dt.date(int(d.findtext("Year")), int(d.findtext("Month")), int(d.findtext("Day")))
            except Exception: pass
        if "received" in h and "accepted" in h:
            doi = next((i.text for i in a.findall(".//ArticleId") if i.get("IdType") == "doi"), "")
            rows.append(dict(journal="iMeta", article_type=typ, title="".join(a.find(".//ArticleTitle").itertext())[:200], doi=doi,
                             received=h["received"].isoformat(), accepted=h["accepted"].isoformat(), days=(h["accepted"] - h["received"]).days, source="PubMed History"))
with open(sys.argv[1], "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
