"""Verify each DOI resolves in Crossref; record title, container, type, issued date."""
import json, sys, time, requests
dois = [l.strip() for l in open(sys.argv[1]) if l.strip()]
out = []
for d in dois:
    for a in range(4):
        try:
            r = requests.get("https://api.crossref.org/works/10.1002/" + d, timeout=30)
            if r.status_code == 200: break
        except Exception: pass
        time.sleep(3)
    m = r.json()["message"] if r.status_code == 200 else {}
    out.append({"doi": "10.1002/" + d, "crossref_ok": bool(m), "title": (m.get("title") or [""])[0],
                "container": (m.get("container-title") or [""])[0], "issued": m.get("issued", {}).get("date-parts", [[None]])[0],
                "crossref_citations": m.get("is-referenced-by-count")})
    print(out[-1]["doi"], out[-1]["crossref_ok"], out[-1]["container"], out[-1]["issued"])
    time.sleep(0.2)
json.dump(out, open(sys.argv[2], "w"), indent=1)
