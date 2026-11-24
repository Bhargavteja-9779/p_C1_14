#!/usr/bin/env bash
# Rebuild data_cache/ (not in git). Idempotent: skips files already present. Fails on unexpected download errors.
#   sampleMetadata: the exact file used in the paper is committed (data/sampleMetadata.csv.gz, sha256 checked).
#   Abundance tables: curatedMetagenomicData release 2021-03-31 via Bioconductor ExperimentHub (MetaCardis: 2022-10-19).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export EH_SQLITE="${EH_SQLITE:-${TMPDIR:-/tmp}/eh/experimenthub.sqlite3}"
pip install -q -r "$ROOT/Target_Journal_Submission/code/requirements.txt"
mkdir -p "$(dirname "$EH_SQLITE")" "$ROOT/data_cache"
[ -s "$EH_SQLITE" ] || curl -sSfL -o "$EH_SQLITE" https://experimenthub.bioconductor.org/metadata/experimenthub.sqlite3
cd "$ROOT/data_cache"
[ -s sampleMetadata.csv ] || gunzip -c "$ROOT/data/sampleMetadata.csv.gz" > sampleMetadata.csv
sha256sum -c "$ROOT/data/sampleMetadata.sha256"
CC="FengQ_2015,GuptaA_2019,HanniganGD_2017,ThomasAM_2018a,ThomasAM_2018b,VogtmannE_2016,WirbelJ_2018,YachidaS_2019,YuJ_2015,ZellerG_2014,HMP_2019_ibdmdb,HallAB_2017,IjazUZ_2017,NielsenHB_2014,KarlssonFH_2013,QinJ_2012,SankaranarayananK_2015,ThomasAM_2019_c"
H="$(tr '\n' ',' < "$ROOT/Target_Journal_Submission/code/experiments/atlas/healthy_studies.txt" | sed 's/,$//')"
python3 "$ROOT/Target_Journal_Submission/code/scripts/fetch_cmd.py" "$CC,$H"
python3 "$ROOT/Target_Journal_Submission/code/scripts/fetch_cmd.py" "2022-10-19.MetaCardis_2020_a.relative_abundance"
rm -f tmp.rda; echo "cohort files: $(ls ra | wc -l) (expected 61)"
