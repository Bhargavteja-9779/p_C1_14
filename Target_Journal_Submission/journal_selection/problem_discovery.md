# STEP 2 - Real-life problem discovery (internal)

## 15 candidate problems (one-line story each)
1. **Operating-point drift of microbiome diagnostics across sites.** Screening labs deploying a stool-metagenome CRC test
   need a fixed decision threshold; thresholds set on published cohorts give very different false-positive / miss rates at a
   new site, causing excess colonoscopies or missed cancers; current work validates with AUROC only. -> KEPT (lead)
2. Drug confounding (metformin, PPIs) inflates microbiome disease signatures. (Strong prior art: Forslund 2015, Vich Vila 2020.) Dropped: mostly done.
3. Contaminant false positives in low-biomass microbiome studies (tumour microbiome controversy). Dropped: no ground-truth data at scale.
4. AMR phenotype prediction fails across lineages/geography. Dropped: crowded field; outside fast CPU budget for genomes.
5. 16S-to-shotgun classifier transfer. Dropped: few paired datasets.
6. Country bias of microbiome ageing clocks. Dropped: weaker stakeholder decision.
7. Wastewater metagenomic AMR trend detection. Dropped: data heterogeneity, unclear ground truth.
8. Hospital strain outbreak detection. Dropped: needs isolate genomes + epi labels.
9. Optimistic AUROC from small microbiome studies. Dropped: overlaps "decade-scale audit of microbiome AI-readiness" (iMeta 2026).
10. Disease-specificity failure (classifier fires on other diseases). Partly done (Thomas 2019 control augmentation); kept as a secondary analysis idea.
11. Abstain/defer when a sample is atypical. Possible D6 extension.
12. Prevalence shift between case-control studies (~50%) and screening (~1%). Merged into 1.
13. Profiler/database version shift breaks deployed models. Dropped: needs reprocessing raw reads (too costly on CPU).
14. Oral microbiome periodontitis signature. Dropped: done in iMeta 2024.
15. IBD flare prediction from longitudinal stool. Dropped: one main cohort (HMP2), weak generalisation test.

## Real-Problem Test for candidate 1
1. Stakeholder: the laboratory director / screening-programme lead who must set the test's positivity cut-off at a new
   hospital or country, and the gastroenterology unit that receives positive referrals (colonoscopy capacity).
2. Cost (cited, to verify in citation audit): CRC ~1.9 million new cases and ~0.9 million deaths in 2020 (GLOBOCAN,
   Sung et al. 2021, CA Cancer J Clin); colonoscopy capacity is a bottleneck in FIT programmes; colonoscopy carries risks
   (bleeding, perforation). False positives use scarce colonoscopy slots; false negatives delay diagnosis.
3. Documented failure: microbiome CRC classifiers lose accuracy across studies (Wirbel 2019; Thomas 2019, Nat Med; Pasolli 2016);
   batch effects across studies are a known barrier (Wang & Le Cao 2020, Brief Bioinform). Our pilot shows realised
   specificity at a 90% target ranges 0.72-1.00 across 11 cohorts, with overdispersion beyond sampling noise (p=2e-7).
4. Data: curatedMetagenomicData (public, uniformly processed MetaPhlAn3 profiles, Bioconductor; source studies public).
5. Real-world measure: unnecessary colonoscopies and missed cancers per 1,000 screened at realistic prevalence; deviation
   of realised false-positive rate from target.
6. Fit: iMeta publishes cross-cohort microbiome ML signatures (periodontitis 2024; vaginal 2025; liver tumour guilds 2026).

## Desk-rejection stress test (editor view) - first pass
- Incremental? Risk: "just recalibrate locally". Answer needed: a label-free method with guarantees and a protocol change
  (AUROC-only LOSO hides the failure) - must be shown with strong evidence. -> continue to novelty engine.
- Known model on known data? The classifier is standard on purpose; the contribution is the deployment step.
- Simpler method would do the same? Must be tested: naive local quantile is a mandatory baseline.
- Gain vanishes under statistics? Pilot overdispersion test says the problem is real; gains must be shown with paired CIs.
- Dataset too small? 20+ cohorts, ~5,000 samples across 4 diseases.
- Leakage? Leave-one-cohort-out; repeated samples (HMP2, Hall) grouped by subject.
