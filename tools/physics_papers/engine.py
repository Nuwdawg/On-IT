"""Layout engine for the 9702 Paper 4 practice papers.

A paper module declares content with the classes below (see SPEC.md);
build.py turns it into a question paper and a mark scheme laid out like the
2025 Cambridge papers. All measurements were taken from 9702_s25_qp_42 and
9702_s25_ms_42: page furniture, the 13 pt line grid, label and text indents,
answer lines and mark brackets sit where they do in those papers.
"""
import math
import re

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas as rl_canvas

import codes
from richtext import (EQ_SPACE, Box, Frac, Low, Sqrt, Sup, draw_line, draw_rich, draw_runs,
                      line_width, math_box, runs, runs_width, width, wrap)

__all__ = ['Paper', 'Question', 'Part', 'Sub', 'Text', 'Lines', 'Space',
           'Answer', 'Mark', 'Fig', 'FigRow', 'Table', 'Eq', 'Frac', 'Sqrt',
           'Sup', 'Low', 'PageBreak', 'MSRow']

# ------------------------------------------------------------------ content


class Paper:
    def __init__(self, number, questions, mark_scheme):
        self.number, self.questions, self.mark_scheme = number, questions, mark_scheme


class Question:
    def __init__(self, blocks):
        self.blocks = blocks


class Part:
    def __init__(self, label, blocks):
        self.label, self.blocks = label, blocks


class Sub:
    def __init__(self, label, blocks):
        self.label, self.blocks = label, blocks


class Text:
    def __init__(self, rich, align='justify'):
        self.rich, self.align = rich, align


class Lines:
    def __init__(self, n, marks):
        self.n, self.marks = n, marks


class Space:
    def __init__(self, n):
        self.n = n


class Answer:
    def __init__(self, label, unit='', marks=None):
        self.label, self.unit, self.marks = label, unit, marks


class Mark:
    def __init__(self, n):
        self.n = n


class Fig:
    def __init__(self, w, h, draw, caption, note=''):
        self.w, self.h, self.draw, self.caption, self.note = w, h, draw, caption, note


class FigRow:
    def __init__(self, figs, gap=40):
        self.figs, self.gap = figs, gap


class Table:
    def __init__(self, rows, col_widths, caption, row_heights=None):
        self.rows, self.col_widths, self.caption = rows, col_widths, caption
        self.row_heights = row_heights


class Eq:
    def __init__(self, *items, align='center'):
        self.items, self.align = items, align


class PageBreak:
    pass


class MSRow:
    def __init__(self, label, points, note=None):
        self.label, self.points, self.note = label, points, note

# ------------------------------------------------------------------ geometry

PW, PH = A4                      # 595.28 x 841.89
LEAD = 13.0
BASE = 8.8                       # baseline below the top of a 13 pt line slot
TOP = 63.8                       # first line slot on a page
BOTTOM = 776.0                   # lowest allowed slot bottom
CENTRE = 297.6
X_QNUM, X_PART, X_SUB_R = 49.6, 72.3, 106.4
X_TEXT = {0: 72.3, 1: 95.0, 2: 117.7}
RIGHT = 545.7                    # right edge of text and mark brackets
DOTS_END = 544.9
DOTS_START = 350.0               # where the dots of "x = ...... unit" begin
DOT_W = width('.', 'Arial', 11)
GREY = 0.93
SERIES = 'August/September 2026'     # a series Cambridge does not run
SERIES_CODE = 'A/S/26'
INK = (0.137, 0.122, 0.125)


def y_(top):
    """Top-down coordinate to reportlab y."""
    return PH - top


def text_at(c, x, top, s, size=11, anchor='l', bold=False, italic=False):
    """Draw rich text whose 13 pt slot starts at `top` (for 11 pt text)."""
    return draw_rich(c, x, y_(top + BASE * size / 11), s, size, anchor, bold, italic)


def dots(c, x0, x1, top):
    n = int((x1 - x0) / DOT_W)
    c.setFont('Arial', 11)
    c.drawString(x1 - n * DOT_W, y_(top + BASE), '.' * n)


def mark_str(n):
    return f'[{n}]'


def marks_of(code):
    m = re.match(r'[A-Z]+(\d+)', code.strip())
    return int(m.group(1)) if m else 0

# ------------------------------------------------------------------ layout items


class Item:
    def __init__(self, kind, h, draw, gap=LEAD, label=None, marks=0):
        self.kind, self.h, self._draw, self.gap = kind, h, draw, gap
        self.label, self.marks = label, marks
        self.labels = []
        self.keep_next = False
        self.extra = []          # extra draw callbacks (e.g. an inline mark)

    def draw(self, c, top):
        self._draw(c, top)
        for f in self.extra:
            f(c, top)


_PART_REF = re.compile(r'(?<![>\w(])(\d{0,2}\([a-h]\)(?:\((?:i|ii|iii|iv|v|vi)\))?)(?![\w<])')


def bold_refs(rich):
    """Cambridge prints references to other parts, e.g. (b)(ii) or 6(a), in bold."""
    return _PART_REF.sub(r'<b>\1</b>', rich)


def _text_item(b, x, label):
    maxw = RIGHT - x
    lines = wrap(bold_refs(b.rich), maxw)

    def draw(c, top):
        for k, (words, last) in enumerate(lines):
            draw_line(c, x, y_(top + BASE + LEAD * k), words, maxw, b.align, last)
    it = Item('text', LEAD * len(lines), draw, label=label)
    it.last_w = line_width(lines[-1][0]) if lines[-1][0] else 0
    it.nlines = len(lines)
    it.x = x
    return it


def _lines_item(b, x, label):
    def draw(c, top):
        for k in range(b.n):
            t = top + 2 * LEAD * k
            if k == b.n - 1 and b.marks is not None:
                m = ' ' + mark_str(b.marks)
                c.setFont('Arial', 11)
                c.drawRightString(RIGHT, y_(t + BASE), m)
                dots(c, x, RIGHT - width(m, 'Arial', 11), t)
            else:
                dots(c, x, DOTS_END, t)
    return Item('lines', LEAD + 2 * LEAD * (b.n - 1), draw, label=label, marks=b.marks or 0)


def _answer_item(b, x, label):
    lab = b.label if '=' in b.label else b.label + ' ='
    tail = (' ' + b.unit if b.unit else '') + (f' {mark_str(b.marks)}' if b.marks is not None else '')
    tail_rs = runs(tail)
    tail_w = runs_width(tail_rs)
    lab_rs = runs(lab)
    lab_w = runs_width(lab_rs)

    def draw(c, top):
        base = y_(top + BASE)
        start = max(DOTS_START, x + lab_w + 6)
        draw_runs(c, start - 5 - lab_w, base, lab_rs)
        dots(c, start, RIGHT - tail_w - 1.5, top)
        draw_runs(c, RIGHT - tail_w, base, tail_rs)
    return Item('answer', LEAD, draw, label=label, marks=b.marks or 0)


def _mark_item(b, label):
    def draw(c, top):
        c.setFont('Arial', 11)
        c.drawRightString(RIGHT, y_(top + BASE), mark_str(b.n))
    return Item('mark', LEAD, draw, label=label, marks=b.n)


def _caption(c, cx, top, caption, note):
    rs = runs(caption, bold=True) + (runs(' ' + note) if note else [])
    w = runs_width(rs)
    draw_runs(c, cx - w / 2, y_(top + BASE), rs)


def _call_fig(c, f, x, top):
    c.saveState()
    c.translate(x, y_(top + f.h))
    c.setLineWidth(0.75)
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)
    c.setFont('Arial', 11)
    f.draw(c)
    c.restoreState()


CAP_GAP = 15.0


def _fig_item(b, label):
    if b.w > 496:
        print(f'  WARNING: {b.caption} is {b.w:.0f} pt wide; the page allows 496')
    def draw(c, top):
        _call_fig(c, b, CENTRE - b.w / 2, top)
        _caption(c, CENTRE, top + b.h + CAP_GAP, b.caption, b.note)
    return Item('fig', b.h + CAP_GAP + LEAD, draw, label=label)


def _figrow_item(b, label):
    tw = sum(f.w for f in b.figs) + b.gap * (len(b.figs) - 1)
    h = max(f.h for f in b.figs)
    if tw > 496:
        print(f'  WARNING: figure row {", ".join(f.caption for f in b.figs)} is {tw:.0f} pt wide; the page allows 496')

    def draw(c, top):
        x = CENTRE - tw / 2
        for f in b.figs:
            _call_fig(c, f, x, top + h - f.h)
            _caption(c, x + f.w / 2, top + h + CAP_GAP, f.caption, f.note)
            x += f.w + b.gap
    return Item('fig', h + CAP_GAP + LEAD, draw, label=label)


def _table_item(b, x, label):
    tw = sum(b.col_widths)
    cx = (x + RIGHT) / 2
    left = max(X_QNUM, min(cx - tw / 2, RIGHT - tw))
    heights = b.row_heights or [26.0] * len(b.rows)
    if len(heights) < len(b.rows):
        heights = list(heights) + [26.0] * (len(b.rows) - len(heights))
    th = sum(heights)

    def draw(c, top):
        _caption(c, left + tw / 2, top, b.caption, '')
        t0 = top + 2 * LEAD
        c.setLineWidth(0.5)
        c.setStrokeColorRGB(*INK)
        c.rect(left, y_(t0 + th), tw, th)
        t = t0
        for r, row in enumerate(b.rows):
            if r:
                c.line(left, y_(t), left + tw, y_(t))
            xx = left
            for k, cell in enumerate(row):
                if k:
                    c.line(xx, y_(t), xx, y_(t + heights[r]))
                cw = b.col_widths[k]
                if cell:
                    ls = wrap(cell, cw - 8)
                    th_txt = LEAD * len(ls)
                    t_txt = t + (heights[r] - th_txt) / 2 - 1.0
                    for j, (words, last) in enumerate(ls):
                        draw_line(c, xx + 4, y_(t_txt + BASE + LEAD * j), words, cw - 8, 'center', True)
                xx += cw
            t += heights[r]
        c.setStrokeColorRGB(0, 0, 0)
    return Item('table', 2 * LEAD + th, draw, label=label)


def _eq_item(b, x, label):
    box = math_box(list(b.items))
    h = max(LEAD, math.ceil((box.asc + box.desc + 2) / LEAD) * LEAD)

    def draw(c, top):
        base = top + (h - box.asc - box.desc) / 2 + box.asc
        if b.align == 'center':
            bx = (x + RIGHT) / 2 - box.w / 2
        else:
            bx = x
        box.draw(c, bx, y_(base))
    return Item('eq', h, draw, label=label)


def _total_item(n):
    def draw(c, top):
        c.setFont('Arial', 11)
        c.drawRightString(RIGHT, y_(top + BASE), f'[Total: {n}]')
    return Item('total', LEAD, draw)


def flatten(qnum, q):
    """Turn a Question into layout items plus the marks per part label."""
    items, pending, part_marks = [], [('q', str(qnum))], {}
    prev_block = [None]

    def add(item, block):
        item.labels, pending[:] = pending[:], []
        items.append(item)
        prev_block[0] = block

    def walk(blocks, level, path):
        for i, b in enumerate(blocks):
            if isinstance(b, Part):
                pending.append(('part', f'({b.label})'))
                walk(b.blocks, 1, f'{qnum}({b.label})')
                continue
            if isinstance(b, Sub):
                pending.append(('sub', f'({b.label})'))
                base = path if level >= 1 else str(qnum)
                walk(b.blocks, 2, re.sub(r'(\([ivx]+\))$', '', base) + f'({b.label})')
                continue
            x = X_TEXT[level]
            if isinstance(b, Text):
                it = _text_item(b, x, path)
                nxt = blocks[i + 1] if i + 1 < len(blocks) else None
                if isinstance(nxt, (Fig, FigRow, Table, Eq, Text)):
                    it.keep_next = True      # a stem stays with what it introduces
                add(it, b)
            elif isinstance(b, Lines):
                add(_lines_item(b, x, path), b)
            elif isinstance(b, Space):
                add(Item('space', LEAD * b.n, lambda c, t: None, label=path), b)
            elif isinstance(b, Answer):
                it = _answer_item(b, x, path)
                if isinstance(prev_block[0], Space):
                    it.gap = 0
                add(it, b)
            elif isinstance(b, Mark):
                prev = items[-1] if items else None
                pb = prev_block[0]
                if (isinstance(pb, Text) and prev is not None and prev.kind == 'text'
                        and prev.x + prev.last_w + 12 + width(mark_str(b.n), 'Arial', 11) <= RIGHT
                        and not pending):
                    t_off = LEAD * (prev.nlines - 1)
                    prev.extra.append(lambda c, top, n=b.n, o=t_off: (
                        c.setFont('Arial', 11), c.drawRightString(RIGHT, y_(top + o + BASE), mark_str(n))))
                    prev.marks += b.n
                    prev_block[0] = b
                    continue
                it = _mark_item(b, path)
                if isinstance(pb, (Text, Space)):
                    it.gap = 0
                elif isinstance(pb, Table):
                    it.gap = 2
                add(it, b)
            elif isinstance(b, (Fig, FigRow)):
                it = _fig_item(b, path) if isinstance(b, Fig) else _figrow_item(b, path)
                caps = [b.caption] if isinstance(b, Fig) else [f.caption for f in b.figs]
                nxt = blocks[i + 1] if i + 1 < len(blocks) else None
                if isinstance(nxt, Text) and any(cap and nxt.rich.lstrip().startswith('On ' + cap) for cap in caps):
                    it.keep_next = True      # "On Fig. 5.2, sketch ..." stays with Fig. 5.2
                add(it, b)
            elif isinstance(b, Table):
                add(_table_item(b, x, path), b)
            elif isinstance(b, Eq):
                add(_eq_item(b, x, path), b)
            elif isinstance(b, PageBreak):
                add(Item('break', 0, lambda c, t: None), b)
            else:
                raise TypeError(f'Q{qnum}: unknown block {b!r}')

    walk(q.blocks, 0, str(qnum))
    for it in items:
        if it.marks:
            part_marks[it.label] = part_marks.get(it.label, 0) + it.marks
    total = sum(part_marks.values())
    items.append(_total_item(total))
    # the gap after a Space is absorbed by the space
    for a, b in zip(items, items[1:]):
        if a.kind == 'space':
            b.gap = 0
        if b.kind == 'space':
            b.gap = 0
    return items, part_marks, total


def _draw_labels(c, item, top):
    for kind, lab in item.labels:
        if kind == 'q':
            text_at(c, X_QNUM, top, lab, bold=True)
        elif kind == 'part':
            text_at(c, X_PART, top, lab, bold=True)
        else:
            text_at(c, X_SUB_R, top, lab, anchor='r', bold=True)


def paginate(items):
    """Group items that must stay together and place groups on pages."""
    groups = []
    for it in items:
        joins = groups and (groups[-1][-1].keep_next or it.kind in ('space', 'answer', 'lines', 'mark', 'total'))
        if joins:
            groups[-1].append(it)
        else:
            groups.append([it])
    pages, page, top = [], [], TOP
    for g in groups:
        if g[0].kind == 'break':
            pages.append(page)
            page, top = [], TOP
            continue
        h = sum(it.h for it in g) + sum(it.gap for it in g[1:])
        if h > BOTTOM - TOP and len(g) > 1:
            # too tall to keep together: let it break between its items
            for k, it in enumerate(g):
                gap = it.gap if page else 0
                if page and top + gap + it.h > BOTTOM:
                    pages.append(page)
                    page, top, gap = [], TOP, 0
                page.append((it, top + gap))
                top += gap + it.h
            continue
        gap = g[0].gap if page else 0
        if page and top + gap + h > BOTTOM:
            pages.append(page)
            page, top, gap = [], TOP, 0
        t = top + gap
        for k, it in enumerate(g):
            if k:
                t += it.gap
            page.append((it, t))
            t += it.h
        top = t
    if page:
        pages.append(page)
    return pages

# ------------------------------------------------------------------ page furniture


def corner_marks(c, w=PW, h=PH, top=31.2, bottom=810.7, left=36.9, right=558.4):
    c.saveState()
    c.setLineWidth(2.8346)
    c.setLineJoin(0)
    c.setLineCap(0)
    for x, t, dx, dy in ((left, top, 1, 1), (right, top, -1, 1), (left, bottom, 1, -1), (right, bottom, -1, -1)):
        p = c.beginPath()
        p.moveTo(x, y_(t + dy * 19.8))
        p.lineTo(x, y_(t))
        p.lineTo(x + dx * 21.2, y_(t))
        c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def margin_bar(c, side):
    c.saveState()
    c.setFillGray(GREY)
    x0 = 574.5 if side == 'right' else 0.0
    c.rect(x0, -10, 21.0, PH + 20, stroke=0, fill=1)
    c.setFillGray(0)
    c.setFont('Arial', 8)
    bx = 587.8 if side == 'right' else 13.3
    for k in range(5):
        c.saveState()
        c.translate(bx, y_(812.6 - 164.0 * k))
        c.rotate(90)
        c.drawString(0, 0, 'DO NOT WRITE IN THIS MARGIN')
        c.restoreState()
    c.restoreState()


class QPDoc:
    def __init__(self, paper):
        self.paper = paper
        self.n = paper.number
        self.comp = f'9702/4{self.n}'
        self.series = SERIES
        self.foot_centre = f'9702/4{self.n}/{SERIES_CODE}'

    def page_marks(self, c, pageno, cover=False):
        """Barcode strip at the top of every page, QR code in the footer."""
        c.setFont('Arial', 8)
        c.drawString(82.2 if cover else 83.9, y_(19.3 + 6.4), f'* {codes.page_code(pageno)} *')
        c.drawString(226.7 if cover else 229.1, y_(19.1 + 6.4), 'NGG')
        codes.code39(c, 65.5, y_(57.8), 179.5, 28.0, codes.page_code(pageno))
        if not cover:
            codes.qr(c, 170.8, y_(812.0), 15.0)

    def furniture(self, c, pageno, total, blank=False, turn_over=True):
        corner_marks(c)
        self.page_marks(c, pageno)
        margin_bar(c, 'right' if pageno % 2 == 0 else 'left')
        text_at(c, CENTRE, 38.5, str(pageno), anchor='c', bold=True)
        c.setFont('Arial', 8)
        c.drawCentredString(CENTRE, y_(798.6 + 6.4), self.foot_centre)
        if pageno % 2 == 1 and turn_over:
            text_at(c, RIGHT, 796.2, '[Turn over', anchor='r', bold=True)
        if blank:
            text_at(c, CENTRE, 63.8, 'BLANK PAGE', anchor='c', bold=True)

    # ---------------------------------------------------------- cover
    def cover(self, c, total):
        corner_marks(c)
        self.page_marks(c, 1, cover=True)
        codes.logo(c, 262.2, y_(56.2), 538.6 - 262.2, 29.0)
        codes.qr(c, 27.0, y_(192.8), 20.0)
        codes.code39(c, 26.8, y_(337.0), 21.2, 113.0, codes.SPEED_OF_LIGHT, vertical=True)
        sym = ['*'] + list(codes.SPEED_OF_LIGHT) + ['*']
        c.setFont('Arial', 8.4)
        for k, ch in enumerate(sym):
            c.drawCentredString(24.0, y_(224.0 + 6.3 + (337.0 - 224.0 - 6.3) * k / (len(sym) - 1)), ch)
        text_at(c, 56.7, 104.6, f'A Level Physics Practice Paper {self.n}', size=18, bold=True)
        c.setLineWidth(0.5)
        c.setStrokeColorRGB(*INK)
        for t1, t2 in ((140.3, 174.3),):
            c.rect(128.2, y_(t2), 538.1 - 128.2, t2 - t1)
        c.rect(128.2, y_(216.8), 251.5 - 128.2, 216.8 - 182.7)
        for xx in (152.8, 177.4, 202.1, 226.7):
            c.line(xx, y_(182.7), xx, y_(216.8))
        c.rect(439.6, y_(216.8), 538.1 - 439.6, 216.8 - 182.7)
        for xx in (464.2, 488.9, 513.5):
            c.line(xx, y_(182.7), xx, y_(216.8))
        for t in (228.4, 347.4, 728.5):
            c.line(56.7, y_(t), 538.6, y_(t))
        c.setStrokeColorRGB(0, 0, 0)
        c.setFont('Arial', 10)
        for (x, t, s) in ((56.7, 147.4, 'CANDIDATE'), (56.7, 159.7, 'NAME'),
                          (56.7, 189.8, 'CENTRE'), (56.7, 202.1, 'NUMBER'),
                          (371.4, 189.8, 'CANDIDATE'), (371.4, 202.1, 'NUMBER')):
            c.drawString(x, y_(t + 7.4), s)
        text_at(c, 56.7, 235.9, 'PHYSICS', bold=True)
        text_at(c, 538.6, 235.9, self.comp, anchor='r', bold=True)
        s10 = 10
        tx = lambda x, t, s, **k: text_at(c, x, t, s, size=s10, **k)
        tx(56.7, 256.7, 'Paper 4 A Level Structured Questions')
        tx(538.6, 256.7, self.series, anchor='r', bold=True)
        tx(538.6, 276.7, '2 hours', anchor='r', bold=True)
        tx(56.7, 301.7, 'You must answer on the question paper.')
        tx(56.7, 326.7, 'No additional materials are needed.')
        tx(56.7, 355.3, 'INSTRUCTIONS', bold=True)
        inst = ['Answer <b>all</b> questions.',
                'Use a black or dark blue pen. You may use an HB pencil for any diagrams or graphs.',
                'Write your name, centre number and candidate number in the boxes at the top of the page.',
                'Write your answer to each question in the space provided.',
                'Do <b>not</b> use an erasable pen or correction fluid.',
                'You may use a calculator.',
                'You should show all your working and use appropriate units.']
        for k, s in enumerate(inst):
            tx(56.7, 368.3 + 13 * k, '●')
            tx(78.0, 368.3 + 13 * k, s)
        tx(56.7, 498.3 - 13, 'INFORMATION', bold=True)
        for k, s in enumerate(['The total mark for this paper is 100.',
                               'The number of marks for each question or part question is shown in brackets [ ].']):
            tx(56.7, 511.3 - 13 + 13 * k, '●')
            tx(78.0, 511.3 - 13 + 13 * k, s)
        msg = f'This document has <b>{total}</b> pages. Any blank pages are indicated.'
        text_at(c, CENTRE, 733.4, msg, size=10, anchor='c')
        c.setFont('Arial', 8)
        c.drawString(56.7, y_(768.8 + 6.4), f'Practice Paper {self.n}')
        text_at(c, 538.6, 777.2, '[Turn over', size=10, anchor='r', bold=True)

    # ---------------------------------------------------------- data pages
    def data_pages(self, c):
        rows2 = [
            ('acceleration of free fall', '<i>g</i>', '9.81 m s<sup>–2</sup>'),
            ('speed of light in free space', '<i>c</i>', '3.00 × 10<sup>8</sup> m s<sup>–1</sup>'),
            ('elementary charge', '<i>e</i>', '1.60 × 10<sup>–19</sup> C'),
            ('unified atomic mass unit', '1 u', '1.66 × 10<sup>–27</sup> kg'),
            ('rest mass of proton', '<i>m</i><sub>p</sub>', '1.67 × 10<sup>–27</sup> kg'),
            ('rest mass of electron', '<i>m</i><sub>e</sub>', '9.11 × 10<sup>–31</sup> kg'),
            ('Avogadro constant', '<i>N</i><sub>A</sub>', '6.02 × 10<sup>23</sup> mol<sup>–1</sup>'),
            ('molar gas constant', '<i>R</i>', '8.31 J K<sup>–1</sup> mol<sup>–1</sup>'),
            ('Boltzmann constant', '<i>k</i>', '1.38 × 10<sup>–23</sup> J K<sup>–1</sup>'),
            ('gravitational constant', '<i>G</i>', '6.67 × 10<sup>–11</sup> N m<sup>2</sup> kg<sup>–2</sup>'),
            ('permittivity of free space', '<i>ε</i><sub>0</sub>', '8.85 × 10<sup>–12</sup> F m<sup>–1</sup>'),
        ]
        text_at(c, 51.1, 65.8, 'Data', bold=True)
        lx, eqx = 51.1, 274.4

        def row(lbl, top, lhs, rhs_items, label_x=51.1, lhs_r=eqx):
            if lbl:
                text_at(c, label_x, top, lbl)
            box = math_box(lhs if isinstance(lhs, list) else [lhs])
            rb = math_box(rhs_items)
            base = y_(top + BASE)
            box.draw(c, lhs_r - box.w, base)
            eq = math_box([f'{EQ_SPACE}={EQ_SPACE}'])
            eq.draw(c, lhs_r, base)
            rb.draw(c, lhs_r + eq.w, base)

        for k, (lbl, lhs, rhs) in enumerate(rows2):
            row(lbl, 91.8 + 26 * k, lhs, [rhs])
        row('', 372.1, ['(', Frac('1', ['4π<i>ε</i><sub>0</sub>'])], ['8.99 × 10<sup>9</sup> m F<sup>–1</sup>)'])
        row('Planck constant', 405.2, '<i>h</i>', ['6.63 × 10<sup>–34</sup> J s'])
        row('Stefan–Boltzmann constant', 431.2, '<i>σ</i>', ['5.67 × 10<sup>–8</sup> W m<sup>–2</sup> K<sup>–4</sup>'])
        text_at(c, 51.1, 479.2, 'Formulae', bold=True)
        row('uniformly accelerated motion', 508.3, '<i>s</i>', ['<i>ut</i> + ', Frac('1', '2', small=True), ' <i>at</i><sup>2</sup>'])
        row('', 524.1, '<i>v</i><sup>2</sup>', ['<i>u</i><sup>2</sup> + 2<i>as</i>'])
        row('hydrostatic pressure', 550.1, 'Δ<i>p</i>', ['<i>ρg</i>Δ<i>h</i>'])
        row('upthrust', 576.1, '<i>F</i>', ['<i>ρgV</i>'])
        row('Doppler effect for sound waves', 612.9, '<i>f</i><sub>o</sub>',
            [Frac('<i>f</i><sub>s</sub><i>v</i>', '<i>v</i> ± <i>v</i><sub>s</sub>')])
        row('electric current', 644.6, '<i>I</i>', ['<i>Anvq</i>'])
        row('resistors in series', 670.6, '<i>R</i>', ['<i>R</i><sub>1</sub> + <i>R</i><sub>2</sub> + ...'])
        row('resistors in parallel', 701.0, [Frac('1', '<i>R</i>')],
            [Frac('1', '<i>R</i><sub>1</sub>'), ' + ', Frac('1', '<i>R</i><sub>2</sub>'), ' + ...'])

    def formulae_page(self, c):
        lx, r = 52.6, 275.9

        def row(lbl, top, lhs, rhs):
            if lbl:
                text_at(c, lx, top, lbl)
            lb = math_box(lhs if isinstance(lhs, list) else [lhs])
            rb = math_box(rhs)
            base = y_(top + BASE)
            lb.draw(c, r - lb.w, base)
            eq = math_box([f'{EQ_SPACE}={EQ_SPACE}'])
            eq.draw(c, r, base)
            rb.draw(c, r + eq.w, base)

        e0 = '<i>ε</i><sub>0</sub>'
        row('gravitational potential', 71.2, '<i>ϕ</i>', ['– ', Frac('<i>GM</i>', '<i>r</i>')])
        row('gravitational potential energy', 107.4, '<i>E</i><sub>P</sub>', ['– ', Frac('<i>GMm</i>', '<i>r</i>')])
        row('pressure of an ideal gas', 143.6, '<i>p</i>',
            [Frac('1', '3', small=True), Frac('<i>Nm</i>', '<i>V</i>'), ' ⟨<i>c</i><sup>2</sup>⟩'])
        row('simple harmonic motion', 172.4, '<i>a</i>', ['– <i>ω</i><sup>2</sup><i>x</i>'])
        row('velocity of particle in s.h.m.', 198.4, '<i>v</i>', ['<i>v</i><sub>0</sub> cos <i>ωt</i>'])
        row('', 216.9, '<i>v</i>', ['± <i>ω</i> ', Sqrt('(<i>x</i><sub>0</sub><sup>2</sup> – <i>x</i><sup>2</sup>)')])
        row('electric potential', 250.6, '<i>V</i>', [Frac('<i>Q</i>', f'4π{e0}<i>r</i>')])
        row('electrical potential energy', 291.3, '<i>E</i><sub>P</sub>', [Frac('<i>Qq</i>', f'4π{e0}<i>r</i>')])
        row('capacitors in series', 330.3, [Frac('1', '<i>C</i>')],
            [Frac('1', '<i>C</i><sub>1</sub>'), ' + ', Frac('1', '<i>C</i><sub>2</sub>'), ' + ...'])
        row('capacitors in parallel', 361.9, '<i>C</i>', ['<i>C</i><sub>1</sub> + <i>C</i><sub>2</sub> + ...'])
        row('discharge of a capacitor', 395.3, '<i>x</i>',
            ['<i>x</i><sub>0</sub>e', Sup('–', Frac('<i>t</i>', '<i>RC</i>'))])
        row('Hall voltage', 432.9, '<i>V</i><sub>H</sub>', [Frac('<i>BI</i>', '<i>ntq</i>')])
        row('alternating current/voltage', 463.2, '<i>x</i>', ['<i>x</i><sub>0</sub> sin <i>ωt</i>'])
        row('radioactive decay', 489.2, '<i>x</i>', ['<i>x</i><sub>0</sub>e<sup>–<i>λt</i></sup>'])
        row('decay constant', 522.5, '<i>λ</i>', [Frac('0.693', ['<i>t</i>', Low(Frac('1', '2', small=True))])])
        row('intensity reflection coefficient', 570.9, [Frac('<i>I</i><sub>R</sub>', '<i>I</i><sub>0</sub>')],
            [Frac('(<i>Z</i><sub>1</sub> – <i>Z</i><sub>2</sub>)<sup>2</sup>', '(<i>Z</i><sub>1</sub> + <i>Z</i><sub>2</sub>)<sup>2</sup>')])
        row('Stefan–Boltzmann law', 606.9, '<i>L</i>', ['4π<i>σr</i><sup>2</sup><i>T</i><sup>4</sup>'])
        # Doppler redshift uses ≈ rather than =
        text_at(c, lx, 640.3, 'Doppler redshift')
        base = y_(640.3 + BASE)
        lb = math_box([Frac('Δ<i>λ</i>', '<i>λ</i>')])
        lb.draw(c, r - lb.w, base)
        rb = math_box([' ≈ ', Frac('Δ<i>f</i>', '<i>f</i>'), ' ≈ ', Frac('<i>v</i>', '<i>c</i>')])  # en-spaced by math_box
        rb.draw(c, r, base)

    # ---------------------------------------------------------- build
    def build(self, path):
        q_pages, report = [], {'parts': {}, 'totals': []}
        for i, q in enumerate(self.paper.questions, 1):
            items, part_marks, total = flatten(i, q)
            report['parts'].update(part_marks)
            report['totals'].append(total)
            q_pages.extend(paginate(items))
        content = 3 + len(q_pages)
        total_pages = int(math.ceil(content / 4.0) * 4)
        c = rl_canvas.Canvas(path, pagesize=A4)
        c.setTitle(f'A Level Physics 9702 Practice Paper {self.n}')
        c.setAuthor('F3XP M.A.R.S.')
        self.cover(c, total_pages)
        c.showPage()
        self.furniture(c, 2, total_pages)
        self.data_pages(c)
        c.showPage()
        self.furniture(c, 3, total_pages)
        self.formulae_page(c)
        c.showPage()
        for k, page in enumerate(q_pages):
            pn = 4 + k
            self.furniture(c, pn, total_pages, turn_over=pn < content)
            for it, top in page:
                _draw_labels(c, it, top)
                it.draw(c, top)
            c.showPage()
        for pn in range(content + 1, total_pages + 1):
            self.furniture(c, pn, total_pages, blank=True, turn_over=False)
            c.showPage()
        c.save()
        report['pages'] = total_pages
        report['q_pages'] = [len(paginate(flatten(i, q)[0])) for i, q in enumerate(self.paper.questions, 1)]
        return report

# ------------------------------------------------------------------ mark scheme

LW, LH = landscape(A4)           # 841.89 x 595.28
MS_L, MS_C1, MS_C2, MS_R = 62.4, 124.6, 736.0, 778.6
MS_TOP, MS_BOTTOM = 49.9, 535.0


def ly(top):
    return LH - top


class MSDoc:
    def __init__(self, paper):
        self.paper = paper
        self.n = paper.number

    def header(self, c, pageno, total):
        draw_rich(c, MS_L, ly(21.6 + 8.8), f'9702/4{self.n}')
        draw_rich(c, LW / 2, ly(21.6 + 8.8), f'A Level Physics Practice Paper {self.n} – Mark Scheme', anchor='c')
        draw_rich(c, LW / 2, ly(34.2 + 8.8), 'PRACTICE PAPER', anchor='c', bold=True)
        draw_rich(c, 779.8, ly(21.6 + 8.8), SERIES, anchor='r')
        c.setFont('Arial', 8)
        c.drawCentredString(LW / 2, ly(549.9 + 6.4), f'Page {pageno} of {total}')

    def cover(self, c, total):
        y = lambda t: PH - t
        codes.logo(c, CENTRE - 95, y(62), 190, 34, align='center')
        draw_rich(c, 56.7, y(104.6 + 14.4), f'A Level Physics Practice Paper {self.n}', size=18, bold=True)
        c.setLineWidth(0.5)
        c.line(56.7, y(137), 538.6, y(137))
        c.line(56.7, y(215), 538.6, y(215))
        draw_rich(c, 56.7, y(150), 'PHYSICS', size=10, bold=True)
        draw_rich(c, 538.6, y(150), f'9702/4{self.n}', size=10, anchor='r', bold=True)
        draw_rich(c, 56.7, y(168), 'Paper 4 A Level Structured Questions', size=10)
        draw_rich(c, 538.6, y(168), SERIES, size=10, anchor='r', bold=True)
        draw_rich(c, 56.7, y(186), 'MARK SCHEME', size=10)
        draw_rich(c, 56.7, y(204), 'Maximum Mark: 100', size=10)
        c.rect(165.0, y(278), 330.0, 42.0)
        draw_rich(c, CENTRE, y(262), 'Practice paper', size=10, anchor='c', bold=True)
        paras = [
            'This mark scheme goes with the practice question paper of the same number. It shows the answers and '
            'the marking points that the paper was written to test, set out in the layout of the 2025 Cambridge '
            'International mark schemes.',
            'Alternative answers that are correct physics should be credited even where they are not listed.',
        ]
        t = 312
        for p in paras:
            for words, last in wrap(p, 538.6 - 56.7, size=10):
                draw_line(c, 56.7, y(t), words, 538.6 - 56.7, 'left', True, size=10)
                t += 12
            t += 12
        c.line(56.7, y(735), 538.6, y(735))
        draw_rich(c, CENTRE, y(749), f'This document consists of <b>{total}</b> printed pages.', size=10, anchor='c')
        c.setFont('Arial', 8)
        draw_rich(c, 538.6, y(792), '[Turn over', size=10, anchor='r', bold=True)

    def guidance(self, c):
        t = MS_TOP
        draw_rich(c, MS_L, ly(t + 8.8), 'Mark categories', bold=True)
        t += 26
        cats = [
            ('B marks', 'Independent marks that do not depend on other marks. The point must be seen in the answer.'),
            ('M marks', 'Method marks on which later <b>A</b> marks depend. If the <b>M</b> mark is not awarded, '
                        'the <b>A</b> marks that follow cannot be awarded either.'),
            ('C marks', 'Compensatory marks. They can be awarded even if the point is not written down, when later '
                        'working shows that it must have been known. If a numerical answer is correct, all the '
                        '<b>C</b> marks before it are awarded automatically.'),
            ('A marks', 'Answer marks. They may depend on an <b>M</b> mark or allow a <b>C</b> mark by implication.'),
        ]
        for k, (h, body) in enumerate(cats):
            draw_rich(c, 68.0, ly(t + 8.8), f'<b>{h[0]}</b>{h[1:]}')
            for words, last in wrap(body, 640):
                draw_line(c, 130.1, ly(t + 8.8), words, 640, 'left', True)
                t += 12.6
            t += 12.6
        t += 12
        draw_rich(c, MS_L, ly(t + 8.8), 'Abbreviations', bold=True)
        t += 22
        abbr = [
            ('/', 'Alternative and acceptable answers for the same marking point.'),
            ('( )', 'Bracketed content indicates words which do not need to be explicitly seen to gain credit but '
                    'which indicate the <b>context</b> for an answer.'),
            ('<u>     </u>', 'Underlined content must be present in the answer to award the mark.'),
            ('ecf', 'Error carried forward: an incorrect earlier answer used correctly later gains the later marks.'),
            ('allow', 'Lists other answers that gain the mark.'),
            ('ignore', 'Lists content that neither gains nor loses credit.'),
        ]
        c.setLineWidth(0.5)
        for a, b in abbr:
            ls = wrap(b, 640)
            h = 8 + 13 * len(ls) + 6
            c.rect(MS_L, ly(t + h), MS_R - MS_L, h)
            c.line(124.6, ly(t), 124.6, ly(t + h))
            draw_rich(c, 68.0, ly(t + 6 + 8.8), a, bold=True)
            for j, (words, last) in enumerate(ls):
                draw_line(c, 130.1, ly(t + 6 + 8.8 + 13 * j), words, 640, 'left', True)
            t += h

    def table_rows(self):
        """Flatten MSRows into drawable rows: (label or '', answer lines, code)."""
        out = []
        aw = MS_C2 - MS_C1 - 7.0
        for row in self.paper.mark_scheme:
            pts = list(row.points)
            for k, (ans, code) in enumerate(pts):
                txt = ans
                if row.note and k == len(pts) - 1:
                    txt = ans + '<br/><br/>' + row.note
                lines = wrap(txt, aw)
                h = max(26.7, 6.0 + 13.0 * len(lines) + 7.7)
                out.append({'label': row.label if k == 0 else '', 'group': row.label,
                            'lines': lines, 'code': code, 'h': h, 'first': k == 0})
        return out

    def build(self, path):
        rows = self.table_rows()
        # paginate rows
        pages, page, t = [], [], MS_TOP + 24.0
        for r in rows:
            if page and t + r['h'] > MS_BOTTOM:
                pages.append(page)
                page, t = [], MS_TOP + 24.0
                r = dict(r, label=r['group'], first=True)
            page.append((r, t))
            t += r['h']
        if page:
            pages.append(page)
        total = 2 + len(pages)
        c = rl_canvas.Canvas(path, pagesize=A4)
        c.setTitle(f'A Level Physics 9702 Practice Paper {self.n} Mark Scheme')
        self.cover(c, total)
        c.showPage()
        c.setPageSize(landscape(A4))
        self.header(c, 2, total)
        self.guidance(c)
        c.showPage()
        aw = MS_C2 - MS_C1 - 7.0
        for k, page in enumerate(pages):
            c.setPageSize(landscape(A4))
            self.header(c, 3 + k, total)
            c.setLineWidth(0.5)
            top = MS_TOP
            hh = 24.0
            c.rect(MS_L, ly(top + hh), MS_R - MS_L, hh)
            for xx in (MS_C1, MS_C2):
                c.line(xx, ly(top), xx, ly(top + hh))
            draw_rich(c, (MS_L + MS_C1) / 2, ly(top + 6.2 + 8.8), 'Question', anchor='c', bold=True)
            draw_rich(c, (MS_C1 + MS_C2) / 2, ly(top + 6.2 + 8.8), 'Answer', anchor='c', bold=True)
            draw_rich(c, (MS_C2 + MS_R) / 2, ly(top + 6.2 + 8.8), 'Marks', anchor='c', bold=True)
            end = page[-1][1] + page[-1][0]['h']
            for xx in (MS_L, MS_C1, MS_C2, MS_R):
                c.line(xx, ly(top + hh), xx, ly(end))
            c.line(MS_L, ly(end), MS_R, ly(end))
            for r, t in page:
                x0 = MS_L if r['first'] else MS_C1
                c.line(x0, ly(t), MS_R, ly(t))
                if r['label']:
                    draw_rich(c, (MS_L + MS_C1) / 2, ly(t + 6.0 + 8.8), r['label'], anchor='c')
                for j, (words, last) in enumerate(r['lines']):
                    draw_line(c, MS_C1 + 3.0, ly(t + 6.0 + 8.8 + 13.0 * j), words, aw, 'left', True)
                draw_rich(c, MS_R - 1.1, ly(t + 6.0 + 8.8), r['code'], anchor='r', bold=True)
            c.showPage()
        c.save()
        return {'pages': total}


def ms_marks(paper):
    out = {}
    for row in paper.mark_scheme:
        out[row.label] = out.get(row.label, 0) + sum(marks_of(code) for _, code in row.points)
    return out
