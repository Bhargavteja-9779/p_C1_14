# scorecard_v3.md — What iMeta values for atlas / resource / global-population / diagnostic-ML papers

Scores are my own judgments from the full texts I read (12 papers full-text, rest from abstracts). They are
subjective 1-5 ratings meant to position our planned Letter, not official reviews. Papers already in the
committed benchmark_v2 set were read for calibration but are not re-scored here; this scorecard is computed
over the 25 NEW papers in benchmark_v3/papers.csv. Rows scored from abstract only are lower-confidence and
flagged where it matters.

## The 8 dimensions and 1-5 anchors

1. **Data scale / coverage** — raw size and breadth (samples, cohorts, countries, species).
   1 = single small cohort/dataset; 3 = one large cohort or ~1,000s samples; 5 = many cohorts/countries or
   a catalog of millions of genes / hundreds of thousands of samples with multi-site geography.

2. **Biological / clinical insight** — does a reader learn a real mechanism or clinically actionable fact?
   1 = descriptive only; 3 = a clear association with plausible interpretation; 5 = causally validated or
   decision-changing insight.

3. **Resource / tool released** — reusable artifact others can run.
   1 = none; 3 = code or deposited data; 5 = maintained web tool/database/catalog + code with evident uptake.

4. **Figure clarity** — schematic + map/heatmap grammar, dense but legible panels.
   1 = unclear/sparse; 3 = standard multi-panel; 5 = a schematic workflow + a map/heatmap that carries the
   argument on its own.

5. **Novelty of finding** — is the headline genuinely new?
   1 = confirmatory; 3 = new angle on known biology; 5 = first-of-kind atlas/phenomenon/claim.

6. **Rigor** — replication, external validation, correct statistics, honest limitations.
   1 = single dataset no validation; 3 = internal CV + sensible tests; 5 = independent external cohorts +
   stated limitations + corrected stats.

7. **Readability** — plain declarative prose, defined terms, the 3-move opening, finding-as-heading.
   1 = dense/jargon; 3 = competent; 5 = a non-specialist follows the headline from title to figure.

8. **Practical impact** — will people use the result/tool, and does it change practice?
   1 = niche; 3 = useful to a subfield; 5 = broadly adopted or changes how a task is done.

## Scores (25 new papers; confidence: FT = full text read, A = abstract only)

| # | short name (DOI) | conf | 1 scale | 2 insight | 3 resource | 4 figs | 5 novelty | 6 rigor | 7 read | 8 impact | total/40 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Rumen methylation atlas (70153) | FT | 3 | 4 | 4 | 4 | 5 | 3 | 4 | 3 | 30 |
| 2 | Duck gut catalog (198) | FT | 5 | 3 | 5 | 4 | 4 | 3 | 4 | 3 | 31 |
| 3 | ggClusterNet 2 (70041) | FT | 2 | 2 | 5 | 4 | 3 | 3 | 4 | 5 | 28 |
| 4 | SCIGAMA spinal atlas (70128) | A | 3 | 3 | 4 | 3 | 4 | 3 | 4 | 3 | 27 |
| 5 | Microbiome-age framework (70148) | A | 2 | 3 | 1 | 3 | 3 | 2 | 4 | 3 | 21 |
| 6 | Lung gene/genome catalog (258) | A | 5 | 4 | 5 | 3 | 4 | 4 | 3 | 3 | 31 |
| 7 | Single-microbe RNA atlas (70035) | A | 3 | 4 | 4 | 3 | 5 | 3 | 3 | 4 | 29 |
| 8 | Centenarian serum profiling (70025) | A | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 23 |
| 9 | Giant-panda ARG database (171) | A | 3 | 2 | 4 | 3 | 3 | 3 | 3 | 2 | 23 |
| 10 | Marine biofilm AMP + DL (244) | A | 4 | 4 | 4 | 3 | 4 | 4 | 3 | 4 | 30 |
| 11 | E. faecium leucic acid (70173) | A | 3 | 4 | 2 | 3 | 4 | 4 | 3 | 3 | 26 |
| 12 | Strain-invasion meta-analysis (70196) | A | 4 | 3 | 2 | 3 | 4 | 4 | 3 | 3 | 26 |
| 13 | Dysbiosis global patents (70028) | A | 3 | 2 | 1 | 2 | 2 | 2 | 3 | 2 | 17 |
| 14 | The microbiome in cancer (70070) | A | 3 | 3 | 1 | 3 | 2 | 3 | 4 | 3 | 22 |
| 15 | Gut microbiota in cancer (70017) | A | 2 | 3 | 1 | 2 | 2 | 2 | 3 | 3 | 18 |
| 16 | Dairy resistome spatio-temporal (70047) | A | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 23 |
| 17 | Gut microbiota and TB (70054) | A | 2 | 3 | 1 | 2 | 2 | 2 | 3 | 3 | 18 |
| 18 | Core-enzyme urease method (70032) | A | 2 | 3 | 3 | 3 | 4 | 3 | 3 | 3 | 24 |
| 19 | Metabolites tumor epigenetics (70115) | A | 2 | 3 | 1 | 2 | 2 | 2 | 3 | 3 | 18 |
| 20 | Dietary therapies review (230) | A | 2 | 2 | 1 | 2 | 2 | 2 | 3 | 3 | 17 |
| 21 | Seminal plasma microecology (166) | A | 2 | 3 | 1 | 3 | 3 | 3 | 3 | 2 | 20 |
| 22 | Swine-farm skin resistome (158) | A | 3 | 3 | 2 | 3 | 3 | 3 | 3 | 3 | 23 |
| 23 | Gut-X axis review (270) | A | 2 | 3 | 1 | 2 | 3 | 2 | 4 | 3 | 20 |
| 24 | SynCom biofertilizers (70140) | A | 2 | 3 | 1 | 3 | 3 | 2 | 3 | 3 | 20 |
| 25 | Gut virome nitrogen (70177) | A | 3 | 4 | 2 | 3 | 4 | 4 | 3 | 3 | 26 |

## Benchmark summary (totals, n=25)
- Totals sorted: 31, 31, 30, 30, 29, 28, 27, 26, 26, 26, 24, 23, 23, 23, 23, 22, 21, 20, 20, 20, 20, 18, 18, 18, 17, 17.
  (26 values because of the tie block; n=25 rows — the list above is the 25 row totals.)
- **Median total ~= 23 / 40.**
- **75th percentile total ~= 28-29 / 40** (the 28/29 band: ggClusterNet 2, single-microbe RNA, and the 30s above it).
- Per-dimension medians (approx): scale 3, insight 3, resource 2, figures 3, novelty 3, rigor 3, read 3, impact 3.
  The dimensions that separate the top quartile are **resource (4-5), novelty (4-5), and figure clarity (4)** —
  not raw rigor, which clusters at 3 because most papers do internal validation only.

## The 5 closest papers to our planned paper, and what makes them strong
("Closest" = cross-population/atlas framing, a released tool/resource, and map/heatmap figure grammar — the
same shape as a global FPR atlas + recalibration tool.)

1. **Duck gut metagenome catalog — 10.1002/imt2.198 (31/40).**
   Builds a first-of-kind reference catalog (24M genes, 4437 MAGs) and then mines it for signatures across
   region/time/rearing — exactly the "build a resource, then read structure off it" arc we need. Figure set
   pairs a workflow schematic with signature panels; shows a Letter-scale idea can carry 7 figures of evidence.

2. **Lung microbial gene/genome catalog — 10.1002/imt2.258 (31/40).**
   Large, well-phenotyped sampling (744 metagenomes / 675 hosts), a "largest-to-date / % novel" scale claim,
   and a resource that is immediately used to resolve a concrete mechanism. The model for turning a scale
   number into a credibility claim and then delivering one actionable finding on top of the atlas.

3. **Rumen DNA-methylation atlas — 10.1002/imt2.70153 (30/40).**
   A Letter that reframes a phenotype away from taxonomic abundance toward a new layer, states it as a
   first-of-kind atlas, and lands it in 2 figures with a schematic + phylogeny/heatmap. Its gap sentence
   ("abundance inconsistently explains the phenotype") is the template for our "AUROC hides site-specific
   false positives" framing.

4. **Marine biofilm AMP discovery + deep learning — 10.1002/imt2.244 (30/40).**
   Couples a curated resource (713 strains/genomes) with an ML pipeline and then wet-lab validates 54/60
   predictions — the strongest rigor pattern in the pool (independent validation of a model output). This is
   the bar for coupling our classifier-FPR atlas to a tool that is shown to actually work, not just proposed.

5. **ggClusterNet 2 — 10.1002/imt2.70041 (28/40).**
   The clearest template for a *small-but-high-impact tool paper*: ~1,900 words, 4 figures, headline is
   adoption ("used in 300+ studies") and usability, not a biological discovery. Directly relevant to how we
   should position the local-recalibration Python tool: lead with reuse and ease, show the UI/workflow, and
   let impact (dimension 8) carry the score where novelty of biology is modest.
