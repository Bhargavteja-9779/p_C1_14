"""Table S1: cohorts, disease, country, sample counts after filtering, role."""
import os, sys, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.data import load, DISEASES, DEV_CRC
rows = []
for dis, cfg in DISEASES.items():
    X, y, g, M = load(dis)
    for s in cfg["studies"]:
        m = M[M.study == s]
        role = "development" if (dis == "CRC" and s in DEV_CRC) else "locked test"
        rows.append(dict(task=f"{cfg['case']} vs control", cohort=s, country=",".join(sorted(m.country.dropna().unique())),
                         controls=int((m.study_condition == "control").sum()), cases=int((m.study_condition == cfg["case"]).sum()), role=role))
t = pd.DataFrame(rows); out = os.path.join(os.path.dirname(__file__), "..", "..", "results", "table_s1_cohorts.csv")
os.makedirs(os.path.dirname(out), exist_ok=True); t.to_csv(out, index=False); print(t.to_string(index=False)); print("total samples", t.controls.sum() + t.cases.sum())
