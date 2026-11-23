"""Load curatedMetagenomicData species relative-abundance profiles + metadata into a single matrix."""
import os, numpy as np, pandas as pd
CACHE = os.environ.get("CMD_CACHE", os.path.join(os.path.dirname(__file__), "..", "..", "..", "data_cache"))
DISEASES = {
    "CRC": dict(case="CRC", studies=["FengQ_2015","GuptaA_2019","HanniganGD_2017","ThomasAM_2018a","ThomasAM_2018b",
                                     "ThomasAM_2019_c","VogtmannE_2016","WirbelJ_2018","YachidaS_2019","YuJ_2015","ZellerG_2014"]),
    "IBD": dict(case="IBD", studies=["HMP_2019_ibdmdb","HallAB_2017","IjazUZ_2017","NielsenHB_2014"]),
    "T2D": dict(case="T2D", studies=["KarlssonFH_2013","MetaCardis_2020_a","QinJ_2012","SankaranarayananK_2015"]),
    "adenoma": dict(case="adenoma", studies=["FengQ_2015","HanniganGD_2017","ThomasAM_2018a","YachidaS_2019","ZellerG_2014"]),
}
DEV_CRC = ["FengQ_2015","GuptaA_2019","HanniganGD_2017","ThomasAM_2018a","ThomasAM_2018b","VogtmannE_2016","WirbelJ_2018","ZellerG_2014"]
LOCKED_CRC = ["YachidaS_2019","YuJ_2015","ThomasAM_2019_c"]

def load(disease, studies=None, one_per_subject=True):
    cfg = DISEASES[disease]; studies = studies or cfg["studies"]
    meta_all = pd.read_csv(os.path.join(CACHE, "sampleMetadata.csv"), low_memory=False).drop_duplicates("sample_id").set_index("sample_id")
    Xs, Ms = [], []
    for s in studies:
        a = pd.read_csv(os.path.join(CACHE, "ra", f"{s}.csv"), index_col=0)
        a.index = [i.split("|")[-1] for i in a.index]
        a = a.groupby(level=0).sum().T
        md = meta_all.loc[meta_all.index.intersection(a.index)]
        md = md[md.study_name == s] if "study_name" in md else md
        md = md[(md.study_condition.isin([cfg["case"], "control"])) & (md.body_site == "stool")]
        if one_per_subject:  # longitudinal cohorts: keep first sample per subject (avoid subject leakage / pseudo-replication)
            md = md.assign(_d=pd.to_numeric(md.get("days_from_first_collection"), errors="coerce").fillna(0)).sort_values("_d")
            md = md[~md.subject_id.duplicated()]
        Xs.append(a.loc[md.index]); Ms.append(md.assign(study=s))
    X = pd.concat(Xs).fillna(0.0); M = pd.concat(Ms)
    y = (M.study_condition == cfg["case"]).astype(int).values
    return X, y, M.study.values, M
