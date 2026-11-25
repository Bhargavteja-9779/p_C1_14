# Round 10 — verification of the novelty reviewer's MAJOR concerns (2026-11-25)
1. "Ref 9 CRC-TrustBench does not resolve": WRONG. Crossref api.crossref.org/works/10.3389/fmicb.2026.1971707 returns
   "CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer
   prediction", Frontiers in Microbiology, 2026-09-25, Zhang, Cidan, Xu et al.; doi.org redirects (302). Keep; rebut.
2. "Case-mix confounding overlaps SIAMCAT's country-confounder analysis": CORRECT. SIAMCAT 2021 (PMC8008609, Fig. 2):
   UC samples only Spanish, controls Spanish + Danish; many species differ more by country than disease; AUROC 0.84 vs
   0.76 Spanish-only; Danish vs Spanish controls separable at AUROC 0.96; "confounding factors can lead to exaggerated
   performance estimates". Action for v13: credit [8] for the mechanism concept; state our contribution as its
   consequence for the FPR of a deployed, published index, quantified (OR 6.7; 64% vs 12%) and tested by retraining.
