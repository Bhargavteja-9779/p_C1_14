import json, sys, statistics, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from acceptance_times_pubmed import sample_ids, dates
src = json.load(open("oa_sources.json"))
todo = {k: v for k, v in src.items() if v["pub"] in ("Elsevier", "IEEE")}
res = {}
for issn, v in todo.items():
    try:
        ids, tot = sample_ids(f'"{issn}"[is]', 40)
        if tot < 30: continue
        ds = sorted(r["days"] for r in dates(ids))
    except Exception as e: continue
    if len(ds) >= 15:
        res[issn] = dict(v, n=len(ds), median=statistics.median(ds), p75=ds[int(round(.75*(len(ds)-1)))])
        if res[issn]["median"] <= 75: print(res[issn], flush=True)
    time.sleep(0.3)
json.dump(res, open("screen_pm.json", "w"))
print("DONE", len(todo), len(res))
