#!/usr/bin/env python3
"""Topical PDFs of the hardest 9702 Paper 4 questions, one per A Level topic.

Every Paper 4 question paper from 2020 onwards is split into its questions,
each matched with its mark scheme rows and the examiner report's comments.
tools/physics_topical.json gives each question's topic and the 7 chosen
for each topic, with the evidence from the examiner reports.

    python3 tools/physics_topical.py split   # split papers, write the cache
    python3 tools/physics_topical.py dump T  # questions and report comments for topic T
    python3 tools/physics_topical.py build   # write physics-topical-papers/*.pdf
"""
import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'physics-9702-paper-4'
OUT = ROOT / 'physics-topical-papers'
DATA = ROOT / 'tools' / 'physics_topical.json'
CACHE = ROOT / 'tools' / '.physics_topical_cache.json'

SESSIONS = {'m': 'February/March', 's': 'May/June', 'w': 'October/November'}
SESSION_ORDER = {'m': 0, 's': 1, 'w': 2}
TOPICS = {
    12: 'Motion in a circle',
    13: 'Gravitational fields',
    14: 'Temperature',
    15: 'Ideal gases',
    16: 'Thermodynamics',
    17: 'Oscillations',
    18: 'Electric fields',
    19: 'Capacitance',
    20: 'Magnetic fields',
    21: 'Alternating currents',
    22: 'Quantum physics',
    23: 'Nuclear physics',
    24: 'Medical physics',
    25: 'Astronomy and cosmology',
}

# question paper geometry (A4 portrait): content sits between the barcode
# strip and the footer, and inside the grey "do not write" margin strips
QP_TOP, QP_X0, QP_X1 = 58.5, 22.0, 573.0
END_MARKERS = ('Permission to reproduce items', 'To avoid the issue of disclosure',
               'Cambridge Assessment International Education is part',
               'Cambridge University Press & Assessment is part')


def stem(path):
    return Path(path).stem


def parse_name(name):
    """'9702_w23_qp_41' -> ('w', 23, '41')."""
    m = re.match(r'9702_([msw])(\d\d)_(?:qp|ms)_(\d\d)$', name)
    return m.group(1), int(m.group(2)), m.group(3)


def paper_label(name):
    s, yy, v = parse_name(name)
    return f'9702/{v} {SESSIONS[s]} 20{yy}'


def short_label(name):
    s, yy, v = parse_name(name)
    return f'9702/{v}/{ {"m": "F/M", "s": "M/J", "w": "O/N"}[s] }/{yy}'


# ------------------------------------------------------------------ question papers

def lines(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']).strip()
            if t:
                out.append((l['bbox'], t, l['spans'][0]))
    return out


def page_bottom(page):
    """y just above the footer (© line) or the copyright notice on the last page."""
    bottom = page.rect.height - 50
    for (x0, y0, x1, y1), t, span in lines(page):
        if y0 > page.rect.height - 70 and ('UCLES' in t or 'Turn over' in t or re.match(r'9702/\d\d/', t)):
            bottom = min(bottom, y0 - 4)
        if any(t.startswith(m) for m in END_MARKERS):
            bottom = min(bottom, y0 - 14)
    return bottom


def is_blank(page):
    body = [t for (x0, y0, x1, y1), t, s in lines(page)
            if QP_TOP < y0 < page_bottom(page) and QP_X0 < x0 < QP_X1 and s['size'] > 6]
    joined = ' '.join(body)
    return (not body or joined.startswith('BLANK PAGE')
            or 'Additional page' in joined or 'additional page' in joined.lower()[:200])


def split_qp(path):
    doc = pymupdf.open(path)
    starts, expect = [], 1
    for pn in range(2, doc.page_count):
        for (x0, y0, x1, y1), t, span in sorted(lines(doc[pn]), key=lambda l: l[0][1]):
            m = re.match(r'^(\d{1,2})\b', t)
            if m and 44 < x0 < 60 and QP_TOP < y0 < 780 and int(m.group(1)) == expect:
                starts.append((expect, pn, y0 - 3))
                expect += 1
    questions = []
    for k, (q, pn, y) in enumerate(starts):
        end_pn, end_y = (starts[k + 1][1], starts[k + 1][2]) if k + 1 < len(starts) else (doc.page_count, None)
        segs = []
        for p in range(pn, end_pn + 1):
            if p >= doc.page_count:
                break
            page = doc[p]
            if p != pn and is_blank(page):
                continue
            top = y if p == pn else QP_TOP
            bottom = page_bottom(page)
            if p == end_pn:
                if end_y is None:
                    break
                bottom = min(bottom, end_y - 2)
            if bottom - top > 12:
                segs.append((p, round(top, 1), round(bottom, 1)))
        text = ' '.join(t for p, a, b in segs for (x0, y0, x1, y1), t, s in lines(doc[p])
                        if a <= y0 < b and QP_X0 < x0 < QP_X1 and s['size'] > 6)
        m = re.search(r'\[Total:\s*(\d+)\]', text)
        questions.append({'q': q, 'segs': segs, 'text': text, 'marks': int(m.group(1)) if m else None})
    return questions


# ------------------------------------------------------------------ mark schemes

LABEL_RE = re.compile(r'^(\d{1,2})(\([a-z]+\))*(\([ivx]+\))*$')


def display_lines(page):
    """Text lines with bounding boxes in display (rotated) coordinates."""
    mat = page.rotation_matrix
    out = []
    for bbox, t, span in lines(page):
        out.append((pymupdf.Rect(bbox) * mat, t, span))
    return out


def split_ms(path):
    """Question number -> list of (page, top, bottom, header top, header bottom),
    in display coordinates. Newer mark schemes start a fresh table (with its own
    header row) for each question, so a page can hold several header rows."""
    doc = pymupdf.open(path)
    rows = []          # (page, y, question)
    tables = {}        # page -> ([(header top, header bottom)], content bottom)
    for pn in range(doc.page_count):
        page = doc[pn]
        dl = display_lines(page)
        heads = sorted({round(r.y0) for r, t, s in dl if t.startswith('Question') and r.x0 < 140})
        if not heads:
            continue
        hrows = [(y - 6, max(r.y1 for r, t, s in dl if t.startswith('Question') and abs(r.y0 - y) < 2) + 5)
                 for y in heads]
        foot = min([r.y0 for r, t, s in dl if r.y0 > page.rect.height - 60] + [page.rect.height - 40])
        tables[pn] = (hrows, foot - 6)
        for r, t, s in dl:
            m = LABEL_RE.match(t)
            if m and r.x0 < 122 and r.y0 > hrows[0][1] - 2:   # the Answer column starts at 125
                rows.append((pn, r.y0, int(m.group(1))))
    rows.sort()
    out = {}
    for k, (pn, y, q) in enumerate(rows):
        if k and rows[k - 1][2] == q:
            continue
        nxt = next(((p2, y2) for p2, y2, q2 in rows[k:] if q2 != q), None)
        segs = []
        for p in sorted(tables):
            if p < pn or (nxt and p > nxt[0]):
                continue
            hrows, bottom = tables[p]
            a = y - 5 if p == pn else hrows[0][1]
            b = (nxt[1] - 5) if (nxt and p == nxt[0]) else bottom
            # a new table header below the start belongs to the next question
            b = min([b] + [h0 - 2 for h0, h1 in hrows if a + 2 < h0 < b])
            head = max([h for h in hrows if h[1] <= a + 6], default=hrows[0])
            if b - a > 8:
                segs.append((p, round(a, 1), round(b, 1), round(head[0], 1), round(head[1], 1)))
        out.setdefault(q, segs)
    return out


# ------------------------------------------------------------------ examiner reports

def split_er(path):
    """Variant ('41') -> question number -> report text."""
    doc = pymupdf.open(path)
    text = '\n'.join(p.get_text() for p in doc)
    text = re.sub(r'\n\s*©[^\n]*\n', '\n', text)
    heads = [(m.start(), m.group(1)) for m in re.finditer(r'Paper 9702/(\d\d)\s*\n', text)]
    out = {}
    for k, (i, v) in enumerate(heads):
        j = heads[k + 1][0] if k + 1 < len(heads) else len(text)
        sec = text[i:j]
        if not v.startswith('4'):
            continue
        qs = {}
        parts = re.split(r'\n\s*Question (\d{1,2})\s*\n', sec)
        for n in range(1, len(parts) - 1, 2):
            qs[int(parts[n])] = re.sub(r'\s+', ' ', parts[n + 1]).strip()
        general = re.sub(r'\s+', ' ', parts[0]).strip()
        out[v] = {'general': general, 'questions': qs}
    return out


# ------------------------------------------------------------------ split command

def norm(text):
    """Question text without answer dots and spacing, for spotting repeats."""
    return re.sub(r'[\s.…]+', ' ', text).strip()


def qp_paths():
    paths = sorted((SRC / 'question-papers').glob('9702_*_qp_4*.pdf'))
    return sorted(paths, key=lambda p: (parse_name(p.stem)[1], SESSION_ORDER[parse_name(p.stem)[0]], parse_name(p.stem)[2]))


def cmd_split():
    cache = {}
    for qp in qp_paths():
        name = qp.stem
        s, yy, v = parse_name(name)
        ms_path = SRC / 'mark-schemes' / f'9702_{s}{yy:02d}_ms_{v}.pdf'
        er_path = SRC / 'examiner-reports' / f'9702_{s}{yy:02d}_er.pdf'
        qs = split_qp(qp)
        ms = split_ms(ms_path)
        er = split_er(er_path).get(v, {}) if er_path.exists() else {}
        for q in qs:
            q['ms'] = ms.get(q['q'], [])
            q['er'] = er.get('questions', {}).get(q['q'], '')
        cache[name] = qs
        missing_ms = [q['q'] for q in qs if not q['ms']]
        print(f'{name}: {len(qs)} questions, marks {[q["marks"] for q in qs]}'
              + (f', no mark scheme rows for {missing_ms}' if missing_ms else '')
              + ('' if er else ', no examiner report'))
    # variants 41 and 43 are the same paper; some reports cover only one of
    # them ("too few candidates"), so share the comments between identical questions
    by_text = {}
    for name, qs in cache.items():
        for q in qs:
            by_text.setdefault((name[5:8], norm(q['text'])), []).append(q)
    for group in by_text.values():
        er = next((q['er'] for q in group if q['er']), '')
        for q in group:
            q['er'] = q['er'] or er
    CACHE.write_text(json.dumps(cache, indent=1))


# ------------------------------------------------------------------ dump command

def qid_parts(qid):
    """'w21_42_Q1' -> ('9702_w21_qp_42', 1)."""
    m = re.match(r'([msw]\d\d)_(\d\d)_Q(\d+)$', qid)
    return f'9702_{m.group(1)}_qp_{m.group(2)}', int(m.group(3))


def qid_label(qid):
    name, q = qid_parts(qid)
    return f'{paper_label(name)}, Question {q}'


def cmd_dump(topic):
    cache = json.loads(CACHE.read_text())
    data = json.loads(DATA.read_text())
    for qid, ts in data['topics'].items():
        if isinstance(ts, list) and topic in ts:
            name, q = qid_parts(qid)
            question = cache[name][q - 1]
            print(f'{qid} ({question["marks"]} marks): {norm(question["text"])[:160]}')
            print(f'    report: {question["er"][:400] or "(no examiner report)"}\n')


# ------------------------------------------------------------------ build command

sys.path.insert(0, str(ROOT / 'tools' / 'physics_papers'))


def cover_pdf(topic, entries, pages):
    """Contents page for one topic, made with the practice-paper fonts."""
    import io
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from richtext import draw_line, draw_rich, wrap
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4
    x, right = 56.7, 538.6
    y = H - 80
    draw_rich(c, x, y, f'Physics 9702 Paper 4 · Topic {topic}', size=18, bold=True)
    y -= 24
    draw_rich(c, x, y, TOPICS[topic], size=15)
    y -= 22
    for words, last in wrap('The seven hardest A Level Structured Questions on this topic from the 2020 to 2026 '
                            'papers, hardest first, followed by their mark schemes.', right - x, size=10.5):
        draw_line(c, x, y, words, right - x, 'left', True, size=10.5)
        y -= 13
    c.setLineWidth(0.5)
    y -= 6
    c.line(x, y, right, y)
    y -= 22
    for k, (e, page) in enumerate(zip(entries, pages), 1):
        name, q = qid_parts(e['q'])
        draw_rich(c, x, y, f'{k}', size=11, bold=True)
        draw_rich(c, x + 18, y, f'<b>{paper_label(name)}, Question {q}</b> ({e["marks"]} marks)', size=11)
        draw_rich(c, right, y, f'page {page}', size=10, anchor='r')
        y -= 14
        why = e['why'] or 'No examiner report: chosen on judgement.'
        for words, last in wrap(f'<i>Examiner report:</i> {why}', right - x - 18, size=9):
            draw_line(c, x + 18, y, words, right - x - 18, 'left', True, size=9)
            y -= 11
        y -= 10
    y = 70
    c.line(x, y + 14, right, y + 14)
    for words, last in wrap('Questions were chosen using the Cambridge examiner reports (Principal Examiner Report for '
                            'Teachers): parts the reports describe as challenging, poorly answered, or answered fully only by '
                            'the strongest candidates. May/June 2020 and May/June 2026 have no report, so questions from those '
                            'series were judged directly. Variant 43 repeats variant 41 in every series, so only 41 is cited.',
                            right - x, size=8.5):
        draw_line(c, x, y, words, right - x, 'left', True, size=8.5)
        y -= 10.5
    c.showPage()
    c.save()
    return pymupdf.open('pdf', buf.getvalue())


def stamp(page, text, y, size=8.5):
    page.insert_text((QP_X0 + 34, y), text, fontsize=size, fontname='helv', color=(0.35, 0.35, 0.35))


def build_topic(topic, chosen, cache):
    out = pymupdf.open()
    entries = []
    for e in chosen:
        name, q = qid_parts(e['q'])
        entries.append(dict(e, marks=cache[name][q - 1]['marks'], name=name, n=q))
    # question pages
    starts, qpages = [], []
    for k, e in enumerate(entries, 1):
        src = pymupdf.open(SRC / 'question-papers' / f'{e["name"]}.pdf')
        segs = cache[e['name']][e['n'] - 1]['segs']
        starts.append(len(qpages) + 2)
        for j, (p, a, b) in enumerate(segs):
            page = out.new_page(width=595.28, height=841.89)
            top = QP_TOP
            page.show_pdf_page(pymupdf.Rect(QP_X0, top, QP_X1, top + (b - a)), src, p,
                               clip=pymupdf.Rect(QP_X0, a, QP_X1, b))
            stamp(page, f'Topic {topic} · {k} of 7 · {short_label(e["name"])} Question {e["n"]}'
                        + (' (continued)' if j else ''), 34)
            qpages.append(page)
    # mark scheme pages (landscape), each question starting a new page
    for k, e in enumerate(entries, 1):
        s, yy, v = parse_name(e['name'])
        src = pymupdf.open(SRC / 'mark-schemes' / f'9702_{s}{yy:02d}_ms_{v}.pdf')
        for pg in src:
            if pg.rotation:
                pg.remove_rotation()
        page, y = None, 0
        for j, (p, a, b, h0, h1) in enumerate(cache[e['name']][e['n'] - 1]['ms']):
            need = (h1 - h0) + (b - a)
            if page is None or y + need > 560:
                page = out.new_page(width=841.89, height=595.28)
                stamp(page, f'Mark scheme · Topic {topic} · {k} of 7 · {short_label(e["name"])} Question {e["n"]}'
                            + (' (continued)' if j else ''), 32)
                y = 44
            W = page.rect.width
            page.show_pdf_page(pymupdf.Rect(0, y, W, y + h1 - h0), src, p, clip=pymupdf.Rect(0, h0, W, h1))
            y += h1 - h0
            page.show_pdf_page(pymupdf.Rect(0, y, W, y + b - a), src, p, clip=pymupdf.Rect(0, a, W, b))
            y += b - a + 14
    cover = cover_pdf(topic, entries, starts)
    out.insert_pdf(cover, start_at=0)
    for i, page in enumerate(out, 1):
        page.insert_text((page.rect.width / 2 - 8, page.rect.height - 22), str(i), fontsize=9, fontname='helv')
    OUT.mkdir(exist_ok=True)
    path = OUT / f'Topic {topic} - {TOPICS[topic]}.pdf'
    out.set_metadata({'title': f'Physics 9702 Paper 4 topical questions: {topic} {TOPICS[topic]}'})
    out.save(path, garbage=4, deflate=True)
    return path, out.page_count


def cmd_build():
    cache = json.loads(CACHE.read_text())
    data = json.loads(DATA.read_text())
    for t in sorted(TOPICS):
        chosen = data['chosen'][str(t)]
        path, n = build_topic(t, chosen, cache)
        print(f'{path.name}: {n} pages')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'split':
        cmd_split()
    elif cmd == 'dump':
        cmd_dump(int(sys.argv[2]))
    elif cmd == 'build':
        if not CACHE.exists():
            cmd_split()
        cmd_build()
    else:
        print(__doc__)
