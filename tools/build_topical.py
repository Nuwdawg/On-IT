#!/usr/bin/env python3
"""Build topical PDFs from the CAIE AS Level IT (9626) Paper 1 past papers.

Every question is cut out of its question paper and mark scheme. The shortlist
in tools/high_signal.json picks 10 questions per syllabus topic; they go into a
questions PDF and a matching mark schemes PDF. tools/question_topics.json gives
the topics of every question.

    python tools/build_topical.py check   # verify every paper splits cleanly
    python tools/build_topical.py dump    # print question text (for classifying)
    python tools/build_topical.py build   # write the two PDFs in topical-papers/
"""
import json
import re
import sys
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "past-papers"
OUT = ROOT / "topical-papers"
TOPICS_FILE = ROOT / "tools" / "question_topics.json"
SHORTLIST_FILE = ROOT / "tools" / "high_signal.json"

TOPICS = {
    1: "Data processing and information",
    2: "Hardware and software",
    3: "Monitoring and control",
    4: "Algorithms and flowcharts",
    5: "eSecurity",
    6: "The digital divide",
    7: "Expert systems",
    8: "Spreadsheets",
    9: "Modelling",
    10: "Database and file concepts",
    11: "Video and audio editing",
}
SESSIONS = {"m": "Feb/March", "s": "May/June", "w": "Oct/Nov"}
SESSION_ORDER = {"m": 0, "s": 1, "w": 2}

# Text that marks the end of question content on a page.
END_MARKERS = (
    "Permission to reproduce items",
    "To avoid the issue of disclosure",
    "Cambridge Assessment International Education is part",
    "Cambridge International Education is part",
    "Cambridge University Press & Assessment is part",
)
FOOTER_RE = re.compile(r"©|UCLES|Turn over|9626/|Page \d|Cambridge University Press")
# Horizontal crop inset from each page edge. Question papers from late 2024 on
# print grey "DO NOT WRITE IN THIS MARGIN" bars 21pt wide down both edges; mark
# schemes have no bars and some tables reach 576 on a 595 wide page.
INSET = {"qp": 23, "ms": 12}

# Question starts for papers whose text layer is scrambled (the only clean
# copies available render correctly but extract as gibberish). Positions were
# read from a readable copy with an identical layout:
# stem -> (starts [(question, page index, y)], skipped page indexes, {page index: content bottom})
LAYOUT_OVERRIDES = {
    "9626_s26_qp_11": (
        [(1, 1, 59.8), (2, 2, 59.8), (3, 3, 59.8), (4, 5, 59.8), (5, 7, 59.8), (6, 7, 410.9), (7, 8, 59.8), (8, 9, 59.8), (9, 11, 59.8)],
        [0, 13, 14, 15], {}),
    "9626_s26_qp_12": (
        [(1, 1, 59.8), (2, 3, 59.8), (3, 5, 59.8), (4, 6, 59.8), (5, 7, 59.8), (6, 8, 59.8), (7, 9, 59.8), (8, 11, 59.8), (9, 11, 371.9)],
        [0], {11: 679.1}),
    "9626_s26_qp_13": (
        [(1, 1, 59.8), (2, 1, 306.9), (3, 1, 475.9), (4, 3, 59.8), (5, 5, 59.8), (6, 6, 59.8), (7, 7, 59.8), (8, 8, 59.8), (9, 11, 59.8), (10, 13, 59.8)],
        [0, 2, 14, 15], {}),
}


def paper_id(path):
    """'9626_s22_qp_11.pdf' -> ('s', 22, '11')."""
    m = re.match(r"9626_([msw])(\d\d)_(?:qp|ms)_(\d\d)\.pdf$", path.name)
    return m.group(1), int(m.group(2)), m.group(3)


def paper_label(path):
    s, yy, v = paper_id(path)
    return f"9626/{v} {SESSIONS[s]} 20{yy}"


def sort_key(path):
    s, yy, v = paper_id(path)
    return (yy, SESSION_ORDER[s], v)


def x_range(page, kind):
    return INSET[kind], page.rect.width - INSET[kind]


def text_lines(page, kind):
    """Non-empty text lines inside the crop area as (x0, y0, x1, y1, text, first_span)."""
    left, right = x_range(page, kind)
    lines = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            t = "".join(s["text"] for s in l["spans"]).strip()
            x0, y0, x1, y1 = l["bbox"]
            if t and x0 >= left and x1 <= right:
                lines.append((x0, y0, x1, y1, t, l["spans"][0]))
    return lines


def ink_boxes(page, kind):
    """Bounding boxes of everything drawn inside the crop area."""
    left, right = x_range(page, kind)
    boxes = [pymupdf.Rect(l[:4]) for l in text_lines(page, kind)]
    for d in page.get_drawings():
        half = (d.get("width") or 0) / 2  # strokes spill past the path's rect
        r = pymupdf.Rect(d["rect"]) + (-half, -half, half, half)
        if r.x0 >= left - 1 and r.x1 <= right + 1 and (r.width > 0.5 or r.height > 0.5):
            boxes.append(r)
    for img in page.get_image_info():
        r = pymupdf.Rect(img["bbox"])
        if r.x1 > left and r.x0 < right:
            boxes.append(r)
    return boxes


def content_limits(page, kind):
    """Vertical range between the running header (page number, barcode) and footer."""
    h = page.rect.height
    boxes = ink_boxes(page, kind)
    lines = text_lines(page, kind)
    top = max([54.0] + [b.y1 for b in boxes if b.y1 < 60.5]
              # the barcode is set in a 5pt font; on some papers it sits lower
              + [y1 for x0, y0, x1, y1, t, span in lines if span["size"] < 6 and y0 < 90]) + 1
    bottom = h - 45
    for x0, y0, x1, y1, t, span in lines:
        if y0 > h - 75 and (FOOTER_RE.search(t) or span["size"] < 6):
            bottom = min(bottom, y0 - 3)
        if any(t.startswith(m) for m in END_MARKERS):
            bottom = min(bottom, y0 - 4)
            for b in boxes:  # the notice has a rule above it
                if b.height < 3 and b.width > 200 and y0 - 12 < b.y1 <= y0:
                    bottom = min(bottom, b.y0 - 2)
    for b in boxes:
        if b.y0 > h - 62:  # corner marks, QR codes
            bottom = min(bottom, b.y0 - 0.3)
    return top, bottom


def body_text(page, kind):
    top, bottom = content_limits(page, kind)
    return " ".join(t for x0, y0, x1, y1, t, _ in text_lines(page, kind)
                    if y0 >= top - 1 and y1 <= bottom + 1)


def is_skip_page(page, kind):
    """Blank pages, "Turn over"-only pages, extra lined pages, copyright pages.

    body_text stops at the copyright notice, so a notice-only page reads as empty.
    """
    body = body_text(page, kind)
    if re.sub(r"[\s\[\]]", "", body) in ("", "BLANKPAGE", "Turnover"):
        return True
    return "If you use the following lined page" in body or body.startswith("Additional page")


def ink_extent(page, top, bottom, kind):
    """Topmost and bottommost ink between top and bottom, or None if empty."""
    ys = [y for b in ink_boxes(page, kind) if b.y0 >= top - 1 and b.y1 <= bottom + 1
          for y in (b.y0, b.y1)]
    return (min(ys), max(ys)) if ys else None


def build_segments(doc, kind, starts, first_page, skip=(), bottoms=None):
    """Turn ordered question starts [(qnum, page, y)] into page segments.

    Returns {qnum: [(page, clip rect), ...]}.
    """
    bottoms = bottoms or {}
    pages = {}
    for pno in range(first_page, doc.page_count):
        page = doc[pno]
        if pno in skip or (not skip and is_skip_page(page, kind)):
            continue
        top, bottom = content_limits(page, kind)
        pages[pno] = (top, min(bottom, bottoms.get(pno, bottom)))

    out = {}
    for i, (q, p_s, y_s) in enumerate(starts):
        if i + 1 < len(starts):
            _, p_e, y_e = starts[i + 1]
        else:
            p_e, y_e = doc.page_count - 1, None
        segs = []
        for pno in range(p_s, p_e + 1):
            if pno not in pages:
                continue
            top, bottom = pages[pno]
            y0 = y_s if pno == p_s else top
            y1 = bottom
            if pno == p_e and y_e is not None:
                y1 = min(y1, y_e - 2)
            if y1 - y0 < 4:
                continue
            ink = ink_extent(doc[pno], y0, y1, kind)
            if ink is None:
                continue
            if pno != p_s:
                y0 = max(top, ink[0] - 4)
            y1 = min(y1, ink[1] + 6)
            if pno != p_s and y1 - y0 < 14:
                continue  # only a stray table border
            left, right = x_range(doc[pno], kind)
            segs.append((pno, pymupdf.Rect(left, y0, right, y1)))
        out[q] = segs
    return out


def qp_layout(doc):
    """Question starts, skipped pages and page bottoms read from the text layer."""
    candidates = []
    for pno in range(1, doc.page_count):
        page = doc[pno]
        if is_skip_page(page, "qp"):
            continue
        for x0, y0, x1, y1, t, span in text_lines(page, "qp"):
            m = re.match(r"(\d{1,2})(\s|$)", span["text"].strip() + " ")
            if x0 < 62 and m and span["size"] >= 10.5:
                candidates.append((int(m.group(1)), pno, y0, x0))
    ones = [c[3] for c in candidates if c[0] == 1]
    qx = ones[0] if ones else 50
    starts, expect = [], 1
    for q, pno, y0, x0 in candidates:
        if q == expect and abs(x0 - qx) < 3:
            starts.append((q, pno, y0 - 4))
            expect += 1
    skip = [pno for pno in range(doc.page_count) if is_skip_page(doc[pno], "qp")]
    bottoms = {pno: content_limits(doc[pno], "qp")[1] for pno in range(doc.page_count)}
    return starts, skip, bottoms


def split_qp(path):
    doc = pymupdf.open(path)
    override = LAYOUT_OVERRIDES.get(path.stem)
    if override:
        starts, skip, bottoms = override
        return doc, build_segments(doc, "qp", starts, 1, set(skip), bottoms)
    starts, _, _ = qp_layout(doc)
    return doc, build_segments(doc, "qp", starts, 1)


def split_ms(path):
    doc = pymupdf.open(path)
    starts, current = [], None
    for pno in range(doc.page_count):
        lines = text_lines(doc[pno], "ms")
        headers = [y0 for x0, y0, x1, y1, t, _ in lines if t == "Question" and x0 < 70]
        if not headers and current is None:
            continue
        for x0, y0, x1, y1, t, _ in sorted(lines, key=lambda l: l[1]):
            m = re.match(r"^(\d{1,2})(\(|$)", t)
            if not (m and x0 < 110 and x1 < 120):
                continue
            q = int(m.group(1))
            if q == current or (current is None and q != 1):
                continue
            above = [h for h in headers if 0 < y0 - h < 40]
            starts.append((q, pno, (max(above) if above else y0) - 8))
            current = q
    first = starts[0][1] if starts else 0
    return doc, build_segments(doc, "ms", starts, first)


def question_text(doc, segs):
    parts = []
    for pno, clip in segs:
        parts.append(doc[pno].get_text(clip=clip))
    t = " ".join(parts)
    t = re.sub(r"\.{4,}", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def qp_files():
    return sorted(PAPERS.glob("9626_*_qp_1*.pdf"), key=sort_key)


def ms_for(qp):
    return qp.with_name(qp.name.replace("_qp_", "_ms_"))


def leftovers(doc, segs, kind):
    """Page furniture (footer, barcode, notice, corner marks) caught inside a cut."""
    found = []
    for pno, clip in segs:
        page = doc[pno]
        h = page.rect.height
        inner = clip + (0, 0.5, 0, -0.5)
        for x0, y0, x1, y1, t, span in text_lines(page, kind):
            r = pymupdf.Rect(x0, y0, x1, y1)
            if not r.intersects(inner):
                continue
            if span["size"] < 6 and t.strip(" ,\t"):
                found.append(f"p{pno + 1} tiny text")
            elif y0 > h - 75 and FOOTER_RE.search(t):
                found.append(f"p{pno + 1} footer {t[:20]!r}")
            elif any(t.startswith(m) for m in END_MARKERS):
                found.append(f"p{pno + 1} notice")
        for b in ink_boxes(page, kind):
            if b.y0 > h - 62 and b.intersects(inner):
                found.append(f"p{pno + 1} footer mark")
    return found


def load_topics():
    data = json.loads(TOPICS_FILE.read_text())
    return data["questions"], data["same_questions"]


def load_shortlist():
    """{topic: [(question paper path, question number), ...]} in reading order."""
    data = json.loads(SHORTLIST_FILE.read_text())
    out = {}
    for n in TOPICS:
        out[n] = []
        for ref in data[str(n)]:  # e.g. "s24_12 Q7"
            m = re.fullmatch(r"([msw]\d\d)_(\d\d) Q(\d+)", ref)
            out[n].append((PAPERS / f"9626_{m.group(1)}_qp_{m.group(2)}.pdf", int(m.group(3))))
    return out


def check_shortlist(questions):
    problems, seen = [], set()
    for n, refs in load_shortlist().items():
        for qp, q in refs:
            topics = questions.get(qp.stem, {}).get(str(q))
            if topics is None:
                problems.append(f"{qp.stem} Q{q} is not a known question")
            elif n not in topics:
                problems.append(f"{qp.stem} Q{q} is listed under topic {n} but tagged {topics}")
            if (qp, q) in seen:
                problems.append(f"{qp.stem} Q{q} is listed twice")
            seen.add((qp, q))
    return problems


def cmd_check():
    """Every paper must split into the same questions as its mark scheme, and
    every question must have at least one topic."""
    questions, same = load_topics()
    ok = True
    for qp in qp_files():
        _, q = split_qp(qp)
        _, m = split_ms(ms_for(qp))
        problems = []
        if not q or sorted(q) != sorted(m):
            problems.append(f"qp has {len(q)} questions, ms has {len(m)}")
        empty = [n for n, segs in list(q.items()) + list(m.items()) if not segs]
        if empty:
            problems.append(f"nothing cut for {sorted(set(empty))}")
        for kind, path, parts in (("qp", qp, q), ("ms", ms_for(qp), m)):
            doc = pymupdf.open(path)
            for n, segs in parts.items():
                junk = leftovers(doc, segs, kind)
                if junk:
                    problems.append(f"{kind} Q{n} includes {', '.join(sorted(set(junk)))}")
        if qp.stem in same:
            original = same[qp.stem]
            doc_a, qa = split_qp(PAPERS / f"{original}.pdf")
            doc_b, qb = split_qp(qp)
            differ = [n for n in qb if question_text(doc_a, qa.get(n, []))[3:]
                      != question_text(doc_b, qb[n])[3:]]
            if sorted(qa) != sorted(qb) or differ:
                problems.append(f"not the same questions as {original}: {differ}")
        else:
            tagged = questions.get(qp.stem, {})
            if sorted(int(n) for n in tagged) != sorted(q):
                problems.append(f"topics given for questions {sorted(map(int, tagged))}")
            bad = [n for n, ts in tagged.items() if not ts or set(ts) - set(TOPICS)]
            if bad:
                problems.append(f"missing or unknown topics for {bad}")
        ok &= not problems
        print(f"{qp.name}: {len(q)} questions  " + ("; ".join(problems) or "ok"))
    problems = check_shortlist(questions)
    ok &= not problems
    print("high_signal.json: " + ("; ".join(problems) or "ok"))
    return 0 if ok else 1


def cmd_dump():
    for qp in qp_files():
        doc, qs = split_qp(qp)
        print(f"\n######## {qp.stem}  ({paper_label(qp)})")
        for q, segs in qs.items():
            print(f"[{qp.stem} Q{q}] {question_text(doc, segs)}")
    return 0


# ---------------------------------------------------------------- build

A4 = pymupdf.paper_rect("a4")
MARGIN_TOP, MARGIN_BOTTOM = 40, 36
LABEL_H = 22
BLUE = (0.10, 0.30, 0.60)
GREY = (0.4, 0.4, 0.4)
MIN_SPLIT_ROOM = 100  # don't start a question piece in less space than this
MIN_PIECE = 60        # nor leave a piece shorter than this on either side of a split
QP_NAME = "AS Level IT 9626 - Paper 1 high-signal questions.pdf"
MS_NAME = "AS Level IT 9626 - Paper 1 high-signal mark schemes.pdf"


def table_borders(page):
    """x positions of a mark scheme table's column borders, read off the
    'Question | Answer | Marks' header row."""
    xs = set()
    for x0, y0, x1, y1, t, _ in text_lines(page, "ms"):
        if t == "Question" and x0 < 70:
            for d in page.get_drawings():
                r = d["rect"]
                if r.width <= 2 and r.y0 <= y1 and r.y1 >= y0:
                    xs.add(round(r.x0))
    return xs


def cut_point(page, clip, max_height, kind):
    """Lowest y in clip, at most max_height below its top, that falls in a gap
    between lines (so a split there cuts no text or picture), or None. In mark
    schemes a split may cross the table's column borders, as at a page break."""
    borders = table_borders(page) if kind == "ms" else set()

    def is_border(b):
        return b.width <= 3 and any(abs(b.x0 + 1 - x) <= 2 for x in borders)

    spans = sorted((b.y0, b.y1) for b in ink_boxes(page, kind)
                   if b.y1 > clip.y0 and b.y0 < clip.y1 and not is_border(b))
    merged = []
    for y0, y1 in spans:
        if merged and y0 <= merged[-1][1] + 1:
            merged[-1][1] = max(merged[-1][1], y1)
        else:
            merged.append([y0, y1])
    cuts = [(a[1] + b[0]) / 2 for a, b in zip(merged, merged[1:]) if b[0] - a[1] >= 4]
    cuts = [y for y in cuts if clip.y0 + MIN_PIECE <= y <= clip.y0 + max_height
            and y <= clip.y1 - MIN_PIECE]
    return max(cuts) if cuts else None


class Writer:
    def __init__(self):
        self.doc = pymupdf.open()
        self.page = None
        self.y = 0
        self.toc = []

    def new_page(self, landscape=False):
        w, h = (A4.height, A4.width) if landscape else (A4.width, A4.height)
        self.page = self.doc.new_page(width=w, height=h)
        self.y = MARGIN_TOP
        return self.page

    def room(self):
        return self.page.rect.height - MARGIN_BOTTOM - self.y

    def heading(self, title):
        """Start a new page with a section title; returns the page index."""
        page = self.new_page()
        page.insert_text((40, 70), title, fontsize=22, fontname="hebo", color=BLUE)
        self.y = 92
        return page.number

    def question(self, label, src, segs, kind):
        """Place a labelled question; returns (page index, label rect).

        A piece that doesn't fit in the space left on a page is split at a gap
        between lines, so long questions run on to the next page instead of
        leaving the bottom of the page empty. Landscape source pages (some mark
        schemes) go on landscape pages, and a piece taller than a whole page is
        scaled down to fit.
        """
        def landscape(pno):
            return src[pno].rect.width > src[pno].rect.height

        def scale(pno, clip, reserve=0):
            usable = (A4.width if landscape(pno) else A4.height) - MARGIN_TOP - MARGIN_BOTTOM
            return min(1.0, (usable - reserve) / clip.height)

        def same_orientation(pno):
            return (self.page.rect.width > self.page.rect.height) == landscape(pno)

        def fits(pno, clip, k, room):
            """How much of clip goes on this page: all of it, a part ending at a cut, or none."""
            if clip.height * k <= room:
                return clip.y1
            if room < MIN_SPLIT_ROOM:
                return None
            return cut_point(src[pno], clip, room / k, kind)

        scales = [scale(pno, clip, LABEL_H if i == 0 else 0) for i, (pno, clip) in enumerate(segs)]
        first_pno, first_clip = segs[0]
        if (self.page is None or not same_orientation(first_pno)
                or fits(first_pno, first_clip, scales[0], self.room() - LABEL_H) is None):
            self.new_page(landscape(first_pno))  # keep the label with the start of the question
        rect = pymupdf.Rect(40, self.y, self.page.rect.width - 40, self.y + 18)
        self.page.draw_line(rect.bl, rect.br, color=BLUE, width=0.8)
        self.page.insert_text((40, self.y + 14), label, fontsize=10, fontname="hebo", color=BLUE)
        placed = (self.page.number, rect)
        self.y += LABEL_H
        for (pno, clip), k in zip(segs, scales):
            while clip.height > 0.5:
                end = fits(pno, clip, k, self.room()) if same_orientation(pno) else None
                if end is None:
                    self.new_page(landscape(pno))
                    continue
                piece = pymupdf.Rect(clip.x0, clip.y0, clip.x1, end)
                target = pymupdf.Rect(piece.x0, self.y, piece.x0 + piece.width * k,
                                      self.y + piece.height * k)
                self.page.show_pdf_page(target, src, pno, clip=piece)
                self.y += piece.height * k + 2
                clip = pymupdf.Rect(clip.x0, end, clip.x1, clip.y1)
                if clip.height > 0.5:
                    self.new_page(landscape(pno))
        self.y += 10
        return placed

    def link(self, page_no, rect, text, to_page_no, to_y=0, size=8):
        """Clickable text right-aligned in rect, jumping to a page."""
        page = self.doc[page_no]
        width = pymupdf.get_text_length(text, fontname="helv", fontsize=size)
        at = pymupdf.Rect(rect.x1 - width, rect.y1 - size - 4, rect.x1, rect.y1)
        page.insert_text((at.x0, rect.y1 - 4), text, fontsize=size, fontname="helv", color=BLUE)
        page.insert_link({"kind": pymupdf.LINK_GOTO, "from": at, "page": to_page_no,
                          "to": pymupdf.Point(0, max(0, to_y - 10))})

    def finish(self, path):
        for page in self.doc:
            if page.number:  # no number on the cover
                text = str(page.number + 1)
                width = pymupdf.get_text_length(text, fontname="helv", fontsize=8)
                page.insert_text(((page.rect.width - width) / 2, page.rect.height - 18), text,
                                 fontsize=8, fontname="helv", color=GREY)
        self.doc.set_toc(self.toc)
        self.doc.save(path, garbage=4, deflate=True)


def cover(w, title, body):
    page = w.new_page()
    page.insert_text((40, 150), "Cambridge International AS Level", fontsize=14,
                     fontname="helv", color=GREY)
    page.insert_text((40, 172), "Information Technology 9626", fontsize=14,
                     fontname="helv", color=GREY)
    page.insert_textbox(pymupdf.Rect(40, 230, A4.width - 40, 340), title, fontsize=30,
                        fontname="hebo", color=BLUE)
    page.insert_textbox(pymupdf.Rect(40, 370, A4.width - 40, 640), body, fontsize=11,
                        fontname="helv")
    page.insert_textbox(pymupdf.Rect(40, 760, A4.width - 40, 800),
                        "Source: Cambridge International 9626 past papers. "
                        "© UCLES / Cambridge University Press & Assessment.",
                        fontsize=8, fontname="helv", color=GREY)


def contents(w, starts):
    """Fill in the contents page now that every topic's first page is known."""
    page = w.doc[1]
    page.insert_text((40, 70), "Contents", fontsize=22, fontname="hebo", color=BLUE)
    y = 120
    for n, first in starts.items():
        page.insert_text((40, y), f"{n}", fontsize=12, fontname="hebo", color=BLUE)
        page.insert_text((66, y), TOPICS[n], fontsize=12, fontname="helv")
        w.link(1, pymupdf.Rect(400, y - 14, A4.width - 40, y + 4), f"p. {first + 1}", first,
               size=11)
        y += 36


def source_label(qp, q, also):
    label = paper_label(qp)
    if qp.stem in also:
        twin = paper_id(Path(also[qp.stem] + ".pdf"))[2]
        label = label.replace(" ", f" and 9626/{twin} ", 1)
    return f"{label} · Question {q}"


def write_pdf(name, kind, title, body, shortlist, also):
    split = split_qp if kind == "qp" else split_ms
    cache = {}
    w = Writer()
    cover(w, title, body)
    w.new_page()  # contents, filled in at the end
    w.toc.append([1, "Contents", 2])
    starts = {}
    for n, refs in shortlist.items():
        heading = f"{n}  {TOPICS[n]}"
        starts[n] = w.heading(heading)
        w.toc.append([1, heading, starts[n] + 1])
        for i, (qp, q) in enumerate(refs, 1):
            path = qp if kind == "qp" else ms_for(qp)
            if path not in cache:
                cache[path] = split(path)
            doc, segs = cache[path]
            label = f"{n}.{i}   {source_label(qp, q, also)}"
            page_no, _ = w.question(label, doc, segs[q], kind)
            w.toc.append([2, label, page_no + 1])
    contents(w, starts)
    w.finish(OUT / name)
    print(f"{name}: {w.doc.page_count} pages")


def cmd_build():
    _, same = load_topics()
    also = {orig: dup for dup, orig in same.items()}
    shortlist = load_shortlist()
    total = sum(len(refs) for refs in shortlist.values())
    each = {len(refs) for refs in shortlist.values()}
    per_topic = f"{each.pop()} per topic" if len(each) == 1 else "a shortlist for each topic"
    first, last = (paper_label(p).split(" ", 1)[1] for p in (qp_files()[0], qp_files()[-1]))
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.pdf"):
        old.unlink()
    write_pdf(QP_NAME, "qp", "Paper 1 Theory\nHigh-signal questions", (
        f"{total} questions, {per_topic} across the {len(TOPICS)} AS Level topics, picked "
        f"from every Paper 1 question from {first} to {last}. In each topic they cover "
        "the points examined most often, favouring longer and more recent questions, "
        "and run in syllabus order.\n\n"
        "Each question is numbered (1.1, 1.2, ...) and labelled with the paper it came "
        f"from. The answers are in \"{MS_NAME}\", numbered the same way."),
        shortlist, also)
    write_pdf(MS_NAME, "ms", "Paper 1 Theory\nHigh-signal mark schemes", (
        f"Mark schemes for the {total} questions in \"{QP_NAME}\", numbered the same way "
        "(1.1, 1.2, ...) and labelled with the paper each question came from."),
        shortlist, also)
    return 0


if __name__ == "__main__":
    cmds = {"check": cmd_check, "dump": cmd_dump, "build": cmd_build}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        sys.exit(__doc__)
    sys.exit(cmds[sys.argv[1]]())
