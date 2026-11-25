"""Fetch all iMeta works (OpenAlex source S4220650979) published 2024-2026 with abstracts."""
import json, sys, time, requests
OUT = sys.argv[1]
url = "https://api.openalex.org/works"
params = {"filter": "primary_location.source.id:S4220650979,from_publication_date:2024-01-01",
          "per-page": 200, "page": 1}
works = []
while True:
    r = requests.get(url, params=params, timeout=60); r.raise_for_status()
    d = r.json(); works += d["results"]
    if not d["results"] or len(works) >= d["meta"]["count"]: break
    params["page"] += 1; time.sleep(0.3)
def abstract(inv):
    if not inv: return ""
    pos = {}
    for w, ps in inv.items():
        for p in ps: pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))
slim = []
for w in works:
    slim.append({"openalex": w["id"], "doi": (w.get("doi") or "").replace("https://doi.org/", "").lower(),
                 "title": w.get("title"), "year": w.get("publication_year"), "date": w.get("publication_date"),
                 "type": w.get("type"), "cited_by": w.get("cited_by_count"),
                 "pmid": (w.get("ids") or {}).get("pmid"), "pmcid": (w.get("ids") or {}).get("pmcid"),
                 "abstract": abstract(w.get("abstract_inverted_index"))})
json.dump(slim, open(OUT, "w"), indent=1)
print(len(slim), "works")
