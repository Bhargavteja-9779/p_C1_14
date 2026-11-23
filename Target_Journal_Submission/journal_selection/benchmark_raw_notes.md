# iMeta journal benchmark - raw notes

Generated 2026-11-23. Sources: PubMed E-utilities (esearch `"Imeta"[ta] AND 2024:2026[dp]`, efetch XML), Europe PMC REST `fullTextXML`. Crossref was not needed (received/accepted dates taken from JATS `<history>` where present; otherwise NA). Helper: `/home/user/p_C1_14/Target_Journal_Submission/code/scripts/benchmark_imeta.py` (+ curated values in `benchmark_curated.json` in the same folder). Raw XML cached in /tmp/claude-0/bench/xml (scratch).

## Selection

- PubMed returned 298 iMeta records dated 2024-2026: 196 Journal Article, 67 Letter, 21 Review, 8 Editorial, 5 Errata, 1 Expression of Concern. All had a PMCID.
- No 2024 record carries the PubMed type 'Letter'; iMeta's 2024 short-format papers are indexed as 'Journal Article' (example: the periodontitis signature paper, JATS article-type `article-commentary`, which has the Letter layout). The table follows the PubMed type for `article_type` and adds a `jats_article_type` column.
- Screening: keyword pre-filter on title+abstract (ML/benchmark/tool/meta-analysis/cohort terms + microbiome terms), then a manual pick of papers closest to computational/ML/bioinformatics microbiome work. 11 PubMed Letters + 14 Research Articles. Some non-microbiome computational papers (RepliChrom, scRiskCell, FluNexus, iMLGAM, SRT benchmark, EasyDesign, TCellSI) were included because there are not enough computational microbiome Letters.
- Definitions: `n_baselines_compared` = competing methods/models/signatures compared quantitatively (feature-set comparisons within one algorithm = 0). `real_world_or_deployment_evidence` = yes when there is a deployed public tool/web service, wet-lab validation or a clinical cohort used in application. `main_text_word_count_estimate` = words in the JATS `<body>`, leaving out figure/table captions and back-matter sections (author contributions, COI, ethics, acknowledgments, data availability, references). It is approximate: it still includes the in-body 'cite this article' line (~40 words) and any short in-body Methods.
- 'NA' = not reported in the main text; 'UNVERIFIED' = could not be confirmed from the main text (usually given only in the Supplementary Information, which was not read).

## Per-paper notes

### A decade-scale audit of microbiome AI-readiness (2026; Letter; doi 10.1002/imt2.70192; PMC13780379)
- Type: Meta-research audit of public human microbiome data/metadata reusability for AI (systematic PRISMA-guided review with tiering framework). Setting: Published human microbiome studies 2012-2025 and their repository deposits.
- Data: 23,781 papers screened; 2,896 studies scored into BHAM tiers; ~720,097 samples. Cohorts/datasets: 2896 (studies audited). Baselines: 0 (not applicable). Repeats: NA.
- Stats: Multinomial logistic regression; binary logistic regression on publication year; Holm correction. Ablation: no. Cross-dataset: no. Real-world: no (policy recommendation; standalone tier-checking tool released). Code: yes: https://github.com/samd1993/MMC.
- Format: ~2470 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 18 refs; title 6 words; dates (JATS): NA.
- Novelty (paraphrased): Provides the first decade-long, sample-level audit quantifying how little human microbiome sequence data is reusable for cross-cohort AI, with a tiered metadata standard. Metrics: Proportion of studies/samples per reusability tier; odds ratios / relative risk ratios over time.

### Integrative host-microbiome modeling uncovers the implication of oral-gut translocation in advanced cirrhosis (2026; Letter; doi 10.1002/imt2.70131; PMC13377410)
- Type: Genome-scale metabolic modeling (reactobiome profiling, community FBA/FVA, host models) of paired oral-gut metagenomes. Setting: Liver cirrhosis patients across severity (MELD) groups.
- Data: GLA cohort (ENA PRJEB52891), RIFSYS cohort (PRJEB38481), healthy controls (PRJEB38483); independent TIPS cohort for validation; sample sizes in Supplement (UNVERIFIED). Cohorts/datasets: 2 (minimum: discovery + independent TIPS cohort; exact count UNVERIFIED). Baselines: 0. Repeats: NA.
- Stats: Kruskal-Wallis; pairwise Wilcoxon rank-sum; linear regression (R2). Ablation: no. Cross-dataset: yes (translocating species re-detected in independent cohort). Real-world: no. Code: yes: https://github.com/sysbiomelab/Oral-gut-liver.
- Format: ~1926 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 20 refs; title 12 words; dates (JATS): NA.
- Novelty (paraphrased): Moves oral-gut translocation in cirrhosis from taxonomy to predicted metabolic function, linking translocating species to ammonia production via metabolic modeling. Metrics: Oral-gut metabolic distance (Bray-Curtis on reactobiome), predicted metabolite fluxes, association with MELD.

### Nationwide profiling of vaginal microbiota in Chinese women reveals age-dependent shifts and predictive biomarkers for reproductive health (2025; Letter; doi 10.1002/imt2.70088; PMC12747552)
- Type: Population-scale microbiome-host factor association and derivation of a microbiome health (balance) score. Setting: 6,423 reproductive-age women from 18 Chinese provinces, with longitudinal follow-up.
- Data: CALM2004 cohort (GSA-human HRA010936, n=6,423); 13 external vaginal microbiome case-control studies for score extrapolation. Cohorts/datasets: 14 (1 discovery + 13 external case-control datasets). Baselines: 0. Repeats: NA.
- Stats: PERMANOVA; linear and logistic regression; generalized additive model; sliding-window t-test; FDR correction. Ablation: no. Cross-dataset: yes (balance score extrapolated to 13 external datasets). Real-world: no. Code: yes: https://github.com/ZJJY-Bioinformatics/CALM2004_landscape/.
- Format: ~2086 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 19 refs; title 17 words; dates (JATS): NA.
- Novelty (paraphrased): Largest East Asian vaginal microbiome survey, revealing an age-40 transition and a balance score that predicts later reproductive-tract outcomes. Metrics: Variance explained (R2), FDR-adjusted associations, balance-score group differences, associations with follow-up outcomes.

### PSOSP uncovers pervasive SOS-independent prophages with distinct genomic and host traits in bacterial genomes (2025; Letter; doi 10.1002/imt2.70073; PMC12527982)
- Type: Bioinformatics tool: prediction of prophage induction mode (SOS-dependent vs independent) from LexA binding heterology index. Setting: Bacterial genomes from public databases; wet-lab induction validation.
- Data: 49,333 complete bacterial genomes (RefSeq-derived); E. coli LexA binding reference set (n=24); experimental test set (n=10 prophages). Cohorts/datasets: 3 (reference binding set, test set, genome survey). Baselines: 0. Repeats: NA.
- Stats: 95% confidence interval for accuracy; group comparisons with p-values (test named in Supplement; UNVERIFIED). Ablation: no. Cross-dataset: no. Real-world: yes (wet-lab induction/VIP-Seq validation; web server). Code: yes: https://github.com/mujiezhang/PSOSP.
- Format: ~2083 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 20 refs; title 14 words; dates (JATS): NA.
- Novelty (paraphrased): Introduces a tool that classifies prophage induction modes and shows SOS-independent prophages are widespread with distinct genomic traits. Metrics: Accuracy, sensitivity, specificity.

### RepliChrom: Interpretable machine learning predicts cancer-associated enhancer-promoter interactions using DNA replication timing (2025; Letter; doi 10.1002/imt2.70052; PMC12371266)
- Type: Interpretable ML (random forest) predicting enhancer-promoter interactions from DNA replication timing. Setting: Human cell lines incl. leukemia; multiple chromatin-interaction technologies.
- Data: Hi-C, Hi-TrAC, ChIA-PET, 5C and replication-timing data across six cell lines (+ general model); Zenodo 11398547. Cohorts/datasets: 6 (cell lines). Baselines: UNVERIFIED (compared with several EPI predictors incl. Lollipop; full list in Supplementary Fig. S6). Repeats: 100 (random resampling) + 5-fold CV.
- Stats: NA in main text. Ablation: no (not in main text). Cross-dataset: yes (cross-cell-line and cross-technology tests). Real-world: no. Code: yes: https://github.com/DaoFuying/RepliChrom.
- Format: ~1971 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 20 refs; title 12 words; dates (JATS): rev-recd=2025-5-14; received=2025-4-20; accepted=2025-5-15.
- Novelty (paraphrased): Shows replication timing alone can predict enhancer-promoter interactions with interpretable features, revealing leukemia-specific loops. Metrics: AUPRC, AUROC (UNVERIFIED), accuracy.

### QSCNAS: A platform for quorum sensing and quenching bacteria analysis in global wastewater treatment plants (2025; Letter; doi 10.1002/imt2.70026; PMC12130577)
- Type: Database / web platform for quorum-sensing and quenching bacteria and communication network analysis. Setting: Activated sludge of wastewater treatment plants worldwide.
- Data: Global activated sludge microbiome (NCBI PRJNA509305): >1,000 samples from 269 WWTPs in 23 countries; curated local QS/QQ gene database. Cohorts/datasets: 1 (global dataset). Baselines: 0. Repeats: NA.
- Stats: NA in main text (network and coefficient-of-variation analyses). Ablation: no. Cross-dataset: no. Real-world: yes (public web platform http://www.qscnas.cn/). Code: yes: https://github.com/basswilson/Canlab-QSCNAS.
- Format: ~1999 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 15 refs; title 15 words; dates (JATS): rev-recd=2025-3-23; received=2025-2-20; accepted=2025-3-24.
- Novelty (paraphrased): Builds a global quorum-sensing communication map and online platform for WWTP microbiomes. Metrics: Relative abundance, occurrence frequency, network properties.

### scRiskCell: A single-cell framework for quantifying islet risk cells and their adaptive dynamics in type 2 diabetes (2025; Letter; doi 10.1002/imt2.70060; PMC12371254)
- Type: Single-cell computational framework assigning disease-risk index to cells; ML prediction of disease state. Setting: Human pancreatic islets across nondiabetic, prediabetic and type 2 diabetes donors.
- Data: Integrated scRNA-seq meta-analysis: 495,945 islet cells from 106 donors (49 ND, 23 preT2D, 34 T2D); 4 external validation datasets. Cohorts/datasets: 5 (integrated discovery + 4 external datasets; number of source studies in discovery UNVERIFIED). Baselines: UNVERIFIED. Repeats: NA.
- Stats: Two-sided Wilcoxon rank-sum with Benjamini-Hochberg; Pearson correlation. Ablation: no. Cross-dataset: yes (4 external datasets). Real-world: yes (web server http://lin-group.cn/server/scRiskCell). Code: yes: https://github.com/xiexq007/scRiskCell.
- Format: ~1907 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 20 refs; title 17 words; dates (JATS): NA.
- Novelty (paraphrased): Quantifies disease-perturbed risk beta cells along the T2D continuum and uses their proportion as a staging biomarker. Metrics: AUC.

### Gut microbiota-mediated immune and metabolic dysregulation in coronary artery disease progression and prognosis (2026; Letter; doi 10.1002/imt2.70147; PMC13519092)
- Type: Prospective multi-omics cohort with ML prognostic modeling plus FMT mouse validation. Setting: Coronary artery disease patients (PUMCH-CAD cohort), median 1.85-year follow-up for MACE.
- Data: 319 participants with fecal metagenomics and serum metabolomics (GSA-human HRA010791); ApoE-/- mouse FMT. Cohorts/datasets: 1. Baselines: 0. Repeats: 1000 (RSF iterations, out-of-bag).
- Stats: PERMANOVA/Adonis; Kaplan-Meier; C-index; correlation analyses. Ablation: no. Cross-dataset: no. Real-world: no (FMT in mice as causal evidence). Code: no (no code URL; data deposited).
- Format: ~2497 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 20 refs; title 13 words; dates (JATS): rev-recd=2026-6-10; received=2026-4-26; accepted=2026-6-10.
- Novelty (paraphrased): Links CAD-severity gut microbial features and aromatic amino acid metabolism to future MACE and shows transmissible atherosclerosis susceptibility. Metrics: C-index (OOB), hazard/risk group separation.

### FluNexus: A versatile web platform for antigenic prediction and visualization of influenza A viruses (2026; Letter; doi 10.1002/imt2.70127; PMC13147951)
- Type: Web platform + benchmark of sequence-based antigenic prediction methods and antigenic mapping. Setting: Influenza A surveillance (H1, H3, H5 subtypes).
- Data: HA1 sequences (GISAID) and HI titers (Crick WIC reports; Smith et al.) for H1, H3, H5. Cohorts/datasets: 3 (subtype datasets). Baselines: 10 (antigenic prediction algorithms benchmarked); mapping compared with 4 (Racmacs, UMAP, PCA, t-SNE). Repeats: NA (cross-validation and retrospective partitions; details in Supplement S5).
- Stats: NA in main text. Ablation: no. Cross-dataset: yes (retrospective temporal testing; subtype generalization). Real-world: yes (public web platform). Code: yes: https://github.com/xingyili/FluNexus-methodbox.
- Format: ~1986 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 20 refs; title 14 words; dates (JATS): rev-recd=2026-4-10; received=2026-3-24; accepted=2026-4-13.
- Novelty (paraphrased): Unifies preprocessing, ten antigenic predictors with a benchmark, and improved antigenic maps in one online platform. Metrics: AUC, AUPRC, antigenic distance agreement (UNVERIFIED).

### Majorbio Cloud 2026 provides comprehensive analysis workflows for microbiome (2026; Letter; doi 10.1002/imt2.70109; PMC13726581)
- Type: Cloud platform update (software/resource description). Setting: Microbiome multi-omics analysis service.
- Data: NA (platform; demonstration workflows). Cohorts/datasets: NA. Baselines: 0. Repeats: NA.
- Stats: Platform offers PERMANOVA, Mantel, RDA, random forest, LASSO, etc.; none used for inference. Ablation: no. Cross-dataset: no. Real-world: yes (deployed platform; users and publications section). Code: no (web service https://cloud.majorbio.com/; no source code).
- Format: ~2503 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 18 refs; title 9 words; dates (JATS): NA.
- Novelty (paraphrased): Describes 26 microbiome workflows with one-click analysis and publication-ready plotting in an updated cloud platform. Metrics: NA.

### Spaceflight redefines ageing-associated microbiota (2025; Letter; doi 10.1002/imt2.70023; PMC12130553)
- Type: Integrative re-analysis of public scRNA-seq and multi-site metagenome/metatranscriptome data plus Mendelian randomization. Setting: Astronauts before/after spaceflight vs. natural ageing cohort.
- Data: PBMC scRNA-seq (ageing cohort, astronauts); gut/oral/skin metagenomes at six flight time points; sizes in Supplement (UNVERIFIED). Cohorts/datasets: 2 (minimum: ageing cohort + astronaut cohort; data from multiple databases, UNVERIFIED). Baselines: 0. Repeats: NA.
- Stats: Differential expression/abundance testing, Mendelian randomization (details in Supplement). Ablation: no. Cross-dataset: no. Real-world: no. Code: yes: https://github.com/liusai118/space.
- Format: ~2410 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 17 refs; title 4 words; dates (JATS): NA.
- Novelty (paraphrased): Argues spaceflight shifts microbiota in ways that partly counter ageing signatures while immune changes mimic ageing. Metrics: NA (descriptive differential analyses).

### A universal oral microbiome-based signature for periodontitis (2024; ResearchArticle; doi 10.1002/imt2.212; PMC11316925)
- Type: Cross-cohort meta-analysis and ML diagnostic signature (random forest) from public shotgun metagenomes. Setting: Periodontitis vs healthy, oral microbiome, 5 countries / 3 continents.
- Data: 8 public oral shotgun cohorts (e.g., PRJDB11203, PRJNA230363, PRJNA396840, PRJNA678453): 6 case-control (117 cases, 106 controls) + 2 case-only (118 cases). Cohorts/datasets: 8. Baselines: 0 (single RF; taxonomic vs functional vs combined feature sets compared). Repeats: NA.
- Stats: Spearman correlation; consistency of biomarkers across >=3 cohorts; sample-cumulation modeling. Ablation: no (feature-type comparison only). Cross-dataset: yes (cohort-to-cohort matrix, LODO, 2 case-only external cohorts). Real-world: no. Code: yes: https://github.com/whchenlab/Oral-Microbiome-Based-Signature-for-Periodontitis.
- Format: ~2017 (approximate; JATS body text excl. captions/back matter) words; 2 fig; 0 tab; 20 refs; title 7 words; dates (JATS): NA.
- Novelty (paraphrased): Identifies cross-cohort consistent species/pathway biomarkers and a generalizable metagenomic classifier for periodontitis. Metrics: AUC (internal, external, LODO), true positive rate.

### Two stable gut microbiome guilds predict liver tumor class and treatment responses (2026; ResearchArticle; doi 10.1002/imt2.70123; PMC13147943)
- Type: Genome-guild (co-abundance network) biomarker model + random forest classification/prediction. Setting: Liver tumors (HCC, iCCA, CRLM, benign); recurrence and anti-PD-1/TACE response.
- Data: Cohort 1: 120 HCC + 76 benign (PRJNA1372073/PRJNA1372070); Cohort 2: 33 HCC vs 7 CRLM; external cohort: 76 CTR, 25 HCC, 19 iCCA; treatment cohorts from Xin et al. and Zhao et al.. Cohorts/datasets: 5 (2 internal, 1 external, 2 published treatment cohorts). Baselines: 0 (compared only with chance-level AUPRC). Repeats: NA (leave-one-out CV).
- Stats: PERMANOVA; Mann-Whitney U with Benjamini-Hochberg; Procrustes analysis. Ablation: no. Cross-dataset: yes (external cohort; transfer across tumor types). Real-world: no. Code: yes: https://github.com/nightkid03/HCC-TCG.
- Format: ~7254 (approximate; JATS body text excl. captions/back matter) words; 6 fig; 0 tab; 61 refs; title 12 words; dates (JATS): NA.
- Novelty (paraphrased): Uses stable competing genome guilds instead of taxa to obtain transferable gut microbiome signatures for liver tumor class and treatment outcome. Metrics: AUROC, AUPRC, accuracy.

### Linking dietary fiber to human malady through cumulative profiling of microbiota disturbance (2025; ResearchArticle; doi 10.1002/imt2.70004; PMC11865338)
- Type: Text-mining meta-analysis with new aggregation algorithm (BHWA) and network analysis; web resource. Setting: Dietary fibers, gut microbiota disturbance and human diseases.
- Data: 10,899 evidence entries from 1,173 articles; 32 dietary fibers; 161 diseases; plus validation experiments. Cohorts/datasets: 1173 (articles mined). Baselines: 0. Repeats: 10000 (randomization iterations).
- Stats: Pearson correlation; FDR; randomization tests; repeated-measures ANOVA. Ablation: no. Cross-dataset: no. Real-world: yes (web tool https://mdifibank.org.cn/). Code: yes: https://github.com/zhangxiner2/Cumulative-Profiling-of-Microbiota-Disturbance (+ Code Ocean capsule).
- Format: ~8257 (approximate; JATS body text excl. captions/back matter) words; 5 fig; 0 tab; 65 refs; title 12 words; dates (JATS): rev-recd=2025-1-27; received=2024-12-23; accepted=2025-1-29.
- Novelty (paraphrased): Proposes a taxonomy-weighted aggregation of literature-reported microbiota disturbances to map fiber-disease relationships. Metrics: Similarity scores, network edge significance.

### Non-differential gut microbes contribute to hypertension and its severity through co-abundances: A multi-regional prospective cohort study (2025; ResearchArticle; doi 10.1002/imt2.268; PMC11865328)
- Type: Microbial co-abundance network inference and random-effects meta-analysis across regions, with replication. Setting: Hypertension in Guangdong Gut Microbiome Project (14 regions).
- Data: GGMP (ENA PRJEB18535): 2,355 hypertensive + 4,644 non-hypertensive; replication: 281 hypertension samples (GMLP + Australian cohort). Cohorts/datasets: 16 (14 regional subcohorts + 2 replication cohorts). Baselines: 0. Repeats: 20 iterations x 100 bootstrap resamples per network.
- Stats: Random-effects meta-analysis; FDR; heterogeneity analysis; differential co-abundance testing. Ablation: no. Cross-dataset: yes (independent replication cohorts). Real-world: no. Code: yes: https://github.com/MicrobiomeCardioMetaLab/HypertensionNetwork_project.
- Format: ~5156 (approximate; JATS body text excl. captions/back matter) words; 6 fig; 0 tab; 74 refs; title 16 words; dates (JATS): NA.
- Novelty (paraphrased): Shows non-differentially abundant microbes contribute to hypertension through replicable co-abundance interactions. Metrics: Number of replicated significant co-abundances, effect sizes.

### iMLGAM: Integrated Machine Learning and Genetic Algorithm-driven Multiomics analysis for pan-cancer immunotherapy response prediction (2025; ResearchArticle; doi 10.1002/imt2.70011; PMC11995183)
- Type: ML ensemble method/R package (genetic algorithm + 50 base learners) for immunotherapy response prediction. Setting: Pan-cancer immune checkpoint blockade cohorts.
- Data: 11 RNA-seq ICB cohorts (1,242 subjects, 6 cancer types); TCGA 9,815 patients (30 cohorts); 7 CRISPR screen cohorts; in-house ICB cohort (n=14). Cohorts/datasets: 11 (ICB cohorts used for training/test/validation). Baselines: 12 (published signatures). Repeats: NA (10-fold CV with grid search).
- Stats: Multivariable logistic regression; ROC; univariate Cox regression. Ablation: no. Cross-dataset: yes (independent validation cohorts). Real-world: yes (Shiny web tool; in-house clinical cohort). Code: yes: https://github.com/Yelab1994/iMLGAM.
- Format: ~7170 (approximate; JATS body text excl. captions/back matter) words; 5 fig; 0 tab; 68 refs; title 14 words; dates (JATS): rev-recd=2025-2-20; received=2025-1-02; accepted=2025-2-21.
- Novelty (paraphrased): Combines gene-pair features with a GA-optimized ensemble to predict ICB response better than existing signatures. Metrics: AUC, F1, TPR/TNR/FPR/FNR.

### A comprehensive benchmarking for spatially resolved transcriptomics clustering methods across variable technologies, organs, and replicates (2025; ResearchArticle; doi 10.1002/imt2.70084; PMC12747554)
- Type: Benchmark of spatial clustering methods. Setting: Spatially resolved transcriptomics across technologies, organs and replicates.
- Data: ~600 real and simulated datasets (10x Visium, MERFISH, seqFISH+, STARmap etc.). Cohorts/datasets: 600 (approximate, datasets). Baselines: 14 (methods benchmarked). Repeats: 5 (replicated runs per sample).
- Stats: Pearson correlation; ANOVA in linear model of preprocessing effects. Ablation: yes (preprocessing-step contribution; simulated domain removal). Cross-dataset: yes (across technologies, organs, replicates). Real-world: no. Code: yes: https://github.com/ZJUFanLab/SRTBenchmark.
- Format: ~7142 (approximate; JATS body text excl. captions/back matter) words; 5 fig; 1 tab; 81 refs; title 15 words; dates (JATS): rev-recd=2025-9-02; received=2025-7-09; accepted=2025-9-04.
- Novelty (paraphrased): Systematic benchmark of 14 spatial clustering tools with analysis of factors driving performance. Metrics: ARI, NMI, FMI and others; runtime; memory.

### Transmission of antimicrobial resistance genes from the environment to human gut is more pronounced in colorectal cancer patients than in healthy subjects (2025; ResearchArticle; doi 10.1002/imt2.70008; PMC11995172)
- Type: Meta-analysis of public + new metagenomes (resistome source tracking). Setting: Colorectal cancer patients vs healthy and city-matched environments.
- Data: 1,605 stool metagenomes (748 CRC, 857 healthy; 110/112 new) and 1,035 environmental samples (56 new); 10 CRC cohorts; GSA CRA022416/CRA022431. Cohorts/datasets: 10 (human cohorts; plus environmental sources). Baselines: 0. Repeats: NA.
- Stats: PERMANOVA; two-tailed Wilcoxon rank-sum. Ablation: no. Cross-dataset: yes (validated in 9 of 10 individual cohorts). Real-world: no. Code: yes: https://github.com/WilsonYangLiu/Environmental-ARGs-in-CRC-resistome.git.
- Format: ~4423 (approximate; JATS body text excl. captions/back matter) words; 6 fig; 0 tab; 42 refs; title 22 words; dates (JATS): rev-recd=2025-2-12; received=2024-11-04; accepted=2025-2-14.
- Novelty (paraphrased): Shows higher environmental-to-gut transmission of antimicrobial resistance genes in CRC patients. Metrics: ARG burden, similarity indices, core index.

### A gut microbiome-lipid axis in early pregnancy is associated with metabolic dysregulation and diabetes risk (2026; ResearchArticle; doi 10.1002/imt2.70166; PMC13455838)
- Type: Nested case-control multi-omics with random forest prediction and mediation. Setting: Early pregnancy, gestational diabetes risk (Tongji-Huaxi-Shuangliu Birth Cohort).
- Data: 784 pregnant women (222 later GDM), metagenomics + lipidomics (NODE OEP00003504); external T2DM meta-analysis (n=8,117) for comparison. Cohorts/datasets: 2 (study cohort + external T2DM dataset). Baselines: 0 (feature-set comparisons only). Repeats: 100 (repeated 5-fold CV).
- Stats: PERMANOVA; MaAsLin2; PLS-DA with permutation; FDR; mediation analysis. Ablation: no. Cross-dataset: no (external dataset used for association comparison only). Real-world: no. Code: yes: https://github.com/ChangHe005/SL-GDM.
- Format: ~7241 (approximate; JATS body text excl. captions/back matter) words; 6 fig; 0 tab; 51 refs; title 15 words; dates (JATS): rev-recd=2026-7-15; received=2026-5-17; accepted=2026-7-24.
- Novelty (paraphrased): Identifies an early-pregnancy gut microbiome-lipid axis preceding GDM and tests it in mice. Metrics: AUC.

### EasyMetagenome: A user-friendly and flexible pipeline for shotgun metagenomic analysis in microbiome research (2025; ResearchArticle; doi 10.1002/imt2.70001; PMC11865343)
- Type: Bioinformatics pipeline (shotgun metagenomics). Setting: General microbiome research.
- Data: Demonstration datasets (UNVERIFIED in main text). Cohorts/datasets: UNVERIFIED. Baselines: 0 (qualitative comparison with other pipelines). Repeats: NA.
- Stats: ANOVA with Tukey HSD; PERMANOVA (demonstration). Ablation: no. Cross-dataset: no. Real-world: yes (released software). Code: yes: https://github.com/YongxinLiu/EasyMetagenome.
- Format: ~4768 (approximate; JATS body text excl. captions/back matter) words; 6 fig; 1 tab; 76 refs; title 13 words; dates (JATS): received=2024-11-29; accepted=2025-1-22.
- Novelty (paraphrased): Provides an easy, modular end-to-end shotgun metagenomic pipeline with visualizations. Metrics: NA.

### microeco 2: A comprehensive R package for downstream analysis of microbiome omics data (2026; ResearchArticle; doi 10.1002/imt2.70132; PMC13377413)
- Type: R package update (statistics, ML, visualization). Setting: Microbiome omics downstream analysis.
- Data: Example datasets (UNVERIFIED). Cohorts/datasets: UNVERIFIED. Baselines: UNVERIFIED (feature comparison with other packages in Table S1). Repeats: 10 (runtime repeats per method).
- Stats: Beta-GLMM; perMANOVA; Benjamini-Hochberg FDR. Ablation: no. Cross-dataset: no. Real-world: yes (released package). Code: yes: https://github.com/ChiLiubio/microeco.
- Format: ~5573 (approximate; JATS body text excl. captions/back matter) words; 5 fig; 0 tab; 52 refs; title 13 words; dates (JATS): rev-recd=2026-4-24; received=2026-1-29; accepted=2026-4-27.
- Novelty (paraphrased): Second major version adds normalization and machine-learning classes and wider method coverage. Metrics: Runtime; feature coverage.

### From mechanism to application: Decrypting light-regulated denitrifying microbiome through geometric deep learning (2024; ResearchArticle; doi 10.1002/imt2.162; PMC10989148)
- Type: Geometric deep learning (GCN with Deep Graph Infomax) on meta-omics + optogenetic experiments. Setting: Light-regulated denitrifying microbiome (bioprocess).
- Data: Own meta-omics (CNCB PRJCA017836; NCBI PRJNA984758). Cohorts/datasets: 1. Baselines: 1 (K-means). Repeats: NA.
- Stats: Pearson correlation. Ablation: yes (with vs without subcellular information). Cross-dataset: no. Real-world: yes (wet-lab regulation experiments). Code: yes: https://github.com/YoungeLiao/DMLA.
- Format: ~6713 (approximate; JATS body text excl. captions/back matter) words; 6 fig; 0 tab; 55 refs; title 12 words; dates (JATS): received=2023-10-02; accepted=2023-10-28.
- Novelty (paraphrased): A discover-model-learn-advance cycle using graph neural networks to decode and steer a denitrifying microbiome. Metrics: Cluster functional annotation score, accuracy.

### Deep learning enhancing guide RNA design for CRISPR/Cas12a-based diagnostics (2024; ResearchArticle; doi 10.1002/imt2.214; PMC11316927)
- Type: Deep learning (CNN) predictor for crRNA design, web tool and wet-lab validation. Setting: CRISPR/Cas12a diagnostics for infectious pathogens.
- Data: 11,496 experimental detection cases (1,533 crRNAs, 34 targets); augmented 33,351 data points. Cohorts/datasets: 1. Baselines: 5 (CNN12a, Transformer12a, Transformer12ae, CNN-derived, Transformer-derived). Repeats: NA (5-fold CV).
- Stats: Spearman; Pearson; ROC. Ablation: yes (with vs without data augmentation). Cross-dataset: yes (hold-out unseen targets; validation on new pathogens). Real-world: yes (wet-lab detection of MPXV, EV71, CV-A16, L. monocytogenes, HPV; website). Code: yes: https://github.com/scRNA-Compt/EasyDesign.
- Format: ~4877 (approximate; JATS body text excl. captions/back matter) words; 4 fig; 0 tab; 29 refs; title 9 words; dates (JATS): NA.
- Novelty (paraphrased): A CNN trained on large Cas12a detection data that designs effective diagnostic crRNAs. Metrics: Spearman rho, Pearson r, AUC.

### Distinct microbial and metabolic shifts characterize acute coronary syndrome and recovery (2025; ResearchArticle; doi 10.1002/imt2.70079; PMC12528003)
- Type: Cross-sectional multi-omics with LightGBM classifiers and SHAP. Setting: Coronary artery disease stages (NCA, sCAD, ACS) and ACS recovery.
- Data: 548 individuals (175 NCA, 161 sCAD, 212 ACS) fecal metagenomics + plasma metabolomics; independent recovery cohort (n=52). Cohorts/datasets: 2. Baselines: 1 (clinical-indicator model). Repeats: NA (10-fold CV; 80/20 hold-out).
- Stats: Kruskal-Wallis; Fisher exact; MaAsLin2 (q<0.1). Ablation: no. Cross-dataset: no (internal hold-out only). Real-world: no. Code: yes: https://github.com/JingXu0701/CAD_MultiOmics.
- Format: ~8859 (approximate; JATS body text excl. captions/back matter) words; 7 fig; 0 tab; 75 refs; title 11 words; dates (JATS): NA.
- Novelty (paraphrased): Gut microbial and metabolic features distinguish ACS from stable CAD and partly normalize after recovery. Metrics: ROC-AUC.

### TCellSI: A novel method for T cell state assessment and its applications in immune environment prediction (2024; ResearchArticle; doi 10.1002/imt2.231; PMC11487559)
- Type: Computational scoring method (rank-based) for T cell states from transcriptomes. Setting: Immune profiling incl. cancer immunotherapy cohorts.
- Data: 379 T cell lines (20 datasets); 34,730 single cells; 4,477 pseudo-bulk; TCGA 10,535; GTEx 7,862; 674 immunotherapy samples. Cohorts/datasets: 20 (minimum; T cell line datasets). Baselines: 3 (p16, p21, CS score for senescence; other signature comparisons UNVERIFIED). Repeats: NA.
- Stats: Mann-Whitney U statistic basis; correlation. Ablation: no. Cross-dataset: yes (3 independent validation cohorts). Real-world: no. Code: yes: https://github.com/GuoBioinfoLab/TCellSI/.
- Format: ~4880 (approximate; JATS body text excl. captions/back matter) words; 6 fig; 0 tab; 54 refs; title 16 words; dates (JATS): NA.
- Novelty (paraphrased): First tool scoring eight T cell states from bulk transcriptomes. Metrics: AUC.

## Summary statistics (from `benchmark_imeta.py build`)

Numbers are parsed from the leading value of each cell; NA/UNVERIFIED cells are left out (the n of each statistic is shown).

| Metric | All (25) | Letters (11) | Research Articles (14) |
|---|---|---|---|
| n_cohorts_or_datasets | median 5 (IQR 2-13; n=22) | 3 (2-6; n=10) | 9 (2-17; n=12) |
| n_baselines_compared | median 0 (IQR 0-1; n=22) | 0 (0-0; n=9) | 0 (0-3; n=13) |
| n_seeds/repeats (reported) | median 100 (IQR 15-550; n=7 of 25) | n=2 (100; 1000) | 20 (10-100; n=5) |
| Ablation | 3/25 (12%) | 0/11 | 3/14 |
| Cross-dataset/external test | 13/25 (52%) | 5/11 | 8/14 |
| Real-world/deployment evidence | 11/25 | 5/11 | 6/14 |
| Code available | 23/25 (92%) | 9/11 | 14/14 |
| Main-text words (approximate) | 4423 (2083-6713) | 2083 (1979-2440; range 1907-2503) | 6143 (4878-7223) |
| Figures | 4 (2-6) | 2 (all 11 have exactly 2) | 6 (5-6) |
| Tables | 0 | 0 (all) | 0 (2 papers have 1) |
| References | 29 (20-61) | 20 (18-20; range 15-20) | 58 (51-73) |
| Title length (words) | 13 (12-15) | 13 (10.5-14.5) | 13 (12-15) |

The values in the 'repeats' row are of mixed kinds: RepliChrom 100 resamplings, RSF 1000 iterations, GDM 100x repeated 5-fold CV, SRT 5 runs, microeco 10 runtime repeats, network 20 iterations, BHWA 10,000 randomizations. ML studies with explicit CV repeats are rare: most use a single k-fold CV, LOOCV or a hold-out split.

## Style observations (paraphrased, no copied sentences)

**Titles.** About 13 words (IQR 12-15) in Wiley title case. Three patterns: (1) a full declarative finding sentence with a verb ("X reveals/predicts/drives Y"); this is the most common pattern for both Letters and research papers. (2) Tool name, colon, descriptor ("NAME: A ... for ..."); used for tools, platforms and packages, often with a version number ("2", "2026", "1.0"). (3) A short noun-phrase claim (e.g., "A universal ... signature for ..."). Titles rarely contain abbreviations other than tool names.

**Abstract and front matter.**
- Research Articles have three parts: an unstructured one-paragraph Abstract (median ~236 words, range 133-315); a Highlights block of 3-4 bullet sentences (~35-87 words in total); and a short graphical-abstract text (~40-130 words).
- Letters have no conventional abstract. Only a short graphical-abstract summary is given (median ~106 words, range 26-188), and PubMed indexes it as the abstract. Letters have no Highlights.
- All 25 papers have a graphical abstract. No 'Plain language summary' was found (0/25). Keywords appear in the XML of some research papers (about 5 per paper).
- Every paper includes a 'cite this article' line and footnotes for equal contribution. The Data availability boilerplate lists supplementary items (methods, figures, tables, graphical abstract, slides, videos, Chinese translated version, update materials) hosted on the iMeta Science site.

**Introduction opening.**
- Letters always begin with the salutation "To the Editor," and then give 1-2 background paragraphs. These go from a broad burden or importance statement, to the specific gap ("however, most studies..."), to a "Here, we..." paragraph that summarizes data scale and main findings. The intro has no heading.
- Research papers open with a field-importance sentence under INTRODUCTION. They then list limitations of prior work, sometimes as an explicit enumeration, and end with a "Here, we developed/present..." paragraph, often numbering the contributions (1)(2)(3).

**How contributions are stated.** Contributions are stated as concrete scale plus result: number of samples, cohorts or genomes, then the key metric (e.g., AUC values, % of studies). Tool papers list features as numbered items. Claims of firstness appear ('first', 'unprecedented', 'largest') but are not universal.

**Section order: Letters (iMeta 'Letter').**
1. "To the Editor," plus untitled intro paragraphs.
2. Either 2-4 ALL-CAPS declarative finding headings (each heading is itself a result sentence), or a "RESULTS AND DISCUSSION" heading with sentence-case declarative subheadings.
3. "CONCLUSION" (common), or a combined "POTENTIAL APPLICATION AND LIMITATIONS" / "Application and clinical relevance" paragraph.
4. Optionally a very short "METHODS" that points to the Supporting Information (sometimes placed first, as in RepliChrom, or last). Full methods are in the Supplement.
5. Back matter: AUTHOR CONTRIBUTIONS, CONFLICT OF INTEREST STATEMENT, (FUNDING INFORMATION), ETHICS STATEMENT, (AI STATEMENT, seen in 2026), Supporting information, ACKNOWLEDGMENTS, DATA AVAILABILITY STATEMENT, REFERENCES.

Letters have exactly 2 multi-panel figures, 0 tables, 15-20 references (20 appears to be a cap) and about 1,900-2,500 words. Most of the evidence is in many supplementary figures and tables (often S1-S15 or more).

**Section order: Research Articles.** INTRODUCTION, RESULTS (declarative subheadings), DISCUSSION, CONCLUSION, METHODS (methods come last), then the same back matter. 4-7 figures, 0-1 tables, about 29-82 references, about 4,400-8,900 words.

**Limitations.**
- Letters give limitations in 1-3 sentences near the end. The sentence usually begins "Limitations include..." or "Our study has some limitations", or the limitations are folded into an application/limitations closing section. Typical items: no external validation, observational design, confounding, data from mixed sources.
- Research Articles have a Discussion paragraph that enumerates limitations (First/Second/...) and ends with a call for independent or prospective validation.

**References.** Numbered in-text citations in square brackets [1], [3, 4, 5], and the list is ordered by citation. The list follows the Wiley author-date-like layout: Surname, Given names, ... Year. "Title in quotes." Journal Volume: pages. DOI (bare, no "https://doi.org").

**Figures.** Dense composite multi-panel figures (A-L or more). Panels mix workflow schematics (often figure panel A = study design or data flow), heatmaps, ROC/PR curves, violin/box plots, networks and UMAP/PCoA. Captions open with a summary-title sentence, then describe each panel and name the test and n (e.g., 'Kruskal-Wallis with pairwise Wilcoxon', 'Two-sided Wilcoxon, BH-adjusted'). For a cross-cohort ML Letter, the periodontitis paper is a template: Fig 1 has a dataset map/flowchart, a cohort-to-cohort AUC matrix with a LODO row, and external-cohort TPR; Fig 2 has biomarker interaction networks.
