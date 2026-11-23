"""Verify candidate references against Crossref by DOI (metadata printed for manual check)."""
import json, sys, urllib.request, time
dois = [l.split("#")[0].strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
out = []
for d in dois:
    try:
        m = json.load(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works/" + d, headers={"User-Agent": "refcheck/0.1"})))["message"]
        au = m.get("author", [{}]); first = au[0].get("family", au[0].get("name", "")) if au else ""
        yr = (m.get("published-print") or m.get("published-online") or m.get("issued"))["date-parts"][0][0]
        out.append(dict(doi=d, ok=True, first=first, n_auth=len(au), year=yr, title=(m.get("title") or [""])[0],
                        venue=(m.get("container-title") or [""])[0], vol=m.get("volume"), page=m.get("page") or m.get("article-number")))
    except Exception as e:
        out.append(dict(doi=d, ok=False, err=str(e)))
    time.sleep(0.2)
json.dump(out, open(sys.argv[2], "w"), indent=1)
for o in out: print(o.get("ok"), o["doi"], o.get("first"), o.get("year"), o.get("venue"), "|", (o.get("title") or o.get("err"))[:110])
