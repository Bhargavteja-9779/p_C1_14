# style_v3.md — How iMeta Letters and short articles are written (quantified)

Scope: built from 12 full-text iMeta papers I parsed from Europe PMC / NCBI PMC (2024-2026), plus
abstracts of the wider 2024-2026 pool. Papers overlapping the committed benchmark_v2 set were still
read for style, but are not re-listed in papers.csv (per coordinator instruction). Numbers below are
measured from main-text body (figures/tables/back-matter excluded) unless marked UNVERIFIED.

## 1. Two formats, one house style
- **Letter** (`jats_article_type = letter`): opens literally "To the Editor,". ~1,900-2,700 main-text
  words, 2 figures, ~16-20 references, NO Highlights box, usually NO standalone Methods in main text
  (one line pointing to Supporting Information). Examples measured: MDIPID 2,648 w / 2 fig / 20 ref
  (10.1002/imt2.70019); rumen methylation 2,038 w / 2 fig / 16 ref (10.1002/imt2.70153); BIOME cohort
  1,892 w / 2 fig / 19 ref (10.1002/imt2.70106).
- **Research article** (`research-article`): 2,800-5,700+ main-text words, 4-7 figures, 36-192 refs,
  has a Highlights box (3-4 bullets) and often a short METHODS section. Examples: MetOrigin 2.0
  3,262 w / 4 fig / 36 ref; RA biobank 3,589 w / 4 fig / 59 ref; duck catalog 4,798 w / 7 fig / 87 ref;
  CRC tissue multi-omics 5,740 w / 7 fig / 192 ref.
- A resource/tool Letter and a resource/tool article read almost identically; the type mostly changes
  length, figure count and whether a Highlights box exists. **An atlas/tool paper lives comfortably as a
  Letter**: 2 figures is the norm, not a limitation.

## 2. Title patterns (measured on this pool)
- Median title length ~13 words (range 8-20). Two dominant templates:
  1. **"ToolName: what it does"** — colon format for every resource/tool/database/cohort paper.
     e.g. "MDIPID: Microbiota-drug interaction and disease phenotype interrelation database";
     "MetOrigin 2.0: Advancing the discovery of microbial metabolites and their origins";
     "BIOME cohort: Multi-system microbiome dynamics and clinical outcomes in massive burn injury patients";
     "MASH-Ocean 1.0: Interactive platform for investigating microbial diversity, function, and biogeography".
     Named tools carry a version number (2.0, 1.0) and an expanded acronym.
  2. **Finding-as-a-sentence** — "X reveals/links/induces/mediates Y".
     e.g. "Microbial DNA methylation links rumen transcriptional activity to methane emission divergence";
     "Duck gut metagenome reveals the microbiome signatures linked to..."; "Spinal cord injury induces acute
     microbiome shock and system-wide transcriptomic reprogramming".
- Our working title ("An atlas of the false-positive rate of 14 gut-microbiome disease classifiers across
  36 healthy populations in 20 countries") fits template 2 but is long; an iMeta-style compression plus a
  named tool (template 1 for the recalibration tool) is the register to aim for.

## 3. Opening (first 150-250 words) — a fixed 3-move structure
Move 1: a **real-world / clinical / economic stake in the first sentence**, almost always with a number or
a superlative, and a citation.
- "Colorectal cancer (CRC) is the third most common cancer worldwide, accounting for ~10% of all cancer
  diagnoses..." (10.1002/imt2.70090)
- "The World Health Organization (WHO) predicts that the global population aged 60 years old and over will
  reach 2.1 billion by 2050..." (10.1002/imt2.70134)
- "Methane (CH4) produced during ruminal fermentation is a major source of greenhouse gas emissions from
  dairy production and represents an energetic loss to the host animal." (10.1002/imt2.70153)

Move 2: **the specific gap**, often with "However," and a statement that prior work is partial, heterogeneous,
or abundance-only.
- "However, investigations on TMAO have mainly been conducted in individuals with a high risk of CVD... while
  studies on the general population are comparatively scarcer." (10.1002/imt2.183)
- "However, differences in microbial taxonomic abundance inconsistently explain variation in methane output
  across animals, highlighting a potential role for microbial functional regulation beyond community structure
  alone." (10.1002/imt2.70153)

Move 3: a **"Here, we ..." / "In this study, we ..."** sentence that states what was built and the single
headline result, with the key number and a Figure 1 pointer.
- "Here, we integrated Oxford Nanopore Technologies long-read sequencing to systematically characterize the
  methylome of the dairy cow rumen microbiome at the metagenome-assembled genome level." (10.1002/imt2.70153)
- "In this study, the Microbiota-Drug Interaction and Disease Phenotype Interrelation Database (MDIPID) was
  therefore introduced to systematically collect... (Figure 1)." (10.1002/imt2.70019)
Letters compress Moves 1-3 into the two untitled paragraphs after "To the Editor,".

## 4. Headings — declarative, not generic
- Research articles use INTRODUCTION / RESULTS / DISCUSSION / CONCLUSION / METHODS (all caps).
- But **subheadings are full findings**, not topic labels:
  "Incident clinical outcomes are associated with TMAO precursors but not with TMA" (10.1002/imt2.183);
  "Microbial community stratification reveals adenoma-to-carcinoma ecological shifts" (10.1002/imt2.70090).
- Letters replace generic headings with ALL-CAPS finding sentences used directly as section titles:
  "METABOLIC REALLOCATION CHARACTERIZES LOW METHANE-EMITTING DAIRY COWS";
  "A GENOME-RESOLVED REFERENCE CATALOG REVEALS HIGH-QUALITY RECONSTRUCTION OF THE RUMEN MICROBIOME"
  (both 10.1002/imt2.70153). Cohort Letters instead use operational headings (STUDY DESIGN, RECRUITMENT,
  BIOLOGICAL SAMPLING PROCEDURES, PROGRESS OF THE COHORT, DISCUSSION — 10.1002/imt2.70106).
- Section-closing sentences are formulaic: "Together, these results...", "Collectively, these findings...",
  "In summary, ...". These appear once per subsection and restate the finding in plain words.

## 5. Figure design (2 figures do a lot of work)
- **Figure 1 almost always contains a schematic/workflow panel (panel A)** — "Schematic overview of this
  study..." (10.1002/imt2.70090); "Overview of study design and performed analyses" (10.1002/imt2.183);
  "Experimental design and rumen metabolic phenotype" (10.1002/imt2.70153). Build the workflow as a drawn
  panel, not prose.
- **Geography is shown as a map.** Cohort/atlas papers lead with a map panel: "Cohort map... across 50
  hospitals spanning 28 provinces" and "Enrollment map showing the geographic distribution... circle sizes
  proportional to the number of enrolled patients" (10.1002/imt2.70106); MASH-Ocean and MASS likewise lean
  on biogeography/site maps. **This is directly our play: a 20-country / 36-population map is squarely in
  house style.**
- **Heatmaps carry the multivariate results.** "Heatmap showing results of the association analysis between
  metabolites and gut microbial taxa" (10.1002/imt2.183); correlation heatmaps in CRC and centenarian papers.
  Our 14x36 FPR matrix as a heatmap is exactly the expected figure grammar.
- Panels are dense (6-10 per figure) and labeled A-H; captions name every panel and spell out every acronym.
- Vector multi-panel figures; a tool paper shows a UI screenshot panel ("Screen shot of quick search for
  'acetate'", 10.1002/imt2.246).

## 6. Number density and statistics
- Measured numbers-per-100-words of body text: tool/cohort Letters run low (MDIPID 3.5, MASH-Ocean 3.6,
  BIOME 4.9, MetOrigin 4.6, ggClusterNet 5.7); data/mechanism articles run high (RA biobank 13.3, CRC tissue
  14.4). Resource papers front-load counts ("6669 MMDR records... 2708 species, 1818 drugs, 482 diseases").
- In-text effect sizes are reported with the number inline ("a 17% increase in risk for CVD events",
  10.1002/imt2.183). CIs and corrected p-values appear in text when inferential (Bonferroni p < 8.33e-9).
- Named tests are standard and listed plainly: PERMANOVA/Adonis, Wilcoxon/Kruskal-Wallis, MaAsLin2,
  random forest, FDR/BH. Little hype vocabulary; claims are hedged ("may", "probably", "suggest").

## 7. How limitations and methods are handled
- **Limitations: 1-3 plain sentences near the end**, often enumerated. "Despite these strengths, we
  acknowledge certain limitations. First, ... potential biases in geographical location and gender may limit
  generalizability. Second, ..." (10.1002/imt2.70106). CRC article: "We acknowledge that our findings
  represent observational associations that require further mechanistic validation... relying on
  transcriptomic data for external validation of protein biomarkers is a limitation." (10.1002/imt2.70090).
  Tone is candid, not defensive; each limitation is one sentence.
- **Methods**: Letters push methods entirely to Supporting Information (one pointer line). Research articles
  keep a condensed METHODS (measured 191-3,973 words); the longest methods belong to population/multi-omics
  papers (TMAO 2,694; CRC 3,973; centenarian 2,812). A tool/atlas paper can keep main-text methods near zero.
- **Back matter order** (consistent): AUTHOR CONTRIBUTIONS -> CONFLICT OF INTEREST -> ETHICS STATEMENT ->
  (AI statement in 2026 papers) -> DATA AVAILABILITY (GitHub URL + data accession) -> ORCID -> REFERENCES ->
  SUPPORTING INFORMATION. A GitHub/web URL in Data Availability is effectively mandatory for resource papers.
- Graphical abstract + ~100-word summary for all; Highlights box only for research articles.

## 8. Five short quotable exemplar sentences (with DOIs)
1. "Here, we integrated Oxford Nanopore Technologies long-read sequencing to systematically characterize the
   methylome of the dairy cow rumen microbiome at the metagenome-assembled genome level." — 10.1002/imt2.70153
   (the "Here, we" headline move).
2. "However, differences in microbial taxonomic abundance inconsistently explain variation in methane output
   across animals, highlighting a potential role for microbial functional regulation beyond community
   structure alone." — 10.1002/imt2.70153 (the gap move; abundance-is-not-enough framing).
3. "Despite these strengths, we acknowledge certain limitations. First, ... potential biases in geographical
   location and gender may limit generalizability." — 10.1002/imt2.70106 (enumerated, one-sentence
   limitations — and note geography framed as a bias, which our atlas directly addresses).
4. "Overall, MDIPID comprises a comprehensive and interconnected network, covering 1818 drugs/substances,
   2708 microbial species, 482 diseases, and 592 microbial proteins." — 10.1002/imt2.70019 (resource papers
   restate scale as a one-line count sentence).
5. "Together, these data highlight intratumoral microbiome dysbiosis in CRC compared with adenomas, while
   indicating that microbial community structures are broadly conserved between early- and advanced-stage
   tumors." — 10.1002/imt2.70090 (the "Together, these ... while ..." closing sentence that states finding +
   nuance in one line).
