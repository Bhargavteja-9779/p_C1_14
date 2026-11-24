"""Command line: fprcal {cutoff,verify,plan,atlas}. Scores are read from a text/CSV file (one number per line, or the
column given by --column)."""
from __future__ import annotations
import argparse, json, sys
import numpy as np
import pandas as pd
from . import core, atlas


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
    for s in (a, v, p, t): s.add_argument("--json", action="store_true")
    x = ap.parse_args(argv)
    if x.cmd == "cutoff":
        r = core.burnin_cutoff(_read(x.scores, x.column), x.alpha, x.pi_max, x.rule, x.delta); out = r.to_dict(); txt = str(r)
    elif x.cmd == "verify":
        r = core.verify_fpr(_read(x.scores, x.column), x.cutoff, x.alpha, x.tolerance); out = r.to_dict(); txt = str(r)
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
