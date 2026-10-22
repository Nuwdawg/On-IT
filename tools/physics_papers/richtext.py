"""Fonts, rich-text runs and a small math layout used by the paper engine.

Rich text is a reportlab-style mini-HTML: <i>, <b>, <u>, <sup>, <sub>, <br/>
and the entities &lt; &gt; &amp;. Body text is Arial 11 pt; Liberation Sans
stands in for Arial (identical metrics) and DejaVu Sans covers the few
symbols Liberation lacks.
"""
import re
from dataclasses import dataclass

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

LIB = '/usr/share/fonts/truetype/liberation/'
DJV = '/usr/share/fonts/truetype/dejavu/'
_FONTS = {
    'Arial': LIB + 'LiberationSans-Regular.ttf',
    'Arial-Bold': LIB + 'LiberationSans-Bold.ttf',
    'Arial-Italic': LIB + 'LiberationSans-Italic.ttf',
    'Arial-BoldItalic': LIB + 'LiberationSans-BoldItalic.ttf',
    'Sym': DJV + 'DejaVuSans.ttf',
    'Sym-Bold': DJV + 'DejaVuSans-Bold.ttf',
    'Sym-Italic': DJV + 'DejaVuSans.ttf',
    'Sym-BoldItalic': DJV + 'DejaVuSans-Bold.ttf',
}
for _name, _path in _FONTS.items():
    if _name not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont(_name, _path))
_ARIAL_CMAP = pdfmetrics.getFont('Arial').face.charToGlyph
# characters Liberation Sans maps but draws as an empty box
_FORCE_SYM = set('∝⇌→')    # → is also too small in Liberation Sans

SUP_SIZE = 8.0     # superscripts and subscripts in 11 pt text
SUP_RISE = 3.85
SUB_RISE = -2.6


def font_name(bold=False, italic=False, sym=False):
    base = 'Sym' if sym else 'Arial'
    if bold and italic:
        return base + '-BoldItalic'
    if bold:
        return base + '-Bold'
    if italic:
        return base + '-Italic'
    return base


def width(text, font, size):
    return pdfmetrics.stringWidth(text, font, size)


@dataclass
class Run:
    text: str
    font: str
    size: float
    rise: float = 0.0
    underline: bool = False
    stack: tuple = None      # (top, bottom) for nuclide notation, drawn right-aligned

    @property
    def w(self):
        if self.stack:
            return max(width(t, self.font, self.size) for t in self.stack) + 0.6
        return width(self.text, self.font, self.size)


_TAG = re.compile(r'<(/?)(i|b|u|sup|sub|br\s*/?)\s*>|<nuc\s+a="([^"]*)"\s+z="([^"]*)"\s*/>')


def _unescape(s):
    return s.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')


def runs(s, size=11.0, bold=False, italic=False):
    """Parse rich text into runs. A '\\n' run marks a forced line break."""
    out = []
    st = {'b': bold, 'i': italic, 'u': False, 'sup': False, 'sub': False}
    pos = 0
    for m in _TAG.finditer(s):
        _emit(out, _unescape(s[pos:m.start()]), st, size)
        closing, tag = m.group(1), m.group(2)
        if m.group(3) is not None:          # <nuc a="4" z="2"/> before an element symbol
            out.append(Run('\x01', 'Arial', size * SUP_SIZE / 11, 0.0, False,
                           (m.group(3), m.group(4))))
        elif tag.startswith('br'):
            out.append(Run('\n', 'Arial', size))
        else:
            st[tag] = not closing
        pos = m.end()
    _emit(out, _unescape(s[pos:]), st, size)
    return out


def _emit(out, text, st, size):
    if not text:
        return
    sz, rise = size, 0.0
    if st['sup']:
        sz, rise = size * SUP_SIZE / 11, size * SUP_RISE / 11
    elif st['sub']:
        sz, rise = size * SUP_SIZE / 11, size * SUB_RISE / 11
    # split into runs of characters Arial can and cannot show
    cur, cur_sym = '', None
    for ch in text:
        sym = (ord(ch) not in _ARIAL_CMAP or ch in _FORCE_SYM) and ch not in '\n'
        if cur and sym != cur_sym:
            out.append(Run(cur, font_name(st['b'], st['i'], cur_sym), sz, rise, st['u']))
            cur = ''
        cur += ch
        cur_sym = sym
    if cur:
        out.append(Run(cur, font_name(st['b'], st['i'], cur_sym), sz, rise, st['u']))


def runs_width(rs):
    return sum(r.w for r in rs if r.text != '\n')


def draw_runs(c, x, y, rs):
    """Draw runs from x with baseline y (reportlab coordinates)."""
    for r in rs:
        if r.text == '\n':
            continue
        w = r.w
        c.setFont(r.font, r.size)
        if r.stack:
            base = r.size * 11 / SUP_SIZE        # size of the text the nuclide sits in
            c.drawRightString(x + w - 0.6, y + base * SUP_RISE / 11, r.stack[0])
            c.drawRightString(x + w - 0.6, y + base * SUB_RISE * 1.25 / 11, r.stack[1])
        else:
            c.drawString(x, y + r.rise, r.text)
        if r.underline:
            c.setLineWidth(0.6)
            c.line(x, y - 1.6, x + w, y - 1.6)
        x += w
    return x


def draw_rich(c, x, y, s, size=11.0, anchor='l', bold=False, italic=False):
    rs = runs(s, size, bold, italic)
    w = runs_width(rs)
    if anchor == 'c':
        x -= w / 2
    elif anchor == 'r':
        x -= w
    draw_runs(c, x, y, rs)
    return w


# ---------------------------------------------------------------- paragraphs

def _words(rs):
    """Split runs into words at ordinary spaces. Returns list of (runs, forced_break_after)."""
    words, cur = [], []
    for r in rs:
        if r.text == '\n':
            words.append((cur, True))
            cur = []
            continue
        parts = r.text.split(' ')
        if r.stack:
            cur.append(r)
            continue
        for k, p in enumerate(parts):
            if k > 0:
                words.append((cur, False))
                cur = []
            if p:
                cur.append(Run(p, r.font, r.size, r.rise, r.underline))
    words.append((cur, False))
    return words


_UNIT = re.compile(r'^(?:[μµkMGmnpc]?(?:m|s|g|N|J|W|V|A|C|F|Ω|K|Pa|Hz|mol|eV|T|Wb|rad|Bq|Gy|Sv|u|ly|pc|AU|min|h|yr|days?|years?)'
                   r'|°C|%)(?:[–-]?\d+)?([.,;:)]*)$')
_TAGS = re.compile(r'<[^>]+>')


def tie_units(s):
    """Join a number to its unit, and the parts of a unit, so a line never
    breaks inside "17 m s–1" (thin spaces, as Cambridge sets them), and keep
    "3.0 × 10" together."""
    s = re.sub(r'\b(Fig\.|Table) (?=\d)', '\\1\u00a0', s)
    toks = s.split(' ')
    if len(toks) < 2:
        return s
    out, chain = toks[0], False
    for a, b in zip(toks, toks[1:]):
        va, vb = _TAGS.sub('', a), _TAGS.sub('', b)
        mb = _UNIT.match(vb)
        if va and mb and (va[-1].isdigit() or (chain and va[-1].isalpha())):
            out += '\u2009' + b
            chain = not mb.group(1)
        elif va and ((va[-1].isdigit() and vb == '×') or (va == '×' and vb[:1].isdigit())):
            out += '\u00a0' + b
            chain = False
        else:
            out += ' ' + b
            chain = False
    return out


def wrap(s, maxw, size=11.0, bold=False, italic=False):
    """Greedy line breaking. Returns lines as (list_of_word_runs, is_last_of_para)."""
    rs = runs(tie_units(s), size, bold, italic)
    space = width(' ', 'Arial', size)
    lines, line, lw = [], [], 0.0
    for wr, forced in _words(rs):
        ww = runs_width(wr)
        if not wr and not forced:
            continue
        if wr:
            add = ww if not line else space + ww
            if line and lw + add > maxw + 0.01:
                lines.append((line, False))
                line, lw = [], 0.0
                add = ww
            line.append(wr)
            lw += add
        if forced:
            lines.append((line, True))
            line, lw = [], 0.0
    if line or not lines:
        lines.append((line, True))
    return lines


def line_width(words, size=11.0):
    space = width(' ', 'Arial', size)
    return sum(runs_width(w) for w in words) + space * max(len(words) - 1, 0)


def draw_line(c, x, y, words, maxw, align, last, size=11.0):
    space = width(' ', 'Arial', size)
    natural = line_width(words, size)
    gap = space
    if align == 'justify' and not last and len(words) > 1:
        gap = space + (maxw - natural) / (len(words) - 1)
    elif align == 'center':
        x += (maxw - natural) / 2
    elif align == 'right':
        x += maxw - natural
    for k, w in enumerate(words):
        if k:
            x += gap
        x = draw_runs(c, x, y, w)


# ---------------------------------------------------------------- math boxes

class Box:
    def __init__(self, w, asc, desc, draw):
        self.w, self.asc, self.desc, self._draw = w, asc, desc, draw

    def draw(self, c, x, y):
        self._draw(c, x, y)


class Frac:
    def __init__(self, num, den, small=False):
        self.num, self.den, self.small = num, den, small


class Sqrt:
    def __init__(self, *items):
        self.items = items


class Sup:
    """Superscript holding math items (e.g. an exponent fraction)."""
    def __init__(self, *items):
        self.items = items


def _as_list(x):
    return list(x) if isinstance(x, (list, tuple)) else [x]


def math_box(items, size=11.0):
    boxes = [_item_box(it, size) for it in _as_list(items)]
    w = sum(b.w for b in boxes)
    asc = max([b.asc for b in boxes] + [size * 0.72])
    desc = max([b.desc for b in boxes] + [size * 0.21])

    def draw(c, x, y):
        for b in boxes:
            b.draw(c, x, y)
            x += b.w
    return Box(w, asc, desc, draw)


def _item_box(it, size):
    if isinstance(it, str):
        rs = runs(it, size)
        w = runs_width(rs)
        asc = size * 0.72 + max([r.rise for r in rs] + [0])
        desc = size * 0.21 + max([-r.rise for r in rs] + [0])
        return Box(w, asc, desc, lambda c, x, y: draw_runs(c, x, y, rs))
    if isinstance(it, Frac):
        fs = size * (7.5 / 11) if it.small else size
        nb, db = math_box(it.num, fs), math_box(it.den, fs)
        bar_w = max(nb.w, db.w) + (1.0 if it.small else 2.0)
        axis = size * 0.32
        gap = 1.2 if it.small else 2.0
        pad = 0.6 if it.small else 1.2

        def draw(c, x, y):
            c.setLineWidth(0.5)
            c.line(x + pad, y + axis, x + pad + bar_w, y + axis)
            nb.draw(c, x + pad + (bar_w - nb.w) / 2, y + axis + gap + nb.desc)
            db.draw(c, x + pad + (bar_w - db.w) / 2, y + axis - gap - db.asc)
        return Box(bar_w + 2 * pad, axis + gap + nb.desc + nb.asc,
                   max(0, -(axis - gap - db.asc - db.desc)), draw)
    if isinstance(it, Sqrt):
        ib = math_box(it.items, size)

        def draw(c, x, y):
            top = y + ib.asc + 1.5
            bot = y - ib.desc
            c.setLineWidth(0.9)
            p = c.beginPath()
            p.moveTo(x, y + 0.35 * ib.asc)
            p.lineTo(x + 2.0, y + 0.45 * ib.asc)
            p.lineTo(x + 4.5, bot)
            p.lineTo(x + 8.0, top)
            p.lineTo(x + 10.0 + ib.w, top)
            c.drawPath(p, stroke=1, fill=0)
            ib.draw(c, x + 9.0, y)
        return Box(ib.w + 11.0, ib.asc + 2.0, ib.desc + 0.5, draw)
    if isinstance(it, Sup):
        fs = size * 0.7
        ib = math_box(it.items, fs)
        rise = size * 0.42

        def draw(c, x, y):
            ib.draw(c, x, y + rise)
        return Box(ib.w, rise + ib.asc, 0, draw)
    if isinstance(it, Box):
        return it
    raise TypeError(f'unknown math item {it!r}')
