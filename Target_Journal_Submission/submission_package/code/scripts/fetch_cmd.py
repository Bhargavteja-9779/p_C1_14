"""Download curatedMetagenomicData relative-abundance matrices from ExperimentHub.
Usage (inside the data cache directory):
  curl -L -o eh.sqlite3 https://experimenthub.bioconductor.org/metadata/experimenthub.sqlite3
  python3 fetch_cmd.py FengQ_2015,ZellerG_2014,...      (2021-03-31 release)
  python3 fetch_cmd.py 2022-10-19.MetaCardis_2020_a.relative_abundance"""
import sqlite3, sys, os, urllib.request, pyreadr
studies = sys.argv[1].split(",")
c = sqlite3.connect(os.environ.get("EH_SQLITE", "eh.sqlite3"))
os.makedirs("ra", exist_ok=True)
for s in studies:
    t = s if s.startswith("20") else f"2021-03-31.{s}.relative_abundance"
    r = c.execute("select rp.id, rp.rdatapath from resources r join rdatapaths rp on rp.resource_id=r.id where r.title=?", (t,)).fetchone()
    if r is None: print("MISSING", s); continue
    out = f"ra/{s.split('.')[1] if s.startswith('20') else s}.csv"
    if os.path.exists(out): continue
    urllib.request.urlretrieve(f"https://experimenthub.bioconductor.org/fetch/{r[0]}", "tmp.rda")
    m = list(pyreadr.read_r("tmp.rda").values())[0]
    m.to_csv(out); print(s, m.shape, flush=True)
