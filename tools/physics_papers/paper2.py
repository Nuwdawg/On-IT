"""9702 Paper 4 practice paper 2: content only (layout is done by engine.py).

Every numerical answer in the mark scheme was checked with a Python script.
Data and Formulae values are those printed in the 2025 papers
(g = 9.81, e = 1.60e-19, h = 6.63e-34, c = 3.00e8, k = 1.38e-23, R = 8.31 ...).
"""
import math

from engine import *
from figs import *

# ====================================================================== helpers


def fmt(v, dec=None):
    """Tick label with `dec` decimal places (default: as few as needed),
    minus as an en dash."""
    if dec is not None:
        s = '%.*f' % (dec, v)
        if float(s) == 0:
            s = '%.*f' % (dec, 0.0)
    elif abs(v - round(v)) < 1e-9:
        s = str(int(round(v)))
    else:
        s = ('%.2f' % v).rstrip('0').rstrip('.')
    return s.replace('-', '–')


def frange(a, b, step):
    out, k = [], 0
    while a + k * step <= b + 1e-9:
        out.append(a + k * step)
        k += 1
    return out


def grid_graph(c, gx, gy, xr, yr, xmajor, ymajor, xlabel, ylabel,
               xstep=None, ystep=None, xtop=False, ylabel_below=False, xdec=None, ydec=None):
    """Graph grid (5 minor squares per major square) with its tick labels on
    the outside edges, so that labels never sit on top of a plotted line.
    The heavy horizontal axis is drawn at zero when zero is in range."""
    nx = int(round((xr[1] - xr[0]) / xmajor * 5))
    ny = int(round((yr[1] - yr[0]) / ymajor * 5))
    g = Graph(c, gx, gy, nx * MINOR, ny * MINOR, xr=xr, yr=yr,
              xmajor=xmajor, ymajor=ymajor, axes=False)
    y0 = 0 if yr[0] <= 0 <= yr[1] else yr[0]
    ay = g.P(xr[0], y0)[1]
    line(c, gx, ay, gx + g.w, ay, w=1.0)
    line(c, gx, gy, gx, gy + g.h, w=1.0)
    edge = gy + g.h if xtop else gy
    for v in frange(xr[0], xr[1], xstep or xmajor):
        px = g.P(v, yr[0])[0]
        if xtop:
            line(c, px, edge, px, edge + 3)
            label(c, px, edge + 6, fmt(v, xdec), anchor='c')
        else:
            line(c, px, edge, px, edge - 3)
            label(c, px, edge - 13, fmt(v, xdec), anchor='c')
    tw = 0
    for v in frange(yr[0], yr[1], ystep or ymajor):
        py = g.P(xr[0], v)[1]
        line(c, gx, py, gx - 3, py)
        s = fmt(v, ydec)
        tw = max(tw, text_width(s))
        label(c, gx - 5, py - 3.9, s, anchor='r')
    if xtop:
        text(c, gx + g.w, edge + 21, xlabel, anchor='r')
    else:
        text(c, gx + g.w, edge - 27, xlabel, anchor='r')
    if ylabel_below:
        text(c, gx, gy - 27, ylabel, anchor='c')
    else:
        text(c, gx - tw - 10, gy + g.h * 0.62, ylabel, anchor='r')
    return g


def sketch_axes(c, ox, oy, w, h, xlabel, ylabel, origin='0'):
    """Plain axes for a sketch graph (no scale)."""
    line(c, ox, oy, ox + w, oy, w=1.0)
    line(c, ox, oy, ox, oy + h, w=1.0)
    if origin:
        text(c, ox - 4, oy - 12, origin, anchor='r')
    text(c, ox + w, oy - 15, xlabel, anchor='r')
    text(c, ox - 6, oy + h - 10, ylabel, anchor='r')


def dashed_circle(c, x, y, r, dash=(3, 2)):
    c.saveState()
    c.setLineWidth(0.75)
    c.setDash(*dash)
    c.circle(x, y, r, stroke=1, fill=0)
    c.restoreState()


def arc_pts(cx, cy, r, a0, a1, n=40, ry=None):
    ry = r if ry is None else ry
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def arc_arrow(c, cx, cy, r, a0, a1, ry=None, head=6):
    pts = arc_pts(cx, cy, r, a0, a1, ry=ry)
    polyline(c, pts[:-2])
    arrow(c, pts[-4][0], pts[-4][1], pts[-1][0], pts[-1][1], head=head)


def leader(c, x1, y1, x2, y2, s, anchor='l', dy=-4):
    """Label at (x1, y1) with a thin leader line to the point (x2, y2)."""
    text(c, x1, y1 + dy, s, anchor=anchor)
    if anchor == 'l':
        line(c, x1 - 3, y1, x2, y2, w=0.5)
    elif anchor == 'r':
        line(c, x1 + 3, y1, x2, y2, w=0.5)
    else:
        line(c, x1, y1 - 7, x2, y2, w=0.5)

# ================================================================== Question 1


def fig_1_1(c):
    ox, oy, r = 150, 86, 66
    dashed_circle(c, ox, oy, r)
    dot(c, ox, oy, 2)
    text(c, ox - 6, oy - 4, 'O', anchor='r')
    # T and B
    line(c, ox, oy + r - 4, ox, oy + r + 4)
    text(c, ox, oy + r + 8, 'T', anchor='c')
    line(c, ox, oy - r - 4, ox, oy - r + 4)
    text(c, ox, oy - r - 15, 'B', anchor='c')
    # ball and string
    a = math.radians(35)
    bx, by = ox + r * math.cos(a), oy + r * math.sin(a)
    line(c, ox, oy, bx - 6 * math.cos(a), by - 6 * math.sin(a), w=1.0)
    circle(c, bx, by, 6, fill=0.6)
    text(c, ox + 0.5 * r * math.cos(a) + 2, oy + 0.5 * r * math.sin(a) + 6, '<i>r</i>', anchor='r')
    leader(c, 250, 150, bx + 5, by + 4, 'ball')
    leader(c, 250, 100, ox + 0.72 * r * math.cos(a), oy + 0.72 * r * math.sin(a) - 1, 'string')
    # direction of motion (anticlockwise)
    arc_arrow(c, ox, oy, r + 11, 145, 200)


def fig_1_2(c):
    base = 22
    hatch(c, 10, base - 10, 380, 10)
    # ramp from the release point down to the ground
    top = 128
    ramp = [(24, top), (56, top)]
    for k in range(1, 41):
        x = 56 + 120 * k / 40
        ramp.append((x, base + (top - base) * (1 + math.cos(math.pi * (x - 56) / 120)) / 2))
    polyline(c, ramp, w=1.2)
    line(c, 176, base, 390, base, w=1.2)
    # loop
    lx, rl = 280, 46
    c.saveState()
    c.setLineWidth(1.2)
    c.circle(lx, base + rl, rl, stroke=1, fill=0)
    c.restoreState()
    dot(c, lx, base + rl, 1.8)
    a = math.radians(40)
    line(c, lx, base + rl, lx + rl * math.cos(a), base + rl + rl * math.sin(a))
    text(c, lx + 0.5 * rl * math.cos(a) - 2, base + rl + 0.5 * rl * math.sin(a) + 4, '<i>r</i>', anchor='r')
    # block
    rect(c, 30, top, 14, 10, fill=0.6)
    leader(c, 76, top + 16, 42, top + 8, 'block')
    # height h
    line(c, 24, top, 8, top, w=0.5, dash=[2, 2])
    darrow(c, 12, base, 12, top)
    text(c, 17, (base + top) / 2 - 4, '<i>h</i>')
    b = math.radians(25)
    leader(c, 352, 110, lx + rl * math.cos(b), base + rl + rl * math.sin(b), 'track')


Q1 = Question([
    Text('A small ball of mass <i>m</i> is attached to one end of a light inextensible string. The other '
         'end of the string is attached to a fixed point O. The ball moves in a vertical circle of radius '
         '<i>r</i> with centre O, as shown in Fig. 1.1.'),
    Fig(320, 172, fig_1_1, 'Fig. 1.1'),
    Text('Point T is at the top of the circle and point B is at the bottom of the circle. '
         'Air resistance is negligible.'),
    Part('a', [
        Text('Show that the minimum speed of the ball at T for which the string remains taut is '
             '√(<i>gr</i>), where <i>g</i> is the acceleration of free fall.'),
        Space(6),
        Mark(2),
    ]),
    Part('b', [
        Text('The ball passes through T with speed <i>v</i>. '
             'A student suggests that the tension in the string when the ball is at B is greater than the '
             'tension when the ball is at T by 2<i>mg</i>, because the weight of the ball acts towards O at T '
             'but away from O at B.'),
        Text('Determine, in terms of <i>m</i> and <i>g</i> only, the difference between the tension in the '
             'string at B and the tension in the string at T. Hence state whether the student is correct.'),
        Space(10),
        Answer('difference in tension', '', 3),
    ]),
    Part('c', [
        Text('The ball has mass 0.15 kg and the radius <i>r</i> of the circle is 0.60 m. The string breaks '
             'if the tension in it exceeds 12.0 N.'),
        Text('Determine the range of values of the speed of the ball at T for which the ball moves in a '
             'complete vertical circle without the string breaking.'),
        Space(10),
        Answer('minimum speed', 'm s<sup>–1</sup>'),
        Answer('maximum speed', 'm s<sup>–1</sup>', 3),
    ]),
    Part('d', [
        Text('The ball and string are replaced by a small block that slides without friction along a track. '
             'The track includes a vertical circular loop of radius <i>r</i>, as shown in Fig. 1.2.'),
        Fig(400, 146, fig_1_2, 'Fig. 1.2'),
        Text('The block is released from rest at a height <i>h</i> above the lowest point of the loop. '
             'A student suggests that the block will just reach the top of the loop if <i>h</i> = 2<i>r</i>.'),
        Text('Explain why the student is wrong and determine, in terms of <i>r</i>, the minimum value of '
             '<i>h</i> for which the block moves all the way round the loop.'),
        Space(8),
        Answer('minimum <i>h</i> =', '', 2),
    ]),
])

MS1 = [
    MSRow('1(a)', [
        ('at minimum speed, tension in string is zero, so weight provides the centripetal force:<br/>'
         '<i>mg</i> = <i>mv</i><sup>2</sup> / <i>r</i>', 'M1'),
        ('<i>v</i><sup>2</sup> = <i>gr</i> so <i>v</i> = √(<i>gr</i>)', 'A1'),
    ]),
    MSRow('1(b)', [
        ('at T: <i>T</i><sub>T</sub> + <i>mg</i> = <i>mv</i><sup>2</sup> / <i>r</i><br/>'
         'at B: <i>T</i><sub>B</sub> – <i>mg</i> = <i>mu</i><sup>2</sup> / <i>r</i>, where <i>u</i> is the '
         'speed at B', 'C1'),
        ('½<i>mu</i><sup>2</sup> = ½<i>mv</i><sup>2</sup> + <i>mg</i>(2<i>r</i>) so '
         '<i>u</i><sup>2</sup> = <i>v</i><sup>2</sup> + 4<i>gr</i>', 'C1'),
        ('<i>T</i><sub>B</sub> – <i>T</i><sub>T</sub> = <i>m</i>(<i>u</i><sup>2</sup> – <i>v</i><sup>2</sup>) / '
         '<i>r</i> + 2<i>mg</i> = 6<i>mg</i>, so the student is <b>not</b> correct', 'A1'),
    ], note='the difference does not depend on <i>v</i>'),
    MSRow('1(c)', [
        ('minimum speed = √(9.81 × 0.60) = 2.4 m s<sup>–1</sup>', 'B1'),
        ('greatest tension is at B:<br/><i>T</i><sub>T</sub> = 12.0 – 6 × 0.15 × 9.81 = 3.17 N<br/>'
         '<b>or</b><br/><i>u</i><sup>2</sup> = (12.0 – 0.15 × 9.81) × 0.60 / 0.15 = 42.1', 'C1'),
        ('<i>v</i><sup>2</sup> = (3.17 + 0.15 × 9.81) × 0.60 / 0.15 <b>or</b> '
         '<i>v</i><sup>2</sup> = 42.1 – 4 × 9.81 × 0.60<br/>maximum speed = 4.3 m s<sup>–1</sup>', 'A1'),
    ], note='12.0 N applied at T, giving 7.3 m s<sup>–1</sup>, scores B1 only'),
    MSRow('1(d)', [
        ('track can only push on the block (towards the centre), so the block must still have a speed of at '
         'least √(<i>gr</i>) at the top / cannot be at rest at the top', 'B1'),
        ('<i>mgh</i> = <i>mg</i>(2<i>r</i>) + ½<i>m</i>(<i>gr</i>) so <i>h</i> = 2.5<i>r</i>', 'B1'),
    ]),
]

# ================================================================== Question 2


def fig_2_1(c):
    gx, gy = 34, 40
    g = grid_graph(c, gx, gy, (0, 20), (-16, 0), 2, 2, '<i>r</i> / 10<sup>6</sup> m',
                   '<i>ϕ</i> / 10<sup>6</sup> J kg<sup>–1</sup>', xtop=True, ylabel_below=True)
    g.curve(lambda r: -60.0 / r, 4.0, 20.0, w=1.2)


Q2 = Question([
    Text('A planet may be considered to be an isolated uniform sphere of radius 4.0 × 10<sup>6</sup> m.'),
    Text('Fig. 2.1 shows the variation of the gravitational potential <i>ϕ</i> with distance <i>r</i> from '
         'the centre of the planet, for points at and above the surface of the planet.'),
    Fig(340, 296, fig_2_1, 'Fig. 2.1'),
    Part('a', [
        Text('Explain why the gravitational potential at every point in the field of the planet is negative.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('Use Fig. 2.1 to determine the gravitational field strength at a distance of '
             '8.0 × 10<sup>6</sup> m from the centre of the planet. Show your working on Fig. 2.1.'),
        Space(8),
        Answer('field strength', 'N kg<sup>–1</sup>', 2),
    ]),
    Part('c', [
        Text('The planet rotates about its axis once every 12.0 hours. A satellite of mass 250 kg is to be '
             'placed in an equatorial orbit so that it remains above the same point on the surface of '
             'the planet.'),
        Sub('i', [
            Text('Use Fig. 2.1 to show that the radius of the orbit is 1.4 × 10<sup>7</sup> m.'),
            Space(11),
            Mark(3),
        ]),
        Sub('ii', [
            Text('Determine the minimum energy needed to move the satellite from rest on the surface of the '
                 'planet into this orbit. Ignore the rotation of the planet.'),
            Space(12),
            Answer('energy', 'J', 3),
        ]),
    ]),
])

MS2 = [
    MSRow('2(a)', [
        ('(gravitational) potential is zero at infinity', 'B1'),
        ('force is attractive, so work is done <b>by</b> the field / energy is released when a mass moves '
         'from infinity to the point<br/><b>or</b><br/>work must be done <b>on</b> a mass to move it from the '
         'point to infinity', 'B1'),
    ]),
    MSRow('2(b)', [
        ('tangent drawn to the line at <i>r</i> = 8.0 × 10<sup>6</sup> m and field strength = (–) gradient', 'C1'),
        ('field strength = 0.94 N kg<sup>–1</sup>', 'A1'),
    ], note='allow 0.85–1.05 N kg<sup>–1</sup><br/>allow <i>g</i> = –<i>ϕ</i> / <i>r</i> = '
            '7.5 × 10<sup>6</sup> / 8.0 × 10<sup>6</sup> for both marks'),
    MSRow('2(c)(i)', [
        ('<i>GM</i> = –<i>ϕr</i> using a point on the line, e.g. 1.5 × 10<sup>7</sup> × 4.0 × 10<sup>6</sup> '
         '= 6.0 × 10<sup>13</sup> N m<sup>2</sup> kg<sup>–1</sup>', 'C1'),
        ('<i>GMm</i> / <i>r</i><sup>2</sup> = <i>mrω</i><sup>2</sup> with <i>ω</i> = 2π / (12.0 × 3600) '
         '= 1.45 × 10<sup>–4</sup> rad s<sup>–1</sup>', 'C1'),
        ('<i>r</i><sup>3</sup> = 6.0 × 10<sup>13</sup> / (1.45 × 10<sup>–4</sup>)<sup>2</sup> leading to '
         '<i>r</i> = 1.42 × 10<sup>7</sup> m', 'A1'),
    ]),
    MSRow('2(c)(ii)', [
        ('increase in gravitational potential energy = 250 × [(–4.2 × 10<sup>6</sup>) – (–1.5 × 10<sup>7</sup>)] '
         '= 2.7 × 10<sup>9</sup> J', 'C1'),
        ('kinetic energy in orbit = <i>GMm</i> / 2<i>r</i> = (6.0 × 10<sup>13</sup> × 250) / '
         '(2 × 1.42 × 10<sup>7</sup>) = 5.3 × 10<sup>8</sup> J', 'C1'),
        ('energy = 3.2 × 10<sup>9</sup> J', 'A1'),
    ], note='2.7 × 10<sup>9</sup> J (kinetic energy in orbit omitted) scores C1 only'),
]

# ================================================================== Question 3


def fig_3_1(c):
    x0, x1, y0, h = 70, 270, 16, 34
    # barrel (open at the right-hand end)
    line(c, x0, y0, x1, y0, w=1.0)
    line(c, x0, y0 + h, x1, y0 + h, w=1.0)
    line(c, x0, y0, x0, y0 + 11, w=1.0)
    line(c, x0, y0 + h, x0, y0 + h - 11, w=1.0)
    # nozzle and seal
    line(c, x0, y0 + 11, x0 - 22, y0 + 11, w=1.0)
    line(c, x0, y0 + h - 11, x0 - 22, y0 + h - 11, w=1.0)
    rect(c, x0 - 30, y0 + 7, 8, h - 14, fill=0.3)
    # piston and rod
    px = 190
    rect(c, px, y0 + 1, 10, h - 2, fill=0.6)
    rect(c, px + 10, y0 + h / 2 - 3, 120, 6, fill=1)
    rect(c, px + 130, y0 - 8, 6, h + 16, fill=0.6)
    arrow(c, px + 170, y0 + h / 2, px + 140, y0 + h / 2)
    text(c, px + 172, y0 + h / 2 - 4, 'push')
    text(c, 125, y0 + h / 2 - 4, 'air', anchor='c')
    leader(c, px - 40, y0 + h + 22, px + 4, y0 + h - 4, 'piston', anchor='r')
    leader(c, 20, y0 + h + 22, x0 - 26, y0 + h - 8, 'seal', anchor='c')


def fig_3_2(c):
    gx, gy = 72, 36
    g = grid_graph(c, gx, gy, (0, 160), (0, 300), 20, 50, '<i>V</i> / cm<sup>3</sup>', '<i>p</i> / kPa')
    g.curve(lambda v: 100 * (150.0 / v) ** 1.4, 75, 150, w=1.2)
    for v in (150, 75):
        px, py = g.P(v, 100 * (150.0 / v) ** 1.4)
        dot(c, px, py, 2.2)
    # direction of the change
    a, b = g.P(116, 100 * (150 / 116) ** 1.4), g.P(106, 100 * (150 / 106) ** 1.4)
    arrow(c, a[0], a[1], b[0], b[1], w=1.2, head=9)
    px, py = g.P(116, 100 * (150 / 116) ** 1.4)
    label(c, px + 6, py + 10, 'rapid compression')


Q3 = Question([
    Part('a', [
        Text('Ice cubes of total mass 150 g at a temperature of –18.0 °C are put into 200 g of water at a '
             'temperature of 30.0 °C in a vacuum flask. The flask has negligible heat capacity and no thermal '
             'energy is transferred between the contents of the flask and the surroundings.'),
        Text('The specific heat capacity of ice is 2.10 J g<sup>–1</sup> °C<sup>–1</sup> and the specific heat '
             'capacity of water is 4.18 J g<sup>–1</sup> °C<sup>–1</sup>. The specific latent heat of fusion of '
             'ice is 334 J g<sup>–1</sup>.'),
        Sub('i', [
            Text('Determine the temperature of the contents of the flask when thermal equilibrium is reached.'),
            Space(10),
            Answer('temperature', '°C', 3),
        ]),
        Sub('ii', [
            Text('Determine the mass of liquid water in the flask when thermal equilibrium is reached.'),
            Space(8),
            Answer('mass', 'g', 2),
        ]),
    ]),
    Part('b', [
        Text('Fig. 3.1 shows some air sealed in a syringe by a piston.'),
        Fig(360, 84, fig_3_1, 'Fig. 3.1'),
        Text('The air has an initial volume of 150 cm<sup>3</sup> and an initial pressure of 100 kPa. '
             'The piston is pushed in so rapidly that no thermal energy is transferred between the air and its '
             'surroundings. The volume of the air decreases to 75 cm<sup>3</sup>. The work done on the air '
             'during this compression is 12 J. The air may be assumed to be an ideal gas.'),
        Sub('i', [
            Text('A student states that the temperature of the air does not change during the compression, '
                 'because no thermal energy is supplied to the air. Use the first law of thermodynamics to '
                 'explain why the student is wrong.'),
            Lines(3, 2),
        ]),
        Sub('ii', [
            Text('Fig. 3.2 shows the variation with volume <i>V</i> of the pressure <i>p</i> of the air during '
                 'the rapid compression.'),
            Fig(330, 222, fig_3_2, 'Fig. 3.2'),
            Text('The air is returned to its initial state. It is then compressed slowly from 150 cm<sup>3</sup> '
                 'to 75 cm<sup>3</sup> so that its temperature remains constant. On Fig. 3.2, sketch the '
                 'variation of <i>p</i> with <i>V</i> for this slow compression.'),
            Mark(2),
        ]),
        Sub('iii', [
            Text('Use Fig. 3.2 to explain whether the thermal energy transferred during the slow compression is '
                 'greater than, equal to or less than 12 J. State the direction of this transfer of thermal '
                 'energy.'),
            Lines(3, 2),
        ]),
    ]),
])

MS3 = [
    MSRow('3(a)(i)', [
        ('energy to warm all the ice to 0 °C = 150 × 2.10 × 18.0 = 5670 J<br/>'
         '<b>and</b> energy to melt all the ice = 150 × 334 = 50 100 J', 'M1'),
        ('energy released by the water cooling to 0 °C = 200 × 4.18 × 30.0 = 25 100 J', 'M1'),
        ('25 100 J &lt; 55 800 J, so not all of the ice melts and temperature = 0 °C', 'A1'),
    ], note='allow: equation assuming all the ice melts gives –21.0 °C (M1 M1), recognised as impossible for '
            'liquid water, so temperature = 0 °C (A1)'),
    MSRow('3(a)(ii)', [
        ('mass of ice melted = (25 080 – 5670) / 334 = 58.1 g', 'C1'),
        ('mass of water = 200 + 58.1 = 258 g', 'A1'),
    ]),
    MSRow('3(b)(i)', [
        ('<i>q</i> = 0 and work done on air = +12 J, so increase in internal energy = <i>q</i> + <i>W</i> '
         '= +12 J', 'B1'),
        ('internal energy of an ideal gas is the total kinetic energy of its molecules, which is proportional to '
         'thermodynamic temperature, so the temperature increases', 'B1'),
    ]),
    MSRow('3(b)(ii)', [
        ('curve starting at (150 cm<sup>3</sup>, 100 kPa) and lying below the given line', 'B1'),
        ('curve ending at (75 cm<sup>3</sup>, 200 kPa)', 'B1'),
    ]),
    MSRow('3(b)(iii)', [
        ('temperature constant so increase in internal energy is zero; thermal energy is transferred '
         '<b>from</b> the air (to the surroundings) and is equal to the work done on the air', 'B1'),
        ('work done = area under the <i>p</i>–<i>V</i> line, which is smaller for the slow compression, so the '
         'thermal energy transferred is less than 12 J', 'B1'),
    ], note='(the value is about 10 J)'),
]

# ================================================================== Question 4


def fig_4_1(c):
    cx, cy, r = 110, 126, 56
    a0, a1 = -48, 228
    pts = arc_pts(cx, cy, r, a0, a1, n=80)
    throat_l, throat_r = (98, 52), (122, 52)
    polyline(c, [throat_r] + pts + [throat_l], w=1.0)
    # gores
    for k in (-0.55, 0, 0.55):
        q = [(cx + r * k * math.sin(math.radians(t)) * 0.9, cy + r * math.cos(math.radians(t)))
             for t in range(-90, 91, 10)]
        polyline(c, [(x, y) for x, y in q if y > 92], w=0.4)
    # burner and flame
    rect(c, 104, 33, 12, 7, fill=0.6)
    polyline(c, [(107, 40), (110, 48), (113, 40)], w=0.6)
    # basket and ropes
    rect(c, 91, 4, 38, 20, fill=None)
    hatch(c, 91, 4, 38, 20, spacing=5)
    line(c, throat_l[0], throat_l[1], 91, 24, w=0.6)
    line(c, throat_r[0], throat_r[1], 129, 24, w=0.6)
    line(c, 106, 33, 101, 24, w=0.5)
    line(c, 114, 33, 119, 24, w=0.5)
    leader(c, 200, 166, 155, 160, 'envelope')
    leader(c, 200, 64, 123, 54, 'opening')
    leader(c, 200, 40, 117, 37, 'burner')
    leader(c, 200, 14, 130, 14, 'basket')


Q4 = Question([
    Part('a', [
        Text('The pressure <i>p</i> of an ideal gas is given by'),
        Eq('<i>p</i> = ', Frac('1', '3', small=True), Frac('<i>Nm</i>', '<i>V</i>'), ' ⟨<i>c</i><sup>2</sup>⟩'),
        Text('where the symbols have their usual meanings. Use this equation to show that the mean '
             'translational kinetic energy of a molecule of an ideal gas is (3/2)<i>kT</i>, where <i>k</i> is the '
             'Boltzmann constant and <i>T</i> is the thermodynamic temperature of the gas.'),
        Space(6),
        Mark(2),
    ]),
    Part('b', [
        Text('Air consists mainly of nitrogen molecules, each of mass 28.0 u, and oxygen molecules, each of '
             'mass 32.0 u.'),
        Text('A student states that, in a sample of air, the oxygen molecules have a greater mean kinetic energy '
             'than the nitrogen molecules because each oxygen molecule has a greater mass.'),
        Sub('i', [
            Text('Explain why the student is wrong.'),
            Lines(2, 1),
        ]),
        Sub('ii', [
            Text('Calculate, for the sample of air, the ratio'),
            Eq(Frac('r.m.s. speed of the nitrogen molecules', 'r.m.s. speed of the oxygen molecules'), ' .'),
            Space(5),
            Answer('ratio', '', 1),
        ]),
    ]),
    Part('c', [
        Text('The envelope of a hot-air balloon has a fixed volume of 2800 m<sup>3</sup>. It is open at its '
             'base, so that the pressure of the air inside it is always equal to the atmospheric pressure of '
             '1.01 × 10<sup>5</sup> Pa. Initially, the air inside the envelope is at the same temperature as the air outside, 15 °C. '
             'A burner then heats the air inside the envelope to 100 °C. The molar mass of air is '
             '0.029 kg mol<sup>–1</sup>.'),
        Text('Fig. 4.1 shows the balloon.'),
        Fig(290, 182, fig_4_1, 'Fig. 4.1'),
        Sub('i', [
            Text('A student states that the pressure of the air inside the envelope increases as it is heated, '
                 'because <i>p</i> / <i>T</i> is constant for an ideal gas. Explain why the student is wrong.'),
            Lines(2, 1),
        ]),
        Sub('ii', [
            Text('Determine the mass of air that leaves the envelope as the air inside it is heated from 15 °C '
                 'to 100 °C.'),
            Space(10),
            Answer('mass', 'kg', 3),
        ]),
        Sub('iii', [
            Text('Use your answer to (c)(ii) to deduce the maximum total mass of the envelope, the basket, the '
                 'burner and the passengers that the balloon can lift when the air inside the envelope is at '
                 '100 °C. Explain your reasoning.'),
            Lines(2, None),
            Answer('maximum mass', 'kg', 1),
        ]),
    ]),
])

MS4 = [
    MSRow('4(a)', [
        ('<i>pV</i> = <i>NkT</i> so (1/3)<i>Nm</i>⟨<i>c</i><sup>2</sup>⟩ = <i>NkT</i>', 'M1'),
        ('½<i>m</i>⟨<i>c</i><sup>2</sup>⟩ = (3/2)<i>kT</i>', 'A1'),
    ]),
    MSRow('4(b)(i)', [
        ('mean kinetic energy = (3/2)<i>kT</i> depends only on (thermodynamic) temperature, which is the same '
         'for both, so the mean kinetic energies are equal', 'B1'),
    ]),
    MSRow('4(b)(ii)', [
        ('ratio = √(32.0 / 28.0) = 1.07', 'A1'),
    ]),
    MSRow('4(c)(i)', [
        ('envelope is open, so air leaves / amount of air inside decreases (and pressure stays atmospheric): '
         '<i>p</i> / <i>T</i> is constant only for a fixed amount of gas at constant volume', 'B1'),
    ]),
    MSRow('4(c)(ii)', [
        ('<i>n</i> = <i>pV</i> / <i>RT</i>: initially <i>n</i> = (1.01 × 10<sup>5</sup> × 2800) / (8.31 × 288) '
         '= 1.18 × 10<sup>5</sup> mol', 'C1'),
        ('finally <i>n</i> = (1.01 × 10<sup>5</sup> × 2800) / (8.31 × 373) = 9.12 × 10<sup>4</sup> mol', 'C1'),
        ('mass = (1.18 × 10<sup>5</sup> – 9.12 × 10<sup>4</sup>) × 0.029 = 780 kg', 'A1'),
    ], note='temperatures in °C score 0'),
    MSRow('4(c)(iii)', [
        ('upthrust is unchanged (weight of displaced cold air) but weight of air inside has decreased by the '
         'weight of 780 kg, so maximum mass = 780 kg', 'B1'),
    ], note='ecf (c)(ii)'),
]

# ================================================================== Question 5


def fig_5_1(c):
    ox, oy, r = 150, 104, 50
    th = 50
    circle(c, ox, oy, r, w=1.0)
    dot(c, ox, oy, 2)
    text(c, ox - 5, oy + 5, 'O', anchor='r')
    px, py = ox + r * math.cos(math.radians(th)), oy + r * math.sin(math.radians(th))
    line(c, ox, oy, px, py, w=0.9)
    dot(c, px, py, 3.2)
    text(c, px + 6, py + 2, 'P')
    text(c, ox + 0.5 * r * math.cos(math.radians(th)) - 4, oy + 0.5 * r * math.sin(math.radians(th)) + 3,
         '<i>r</i>', anchor='r')
    line(c, ox, oy, ox + r + 22, oy, w=0.5, dash=[3, 2])
    polyline(c, arc_pts(ox, oy, 17, 0, th, n=16), w=0.6)
    text(c, ox + 22, oy + 6, '<i>θ</i>')
    arc_arrow(c, ox, oy, r + 10, 105, 150)
    text(c, ox - 46, oy + 50, '<i>ω</i>', anchor='r')
    leader(c, 258, 58, ox + r * math.cos(math.radians(-30)) + 1, oy + r * math.sin(math.radians(-30)),
           'turntable')
    # light
    for x in (74, 112, 196, 234):
        arrow(c, x, 184, x, 162)
    text(c, 246, 174, 'parallel beam')
    text(c, 246, 161, 'of light')
    # screen
    sy = 26
    line(c, 50, sy, 290, sy, w=1.4)
    hatch(c, 50, sy - 8, 240, 8, spacing=4)
    text(c, 296, sy - 4, 'screen')
    line(c, px, py - 4, px, sy, w=0.5, dash=[3, 2])
    line(c, ox, oy - r, ox, sy, w=0.5, dash=[3, 2])
    rect(c, px - 3, sy, 6, 4, fill=0)
    text(c, px + 6, sy + 4, 'S')
    darrow(c, ox, sy + 14, px, sy + 14, head=5)
    text(c, (ox + px) / 2, sy + 19, '<i>x</i>', anchor='c')


def fig_5_3(c):
    gx, gy = 70, 34
    g = grid_graph(c, gx, gy, (0, 1.6), (-3, 3), 0.2, 1, '<i>t</i> / s', '<i>x</i> / cm', xdec=1)
    # second vertical scale, on the right, for the velocity of Y (5 cm s-1 per cm)
    rx = gx + g.w
    line(c, rx, gy, rx, gy + g.h, w=1.0)
    for v in range(-15, 16, 5):
        py = g.P(0, v / 5.0)[1]
        line(c, rx, py, rx + 3, py)
        label(c, rx + 5, py - 3.9, fmt(v))
    text(c, rx + 30, gy + g.h * 0.62, '<i>v</i> / cm s<sup>–1</sup>')
    g.curve(lambda t: 2.0 * math.sin(2 * math.pi * t / 0.8), 0, 1.6, w=1.2)
    g.curve(lambda t: 12.0 / 5.0 * math.cos(2 * math.pi * (t - 0.3) / 0.8), 0, 1.6, w=1.2)
    # curve labels above the grid, with leaders to the maxima
    for t0, y0, s in ((0.2, 2.0, '<i>x</i> of X'), (1.1, 2.4, '<i>v</i> of Y')):
        px, py = g.P(t0, y0)
        line(c, px, py + 2, px, gy + g.h + 8, w=0.5)
        text(c, px, gy + g.h + 11, s, anchor='c')


def fig_5_2(c):
    ox, oy, w, h = 46, 18, 250, 108
    sketch_axes(c, ox, oy, w, h, '<i>f</i>', '<i>A</i>')

    def amp(f):
        return 1.0 / math.sqrt((1 - f * f) ** 2 + (0.16 * f) ** 2)
    pk = max(amp(k / 1000) for k in range(500, 1500))
    sx, sy = w / 2.3, (h * 0.8) / pk
    pts = [(ox + sx * f, oy + sy * amp(f)) for f in [k / 400 for k in range(0, 921)]]
    polyline(c, pts, w=1.2)


Q5 = Question([
    Text('Fig. 5.1 is a view from above of a peg P fixed to the edge of a horizontal turntable of radius '
         '<i>r</i>.'),
    Fig(340, 186, fig_5_1, 'Fig. 5.1', note='(view from above)'),
    Text('The turntable rotates about its centre O with constant angular speed <i>ω</i>. A horizontal parallel '
         'beam of light casts a shadow S of the peg on a vertical screen. At the instant shown, the line OP '
         'makes an angle <i>θ</i> with a line through O that is parallel to the screen. The displacement of S '
         'from the point on the screen directly opposite O is <i>x</i>.'),
    Part('a', [
        Text('By considering the acceleration of P, explain why S moves with simple harmonic motion.'),
        Lines(4, 3),
    ]),
    Part('b', [
        Text('The angular speed of the turntable is doubled. State the factor by which the maximum acceleration '
             'of S increases.'),
        Answer('factor', '', 1),
    ]),
    Part('c', [
        Text('A mass on a spring is made to oscillate by a periodic driving force of frequency <i>f</i>. '
             'Fig. 5.2 shows the variation with <i>f</i> of the amplitude <i>A</i> of the oscillations when the '
             'damping is light.'),
        Fig(310, 130, fig_5_2, 'Fig. 5.2'),
        Text('On Fig. 5.2, sketch a line to show the variation with <i>f</i> of <i>A</i> when the damping is '
             'increased.'),
        Mark(2),
    ]),
    Part('d', [
        Text('Two oscillators X and Y have the same frequency. Fig. 5.3 shows the variation with time <i>t</i> '
             'of the displacement <i>x</i> of X and the variation with <i>t</i> of the velocity <i>v</i> of Y.'),
        Fig(400, 230, fig_5_3, 'Fig. 5.3'),
        Sub('i', [
            Text('Determine the phase difference between the displacement of X and the displacement of Y.'),
            Space(7),
            Answer('phase difference', '°', 2),
        ]),
        Sub('ii', [
            Text('Determine the amplitude of the oscillations of Y.'),
            Space(7),
            Answer('amplitude', 'cm', 2),
        ]),
    ]),
])

MS5 = [
    MSRow('5(a)', [
        ('P has (centripetal) acceleration <i>rω</i><sup>2</sup> directed towards O', 'B1'),
        ('acceleration of S is the component of this parallel to the screen: '
         '<i>rω</i><sup>2</sup> cos <i>θ</i> = <i>ω</i><sup>2</sup><i>x</i>, since <i>x</i> = <i>r</i> cos '
         '<i>θ</i>', 'B1'),
        ('<i>a</i> = –<i>ω</i><sup>2</sup><i>x</i> with <i>ω</i> constant: acceleration of S is proportional to '
         'its displacement and directed towards the equilibrium position / opposite to the displacement', 'B1'),
    ]),
    MSRow('5(b)', [
        ('4', 'B1'),
    ], note='maximum acceleration = <i>rω</i><sup>2</sup>'),
    MSRow('5(c)', [
        ('line below the given line at all frequencies, with a flatter (less sharp) peak', 'B1'),
        ('peak at the same or a slightly lower frequency, <b>not</b> a higher frequency', 'B1'),
    ]),
    MSRow('5(d)(i)', [
        ('displacement of Y is maximum a quarter of a period (0.20 s) after its velocity is maximum, i.e. at '
         '<i>t</i> = 0.50 s; displacement of X is maximum at <i>t</i> = 0.20 s', 'C1'),
        ('phase difference = (0.30 / 0.80) × 360° = 135°', 'A1'),
    ], note='allow 2.4 rad or 225°<br/>45° (velocity of Y treated as its displacement) scores 0'),
    MSRow('5(d)(ii)', [
        ('<i>v</i><sub>0</sub> = <i>ωx</i><sub>0</sub> with <i>ω</i> = 2π / 0.80 = 7.85 rad s<sup>–1</sup>', 'C1'),
        ('<i>x</i><sub>0</sub> = 12 / 7.85 = 1.5 cm', 'A1'),
    ]),
]

# ================================================================== Question 6


def fig_6_1(c):
    ax, bx, y = 90, 300, 30
    line(c, 20, y, 380, y, w=0.5, dash=[3, 3])
    circle(c, ax, y, 5, fill=0)
    circle(c, bx, y, 5, fill=0)
    text(c, ax - 10, y + 8, 'A', anchor='r')
    text(c, bx + 10, y + 8, 'B')
    text(c, ax, y - 20, '+8.0 nC', anchor='c')
    text(c, bx, y - 20, '–2.0 nC', anchor='c')
    line(c, ax, y + 9, ax, y + 40, w=0.5)
    line(c, bx, y + 9, bx, y + 40, w=0.5)
    darrow(c, ax, y + 34, bx, y + 34)
    text(c, (ax + bx) / 2, y + 39, '0.30 m', anchor='c')


def fig_6_2(c):
    s = 26.0                          # points per cm
    x0, L, d = 120, 6.0 * s, 2.5 * s
    yb = 40                           # top surface of the lower plate
    yt = yb + d                       # lower surface of the upper plate
    rect(c, x0, yb - 6, L, 6, fill=0.6)
    rect(c, x0, yt, L, 6, fill=0.6)
    text(c, x0 + L + 6, yt - 1, '+120 V')
    text(c, x0 + L + 6, yb - 7, '0 V')
    ym = (yb + yt) / 2
    # electron path (deflection exaggerated)
    defl = 12.0
    line(c, 72, ym, x0, ym, w=1.0)
    arrow(c, 72, ym, 96, ym)
    text(c, 72, ym + 6, 'electron')
    pts = [(x0 + L * k / 40, ym + defl * (k / 40) ** 2) for k in range(41)]
    polyline(c, pts, w=1.0)
    slope = 2 * defl / L
    line(c, x0 + L, ym + defl, 380, ym + defl + slope * (380 - x0 - L), w=1.0)
    # dimensions
    darrow(c, x0, yt + 18, x0 + L, yt + 18)
    line(c, x0, yt + 8, x0, yt + 22, w=0.5)
    line(c, x0 + L, yt + 8, x0 + L, yt + 22, w=0.5)
    text(c, x0 + L / 2, yt + 23, '6.0 cm', anchor='c')
    line(c, x0 - 4, yt, 40, yt, w=0.5, dash=[2, 2])
    line(c, x0 - 4, yb, 40, yb, w=0.5, dash=[2, 2])
    darrow(c, 48, yb, 48, yt)
    text(c, 42, ym - 4, '2.5 cm', anchor='r')


Q6 = Question([
    Part('a', [
        Text('Define electric field strength.'),
        Lines(2, 1),
    ]),
    Part('b', [
        Text('Two point charges A and B are separated by a distance of 0.30 m in a vacuum, as shown in '
             'Fig. 6.1.'),
        Fig(400, 84, fig_6_1, 'Fig. 6.1'),
        Text('The charge of A is +8.0 nC and the charge of B is –2.0 nC.'),
        Sub('i', [
            Text('Determine the distance from A of the point on the line through A and B at which the electric '
                 'field strength is zero.'),
            Space(10),
            Answer('distance', 'm', 3),
        ]),
        Sub('ii', [
            Text('Calculate the electric potential at the point in (b)(i).'),
            Space(7),
            Answer('potential', 'V', 2),
        ]),
    ]),
    Part('c', [
        Text('Electrons are accelerated from rest through a potential difference (p.d.) of 1500 V. They then '
             'enter the region between two horizontal metal plates, midway between the plates, as shown in '
             'Fig. 6.2.'),
        Fig(400, 146, fig_6_2, 'Fig. 6.2', note='(not to scale)'),
        Text('The plates have length 6.0 cm and are separated by 2.5 cm. The p.d. between the plates is '
             '120 V. The electrons enter the region between the plates with speed '
             '2.30 × 10<sup>7</sup> m s<sup>–1</sup> in a direction parallel to the plates. Assume that the '
             'electric field is uniform between the plates and zero outside them.'),
        Sub('i', [
            Text('Determine the vertical distance moved by an electron while it is between the plates.'),
            Space(11),
            Answer('distance', 'm', 3),
        ]),
        Sub('ii', [
            Text('The electrons are replaced by protons that are accelerated from rest through the same p.d. of '
                 '1500 V and then enter the region between the plates at the same point.'),
            Text('A student suggests that the protons will be deflected much less than the electrons, because '
                 'the mass of a proton is much greater than the mass of an electron.'),
            Text('Explain why the student is wrong, and describe the deflection of the protons.'),
            Lines(4, 2),
        ]),
    ]),
])

MS6 = [
    MSRow('6(a)', [
        ('force per unit positive charge', 'B1'),
    ]),
    MSRow('6(b)(i)', [
        ('fields of A and B are in opposite directions only outside AB, and the point must be nearer the '
         'smaller charge, so it is beyond B', 'B1'),
        ('8.0 / <i>x</i><sup>2</sup> = 2.0 / (<i>x</i> – 0.30)<sup>2</sup>', 'C1'),
        ('<i>x</i> = 0.60 m', 'A1'),
    ], note='0.20 m (a point between A and B) scores 0'),
    MSRow('6(b)(ii)', [
        ('<i>V</i> = <i>Q</i> / 4π<i>ε</i><sub>0</sub><i>r</i> for each charge, with the potentials added as '
         'scalars', 'C1'),
        ('<i>V</i> = 8.99 × 10<sup>9</sup> × [(8.0 × 10<sup>–9</sup> / 0.60) – (2.0 × 10<sup>–9</sup> / 0.30)] '
         '= 60 V', 'A1'),
    ], note='ecf (b)(i)'),
    MSRow('6(c)(i)', [
        ('<i>E</i> = 120 / 0.025 = 4800 V m<sup>–1</sup> and <i>a</i> = <i>eE</i> / <i>m</i> = '
         '8.4 × 10<sup>14</sup> m s<sup>–2</sup>', 'C1'),
        ('<i>t</i> = 0.060 / 2.30 × 10<sup>7</sup> = 2.6 × 10<sup>–9</sup> s', 'C1'),
        ('distance = ½<i>at</i><sup>2</sup> = 2.9 × 10<sup>–3</sup> m', 'A1'),
    ]),
    MSRow('6(c)(ii)', [
        ('deflection = ½(<i>qE</i> / <i>m</i>)(<i>L</i> / <i>v</i>)<sup>2</sup> and ½<i>mv</i><sup>2</sup> = '
         '<i>qV</i>, so deflection = <i>EL</i><sup>2</sup> / 4<i>V</i>, which does not depend on the mass '
         '(or charge) of the particle', 'B1'),
        ('protons are deflected by the same distance (2.9 × 10<sup>–3</sup> m) but in the opposite direction '
         '(towards the 0 V plate)', 'B1'),
    ]),
]

# ================================================================== Question 7


def fig_7_1(c):
    top, bot = 150, 24
    # battery
    bx = 40
    wire(c, [(bx, 100), (bx, top), (122, top)])
    cell(c, bx, 100, bx, 64)
    wire(c, [(bx, 64), (bx, bot), (330, bot)])
    text(c, bx - 14, 78, '12.0 V', anchor='r')
    # two-way switch: contacts 1 and 2, pivot below them
    c1, c2, pv = (122, top), (178, top), (150, 120)
    for p in (c1, c2, pv):
        circle(c, p[0], p[1], 2.2, fill=1)
    line(c, pv[0], pv[1] + 2, 125, top - 6, w=1.0)
    text(c, c1[0], top + 8, '1', anchor='c')
    text(c, c2[0], top + 8, '2', anchor='c')
    text(c, pv[0] + 8, pv[1] - 2, 'S')
    # X
    wire(c, [(150, 118), (150, 96)])
    capacitor(c, 150, 96, 150, 64)
    wire(c, [(150, 64), (150, bot)])
    text(c, 136, 76, 'X', anchor='r')
    # R and Y
    wire(c, [(180, top), (220, top)])
    resistor(c, 220, top, 280, top, label='<i>R</i>')
    wire(c, [(280, top), (330, top), (330, 96)])
    capacitor(c, 330, 96, 330, 64)
    wire(c, [(330, 64), (330, bot)])
    text(c, 344, 76, 'Y')
    dot(c, 150, bot, 2)


def fig_7_2(c):
    g = grid_graph(c, 74, 40, (0, 20), (-0.4, 2.0), 2, 0.4, '<i>t</i> / s', 'ln (<i>V</i> / V)')
    g.line(0, math.log(6.0), 20, math.log(6.0) - 20 / 9.4, w=1.2)


Q7 = Question([
    Part('a', [
        Text('Define capacitance.'),
        Lines(2, 1),
    ]),
    Part('b', [
        Text('Fig. 7.1 shows a circuit containing two identical capacitors X and Y, each of capacitance '
             '<i>C</i>, a resistor of resistance <i>R</i>, a two-way switch S and a battery of electromotive '
             'force (e.m.f.) 12.0 V and negligible internal resistance.'),
        Fig(380, 170, fig_7_1, 'Fig. 7.1'),
        Text('Capacitor Y is initially uncharged. Switch S is first moved to position 1, so that X becomes fully '
             'charged. S is then moved to position 2. Charge flows until the potential difference (p.d.) across '
             'X is equal to the p.d. across Y.'),
        Sub('i', [
            Text('Show that the final p.d. across each capacitor is 6.0 V.'),
            Space(5),
            Mark(1),
        ]),
        Sub('ii', [
            Text('Show that half of the energy that was stored in X before S was moved to position 2 is '
                 'dissipated in the resistor.'),
            Space(8),
            Mark(2),
        ]),
        Sub('iii', [
            Text('A student suggests that less energy would be dissipated if a resistor of much smaller '
                 'resistance were used. Explain why the student is wrong.'),
            Lines(3, 2),
        ]),
    ]),
    Part('c', [
        Text('After the current has fallen to zero, X and Y are disconnected from the rest of the circuit, '
             'while still connected to each other. They are then discharged together through a resistor of '
             'resistance 10.0 kΩ.'),
        Text('Fig. 7.2 shows the variation with time <i>t</i> of ln (<i>V</i> / V), where <i>V</i> is the p.d. '
             'across X during this discharge.'),
        Fig(380, 236, fig_7_2, 'Fig. 7.2'),
        Text('Use Fig. 7.2 to determine the capacitance <i>C</i> of X.'),
        Space(11),
        Answer('<i>C</i>', 'μF', 3),
    ]),
])

MS7 = [
    MSRow('7(a)', [
        ('charge per unit potential difference', 'B1'),
    ], note='allow (ratio of) charge to potential difference'),
    MSRow('7(b)(i)', [
        ('charge is conserved: charge 12.0<i>C</i> is shared by a total capacitance 2<i>C</i>, so '
         '<i>V</i> = 12.0<i>C</i> / 2<i>C</i> = 6.0 V', 'B1'),
    ]),
    MSRow('7(b)(ii)', [
        ('initial energy = ½<i>C</i> × 12.0<sup>2</sup> = 72<i>C</i> <b>and</b> final energy = 2 × ½<i>C</i> × '
         '6.0<sup>2</sup> = 36<i>C</i>', 'M1'),
        ('energy dissipated = 72<i>C</i> – 36<i>C</i> = 36<i>C</i>, which is half of the initial energy', 'A1'),
    ]),
    MSRow('7(b)(iii)', [
        ('final p.d.s, and so the final stored energy, are fixed by conservation of charge alone and do not '
         'depend on the resistance', 'B1'),
        ('so the same energy (half) is dissipated: a smaller resistance gives a larger current for a shorter '
         'time', 'B1'),
    ]),
    MSRow('7(c)', [
        ('gradient = –1 / <i>τ</i>, e.g. (–0.34 – 1.79) / 20 = –0.106 s<sup>–1</sup>, so <i>τ</i> = 9.4 s', 'C1'),
        ('X and Y in parallel: <i>τ</i> = <i>R</i> × 2<i>C</i>', 'C1'),
        ('<i>C</i> = 9.4 / (2 × 10.0 × 10<sup>3</sup>) = 4.7 × 10<sup>–4</sup> F = 470 μF', 'A1'),
    ], note='allow 450–490 μF<br/>940 μF (total capacitance) scores C1 only'),
]

# ================================================================== Question 8


def fig_8_1(c):
    rect(c, 20, 40, 64, 116, fill=0.85)
    rect(c, 300, 40, 64, 116, fill=0.85)
    text(c, 52, 92, '<b>N</b>', anchor='c')
    text(c, 332, 92, '<b>S</b>', anchor='c')
    for y in (52, 80, 116, 144):
        arrow(c, 86, y, 298, y, head=6)
    # coil, in the plane of the page
    c.saveState()
    c.setLineWidth(1.6)
    c.rect(150, 64, 84, 68, stroke=1, fill=0)
    c.restoreState()
    # axis of rotation
    line(c, 192, 22, 192, 186, w=0.6, dash=[5, 3])
    arc_arrow(c, 192, 176, 26, 210, 510, ry=6)
    text(c, 226, 186, 'axis of rotation')
    leader(c, 262, 20, 228, 64, 'coil')
    text(c, 192, 6, 'uniform magnetic field', anchor='c')


def fig_8_2(c):
    y1, y2 = 66, 24
    rect(c, 20, 14, 64, 62)
    text(c, 52, 41, 'coil', anchor='c')
    line(c, 84, y1, 330, y1, w=1.0)
    line(c, 84, y2, 330, y2, w=1.0)
    wire(c, [(330, y1), (352, y1)])
    resistor(c, 352, y1, 352, y2)
    wire(c, [(352, y2), (330, y2)])
    text(c, 364, (y1 + y2) / 2 - 4, '8.0 Ω')
    leader(c, 200, 86, 200, y1 + 1, 'leads', anchor='c')
    line(c, 200, y2 + 1, 200, y1 - 1, w=0.5)


Q8 = Question([
    Text('Fig. 8.1 shows a flat rectangular coil in a uniform magnetic field between the poles of a magnet.'),
    Fig(380, 196, fig_8_1, 'Fig. 8.1'),
    Text('The coil rotates with constant angular speed about an axis that is perpendicular to the magnetic '
         'field. At the instant shown, the plane of the coil is parallel to the magnetic field.'),
    Part('a', [
        Text('State Faraday’s law of electromagnetic induction.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('A student states that the electromotive force (e.m.f.) induced in the coil is zero at the instant '
             'shown in Fig. 8.1, because no magnetic flux passes through the coil at this instant.'),
        Text('Explain why the student is wrong.'),
        Lines(3, 2),
    ]),
    Part('c', [
        Text('The ends of the coil are connected to a resistor of resistance 8.0 Ω. The e.m.f. <i>E</i>, in V, '
             'induced in the coil varies with time <i>t</i>, in s, according to the equation'),
        Eq('<i>E</i> = 25 sin (120π<i>t</i>).'),
        Text('The coil has negligible resistance.'),
        Sub('i', [
            Text('Calculate the mean power dissipated in the resistor.'),
            Space(7),
            Answer('mean power', 'W', 2),
        ]),
        Sub('ii', [
            Text('The angular speed of the coil is doubled. Determine the new mean power dissipated in the '
                 'resistor.'),
            Space(7),
            Answer('mean power', 'W', 2),
        ]),
    ]),
    Part('d', [
        Text('The coil is connected to the resistor by two long straight leads that are parallel to each other '
             'and close together, as shown in Fig. 8.2.'),
        Fig(400, 96, fig_8_2, 'Fig. 8.2'),
        Sub('i', [
            Text('Explain why the magnetic force between the two leads is always repulsive, even though the '
                 'current in the leads is alternating.'),
            Lines(2, 1),
        ]),
        Sub('ii', [
            Text('For the e.m.f. in (c), state the frequency with which the magnitude of the force between the '
                 'leads varies.'),
            Answer('frequency', 'Hz', 1),
        ]),
    ]),
])

MS8 = [
    MSRow('8(a)', [
        ('(magnitude of) induced e.m.f. is proportional to', 'M1'),
        ('rate of change of (magnetic) flux linkage', 'A1'),
    ]),
    MSRow('8(b)', [
        ('flux linkage is zero but its rate of change is maximum (at this instant)', 'B1'),
        ('the sides of the coil are moving perpendicular to the field / cutting the field lines at the greatest '
         'rate, so the e.m.f. is maximum', 'B1'),
    ]),
    MSRow('8(c)(i)', [
        ('mean power = <i>E</i><sub>0</sub><sup>2</sup> / 2<i>R</i> <b>or</b> <i>E</i><sub>r.m.s.</sub> = '
         '25 / √2 = 17.7 V', 'C1'),
        ('mean power = 25<sup>2</sup> / (2 × 8.0) = 39 W', 'A1'),
    ], note='78 W scores 0'),
    MSRow('8(c)(ii)', [
        ('rate of change of flux linkage doubles, so peak e.m.f. doubles to 50 V', 'C1'),
        ('mean power = 50<sup>2</sup> / (2 × 8.0) = 160 W', 'A1'),
    ], note='allow 156 W; allow 4 × (c)(i)<br/>39 W (only the frequency changes) scores 0'),
    MSRow('8(d)(i)', [
        ('currents in the two leads are always in opposite directions: when the current reverses, it reverses '
         'in both leads (field and current both reverse), so the force does not change direction', 'B1'),
    ]),
    MSRow('8(d)(ii)', [
        ('120 Hz', 'B1'),
    ]),
]

# ================================================================== Question 9

LMIN, KB, KA = 4.44, 6.375, 7.144          # wavelengths / 10^-11 m


def spectrum(lam):
    if lam <= LMIN:
        return 0.0
    cont = (lam / LMIN - 1) / lam ** 2 * math.exp(-(lam / 11.0) ** 3)
    peaks = 0.012 * math.exp(-((lam - KA) / 0.11) ** 2) + 0.008 * math.exp(-((lam - KB) / 0.11) ** 2)
    return cont + peaks


def fig_9_1(c):
    ox, oy, w, h = 46, 24, 300, 156
    sketch_axes(c, ox, oy, w, h, 'wavelength', 'intensity')
    sx = 14.0
    peak = max(spectrum(k / 200) for k in range(800, 2000))
    sy = (h * 0.44) / peak
    pts = [(ox + sx * (k / 200), oy + sy * spectrum(k / 200)) for k in range(int(LMIN * 200), 20 * 200 + 1)]
    polyline(c, [(ox + sx * LMIN, oy)] + pts, w=1.1)
    line(c, ox + sx * LMIN, oy, ox + sx * LMIN, oy - 4)
    text(c, ox + sx * LMIN, oy - 15, 'λ<sub>min</sub>', anchor='c')
    text(c, ox + sx * KA + 3, oy + sy * spectrum(KA) + 2, 'P')
    text(c, ox + sx * KB - 3, oy + sy * spectrum(KB) + 2, 'Q', anchor='r')


def fig_9_2(c):
    x0, x1 = 60, 220
    levels = [(144, '0'), (124, '–0.5 keV'), (100, '–2.6 keV'), (12, '–20.0 keV')]
    for y, s in levels:
        line(c, x0, y, x1, y, w=1.0)
        text(c, x1 + 8, y - 4, s)
    arrow(c, 110, 100, 110, 13, head=7)
    text(c, 104, 52, 'P', anchor='r')
    arrow(c, 170, 124, 170, 13, head=7)
    text(c, 176, 64, 'Q')


Q9 = Question([
    Text('X-rays are produced when electrons that have been accelerated from rest through a potential '
         'difference (p.d.) strike a molybdenum target.'),
    Text('Fig. 9.1 shows the spectrum of the X-rays produced when the accelerating p.d. is 28.0 kV.'),
    Fig(360, 184, fig_9_1, 'Fig. 9.1'),
    Text('The spectrum consists of a continuous range of wavelengths, with a minimum wavelength '
         'λ<sub>min</sub>, together with two sharp peaks P and Q.'),
    Part('a', [
        Text('Explain why there is a minimum wavelength.'),
        Lines(2, 1),
    ]),
    Part('b', [
        Text('Calculate λ<sub>min</sub>.'),
        Space(6),
        Answer('λ<sub>min</sub>', 'm', 2),
    ]),
    Part('c', [
        Text('The current in the X-ray tube is doubled. The accelerating p.d. is unchanged.'),
        Text('On Fig. 9.1, sketch the spectrum of the X-rays that are now produced.'),
        Mark(2),
    ]),
    Part('d', [
        Text('Each sharp peak is produced when an incident electron removes an electron from the lowest energy '
             'level of a molybdenum atom in the target. An electron from a higher energy level then moves into '
             'the vacancy, emitting a photon.'),
        Text('Fig. 9.2 shows some of the energy levels of a molybdenum atom.'),
        Fig(320, 150, fig_9_2, 'Fig. 9.2', note='(not to scale)'),
        Text('The photons in peak P have energy 17.4 keV. A student suggests that peak P would still be '
             'produced if the accelerating p.d. were reduced to 18.0 kV, because each electron would then have '
             'enough energy to produce a photon of energy 17.4 keV.'),
        Text('Use Fig. 9.2 to explain why the student is wrong.'),
        Lines(3, 2),
    ]),
    Part('e', [
        Text('A different X-ray tube is used to produce an image of a limb. For the X-ray photons used, the '
             'half-value thickness (the thickness of material that halves the intensity of a parallel beam) is '
             '3.5 cm for soft tissue and 1.3 cm for bone.'),
        Text('Along path A through the limb, a parallel beam of X-rays passes through 7.0 cm of soft tissue only. '
             'Along path B, the beam passes through 2.0 cm of bone and 5.0 cm of soft tissue.'),
        Text('Determine the ratio'),
        Eq(Frac('intensity of X-rays emerging along path B', 'intensity of X-rays emerging along path A'), ' .'),
        Space(9),
        Answer('ratio', '', 3),
    ]),
])

MS9 = [
    MSRow('9(a)', [
        ('minimum wavelength (maximum photon energy) when all of the kinetic energy <i>eV</i> of one electron '
         'produces one photon', 'B1'),
    ]),
    MSRow('9(b)', [
        ('<i>eV</i> = <i>hc</i> / λ<sub>min</sub>', 'C1'),
        ('λ<sub>min</sub> = (6.63 × 10<sup>–34</sup> × 3.00 × 10<sup>8</sup>) / '
         '(1.60 × 10<sup>–19</sup> × 28.0 × 10<sup>3</sup>) = 4.44 × 10<sup>–11</sup> m', 'A1'),
    ]),
    MSRow('9(c)', [
        ('same λ<sub>min</sub>, with peaks P and Q at the same wavelengths', 'B1'),
        ('greater (about double) intensity at all wavelengths', 'B1'),
    ]),
    MSRow('9(d)', [
        ('for peak P there must be a vacancy in the lowest level, so an electron must first be removed from '
         'the –20.0 keV level', 'B1'),
        ('this needs (at least) 20.0 keV, but each electron would have only 18.0 keV', 'B1'),
    ]),
    MSRow('9(e)', [
        ('<i>μ</i> = ln 2 / <i>x</i><sub>½</sub>: <i>μ</i> = 0.198 cm<sup>–1</sup> (soft tissue) and '
         '0.533 cm<sup>–1</sup> (bone)<br/><b>or</b><br/>'
         'path A is 2.0 half-value thicknesses; path B is 1.54 + 1.43 half-value thicknesses', 'C1'),
        ('<i>I</i><sub>A</sub> / <i>I</i><sub>0</sub> = 0.25 <b>and</b> <i>I</i><sub>B</sub> / <i>I</i><sub>0</sub> '
         '= 0.128', 'C1'),
        ('ratio = 0.51', 'A1'),
    ]),
]

# ================================================================= Question 10


def semf(a):
    """Binding energy per nucleon / MeV (liquid-drop model) for the sketch."""
    z = a / (2 + 0.0155 * a ** (2 / 3))
    return (15.8 - 18.3 * a ** (-1 / 3) - 0.714 * z * (z - 1) / a ** (4 / 3)
            - 23.2 * (a - 2 * z) ** 2 / a ** 2)


def fig_10_1(c):
    ox, oy = 62, 30
    sx, sy = 1.1, 12.6
    line(c, ox, oy, ox + 250 * sx, oy, w=1.0)
    line(c, ox, oy, ox, oy + 10 * sy, w=1.0)
    for a in range(0, 251, 50):
        line(c, ox + a * sx, oy, ox + a * sx, oy - 3)
        text(c, ox + a * sx, oy - 13, str(a), anchor='c')
    for e in range(0, 11, 2):
        line(c, ox, oy + e * sy, ox - 3, oy + e * sy)
        text(c, ox - 5, oy + e * sy - 3.9, str(e), anchor='r')
    text(c, ox + 250 * sx, oy - 27, '<i>A</i>', anchor='r')
    text(c, ox - 22, oy + 7.3 * sy, '<i>E</i><sub>B</sub> / MeV', anchor='r')
    pts = [(ox + a * sx, oy + semf(a) * sy) for a in [2 + k * 0.25 for k in range(0, 993)]]
    polyline(c, pts, w=1.2)
    for a, name, dx, dy, anc in ((2, 'hydrogen-2', 8, -3, 'l'), (56, 'iron-56', 0, 9, 'c'),
                                 (235, 'uranium-235', 0, 9, 'c')):
        px, py = ox + a * sx, oy + semf(a) * sy
        dot(c, px, py, 2.4)
        text(c, px + dx, py + dy, name, anchor=anc)


def fig_10_2(c):
    g = grid_graph(c, 76, 34, (0, 24), (0, 600), 2, 100, '<i>t</i> / h', '<i>C</i> / min<sup>–1</sup>')
    g.curve(lambda t: 30 + 560 * 2 ** (-t / 6.0), 0, 24, w=1.2)


Q10 = Question([
    Part('a', [
        Text('Fig. 10.1 shows the variation with nucleon number <i>A</i> of the binding energy per nucleon '
             '<i>E</i><sub>B</sub> of nuclei.'),
        Fig(360, 164, fig_10_1, 'Fig. 10.1'),
        Text('A student suggests that, because energy is released when a nucleus of uranium-235 undergoes '
             'fission, energy must be absorbed when two nuclei of hydrogen-2 fuse, since fusion is the reverse '
             'of fission. Use Fig. 10.1 to explain why the student is wrong.'),
        Lines(3, 2),
    ]),
    Part('b', [
        Text('A sample of a radioactive isotope is placed near a detector. Fig. 10.2 shows the variation with '
             'time <i>t</i> of the count rate <i>C</i> recorded by the detector. The recorded count rate includes '
             'a background count rate of 30\u00a0min<sup>–1</sup>.'),
        Fig(440, 214, fig_10_2, 'Fig. 10.2'),
        Text('Use Fig. 10.2 to determine the half-life of the isotope.'),
        Space(8),
        Answer('half-life', 'h', 3),
    ]),
    Part('c', [
        Text('Type Ia supernovae are used as standard candles.'),
        Sub('i', [
            Text('State what is meant by a standard candle.'),
            Lines(2, 1),
        ]),
        Sub('ii', [
            Text('A type Ia supernova in a distant galaxy has a peak luminosity of 2.0 × 10<sup>36</sup> W. '
                 'The maximum radiant flux intensity received at the Earth from the supernova is '
                 '1.5 × 10<sup>–15</sup> W m<sup>–2</sup>. Determine the distance of the galaxy from the Earth.'),
            Space(7),
            Answer('distance', 'm', 2),
        ]),
        Sub('iii', [
            Text('A spectral line that has a wavelength of 656 nm when measured in a laboratory is observed in '
                 'the light from the galaxy to have a wavelength of 708 nm. Use your answer to (c)(ii) to '
                 'determine a value for the Hubble constant.'),
            Space(7),
            Answer('Hubble constant', 's<sup>–1</sup>', 2),
        ]),
    ]),
])

MS10 = [
    MSRow('10(a)', [
        ('fission of heavy nuclei and fusion of light nuclei both form nuclei with a greater binding energy per '
         'nucleon (closer to the peak near <i>A</i> = 56)', 'B1'),
        ('so in both processes the total binding energy increases / the total mass decreases and energy is '
         'released: fusion of light nuclei is not the reverse of fission of heavy nuclei', 'B1'),
    ]),
    MSRow('10(b)', [
        ('background subtracted: initial count rate from the isotope = 590 – 30 = 560 min<sup>–1</sup>', 'C1'),
        ('time for the corrected count rate to halve, e.g. 560 min<sup>–1</sup> to 280 min<sup>–1</sup> '
         '(recorded 310 min<sup>–1</sup>)', 'C1'),
        ('half-life = 6.0 h', 'A1'),
    ], note='allow 5.8–6.2 h<br/>6.5 h (background not subtracted) scores 0'),
    MSRow('10(c)(i)', [
        ('(astronomical) object of known luminosity', 'B1'),
    ]),
    MSRow('10(c)(ii)', [
        ('<i>F</i> = <i>L</i> / 4π<i>d</i><sup>2</sup>', 'C1'),
        ('<i>d</i> = [2.0 × 10<sup>36</sup> / (4π × 1.5 × 10<sup>–15</sup>)]<sup>½</sup> = '
         '1.0 × 10<sup>25</sup> m', 'A1'),
    ]),
    MSRow('10(c)(iii)', [
        ('<i>v</i> = <i>c</i>Δλ / λ = 3.00 × 10<sup>8</sup> × 52 / 656 = 2.4 × 10<sup>7</sup> m s<sup>–1</sup>', 'C1'),
        ('<i>H</i><sub>0</sub> = <i>v</i> / <i>d</i> = 2.3 × 10<sup>–18</sup> s<sup>–1</sup>', 'A1'),
    ], note='ecf (c)(ii)'),
]

# ====================================================================== paper

MS = MS1 + MS2 + MS3 + MS4 + MS5 + MS6 + MS7 + MS8 + MS9 + MS10

PAPER = Paper(
    number=2,
    questions=[Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10],
    mark_scheme=MS,
)
