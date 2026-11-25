# Referee report — Novelty & Related Work (iMeta Letter)

**Manuscript:** manuscript_v12.md — "Gut-microbiome classifiers flag healthy people at population-specific rates…"
**Reviewer role:** Independent referee, novelty and prior art.
**Score:** 8/10
**Decision:** Minor revision.

## Summary judgement

The core contributions are genuinely new as a package: (i) a systematic *false-positive-rate* atlas of 28 classifiers across 36 unseen healthy populations at a fixed cut-off; (ii) an audit showing a *published, deployed* index (GMWI2) mislabels whole regions **inside its own training data**; (iii) a retraining experiment that pins the cause to geographic case-mix imbalance; and (iv) a label-free, site-level recalibration rule with exact guarantees. I could not find prior work that reports any of (i)–(iii). The manuscript is unusually disciplined about hedging — it labels post hoc analyses, reports failed pre-specified hypotheses (AUROC cost exceeding the margin; non-replicating distance findings), and explicitly disclaims novelty where due (conformal/reference-limit rule, DEBIAS-M/MMUPHin). The key citations check out: GMWI2 [22], *B. plebeius* seaweed-enzyme transfer [23], DEBIAS-M [19], MMUPHin [20], SIAMCAT [8], Piccinno [3] and Poyet [10] all resolve on Crossref with matching titles/venues. The main residual issues are (a) one citation I could not verify exists, and (b) under-crediting SIAMCAT and shortcut-learning work for the *confounding mechanism itself*, which the manuscript frames as if newly named.

## Claim → closest prior work → difference

| Claim in manuscript | Closest prior work | Exact difference |
|---|---|---|
| Fixed cut-off gives wildly different FPR per population (0–77%); I² atlas of 28 classifiers, 36 populations | SIAMCAT [8] (Wirbel 2021): external controls raise false positives / weaken specificity; "control augmentation" fix. [doi.org/10.1186/s13059-021-02306-1](https://doi.org/10.1186/s13059-021-02306-1) | SIAMCAT shows *that* transfer inflates FPR and offers a training fix; it does not quantify per-population FPR heterogeneity (I², prediction intervals) across 14 diseases, nor show AUROC fails to predict portability. This is new. |
| GMWI2 mislabels East Asian healthy people (64% vs 12%), even in training data | GMWI2 paper [22] (Chang 2024). [doi.org/10.1038/s41467-024-51651-9](https://doi.org/10.1038/s41467-024-51651-9) | GMWI2 reports pooled balanced accuracy; it never breaks down FPR by region or flags the East-Asian failure. The re-analysis of the developers' *own* published scores is new and striking. |
| "Geographic case-mix confounding": pooled training encodes region-typical commensals as disease markers | SIAMCAT [8] Denmark/Spain UC confounder example; shortcut-learning in pooled multicountry data (e.g., Microbial-Keratitis preprint, [arxiv.org/pdf/2607.03740](https://arxiv.org/pdf/2607.03740)); case-mix matching (Nat 2020). | The mechanism (country confounded with case status → shortcut) is *known*. Novelty is the quantitative case-mix OR (6.7), the retraining-with-country-balancing test (88% gap reduction), and tying it to a deployed index — not the concept. Manuscript should credit SIAMCAT's confounder analysis more explicitly here. |
| *B. plebeius* carries a "disease" weight despite being a healthy East-Asian commensal | Hehemann 2010 [23]; East-Asian-distinct microbiome (eLife 2021, [elifesciences.org/articles/70349](https://elifesciences.org/articles/70349)). | Correctly cited as a diet/geography marker. Using it as a worked example of a mis-weighted commensal is new and well supported. |
| Label-free burn-in recalibration (order statistic / conformal), exact Beta FPR | Lei [14], Bates [15], Tong [16]; refineR/reference-limit [17]. | Explicitly disclaimed as not new ("laboratory medicine sets reference limits in a similar way"). Appropriately hedged; novelty is only the within-site-vs-across-site test. No over-claim. |
| Country-balanced reweighting at training time reduces FPR heterogeneity | Case-mix-shift reweighting (BMC MRM 2025); DEBIAS-M [19]; MMUPHin [20]. | Related reweighting ideas exist; manuscript concedes it is "not a clean deployment fix" and did not run DEBIAS-M/MMUPHin/ConQuR. Honest. |

## Concerns

**MAJOR**

1. **Reference 9 (CRC-TrustBench, *Front Microbiol* 2026, DOI 10.3389/fmicb.2026.1971707) does not resolve on Crossref and does not surface in web search.** It supports "CRC models lose calibration across countries." The manuscript does not depend on it, but a Letter should not cite an unverifiable source. *Resolution:* confirm the DOI/paper exists (Frontiers indexing can lag; if it is a 2026 article, provide a working link), or replace with an established cross-country CRC-transfer reference (e.g., Wirbel 2019 [1] / Thomas 2019 [2], which already demonstrate LOSO calibration loss). If it cannot be verified, remove it.

2. **The named mechanism "geographic case-mix confounding" is presented as original coinage without crediting that SIAMCAT [8] already demonstrated country-confounded case-control structure** (controls from one country, cases from another) producing spurious signal. The manuscript cites [8] only for FPR inflation and control augmentation, not for the confounding insight it shares. *Resolution:* add one sentence acknowledging SIAMCAT's confounder analysis (and optionally host-matching work) as the origin of the mechanism, and frame the contribution as *quantifying and deploying* it rather than discovering it. This strengthens, not weakens, the paper.

**MINOR**

3. "Predictors trained on industrialised populations lose accuracy elsewhere [10]" (Poyet, *Cell* 2026) — citation resolves, but check the published version actually makes a *predictive-accuracy* claim rather than only descriptive microbiome shifts; reword if it is descriptive. *Resolution:* verify the sentence against the final text.

4. The claim that balancing is "not specific to GMWI2" rests on five disease classifiers with modest CIs (−0.23 to −0.03). Fine as stated (pre-specified), but consider softening "confirming" to "supporting." *Resolution:* one-word edit.

5. Consider citing a shortcut-learning / geographic-confounding analogue from outside microbiome (e.g., the multicountry keratitis preprint) to situate the mechanism in the broader ML-generalisation literature. Optional. *Resolution:* author discretion.

## Sources checked

Crossref DOI resolution: refs 3, 8, 10, 19, 20, 22, 23 (all matched); ref 9 **not found**. Web search (8 phrasings): GMWI2 validation (PMC11358288), SIAMCAT confounder/control-augmentation, *B. plebeius*/*Phocaeicola plebeius* geography (PMC4542028, eLife 70349), microbiome transportability/specificity (gut.bmj, SIAMCAT), label-free recalibration & clinical model updating (UPA Nat Commun 2023, weighted conformal medRxiv 2023, case-mix-shift BMC MRM 2025), DEBIAS-M/MMUPHin, CRC-TrustBench (no match).
