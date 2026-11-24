#!/usr/bin/env python3
"""Minimal Markdown -> .docx for the manuscript (headings, paragraphs, bullets, numbered lists, pipe tables, *italic*,
**bold**), embedding figures after the legends. usage: md_to_docx.py IN.md OUT.docx FIGDIR"""
import sys, re, os
from docx import Document
from docx.shared import Pt, Inches
src, out, figdir = sys.argv[1:4]
doc = Document(); st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(11)
def runs(p, text):
    for part in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if part.startswith("**") and part.endswith("**"): p.add_run(part[2:-2]).bold = True
        elif part.startswith("*") and part.endswith("*") and len(part) > 2: p.add_run(part[1:-1]).italic = True
        elif part: p.add_run(part)
blocks, buf = [], []
for line in open(src).read().splitlines():
    if not line.strip():
        if buf: blocks.append(buf); buf = []
        continue
    if line.startswith(("#", "|", "- ", "---")) or re.match(r"^\d+\. ", line) or (line.startswith("  ") and buf and buf[-1].lstrip().startswith(("- ",))):
        if line.startswith("  ") and buf: buf[-1] += " " + line.strip(); continue
        if buf and not (line.startswith("|") and buf[-1].startswith("|")): blocks.append(buf); buf = []
        buf.append(line); continue
    if buf and (buf[-1].startswith(("- ",)) or re.match(r"^\d+\. ", buf[-1])) and line.startswith("  "): buf[-1] += " " + line.strip(); continue
    if buf and (buf[-1].startswith(("#", "|", "- ")) or re.match(r"^\d+\. ", buf[-1])): blocks.append(buf); buf = []
    buf.append(line)
if buf: blocks.append(buf)
FIGS = {"Figure 1.": "Figure1_atlas_lasso_strict.png", "Figure 2.": "Figure2_mechanism.png", "Figure 3.": "Figure3_fixes_stress.png"}
for b in blocks:
    first = b[0]
    if first.startswith("#"):
        lvl = len(first) - len(first.lstrip("#")); doc.add_heading(first.lstrip("#").strip(), level=min(lvl, 3)); continue
    if first.startswith("---"): continue
    if first.startswith("|"):
        rows = [[c.strip() for c in r.strip("|").split("|")] for r in b if not re.match(r"^\|[\s\-|]+\|$", r)]
        t = doc.add_table(rows=len(rows), cols=len(rows[0])); t.style = "Table Grid"
        for i, r in enumerate(rows):
            for j, c in enumerate(r): t.cell(i, j).text = c
        continue
    if all(l.startswith("- ") for l in b):
        for l in b: runs(doc.add_paragraph(style="List Bullet"), l[2:])
        continue
    if all(re.match(r"^\d+\. ", l) for l in b):
        for l in b: runs(doc.add_paragraph(), l)
        continue
    text = " ".join(l.strip() for l in b); p = doc.add_paragraph(); runs(p, text)
    for k, f in FIGS.items():
        if text.startswith(f"**{k}") and os.path.exists(os.path.join(figdir, f)): doc.add_picture(os.path.join(figdir, f), width=Inches(6.5))
doc.save(out); print("wrote", out)
