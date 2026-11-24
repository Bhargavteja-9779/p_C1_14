#!/usr/bin/env python3
"""G11 integrity audit: every decimal number / percentage in a manuscript must match a value in a result file.
usage: audit_numbers.py MANUSCRIPT.md [results dirs...]   (defaults: v4 + v3 atlas results)
A number matches if some result value rounds to it at the same number of decimals (percentages are also tried /100).
Integers >= 1000 (counts) are checked too; small integers, years and citation/figure numbers are skipped.
Exit code 1 if anything is unmatched. Writes logs/audit_<name>.txt."""
import sys, os, re, json, glob, gzip, math
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
man = sys.argv[1]
dirs = sys.argv[2:] or [os.path.join(R, "Target_Journal_Submission/code/experiments/atlas/v4/results"),
                         os.path.join(R, "Target_Journal_Submission/code/experiments/atlas/results"),
                         os.path.join(R, "Target_Journal_Submission/journal_selection")]
NUM = re.compile(r"(?<![\w.])-?\d[\d,]*\.?\d*%?")
vals = set()
def add(x):
    try: f = float(x)
    except Exception: return
    if math.isnan(f) or math.isinf(f): return
    for v in (f, abs(f), f * 100, abs(f) * 100):
        for d in range(0, 5): vals.add(round(v, d))
for d in dirs:
    for p in glob.glob(os.path.join(d, "**", "*"), recursive=True):
        if os.path.isdir(p) or not re.search(r"\.(csv|json|md|txt|csv\.gz)$", p): continue
        op = gzip.open if p.endswith(".gz") else open
        if os.path.getsize(p) > 50e6: continue
        try:
            with op(p, "rt") as fh:
                for tok in re.findall(r"-?\d+\.?\d*(?:e-?\d+)?", fh.read()): add(tok)
        except Exception: pass
text = open(man).read()
text = re.split(r"\n#+\s*REFERENCES|\n#+\s*References", text)[0]          # reference list not audited
text = re.sub(r"\(\s*(?:Fig|Figure|Table|S)[^)]*\)", " ", text)       # figure/table refs
text = re.sub(r"\[[\d,\-– ]+\]", " ", text)                           # citation numbers
text = re.sub(r"10\.\d{4,}/\S+", " ", text)                           # DOIs
bad, n = [], 0
for line_no, line in enumerate(text.splitlines(), 1):
    for m in NUM.finditer(line):
        tok = m.group(0); pct = tok.endswith("%"); s = tok.rstrip("%").replace(",", "")
        if s in ("", "-"): continue
        f = float(s); dec = len(s.split(".")[1]) if "." in s else 0
        if dec == 0 and not pct and (abs(f) < 1000 or 1900 <= f <= 2100): continue
        n += 1
        cands = [f] + ([f / 100] if pct else [])
        if not any(round(c, dec + (2 if (pct and c == f / 100) else 0)) in vals for c in cands): bad.append((line_no, tok, line.strip()[:120]))
out = os.path.join(R, "logs", f"audit_{os.path.basename(man)}.txt"); os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, "w") as fh:
    fh.write(f"checked {n} numbers, unmatched {len(bad)}\n")
    for b in bad: fh.write(f"line {b[0]}: {b[1]} | {b[2]}\n")
print(open(out).read()[:4000]); sys.exit(1 if bad else 0)
