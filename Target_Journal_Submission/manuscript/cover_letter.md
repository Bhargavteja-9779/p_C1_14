[Date]

The Editors
*iMeta*

Dear Editors,

We submit our manuscript, **"Microbiome colorectal cancer tests lose specificity at new sites; local recalibration restores it"**, for consideration as a Letter in *iMeta*.

Stool metagenomic classifiers for colorectal cancer are validated by AUROC, but a test in use works at one cut-off. Earlier work showed that CRC signatures can fire in other diseases (Wirbel et al. 2021; Thomas et al. 2019). For a microbiome journal, the Letter connects a deployment problem to its microbial basis (oral-origin marker taxa, metformin) and provides an open tool. It asks what this means for the specificity a fixed cut-off actually delivers, and how to restore it without a new labelled study.

- **Specificity does not travel.** A CRC test cut-off set for 90% specificity gave false-positive rates from 0% to 37% across 11 CRC cohorts, far beyond sampling noise (overdispersion p < 10^-15), and the same happened for IBD and type 2 diabetes classifiers. A simple batch correction reduced this spread but did not remove it.
- **Which patients are over-flagged depends on the setting, through two routes.** In severe disease (cirrhosis, atherosclerosis), hallmark CRC taxa of oral origin explained most of the excess. In a locked cardiometabolic cohort, the excess in type 2 diabetes was largely explained by medication: metformin users were flagged 2.4 times as often as non-users (exploratory). People with mild cardiometabolic labels inside CRC cohorts were not over-flagged.
- **Local recalibration restores specificity.** At stable, well-sampled sites, a label-free local cut-off with a prevalence bound is sufficient, including in an evaluation without resampling and under a real country-by-country shift. A rule that uses only colonoscopy outcomes of test-positive people, with a finite-sample guarantee, additionally recovers from large score drift and stays efficient at higher prevalence. Both rules and a site audit are released as an open-source package (cutoffguard).

All methods and endpoints were fixed in a protocol, frozen in a time-stamped commit before the held-out sites were analysed once. A later medication analysis was frozen the same way before it was run. We report every result, including hypotheses that were not supported, and we label post hoc analyses as such. All data are public, and the code, protocols and development log are openly available.

This manuscript has not been published and is not under consideration elsewhere. All authors approved the submission. The authors declare no conflicts of interest and received no specific funding. The use of AI-assisted technologies is declared in the manuscript.

Sincerely,

[Second Author] (corresponding author), on behalf of all authors
Vellore Institute of Technology (VIT), Vellore 632014, Tamil Nadu, India
Email: [corresponding author email]
