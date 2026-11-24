# Benchmark v2 - iMeta 2024-2026 papers relevant to a cross-cohort microbiome classifier-calibration study

Built 2026-11-24. All 45 papers in `benchmark_v2.csv` were retrieved from OpenAlex (journal source S4220650979)
and their DOIs were resolved in Crossref (45/45 OK, container "iMeta"). 43/45 full texts were parsed from
Europe PMC `fullTextXML`; 2 (imt2.201 MASH-Ocean, imt2.229 tigeR) had no retrievable full text, so their figure/word
fields are marked UNVERIFIED. Wiley onlinelibrary was not used.

## How the set was built (scripts in `scripts/`)
1. `01_fetch_openalex.py` - all iMeta works with publication date >= 2024-01-01 (334 records: 267 articles, 21 reviews,
   rest paratext/editorial/errata). Crossref (335) and Europe PMC (314) totals agree, so the pool is essentially complete.
2. `02_screen.py` - keyword relevance screen (ML, diagnosis, multi-cohort, atlas/resource, batch/reproducibility,
   geography/population, gut, disease) on title+abstract -> `raw/screen_ranked.json`.
3. Manual selection of 51 candidates, then 45 kept (dropped: off-topic perspective/review pieces and mouse-only work).
4. `03b_fetch_xml_parallel.py` - Europe PMC metadata + full-text XML (`raw/xml/`). (`03_fetch_fulltext.py` was the first,
   slower serial version; it was stopped after Europe PMC 503 errors.)
5. `04_parse_xml.py` - main-text word count (body sections minus back matter, figure captions and tables; includes
   Methods for Research Articles), number of main figures, panels per figure (max panel letter in caption; single-panel = 1),
   references, headings. `05_extract_avail.py` - data-availability text, scale and limitation sentences.
6. `07_crossref_verify.py` - DOI verification. `08_build_csv.py` - builds the CSV; the descriptive columns
   (data scale, methods, tool, headline, strength) were written by hand from the retrieved abstracts/full texts.
7. `09_scores.py` - scorecard scores and percentiles.

## Composition (relevance_group)
- A (21): human-microbiome ML / diagnosis / multi-cohort / population variation.
- B (3): cohort-profile Letters (MASS, Western China Birth Cohort, BIOME).
- C (12): resources, databases, platforms, pipelines, atlases.
- D (5): non-microbiome ML or multi-cohort predictors / benchmarks / population-difference papers.
- E (4): reproducibility and geography papers.
- 18 of 45 DOIs also appear in the v1 benchmark (`../journal_benchmark.csv`), kept because they are among the most
  relevant; 27 are new.

## Format facts (from parsed full text)
| Format | n | Main-text words (median, range) | Main figures (median) | Panels total (median) | Refs (median) | OpenAlex cites (median) |
|---|---|---|---|---|---|---|
| Letter (incl. JATS "article-commentary" Letters) | 18 | 1,934 (992-2,487) | 2 | 9.5 | 19 | 6 |
| Research Article | 25 | 6,048 (3,045-10,386) | 6 | 25 | 65 | 16 |

Word counts are approximate (Europe PMC renders back matter inside `<body>`, which the parser removes by heading).
Panel counts are estimates from caption letters.

## What the most relevant set shows
- **No iMeta 2024-2026 paper studies false-positive rate or calibration drift of microbiome classifiers across healthy
  populations.** The nearest analogues are: the cross-cohort periodontitis signature (imt2.212: 8 cohorts, 5 countries,
  cohort-transfer AUC matrix + LODO), the guild-based HCC classifier that frames taxon-level irreproducibility as the
  problem (imt2.70123), the 14-region hypertension meta-analysis (imt2.268), and the AI-readiness audit (imt2.70192).
  This supports novelty but also means reviewers will have no in-journal template for specificity/FPR as the endpoint;
  define it carefully.
- Classifier papers report AUROC almost exclusively; none report specificity at a fixed cut-off per population. Our
  FPR-at-fixed-threshold atlas is a different, more clinical, quantity, and it should be explained as such.
- Cross-cohort generalisation is shown as a train x test AUC heatmap (imt2.212) or as external validation cohorts
  (imt2.70123, imt2.70090, imt2.70011). Reporting weaker external results honestly (imt2.70090 shows 0.735) is accepted.
- Geography is shown with a world/China map panel (imt2.212 Fig 1A, imt2.169 Fig 1A, imt2.218, imt2.70106, imt2.70192 Fig 2).
- Resource value is rewarded with citations: the top-cited 2024-2026 items are tools/platforms (Wekemo 325, iMLGAM 152,
  Lachnospiraceae resource 79, EasyMetagenome 65, MetOrigin 2.0 63). A released calibration tool/package raises reach.
- Letters with a single big number and a call to action (imt2.70192: 5.9% / 85.5%) fit the format well.
- Most human-cohort papers have restricted individual metadata ("available on request"); papers that release code and
  derived tables (Code Ocean, GitHub) stand out on openness.

## Caveats
- Citation counts are OpenAlex `cited_by_count` on 2026-11-24 and favour 2024 papers.
- Article type: iMeta Letters are tagged in JATS as `letter` (2025-2026) or `article-commentary` (2024 and some 2025);
  "To the Editor" opening was used as the deciding signal. imt2.201 and imt2.229 types are UNVERIFIED.
- Data-scale numbers come from abstracts or full-text sentences; where a number was not stated it is marked UNVERIFIED.
