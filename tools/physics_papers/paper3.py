"""9702 Paper 4 practice paper 3.

Q1  gravitational fields, circular orbits      Q6  capacitance
Q2  temperature, ideal gases                    Q7  electromagnetic induction, Hall effect
Q3  thermodynamics                              Q8  alternating currents, rectification
Q4  oscillations                                Q9  quantum physics, nuclear physics
Q5  electric fields                             Q10 medical physics, astronomy

Every numerical answer in the mark scheme was checked with a Python script.
"""
import math
import re

from engine import *
from figs import *
from richtext import Box, draw_runs, runs, runs_width


# ================================================================== helpers

def _sq(n):
    """Length of n minor grid squares."""
    return n * MINOR


def _lb_axes(c, g, xt, yt, xlabel, ylabel):
    """Axes along the left and bottom edges of graph g (for ranges that
    include negative values, where the Graph default would put the axis
    inside the grid)."""
    x0, y0 = g.x, g.y
    line(c, x0, y0, x0 + g.w, y0, w=1.0)
    line(c, x0, y0, x0, y0 + g.h, w=1.0)
    for v, s in xt:
        px = g.P(v, g.yr[0])[0]
        line(c, px, y0, px, y0 - 3)
        label(c, px, y0 - 13, s, anchor='c')
    ytw = 0
    for v, s in yt:
        py = g.P(g.xr[0], v)[1]
        line(c, x0, py, x0 - 3, py)
        label(c, x0 - 5, py - 3.9, s, anchor='r')
        ytw = max(ytw, text_width(s))
    label(c, x0 + g.w, y0 - 27, xlabel, anchor='r')
    label(c, x0 - ytw - 10, y0 + g.h * 0.62, ylabel, anchor='r')


def _ticks(lo, hi, step, fmt=lambda v: ('%g' % v).replace('-', '–')):
    out, v = [], lo
    while v <= hi + 1e-9:
        out.append((v, fmt(round(v, 6))))
        v += step
    return out


def _ellipse(cx, cy, a, b, ang=0.0, t0=0.0, t1=2 * math.pi, n=120):
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    for k in range(n + 1):
        t = t0 + (t1 - t0) * k / n
        x, y = a * math.cos(t), b * math.sin(t)
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def _rot(c, x1, y1, x2, y2, fn):
    """Draw a horizontal circuit symbol fn(c, 0, 0, L, 0) along any direction."""
    L = math.hypot(x2 - x1, y2 - y1)
    c.saveState()
    c.translate(x1, y1)
    c.rotate(math.degrees(math.atan2(y2 - y1, x2 - x1)))
    fn(c, 0, 0, L, 0)
    c.restoreState()


def _earth(c, x, y):
    """Earth symbol hanging below (x, y)."""
    line(c, x, y, x, y - 10)
    for k, hw in enumerate((9, 6, 3)):
        line(c, x - hw, y - 10 - 3 * k, x + hw, y - 10 - 3 * k, w=1.0)


def _nuc(A, Z, sym):
    """Nuclide symbol with nucleon number above proton number (math box)."""
    ra, rz, rs = runs(str(A), 8.0), runs(str(Z), 8.0), runs(sym, 11.0)
    wa, wz, ws = runs_width(ra), runs_width(rz), runs_width(rs)
    wl = max(wa, wz)

    def draw(c, x, y):
        draw_runs(c, x + wl - wa, y + 5.2, ra)
        draw_runs(c, x + wl - wz, y - 3.2, rz)
        draw_runs(c, x + wl + 0.8, y, rs)
    return Box(wl + 0.8 + ws, 11.2, 5.0, draw)


# ================================================================== Question 1

def fig_1_1(c):
    cx, cy, R = 150, 80, 64
    polyline(c, _ellipse(cx, cy, R, R), w=0.75, dash=[4, 3])
    circle(c, cx, cy, 24, fill=0.85)
    ang = math.radians(38)
    sx, sy = cx + R * math.cos(ang), cy + R * math.sin(ang)
    line(c, cx, cy, sx, sy)
    dot(c, cx, cy, 1.6)
    dot(c, sx, sy, 4.5)
    mx, my = cx + 0.62 * R * math.cos(ang), cy + 0.62 * R * math.sin(ang)
    text(c, mx - 4, my + 5, '<i>r</i>', anchor='r')
    # direction of motion
    a0, a1 = math.radians(95), math.radians(118)
    arrow(c, cx + R * math.cos(a0), cy + R * math.sin(a0), cx + R * math.cos(a1), cy + R * math.sin(a1))
    text(c, sx + 9, sy + 4, 'satellite, mass <i>m</i>')
    line(c, cx - 22, cy - 8, cx - R - 10, cy - 22, w=0.5)
    text(c, cx - R - 13, cy - 26, 'planet, mass <i>M</i>', anchor='r')
    text(c, cx + R + 6, cy - 50, 'orbit')
    t = math.radians(-25)
    line(c, cx + R + 4, cy - 44, cx + R * math.cos(t) + 2, cy + R * math.sin(t), w=0.5)


def fig_1_2(c):
    cx, cy, Re = 190, 75, 28
    ang = math.radians(30)
    a, b = 140, 17
    # plane of the equator
    line(c, 15, cy, 365, cy, dash=[5, 3])
    text(c, 365, cy - 15, 'plane of equator', anchor='r')
    # whole orbit, then the Earth over its back half, then the front half again
    polyline(c, _ellipse(cx, cy, a, b, ang), w=0.9)
    circle(c, cx, cy, Re, w=0.9, fill=1)
    line(c, cx - Re, cy, cx + Re, cy, w=0.6)
    polyline(c, _ellipse(cx, cy, a, b, ang, math.pi, 2 * math.pi), w=0.9)
    line(c, cx, cy - Re - 14, cx, cy + Re + 14)
    text(c, cx, cy + Re + 18, 'N', anchor='c')
    text(c, cx, cy - Re - 26, 'S', anchor='c')
    text(c, cx - 3, cy + 7, 'Earth', size=8, anchor='r')
    # plane of the orbit, and the angle between it and the plane of the equator
    line(c, cx, cy, cx + (a + 10) * math.cos(ang), cy + (a + 10) * math.sin(ang), w=0.5, dash=[5, 3])
    pts = [(cx + 105 * math.cos(t), cy + 105 * math.sin(t)) for t in [ang * k / 30 for k in range(31)]]
    polyline(c, pts, w=0.6)
    text(c, cx + 112 * math.cos(ang / 2), cy + 112 * math.sin(ang / 2) - 4, '30°')
    # satellite X on the front of the orbit
    t = 2.75
    xs, ys = (cx + a * math.cos(t) * math.cos(ang) - b * math.sin(t) * math.sin(ang),
              cy + a * math.cos(t) * math.sin(ang) + b * math.sin(t) * math.cos(ang))
    dot(c, xs, ys, 4)
    text(c, xs - 5, ys + 5, 'X', anchor='r')
    # direction of motion on the front half
    p = _ellipse(cx, cy, a, b, ang, -1.75, -1.45, n=4)
    arrow(c, p[0][0], p[0][1], p[-1][0], p[-1][1])
    text(c, cx + 14, cy + 68, 'orbit of X', anchor='r')
    line(c, cx + 16, cy + 70, cx + 62, cy + 52, w=0.5)


Q1 = Question([
    Text('A satellite of mass <i>m</i> moves in a circular orbit of radius <i>r</i> about a planet of mass '
         '<i>M</i>, as shown in Fig. 1.1. The planet may be considered to be a point mass at its centre. The '
         'gravitational constant is <i>G</i>.'),
    Fig(340, 155, fig_1_1, 'Fig. 1.1', note='(not to scale)'),
    Part('a', [
        Text('Show that the period <i>T</i> of the orbit is given by'),
        Eq('<i>T</i><sup>2</sup> = ', Frac('4π<sup>2</sup>', '<i>GM</i>'), ' <i>r</i><sup>3</sup>.'),
        Space(7),
        Mark(2),
    ]),
    Part('b', [
        Text('The Earth has mass 5.98 × 10<sup>24</sup> kg and rotates once on its axis every 24.0 hours.'),
        Sub('i', [
            Text('Calculate the radius of a geostationary orbit about the Earth.'),
            Space(8),
            Answer('radius', 'm', 2),
        ]),
        Sub('ii', [
            Text('A satellite X moves in a circular orbit that has the radius calculated in (b)(i). X moves '
                 'around the Earth in the same direction as the Earth rotates. The plane of the orbit of X is at '
                 'an angle of 30° to the plane of the equator, as shown in Fig. 1.2.'),
            Fig(380, 150, fig_1_2, 'Fig. 1.2', note='(not to scale)'),
            Text('A student states that X is a geostationary satellite because its orbital period is 24.0 hours. '
                 'Explain why the student is wrong.'),
            Lines(3, 2),
        ]),
    ]),
    Part('c', [
        Text('A satellite of mass 1200 kg is moved from a circular orbit of radius 6.80 × 10<sup>6</sup> m about '
             'the Earth to a geostationary orbit.'),
        Sub('i', [
            Text('Determine the minimum energy that must be supplied to the satellite by its rocket engines.'),
            Space(10),
            Answer('energy', 'J', 3),
        ]),
        Sub('ii', [
            Text('The speed of the satellite in the geostationary orbit is less than its speed in the original '
                 'orbit. Explain how this is possible when energy has been supplied to the satellite.'),
            Lines(3, 2),
        ]),
    ]),
])

MS1 = [
    MSRow('1(a)', [
        ('gravitational force provides the centripetal force:<br/>'
         '<i>GMm</i> / <i>r</i><sup>2</sup> = <i>mrω</i><sup>2</sup> <b>or</b> '
         '<i>GMm</i> / <i>r</i><sup>2</sup> = <i>mv</i><sup>2</sup> / <i>r</i>', 'M1'),
        ('<i>ω</i> = 2π / <i>T</i> <b>or</b> <i>v</i> = 2π<i>r</i> / <i>T</i>, and algebra leading to '
         '<i>T</i><sup>2</sup> = (4π<sup>2</sup> / <i>GM</i>) <i>r</i><sup>3</sup>', 'A1'),
    ]),
    MSRow('1(b)(i)', [
        ('<i>T</i> = 24.0 × 3600 = 8.64 × 10<sup>4</sup> s and '
         '<i>r</i><sup>3</sup> = <i>GMT</i><sup>2</sup> / 4π<sup>2</sup>', 'C1'),
        ('<i>r</i><sup>3</sup> = 6.67 × 10<sup>–11</sup> × 5.98 × 10<sup>24</sup> × (8.64 × 10<sup>4</sup>)'
         '<sup>2</sup> / 4π<sup>2</sup><br/>'
         '<i>r</i> = 4.23 × 10<sup>7</sup> m', 'A1'),
    ]),
    MSRow('1(b)(ii)', [
        ('orbit of X is not in the plane of the equator / X is not always above the equator', 'B1'),
        ('X moves north and south (of the equator) relative to the Earth\'s surface, so it does not stay above '
         'the same point on the Earth\'s surface', 'B1'),
    ], note='a period of 24 hours is necessary but not sufficient: a geostationary orbit must also be equatorial '
            'and from west to east'),
    MSRow('1(c)(i)', [
        ('<i>mv</i><sup>2</sup> / <i>r</i> = <i>GMm</i> / <i>r</i><sup>2</sup> so '
         '<i>E</i><sub>K</sub> = <i>GMm</i> / 2<i>r</i><br/>'
         'and total energy = <i>E</i><sub>K</sub> + <i>E</i><sub>P</sub> = –<i>GMm</i> / 2<i>r</i>', 'C1'),
        ('energy supplied = increase in total energy = ½<i>GMm</i> (1 / <i>r</i><sub>1</sub> – 1 / '
         '<i>r</i><sub>2</sub>)<br/>'
         '= ½ × 6.67 × 10<sup>–11</sup> × 5.98 × 10<sup>24</sup> × 1200 × '
         '[1 / (6.80 × 10<sup>6</sup>) – 1 / (4.23 × 10<sup>7</sup>)]', 'C1'),
        ('= 2.95 × 10<sup>10</sup> J', 'A1'),
    ], note='the increase in gravitational potential energy alone (5.91 × 10<sup>10</sup> J) ignores the '
            'decrease in kinetic energy: max. 1 mark'),
    MSRow('1(c)(ii)', [
        ('<i>v</i><sup>2</sup> = <i>GM</i> / <i>r</i>, so speed and kinetic energy decrease as <i>r</i> '
         'increases', 'B1'),
        ('gravitational potential energy increases by twice the decrease in kinetic energy, so the total energy '
         'increases<br/><b>or</b><br/>energy supplied = gain in gravitational potential energy – loss in kinetic '
         'energy', 'B1'),
    ]),
]


# ================================================================== Question 2

def fig_2_1(c):
    # beaker of water
    polyline(c, [(40, 125), (40, 15), (180, 15), (180, 125)], w=1.0)
    line(c, 40, 105, 180, 105, w=0.6)
    for x in range(48, 176, 16):
        line(c, x, 108, x + 7, 108, w=0.4)
    # bulb and tube (drawn as a pair of lines)
    bx, by, br = 110, 55, 22
    circle(c, bx, by, br, w=1.0, fill=1)
    text(c, bx, by - 4, 'gas', anchor='c')
    for d in (-2.5, 2.5):
        line(c, bx + d, by + br - 0.4, bx + d, 150 + d, w=0.9)
        line(c, bx + d, 150 + d, 318 - d, 150 + d, w=0.9)
        line(c, 318 - d, 150 + d, 318 - d, 112, w=0.9)
    # pressure gauge
    gx, gy, gr = 318, 90, 22
    circle(c, gx, gy, gr, w=1.0, fill=1)
    for k in range(9):
        t = math.radians(210 - 30 * k)
        line(c, gx + 15 * math.cos(t), gy + 15 * math.sin(t), gx + 19 * math.cos(t), gy + 19 * math.sin(t), w=0.6)
    arrow(c, gx, gy, gx + 13 * math.cos(math.radians(55)), gy + 13 * math.sin(math.radians(55)), head=4)
    dot(c, gx, gy, 1.5)
    text(c, gx, gy - gr - 14, 'pressure gauge', anchor='c')
    text(c, 60, 85, 'water')
    text(c, 205, 52, 'bulb')
    line(c, 203, 55, bx + br + 1, 58, w=0.5)
    text(c, 205, 128, 'narrow tube')
    line(c, 225, 138, 225, 147, w=0.5)


def fig_2_2(c):
    g = Graph(c, 80, 32, _sq(40), _sq(40), xr=(-300, 100), yr=(0, 160), xmajor=50, ymajor=20,
              minor=5, axes=False)
    _lb_axes(c, g, _ticks(-300, 100, 100), _ticks(0, 160, 20), '<i>θ</i> / °C', '<i>p</i> / kPa')
    for th in (0, 20, 40, 60, 80, 100):
        g.mark(th, 55.0 * (th + 273.15) / 273.15)


Q2 = Question([
    Part('a', [
        Text('State <b>two</b> of the basic assumptions of the kinetic theory of gases.'),
        Lines(4, 2),
    ]),
    Part('b', [
        Text('A constant-volume gas thermometer is shown in Fig. 2.1. The bulb contains a fixed mass of a gas '
             'that may be assumed to be ideal.'),
        Fig(380, 150, fig_2_1, 'Fig. 2.1'),
        Text('The volume of the gas is kept constant. The bulb is placed in water at different Celsius '
             'temperatures <i>θ</i> and the pressure <i>p</i> of the gas is measured. The results are shown in '
             'Fig. 2.2.'),
        Fig(330, 264, fig_2_2, 'Fig. 2.2'),
        Sub('i', [
            Text('On Fig. 2.2, draw the best-fit line for the points and extend it to determine the Celsius '
                 'temperature at which the pressure of the gas would be zero.'),
            Space(2),
            Answer('temperature', '°C', 2),
        ]),
        Sub('ii', [
            Text('The bulb is emptied and then filled with twice the number of molecules of the same gas. The '
                 'volume of the bulb is unchanged.'),
            Text('On Fig. 2.2, draw a line to show the variation with <i>θ</i> of <i>p</i> for this gas for temperatures '
                 'from –273 °C to 100 °C.'),
            Mark(2),
        ]),
    ]),
    Part('c', [
        Text('A thermistor thermometer is calibrated by assuming that the resistance of the thermistor varies '
             'linearly with temperature between the ice point (0 °C) and the steam point (100 °C). The resistance '
             'of the thermistor is 32.0 kΩ at the ice point and 0.770 kΩ at the steam point.'),
        Text('The thermistor and the bulb of the gas thermometer in (b) are placed together in a liquid. The gas '
             'thermometer shows that the temperature of the liquid is 50 °C. The resistance of the thermistor is '
             '3.73 kΩ.'),
        Sub('i', [
            Text('Calculate the temperature of the liquid shown by the thermistor thermometer.'),
            Space(8),
            Answer('temperature', '°C', 2),
        ]),
        Sub('ii', [
            Text('Both thermometers read correctly at the ice point and at the steam point. Explain why they give '
                 'different readings for the temperature of the liquid, and state which reading is the '
                 'thermodynamic temperature of the liquid.'),
            Lines(3, 2),
        ]),
    ]),
])

MS2 = [
    MSRow('2(a)', [
        ('any two from:<br/>'
         '• large number of molecules in random motion<br/>'
         '• no intermolecular forces (except during collisions)<br/>'
         '• volume of molecules negligible compared with volume of container / gas<br/>'
         '• collisions (of molecules with each other and with walls) are elastic<br/>'
         '• time of collision negligible compared with time between collisions', 'B2'),
    ]),
    MSRow('2(b)(i)', [
        ('straight line through the points, extended to <i>p</i> = 0', 'B1'),
        ('temperature = –273 °C (allow –260 °C to –290 °C)', 'B1'),
    ]),
    MSRow('2(b)(ii)', [
        ('straight line with twice the pressure at each temperature: <i>p</i> = 110 kPa at 0 °C '
         '(and 150 kPa at 100 °C)', 'B1'),
        ('line meets <i>p</i> = 0 at the same temperature as the original line (–273 °C)', 'B1'),
    ], note='<i>p</i> is proportional to <i>NT</i> at constant <i>V</i>, so <i>p</i> = 0 at <i>T</i> = 0 K '
            'whatever the amount of gas'),
    MSRow('2(c)(i)', [
        ('temperature = (<i>R</i><sub>0</sub> – <i>R</i>) / (<i>R</i><sub>0</sub> – <i>R</i><sub>100</sub>) × '
         '100<br/>= (32.0 – 3.73) / (32.0 – 0.770) × 100', 'C1'),
        ('= 91 °C', 'A1'),
    ]),
    MSRow('2(c)(ii)', [
        ('resistance of the thermistor does not vary linearly with (thermodynamic) temperature, so the two '
         'scales agree only at the fixed points (where they were calibrated)', 'B1'),
        ('the gas thermometer reading (50 °C / 323 K) is the thermodynamic temperature, since <i>p</i> is '
         'proportional to <i>T</i> for an ideal gas at constant volume', 'B1'),
    ]),
]


# ================================================================== Question 3

def fig_3_1(c):
    g = Graph(c, 75, 38, _sq(35), _sq(35), xr=(0, 3.5), yr=(0, 3.5), xmajor=0.5, ymajor=0.5, minor=5,
              xlabel='<i>V</i> / 10<sup>–3</sup> m<sup>3</sup>', ylabel='<i>p</i> / 10<sup>5</sup> Pa',
              xticks=[(0, '0'), (1, '1.0'), (2, '2.0'), (3, '3.0')],
              yticks=[(0, '0'), (1, '1.0'), (2, '2.0'), (3, '3.0')])
    A, B, C = (3.0, 1.0), (1.0, 1.0), (1.0, 3.0)
    g.points([A, B, C, A], w=1.4)
    for (p, q) in ((A, B), (B, C), (C, A)):
        a, b = g.P(*p), g.P(*q)
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        dx, dy = (b[0] - a[0]), (b[1] - a[1])
        L = math.hypot(dx, dy)
        arrow(c, m[0] - 7 * dx / L, m[1] - 7 * dy / L, m[0] + 7 * dx / L, m[1] + 7 * dy / L, w=1.4, head=9)
    for p, s, dx, dy in ((A, 'A', 6, -14), (B, 'B', -14, -14), (C, 'C', -14, 4)):
        px, py = g.P(*p)
        label(c, px + dx, py + dy, s)
    g.finish()


def fig_3_2(c):
    # insulated rigid container
    rect(c, 20, 10, 320, 100, lw=1.0)
    rect(c, 34, 24, 292, 72, lw=1.0, fill=1)
    hatch(c, 20, 10, 320, 14)
    hatch(c, 20, 96, 320, 14)
    hatch(c, 20, 24, 14, 72)
    hatch(c, 326, 24, 14, 72)
    rect(c, 34, 24, 292, 72, lw=1.0)
    rect(c, 178, 24, 4, 72, lw=0.75, fill=0.6)
    text(c, 106, 55, 'ideal gas', anchor='c')
    text(c, 254, 55, 'vacuum', anchor='c')
    text(c, 350, 99, 'thermal')
    text(c, 350, 86, 'insulation')
    line(c, 348, 95, 336, 102, w=0.5)
    text(c, 196, 116, 'partition')
    line(c, 194, 119, 181, 90, w=0.5)


Q3 = Question([
    Part('a', [
        Text('State what is meant by the <i>internal energy</i> of a system.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('A fixed mass of an ideal gas is taken through the cycle of changes A → B → C → A shown in '
             'Fig. 3.1.'),
        Fig(330, 255, fig_3_1, 'Fig. 3.1'),
        Text('During A → B, the gas is compressed at constant pressure. During B → C, the gas is heated at '
             'constant volume. During C → A, the gas expands and the variation of pressure <i>p</i> with volume '
             '<i>V</i> is a straight line.'),
        Text('Table 3.1 shows some of the energy changes during the cycle. <i>W</i> is the work done <b>on</b> '
             'the gas, <i>q</i> is the thermal energy supplied <b>to</b> the gas and Δ<i>U</i> is the increase in '
             'internal energy of the gas. Complete Table 3.1.'),
        Table([
            ['change', '<i>W</i> / J', '<i>q</i> / J', 'Δ<i>U</i> / J'],
            ['A → B', '+200', '–500', ''],
            ['B → C', '', '+300', ''],
            ['C → A', '', '', ''],
        ], [90, 90, 90, 90], 'Table 3.1', row_heights=[26, 32, 32, 32]),
        Mark(3),
    ]),
    Part('c', [
        Text('State and explain whether the temperature of the gas is constant during the change C → A.'),
        Lines(3, 2),
    ]),
    Part('d', [
        Text('A rigid container is surrounded by thermal insulation. The container is divided into two equal '
             'sections by a partition, as shown in Fig. 3.2.'),
        Fig(400, 130, fig_3_2, 'Fig. 3.2'),
        Text('One section contains an ideal gas and the other section is a vacuum. The partition is removed and '
             'the gas expands to fill the whole container.'),
        Text('State and explain whether the temperature of the gas changes.'),
        Lines(4, 3),
    ]),
])

MS3 = [
    MSRow('3(a)', [
        ('sum of (random) kinetic and potential energies', 'B1'),
        ('of the molecules', 'B1'),
    ]),
    MSRow('3(b)', [
        ('A → B: Δ<i>U</i> = –300 J<br/>B → C: <i>W</i> = 0 and Δ<i>U</i> = +300 J', 'B1'),
        ('C → A: <i>W</i> = –400 J (area under line, negative because the gas expands)', 'B1'),
        ('C → A: Δ<i>U</i> = 0 (Δ<i>U</i> for the whole cycle is zero) and <i>q</i> = +400 J', 'B1'),
    ]),
    MSRow('3(c)', [
        ('temperature is not constant', 'B1'),
        ('<i>pV</i> (proportional to <i>T</i>) is 300 J at C and at A but is greater between them, e.g. 400 J at '
         '<i>V</i> = 2.0 × 10<sup>–3</sup> m<sup>3</sup>, so temperature rises and then falls', 'B1'),
    ], note='Δ<i>U</i> = 0 means only that the temperatures at C and A are equal'),
    MSRow('3(d)', [
        ('no work is done (<i>W</i> = 0) because the gas expands into a vacuum / does not push against '
         'anything', 'B1'),
        ('no thermal energy is transferred (<i>q</i> = 0) because the container is insulated', 'B1'),
        ('so Δ<i>U</i> = 0 and, since the internal energy of an ideal gas is kinetic energy of the molecules '
         'only, the temperature does not change', 'B1'),
    ]),
]


# ================================================================== Question 4

def _track_and_wall(c):
    hatch(c, 20, 20, 14, 70)
    line(c, 34, 20, 34, 90, w=1.0)
    rect(c, 34, 12, 336, 10, lw=0.9)
    text(c, 300, -2, 'air track', anchor='c')


def _glider(c, x):
    polyline(c, [(x, 22), (x + 66, 22), (x + 66, 50), (x + 56, 60), (x + 10, 60), (x, 50)], w=1.0,
             close=True, fill=1)


def fig_4_1(c):
    _track_and_wall(c)
    spring(c, 34, 40, 220, 40, coils=10, amp=6)
    _glider(c, 220)
    text(c, 253, 66, 'glider', anchor='c')
    text(c, 127, 54, 'spring', anchor='c')


def fig_4_2(c):
    g = Graph(c, 70, 40, _sq(50), _sq(25), xr=(-5, 5), yr=(0, 50), xmajor=1, ymajor=10, minor=5,
              axes=False)
    _lb_axes(c, g, _ticks(-5, 5, 1), _ticks(0, 50, 10), '<i>x</i> / cm', '<i>E</i><sub>P</sub> / mJ')
    g.curve(lambda x: 2.5 * x * x, -4.0, 4.0, w=1.2)
    px, py = g.P(-3.4, 2.5 * 3.4 ** 2)
    label(c, px - 7, py - 2, '<i>E</i><sub>P</sub>', anchor='r')


def fig_4_3(c):
    _track_and_wall(c)
    spring(c, 34, 40, 124, 40, coils=6, amp=6)
    rect(c, 124, 30, 6, 20, lw=0.75, fill=0.6)
    spring(c, 130, 40, 220, 40, coils=6, amp=6)
    _glider(c, 220)
    text(c, 253, 66, 'glider', anchor='c')
    text(c, 79, 54, 'spring', anchor='c')
    text(c, 175, 54, 'spring', anchor='c')


Q4 = Question([
    Part('a', [
        Text('State what is meant by <i>simple harmonic motion</i>.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('A glider of mass 0.50 kg on a horizontal air track is attached to a fixed support by a light '
             'spring, as shown in Fig. 4.1.'),
        Fig(380, 100, fig_4_1, 'Fig. 4.1'),
        Text('Frictional forces are negligible. The glider is displaced 4.0 cm from its equilibrium position and '
             'released. It then oscillates with simple harmonic motion.'),
        Text('Fig. 4.2 shows the variation with displacement <i>x</i> of the elastic potential energy '
             '<i>E</i><sub>P</sub> stored in the spring.'),
        Fig(380, 190, fig_4_2, 'Fig. 4.2'),
        Sub('i', [
            Text('Use Fig. 4.2 to show that the spring constant of the spring is 50 N m<sup>–1</sup>.'),
            Space(5),
            Mark(1),
        ]),
        Sub('ii', [
            Text('On Fig. 4.2, draw lines to show the variation with <i>x</i> of:<br/><br/>'
                 '1.  the kinetic energy of the glider (label this line K)<br/>'
                 '2.  the total energy of the oscillations (label this line T).'),
            Mark(2),
        ]),
    ]),
    Part('c', [
        Text('The spring is replaced by two springs connected end to end, as shown in Fig. 4.3. Each spring is '
             'identical to the original spring.'),
        Fig(380, 100, fig_4_3, 'Fig. 4.3'),
        Text('The glider is displaced 2.0 cm from its new equilibrium position and released.'),
        Text('Determine the period of the oscillations of the glider.'),
        Space(10),
        Answer('period', 's', 3),
    ]),
    Part('d', [
        Text('The glider is attached again to the single spring of Fig. 4.1, displaced 4.0 cm and released. The '
             'air supply to the track is reduced so that the oscillations are lightly damped. After several '
             'oscillations, the amplitude has decreased to 2.0 cm.'),
        Text('Determine the energy that has been dissipated.'),
        Space(8),
        Answer('energy', 'mJ', 2),
    ]),
])

MS4 = [
    MSRow('4(a)', [
        ('acceleration (directly) proportional to displacement (from a fixed point)', 'B1'),
        ('acceleration in the opposite direction to the displacement / directed towards the fixed point', 'B1'),
    ]),
    MSRow('4(b)(i)', [
        ('<i>E</i><sub>P</sub> = ½<i>kx</i><sup>2</sup> with <i>E</i><sub>P</sub> = 40 mJ at <i>x</i> = 4.0 cm:'
         '<br/><i>k</i> = 2 × 0.040 / 0.040<sup>2</sup> = 50 N m<sup>–1</sup>', 'B1'),
    ]),
    MSRow('4(b)(ii)', [
        ('T: horizontal line at 40 mJ from <i>x</i> = –4.0 cm to <i>x</i> = +4.0 cm', 'B1'),
        ('K: inverted parabola, 40 mJ at <i>x</i> = 0 and zero at <i>x</i> = ±4.0 cm, crossing the '
         '<i>E</i><sub>P</sub> line at 20 mJ (<i>x</i> = ±2.8 cm)', 'B1'),
    ]),
    MSRow('4(c)', [
        ('same tension in each spring so each extends by half the displacement: effective spring constant '
         '= 25 N m<sup>–1</sup>', 'C1'),
        ('<i>a</i> = –(<i>k</i> / <i>m</i>)<i>x</i> so <i>ω</i> = √(25 / 0.50) = 7.1 rad s<sup>–1</sup>', 'C1'),
        ('<i>T</i> = 2π / <i>ω</i> = 0.89 s', 'A1'),
    ], note='the period does not depend on the amplitude, so the 2.0 cm displacement is not used<br/>'
            'springs treated as in parallel (<i>k</i> = 100 N m<sup>–1</sup>, <i>T</i> = 0.44 s): max. 1 mark'),
    MSRow('4(d)', [
        ('energy is proportional to (amplitude)<sup>2</sup> / <i>E</i> = ½<i>kx</i><sub>0</sub><sup>2</sup>: '
         'energy remaining = 40 / 4 = 10 mJ', 'C1'),
        ('energy dissipated = 40 – 10 = 30 mJ', 'A1'),
    ], note='20 mJ (energy taken as proportional to amplitude) scores 0'),
]


# ================================================================== Question 5

_KQ, _H, _A = 11.25, 0.05, 0.01        # image-charge model: kQ / V m, height / m, sphere radius / m


def _pot(x, z):
    return _KQ * (1 / math.hypot(x, z - _H) - 1 / math.hypot(x, z + _H))


def _contour(level, n=180):
    pts = []
    for k in range(n + 1):
        th = 2 * math.pi * k / n
        dx, dz = math.cos(th), math.sin(th)
        lo, hi = _A, 1.0
        if dz < 0:
            hi = min(hi, _H / -dz - 1e-9)
        hi = min(hi, 0.2)
        for _ in range(50):
            mid = (lo + hi) / 2
            if _pot(mid * dx, _H + mid * dz) > level:
                lo = mid
            else:
                hi = mid
        pts.append((lo * dx, _H + lo * dz))
    return pts


def fig_5_1(c):
    s = 2400.0                       # points per metre (24 pt per cm)
    ox, oz = 190, 28                 # plate surface at the centre of the figure
    P = lambda x, z: (ox + s * x, oz + s * z)
    # earthed plate
    rect(c, ox - 165, oz - 6, 330, 6, lw=0.9, fill=0.6)
    _earth(c, ox + 140, oz - 6)
    text(c, ox - 160, oz - 22, 'earthed metal plate')
    # equipotentials
    for lev in (750, 500, 250):
        pts = [P(x, z) for x, z in _contour(lev)]
        polyline(c, pts, w=0.75, dash=[4, 2.5])
    # sphere
    sx, sz = P(0, _H)
    circle(c, sx, sz, s * _A, w=1.0, fill=0.85)
    text(c, sx, sz - 4, 'S', anchor='c')
    # labels of the equipotentials, with horizontal leaders to the right
    for lev, deg in ((750, 78), (500, 20), (250, -14)):
        x, z = _contour(lev, n=360)[deg % 360]
        px, pz = P(x, z)
        tx = ox + 106
        line(c, px, pz, tx - 4, pz, w=0.5)
        text(c, tx, pz - 3.9, f'+{lev} V')
    # line XY
    xX, zX = P(0, 0)
    xY, zY = P(0, _H - _A)
    line(c, xX, zX, xY, zY, w=0.6)
    dot(c, xX, zX, 1.8)
    dot(c, xY, zY, 1.8)
    text(c, xX + 5, zX + 5, 'X')
    label(c, xY - 5, zY - 15, 'Y', anchor='r')
    # points P and Q on the 500 V line, and a path between them that dips towards the plate
    pts = _contour(500, n=360)
    xp, zp = pts[180]
    xq, zq = pts[0]
    pP, pQ = P(xp, zp), P(xq, zq)
    dot(c, *pP, 2.2)
    dot(c, *pQ, 2.2)
    text(c, pP[0] - 6, pP[1] + 4, 'P', anchor='r')
    text(c, pQ[0] + 6, pQ[1] + 4, 'Q')
    path = []
    for k in range(61):
        u = -1 + 2 * k / 60
        x = xq * u
        z = zp - (zp - 0.013) * (1 - u * u) ** 0.7
        path.append(P(x, z))
    polyline(c, path, w=0.9, dash=[1, 2])
    a, b = path[22], path[24]
    arrow(c, a[0], a[1], b[0], b[1], head=6)


def fig_5_2(c):
    g = Graph(c, 70, 29, _sq(40), _sq(20), xr=(0, 4.0), yr=(0, 1000), xmajor=0.5, ymajor=250, minor=5,
              xlabel='<i>x</i> / cm', ylabel='<i>V</i> / V',
              xticks=[(v, '%.1f' % v if v else '0') for v in (0, 1, 2, 3, 4)],
              yticks=[(v, str(v)) for v in range(0, 1001, 250)])
    g.curve(lambda xc: _pot(0, xc / 100), 0, 4.0, w=1.2)
    g.finish()


Q5 = Question([
    Text('An isolated metal sphere S is held above a large horizontal metal plate that is earthed. The sphere '
         'is charged so that its electric potential is +1000 V. Fig. 5.1 shows the lines of equal electric '
         'potential (equipotential lines) for potentials of +750 V, +500 V and +250 V around the sphere.'),
    Fig(400, 232, fig_5_1, 'Fig. 5.1'),
    Part('a', [
        Sub('i', [
            Text('On Fig. 5.1, draw an arrow at point P to show the direction of the electric field at P.'),
            Mark(1),
        ]),
        Sub('ii', [
            Text('Points P and Q lie on the same equipotential line. A small positive charge is moved from P to Q '
                 'along the dotted path shown in Fig. 5.1. State and explain the total work done on the charge by '
                 'the electric field.'),
            Lines(3, 2),
        ]),
    ]),
    Part('b', [
        Text('Point X is on the plate and point Y is on the sphere, vertically above X. Fig. 5.2 shows the '
             'variation of the electric potential <i>V</i> with distance <i>x</i> from X along XY.'),
        Fig(330, 148, fig_5_2, 'Fig. 5.2'),
        Sub('i', [
            Text('A student states that the electric field strength at X is zero because the electric potential '
                 'at X is zero. Use Fig. 5.2 to explain why the student is wrong.'),
            Lines(3, 2),
        ]),
        Sub('ii', [
            Text('A charged oil droplet of mass 7.2 × 10<sup>–16</sup> kg is held stationary at the point on XY '
                 'where <i>x</i> = 2.0 cm. Air resistance and upthrust are negligible.'),
            Text('Use Fig. 5.2 to determine the number of excess electrons on the droplet.'),
            Space(10),
            Answer('number', '', 3),
        ]),
        Sub('iii', [
            Text('The charge on the sphere is now doubled. The droplet is initially at rest at the same point. '
                 'Determine the magnitude and the direction of the initial acceleration of the droplet.'),
            Space(6),
            Answer('magnitude', 'm s<sup>–2</sup>', None),
            Answer('direction', '', 2),
        ]),
    ]),
])

MS5 = [
    MSRow('5(a)(i)', [
        ('arrow at P perpendicular to the equipotential line, pointing away from the sphere (towards lower '
         'potential)', 'B1'),
    ]),
    MSRow('5(a)(ii)', [
        ('zero', 'B1'),
        ('P and Q are at the same potential, so work done = <i>q</i>Δ<i>V</i> = 0 (whatever the path)', 'B1'),
    ]),
    MSRow('5(b)(i)', [
        ('field strength = (–) potential gradient / <i>E</i> = –d<i>V</i> / d<i>x</i>', 'B1'),
        ('gradient of the graph at <i>x</i> = 0 is not zero (about 90 V cm<sup>–1</sup> = '
         '9 × 10<sup>3</sup> V m<sup>–1</sup>), so the field strength at X is not zero', 'B1'),
    ]),
    MSRow('5(b)(ii)', [
        ('tangent at <i>x</i> = 2.0 cm: field strength = gradient = 1.5 × 10<sup>4</sup> V m<sup>–1</sup> '
         '(allow 1.3 × 10<sup>4</sup> to 1.7 × 10<sup>4</sup> V m<sup>–1</sup>)', 'C1'),
        ('<i>qE</i> = <i>mg</i> so <i>q</i> = 7.2 × 10<sup>–16</sup> × 9.81 / 1.5 × 10<sup>4</sup> = '
         '4.7 × 10<sup>–19</sup> C', 'C1'),
        ('number = <i>q</i> / <i>e</i> = 3', 'A1'),
    ], note='the final answer must be an integer: a non-integer answer (e.g. 2.9) scores max. 2'),
    MSRow('5(b)(iii)', [
        ('potential and field strength at every point double, so the electric force on the droplet becomes '
         '2<i>mg</i> (upwards)', 'B1'),
        ('resultant force = <i>mg</i> upwards so acceleration = 9.81 m s<sup>–2</sup> upwards', 'B1'),
    ]),
]


# ================================================================== Question 6

def fig_6_1(c):
    # plates
    xl, xr, y0, y1 = 165, 205, 35, 100
    line(c, xl, y0, xl, y1, w=2.6)
    line(c, xr, y0, xr, y1, w=2.6)
    darrow(c, xl, y1 + 10, xr, y1 + 10, head=5)
    text(c, (xl + xr) / 2, y1 + 15, '<i>d</i>', anchor='c')
    # circuit
    wire(c, [(xl, 68), (70, 68), (70, 15), (120, 15)])
    cell(c, 120, 15, 160, 15)
    wire(c, [(160, 15), (215, 15)])
    switch(c, 215, 15, 255, 15)
    wire(c, [(255, 15), (300, 15), (300, 68), (xr, 68)])
    text(c, 140, 32, '12 V', anchor='c')
    text(c, 235, 30, 'S', anchor='c')
    text(c, xr + 12, y1 - 6, 'metal plates')


def fig_6_2(c):
    g = Graph(c, 70, 32, _sq(50), _sq(25), xr=(0, 10), yr=(0, 2.5), xmajor=1, ymajor=0.5, minor=5,
              xlabel='<i>t</i> / s', ylabel='ln (<i>V</i> / V)',
              xticks=[(v, str(v)) for v in range(0, 11, 2)],
              yticks=[(v, '%.1f' % v if v else '0') for v in (0, 0.5, 1.0, 1.5, 2.0, 2.5)])
    f = lambda t: math.log(10.0) - t / 4.7
    g.line(0, f(0), 10, f(10), w=1.2)
    g.finish()


Q6 = Question([
    Part('a', [
        Text('Define the <i>capacitance</i> of a parallel plate capacitor.'),
        Lines(2, 1),
    ]),
    Part('b', [
        Text('A parallel plate capacitor is connected to a battery of electromotive force (e.m.f.) 12 V and a '
             'switch S, as shown in Fig. 6.1.'),
        Fig(330, 120, fig_6_1, 'Fig. 6.1'),
        Text('The capacitance of the capacitor is inversely proportional to the separation of its plates. The '
             'plates are initially a distance <i>d</i> apart and the capacitor is fully charged. Two separate '
             'experiments are carried out, each starting from this initial state.'),
        Text('Experiment 1: switch S remains closed while the plates are slowly pulled apart until their '
             'separation is 2<i>d</i>.<br/>'
             'Experiment 2: switch S is opened and then the plates are slowly pulled apart until their '
             'separation is 2<i>d</i>.'),
        Sub('i', [
            Text('Complete Table 6.1 by giving the ratio <i>final value</i> / <i>initial value</i> of each '
                 'quantity. The first row has been completed for you.'),
            Table([
                ['quantity', 'experiment 1<br/>(S closed)', 'experiment 2<br/>(S open)'],
                ['capacitance', '0.5', '0.5'],
                ['magnitude of charge on each plate', '', ''],
                ['potential difference between plates', '', ''],
                ['energy stored', '', ''],
            ], [200, 110, 110], 'Table 6.1', row_heights=[34, 24, 28, 28, 28]),
            Mark(3),
        ]),
        Sub('ii', [
            Text('Work is done to pull the plates apart in both experiments. Explain why, in experiment 1, the '
                 'energy stored in the capacitor decreases.'),
            Lines(3, 2),
        ]),
    ]),
    Part('c', [
        Text('A capacitor of capacitance 470 μF is charged to a potential difference (p.d.) of 10.0 V. It is '
             'then discharged through a resistor of resistance <i>R</i>. Fig. 6.2 shows the variation with time '
             '<i>t</i> of ln (<i>V</i> / V), where <i>V</i> is the p.d. across the capacitor.'),
        Fig(380, 184, fig_6_2, 'Fig. 6.2'),
        Sub('i', [
            Text('Use Fig. 6.2 to determine <i>R</i>.'),
            Space(8),
            Answer('<i>R</i>', 'Ω', 2),
        ]),
        Sub('ii', [
            Text('Determine the time taken for the energy stored in the capacitor to decrease to half of its '
                 'initial value.'),
            Space(8),
            Answer('time', 's', 2),
        ]),
    ]),
])

MS6 = [
    MSRow('6(a)', [
        ('(magnitude of) charge on one plate per unit potential difference between the plates', 'B1'),
    ]),
    MSRow('6(b)(i)', [
        ('experiment 1: charge 0.5 and p.d. 1 (unchanged)', 'B1'),
        ('experiment 2: charge 1 (unchanged) and p.d. 2', 'B1'),
        ('energy stored: 0.5 in experiment 1 and 2 in experiment 2', 'B1'),
    ]),
    MSRow('6(b)(ii)', [
        ('charge on the plates decreases, so charge flows back through the battery (against its e.m.f.) / '
         'the battery is charged', 'B1'),
        ('energy is transferred to the battery: both the work done in pulling the plates apart and the '
         'decrease in stored energy are transferred to the battery', 'B1'),
    ]),
    MSRow('6(c)(i)', [
        ('gradient = –1 / <i>RC</i><br/>gradient = –(2.30 – 0.18) / 10 = –0.21 s<sup>–1</sup>', 'C1'),
        ('<i>R</i> = 1 / (0.213 × 470 × 10<sup>–6</sup>) = 1.0 × 10<sup>4</sup> Ω', 'A1'),
    ]),
    MSRow('6(c)(ii)', [
        ('energy is proportional to <i>V</i><sup>2</sup>, so energy halves when <i>V</i> = '
         '<i>V</i><sub>0</sub> / √2 / when ln (<i>V</i> / V) has decreased by ½ ln 2 = 0.35', 'C1'),
        ('<i>t</i> = ½<i>RC</i> ln 2 = 0.5 × 4.7 × 0.693 = 1.6 s', 'A1'),
    ], note='3.3 s (the time for the p.d. to halve) scores 0'),
]


# ================================================================== Question 7

_G, _Z0, _AC, _FMAX = 9.81, 0.05, 0.025, 8.0


def _flux(t_ms):
    t = t_ms / 1000.0
    z = _Z0 - 0.5 * _G * t * t
    return _FMAX * (1 + (z / _AC) ** 2) ** -1.5


def fig_7_1(c):
    cx = 120
    # coil: loops on a vertical former
    ys = [22 + 8 * k for k in range(7)]
    for y in ys:
        polyline(c, _ellipse(cx, y, 34, 6, 0, 0, math.pi), w=0.5)
    line(c, cx - 34, ys[0], cx - 34, ys[-1], w=0.6)
    line(c, cx + 34, ys[0], cx + 34, ys[-1], w=0.6)
    for y in ys:
        polyline(c, _ellipse(cx, y, 34, 6, 0, math.pi, 2 * math.pi), w=1.0)
    # leads to the resistor
    wire(c, [(cx + 34, ys[-1]), (240, ys[-1]), (240, 66)])
    resistor(c, 240, 66, 240, 30, label='resistor')
    wire(c, [(240, 30), (240, ys[0]), (cx + 34, ys[0])])
    # magnet above the coil
    rect(c, cx - 9, 92, 18, 52, lw=1.0, fill=1)
    line(c, cx - 9, 118, cx + 9, 118)
    text(c, cx, 101, 'N', anchor='c')
    text(c, cx, 127, 'S', anchor='c')
    arrow(c, cx - 30, 136, cx - 30, 104)
    text(c, cx + 18, 132, 'magnet')
    text(c, cx - 50, 30, 'coil', anchor='r')
    line(c, cx - 48, 34, cx - 36, 42, w=0.5)


def fig_7_2(c):
    g = Graph(c, 60, 30, _sq(75), _sq(25), xr=(0, 150), yr=(0, 10), xmajor=10, ymajor=2, minor=5,
              xlabel='<i>t</i> / ms', ylabel='<i>N</i>Φ / mWb',
              xticks=[(v, str(v)) for v in range(0, 151, 20)])
    g.curve(_flux, 0, 150, n=400, w=1.2)
    g.finish()


def fig_7_3(c):
    g = Graph(c, 60, 4, _sq(75), _sq(18), xr=(0, 150), yr=(-1, 1), xmajor=10, ymajor=1, minor=5,
              grid=False, xlabel='<i>t</i> / ms', ylabel='<i>E</i>',
              xticks=[(v, str(v) if v else '') for v in range(0, 151, 20)], yticks=[(0, '0')])
    g.finish()


def fig_7_4(c):
    x0, y0, w, h = 90, 20, 170, 42
    ym = y0 + h / 2
    rect(c, x0, y0, w, h, lw=1.0, fill=0.92)
    for i in range(5):
        for j in range(2):
            px, py = x0 + 25 + 30 * i, y0 + 11 + 20 * j
            line(c, px - 3, py - 3, px + 3, py + 3, w=0.6)
            line(c, px - 3, py + 3, px + 3, py - 3, w=0.6)
    # current leads
    line(c, 20, ym, x0, ym)
    arrow(c, 35, ym, 62, ym)
    text(c, 48, ym + 6, '<i>I</i>', anchor='c')
    line(c, x0 + w, ym, 330, ym)
    arrow(c, 290, ym, 317, ym)
    text(c, 303, ym + 6, '<i>I</i>', anchor='c')
    # Hall voltage leads to a voltmeter
    xm = x0 + w / 2
    wire(c, [(xm, y0 + h), (xm, 78), (370, 78), (370, ym + 9)])
    meter(c, 370, ym, 'V')
    wire(c, [(370, ym - 9), (370, 4), (xm, 4), (xm, y0)])
    dot(c, xm, y0 + h, 1.8)
    dot(c, xm, y0, 1.8)
    text(c, xm - 6, y0 + h + 5, 'P', anchor='r')
    text(c, xm - 6, y0 - 11, 'Q', anchor='r')
    text(c, x0 + w + 6, y0 + h + 5, 'slice')


Q7 = Question([
    Part('a', [
        Text('State Faraday\'s law of electromagnetic induction.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('A bar magnet is held vertically above a coil of wire, as shown in Fig. 7.1. The coil is connected '
             'to a resistor.'),
        Fig(300, 150, fig_7_1, 'Fig. 7.1'),
        Text('The magnet is released from rest at time <i>t</i> = 0 and falls through the coil. Fig. 7.2 shows '
             'the variation with <i>t</i> of the magnetic flux linkage <i>N</i>Φ of the coil.'),
        Fig(490, 180, fig_7_2, 'Fig. 7.2'),
        Sub('i', [
            Text('On Fig. 7.3, sketch the variation with <i>t</i> of the electromotive force (e.m.f.) <i>E</i> '
                 'induced in the coil.'),
            Fig(490, 106, fig_7_3, 'Fig. 7.3'),
            Mark(3),
        ]),
        Sub('ii', [
            Text('Use Lenz\'s law to explain the direction of the force exerted on the magnet by the current in '
                 'the coil as the magnet <b>leaves</b> the coil.'),
            Lines(3, 2),
        ]),
    ]),
    Part('c', [
        Text('Fig. 7.4 shows a thin slice of a conductor carrying a current <i>I</i> in a uniform magnetic '
             'field directed into the page. The Hall voltage is measured between points P and Q. The charge '
             'carriers in the slice are electrons.'),
        Fig(400, 82, fig_7_4, 'Fig. 7.4'),
        Text('The slice is replaced by a slice with the same dimensions made of a material in which the charge '
             'carriers are positive. The number density of the charge carriers in the new slice is one quarter '
             'of that in the original slice. The current and the magnetic field are unchanged. State and '
             'explain <b>two</b> differences between the new Hall voltage and the original Hall voltage.'),
        Lines(4, 3),
    ]),
])

MS7 = [
    MSRow('7(a)', [
        ('e.m.f. induced is proportional to', 'M1'),
        ('rate of change of magnetic flux linkage / rate of cutting of magnetic flux', 'A1'),
    ]),
    MSRow('7(b)(i)', [
        ('<i>E</i> = 0 at <i>t</i> ≈ 100 ms (when the flux linkage is maximum), with pulses of opposite sign '
         'before and after this time', 'B1'),
        ('magnitude of <i>E</i> greatest where the gradient of Fig. 7.2 is greatest (at <i>t</i> ≈ 90 ms and '
         '<i>t</i> ≈ 115 ms) and <i>E</i> ≈ 0 at <i>t</i> = 0 and at <i>t</i> = 150 ms', 'B1'),
        ('second pulse has a larger peak and a shorter duration than the first', 'B1'),
    ], note='<i>E</i> = –d(<i>N</i>Φ) / d<i>t</i>, so the first pulse is negative and the second positive; '
            'allow the inverted sketch'),
    MSRow('7(b)(ii)', [
        ('induced current opposes the change that produces it / opposes the motion of the magnet / opposes '
         'the decrease in flux linkage', 'B1'),
        ('force on the magnet is upwards (the coil attracts the magnet as it leaves)', 'B1'),
    ], note='a downward force (magnet "pushed out" of the coil) scores 0'),
    MSRow('7(c)', [
        ('Hall voltage is reversed in polarity / the other face (Q instead of P, or P instead of Q) is now '
         'at the higher potential', 'B1'),
        ('positive carriers move in the opposite direction to electrons, so the magnetic force (<i>BQv</i>) on '
         'them is in the same direction: they collect on the same face, but the charge there is now positive',
         'B1'),
        ('Hall voltage is four times larger because <i>V</i><sub>H</sub> = <i>BI</i> / <i>ntq</i>, so '
         '<i>V</i><sub>H</sub> is proportional to 1 / <i>n</i> (the drift speed is four times larger)', 'B1'),
    ]),
]


# ================================================================== Question 8

def fig_8_1(c):
    T, B, L, R = (200, 150), (200, 50), (150, 100), (250, 100)
    for p, q in ((L, T), (T, R), (L, B), (B, R)):
        _rot(c, p[0], p[1], q[0], q[1], diode)
    for p in (T, B, L, R):
        dot(c, *p, 2)
    text(c, 166, 132, 'D1', anchor='r')
    text(c, 234, 132, 'D2')
    text(c, 166, 61, 'D3', anchor='r')
    text(c, 234, 61, 'D4')
    # supply
    ac_supply(c, 50, 100)
    wire(c, [(50, 109), (50, 170), (200, 170), (200, 150)])
    wire(c, [(50, 91), (50, 32), (200, 32), (200, 50)])
    circle(c, 50, 170, 2.5, fill=1)
    circle(c, 50, 32, 2.5, fill=1)
    text(c, 42, 166, 'A', anchor='r')
    text(c, 42, 28, 'B', anchor='r')
    # load
    wire(c, [(250, 100), (330, 100)])
    resistor(c, 330, 100, 330, 30)
    text(c, 342, 61, 'load resistor')
    text(c, 342, 48, '<i>R</i> = 150 Ω')
    wire(c, [(330, 30), (330, 12), (122, 12), (122, 100), (150, 100)])


def fig_8_2(c):
    g = Graph(c, 60, 38, _sq(60), _sq(25), xr=(0, 30), yr=(0, 20), xmajor=2.5, ymajor=4, minor=5,
              xlabel='<i>t</i> / ms', ylabel='<i>V</i> / V',
              xticks=[(v, str(v)) for v in range(0, 31, 5)],
              yticks=[(v, str(v)) for v in range(0, 21, 4)])
    g.curve(lambda t: abs(17.0 * math.sin(2 * math.pi * t / 20)), 0, 30, n=400, w=1.0, dash=[4, 3])
    g.finish()


Q8 = Question([
    Part('a', [
        Text('State what is meant by the root-mean-square (r.m.s.) value of an alternating current.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('Four ideal diodes D1, D2, D3 and D4 are used in the bridge rectifier shown in Fig. 8.1.'),
        Fig(420, 185, fig_8_1, 'Fig. 8.1'),
        Text('The sinusoidal alternating supply has a peak voltage of 17.0 V and a frequency of 50 Hz. Terminal A '
             'of the supply is positive with respect to terminal B between time <i>t</i> = 0 and '
             '<i>t</i> = 10 ms.'),
        Text('Fig. 8.2 shows, as a dashed line, the variation with <i>t</i> of the potential difference (p.d.) '
             '<i>V</i> across the load resistor.'),
        Fig(440, 195, fig_8_2, 'Fig. 8.2'),
        Sub('i', [
            Text('State the <b>two</b> diodes that conduct between <i>t</i> = 0 and <i>t</i> = 10 ms.'),
            Lines(1, 1),
        ]),
        Sub('ii', [
            Text('Calculate the mean power dissipated in the load resistor.'),
            Space(8),
            Answer('mean power', 'W', 2),
        ]),
    ]),
    Part('c', [
        Text('Diode D4 develops a fault so that it no longer conducts in either direction.'),
        Sub('i', [
            Text('On Fig. 8.2, draw a solid line to show the variation with <i>t</i> of <i>V</i> between '
                 '<i>t</i> = 0 and <i>t</i> = 30 ms.'),
            Mark(1),
        ]),
        Sub('ii', [
            Text('Determine the r.m.s. value of <i>V</i>.'),
            Space(8),
            Answer('r.m.s. value', 'V', 2),
        ]),
    ]),
    Part('d', [
        Text('A capacitor is now connected in parallel with the load resistor to smooth the output p.d. Diode D4 '
             'is still faulty.'),
        Text('Suggest and explain how the variation (ripple) of the smoothed output p.d. compares with the ripple '
             'when all four diodes are working.'),
        Lines(3, 2),
    ]),
])

MS8 = [
    MSRow('8(a)', [
        ('the value of the direct current', 'B1'),
        ('that dissipates (thermal) energy at the same (average) rate in a resistor', 'B1'),
    ]),
    MSRow('8(b)(i)', [
        ('D2 and D3', 'B1'),
    ]),
    MSRow('8(b)(ii)', [
        ('full-wave rectified p.d. has the same r.m.s. value as the supply: <i>V</i><sub>r.m.s.</sub> = '
         '17.0 / √2 = 12.0 V', 'C1'),
        ('<i>P</i> = <i>V</i><sub>r.m.s.</sub><sup>2</sup> / <i>R</i> = 12.0<sup>2</sup> / 150 = 0.96 W', 'A1'),
    ], note='allow <i>P</i> = <i>V</i><sub>0</sub><sup>2</sup> / 2<i>R</i>'),
    MSRow('8(c)(i)', [
        ('half-wave output: the humps between 0 and 10 ms and between 20 ms and 30 ms only (peak 17 V), with '
         '<i>V</i> = 0 from 10 ms to 20 ms', 'B1'),
    ]),
    MSRow('8(c)(ii)', [
        ('mean power / mean value of <i>V</i><sup>2</sup> is halved', 'C1'),
        ('<i>V</i><sub>r.m.s.</sub> = 12.0 / √2 (= 17.0 / 2) = 8.5 V', 'A1'),
    ], note='6.0 V (r.m.s. value halved) scores 0'),
    MSRow('8(d)', [
        ('ripple is greater / minimum p.d. is lower', 'B1'),
        ('peaks occur every 20 ms instead of every 10 ms, so the capacitor discharges (through the resistor) for '
         'about twice as long between peaks', 'B1'),
    ]),
]


# ================================================================== Question 9

def fig_9_1(c):
    # electron gun
    rect(c, 20, 52, 8, 36, lw=0.9, fill=0.6)
    text(c, 24, 96, 'cathode', anchor='c')
    line(c, 70, 50, 70, 66, w=2.2)
    line(c, 70, 74, 70, 90, w=2.2)
    text(c, 70, 96, 'anode', anchor='c')
    wire(c, [(24, 52), (24, 26), (38, 26)])
    cell(c, 56, 26, 38, 26)
    wire(c, [(56, 26), (70, 26), (70, 50)])
    text(c, 47, 6, '4.0 kV', anchor='c')
    arrow(c, 30, 70, 64, 70, head=5)
    line(c, 64, 70, 160, 70, w=0.9)
    arrow(c, 100, 70, 125, 70, head=6)
    text(c, 110, 78, 'electron beam', anchor='c')
    # graphite film and screen
    line(c, 160, 50, 160, 90, w=2.0)
    text(c, 160, 96, 'graphite film', anchor='c')
    for ang in (12, 22):
        t = math.radians(ang)
        line(c, 160, 70, 290, 70 + 130 * math.tan(t), w=0.5, dash=[3, 2])
        line(c, 160, 70, 290, 70 - 130 * math.tan(t), w=0.5, dash=[3, 2])
    line(c, 160, 70, 290, 70, w=0.5, dash=[3, 2])
    line(c, 290, 10, 290, 130, w=2.2)
    text(c, 290, 136, 'screen', anchor='c')
    # pattern on the screen, seen from the front
    px, py = 395, 70
    text(c, px, 136, 'pattern on screen', anchor='c')
    rect(c, px - 55, 15, 110, 110, lw=0.75)
    c.saveState()
    c.setStrokeGray(0.35)
    for r in (26, 47):
        c.setLineWidth(3.5)
        c.circle(px, py, r, stroke=1, fill=0)
    c.restoreState()
    dot(c, px, py, 5)


def fig_9_2(c):
    lev = (-1.6, -3.7, -5.5, -10.4)
    s = 12.0
    y = lambda e: 144 + s * e
    for e in lev:
        line(c, 60, y(e), 260, y(e), w=1.0)
        text(c, 268, y(e) - 4, ('%.1f' % e).replace('-', '–') + ' eV')
    text(c, 160, y(-10.4) - 15, 'ground state', anchor='c')


Q9 = Question([
    Part('a', [
        Text('Electrons are accelerated from rest through a potential difference of 4.0 kV. They are then '
             'incident on a thin film of graphite in a vacuum, as shown in Fig. 9.1. A pattern of concentric '
             'rings is seen on a fluorescent screen.'),
        Fig(460, 145, fig_9_1, 'Fig. 9.1', note='(not to scale)'),
        Sub('i', [
            Text('Calculate the de Broglie wavelength of the electrons.'),
            Space(8),
            Answer('wavelength', 'm', 2),
        ]),
        Sub('ii', [
            Text('The accelerating potential difference is increased to 16 kV. A student predicts that the radius '
                 'of each ring will decrease to one quarter of its original value. Explain why the student is '
                 'wrong.'),
            Lines(3, 2),
        ]),
    ]),
    Part('b', [
        Text('Fig. 9.2 shows four energy levels of an isolated atom.'),
        Fig(330, 130, fig_9_2, 'Fig. 9.2'),
        Text('Atoms of a gas are excited so that some of their electrons are in the –1.6 eV energy level.'),
        Sub('i', [
            Text('State the number of different wavelengths of photon that may be emitted as these electrons '
                 'return to the –10.4 eV level.'),
            Answer('number', '', 1),
        ]),
        Sub('ii', [
            Text('Determine the longest wavelength of the emitted photons.'),
            Space(7),
            Answer('wavelength', 'm', 2),
        ]),
    ]),
    Part('c', [
        Text('A nucleus of uranium-235 absorbs a slow-moving neutron and undergoes fission according to the '
             'equation'),
        Eq(_nuc(235, 92, 'U'), ' + ', _nuc(1, 0, 'n'), '  →  ', _nuc(141, 56, 'Ba'), ' + ', _nuc(92, 36, 'Kr'),
           ' + 3', _nuc(1, 0, 'n'), '.'),
        Text('Table 9.1 shows the binding energy per nucleon of each of the nuclei.'),
        Table([
            ['nucleus', 'binding energy per nucleon / MeV'],
            ['uranium-235', '7.59'],
            ['barium-141', '8.33'],
            ['krypton-92', '8.51'],
        ], [140, 220], 'Table 9.1'),
        Sub('i', [
            Text('Determine the energy, in MeV, released in this fission.'),
            Space(7),
            Answer('energy', 'MeV', 2),
        ]),
        Sub('ii', [
            Text('Explain, with reference to binding energy per nucleon, why the fusion of two light nuclei can '
                 'also release energy.'),
            Lines(2, 1),
        ]),
    ]),
])

MS9 = [
    MSRow('9(a)(i)', [
        ('<i>p</i> = √(2<i>m</i><sub>e</sub><i>eV</i>) = √(2 × 9.11 × 10<sup>–31</sup> × 1.60 × 10<sup>–19</sup> '
         '× 4000) = 3.4 × 10<sup>–23</sup> N s', 'C1'),
        ('<i>λ</i> = <i>h</i> / <i>p</i> = 6.63 × 10<sup>–34</sup> / 3.4 × 10<sup>–23</sup> = 1.9 × 10<sup>–11</sup> m',
         'A1'),
    ]),
    MSRow('9(a)(ii)', [
        ('<i>p</i> is proportional to √<i>V</i> so <i>λ</i> is proportional to 1 / √<i>V</i>: the wavelength '
         'halves (it does not decrease to one quarter)', 'B1'),
        ('angle of diffraction (approximately) proportional to wavelength, so the radius of each ring '
         '(approximately) halves', 'B1'),
    ]),
    MSRow('9(b)(i)', [
        ('6', 'B1'),
    ]),
    MSRow('9(b)(ii)', [
        ('longest wavelength from the smallest energy difference: –3.7 – (–5.5) = 1.8 eV', 'C1'),
        ('<i>λ</i> = <i>hc</i> / Δ<i>E</i> = (6.63 × 10<sup>–34</sup> × 3.00 × 10<sup>8</sup>) / (1.8 × 1.60 × '
         '10<sup>–19</sup>) = 6.9 × 10<sup>–7</sup> m', 'A1'),
    ], note='the 2.1 eV transition between the two highest levels (5.9 × 10<sup>–7</sup> m) scores 0'),
    MSRow('9(c)(i)', [
        ('binding energy of products = (141 × 8.33) + (92 × 8.51) = 1957 MeV<br/>'
         'binding energy of uranium-235 = 235 × 7.59 = 1784 MeV', 'C1'),
        ('energy released = 1957 – 1784 = 174 MeV', 'A1'),
    ], note='free neutrons have no binding energy'),
    MSRow('9(c)(ii)', [
        ('binding energy per nucleon increases with nucleon number for light nuclei, so the product nucleus has '
         'a greater (total) binding energy (and less mass) than the two light nuclei', 'B1'),
    ]),
]


# ================================================================== Question 10

def fig_10_1(c):
    cx, cy, R = 200, 100, 88
    for k in range(28):
        t = 2 * math.pi * k / 28
        c.saveState()
        c.translate(cx + R * math.cos(t), cy + R * math.sin(t))
        c.rotate(math.degrees(t))
        filled = k in (0, 14)
        rect(c, -5, -8, 12, 16, lw=0.75, fill=0.6 if filled else 1)
        c.restoreState()
    polyline(c, _ellipse(cx, cy, 62, 45), w=0.9)
    text(c, cx - 30, cy + 22, 'patient', anchor='c')
    d1, d2 = (cx - R - 1, cy), (cx + R + 1, cy)
    line(c, d1[0] + 5, cy, d2[0] - 5, cy, w=0.5, dash=[3, 2])
    ex = cx - 22
    dot(c, ex, cy, 2.5)
    arrow(c, ex - 4, cy + 0, ex - 40, cy, head=6)
    arrow(c, ex + 4, cy + 0, ex + 40, cy, head=6)
    text(c, ex - 24, cy + 7, 'γ', anchor='c')
    text(c, ex + 24, cy + 7, 'γ', anchor='c')
    dot(c, cx, cy, 1.8)
    text(c, cx + 3, cy - 14, 'M', anchor='c')
    text(c, d1[0] - 14, cy - 4, 'D<sub>1</sub>', anchor='r')
    text(c, d2[0] + 14, cy - 4, 'D<sub>2</sub>')
    text(c, cx + R + 6, cy + R - 14, 'ring of detectors')


def fig_10_2(c):
    x0, x1 = 90, 410
    lo, hi = 600, 720
    X = lambda l: x0 + (l - lo) / (hi - lo) * (x1 - x0)
    for k, (name, lam) in enumerate((('laboratory', 656.3), ('galaxy', 689.1))):
        yb = 92 - 38 * k
        rect(c, x0, yb, x1 - x0, 22, lw=0.75, fill=0.85)
        line(c, X(lam), yb, X(lam), yb + 22, w=2.0)
        text(c, x0 - 8, yb + 7, name, anchor='r')
    line(c, x0, 36, x1, 36)
    for l in range(lo, hi + 1, 20):
        line(c, X(l), 36, X(l), 32)
        text(c, X(l), 20, str(l), anchor='c')
    text(c, x1, 4, 'wavelength / nm', anchor='r')


Q10 = Question([
    Part('a', [
        Text('In positron emission tomography (PET scanning), a tracer containing a β<sup>+</sup> emitter is '
             'introduced into the body of a patient. Each emitted positron annihilates with an electron in the '
             'tissue, producing two gamma-ray photons.'),
        Sub('i', [
            Text('Explain why the two photons travel in opposite directions.'),
            Lines(3, 2),
        ]),
        Sub('ii', [
            Text('The two photons from one annihilation event are detected by detectors D<sub>1</sub> and '
                 'D<sub>2</sub> in a ring of detectors around the patient, as shown in Fig. 10.1. Point M is the '
                 'midpoint of the line joining D<sub>1</sub> and D<sub>2</sub>.'),
            Fig(400, 200, fig_10_1, 'Fig. 10.1'),
            Text('One photon arrives at D<sub>1</sub> 0.40 ns before the other photon arrives at '
                 'D<sub>2</sub>.'),
            Text('Determine the distance of the point of annihilation from M.'),
            Space(7),
            Answer('distance', 'm', 2),
        ]),
    ]),
    Part('b', [
        Text('Light from a distant galaxy is observed from the Earth. Fig. 10.2 shows the position of one line '
             'in the spectrum of hydrogen measured in a laboratory and in the light received from the galaxy.'),
        Fig(440, 120, fig_10_2, 'Fig. 10.2'),
        Text('The wavelength of the line is 656.3 nm in the laboratory and 689.1 nm in the light from the '
             'galaxy.'),
        Sub('i', [
            Text('Calculate the speed of the galaxy relative to the Earth.'),
            Space(7),
            Answer('speed', 'm s<sup>–1</sup>', 2),
        ]),
        Sub('ii', [
            Text('The Hubble constant is 2.3 × 10<sup>–18</sup> s<sup>–1</sup>.'),
            Text('Calculate the distance of the galaxy from the Earth.'),
            Space(5),
            Answer('distance', 'm', 1),
        ]),
        Sub('iii', [
            Text('Assume that the galaxy has moved away from the Earth at a constant speed since the Big Bang.'),
            Text('Use your answers in (b)(i) and (b)(ii) to estimate the age of the Universe, in years.'),
            Space(6),
            Answer('age', 'years', 2),
        ]),
    ]),
])

MS10 = [
    MSRow('10(a)(i)', [
        ('(total) momentum of the positron and electron before annihilation is (approximately) zero', 'B1'),
        ('momentum is conserved, so the photons have equal and opposite momenta / a single photon would have '
         'non-zero momentum', 'B1'),
    ]),
    MSRow('10(a)(ii)', [
        ('difference in distances travelled = <i>c</i>Δ<i>t</i> = 3.00 × 10<sup>8</sup> × 0.40 × '
         '10<sup>–9</sup> = 0.12 m', 'C1'),
        ('distance from M = <i>c</i>Δ<i>t</i> / 2 = 0.060 m (on the D<sub>1</sub> side of M)', 'A1'),
    ], note='0.12 m scores 1 mark'),
    MSRow('10(b)(i)', [
        ('Δ<i>λ</i> / <i>λ</i> = <i>v</i> / <i>c</i>, where <i>λ</i> is the emitted (laboratory) wavelength', 'C1'),
        ('<i>v</i> = 3.00 × 10<sup>8</sup> × (689.1 – 656.3) / 656.3 = 1.50 × 10<sup>7</sup> m s<sup>–1</sup>',
         'A1'),
    ], note='689.1 nm in the denominator (1.43 × 10<sup>7</sup> m s<sup>–1</sup>) scores 1 mark'),
    MSRow('10(b)(ii)', [
        ('<i>d</i> = <i>v</i> / <i>H</i><sub>0</sub> = 1.50 × 10<sup>7</sup> / 2.3 × 10<sup>–18</sup> = '
         '6.5 × 10<sup>24</sup> m', 'B1'),
    ]),
    MSRow('10(b)(iii)', [
        ('time = <i>d</i> / <i>v</i> = 1 / <i>H</i><sub>0</sub> = 4.3 × 10<sup>17</sup> s', 'C1'),
        ('age = 4.3 × 10<sup>17</sup> / (3.16 × 10<sup>7</sup>) = 1.4 × 10<sup>10</sup> years', 'A1'),
    ], note='the speed and distance of the galaxy cancel: any galaxy that obeys Hubble\'s law gives the same '
            'estimate'),
]


# ================================================================== paper

def _tie_refs(blocks):
    """Keep "Fig. 2.2", "Table 3.1" and "t = 10 ms" together when a paragraph is wrapped."""
    for b in blocks:
        if isinstance(b, Text):
            b.rich = re.sub(r'(Fig\.|Table) (\d)', '\\1\u00a0\\2', b.rich)
            b.rich = re.sub(r'(</i>(?:<sub>[^<]*</sub>)?) = ', '\\1\u00a0=\u00a0', b.rich)
        elif isinstance(b, (Part, Sub)):
            _tie_refs(b.blocks)


for _q in (Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10):
    _tie_refs(_q.blocks)

MS = MS1 + MS2 + MS3 + MS4 + MS5 + MS6 + MS7 + MS8 + MS9 + MS10

PAPER = Paper(
    number=3,
    questions=[Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10],
    mark_scheme=MS,
)
