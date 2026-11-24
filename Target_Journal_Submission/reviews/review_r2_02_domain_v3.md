# Review round 2 (on manuscript_v3) - Domain referee report (independent reviewer agent, 2026-11-24; report arrived TRUNCATED after major item 2)

Overall: heterogeneity holds on a strict control subset (chi2 P~0 for all 6 classifiers), but headline extremes (56%, 87%
CRC) come from one hospital cohort; mechanism under-explored; deployment claims over-stated.

MAJOR 1. Many "healthy controls" are not healthy (checked in sampleMetadata):
- VincentC_2016 hospital inpatients, 73% antibiotics, median age 75.
- MetaCardis_2020_a 64% metabolic syndrome/IGT; 46% coded current antibiotics (likely curation problem).
- FengQ_2015 74% T2D/fatty liver; LoombaR_2017 100% fatty liver; YuJ_2015 30% T2D; ThomasAM_2018a 43% hypertension/hypercholesterolaemia.
- Pregnant/postpartum mothers: BackhedF_2015, YassourM_2018, FerrettiP_2018, ShaoY_2019, TettAJ_2019_a/b/c.
- RaymondF_2016 cephalosporin trial; HMP_2019_ibdmdb, IjazUZ_2017 symptomatic referrals / IBD kindred;
  colonoscopy-referred: ZellerG, VogtmannE, HanniganGD, ThomasAM_2018a; CosteaPI_2017 longitudinal methods set.
Strict rerun (person level: drop disease!=healthy, current antibiotics, pregnancy, family_role; study level: drop the 21
studies above; cohorts n>=15):
| classifier | all: max FPR / % out of band | strict: max FPR / % out of band | strict cohorts |
|---|---|---|---|
| CRC LASSO | 0.56 / 65% | 0.32 / 58% | 33 |
| CRC RF | 0.87 / 63% | 0.135 / 58% (none >0.20) | 33 |
| IBD LASSO | 0.84 / 62% | 0.63 / 60% | 37 |
| T2D LASSO | 0.61 / 65% | 0.61 / 61% | 36 |
Screening age 50-75: CRC LASSO 0-0.36, 75% out of band (20 cohorts, 2,014 people).
T2D set has 127 "controls" with diabetes/fatty liver/hypertension: flag rate 0.33 vs 0.14 in healthy (FengQ: 51% vs 12.5%) -
some "false positives" are true positives.
FIX: strict subset = primary analysis, full set = sensitivity; supplementary table of control type per cohort; revise
"0-87%"; report the 21-study exclusion list.

MAJOR 2. Mechanism thin; pre-specified taxon decomposition (w_j * delta z_j, protocol_atlas.md Secondary) not reported. Reviewer's run:
- CRC/VincentC (logit shift +2.3): oral anaerobes Porphyromonas asaccharolytica (+0.68), Peptostreptococcus, Dialister
  pneumosintes, Parvimonas -> "oralisation" of hospitalised/elderly/antibiotic/PPI guts, not a processing artefact.
- CRC/LokmerA (Cameroon): Prevotella sp. CAG-520, Veillonella parvula.
- T2D/non-westernised: Enterobacteriaceae/Escherichia (+0.79 combined), Catenibacterium; depletion of Anaerostipes hadrus.
- IBD/west... [report truncated here]
