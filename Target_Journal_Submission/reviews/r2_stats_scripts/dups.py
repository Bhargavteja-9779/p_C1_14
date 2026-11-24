import os,sys,numpy as np,pandas as pd
sys.path.insert(0,'.'); sys.path.insert(0,'../..')
from atlas_run import load_controls, healthy_studies, CACHE
from src.data import load, DISEASES
Xs=[];lab=[]
hs=[s for s in healthy_studies() if os.path.exists(os.path.join(CACHE,'ra',f'{s}.csv'))]
for s in hs:
    X,md=load_controls(s); Xs.append(X); lab+= [('H',s,i,md.loc[i,'subject_id']) for i in X.index]
for d in ['CRC','IBD','T2D']:
    X,y,g,M=load(d); Xs.append(X); lab+=[('T'+d,gg,i,M.loc[i,'subject_id'] if i in M.index else None) for gg,i in zip(g,X.index)]
A=pd.concat(Xs).fillna(0.0).values.astype(np.float32)
A=A/(A.sum(1,keepdims=True)+1e-12); L=np.log10(A+1e-5); L-=L.mean(1,keepdims=True); L/=np.linalg.norm(L,axis=1,keepdims=True)
lab=pd.DataFrame(lab,columns=['kind','study','sample','subject'])
print(len(lab), lab.kind.value_counts().to_dict())
hits=[]
for i0 in range(0,len(L),2000):
    C=L[i0:i0+2000]@L.T
    ii,jj=np.where(C>0.99)
    for a,b in zip(ii+i0,jj):
        if a<b and lab.study[a]!=lab.study[b]: hits.append((a,b,C[a-i0,b]))
h=pd.DataFrame(hits,columns=['a','b','r'])
h['ka']=lab.kind.values[h.a]; h['sa']=lab.study.values[h.a]; h['kb']=lab.kind.values[h.b]; h['sb']=lab.study.values[h.b]
h['same_sample_id']=lab['sample'].values[h.a]==lab['sample'].values[h.b]
h=h[~h.same_sample_id]
print(h.groupby(['ka','sa','kb','sb']).size().to_string())
r=pd.read_csv('results/atlas_rows.csv.gz')
dupS=set(lab['sample'].values[np.r_[h.a.values,h.b.values]])
for s,d in [('DhakanDB_2019','CRC'),('JieZ_2017','T2D'),('JieZ_2017','CRC'),('ThomasAM_2019_c','T2D'),('ThomasAM_2019_c','IBD'),('DhakanDB_2019','T2D')]:
    for m in ['lasso','rf']:
        g=r[(r.study==s)&(r.disease==d)&(r.model==m)]
        if len(g)==0: print(s,d,m,'absent'); continue
        dd=g.sample_id.isin(dupS)
        print(s,d,m,'n',len(g),'ndup',dd.sum(),'FPR dup',round(g.flag[dd].mean(),3),'nondup',round(g.flag[~dd].mean(),3))
