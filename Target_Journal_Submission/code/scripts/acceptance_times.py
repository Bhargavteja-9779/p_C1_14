"""Measure received->accepted days from Crossref 'assertion' metadata (Springer Nature deposits these).
Random sample of research articles published in a window. Writes per-article CSV + summary."""
import json, sys, time, urllib.request, urllib.parse, csv, statistics, datetime as dt
from dateutil import parser as dp

def fetch(issn, n=100, frm="2025-06-01", until="2026-11-22"):
    q = urllib.parse.urlencode({"filter": f"from-pub-date:{frm},until-pub-date:{until},type:journal-article",
                                "sample": n, "mailto": ""})
    url = f"https://api.crossref.org/journals/{issn}/works?{q}"
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)["message"]["items"]
        except Exception as e:
            time.sleep(3)
    return []

def rows_for(issn, name, n):
    out = []
    for it in fetch(issn, n):
        a = {x.get("name"): x.get("value") for x in it.get("assertion", [])}
        if "received" not in a or "accepted" not in a: continue
        try:
            r = dp.parse(a["received"]); c = dp.parse(a["accepted"])
        except Exception: continue
        d = (c - r).days
        if d < 0: continue
        out.append(dict(journal=name, issn=issn, title=(it.get("title") or [""])[0][:200], doi=it["DOI"],
                        received=r.date().isoformat(), accepted=c.date().isoformat(), days=d))
    return out

if __name__ == "__main__":
    cands = json.loads(sys.argv[1]); outcsv = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    allrows = []
    for name, issn in cands.items():
        rows = rows_for(issn, name, n); allrows += rows
        ds = sorted(r["days"] for r in rows)
        if ds:
            p75 = ds[int(round(0.75*(len(ds)-1)))]
            print(f"{name:55s} n={len(ds):3d} median={statistics.median(ds):6.1f} p75={p75:4d} max={ds[-1]:4d}", flush=True)
        else:
            print(f"{name:55s} no dates", flush=True)
    with open(outcsv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["journal","issn","title","doi","received","accepted","days"]); w.writeheader(); w.writerows(allrows)
