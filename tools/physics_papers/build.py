#!/usr/bin/env python3
"""Build the 9702 Paper 4 practice papers and their mark schemes.

    python3 tools/physics_papers/build.py            # all papers
    python3 tools/physics_papers/build.py 2          # one paper
    python3 tools/physics_papers/build.py 2 --png    # also render page previews

PDFs go to physics-practice-papers/. Each build checks that every part's
marks in the question paper match the mark scheme and that the paper is out
of 100.
"""
import importlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parent.parent
OUT = ROOT / 'physics-practice-papers'

from engine import MSDoc, QPDoc, ms_marks  # noqa: E402


def build(n, png_dir=None):
    mod = importlib.import_module(f'paper{n}')
    paper = mod.PAPER
    OUT.mkdir(exist_ok=True)
    qp = OUT / f'9702 Practice Paper {n}.pdf'
    ms = OUT / f'9702 Practice Paper {n} - mark scheme.pdf'
    rep = QPDoc(paper).build(str(qp))
    msrep = MSDoc(paper).build(str(ms))
    problems = []
    total = sum(rep['totals'])
    if total != 100:
        problems.append(f'paper total is {total}, not 100')
    msm = ms_marks(paper)
    for label in sorted(set(rep['parts']) | set(msm)):
        a, b = rep['parts'].get(label, 0), msm.get(label, 0)
        if a != b:
            problems.append(f'{label}: question paper {a} marks, mark scheme {b}')
    print(f'Paper {n}: {rep["pages"]} pages, question totals {rep["totals"]} = {total}, '
          f'pages per question {rep["q_pages"]}; mark scheme {msrep["pages"]} pages')
    for p in problems:
        print('  PROBLEM:', p)
    if png_dir:
        import pymupdf
        d = Path(png_dir)
        d.mkdir(parents=True, exist_ok=True)
        for old in d.glob(f'p{n}_*.png'):
            old.unlink()
        for f, tag in ((qp, 'qp'), (ms, 'ms')):
            doc = pymupdf.open(f)
            for i, page in enumerate(doc):
                page.get_pixmap(dpi=80).save(d / f'p{n}_{tag}_{i + 1:02d}.png')
    return not problems


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    png = '--png' in sys.argv
    nums = [int(a) for a in args] or [1, 2, 3]
    scratch = '/tmp/claude-0/-home-user-On-IT/df9ae915-b3dd-5c06-b77b-3161193db54d/scratchpad/preview'
    ok = all([build(n, scratch if png else None) for n in nums])
    sys.exit(0 if ok else 1)
