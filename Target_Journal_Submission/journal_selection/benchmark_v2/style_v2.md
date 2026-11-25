# Style analysis v2 - 11 iMeta papers read in full text (Europe PMC JATS XML)

Own words throughout; only short phrases are quoted. Word counts exclude back matter, captions and tables
(Research Article counts include the Methods section). Panel counts are estimates from caption letters.

| DOI | Type | Words (Methods) | Main figs / panels | Refs | Read for |
|---|---|---|---|---|---|
| 10.1002/imt2.212 periodontitis signature | Letter (2024) | 2,013 (0) | 2 / 5+4 | 20 | closest analogue: cross-cohort ML |
| 10.1002/imt2.70192 AI-readiness audit | Letter | 1,847 (0) | 2 / 1+6 | 18 | reproducibility framing, one-number story |
| 10.1002/imt2.70088 nationwide vaginal microbiome | Letter | 2,060 (0) | 2 / 3+5 | 19 | population atlas + derived score |
| 10.1002/imt2.70123 HCC two-guild classifier | Research Article | 7,249 (1,729) | 6 / 55 | 61 | irreproducibility framing + classifier |
| 10.1002/imt2.268 hypertension, 14 regions | Research Article | 5,151 (1,259) | 6 / 25 | 74 | per-region meta-analysis |
| 10.1002/imt2.169 infant resistome, 19 cohorts | Research Article | 6,211 (2,162) | 6 / 36 | 65 | global public-data re-analysis, map |
| 10.1002/imt2.70004 fibre-disease atlas | Research Article | 8,252 (3,884) | 5 / 23 | 65 | atlas heatmap + web resource |
| 10.1002/imt2.70008 CRC resistome transmission | Research Article | 4,418 (1,482) | 6 / 25 | 42 | big pooled cohort, workflow figure |
| 10.1002/imt2.70011 iMLGAM | Research Article | 7,165 (2,991) | 5 / 33 | 68 | ML predictor + tool, batch-robust design |
| 10.1002/imt2.70079 ACS multi-omics classifier | Research Article | 8,855 (2,934) | 7 / 33 | 75 | statistics/limitation reporting, SHAP |
| 10.1002/imt2.70084 spatial-clustering benchmark | Research Article | 7,137 (2,828) | 5 / 24 | 81 | benchmarking across heterogeneity sources |

## 1. Structure and headings
- **Letters (2025-2026)** open with "To the Editor," followed by two or three untitled paragraphs: disease burden or
  field trend -> what current approaches miss -> a "Here, we..." paragraph with scale and the main result. Then 2-4
  ALL-CAPS headings that are each a complete finding sentence (imt2.70192: three headings, the last one forward-looking;
  imt2.70088: three findings, the third introducing the derived score). Some Letters instead use RESULTS AND DISCUSSION
  with sentence-case subheads (imt2.212 has five subheads, each a claim, e.g. that taxonomy-based classifiers
  generalise across cohorts and that function-based ones do not). A short CONCLUSION closes; METHODS is a one-line
  pointer to the Supporting Information.
- **Research Articles** use INTRODUCTION / RESULTS / DISCUSSION / CONCLUSION / METHODS. Results have 5-10 declarative
  subheads, each one figure-sized claim. Methods subsections are granular (10-15), always ending with "Statistical analysis".
- Abstract blocks: Research Articles carry a main abstract (130-310 words), a graphical-abstract summary (75-130 words) and
  Highlights (35-100 words, typically 3-4 bullets). Letters carry only the graphical-abstract summary (85-190 words).
- Titles state the finding as a sentence ("X reveals Y", "X predicts Y", "Infant age inversely correlates with...") or a
  resource name plus colon. Short titles (5-10 words) are common for the most visible Letters.

## 2. Length
- Letters: about 1,850-2,500 words of main text, ~20 references, 2 figures. All three Letters read sit at the middle of
  the 1,500-3,000 band. Research Articles: 4,400-8,900 words incl. Methods (Methods ~1,300-3,900), 40-80 references,
  5-7 figures.

## 3. Figure design
- **Figure 1 is almost always a design/overview panel.** Research Articles: a full-width study-design and workflow
  schematic as Fig 1 or Fig 1A (imt2.268, imt2.70008, imt2.70079 and imt2.70004 use a single-panel overview figure;
  imt2.70084 uses a 2-panel workflow + dataset overview). Letters squeeze this into panel A of Fig 1 (imt2.212: flowchart with a world map of cohort origins).
- **Geography is drawn, not listed.** World or China map of sampling sites is the default for multi-site work
  (imt2.212 Fig 1A, imt2.169 Fig 1A, imt2.218, imt2.70106; imt2.70192 shows the geography of audited studies in Fig 2).
- **Cross-cohort performance as a matrix heatmap.** imt2.212 shows a train-cohort x test-cohort AUC heatmap with the
  diagonal (within-cohort CV) and an added LODO row; this is the closest visual template for a 14 tests x 36 populations
  FPR atlas.
- **Atlas heatmaps** with rows = features/diseases and columns = fibres/diseases (imt2.70004 Fig 4) and association
  heatmaps (imt2.70088 Fig 1) are used for breadth; network plots and Sankey diagrams are frequent secondary panels.
- Panel density: Letters ~4-8 panels per figure; Research Articles 3-13 per figure (some up to ~19). Each panel is
  referenced in text in order (Figure 1A-F).
- Classifier results: ROC curves plus boxplots of AUC; imt2.70079 adds SHAP importance; imt2.70123 adds forest plots.

## 4. Problem framing
- Opening sentences quantify burden (global prevalence, deaths, cases) with a citation, then narrow to a specific
  methodological gap. The strongest framings name **why existing results fail to transfer**: imt2.70123 blames taxon-level
  database dependency and ignored interactions; imt2.212 criticises earlier models for low resolution, few datasets and
  narrow population coverage; imt2.70192 argues AI needs reusable metadata the field does not deposit; imt2.70088 notes
  that variability across ethnicities and lifestyles makes findings inconsistent across populations.
- The gap sentence is followed by "Here, we..." with three numbers (samples, cohorts/regions, headline effect).
- Our paper fits this pattern naturally: burden of false-positive referrals -> classifiers validated by AUC in a few
  cohorts -> specificity at a fixed cut-off has never been mapped across healthy populations -> "Here, we..."

## 5. Limitations
- Letters: one to three sentences in the CONCLUSION, naming concrete missing variables and design limits
  (imt2.70088: no hormone measurements; observational design prevents causal claims). imt2.212 has no explicit limitation
  paragraph, only a forward-looking statement that clinical and multi-centre longitudinal testing is still needed.
- Research Articles: a dedicated paragraph near the end of DISCUSSION that opens by saying the study has several limitations,
  then lists them as "First... Second..." (imt2.268, imt2.70008, imt2.70079). Typical items: single centre/region,
  cross-sectional design, causality, sample size of a subgroup ("interpret with caution", imt2.70123).
- Tone is matter-of-fact; limitations are paired with a concrete next step (larger, multi-centre, longitudinal cohorts).

## 6. Statistics reporting
- AUROC/AUC is the dominant performance metric; few papers give CIs for AUC. imt2.212 reports mean and IQR across
  cohorts; imt2.70090 gives internal and two external AUROCs; imt2.183 gives hazard ratios with 95% CI.
- Multiple-testing control is stated (FDR / Benjamini-Hochberg / q-values) in most association papers (imt2.268 uses FDR
  throughout; imt2.70079 uses q-values; imt2.70088 FDR).
- Community-level tests: PERMANOVA, Wilcoxon rank-sum; random-effects meta-analysis across regions (imt2.268); permutation
  tests for classifier significance (imt2.70123); bootstrap for CIs (imt2.70192).
- Validation vocabulary: repeated k-fold CV, LODO, external/independent cohort, sample-cumulation (minimum n) modelling
  (imt2.212 estimated that ~40 samples sufficed - directly relevant to our "~100 local people" burn-in claim).
- p-values are usually given as thresholds (p < 0.05/0.01/0.001) in text and stars in figures.

## 7. Resource and tool emphasis
- Data-availability statements are detailed: accession per cohort, GitHub for scripts and figure source data, plus the
  journal's standard line on supplementary materials (slides, videos, Chinese translation). Restricted clinical metadata
  is common and accepted if stated.
- Releasing something reusable is a recurring strength signal: tier-checker tool (imt2.70192), web resource + Code Ocean
  capsule (imt2.70004), R package + web tool (imt2.70011), benchmark code (imt2.70084). Classifier papers without a tool
  (imt2.212, imt2.70123) rely on breadth instead.
- Tool papers quantify the resource (number of workflows, datasets, modules) in the abstract.

## 8. Language
- Short declarative claims; numbers in the abstract; active voice ("we identified", "we constructed"). Hedging appears as
  "suggest", "may", "potential" for mechanism, but the headline is stated plainly. Little hype in Letters; Research
  Articles use more emphatic adjectives ("profound", "strikingly").

## Implications for our manuscript (Letter format)
1. "To the Editor," + 2 framing paragraphs + "Here, we..." with: 14 tests, 36 healthy populations, 28 countries, range of
   FPR, and the burn-in result with ~100 people.
2. Three ALL-CAPS finding headings (e.g. fixed cut-offs give very different false-positive rates across healthy
   populations / the variation follows population and study features / a label-free local burn-in restores the target
   specificity).
3. Fig 1: A world map of the 36 populations + B schematic of the fixed-threshold test + C 14 x 36 FPR atlas heatmap +
   D summary distribution. Fig 2: A burn-in schematic + B FPR before/after per population + C n-required curve
   (sample-cumulation style) + D sensitivity preserved on case cohorts.
4. Limitations in 2-3 sentences: healthy-only definition, public-data heterogeneity (sequencing/batch), sensitivity on
   local cases not re-estimated, burn-in assumes a mostly healthy local intake.
5. Release a small package/script and the per-population FPR table (GitHub + Zenodo) and say so in the abstract.
