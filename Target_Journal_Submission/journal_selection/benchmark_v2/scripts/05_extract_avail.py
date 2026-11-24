"""Extract data-availability text and scale-related sentences (countries/cohorts/samples) from JATS XML. Data only."""
import json, re, sys, os
import xml.etree.ElementTree as ET
def txt(e): return " ".join("".join(e.itertext()).split()) if e is not None else ""
out = {}
for fn in sorted(os.listdir(sys.argv[1])):
    root = ET.parse(os.path.join(sys.argv[1], fn)).getroot()
    da = ""
    for s in root.iter("sec"):
        if re.match(r"DATA AVAILABILITY", txt(s.find("title")), re.I): da = txt(s)
    body = txt(root.find(".//body"))
    sents = re.split(r"(?<=[.!?])\s+", body)
    scale = [x for x in sents if re.search(r"\b\d[\d,]*\s+(countries|cohorts|datasets|data sets|studies|samples|metagenomes|participants|individuals|subjects|cities|provinces|regions)\b", x, re.I)]
    lim = [x for x in sents if re.search(r"limitation|caveat|should be interpreted|future studies|cannot exclude|may not generali", x, re.I)]
    out[fn[:-4]] = {"data_availability": da[:1500], "scale_sents": scale[:12], "limitation_sents": lim[:8]}
json.dump(out, open(sys.argv[2], "w"), indent=1)
