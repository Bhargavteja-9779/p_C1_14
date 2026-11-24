set -e
cd "$1"; export CMD_CACHE=/home/user/p_C1_14/data_cache
for s in dedup.py atlas_v4.py analyse_atlas_v4.py deploy_v4.py summarise_v4.py; do echo "== $s"; python3 -W ignore $s > /dev/null; done
python3 - <<'PY'
import pandas as pd, json, numpy as np
a=pd.read_csv('results/heterogeneity_v4.csv'); b=pd.read_csv('ref/heterogeneity_v4.csv')
print('heterogeneity max abs diff', float((a.select_dtypes('number')-b.select_dtypes('number')).abs().max().max()))
x=json.load(open('results/summary_v4.json')); y=json.load(open('ref/summary_v4.json'))
print('v3 criterion', x['v3_criterion_dedup']==y['v3_criterion_dedup'], 'H-NX1', x['H-NX1']==y['H-NX1'], 'H-NX2', x['H-NX2']==y['H-NX2'])
print('excluded identical', open('results/excluded_samples.txt').read()==open('ref/excluded_samples.txt').read())
PY
