"""Drawing helpers for figures, in the style of Cambridge question papers.

Every function takes the reportlab canvas first. Coordinates are points with
the origin at the bottom-left of the figure box (the engine translates).
"""
import math

from richtext import draw_rich, runs, runs_width

__all__ = ['text', 'label', 'line', 'polyline', 'arrow', 'darrow', 'circle', 'rect', 'hatch',
           'spring', 'dot', 'resistor', 'capacitor', 'cell', 'switch', 'diode', 'lamp',
           'meter', 'ac_supply', 'wire', 'Graph', 'MINOR', 'text_width']

MINOR = 5.67            # 2 mm grid square in points


def text(c, x, y, s, size=11, anchor='l', bold=False, italic=False):
    """Rich-text label with its baseline at y."""
    c.saveState()
    c.setFillGray(0)
    w = draw_rich(c, x, y, s, size, anchor, bold, italic)
    c.restoreState()
    return w


def label(c, x, y, s, size=11, anchor='l', pad=1.2):
    """Text on a white knock-out box, for labels that sit on a grid."""
    w = text_width(s, size)
    x0 = x - w / 2 if anchor == 'c' else (x - w if anchor == 'r' else x)
    c.saveState()
    c.setFillGray(1)
    c.rect(x0 - pad, y - size * 0.25, w + 2 * pad, size * 1.05, stroke=0, fill=1)
    c.restoreState()
    return text(c, x, y, s, size=size, anchor=anchor)


def text_width(s, size=11):
    return runs_width(runs(s, size))


def line(c, x1, y1, x2, y2, w=0.75, dash=None):
    c.saveState()
    c.setLineWidth(w)
    if dash:
        c.setDash(dash)
    c.line(x1, y1, x2, y2)
    c.restoreState()


def polyline(c, pts, w=0.75, close=False, fill=None, dash=None):
    c.saveState()
    c.setLineWidth(w)
    c.setLineJoin(1)
    if dash:
        c.setDash(dash)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    if fill is not None:
        c.setFillGray(fill)
    c.drawPath(p, stroke=1 if w else 0, fill=1 if fill is not None else 0)
    c.restoreState()


def _head(c, x1, y1, x2, y2, head):
    ang = math.atan2(y2 - y1, x2 - x1)
    a = math.radians(20)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(x2 - head * math.cos(ang - a), y2 - head * math.sin(ang - a))
    p.lineTo(x2 - head * math.cos(ang + a), y2 - head * math.sin(ang + a))
    p.close()
    c.setFillGray(0)
    c.drawPath(p, stroke=0, fill=1)


def arrow(c, x1, y1, x2, y2, w=0.75, head=6):
    c.saveState()
    c.setLineWidth(w)
    ang = math.atan2(y2 - y1, x2 - x1)
    back = head * 0.8
    c.line(x1, y1, x2 - back * math.cos(ang), y2 - back * math.sin(ang))
    _head(c, x1, y1, x2, y2, head)
    c.restoreState()


def darrow(c, x1, y1, x2, y2, w=0.75, head=6):
    c.saveState()
    c.setLineWidth(w)
    ang = math.atan2(y2 - y1, x2 - x1)
    back = head * 0.8
    c.line(x1 + back * math.cos(ang), y1 + back * math.sin(ang),
           x2 - back * math.cos(ang), y2 - back * math.sin(ang))
    _head(c, x1, y1, x2, y2, head)
    _head(c, x2, y2, x1, y1, head)
    c.restoreState()


def circle(c, x, y, r, w=0.75, fill=None):
    c.saveState()
    c.setLineWidth(w)
    if fill is not None:
        c.setFillGray(fill)
    c.circle(x, y, r, stroke=1 if w else 0, fill=1 if fill is not None else 0)
    c.restoreState()


def rect(c, x, y, w, h, lw=0.75, fill=None):
    c.saveState()
    c.setLineWidth(lw)
    if fill is not None:
        c.setFillGray(fill)
    c.rect(x, y, w, h, stroke=1 if lw else 0, fill=1 if fill is not None else 0)
    c.restoreState()


def hatch(c, x, y, w, h, spacing=4, angle=45, lw=0.5):
    """Hatched rectangle (no outline), e.g. a wall, ceiling or the ground.
    The lines sit on a fixed grid, so hatched strips that touch join up
    without a seam."""
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.setLineWidth(lw)
    t = math.tan(math.radians(angle))
    step = spacing / math.sin(math.radians(angle))
    # lines are X = k*step + Y/t; cover every line that crosses the box
    k0 = math.floor((x - (y + h) / t) / step) - 1
    k1 = math.ceil((x + w - y / t) / step) + 1
    for k in range(k0, k1 + 1):
        x_at_y = k * step + y / t
        c.line(x_at_y, y, x_at_y + h / t, y + h)
    c.restoreState()


def spring(c, x1, y1, x2, y2, coils=8, amp=5, w=0.75):
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    nx, ny = -uy, ux
    lead = min(6, L * 0.08)
    pts = [(x1, y1), (x1 + ux * lead, y1 + uy * lead)]
    n = coils * 2
    for k in range(1, n + 1):
        s = lead + (L - 2 * lead) * (k - 0.5) / n
        side = amp if k % 2 else -amp
        pts.append((x1 + ux * s + nx * side, y1 + uy * s + ny * side))
    pts += [(x2 - ux * lead, y2 - uy * lead), (x2, y2)]
    polyline(c, pts, w=w)


def dot(c, x, y, r=2):
    c.saveState()
    c.setFillGray(0)
    c.circle(x, y, r, stroke=0, fill=1)
    c.restoreState()


def wire(c, pts, w=0.75):
    polyline(c, pts, w=w)

# ------------------------------------------------------------------ circuits


def _frame(x1, y1, x2, y2):
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    return L, ux, uy, -uy, ux, (x1 + x2) / 2, (y1 + y2) / 2


def _label(c, x1, y1, x2, y2, label, off=10):
    if not label:
        return
    L, ux, uy, nx, ny, mx, my = _frame(x1, y1, x2, y2)
    if abs(uy) < 0.5:       # horizontal component: label above
        text(c, mx, my + off + 1, label, anchor='c')
    else:                   # vertical: label to the right
        text(c, mx + off + 3, my - 4, label, anchor='l')


def resistor(c, x1, y1, x2, y2, label=None, w=0.75):
    L, ux, uy, nx, ny, mx, my = _frame(x1, y1, x2, y2)
    hl, hw = 13, 4.5
    c.saveState()
    c.setLineWidth(w)
    c.line(x1, y1, mx - ux * hl, my - uy * hl)
    c.line(mx + ux * hl, my + uy * hl, x2, y2)
    pts = [(mx - ux * hl + nx * hw, my - uy * hl + ny * hw), (mx + ux * hl + nx * hw, my + uy * hl + ny * hw),
           (mx + ux * hl - nx * hw, my + uy * hl - ny * hw), (mx - ux * hl - nx * hw, my - uy * hl - ny * hw)]
    c.restoreState()
    polyline(c, pts, w=w, close=True)
    _label(c, x1, y1, x2, y2, label, off=hw + 3)


def capacitor(c, x1, y1, x2, y2, label=None, w=0.75):
    L, ux, uy, nx, ny, mx, my = _frame(x1, y1, x2, y2)
    g, pl = 3.0, 9.0
    c.saveState()
    c.setLineWidth(w)
    c.line(x1, y1, mx - ux * g, my - uy * g)
    c.line(mx + ux * g, my + uy * g, x2, y2)
    c.setLineWidth(1.2)
    for s in (-g, g):
        c.line(mx + ux * s + nx * pl, my + uy * s + ny * pl, mx + ux * s - nx * pl, my + uy * s - ny * pl)
    c.restoreState()
    _label(c, x1, y1, x2, y2, label, off=pl + 2)


def cell(c, x1, y1, x2, y2, label=None, w=0.75):
    """Long thin plate (+) on the (x1, y1) side, short thick plate (–) on the other."""
    L, ux, uy, nx, ny, mx, my = _frame(x1, y1, x2, y2)
    g = 3.0
    c.saveState()
    c.setLineWidth(w)
    c.line(x1, y1, mx - ux * g, my - uy * g)
    c.line(mx + ux * g, my + uy * g, x2, y2)
    c.setLineWidth(0.9)
    c.line(mx - ux * g + nx * 10, my - uy * g + ny * 10, mx - ux * g - nx * 10, my - uy * g - ny * 10)
    c.setLineWidth(2.6)
    c.line(mx + ux * g + nx * 5, my + uy * g + ny * 5, mx + ux * g - nx * 5, my + uy * g - ny * 5)
    c.restoreState()
    _label(c, x1, y1, x2, y2, label, off=12)


def switch(c, x1, y1, x2, y2, closed=False, w=0.75):
    L, ux, uy, nx, ny, mx, my = _frame(x1, y1, x2, y2)
    g = 10.0
    a = (mx - ux * g, my - uy * g)
    b = (mx + ux * g, my + uy * g)
    c.saveState()
    c.setLineWidth(w)
    c.line(x1, y1, *a)
    c.line(*b, x2, y2)
    if closed:
        c.line(*a, *b)
    else:
        ang = math.radians(28)
        ex = a[0] + 2 * g * (ux * math.cos(ang) + nx * math.sin(ang))
        ey = a[1] + 2 * g * (uy * math.cos(ang) + ny * math.sin(ang))
        c.line(*a, ex, ey)
    c.restoreState()


def diode(c, x1, y1, x2, y2, w=0.75):
    L, ux, uy, nx, ny, mx, my = _frame(x1, y1, x2, y2)
    s, hw = 6.0, 6.0
    c.saveState()
    c.setLineWidth(w)
    c.line(x1, y1, mx - ux * s, my - uy * s)
    c.line(mx + ux * s, my + uy * s, x2, y2)
    c.line(mx + ux * s + nx * hw, my + uy * s + ny * hw, mx + ux * s - nx * hw, my + uy * s - ny * hw)
    c.restoreState()
    polyline(c, [(mx - ux * s + nx * hw, my - uy * s + ny * hw), (mx + ux * s, my + uy * s),
                 (mx - ux * s - nx * hw, my - uy * s - ny * hw)], w=w, close=True)


def lamp(c, x1, y1, x2, y2, w=0.75):
    L, ux, uy, nx, ny, mx, my = _frame(x1, y1, x2, y2)
    r = 8.0
    c.saveState()
    c.setLineWidth(w)
    c.line(x1, y1, mx - ux * r, my - uy * r)
    c.line(mx + ux * r, my + uy * r, x2, y2)
    c.circle(mx, my, r)
    d = r * 0.707
    c.line(mx - d, my - d, mx + d, my + d)
    c.line(mx - d, my + d, mx + d, my - d)
    c.restoreState()


def meter(c, x, y, letter, r=9.0, w=0.75):
    circle(c, x, y, r, w=w, fill=1)
    text(c, x, y - 3.9, letter, anchor='c')


def ac_supply(c, x, y, r=9.0, w=0.75):
    circle(c, x, y, r, w=w, fill=1)
    pts = [(x - 5 + 10 * k / 20, y + 2.6 * math.sin(2 * math.pi * k / 20)) for k in range(21)]
    polyline(c, pts, w=w)

# ------------------------------------------------------------------ graphs


def _fmt(v):
    if abs(v - round(v)) < 1e-9:
        s = str(int(round(v)))
    else:
        s = ('%.3f' % v).rstrip('0').rstrip('.')
    return s.replace('-', '–')


class Graph:
    """A Cambridge-style graph grid.

    (x, y) is the bottom-left corner of the plotting area; w and h should be
    whole numbers of minor squares (MINOR = 5.67 pt). Axis tick labels sit
    outside the plotting area, so leave room in the figure box for them.
    """

    def __init__(self, c, x, y, w, h, xr=(0, 10), yr=(0, 10), xmajor=1, ymajor=1, minor=5,
                 grid=True, xlabel='', ylabel='', xticks=None, yticks=None, axes=True,
                 xlabel_pos='right', ylabel_pos='side', labels_outside=False):
        self.c, self.x, self.y, self.w, self.h = c, x, y, w, h
        self.xr, self.yr = xr, yr
        self._labels = []
        if grid:
            self._grid(xmajor, ymajor, minor)
        self.labels_outside = labels_outside
        if axes:
            self._axes(xmajor, ymajor, xticks, yticks, xlabel, ylabel, xlabel_pos, ylabel_pos)

    def P(self, xv, yv):
        return (self.x + (xv - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w,
                self.y + (yv - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h)

    def _grid(self, xmajor, ymajor, minor):
        c = self.c
        c.saveState()
        nx = int(round((self.xr[1] - self.xr[0]) / xmajor * minor))
        ny = int(round((self.yr[1] - self.yr[0]) / ymajor * minor))
        for k in range(nx + 1):
            xx = self.x + self.w * k / nx
            c.setLineWidth(0.6 if k % minor == 0 else 0.25)
            c.setStrokeGray(0 if k % minor == 0 else 0.25)
            c.line(xx, self.y, xx, self.y + self.h)
        for k in range(ny + 1):
            yy = self.y + self.h * k / ny
            c.setLineWidth(0.6 if k % minor == 0 else 0.25)
            c.setStrokeGray(0 if k % minor == 0 else 0.25)
            c.line(self.x, yy, self.x + self.w, yy)
        c.restoreState()

    def _ticks(self, lo, hi, step):
        out, v = [], lo
        while v <= hi + 1e-9:
            out.append((v, _fmt(v)))
            v += step
        return out

    def _axes(self, xmajor, ymajor, xticks, yticks, xlabel, ylabel, xlabel_pos, ylabel_pos):
        c = self.c
        y0 = 0 if self.yr[0] <= 0 <= self.yr[1] else self.yr[0]
        x0 = 0 if self.xr[0] <= 0 <= self.xr[1] else self.xr[0]
        ax_y = self.P(0, y0)[1]
        ax_x = self.P(x0, 0)[0]
        line(c, self.x, ax_y, self.x + self.w, ax_y, w=1.0)
        line(c, ax_x, self.y, ax_x, self.y + self.h, w=1.0)
        xt = xticks if xticks is not None else self._ticks(self.xr[0], self.xr[1], xmajor)
        yt = yticks if yticks is not None else self._ticks(self.yr[0], self.yr[1], ymajor)
        label = self._label
        top = ax_y >= self.y + self.h - 1        # x-axis along the top edge (all-negative y)
        tx = 3 if ax_y > self.y + 1 else 0       # ticks cross an axis inside the grid
        ty = 3 if ax_x > self.x + 1 else 0
        # where the tick labels go: beside the axis, or outside the grid
        if top:
            lx_y, xl_y = ax_y + 5, ax_y + 19
        elif self.labels_outside:
            lx_y, xl_y = self.y - 13, self.y - 27
        else:
            lx_y, xl_y = ax_y - 13, ax_y - 27
        ly_x = self.x - 5 if self.labels_outside else ax_x - 5
        for v, s in xt:
            px = self.P(v, 0)[0]
            line(c, px, ax_y + (3 if top else tx), px, ax_y - (0 if top else 3), w=0.75)
            if s:
                label(c, px, lx_y, s, anchor='c')
        for v, s in yt:
            py = self.P(0, v)[1]
            line(c, ax_x + ty, py, ax_x - 3, py, w=0.75)
            if s:
                label(c, ly_x, py - 3.9, s, anchor='r')
        ax_x = self.x if self.labels_outside else ax_x
        if xlabel:
            if xlabel_pos == 'right':
                label(c, self.x + self.w, xl_y, xlabel, anchor='r')
            else:
                label(c, self.x + self.w / 2, xl_y, xlabel, anchor='c')
        if ylabel:
            ytw = max([text_width(s) for _, s in yt] + [0])
            if ylabel_pos == 'top':
                label(c, ax_x, self.y + self.h + 10, ylabel, anchor='c')
            else:
                label(c, ax_x - ytw - 10, self.y + self.h * 0.62, ylabel, anchor='r')

    def _label(self, c, x, y, s, anchor='l'):
        self._labels.append((x, y, s, anchor))
        label(c, x, y, s, anchor=anchor)

    def finish(self):
        """Redraw the axis labels on top of anything plotted over them."""
        for x, y, s, anchor in self._labels:
            label(self.c, x, y, s, anchor=anchor)

    def curve(self, f, x0, x1, n=200, w=1.0, dash=None):
        pts = []
        for k in range(n + 1):
            xv = x0 + (x1 - x0) * k / n
            pts.append(self.P(xv, f(xv)))
        polyline(self.c, pts, w=w, dash=dash)

    def points(self, pts, w=1.0, dash=None):
        polyline(self.c, [self.P(*p) for p in pts], w=w, dash=dash)

    def line(self, x1, y1, x2, y2, w=1.0, dash=None):
        a, b = self.P(x1, y1), self.P(x2, y2)
        line(self.c, a[0], a[1], b[0], b[1], w=w, dash=dash)

    def mark(self, xv, yv, style='x', size=3.0):
        px, py = self.P(xv, yv)
        if style == 'x':
            line(self.c, px - size, py - size, px + size, py + size, w=0.75)
            line(self.c, px - size, py + size, px + size, py - size, w=0.75)
        else:
            dot(self.c, px, py, 2)

    def text(self, xv, yv, s, anchor='l', dx=0, dy=0, size=11):
        px, py = self.P(xv, yv)
        text(self.c, px + dx, py + dy, s, size=size, anchor=anchor)
