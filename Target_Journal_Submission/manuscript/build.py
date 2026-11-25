"""Build manuscript.md and supporting_information.md from *_src.md: citation keys [@a; @b] are numbered by first
appearance (main text first, then SI) and the reference list is written in that order. Run: python build.py"""
import os, re
H = os.path.dirname(os.path.abspath(__file__))
REFS = {
 "pasolli2016": "Pasolli E, Truong DT, Malik F, Waldron L, Segata N. Machine learning meta-analysis of large metagenomic datasets: tools and biological insights. PLoS Comput Biol. 2016;12:e1004977. https://doi.org/10.1371/journal.pcbi.1004977",
 "wirbel2019": "Wirbel J, Pyl PT, Kartal E, et al. Meta-analysis of fecal metagenomes reveals global microbial signatures that are specific for colorectal cancer. Nat Med. 2019;25:679-689. https://doi.org/10.1038/s41591-019-0406-6",
 "thomas2019": "Thomas AM, Manghi P, Asnicar F, et al. Metagenomic analysis of colorectal cancer datasets identifies cross-cohort microbial diagnostic signatures and a link with choline degradation. Nat Med. 2019;25:667-678. https://doi.org/10.1038/s41591-019-0405-7",
 "duvallet2017": "Duvallet C, Gibbons SM, Gurry T, Irizarry RA, Alm EJ. Meta-analysis of gut microbiome studies identifies disease-specific and shared responses. Nat Commun. 2017;8:1784. https://doi.org/10.1038/s41467-017-01973-8",
 "imperiale2014": "Imperiale TF, Ransohoff DF, Itzkowitz SH, et al. Multitarget stool DNA testing for colorectal-cancer screening. N Engl J Med. 2014;370:1287-1297. https://doi.org/10.1056/NEJMoa1311194",
 "baxter2016": "Baxter NT, Ruffin MT, Rogers MAM, Schloss PD. Microbiota-based model improves the sensitivity of fecal immunochemical test for detecting colonic lesions. Genome Med. 2016;8:37. https://doi.org/10.1186/s13073-016-0290-3",
 "toes2017": "Toes-Zoutendijk E, van Leerdam ME, Dekker E, et al. Real-time monitoring of results during first year of Dutch colorectal cancer screening program and optimization by altering fecal immunochemical test cut-off levels. Gastroenterology. 2017;152:767-775.e2. https://doi.org/10.1053/j.gastro.2016.11.022",
 "vancalster2019": "Van Calster B, McLernon DJ, van Smeden M, Wynants L, Steyerberg EW. Calibration: the Achilles heel of predictive analytics. BMC Med. 2019;17:230. https://doi.org/10.1186/s12916-019-1466-7",
 "steyerberg2004": "Steyerberg EW, Borsboom GJJM, van Houwelingen HC, Eijkemans MJC, Habbema JDF. Validation and updating of predictive logistic regression models: a study on sample size and shrinkage. Stat Med. 2004;23:2567-2586. https://doi.org/10.1002/sim.1844",
 "zhang2026": "Zhang Y, Cidan Y, Xu J, et al. CRC-TrustBench: benchmarking cross-study and cross-country generalization in gut metagenomic colorectal cancer prediction. Front Microbiol. 2026;17:1971707. https://doi.org/10.3389/fmicb.2026.1971707",
 "qiu2026": "Qiu J, Zhao YQ, Zheng Y. Shift-adjusted Neyman-Pearson classifiers via single index modeling (SACSIM). Biometrics. 2026;82:ujag138. https://doi.org/10.1093/biomtc/ujag138",
 "nearing2021": "Nearing JT, Comeau AM, Langille MGI. Identifying biases and their potential solutions in human microbiome studies. Microbiome. 2021;9:113. https://doi.org/10.1186/s40168-021-01059-0",
 "wang2020": "Wang Y, Lê Cao KA. Managing batch effects in microbiome data. Brief Bioinform. 2020;21:1954-1970. https://doi.org/10.1093/bib/bbz105",
 "gibbons2018": "Gibbons SM, Duvallet C, Alm EJ. Correcting for batch effects in case-control microbiome studies. PLoS Comput Biol. 2018;14:e1006102. https://doi.org/10.1371/journal.pcbi.1006102",
 "austin2025": "Austin GI, Brown Kav A, ElNaggar S, et al. Processing-bias correction with DEBIAS-M improves cross-study generalization of microbiome-based prediction models. Nat Microbiol. 2025;10:897-911. https://doi.org/10.1038/s41564-025-01954-4",
 "pasolli2017": "Pasolli E, Schiffer L, Manghi P, et al. Accessible, curated metagenomic data through ExperimentHub. Nat Methods. 2017;14:1023-1024. https://doi.org/10.1038/nmeth.4468",
 "wirbel2021": "Wirbel J, Zych K, Essex M, et al. Microbiome meta-analysis and cross-disease comparison enabled by the SIAMCAT machine learning toolbox. Genome Biol. 2021;22:93. https://doi.org/10.1186/s13059-021-02306-1",
 "saerens2002": "Saerens M, Latinne P, Decaestecker C. Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure. Neural Comput. 2002;14:21-41. https://doi.org/10.1162/089976602753284446",
 "alexandari2020": "Alexandari A, Kundaje A, Shrikumar A. Maximum likelihood with bias-corrected calibration is hard-to-beat at label shift adaptation. Proc Mach Learn Res. 2020;119:222-232 (ICML 2020). https://doi.org/10.48550/arxiv.1901.06852",
 "brummer2014": "Brümmer N, Garcia-Romero D. Generative modelling for unsupervised score calibration. In: Proc IEEE ICASSP 2014. p. 1680-1684. https://doi.org/10.1109/icassp.2014.6853884",
 "zheng2026": "Zheng H, Chen W. High AUROC can mask decision failure in sepsis transcriptomic classifiers: preprocessing stability outweighs post hoc calibration across cohorts. PLoS One. 2026;21:e0357585. https://doi.org/10.1371/journal.pone.0357585",
 "wilks1941": "Wilks SS. Determination of sample sizes for setting tolerance limits. Ann Math Stat. 1941;12:91-96. https://doi.org/10.1214/aoms/1177731788",
 "tong2018": "Tong X, Feng Y, Li JJ. Neyman-Pearson classification algorithms and NP receiver operating characteristics. Sci Adv. 2018;4:eaao1659. https://doi.org/10.1126/sciadv.aao1659",
 "yao2023": "Yao S, Rava B, Tong X, James G. Asymmetric error control under imperfect supervision: a label-noise-adjusted Neyman-Pearson umbrella algorithm. J Am Stat Assoc. 2023;118:1824-1836. https://doi.org/10.1080/01621459.2021.2016423",
 "bashari2025": "Bashari M, Sesia M, Romano Y. Robust conformal outlier detection under contaminated reference data. In: Proc ICML 2025. https://doi.org/10.48550/arxiv.2502.04807",
 "angelopoulos2023": "Angelopoulos AN, Bates S. Conformal prediction: a gentle introduction. Found Trends Mach Learn. 2023;16:494-591. https://doi.org/10.1561/2200000101",
 "jones2018": "Jones GRD, Haeckel R, Loh TP, et al. Indirect methods for reference interval determination - review and recommendations. Clin Chem Lab Med. 2018;57:20-29. https://doi.org/10.1515/cclm-2018-0073",
}
CITE = re.compile(r"\[@([^\]]+)\]")
order = []
def keys(m): return [k.strip().lstrip("@") for k in m.group(1).split(";")]
def collect(t):
    for m in CITE.finditer(t):
        for k in keys(m):
            assert k in REFS, f"unknown key {k}"
            if k not in order: order.append(k)
def fmt(ns):
    ns = sorted(ns); out = []; i = 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1: j += 1
        out.append(f"{ns[i]}-{ns[j]}" if j - i >= 2 else ", ".join(map(str, ns[i:j + 1]))); i = j + 1
    return ", ".join(out)
ms, si = [open(os.path.join(H, f)).read() for f in ("manuscript_src.md", "supporting_information_src.md")]
collect(ms); collect(si)
num = {k: i + 1 for i, k in enumerate(order)}
sub = lambda t: CITE.sub(lambda m: "[" + fmt([num[k] for k in keys(m)]) + "]", t)
reflist = "\n".join(f"{num[k]}. {REFS[k]}" for k in order)
unused = [k for k in REFS if k not in num]
open(os.path.join(H, "manuscript.md"), "w").write(sub(ms).replace("{{REFERENCES}}", reflist))
open(os.path.join(H, "supporting_information.md"), "w").write(sub(si))
print(f"{len(order)} references cited; unused: {unused}")
