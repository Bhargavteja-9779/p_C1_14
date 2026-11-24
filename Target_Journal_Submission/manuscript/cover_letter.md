[Date]

The Editors
*iMeta*

Dear Editors,

We submit our manuscript, **"Gut microbiome colorectal cancer classifiers lose specificity across sites and patient groups, and local recalibration restores it"**, for consideration as a Letter in *iMeta*.

Stool metagenomic classifiers for colorectal cancer are validated by AUROC, but a test in use works at one cut-off. Earlier work showed that CRC signatures can fire in other diseases (Wirbel et al. 2021; Thomas et al. 2019). Our Letter asks what this means for the specificity a fixed cut-off actually delivers, and how to restore it without a new labelled study.

- **Specificity does not travel.** Cut-offs set for 90% specificity gave false-positive rates from 0% to 75% across 16 held-out sites (11 cohorts, four diseases). A simple batch correction reduced this spread but did not remove it.
- **Which patients are over-flagged depends on the setting, through two routes.** In severe disease (cirrhosis, atherosclerosis), hallmark CRC taxa of oral origin explained most of the excess. In a locked cardiometabolic cohort, the excess in type 2 diabetes was largely explained by medication: metformin users were flagged 2.4 times as often as non-users (exploratory). People with mild cardiometabolic labels inside CRC cohorts were not over-flagged.
- **Local recalibration restores specificity.** We compare label-free and outcome-based rules and report honestly where each works. A rule that uses only colonoscopy outcomes of test-positive people carries a finite-sample guarantee and adds recovery from score drift, per-group control and a high-confidence option. We release it as an open-source package (cutoffguard).

All methods and endpoints were fixed in a protocol, frozen in a time-stamped commit before the held-out sites were analysed once. A later medication analysis was frozen the same way before it was run. We report every result, including hypotheses that were not supported, and we label post hoc analyses as such. All data are public, and the code, protocols and development log are openly available.

This manuscript has not been published and is not under consideration elsewhere. All authors approved the submission. The authors declare no conflicts of interest and received no specific funding. The use of AI-assisted technologies is declared in the manuscript.

Sincerely,

[Second Author] (corresponding author), on behalf of all authors
Vellore Institute of Technology (VIT), Vellore 632014, Tamil Nadu, India
Email: [corresponding author email]
