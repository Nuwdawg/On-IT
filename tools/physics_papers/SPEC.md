# A Level Physics 9702 Paper 4 practice papers: content spec

Three practice papers in the exact layout of the 2025 Cambridge 9702 Paper 4
question papers, each with a mark scheme in the 2025 mark scheme layout.
The layout engine (`engine.py`, `figs.py`) is written separately. Each paper is
one Python module (`paper1.py`, `paper2.py`, `paper3.py`) that only declares
content using the classes below.

Reference papers (read them to absorb the wording and style):
`physics-9702-paper-4/question-papers/9702_s25_qp_41.pdf` ... `9702_w25_qp_44.pdf`
and the matching `mark-schemes/9702_*25_ms_4*.pdf`. Text can be pulled with
`python3 -c "import pymupdf; print(''.join(p.get_text() for p in pymupdf.open(PATH)))"`
and pages rendered with `page.get_pixmap(dpi=80).save(...)`.

## What makes these papers different

The maths practice papers in `maths-9709/` show the target calibre: they look
like standard papers and most questions open with routine parts, but later
parts join two topics, use general constants (answers in terms of symbols),
give hints that are less direct, give a condition instead of an instruction,
and use short contexts. For physics, every question must also have at least
one part that **punishes a gap in fundamental understanding** and
**subverts the expected answer**, for example:

- a formula plugged in blindly gives an impossible result (cos θ > 1, a
  negative time, a speed above c) and the candidate must recognise it;
- the "obvious" answer is wrong because of a hidden subtlety (r.m.s. of a
  non-sinusoidal or rectified waveform; a satellite speeding up when drag
  acts; tension in a conical pendulum independent of angle; work done ON vs
  BY a gas; stopping potential unchanged by intensity; field strength larger
  at the smaller of two connected spheres; ratio of energies at half
  amplitude being 3:1 not 1:1; period of a charged particle in B independent
  of speed);
- a quantity the candidate expects to change does not (or vice versa), and
  they must say why;
- "explain why a student's claim is wrong" parts;
- answers in terms of given symbols rather than numbers.

Keep it fair: everything is inside the 2025-2027 9702 syllabus (A Level topics
12-25, plus AS knowledge they build on). No university material. Data are
realistic. Every number must be checked with Python before it goes in the
mark scheme.

## Paper structure (match the 2025 papers)

- 10 questions, **100 marks in total**, each question 8-12 marks.
- Each question covers its assigned topics (see the allocation in the task).
  Together the 10 questions cover **all 14** A Level topics:
  12 Motion in a circle, 13 Gravitational fields, 14 Temperature,
  15 Ideal gases, 16 Thermodynamics, 17 Oscillations, 18 Electric fields,
  19 Capacitance, 20 Magnetic fields (incl. electromagnetic induction),
  21 Alternating currents, 22 Quantum physics, 23 Nuclear physics,
  24 Medical physics, 25 Astronomy and cosmology.
- Each question starts on a new page and should fill about two pages.
- Command words as Cambridge uses them: State, Define, Explain, Describe,
  Suggest, Calculate, Determine, Show that, Sketch, On Fig. 1.1, draw ...,
  Complete Table 2.1.
- Most questions open with a definition/statement part worth 1-2 marks.
- Use at least 2 figures per question on average (circuits, apparatus, field
  diagrams, graphs on a grid, p-V diagrams, energy levels, spectra...). At
  least 3 questions per paper have a graph on a grid the candidate reads
  from or sketches on.

## Writing conventions

- Rich text uses reportlab mini-HTML: `<i>`, `<b>`, `<sup>`, `<sub>`.
  Quantity symbols in italic (`<i>V</i>`, `<i>V</i><sub>C</sub>`,
  `<i>E</i><sub>K</sub>`), units upright.
- Minus signs and negative powers use an en dash: `m s<sup>–1</sup>`,
  `1.6 × 10<sup>–19</sup> C`. Multiplication sign `×`. Degrees `°C`.
  Greek letters as Unicode: λ ω ρ ε θ φ σ μ Ω τ Δ.
- Bold for **not**, **all**, **two** etc. where Cambridge would bold them:
  `<b>not</b>`.
- Refer to figures as `Fig. 3.1` and tables as `Table 3.1` (question.number).
- Nuclides: `<nuc a="235" z="92"/>U` gives the stacked mass and proton
  numbers in front of the symbol, as Cambridge prints them.
- Part labels: questions have parts (a), (b), (c)... and sub-parts (i), (ii)...

## Content classes (import with `from engine import *`)

```python
PAPER = Paper(
    number=1,                       # 1, 2 or 3
    questions=[Q1, Q2, ...],        # list of Question
    mark_scheme=MS,                 # list of MSRow (see below)
)

Q1 = Question([                     # question number is its position
    Text('Optional stem text at question level.'),
    Part('a', [
        Text('Define the radian.'),
        Lines(2, 1),                # 2 dotted answer lines, last ends "[1]"
    ]),
    Part('b', [
        Text('Stem for (b) ...'),
        Fig(380, 200, draw_fig_1_1, 'Fig. 1.1', note='(not to scale)'),
        Text('More stem text after the figure.'),
        Sub('i', [
            Text('Calculate the angular speed of the rear wheel.'),
            Space(8),               # blank working space, in 13 pt lines
            Answer('angular speed', 'rad s<sup>–1</sup>', 2),
        ]),
        Sub('ii', [
            Text('Show that the distance moved ... is 0.24 m.'),
            Space(7),
            Mark(1),                # lone "[1]" at the right margin
        ]),
    ]),
])
```

Blocks (all can appear at question, part or sub-part level):

| Block | Meaning |
|---|---|
| `Text(rich, align='justify')` | Paragraph. `align` may be `'left'` or `'center'`. Successive Text blocks get a blank line between them (Cambridge style). Use `Text(a + '<br/>' + b)` for lines with no gap. |
| `Lines(n, marks)` | n dotted answer lines; last ends with `[marks]` (`marks=None` for unmarked lines, e.g. before an `Answer`). Convention: marks + 1 lines for explanations (1 mark → 2 lines, 2 → 3, 3 → 4). |
| `Space(n)` | n × 13 pt blank working space. Calculations: [1] 6, [2] 8, [3] 10, [4] 12. |
| `Answer(label, unit, marks)` | `label = ........ unit [marks]` right-aligned. `marks=None` for an earlier line of a multi-answer part (only the last carries the marks). `label` is rich text, e.g. `'<i>C</i>'`; unit may be `''`. |
| `Mark(n)` | Lone `[n]` at the right margin (show-that, drawing on a figure). |
| `Fig(w, h, draw, caption, note='')` | Figure box w × h points, centred on the page. `draw(c)` is called with the origin at the box's bottom-left (reportlab coordinates, y up, units in points). Caption bold below, e.g. `'Fig. 2.1'`; `note` is plain text after the caption, e.g. `'(not to scale)'`. Max width 490. |
| `FigRow([Fig, Fig])` | Figures side by side, each with its own caption. |
| `Table(rows, col_widths, caption, row_heights=None)` | Ruled table, caption bold **above**. `rows` is a list of rows of rich-text cells; empty strings are blank cells for the candidate. Default row height 26; pass `row_heights` to make answer cells taller. |
| `Eq(*items, align='center')` | Displayed equation. Items: rich-text strings, `Frac(num, den)`, `Sqrt(item)`. `num`/`den` may be strings or lists of items. |
| `PageBreak()` | Force the next block onto a new page (rarely needed). |

The engine adds `[Total: n]` at the end of each question automatically from
the marks, and checks the paper totals 100.

## Figures

`draw(c)` receives a reportlab canvas. Use the helpers in `figs.py`
(`from figs import *`) or plain reportlab calls. Cambridge style: black
lines 0.75-1 pt, no colour, labels in Arial 11 pt (regular for words,
italic for quantity symbols), grey (0.6) or hatching for shading, arrows with
small filled heads. Graph grids: 2 mm minor squares (5.67 pt) with heavier
lines every 5 squares, axes labelled `quantity / unit`.

`figs.py` helpers (coordinates in points, origin bottom-left of the figure):

```python
text(c, x, y, s, size=11, anchor='l')   # rich text label; anchor 'l','c','r'; y = baseline
line(c, x1, y1, x2, y2, w=0.75, dash=None)
polyline(c, pts, w=0.75, close=False, fill=None)
arrow(c, x1, y1, x2, y2, w=0.75, head=6)        # head at (x2, y2)
darrow(c, x1, y1, x2, y2, w=0.75, head=6)       # heads both ends
circle(c, x, y, r, w=0.75, fill=None)           # fill: grey level 0-1 or None
rect(c, x, y, w, h, lw=0.75, fill=None)
hatch(c, x, y, w, h, spacing=4, angle=45)       # hatched region (walls, ground)
spring(c, x1, y1, x2, y2, coils=8, amp=5)
dot(c, x, y, r=2)

# circuit symbols between two terminal points, horizontal or vertical,
# drawing the connecting wire as well
resistor(c, x1, y1, x2, y2, label=None)
capacitor(c, x1, y1, x2, y2, label=None)
cell(c, x1, y1, x2, y2, label=None)          # long plate (+) at the (x1, y1) end
switch(c, x1, y1, x2, y2, closed=False)
diode(c, x1, y1, x2, y2)                     # conducts from (x1,y1) to (x2,y2)
lamp(c, x1, y1, x2, y2)
meter(c, x, y, letter)                       # circle r = 9 with V, A, mA...
ac_supply(c, x, y)                           # circle with ~
wire(c, pts)                                 # polyline of wire

# graphs
g = Graph(c, x, y, w, h, xr=(0, 12), yr=(0, 8),
          xmajor=4, ymajor=4, minor=5,           # minor = subdivisions per major
          grid=True, xlabel='<i>V</i><sub>C</sub> / V', ylabel='<i>Q</i> / mC',
          xticks=None, yticks=None,              # None = label every major line, else
                                                 # a list of (value, 'label') tuples
          axes=True,                             # False: draw your own axes
          xlabel_pos='right', ylabel_pos='side', # or 'center' / 'top'
          labels_outside=False)                  # True: tick labels along the grid's
                                                 # bottom and left edges, not on the axes
g.P(xv, yv) -> (px, py)                          # data to figure coordinates
g.curve(f, x0, x1, n=200, w=1)                   # plot y = f(x)
g.points(list_of_xy, w=1)                        # straight segments through points
g.mark(xv, yv, style='x')                        # plotted point (cross) or 'dot'
g.line(x1, y1, x2, y2, w=1.0, dash=None)         # straight line in data coordinates
g.text(xv, yv, s, anchor='l', dx=0, dy=0)        # label at a data point
label(c, x, y, s, anchor='l')                    # text on a white knock-out box
g.finish()                                       # redraw tick and axis labels on top of plotted lines
```

Graph sizes must be whole numbers of minor squares (5.67 pt each).

## Mark scheme (2025 layout)

```python
MS = [
    MSRow('1(a)', [
        ('angle subtended at the centre of a circle', 'B1'),
        ('by an arc equal in length to the radius', 'B1'),
    ]),
    MSRow('1(b)(i)', [
        ('<i>v</i> = <i>rω</i>', 'C1'),
        ('<i>ω</i> = 17 / 0.46 = 37 rad s<sup>–1</sup>', 'A1'),
    ]),
    MSRow('1(b)(ii)', [...], note='optional examiner guidance shown in the same cell'),
]
```

- One tuple per marking point, in order; codes B1, M1, A1, C1 (or B2 etc.).
- Use `<br/>` for line breaks, `<b>or</b>` between alternatives, `allow ...`,
  `ignore ...`, `ecf ...` as Cambridge does.
- The marks in each MSRow must equal the marks printed for that part in the
  question paper. The engine checks this.
- Questions with a total row label like `'1(b)(ii)'` exactly as Cambridge
  writes them.

## Building and checking (engine is ready)

```
cd /home/user/On-IT/tools/physics_papers
python3 build.py 1 --png      # builds paper 1 (use 2 or 3 for the others)
```

This writes `physics-practice-papers/9702 Practice Paper N.pdf` and
`... - mark scheme.pdf`, prints pages per question, and prints a PROBLEM
line for any part whose question-paper marks differ from the mark scheme,
or if the paper is not out of 100. `--png` renders every page to
`/tmp/claude-0/-home-user-On-IT/df9ae915-b3dd-5c06-b77b-3161193db54d/scratchpad/preview/pN_qp_XX.png`
(and `pN_ms_XX.png`) at 80 dpi; open them with the Read tool to check the
layout and the figures. Only touch your own paper module: `engine.py`,
`figs.py` and `richtext.py` are shared (report problems instead of editing
them).

Layout notes:
- A Text right after a figure that names it (`On Fig. 5.2, sketch ...`)
  is kept on the same page as the figure.
- An all-negative y range puts the x-axis along the top with its labels above.
- Numbers and units are tied automatically (`17 m s<sup>–1</sup>` never
  breaks across lines), so write units with ordinary spaces.
- A page holds about 700 pt of content between the page number and the
  footer. Each question starts on a new page; aim for every question to end
  near the bottom of its second page (look at `pages per question`).
- `Fig` captions sit 15 pt below the figure; leave room inside the figure
  box for axis tick labels (about 30 pt below and 30 pt left of a graph's
  plotting area).
