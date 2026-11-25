import json, sys, statistics, concurrent.futures as cf
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from acceptance_times import rows_for
src = json.load(open("oa_sources.json"))
todo = {k: v for k, v in src.items() if v["pub"] not in ("Elsevier", "IEEE", "ACM")}
res = {}
def work(issn):
    rs = rows_for(issn, todo[issn]["name"], 40)
    ds = sorted(r["days"] for r in rs)
    return issn, ds
with cf.ThreadPoolExecutor(8) as ex:
    for issn, ds in ex.map(work, list(todo)):
        if len(ds) >= 15:
            res[issn] = dict(todo[issn], n=len(ds), median=statistics.median(ds), p75=ds[int(round(.75*(len(ds)-1)))])
json.dump(res, open("screen.json", "w"))
fast = sorted((v for v in res.values() if v["median"] <= 75), key=lambda v: v["p75"])
print(len(todo), "screened;", len(res), "with dates;", len(fast), "median<=75")
for v in fast: print(f'{v["name"][:60]:60s} {v["pub"]:16s} cit={v["cit"]:5.1f} n={v["n"]:2d} med={v["median"]:5.1f} p75={v["p75"]}')
