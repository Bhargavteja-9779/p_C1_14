#!/usr/bin/env bash
# Rebuild data_cache/ (not in git) from public sources. Idempotent: skips files already present.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
pip install -q scikit-learn==1.9.1 pandas scipy matplotlib pyreadr statsmodels
mkdir -p /tmp/claude-0/eh "$ROOT/data_cache"
[ -s /tmp/claude-0/eh/eh.sqlite3 ] || curl -sSfL -o /tmp/claude-0/eh/eh.sqlite3 https://experimenthub.bioconductor.org/metadata/experimenthub.sqlite3
cd "$ROOT/data_cache"
if [ ! -s sampleMetadata.csv ]; then
  curl -sSfL -o sm.rda https://raw.githubusercontent.com/waldronlab/curatedMetagenomicData/devel/data/sampleMetadata.rda
  python3 -c "import pyreadr; list(pyreadr.read_r('sm.rda').values())[0].to_csv('sampleMetadata.csv', index=False)"
fi
CC="FengQ_2015,GuptaA_2019,HanniganGD_2017,ThomasAM_2018a,ThomasAM_2018b,VogtmannE_2016,WirbelJ_2018,YachidaS_2019,YuJ_2015,ZellerG_2014,HMP_2019_ibdmdb,HallAB_2017,IjazUZ_2017,NielsenHB_2014,KarlssonFH_2013,QinJ_2012,SankaranarayananK_2015,ThomasAM_2019_c"
H="$(tr '\n' ',' < "$ROOT/Target_Journal_Submission/code/experiments/atlas/healthy_studies.txt" | sed 's/,$//')"
python3 "$ROOT/Target_Journal_Submission/code/scripts/fetch_cmd.py" "$CC,$H" || true
python3 "$ROOT/Target_Journal_Submission/code/scripts/fetch_cmd.py" "2022-10-19.MetaCardis_2020_a.relative_abundance" || true
ls ra | wc -l
