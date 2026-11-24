"""POST HOC P9: clinical trade-off as net benefit per 1,000 screened, NB = cancers detected - w x false-positive referrals,
for exchange rates of 1 detected cancer per 20, 50, 100 false-positive colonoscopies (w = 1/20, 1/50, 1/100), at 1% prevalence,
12-month averages; locked CRC sites (pre-specified simulation) and all 11 CRC sites (post hoc P6)."""
import os, numpy as np, pandas as pd
H = os.path.dirname(os.path.abspath(__file__))
S = pd.read_csv(os.path.join(H, "final", "results", "sequential.csv.gz")); S = S[(S.setting == "primary") & (S.disease == "CRC") & (S.pi == 0.01)]
cd = pd.read_csv(os.path.join(H, "addendum_results", "posthoc_crc_deploy.csv.gz"))
rows = []
for name, d in [("locked CRC sites", S), ("11 CRC sites", cd)]:
    for m, q in d.groupby("method"):
        fp = 1000 * 0.99 * q.fpr.mean(); det = 1000 * 0.01 * q.sens.mean()
        r = dict(sites=name, method=m, false_pos_per1000=fp, cancers_detected_per1000=det)
        for wname, w in [("NB_w1/20", 1 / 20), ("NB_w1/50", 1 / 50), ("NB_w1/100", 1 / 100)]: r[wname] = det - w * fp
        rows.append(r)
D = pd.DataFrame(rows); D.to_csv(os.path.join(H, "addendum_results", "posthoc_net_benefit.csv"), index=False)
print(D.round(2).to_string(index=False))
for name in D.sites.unique():
    a = D[(D.sites == name) & (D.method == "source")].iloc[0]; b = D[(D.sites == name) & (D.method == "vp")].iloc[0]
    print(name, "break-even false positives per extra cancer:", round((a.false_pos_per1000 - b.false_pos_per1000) / (a.cancers_detected_per1000 - b.cancers_detected_per1000), 1))
