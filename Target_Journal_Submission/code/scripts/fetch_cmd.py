"""Download curatedMetagenomicData (2021-03-31 release, MetaPhlAn3) relative-abundance matrices from ExperimentHub."""
import sqlite3, sys, os, urllib.request, pyreadr
studies = sys.argv[1].split(","); MISSING = []
c = sqlite3.connect(os.environ.get("EH_SQLITE", "/tmp/eh/experimenthub.sqlite3"))
os.makedirs("ra", exist_ok=True)
for s in studies:
    t = s if s.startswith("20") else f"2021-03-31.{s}.relative_abundance"
    r = c.execute("select rp.id, rp.rdatapath from resources r join rdatapaths rp on rp.resource_id=r.id where r.title=?", (t,)).fetchone()
    if r is None: print("MISSING", s); MISSING.append(s); continue
    out = f"ra/{s.split(".")[1] if s.startswith("20") else s}.csv"
    if os.path.exists(out): continue
    urllib.request.urlretrieve(f"https://experimenthub.bioconductor.org/fetch/{r[0]}", "tmp.rda")
    m = list(pyreadr.read_r("tmp.rda").values())[0]
    m.to_csv(out); print(s, m.shape, flush=True)
KNOWN = {"BedarfJR_2017", "PehrssonE_2016", "MetaCardis_2020_a"}  # absent from the 2021-03-31 release (MetaCardis fetched from 2022-10-19)
if set(MISSING) - KNOWN: sys.exit(f"unexpected missing studies: {set(MISSING) - KNOWN}")
