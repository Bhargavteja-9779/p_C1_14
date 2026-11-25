"""Command line: fprcal {cutoff,verify,plan,atlas,score}. Scores are read from a text/CSV file (one number per line, or the
column given by --column)."""
from __future__ import annotations
import argparse, json, sys, warnings
import numpy as np
import pandas as pd
from . import core, atlas, models


def _read(path, column):
    if column is None:
        return np.loadtxt(path if path != "-" else sys.stdin, dtype=float, ndmin=1)
    return pd.read_csv(path)[column].astype(float).values


def main(argv=None):
    ap = argparse.ArgumentParser(prog="fprcal", description=__doc__)
    sp = ap.add_subparsers(dest="cmd", required=True)
    a = sp.add_parser("cutoff", help="label-free burn-in cut-off from the first N scores at a site")
    a.add_argument("scores"); a.add_argument("--column"); a.add_argument("--alpha", type=float, default=.10)
    a.add_argument("--pi-max", type=float, default=0.0); a.add_argument("--rule", choices=["expected", "pac"], default="expected")
    a.add_argument("--delta", type=float, default=.05)
    v = sp.add_parser("verify", help="check a stated FPR on local healthy people")
    v.add_argument("scores"); v.add_argument("--cutoff", type=float, required=True); v.add_argument("--column")
    v.add_argument("--alpha", type=float, default=.10); v.add_argument("--tolerance", type=float, default=.05)
    p = sp.add_parser("plan", help="burn-in size planning table")
    p.add_argument("--alpha", type=float, default=.10); p.add_argument("--pi-max", type=float, default=0.0); p.add_argument("--delta", type=float, default=.05)
    t = sp.add_parser("atlas", help="expected FPR spread of a test across healthy populations")
    t.add_argument("test", nargs="?"); t.add_argument("--model", choices=["lasso", "rf"], default="lasso")
    sc = sp.add_parser("score", help="score samples with the shipped LASSO atlas tests (research use)")
    sc.add_argument("table", help="CSV: rows = samples, columns = taxa (relative abundance in %%); --taxa-rows if transposed")
    sc.add_argument("--test", help="one test (default: all 14)"); sc.add_argument("--taxa-rows", action="store_true"); sc.add_argument("--out")
    sc.add_argument("--max-missing", type=float, default=.05,
                    help="largest allowed share of a test's total |coefficient| weight on features missing from the input (default 0.05)")
    sc.add_argument("--allow-missing", action="store_true",
                    help="score even if more weight is missing (missing features set to their training mean; a warning is printed)")
    for s in (a, v, p, t): s.add_argument("--json", action="store_true")
    x = ap.parse_args(argv)
    if x.cmd == "cutoff":
        r = core.burnin_cutoff(_read(x.scores, x.column), x.alpha, x.pi_max, x.rule, x.delta); out = r.to_dict(); txt = str(r)
    elif x.cmd == "verify":
        r = core.verify_fpr(_read(x.scores, x.column), x.cutoff, x.alpha, x.tolerance); out = r.to_dict(); txt = str(r)
    elif x.cmd == "score":
        tab = pd.read_csv(x.table, index_col=0); tab = tab.T if x.taxa_rows else tab
        try:
            with warnings.catch_warnings(record=True) as wl:
                warnings.simplefilter("always")
                if x.test:
                    s = models.score(tab, x.test, x.max_missing, x.allow_missing)
                    res = pd.DataFrame({s.name: s, "flag": (s >= s.attrs["cutoff"]).astype(int),
                                        "missing_weight": s.attrs["missing_weight"], "absent_weight": s.attrs["absent_weight"]})
                    mw = s.attrs["missing_weight"]
                    note = (f"cut-off {s.attrs['cutoff']:.4f}; missing-feature share of |w| per sample: max {mw.max():.3f} "
                            f"(limit {x.max_missing}); model clades not detected in the table (counted as 0%): "
                            f"|w| share max {s.attrs['absent_weight'].max():.3f}")
                else:
                    res = models.score_all(tab, x.max_missing, x.allow_missing)
                    mw = res.filter(like="_missing_weight").max()
                    note = ("flag = score >= training cut-off (targets FPR 0.10 on training controls; see `fprcal atlas`); "
                            f"largest missing-feature share of |w| over tests and samples: {mw.max():.3f} ({mw.idxmax().replace('_missing_weight', '')})")
        except models.MissingFeaturesError as e:
            print(f"fprcal score: error: {e}", file=sys.stderr); raise SystemExit(2)
        for w in {str(w.message) for w in wl}: print(f"WARNING: {w}", file=sys.stderr)
        if x.out: res.to_csv(x.out)
        print(res.round(4).to_string() if not x.out else f"wrote {x.out}"); print(note, file=sys.stderr); return
    elif x.cmd == "plan":
        out = core.plan(x.alpha, x.pi_max, x.delta); txt = pd.DataFrame(out).round(3).to_string(index=False)
    else:
        if not x.test:
            out = atlas.tests(); txt = "tests: " + ", ".join(out)
        else:
            out = atlas.lookup(x.test, x.model)
            txt = (f"{out['test']} ({x.model}, AUROC {out['auroc']:.2f}): pooled FPR {out['pooled_fpr']:.3f} at a 0.10 target; "
                   f"95% prediction interval for a new population {out['pi95'][0]:.3f}-{out['pi95'][1]:.3f}; I2 = {out['I2']:.2f}; "
                   f"{out['share_outside_005_015']:.0%} of {out['populations']} populations outside 0.05-0.15.\n"
                   f"highest: " + "; ".join(f"{r['study']} ({r['country']}) {r['fpr']:.2f}" for r in out["highest"]))
    print(json.dumps(out, indent=1, default=float) if x.json else txt)


if __name__ == "__main__":
    main()
