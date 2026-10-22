"""9702 Paper 4 practice paper 1: content, figures and mark scheme.

Every numerical answer in the mark scheme was checked with a Python script
using the Data values printed on the real papers (g = 9.81 m s-2,
e = 1.60e-19 C, h = 6.63e-34 J s, 1/4πε0 = 8.99e9 m F-1, ...).
"""
import math
import re

from engine import *
from figs import *

# ------------------------------------------------------------------ helpers


def _ellipse(c, cx, cy, a, b, a0=0.0, a1=360.0, w=0.75, dash=None, n=120):
    """Arc of an ellipse (angles in degrees, anticlockwise from +x)."""
    pts = []
    for k in range(n + 1):
        t = math.radians(a0 + (a1 - a0) * k / n)
        pts.append((cx + a * math.cos(t), cy + b * math.sin(t)))
    polyline(c, pts, w=w, dash=dash)


def _arc(c, cx, cy, r, a0, a1, w=0.75, n=40):
    _ellipse(c, cx, cy, r, r, a0, a1, w=w, n=n)


def _cross(c, x, y, s=2.6):
    line(c, x - s, y - s, x + s, y + s, w=0.6)
    line(c, x - s, y + s, x + s, y - s, w=0.6)


def _band(c, cx, cy, a, b, t, a0=0.0, a1=360.0, fill=0.7, n=120):
    """A flat ring seen obliquely: elliptical band of radial width t."""
    outer, inner = [], []
    for k in range(n + 1):
        ang = math.radians(a0 + (a1 - a0) * k / n)
        outer.append((cx + a * math.cos(ang), cy + b * math.sin(ang)))
        inner.append((cx + (a - t) * math.cos(ang), cy + (b - t * b / a) * math.sin(ang)))
    if a1 - a0 >= 360:
        polyline(c, outer, close=True, fill=fill)
        polyline(c, inner, close=True, fill=1)
    else:
        polyline(c, outer + inner[::-1], close=True, fill=fill)


# ================================================================== Q1 figures


def fig_1_1(c):
    px, py = 170.0, 192.0
    hatch(c, 115, py, 110, 9)
    line(c, 115, py, 225, py, w=1)
    th, L = math.radians(38), 165.0
    bx, by = px + L * math.sin(th), py - L * math.cos(th)
    a, b = bx - px, 20.0
    line(c, px, py, px, by, dash=[3, 2])                      # vertical through P
    _ellipse(c, px, by, a, b, 0, 180, dash=[3, 2])            # far half of the path
    _ellipse(c, px, by, a, b, 180, 360)                       # near half of the path
    arrow(c, 152, by - b + 0.3, 182, by - b + 0.2, head=6)     # direction of motion
    line(c, px, by, bx, by, dash=[3, 2])                      # radius
    dot(c, px, by, 1.6)
    text(c, 214, by + 4, '<i>r</i>')
    line(c, px, py, bx, by, w=1.0)                            # string
    circle(c, bx, by, 6, fill=0)                              # bob
    dot(c, px, py, 1.8)
    text(c, px - 6, py - 12, 'P', anchor='r')
    _arc(c, px, py, 34, -90, -90 + 38)
    ang = math.radians(-90 + 19)
    text(c, px + 45 * math.cos(ang), py + 45 * math.sin(ang) - 4, '<i>θ</i>', anchor='c')
    text(c, 234, 124, 'string, length 0.80 m')
    text(c, bx + 11, by - 4, 'bob, mass 0.20 kg')
    text(c, 18, 18, 'horizontal circle')
    line(c, 70, 28, 96, 47)


def fig_1_2(c):
    g = Graph(c, 70, 35, 40 * MINOR, 40 * MINOR, xr=(0, 8), yr=(0, 1.6), xmajor=1, ymajor=0.2,
              yticks=[(0.2 * k, '%.1f' % (0.2 * k)) for k in range(9)],
              xlabel='<i>ω</i> / rad s<sup>–1</sup>', ylabel='cos <i>θ</i>')
    g.finish()


# ================================================================== Q2 figures


def fig_2_1(c):
    ex, mx, y = 60.0, 350.0, 52.0
    circle(c, ex, y, 34)
    circle(c, mx, y, 11)
    dot(c, ex, y, 1.6)
    dot(c, mx, y, 1.3)
    line(c, ex, y, mx, y, dash=[3, 2])
    nx = ex + 0.90 * (mx - ex)
    dot(c, nx, y, 2.2)
    text(c, nx, y + 7, 'N', anchor='c')
    text(c, ex, y + 40, 'Earth', anchor='c')
    text(c, mx, y + 17, 'Moon', anchor='c')
    line(c, ex, y - 34, ex, 2, w=0.5)
    line(c, mx, y - 11, mx, 2, w=0.5)
    darrow(c, ex, 7, mx, 7)
    text(c, (ex + mx) / 2, 11, '<i>D</i>', anchor='c')


def fig_2_2(c):
    x0, ytop, ybot, xend = 40.0, 152.0, 14.0, 380.0
    ex = 55.0                       # surface of the Earth (not to scale)
    mx, rm = 358.0, 11.0            # centre and radius of the Moon (not to scale)
    hatch(c, x0, ybot, ex - x0, ytop - ybot, spacing=5)
    hatch(c, mx - rm, ybot, 2 * rm, ytop - ybot, spacing=5)
    line(c, ex, ybot, ex, ytop, w=0.5)
    line(c, mx - rm, ybot, mx - rm, ytop, w=0.5)
    line(c, mx + rm, ybot, mx + rm, ytop, w=0.5)
    line(c, x0, ytop, xend, ytop, w=1.0)
    line(c, x0, ytop, x0, ybot - 4, w=1.0)
    text(c, x0 - 5, ytop - 4, '0', anchor='r')
    text(c, x0 - 7, 80, '<i>φ</i>', anchor='r')
    text(c, xend + 4, ytop - 4, '<i>x</i>')
    xn = x0 + 0.90 * (mx - x0)
    line(c, xn, ytop, xn, ytop + 4)
    text(c, xn - 2, ytop + 8, '0.90<i>D</i>', anchor='c')
    text(c, (x0 + ex) / 2 + 2, 2, 'Earth', anchor='c')
    text(c, mx, 2, 'Moon', anchor='c')
    dot(c, ex, 28, 2.4)
    text(c, ex + 6, 25, 'S')


# ================================================================== Q3 figure


def _tube(c, pts, gap=3.0, w=0.75):
    """Narrow tube drawn as two parallel lines along a path of straight segments."""
    def offset(sign):
        out = []
        for k, (x, y) in enumerate(pts):
            if k == 0:
                dx, dy = pts[1][0] - x, pts[1][1] - y
            else:
                dx, dy = x - pts[k - 1][0], y - pts[k - 1][1]
            L = math.hypot(dx, dy)
            nx, ny = -dy / L, dx / L
            if 0 < k < len(pts) - 1:
                ex_, ey_ = pts[k + 1][0] - x, pts[k + 1][1] - y
                L2 = math.hypot(ex_, ey_)
                mx_, my_ = -ey_ / L2, ex_ / L2
                out.append((x + sign * gap * (nx + mx_), y + sign * gap * (ny + my_)))
            else:
                out.append((x + sign * gap * nx, y + sign * gap * ny))
        return out
    polyline(c, offset(1), w=w)
    polyline(c, offset(-1), w=w)


def fig_3_1(c):
    # vessel A on a heater
    rect(c, 40, 48, 70, 58, lw=1)
    rect(c, 40, 34, 70, 9, lw=0.75, fill=0.6)
    text(c, 34, 35, 'heater', anchor='r')
    text(c, 75, 72, 'A', anchor='c')
    # water bath and vessel B
    polyline(c, [(190, 140), (190, 12), (330, 12), (330, 140)], w=1)
    line(c, 190, 131, 252, 131, w=0.6)
    line(c, 258, 131, 330, 131, w=0.6)
    for xx in range(198, 330, 14):
        if not 246 <= xx <= 262:
            line(c, xx, 127, xx + 6, 127, w=0.5)
    rect(c, 210, 26, 95, 92, lw=1)
    text(c, 257.5, 68, 'B', anchor='c')
    # connecting tube
    rect(c, 72.6, 104.5, 4.8, 3, lw=0, fill=1)
    rect(c, 252.6, 116.5, 4.8, 3, lw=0, fill=1)
    _tube(c, [(75, 106), (75, 156), (255, 156), (255, 118)], gap=2.4)
    text(c, 165, 164, 'narrow tube', anchor='c')
    text(c, 336, 70, 'water at')
    text(c, 336, 57, '27 °C')


# ================================================================== Q4 figures


def fig_4_1(c):
    x1, x2 = 80.0, 180.0
    rect(c, x1, 30, x2 - x1, 32, lw=0, fill=0.85)            # water
    polyline(c, [(x1, 140), (x1, 30), (x2, 30), (x2, 140)], w=1.2)
    rect(c, x1 + 0.6, 62, x2 - x1 - 1.2, 14, lw=0.75)          # piston
    hatch(c, x1 + 0.6, 62, x2 - x1 - 1.2, 14, spacing=4)
    text(c, 130, 41, 'water', anchor='c')
    for xx in (100, 130, 160):
        arrow(c, xx, 108, xx, 79, head=6)
    text(c, 130, 122, 'atmosphere', anchor='c')
    text(c, 196, 65, 'piston')
    line(c, 194, 68, 181, 69, w=0.5)
    rect(c, 90, 14, 80, 8, lw=0.75, fill=0.6)
    text(c, 196, 14, 'heater')
    line(c, 194, 17, 171, 18, w=0.5)


def fig_4_2(c):
    g = Graph(c, 85, 40, 45 * MINOR, 45 * MINOR, xr=(0, 4.5), yr=(0, 4.5), xmajor=0.5, ymajor=0.5,
              xticks=[(v, str(v)) for v in range(5)], yticks=[(v, str(v)) for v in range(5)],
              xlabel='<i>V</i> / 10<sup>–3</sup> m<sup>3</sup>', ylabel='<i>p</i> / 10<sup>5</sup> Pa')
    A, B, C = (1, 1), (4, 1), (1, 4)
    g.points([A, B, C, A], w=1.3)
    for p, q in (((2.25, 1), (2.75, 1)), ((2.68, 2.32), (2.32, 2.68)), ((1, 2.75), (1, 2.25))):
        arrow(c, *g.P(*p), *g.P(*q), w=1.3, head=8)
    for (xv, yv), s, dx, dy in ((A, 'A', -11, -13), (B, 'B', 5, -13), (C, 'C', -11, 3)):
        px, py = g.P(xv, yv)
        label(c, px + dx, py + dy, s)
    g.finish()


# ================================================================== Q5 figures


def fig_5_1(c):
    hatch(c, 60, 112, 100, 9)
    line(c, 60, 112, 160, 112, w=1)
    spring(c, 110, 112, 110, 42, coils=8, amp=7)
    rect(c, 88, 12, 44, 30, lw=1)
    text(c, 126, 73, 'spring')
    text(c, 140, 22, 'block')


def fig_5_2(c):
    g = Graph(c, 50, 12, 60 * MINOR, 30 * MINOR, xr=(0, 1.2), yr=(-6, 6), xmajor=0.1, ymajor=2,
              xticks=[(0.2 * k, '%.1f' % (0.2 * k)) for k in range(1, 7)],
              yticks=[(v, str(v).replace('-', '–')) for v in range(-6, 7, 2)],
              xlabel='<i>t</i> / s', ylabel='<i>x</i> / cm')
    g.curve(lambda t: 4.0 * math.cos(2 * math.pi * (t - 0.3) / 0.8), 0, 1.2, n=400, w=1.1)
    g.finish()


# ================================================================== Q6 figures


def fig_6_1(c):
    cx, cy, r = 110.0, 108.0, 45.0
    rect(c, 106, 20, 8, cy - r - 20 + 0.5, lw=0.75, fill=0.75)
    rect(c, 78, 12, 64, 8, lw=0.75, fill=0.75)
    circle(c, cx, cy, r, w=1)
    dot(c, cx, cy, 1.6)
    line(c, cx, cy, cx + r, cy)
    text(c, cx + r / 2, cy + 4, '0.10 m', anchor='c')
    text(c, 176, 146, 'metal sphere X')
    line(c, 174, 149, cx + r * 0.72, cy + r * 0.69, w=0.5)
    text(c, 132, 30, 'insulating stand')
    line(c, 130, 33, 115, 38, w=0.5)


def fig_6_2(c):
    y = 52.0
    circle(c, 60, y, 32, w=1)
    circle(c, 345, y, 16, w=1)
    line(c, 92, y, 200, y, w=1)
    line(c, 214, y, 329, y, w=1)
    line(c, 196, y - 7, 204, y + 7)
    line(c, 210, y - 7, 218, y + 7)
    text(c, 60, y + 40, 'sphere X', anchor='c')
    text(c, 345, y + 24, 'sphere Y', anchor='c')
    text(c, 150, y + 7, 'long thin wire', anchor='c')


# ================================================================== Q7 figures


def fig_7_1(c):
    g = Graph(c, 50, 12, 60 * MINOR, 40 * MINOR, xr=(0, 60), yr=(-9, 15), xmajor=5, ymajor=3,
              xticks=[(v, str(v)) for v in range(10, 61, 10)],
              yticks=[(v, str(v).replace('-', '–')) for v in range(-9, 16, 3)],
              ylabel='<i>V</i> / V')
    px, py = g.P(60, 0)
    text(c, px + 6, py - 4, '<i>t</i> / ms')
    pts = [(0, 12), (5, 12), (5, -6), (15, -6), (15, 12), (25, 12), (25, -6), (35, -6), (35, 12),
           (45, 12), (45, -6), (55, -6), (55, 12), (60, 12)]
    g.points(pts, w=1.3)
    g.finish()


def fig_7_2(c):
    top, bot = 128.0, 20.0
    wire(c, [(40, bot), (40, top), (100, top)])
    ac_supply(c, 40, (top + bot) / 2)
    diode(c, 100, top, 150, top)
    wire(c, [(150, top), (300, top)])
    wire(c, [(40, bot), (300, bot)])
    capacitor(c, 210, top, 210, bot, label='100 μF')
    resistor(c, 300, top, 300, bot, label='1.0 kΩ')
    dot(c, 210, top)
    dot(c, 210, bot)
    darrow(c, 372, bot + 3, 372, top - 3)
    text(c, 380, (top + bot) / 2 - 4, '<i>V</i><sub>OUT</sub>')
    line(c, 300, top, 372, top, w=0.5, dash=[2, 2])
    line(c, 300, bot, 372, bot, w=0.5, dash=[2, 2])


# ================================================================== Q8 figures


def fig_8_1(c):
    yb = 66.0                                   # line of the beam
    arrow(c, 8, yb, 52, yb, head=6)
    text(c, 10, yb + 6, 'ions')
    # first barrier with slit S1
    line(c, 60, 34, 60, yb - 4, w=1.6)
    line(c, 60, yb + 4, 60, 98, w=1.6)
    text(c, 60, 103, 'S<sub>1</sub>', anchor='c')
    # plates, with E and B1 between them
    rect(c, 74, 88, 124, 5, lw=0.75, fill=0.6)
    rect(c, 74, 39, 124, 5, lw=0.75, fill=0.6)
    text(c, 136, 98, '+', anchor='c')
    text(c, 136, 27, '–', anchor='c')
    for xx in range(88, 170, 20):
        for yy in (54, 78):
            _cross(c, xx, yy)
    line(c, 60, yb, 210, yb, w=1.0)
    text(c, 136, 10, '<i>E</i> and <i>B</i><sub>1</sub>', anchor='c')
    # second barrier with slit S2, detector above the slit
    line(c, 210, 26, 210, yb - 4, w=1.6)
    line(c, 210, yb + 4, 210, 232, w=1.6)
    text(c, 205, yb + 6, 'S<sub>2</sub>', anchor='r')
    rect(c, 210, 140, 5, 88, lw=0.75, fill=0.25)
    text(c, 204, 180, 'detector', anchor='r')
    # semicircular path in B2
    r = 64.0
    pts = [(210 + r * math.sin(t), yb + r - r * math.cos(t))
           for t in [math.pi * k / 120 for k in range(121)]]
    polyline(c, pts, w=1.0)
    arrow(c, 210 + r, yb + r - 8, 210 + r, yb + r + 4, head=7)
    text(c, 282, yb + r - 4, 'path of ions')
    for xx in range(236, 413, 22):
        for yy in range(36, 229, 22):
            d = math.hypot(xx - 210, yy - (yb + r))
            if abs(d - r) < 7 or (278 <= xx <= 352 and yb + r - 14 <= yy <= yb + r + 10):
                continue
            _cross(c, xx, yy)
    text(c, 320, 10, '<i>B</i><sub>2</sub> only', anchor='c')


def fig_8_2(c):
    hatch(c, 20, 0, 340, 9)
    line(c, 20, 9, 360, 9, w=1)
    for mx in (110.0, 270.0):
        rect(c, mx - 12, 9, 24, 90, lw=1)
        line(c, mx - 12, 54, mx + 12, 54)
        text(c, mx, 72, 'N', anchor='c')
        text(c, mx, 27, 'S', anchor='c')
    _band(c, 110, 130, 36, 10, 5)
    _band(c, 270, 130, 36, 10, 5, a0=-78, a1=258)
    text(c, 110, 148, 'complete copper ring', anchor='c')
    text(c, 270, 148, 'copper ring with slit', anchor='c')
    text(c, 322, 103, 'slit')
    line(c, 320, 107, 274, 119, w=0.5)
    text(c, 190, 58, 'bar magnet', anchor='c')
    line(c, 160, 62, 123, 66, w=0.5)
    line(c, 220, 62, 257, 66, w=0.5)


# ================================================================== Q9 figure


def fig_9_1(c):
    g = Graph(c, 55, 35, 70 * MINOR, 35 * MINOR, xr=(0, 14), yr=(0, 7), xmajor=1, ymajor=1,
              yticks=[(v, str(v)) for v in range(7)] + [(7, '')],
              xlabel='<i>f</i> / 10<sup>14</sup> Hz',
              ylabel='<i>E</i><sub>K max</sub> / 10<sup>–19</sup> J', ylabel_pos='top')
    g.line(5.0, 0, 14.0, 6.0, w=1.3)
    px, py = g.P(11.0, 4.7)
    label(c, px, py, 'metal X', anchor='r')
    g.finish()


# ================================================================== Q10 figures


def fig_10_1(c):
    line(c, 30, 120, 300, 120, w=1)                 # skin surface
    rect(c, 118, 120, 84, 6, lw=0.75, fill=0.6)     # gel
    rect(c, 130, 126, 60, 26, lw=1)                 # transducer
    text(c, 208, 135, 'transducer')
    text(c, 112, 121, 'gel', anchor='r')
    hatch(c, 30, 8, 270, 30, spacing=5)
    line(c, 30, 38, 300, 38, w=1)
    label(c, 70, 19, 'bone', anchor='c')
    text(c, 70, 75, 'soft tissue', anchor='c')
    arrow(c, 150, 116, 150, 42, head=7)
    arrow(c, 170, 42, 170, 116, head=7)
    darrow(c, 262, 120, 262, 38)
    text(c, 268, 75, '6.0 cm')


def _planck(lam_nm, T):
    lam = lam_nm * 1e-9
    x = 6.63e-34 * 3.00e8 / (lam * 1.38e-23 * T)
    return lam ** -5 / math.expm1(x) if x < 700 else 0.0


def fig_10_2(c):
    g = Graph(c, 45, 35, 50 * MINOR, 30 * MINOR, xr=(0, 2000), yr=(0, 1.2), xmajor=200, ymajor=0.2,
              xticks=[(v, str(v)) for v in range(0, 2001, 400)],
              xlabel='<i>λ</i> / nm', ylabel='relative intensity', ylabel_pos='top')
    for lmax, name in ((320, 'P'), (960, 'Q')):
        # temperature for which the peak (from Planck's law) is exactly at lmax
        T = 6.63e-34 * 3.00e8 / (4.965114 * 1.38e-23 * lmax * 1e-9)
        peak = _planck(lmax, T)
        g.curve(lambda l, T=T, peak=peak: _planck(l, T) / peak, 30, 2000, n=500, w=1.1)
        px, py = g.P(lmax, 1.0)
        label(c, px + 9, py + 3, name)
    g.finish()


# ================================================================== questions

Q1 = Question([
    Text('A small bob of mass 0.20 kg is attached to one end of a light inextensible string of length '
         '0.80 m. The other end of the string is attached to a fixed point P. The bob moves with constant '
         'speed in a horizontal circle, as shown in Fig. 1.1.'),
    Fig(400, 212, fig_1_1, 'Fig. 1.1'),
    Text('The string makes an angle <i>θ</i> with the vertical. The angular speed of the bob is <i>ω</i>.'),
    Part('a', [
        Text('Explain why the bob is accelerating even though its speed is constant.'),
        Lines(2, 1),
    ]),
    Part('b', [
        Text('By considering the horizontal component of the tension <i>T</i> in the string, show that'),
        Eq('<i>T</i> = <i>mω</i><sup>2</sup><i>L</i>'),
        Text('where <i>m</i> is the mass of the bob and <i>L</i> is the length of the string.'),
        Space(6),
        Mark(2),
    ]),
    Part('c', [
        Text('The string breaks when the tension in it exceeds 12 N. Calculate the maximum angular speed at '
             'which the bob can move in this way.'),
        Space(7),
        Answer('maximum angular speed', 'rad s<sup>–1</sup>', 2),
    ]),
    Part('d', [
        Text('The angular speed <i>ω</i> of the bob is now varied.'),
        Text('On Fig. 1.2, sketch the variation of cos <i>θ</i> with <i>ω</i> for values of <i>ω</i> from 0 '
             'to 8.0 rad s<sup>–1</sup>.'),
        Fig(322, 272, fig_1_2, 'Fig. 1.2'),
        Mark(3),
    ]),
    Part('e', [
        Text('The bob is replaced by a bob of mass 0.40 kg. The string is unchanged.'),
        Text('State and explain the effect, if any, of this change on the line you have drawn on Fig. 1.2.'),
        Lines(3, 2),
    ]),
])

Q2 = Question([
    Part('a', [
        Text('Define <i>gravitational potential</i> at a point.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('The Earth and the Moon may be considered to be isolated uniform spheres. The mass of the Earth '
             'is 5.97 × 10<sup>24</sup> kg and the mass of the Moon is 7.35 × 10<sup>22</sup> kg. The distance '
             'between their centres is <i>D</i>, as shown in Fig. 2.1.'),
        Fig(400, 100, fig_2_1, 'Fig. 2.1', note='(not to scale)'),
        Text('Point N lies on the line joining the centres of the Earth and the Moon. At point N, the '
             'resultant gravitational field strength due to the Earth and the Moon is zero.'),
        Sub('i', [
            Text('Show that the distance of point N from the centre of the Earth is 0.90<i>D</i>.'),
            Space(7),
            Mark(2),
        ]),
        Sub('ii', [
            Text('Fig. 2.2 shows axes for a graph of gravitational potential <i>φ</i> against distance <i>x</i> '
                 'from the centre of the Earth. The shaded regions represent the Earth and the Moon. Point S '
                 'shows the potential at the surface of the Earth.'),
            Fig(400, 164, fig_2_2, 'Fig. 2.2', note='(not to scale)'),
            Text('On Fig. 2.2, sketch the variation of <i>φ</i> with <i>x</i> from the surface of the Earth to '
                 'the surface of the Moon.'),
            Mark(2),
        ]),
        Sub('iii', [
            Text('A spacecraft travels from the Earth to the Moon. Its engines are switched off shortly after '
                 'launch.'),
            Text('Use your answer to (b)(ii) to explain why the spacecraft needs to be launched with only '
                 'enough kinetic energy to reach point N.'),
            Lines(2, 1),
        ]),
    ]),
    Part('c', [
        Text('A satellite of mass 450 kg is in a low circular orbit around the Earth. The upper atmosphere '
             'exerts a very small resistive force on the satellite, so that the radius of its orbit slowly '
             'decreases. Over several weeks, the radius decreases from 6.72 × 10<sup>6</sup> m to '
             '6.69 × 10<sup>6</sup> m. The orbit may be assumed to remain circular.'),
        Sub('i', [
            Text('Determine the change in the kinetic energy of the satellite. State whether the kinetic '
                 'energy increases or decreases.'),
            Space(8),
            Answer('change in kinetic energy', 'J', 2),
        ]),
        Sub('ii', [
            Text('A student states that, because the resistive force acts in the opposite direction to the '
                 'velocity of the satellite, the speed of the satellite must decrease.'),
            Text('Use your answer to (c)(i) to explain why the student is wrong.'),
            Lines(2, 1),
        ]),
    ]),
])

Q3 = Question([
    Text('Two rigid vessels A and B are connected by a narrow tube of negligible volume, as shown in '
         'Fig. 3.1.'),
    Fig(400, 172, fig_3_1, 'Fig. 3.1'),
    Text('Vessel A has a volume of 1.0 × 10<sup>–3</sup> m<sup>3</sup> and vessel B has a volume of '
         '2.0 × 10<sup>–3</sup> m<sup>3</sup>. The vessels contain an ideal gas. Initially, all of the gas is at '
         'a temperature of 27 °C and a pressure of 1.20 × 10<sup>5</sup> Pa.'),
    Text('Vessel A is then heated so that the gas in it reaches a temperature of 177 °C. Vessel B is kept in '
         'a water bath so that the gas in it stays at 27 °C. The gas is left until the pressure no longer '
         'changes.'),
    Part('a', [
        Text('A student states that the temperature of the gas in A has been increased by a factor of 6.6.'),
        Text('Explain why this statement is incorrect.'),
        Lines(2, 1),
    ]),
    Part('b', [
        Text('The student then predicts that the pressure of the gas in A increases by 50% and that the '
             'pressure of the gas in B does not change, because the temperature of the gas in B does not '
             'change.'),
        Text('Explain why <b>both</b> parts of this prediction are wrong.'),
        Lines(3, 2),
    ]),
    Part('c', [
        Sub('i', [
            Text('Show that the final pressure of the gas is 1.35 × 10<sup>5</sup> Pa.'),
            Space(8),
            Mark(2),
        ]),
        Sub('ii', [
            Text('Determine the number of gas molecules that move from A to B.'),
            Space(8),
            Answer('number', '', 2),
        ]),
    ]),
    Part('d', [
        Sub('i', [
            Text('The pressure of the gas in B has increased.'),
            Text('State, with a reason, whether the root-mean-square (r.m.s.) speed of the molecules in B has '
                 'changed.'),
            Lines(2, 1),
        ]),
        Sub('ii', [
            Text('Determine the ratio'),
            Eq(Frac('r.m.s. speed of the molecules in A', 'r.m.s. speed of the molecules in B'), '.'),
            Space(6),
            Answer('ratio', '', 2),
        ]),
    ]),
])

Q4 = Question([
    Part('a', [
        Text('A cylinder fitted with a light frictionless piston contains 0.150 kg of water at 100 °C, as shown '
             'in Fig. 4.1.'),
        Fig(270, 146, fig_4_1, 'Fig. 4.1'),
        Text('The atmosphere above the piston has a constant pressure of 1.01 × 10<sup>5</sup> Pa. The water is '
             'heated until all of it has turned into steam at 100 °C. The specific latent heat of vaporisation '
             'of water is 2.26 × 10<sup>6</sup> J kg<sup>–1</sup>. Data for water and steam at 100 °C are given '
             'in Table 4.1.'),
        Table([['', 'water', 'steam'],
               ['density / kg m<sup>–3</sup>', '958', '0.598']],
              [190, 100, 100], 'Table 4.1'),
        Sub('i', [
            Text('Calculate the work done <b>on</b> the water as it turns into steam.'),
            Space(8),
            Answer('work done on the water', 'J', 2),
        ]),
        Sub('ii', [
            Text('Use the first law of thermodynamics to determine the increase in the internal energy of the '
                 'water as it turns into steam.'),
            Space(7),
            Answer('increase in internal energy', 'J', 2),
        ]),
        Sub('iii', [
            Text('The temperature of the water does not change as it turns into steam.'),
            Text('Explain, in terms of its molecules, why the internal energy of the water increases.'),
            Lines(3, 2),
        ]),
    ]),
    Part('b', [
        Text('A fixed mass of an ideal gas is taken around the cycle A → B → C → A shown in Fig. 4.2.'),
        Fig(360, 305, fig_4_2, 'Fig. 4.2'),
        Sub('i', [
            Text('Determine the net work done <b>on</b> the gas during one cycle.'),
            Space(6),
            Answer('net work done on the gas', 'J', 2),
        ]),
        Sub('ii', [
            Text('Use the first law of thermodynamics to explain whether, during one cycle, there is a net '
                 'transfer of thermal energy to the gas or from the gas. State the magnitude of this net '
                 'transfer.'),
            Lines(3, 2),
        ]),
    ]),
])

Q5 = Question([
    Part('a', [
        Text('State what is meant by <i>simple harmonic motion</i>.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('A block of mass 0.25 kg hangs from the lower end of a vertical spring. The upper end of the '
             'spring is attached to a fixed support, as shown in Fig. 5.1.'),
        Fig(220, 124, fig_5_1, 'Fig. 5.1'),
        Text('The block is displaced vertically and released. It oscillates with simple harmonic motion. '
             'Fig. 5.2 shows part of the variation with time <i>t</i> of the displacement <i>x</i> of the block '
             'from its equilibrium position.'),
        Fig(416, 195, fig_5_2, 'Fig. 5.2'),
        Sub('i', [
            Text('Use Fig. 5.2 to determine the maximum speed of the block.'),
            Space(8),
            Answer('maximum speed', 'm s<sup>–1</sup>', 2),
        ]),
        Sub('ii', [
            Text('A student states that, when the displacement of the block is 2.0 cm, half of the total energy '
                 'of the oscillations is kinetic energy of the block.'),
            Text('By calculating the speed of the block when its displacement is 2.0 cm, determine the fraction '
                 'of the total energy of the oscillations that is kinetic energy at this displacement.'),
            Space(10),
            Answer('fraction', '', 3),
        ]),
    ]),
    Part('c', [
        Text('The block and spring are taken to the Moon, where the acceleration of free fall is '
             '1.62 m s<sup>–2</sup>. The block is again made to oscillate vertically. The spring obeys '
             'Hooke’s law.'),
        Text('A student predicts that the period of the oscillations will be longer on the Moon because the '
             'gravitational field strength is smaller.'),
        Text('By considering the resultant force on the block when it is displaced from its equilibrium '
             'position, explain why the student is wrong.'),
        Lines(4, 2),
    ]),
])

Q6 = Question([
    Part('a', [
        Text('Define <i>capacitance</i>.'),
        Lines(2, 1),
    ]),
    Part('b', [
        Text('An isolated metal sphere X of radius 0.10 m is supported on an insulating stand, as shown in '
             'Fig. 6.1.'),
        Fig(280, 160, fig_6_1, 'Fig. 6.1'),
        Text('Sphere X is charged so that its potential is 40 kV. The charge on the sphere may be considered to '
             'be a point charge at its centre.'),
        Text('Show that the capacitance of sphere X is 1.1 × 10<sup>–11</sup> F.'),
        Space(7),
        Mark(2),
    ]),
    Part('c', [
        Text('Sphere X is now connected by a long thin wire to an isolated metal sphere Y of radius 0.050 m. '
             'Sphere Y is initially uncharged. The arrangement is shown in Fig. 6.2.'),
        Fig(400, 104, fig_6_2, 'Fig. 6.2', note='(not to scale)'),
        Text('The spheres are far apart, so that the charge on each sphere has no effect on the potential of '
             'the other sphere. Charge flows along the wire until the spheres are at the same potential.'),
        Sub('i', [
            Text('Determine the final potential of the spheres.'),
            Space(8),
            Answer('potential', 'kV', 2),
        ]),
        Sub('ii', [
            Text('Determine the total energy dissipated as the charge flows along the wire.'),
            Space(8),
            Answer('energy', 'J', 2),
        ]),
        Sub('iii', [
            Text('Suggest what happens to the energy calculated in (c)(ii).'),
            Lines(2, 1),
        ]),
        Sub('iv', [
            Text('A student states that, because sphere X has a greater charge than sphere Y, the electric field '
                 'strength at the surface of X is greater than that at the surface of Y.'),
            Text('Determine the ratio'),
            Eq(Frac('electric field strength at the surface of Y', 'electric field strength at the surface of X'),
               '.'),
            Space(6),
            Answer('ratio', '', 2),
        ]),
    ]),
])

Q7 = Question([
    Part('a', [
        Text('State what is meant by the <i>root-mean-square</i> (r.m.s.) value of an alternating voltage.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('The potential difference (p.d.) <i>V</i> across a resistor of resistance 18 Ω varies with time '
             '<i>t</i> as shown in Fig. 7.1.'),
        Fig(436, 251, fig_7_1, 'Fig. 7.1'),
        Sub('i', [
            Text('Determine the mean power dissipated in the resistor.'),
            Space(8),
            Answer('mean power', 'W', 2),
        ]),
        Sub('ii', [
            Text('Hence determine the r.m.s. value of <i>V</i>.'),
            Space(5),
            Answer('r.m.s. value', 'V', 1),
        ]),
    ]),
    Part('c', [
        Text('A sinusoidal alternating supply of peak voltage 12 V and frequency 50 Hz is connected to a diode, '
             'a capacitor of capacitance 100 μF and a resistor of resistance 1.0 kΩ, as shown in Fig. 7.2.'),
        Fig(420, 148, fig_7_2, 'Fig. 7.2'),
        Text('Assume that there is no p.d. across the diode when it is conducting. The output p.d. '
             '<i>V</i><sub>OUT</sub> varies between a maximum value of 12 V and a minimum value. The difference '
             'between the maximum and minimum values is the ripple voltage.'),
        Sub('i', [
            Text('Between successive maximum values of <i>V</i><sub>OUT</sub>, the capacitor discharges through '
                 'the resistor for a time that is approximately equal to one period of the supply.'),
            Text('Determine the ripple voltage.'),
            Space(10),
            Answer('ripple voltage', 'V', 3),
        ]),
        Sub('ii', [
            Text('The circuit is changed so that it produces full-wave rectification. The supply, the capacitor '
                 'and the resistor are unchanged.'),
            Text('Explain why the ripple voltage is approximately halved.'),
            Lines(3, 2),
        ]),
    ]),
])

Q8 = Question([
    Text('Fig. 8.1 shows the main parts of a mass spectrometer. The apparatus is in a vacuum.'),
    Fig(420, 236, fig_8_1, 'Fig. 8.1'),
    Text('Positive ions pass through slit S<sub>1</sub> into a region between two parallel metal plates. In '
         'this region there is a uniform electric field of field strength <i>E</i> and a uniform magnetic field '
         'of flux density <i>B</i><sub>1</sub>. Ions that pass through slit S<sub>2</sub> enter a region where '
         'there is a uniform magnetic field of flux density <i>B</i><sub>2</sub> only. Both magnetic fields are '
         'directed into the page. The ions travel in a semicircle and arrive at a detector.'),
    Part('a', [
        Text('Explain why the only ions that pass through slit S<sub>2</sub> are those with speed '
             '<i>v</i> given by'),
        Eq('<i>v</i> = ', Frac('<i>E</i>', '<i>B</i><sub>1</sub>'), '.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('The plates are 15 mm apart and the p.d. between them is 1.5 kV. Flux density <i>B</i><sub>1</sub> '
             'is 0.50 T and flux density <i>B</i><sub>2</sub> is 0.40 T.'),
        Text('A beam of singly charged neon-20 ions (<sup>20</sup>Ne<sup>+</sup>) and singly charged neon-22 '
             'ions (<sup>22</sup>Ne<sup>+</sup>) enters through slit S<sub>1</sub>. The mass of each ion, in u, '
             'may be taken to be equal to its nucleon number.'),
        Sub('i', [
            Text('Determine the distance between the points at which the two types of ion arrive at the '
                 'detector.'),
            Space(9),
            Answer('distance', 'm', 3),
        ]),
        Sub('ii', [
            Text('Some of the neon-22 ions in the beam are doubly charged (<sup>22</sup>Ne<sup>2+</sup>).'),
            Text('Determine the distance from slit S<sub>2</sub> at which these ions arrive at the detector.'),
            Space(7),
            Answer('distance', 'm', 2),
        ]),
    ]),
    Part('c', [
        Text('A complete copper ring and an identical copper ring with a narrow slit cut in it are held '
             'horizontally above two identical vertical bar magnets, as shown in Fig. 8.2.'),
        Fig(380, 160, fig_8_2, 'Fig. 8.2'),
        Text('The rings are released at the same time and fall towards the magnets. The ring with the slit '
             'falls with acceleration <i>g</i>. The complete ring falls with an acceleration that is less than '
             '<i>g</i>. A student suggests that this is because no electromotive force (e.m.f.) is induced in '
             'the ring with the slit.'),
        Text('Explain why the student is wrong, and why the accelerations of the two rings are different.'),
        Lines(4, 3),
    ]),
])

Q9 = Question([
    Part('a', [
        Text('Electromagnetic radiation of frequency <i>f</i> is incident on the surface of metal X. Fig. 9.1 '
             'shows the variation with <i>f</i> of the maximum kinetic energy <i>E</i><sub>K max</sub> of the '
             'electrons emitted from the surface.'),
        Fig(472, 258, fig_9_1, 'Fig. 9.1'),
        Sub('i', [
            Text('Use Fig. 9.1 to determine a value for the Planck constant.'),
            Space(6),
            Answer('Planck constant', 'J s', 2),
        ]),
        Sub('ii', [
            Text('Determine the work function energy of metal X.'),
            Space(4),
            Answer('work function energy', 'J', 1),
        ]),
    ]),
    Part('b', [
        Text('Metal Y has a work function energy of 5.0 × 10<sup>–19</sup> J.'),
        Text('On Fig. 9.1, draw a line to show the variation with <i>f</i> of <i>E</i><sub>K max</sub> for '
             'metal Y.'),
        Mark(2),
    ]),
    Part('c', [
        Text('The intensity of the radiation incident on metal X is doubled. The frequency is unchanged.'),
        Text('State and explain the effect, if any, on the line for metal X in Fig. 9.1.'),
        Lines(2, 1),
    ]),
    Part('d', [
        Text('An electron and a proton are each accelerated from rest through the same potential difference. '
             'A student states that, because they gain the same kinetic energy, they have the same de Broglie '
             'wavelength.'),
        Text('Determine the ratio'),
        Eq(Frac('de Broglie wavelength of the electron', 'de Broglie wavelength of the proton'), '.'),
        Space(6),
        Answer('ratio', '', 2),
    ]),
    Part('e', [
        Text('A deuterium nucleus and a tritium nucleus fuse according to the equation'),
        Eq('<sup>2</sup><sub>1</sub>H  +  <sup>3</sup><sub>1</sub>H  →  <sup>4</sup><sub>2</sub>He  +  '
           '<sup>1</sup><sub>0</sub>n'),
        Text('Data for the binding energy per nucleon of the nuclei are given in Table 9.1.'),
        Table([['nucleus', 'binding energy per nucleon / MeV'],
               ['<sup>2</sup><sub>1</sub>H', '1.11'],
               ['<sup>3</sup><sub>1</sub>H', '2.83'],
               ['<sup>4</sup><sub>2</sub>He', '7.07']],
              [110, 230], 'Table 9.1'),
        Text('Determine the energy released, in MeV, in this reaction.'),
        Space(7),
        Answer('energy', 'MeV', 2),
    ]),
])

Q10 = Question([
    Part('a', [
        Text('Ultrasound is used to obtain diagnostic information about structures inside the body. '
             'Table 10.1 shows the specific acoustic impedance <i>Z</i> of some materials.'),
        Table([['material', '<i>Z</i> / kg m<sup>–2</sup> s<sup>–1</sup>'],
               ['air', '4.30 × 10<sup>2</sup>'],
               ['gel', '1.50 × 10<sup>6</sup>'],
               ['soft tissue', '1.63 × 10<sup>6</sup>'],
               ['bone', '7.80 × 10<sup>6</sup>']],
              [150, 170], 'Table 10.1', row_heights=[22] * 5),
        Text('Use data from Table 10.1 to explain why a gel is applied between the ultrasound transducer and '
             'the skin.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('A pulse of ultrasound passes through a layer of soft tissue of thickness 6.0 cm and is partly '
             'reflected at a boundary between the soft tissue and bone, as shown in Fig. 10.1.'),
        Fig(330, 158, fig_10_1, 'Fig. 10.1'),
        Text('The reflected pulse returns through the same soft tissue to the transducer. The linear '
             'attenuation coefficient of soft tissue for this ultrasound is 0.23 cm<sup>–1</sup>.'),
        Text('Calculate the intensity of the reflected pulse arriving at the transducer as a fraction of the '
             'intensity of the pulse entering the soft tissue.'),
        Space(8),
        Answer('fraction', '', 3),
    ]),
    Part('c', [
        Text('Fig. 10.2 shows the variation with wavelength <i>λ</i> of the intensity of the radiation emitted '
             'by two stars P and Q. Each curve has been scaled so that its maximum value is 1.0.'),
        Fig(360, 228, fig_10_2, 'Fig. 10.2'),
        Text('The radius of star Q is 45 times the radius of star P. A student states that star P must have the '
             'greater luminosity because it has the higher surface temperature.'),
        Text('Use Fig. 10.2 to determine the ratio of the luminosity of star Q to the luminosity of star P.'),
        Space(8),
        Answer('ratio', '', 3),
    ]),
    Part('d', [
        Text('A spectral line of hydrogen has a wavelength of 656.3 nm when measured in a laboratory. In the '
             'light from a distant galaxy, the same line has a wavelength of 678.9 nm. The galaxy is a distance '
             'of 4.6 × 10<sup>24</sup> m from the Earth.'),
        Sub('i', [
            Text('Assume that the galaxy has moved away from the Earth at a constant speed since the Big Bang.'),
            Text('Estimate the age of the universe, in years.'),
            Space(7),
            Answer('age', 'years', 2),
        ]),
        Sub('ii', [
            Text('A second galaxy is twice as far from the Earth. Explain, with reference to Hubble’s law, why '
                 'it gives the same estimate for the age of the universe.'),
            Lines(2, 1),
        ]),
    ]),
])

# ================================================================== mark scheme

MS = [
    # ---------------------------------------------------------------- Q1
    MSRow('1(a)', [
        ('direction of motion (and so velocity) changes continuously, so velocity changes '
         '<b>or</b> velocity is a vector and its direction changes', 'B1'),
    ]),
    MSRow('1(b)', [
        ('horizontal component of tension provides the centripetal force: '
         '<i>T</i> sin <i>θ</i> = <i>mω</i><sup>2</sup><i>r</i>', 'M1'),
        ('<i>r</i> = <i>L</i> sin <i>θ</i> so <i>T</i> sin <i>θ</i> = <i>mω</i><sup>2</sup><i>L</i> sin <i>θ</i>, '
         'leading to <i>T</i> = <i>mω</i><sup>2</sup><i>L</i>', 'A1'),
    ]),
    MSRow('1(c)', [
        ('12 = 0.20 × <i>ω</i><sup>2</sup> × 0.80', 'C1'),
        ('<i>ω</i> = 8.7 rad s<sup>–1</sup>', 'A1'),
    ], note='The angle <i>θ</i> is not needed: <i>T</i> = <i>mω</i><sup>2</sup><i>L</i> does not depend on '
            '<i>θ</i>.'),
    MSRow('1(d)', [
        ('horizontal line at cos <i>θ</i> = 1.0 from <i>ω</i> = 0 to <i>ω</i> = 3.5 rad s<sup>–1</sup> '
         '(string vertical for <i>ω</i> ≤ √(<i>g</i> / <i>L</i>) = 3.5 rad s<sup>–1</sup>)', 'B1'),
        ('for <i>ω</i> &gt; 3.5 rad s<sup>–1</sup>: curve decreasing from cos <i>θ</i> = 1.0 with decreasing '
         'magnitude of gradient (cos <i>θ</i> = <i>mg</i> / <i>T</i> = <i>g</i> / <i>ω</i><sup>2</sup><i>L</i>)',
         'B1'),
        ('curve passes through (5.0, 0.49) and (8.0, 0.19), each ± half a small square', 'B1'),
    ], note='A line that goes above cos <i>θ</i> = 1.0 (e.g. through (3.0, 1.36)) cannot score the first '
            'mark: cos <i>θ</i> cannot exceed 1, so for <i>ω</i> &lt; 3.5 rad s<sup>–1</sup> the bob does '
            'not move in a horizontal circle.'),
    MSRow('1(e)', [
        ('no change to the values of cos <i>θ</i>, because cos <i>θ</i> = <i>g</i> / <i>ω</i><sup>2</sup><i>L</i> '
         'does not depend on <i>m</i>', 'B1'),
        ('<i>T</i> doubles, so the string breaks at <i>ω</i> = √(12 / (0.40 × 0.80)) = 6.1 rad s<sup>–1</sup> '
         'and the line now ends at 6.1 rad s<sup>–1</sup>', 'B1'),
    ]),
    # ---------------------------------------------------------------- Q2
    MSRow('2(a)', [
        ('work done per unit mass', 'B1'),
        ('(work done) in bringing a small (test) mass from infinity (to the point)', 'B1'),
    ]),
    MSRow('2(b)(i)', [
        ('<i>GM</i><sub>E</sub> / <i>x</i><sup>2</sup> = <i>GM</i><sub>M</sub> / (<i>D</i> – <i>x</i>)<sup>2</sup>',
         'M1'),
        ('(<i>D</i> – <i>x</i>) / <i>x</i> = √(7.35 × 10<sup>22</sup> / 5.97 × 10<sup>24</sup>) = 0.111, '
         'leading to <i>x</i> = <i>D</i> / 1.111 = 0.90<i>D</i>', 'A1'),
    ]),
    MSRow('2(b)(ii)', [
        ('curve starting at S, negative throughout, increasing to a maximum (zero gradient) at '
         '<i>x</i> = 0.90<i>D</i>', 'B1'),
        ('curve then decreases to the surface of the Moon, ending at a potential much less negative than at S',
         'B1'),
    ]),
    MSRow('2(b)(iii)', [
        ('beyond N the potential decreases towards the Moon <b>or</b> beyond N the resultant force is towards the '
         'Moon, so the spacecraft accelerates (gains kinetic energy) towards the Moon', 'B1'),
    ]),
    MSRow('2(c)(i)', [
        ('<i>GMm</i> / <i>r</i><sup>2</sup> = <i>mv</i><sup>2</sup> / <i>r</i> so <i>E</i><sub>K</sub> = '
         '<i>GMm</i> / 2<i>r</i>', 'C1'),
        ('Δ<i>E</i><sub>K</sub> = ½ × 6.67 × 10<sup>–11</sup> × 5.97 × 10<sup>24</sup> × 450 × '
         '(1 / 6.69 × 10<sup>6</sup> – 1 / 6.72 × 10<sup>6</sup>)<br/>'
         '= 6.0 × 10<sup>7</sup> J, an increase', 'A1'),
    ]),
    MSRow('2(c)(ii)', [
        ('kinetic energy increases so speed increases: the loss of gravitational potential energy '
         '(1.2 × 10<sup>8</sup> J) is twice the gain in kinetic energy, the other half being the work done '
         'against the resistive force', 'B1'),
    ]),
    # ---------------------------------------------------------------- Q3
    MSRow('3(a)', [
        ('ratios of temperature need thermodynamic temperatures (the zero of the Celsius scale is not absolute '
         'zero): factor is 450 K / 300 K = 1.5', 'B1'),
    ]),
    MSRow('3(b)', [
        ('the vessels are connected so (when the gas settles) the pressure is the same in A and B', 'B1'),
        ('gas (molecules) moves from A to B, so the pressure in A rises by less than 50% and the pressure in B '
         'increases', 'B1'),
    ]),
    MSRow('3(c)(i)', [
        ('amount of gas is constant: <i>p</i><sub>0</sub>(<i>V</i><sub>A</sub> + <i>V</i><sub>B</sub>) / '
         '<i>T</i><sub>0</sub> = <i>p</i>(<i>V</i><sub>A</sub> / <i>T</i><sub>A</sub> + <i>V</i><sub>B</sub> / '
         '<i>T</i><sub>B</sub>)', 'M1'),
        ('1.20 × 10<sup>5</sup> × 3.0 × 10<sup>–3</sup> / 300 = <i>p</i> × (1.0 × 10<sup>–3</sup> / 450 + '
         '2.0 × 10<sup>–3</sup> / 300)<br/>leading to <i>p</i> = 1.35 × 10<sup>5</sup> Pa', 'A1'),
    ]),
    MSRow('3(c)(ii)', [
        ('<i>pV</i> = <i>NkT</i>: in A initially <i>N</i> = 1.20 × 10<sup>5</sup> × 1.0 × 10<sup>–3</sup> / '
         '(1.38 × 10<sup>–23</sup> × 300) = 2.90 × 10<sup>22</sup><br/>and finally <i>N</i> = '
         '1.35 × 10<sup>5</sup> × 1.0 × 10<sup>–3</sup> / (1.38 × 10<sup>–23</sup> × 450) = '
         '2.17 × 10<sup>22</sup>', 'C1'),
        ('number = 7.2 × 10<sup>21</sup>', 'A1'),
    ], note='allow: fraction of the molecules in A falls from 1/3 to 1/4 of the total of '
            '8.70 × 10<sup>22</sup>'),
    MSRow('3(d)(i)', [
        ('unchanged, because r.m.s. speed depends only on (thermodynamic) temperature '
         '(½<i>m</i>⟨<i>c</i><sup>2</sup>⟩ = 3/2 <i>kT</i>); the pressure rises because there are more molecules '
         'in B', 'B1'),
    ]),
    MSRow('3(d)(ii)', [
        ('r.m.s. speed ∝ √<i>T</i>', 'C1'),
        ('ratio = √(450 / 300) = 1.2', 'A1'),
    ], note='Use of Celsius temperatures, √(177 / 27) = 2.6, scores 0.'),
    # ---------------------------------------------------------------- Q4
    MSRow('4(a)(i)', [
        ('Δ<i>V</i> = 0.150 / 0.598 – 0.150 / 958 (= 0.251 m<sup>3</sup>) and <i>W</i> = –<i>p</i>Δ<i>V</i>',
         'C1'),
        ('<i>W</i> = –1.01 × 10<sup>5</sup> × 0.251 = –2.5 × 10<sup>4</sup> J', 'A1'),
    ], note='The negative sign is needed for A1: the steam expands and does work on the atmosphere.'),
    MSRow('4(a)(ii)', [
        ('<i>q</i> = <i>mL</i> = 0.150 × 2.26 × 10<sup>6</sup> = 3.39 × 10<sup>5</sup> J', 'C1'),
        ('Δ<i>U</i> = <i>q</i> + <i>W</i> = 3.39 × 10<sup>5</sup> – 2.5 × 10<sup>4</sup> = 3.1 × 10<sup>5</sup> J',
         'A1'),
    ], note='ecf from (a)(i). 3.6 × 10<sup>5</sup> J (adding the work done) scores C1 only.'),
    MSRow('4(a)(iii)', [
        ('temperature is constant so the (mean) kinetic energy of the molecules does not change', 'B1'),
        ('(intermolecular) potential energy of the molecules increases as they move apart / bonds are broken',
         'B1'),
    ]),
    MSRow('4(b)(i)', [
        ('work done = area enclosed by the cycle = ½ × 3.0 × 10<sup>–3</sup> × 3.0 × 10<sup>5</sup>', 'C1'),
        ('= (+)450 J', 'A1'),
    ], note='The work done on the gas is positive because the compression (B → C) happens at a higher '
            'pressure than the expansion (A → B). –450 J scores C1 only.'),
    MSRow('4(b)(ii)', [
        ('gas returns to its original state (temperature) so Δ<i>U</i> = 0 for one cycle', 'B1'),
        ('<i>q</i> = –<i>W</i> = –450 J, so there is a net transfer of 450 J (of thermal energy) from the gas',
         'B1'),
    ]),
    # ---------------------------------------------------------------- Q5
    MSRow('5(a)', [
        ('acceleration (directly) proportional to displacement (from a fixed point)', 'B1'),
        ('acceleration in the opposite direction to displacement <b>or</b> acceleration (always) directed '
         'towards the fixed point', 'B1'),
    ]),
    MSRow('5(b)(i)', [
        ('<i>ω</i> = 2π / 0.80 (= 7.85 rad s<sup>–1</sup>)', 'C1'),
        ('<i>v</i><sub>0</sub> = <i>ωx</i><sub>0</sub> = 7.85 × 0.040 = 0.31 m s<sup>–1</sup>', 'A1'),
    ]),
    MSRow('5(b)(ii)', [
        ('<i>v</i> = <i>ω</i>√(<i>x</i><sub>0</sub><sup>2</sup> – <i>x</i><sup>2</sup>) = '
         '7.85 × √(0.040<sup>2</sup> – 0.020<sup>2</sup>)', 'C1'),
        ('<i>v</i> = 0.27 m s<sup>–1</sup>', 'C1'),
        ('fraction = (0.272 / 0.314)<sup>2</sup> = 0.75', 'A1'),
    ], note='allow <i>E</i><sub>K</sub> / <i>E</i> = (<i>x</i><sub>0</sub><sup>2</sup> – <i>x</i><sup>2</sup>) / '
            '<i>x</i><sub>0</sub><sup>2</sup> = 3/4. An answer of 0.5 scores 0.'),
    MSRow('5(c)', [
        ('at equilibrium the tension in the spring balances the weight, so for a displacement <i>x</i> from '
         'equilibrium the resultant force is –<i>kx</i>, which does not depend on <i>g</i>', 'B1'),
        ('<i>a</i> = –(<i>k</i> / <i>m</i>)<i>x</i>, so <i>ω</i><sup>2</sup> = <i>k</i> / <i>m</i> and the '
         'period is unchanged (only the equilibrium extension changes)', 'B1'),
    ]),
    # ---------------------------------------------------------------- Q6
    MSRow('6(a)', [
        ('charge / potential', 'B1'),
    ], note='allow charge per unit potential'),
    MSRow('6(b)', [
        ('<i>V</i> = <i>Q</i> / 4π<i>ε</i><sub>0</sub><i>r</i> and <i>C</i> = <i>Q</i> / <i>V</i> leading to '
         '<i>C</i> = 4π<i>ε</i><sub>0</sub><i>r</i>', 'M1'),
        ('<i>C</i> = 0.10 / 8.99 × 10<sup>9</sup> = 1.1 × 10<sup>–11</sup> F', 'A1'),
    ]),
    MSRow('6(c)(i)', [
        ('charge is conserved: <i>Q</i> = 1.11 × 10<sup>–11</sup> × 40 × 10<sup>3</sup> = 4.4 × 10<sup>–7</sup> C '
         'and <i>C</i><sub>Y</sub> = 0.050 / 8.99 × 10<sup>9</sup> = 5.6 × 10<sup>–12</sup> F', 'C1'),
        ('<i>V</i> = <i>Q</i> / (<i>C</i><sub>X</sub> + <i>C</i><sub>Y</sub>) = 4.4 × 10<sup>–7</sup> / '
         '1.67 × 10<sup>–11</sup> = 27 kV', 'A1'),
    ], note='allow <i>V</i> = 40 × 0.10 / 0.15 = 27 kV'),
    MSRow('6(c)(ii)', [
        ('energy = ½<i>QV</i> <b>or</b> ½<i>CV</i><sup>2</sup>: initially 8.9 × 10<sup>–3</sup> J, finally '
         '5.9 × 10<sup>–3</sup> J', 'C1'),
        ('energy dissipated = 3.0 × 10<sup>–3</sup> J', 'A1'),
    ], note='One third of the initial energy is dissipated, whatever the resistance of the wire.'),
    MSRow('6(c)(iii)', [
        ('converted to thermal energy in the wire (by the current in its resistance)', 'B1'),
    ], note='allow emitted as electromagnetic radiation'),
    MSRow('6(c)(iv)', [
        ('<i>E</i> = <i>Q</i> / 4π<i>ε</i><sub>0</sub><i>r</i><sup>2</sup> = <i>V</i> / <i>r</i>, with <i>V</i> '
         'the same for both spheres', 'C1'),
        ('ratio = 0.10 / 0.050 = 2.0', 'A1'),
    ], note='Y has half the charge of X but a quarter of the surface area, so the field at the surface of the '
            'smaller sphere is the greater.'),
    # ---------------------------------------------------------------- Q7
    MSRow('7(a)', [
        ('the constant / direct voltage', 'M1'),
        ('that produces the same (mean) power in a resistor (as the alternating voltage)', 'A1'),
    ]),
    MSRow('7(b)(i)', [
        ('<i>P</i> = <i>V</i><sup>2</sup> / <i>R</i>: 12<sup>2</sup> / 18 = 8.0 W and 6.0<sup>2</sup> / 18 = '
         '2.0 W', 'C1'),
        ('mean power = (8.0 + 2.0) / 2 = 5.0 W', 'A1'),
    ], note='Use of the mean p.d. (3.0 V) or of 12 / √2 scores 0.'),
    MSRow('7(b)(ii)', [
        ('<i>V</i><sub>r.m.s.</sub> = √(5.0 × 18) = 9.5 V', 'A1'),
    ], note='allow √90 V; ecf from (b)(i)'),
    MSRow('7(c)(i)', [
        ('<i>τ</i> = <i>RC</i> = 1.0 × 10<sup>3</sup> × 100 × 10<sup>–6</sup> = 0.10 s and <i>t</i> = 1 / 50 = '
         '0.020 s', 'C1'),
        ('<i>V</i> = 12 e<sup>–0.020 / 0.10</sup> = 9.8 V', 'C1'),
        ('ripple voltage = 12 – 9.8 = 2.2 V', 'A1'),
    ]),
    MSRow('7(c)(ii)', [
        ('capacitor now discharges for (about) half the time (0.010 s) between maximum values', 'B1'),
        ('discharge time is much less than <i>RC</i>, so the decrease in p.d. is approximately proportional to '
         'time', 'B1'),
    ], note='Exact values: 1.14 V for full-wave and 2.18 V for half-wave rectification.'),
    # ---------------------------------------------------------------- Q8
    MSRow('8(a)', [
        ('electric force (<i>qE</i>) and magnetic force (<i>B</i><sub>1</sub><i>qv</i>) act in opposite '
         'directions', 'B1'),
        ('no deflection only when the forces are equal: <i>qE</i> = <i>B</i><sub>1</sub><i>qv</i>, so '
         '<i>v</i> = <i>E</i> / <i>B</i><sub>1</sub>; ions with other speeds are deflected (and hit the '
         'barrier)', 'B1'),
    ]),
    MSRow('8(b)(i)', [
        ('<i>v</i> = <i>E</i> / <i>B</i><sub>1</sub> = (1.5 × 10<sup>3</sup> / 0.015) / 0.50 = '
         '2.0 × 10<sup>5</sup> m s<sup>–1</sup>', 'C1'),
        ('<i>r</i> = <i>mv</i> / <i>Bq</i> = 20 × 1.66 × 10<sup>–27</sup> × 2.0 × 10<sup>5</sup> / '
         '(0.40 × 1.60 × 10<sup>–19</sup>) = 0.104 m (and 0.114 m for neon-22)', 'C1'),
        ('distance = 2 × (0.1141 – 0.1038) = 0.021 m', 'A1'),
    ], note='The ions travel in semicircles, so the separation is the difference in diameters. '
            '0.010 m scores C1 C1 only.'),
    MSRow('8(b)(ii)', [
        ('speed selected is unchanged (2.0 × 10<sup>5</sup> m s<sup>–1</sup>) because both forces double / '
         '<i>v</i> = <i>E</i> / <i>B</i><sub>1</sub> does not depend on charge', 'C1'),
        ('radius = 0.114 / 2 = 0.057 m, so distance = 0.11 m', 'A1'),
    ]),
    MSRow('8(c)', [
        ('(magnetic) flux linking each ring changes as it falls, so (by Faraday’s law) an e.m.f. is induced in '
         '<b>both</b> rings', 'B1'),
        ('the complete ring is a closed circuit so there is an induced current in it; there is no current in '
         'the ring with the slit', 'B1'),
        ('the current produces a (magnetic) force that opposes the motion (Lenz’s law), so the acceleration is '
         'less than <i>g</i>; no current means no force on the ring with the slit', 'B1'),
    ]),
    # ---------------------------------------------------------------- Q9
    MSRow('9(a)(i)', [
        ('Planck constant = gradient of the line', 'C1'),
        ('e.g. 6.0 × 10<sup>–19</sup> / ((14.0 – 5.0) × 10<sup>14</sup>) = 6.7 × 10<sup>–34</sup> J s', 'A1'),
    ], note='allow 6.5 × 10<sup>–34</sup> to 6.8 × 10<sup>–34</sup> J s'),
    MSRow('9(a)(ii)', [
        ('work function energy = <i>hf</i><sub>0</sub> = 6.7 × 10<sup>–34</sup> × 5.0 × 10<sup>14</sup> = '
         '3.3 × 10<sup>–19</sup> J', 'A1'),
    ], note='allow from the intercept of the extrapolated line on the <i>E</i><sub>K max</sub> axis'),
    MSRow('9(b)', [
        ('straight line parallel to the line for metal X', 'B1'),
        ('line meets the <i>f</i>-axis at 7.5 × 10<sup>14</sup> Hz', 'B1'),
    ], note='threshold frequency = 5.0 × 10<sup>–19</sup> / 6.7 × 10<sup>–34</sup>; allow 7.4 to 7.6 × '
            '10<sup>14</sup> Hz'),
    MSRow('9(c)', [
        ('no change, because <i>E</i><sub>K max</sub> depends only on the photon energy (frequency); more '
         'photons per second only increase the rate of emission of electrons', 'B1'),
    ]),
    MSRow('9(d)', [
        ('<i>λ</i> = <i>h</i> / <i>p</i> and <i>p</i> = √(2<i>mE</i><sub>K</sub>), with the same '
         '<i>E</i><sub>K</sub>', 'C1'),
        ('ratio = √(<i>m</i><sub>p</sub> / <i>m</i><sub>e</sub>) = √(1.67 × 10<sup>–27</sup> / '
         '9.11 × 10<sup>–31</sup>) = 43', 'A1'),
    ]),
    MSRow('9(e)', [
        ('binding energies: <sup>2</sup>H 2 × 1.11 = 2.22 MeV, <sup>3</sup>H 3 × 2.83 = 8.49 MeV, '
         '<sup>4</sup>He 4 × 7.07 = 28.28 MeV', 'C1'),
        ('energy released = 28.28 – (2.22 + 8.49) = 17.6 MeV', 'A1'),
    ], note='The neutron has no binding energy. 7.07 – 1.11 – 2.83 = 3.13 MeV scores 0.'),
    # ---------------------------------------------------------------- Q10
    MSRow('10(a)', [
        ('<i>Z</i> of air is very different from <i>Z</i> of skin / soft tissue, so (almost) all of the '
         'ultrasound would be reflected at an air–skin boundary', 'B1'),
        ('<i>Z</i> of gel is close to <i>Z</i> of soft tissue, so (almost) all of the ultrasound is transmitted '
         'into the body', 'B1'),
    ]),
    MSRow('10(b)', [
        ('<i>I</i><sub>R</sub> / <i>I</i><sub>0</sub> = (7.80 – 1.63)<sup>2</sup> / (7.80 + 1.63)<sup>2</sup> = '
         '0.43', 'C1'),
        ('total path in tissue = 12 cm: e<sup>–0.23 × 12</sup> = 0.063', 'C1'),
        ('ratio = 0.43 × 0.063 = 0.027', 'A1'),
    ], note='Use of a path of 6.0 cm (giving 0.11) scores max 2.'),
    MSRow('10(c)', [
        ('<i>λ</i><sub>max</sub> = 320 nm for P and 960 nm for Q; <i>λ</i><sub>max</sub><i>T</i> = constant, so '
         '<i>T</i><sub>P</sub> / <i>T</i><sub>Q</sub> = 3.0', 'C1'),
        ('<i>L</i> = 4π<i>σr</i><sup>2</sup><i>T</i><sup>4</sup> so <i>L</i><sub>Q</sub> / <i>L</i><sub>P</sub> = '
         '45<sup>2</sup> × (1 / 3.0)<sup>4</sup>', 'C1'),
        ('ratio = 25', 'A1'),
    ], note='The cooler star Q is 25 times as luminous as P because of its much larger radius.'),
    MSRow('10(d)(i)', [
        ('<i>v</i> = <i>c</i>Δ<i>λ</i> / <i>λ</i> = 3.00 × 10<sup>8</sup> × (678.9 – 656.3) / 656.3 = '
         '1.03 × 10<sup>7</sup> m s<sup>–1</sup>', 'C1'),
        ('<i>t</i> = <i>d</i> / <i>v</i> = 4.6 × 10<sup>24</sup> / 1.03 × 10<sup>7</sup> = '
         '4.5 × 10<sup>17</sup> s = 1.4 × 10<sup>10</sup> years', 'A1'),
    ]),
    MSRow('10(d)(ii)', [
        ('<i>v</i> = <i>H</i><sub>0</sub><i>d</i> so <i>v</i> ∝ <i>d</i>: twice the distance means twice the '
         'speed, so <i>t</i> = <i>d</i> / <i>v</i> = 1 / <i>H</i><sub>0</sub> is the same', 'B1'),
    ]),
]

def _tie_refs(blocks):
    """Keep 'Fig. 1.1' and 'Table 4.1' together on one line."""
    for b in blocks:
        if isinstance(b, (Part, Sub)):
            _tie_refs(b.blocks)
        elif isinstance(b, Text):
            b.rich = re.sub(r'(Fig\.|Table) (\d)', '\\1\u00a0\\2', b.rich)


for _q in (Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10):
    _tie_refs(_q.blocks)

PAPER = Paper(number=1, questions=[Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10], mark_scheme=MS)
