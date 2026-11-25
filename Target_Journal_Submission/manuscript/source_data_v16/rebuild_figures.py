"""Redraw the submitted (v16) figures; Figures 1, 3, S1 are unchanged from v15 and compared with figures_v15 (identical copies in figures_v16) from the files in this folder only, and compare them with manuscript/figures_v15.

The v15 figure scripts locate their inputs relative to their own position in the repository. This script copies the four
scripts (unchanged) and the fprcal package into a temporary mirror of the repository layout, puts the source-data copies
where the scripts look for them (and nothing else), runs the scripts there and compares the PNGs pixel by pixel with the
published ones. The repository itself is not written to.

    python Target_Journal_Submission/manuscript/source_data_v16/rebuild_figures.py [--out DIR] [--keep]

Needs the environment in environment.yml (Figure 1 also needs geopandas)."""
from __future__ import annotations
import argparse, os, shutil, subprocess, sys, tempfile
import numpy as np

SD = os.path.dirname(os.path.abspath(__file__))
TJS = os.path.normpath(os.path.join(SD, "..", ".."))
ATL = os.path.join(TJS, "code", "experiments", "atlas")
# (script relative to code/experiments/atlas, outputs relative to Target_Journal_Submission/manuscript)
SCRIPTS = [("v5/make_fig_atlas_v15.py", ["figures_v15/figure1_atlas.png"]),
           ("v6/make_fig_gmwi2_v16.py", ["figures_v16/figure2_published_test.png"]),
           ("v5/make_fig_site_v15.py", ["figures_v15/figure3_site.png", "figures_v15/figureS1_site_methods.png"]),
           ("make_graphical_abstract_v16.py", ["graphical_abstract/graphical_abstract_v16.png"])]
# source-data file -> where the scripts read it (relative to the mirror root = repository root)
A = "Target_Journal_Submission/code/experiments/atlas/"
PLACE = {
    "figure1/atlas_perpop_strict_v5.csv": "Target_Journal_Submission/code/tool/fprcal/data/atlas_perpop_strict_v5.csv",
    "figure1/v5_perpop_strict.csv": A + "v5/results/v5_perpop_strict.csv",
    "figure1/v5_het_strict.csv": A + "v5/results/v5_het_strict.csv",
    "figure1/v5_popindex_strict_lasso.csv": A + "v5/results/v5_popindex_strict_lasso.csv",
    "figure1/ne_110m_admin_0_countries.zip": A + "v5/data/ne_110m_admin_0_countries.zip",
    "figure2/gmwi2_results.json": A + "v6/results/gmwi2_results.json",
    "figure2/gmwi2_published_training_perstudy.csv": A + "v6/results/gmwi2_published_training_perstudy.csv",
    "figure2/gmwi2_perpop_strict.csv": A + "v6/results/gmwi2_perpop_strict.csv",
    "figure2/gmwi2_eastasia_taxa.csv": A + "v6/results/gmwi2_eastasia_taxa.csv",
    "figure2/v6b_perstudy_naive.csv": A + "v6/results/v6b_perstudy_naive.csv",
    "figure2/v6b_perstudy_balanced.csv": A + "v6/results/v6b_perstudy_balanced.csv",
    "figure2/v6b_results.json": A + "v6/results/v6b_results.json",
    "figure2/sampleMetadata.csv.gz": "data/sampleMetadata.csv.gz",
    "figure3/v5_h4_units.csv": A + "v5/results/v5_h4_units.csv",
    "figure3/deploy_v4_cc_summary.csv": A + "v4/results/deploy_v4_cc_summary.csv",
    "figureS1/verify_power_v5.csv": A + "v5/results/verify_power_v5.csv",
    # graphical abstract: identical copies of files above (same paths in the mirror; checked to be byte-identical)
    "graphical_abstract/v5_perpop_strict.csv": A + "v5/results/v5_perpop_strict.csv",
    "graphical_abstract/gmwi2_published_training_perstudy.csv": A + "v6/results/gmwi2_published_training_perstudy.csv",
    "graphical_abstract/v5_h4_units.csv": A + "v5/results/v5_h4_units.csv",
}


def same_png(a, b):
    import matplotlib.image as mpimg
    x, y = mpimg.imread(a), mpimg.imread(b)
    if x.shape != y.shape: return False, f"size {x.shape[:2]} vs {y.shape[:2]}"
    d = np.abs(x.astype(float) - y.astype(float)); return bool(d.max() == 0), f"max pixel diff {d.max():.4f}, {np.mean(d.max(axis=-1) > 0):.2%} pixels differ"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", help="copy the redrawn PNG/PDF files here"); ap.add_argument("--keep", action="store_true", help="keep the mirror")
    x = ap.parse_args()
    root = tempfile.mkdtemp(prefix="srcdata_v16_"); ok_all = True
    try:
        for src, dst in PLACE.items():
            d = os.path.join(root, dst); os.makedirs(os.path.dirname(d), exist_ok=True)
            if os.path.exists(d):
                assert open(d, "rb").read() == open(os.path.join(SD, src), "rb").read(), f"{src} differs from its twin"
            else: shutil.copy(os.path.join(SD, src), d)
        tool = os.path.join(root, "Target_Journal_Submission/code/tool/fprcal")
        for f in os.listdir(os.path.join(TJS, "code", "tool", "fprcal")):          # package code (not data) for Fig 3/S1
            if f.endswith(".py"): shutil.copy(os.path.join(TJS, "code", "tool", "fprcal", f), tool)
        man = os.path.join(root, "Target_Journal_Submission", "manuscript")
        for sub in ("figures_v15", "figures_v16", "graphical_abstract"): os.makedirs(os.path.join(man, sub), exist_ok=True)
        for script, outs in SCRIPTS:
            s = os.path.join(root, A, script); os.makedirs(os.path.dirname(s), exist_ok=True); shutil.copy(os.path.join(ATL, script), s)
            r = subprocess.run([sys.executable, s], cwd=os.path.dirname(s), capture_output=True, text=True)
            if r.returncode:
                ok_all = False; print(f"FAILED {script}:\n{r.stderr[-2000:]}"); continue
            for o in outs:
                same, msg = same_png(os.path.join(man, o), os.path.join(TJS, "manuscript", o))
                print(f"{'IDENTICAL' if same else 'DIFFERENT'}  {o}  ({script}; {msg})"); ok_all &= same
                if x.out:
                    os.makedirs(x.out, exist_ok=True)
                    for e in (".png", ".pdf"): shutil.copy(os.path.join(man, o[:-4] + e), x.out)
    finally:
        if x.keep: print("mirror kept at", root)
        else: shutil.rmtree(root, ignore_errors=True)
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
