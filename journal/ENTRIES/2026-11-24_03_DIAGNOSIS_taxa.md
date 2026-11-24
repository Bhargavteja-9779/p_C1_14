# 2026-11-24 — DIAGNOSIS / OBSERVATION (why some populations are over-flagged; P8 taxon decomposition, LASSO, strict set)
File: v4/results/taxa_shift_v4.csv, taxa_top_v4.csv. (Bug fixed before reading results: the oral-genus matcher first
read the rank prefix "s" instead of the genus; logged as a deviation.)
- The population's mean score shift tracks its FPR closely (Spearman rho: CRC 0.76, IBD 0.91, T2D 0.90, LASSO, strict set).
- IBD test: the five most over-flagged healthy populations are all Asian (GuptaA India 0.62, YachidaS Japan 0.47, QinJ
  China 0.41, DhakanDB India 0.40, JieZ China 0.34). The shift comes from LOWER abundance of taxa the model learned as
  health markers in its Western training cohorts (Gemmiger formicilis, Asaccharobacter celatus, Roseburia sp. CAG-182,
  Ruminococcus bromii). Oral taxa contribute almost nothing (<3% of the positive shift).
- T2D test: over-flagged populations are non-westernised (BritoIL Fiji 0.61, LokmerA Cameroon 0.59, PasolliE Madagascar
  0.52): Enterobacteriaceae/Escherichia, Catenibacterium, Collinsella massiliensis up; Anaerostipes hadrus down.
- CRC test (strict set): LokmerA Cameroon 0.32 via Prevotella sp. CAG-520, lower Streptococcus salivarius (negative
  weight) and Veillonella parvula. Oral taxa ~18-23% of the positive shift in the top two.
My reading: the false alarms are mostly "health markers of the training population" that are simply rarer elsewhere,
not a processing artefact. This is the mechanism the domain reviewer asked for. It is descriptive (no causal claim).
CAVEAT: v3 claimed A3 ("non-westernised over-flagged by CRC test") was falsified on the full set; the top CRC
populations in the strict set are non-westernised. I must re-test A3 on the strict set and report both, not pick one.
