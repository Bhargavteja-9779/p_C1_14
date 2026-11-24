import pandas as pd, numpy as np, statsmodels.formula.api as smf, warnings; warnings.filterwarnings('ignore')
r=pd.read_csv('results/atlas_rows.csv.gz'); C=pd.read_csv('results/atlas_covars.csv.gz').set_index('sample_id')
r=r[~r.study.str.startswith('TRAIN')].join(C,on='sample_id')
icc=lambda f: float(f.cov_re.iloc[0,0]/(f.cov_re.iloc[0,0]+f.scale))
for (d,m),g in r.groupby(['disease','model']):
    g=g[g.groupby('study').study.transform('size')>=10]
    f=smf.mixedlm('score~1',g,groups=g.study).fit()
    cc=g.dropna(subset=['age','BMI','gender']); cc=cc[cc.groupby('study').study.transform('size')>=10]
    # cohorts lost
    # rank-based ICC (normal scores) to check sensitivity to tails
    from scipy.stats import norm, rankdata
    g2=g.assign(q=norm.ppf((rankdata(g.score)-.5)/len(g)))
    fq=smf.mixedlm('q~1',g2,groups=g2.study).fit()
    # flag-scale latent ICC approx (logistic latent: var_u/(var_u+pi^2/3)) via logit of cohort fpr moments skipped; ANOVA ICC on flags
    print(d,m,'all: n',len(g),'coh',g.study.nunique(),'ICC',round(icc(f),3),'normal-score ICC',round(icc(fq),3),
          '| complete-case n',len(cc),'coh',cc.study.nunique(),'ICC',round(icc(smf.mixedlm('score~1',cc,groups=cc.study).fit()),3))
