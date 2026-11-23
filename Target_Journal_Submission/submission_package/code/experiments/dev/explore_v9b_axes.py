"""DEV ONLY. Round 9b: split the CRC-score gap (condition - controls) into (a) oral-origin taxa enriched,
(b) commensal depletion (negative-coefficient species), (c) other enriched taxa. Uses explore_v9_contrib.csv."""
import os, pandas as pd
D = os.path.dirname(__file__); C = pd.read_csv(os.path.join(D, "explore_v9_contrib.csv"), index_col=0)
ORAL = ["Streptococcus", "Veillonella", "Fusobacterium", "Gemella", "Peptostreptococcus", "Parvimonas", "Porphyromonas",
        "Lactobacillus_salivarius", "Actinomyces", "Haemophilus", "Solobacterium", "Dialister_pneumosintes", "Rothia",
        "Prevotella_intermedia", "Prevotella_nigrescens", "Campylobacter", "Eikenella", "Granulicatella", "Atopobium", "Filifactor"]
coh = [c for c in C.columns if c.endswith(("2014", "2016", "2017", "2020"))]
cat = C.index.to_series().apply(lambda s: "oral" if any(o in s for o in ORAL) and C.loc[s, "coef"] > 0
                                else "commensal_depletion" if C.loc[s, "coef"] < 0 else "other_enriched")
T = C[coh].groupby(cat).sum(); T.loc["total"] = T.sum()
print(T.round(3).to_string())
print("\nshare of gap:\n", (T.loc[["oral", "commensal_depletion", "other_enriched"]] / T.loc["total"]).round(2).to_string())
print("\noral taxa in CRC model:", sorted(cat.index[cat == "oral"]))
T.to_csv(os.path.join(D, "explore_v9b_axes.csv"))
