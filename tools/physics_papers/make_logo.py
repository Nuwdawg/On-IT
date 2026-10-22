#!/usr/bin/env python3
"""Make the black-and-white logo printed at the top of the covers.

    python3 tools/physics_papers/make_logo.py [IMAGE] [--line1 F3XP] [--line2 M.A.R.S.]

The source is a photo of a round embroidered patch (logo_source.jpg, from
github.com/xnkhi/temp). The patch is cut out of its dark background and
turned into a black-and-white badge: black thread and the blue sky become
black, and everything else (the yellow ring, the planet, Saturn, the stars
and the alien) becomes white, so the picture still reads at crest size. A
clean black rim is drawn round it.

The badge is then set out like Cambridge's logo: crest on the left, then
two lines of text, the first semibold and the second regular, at the same
sizes and spacing. The result is saved as logo.png, which the engine fits
into the logo box at the top of each cover.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / 'logo.png'
INTER = '/usr/share/fonts/opentype/inter/'
PX = 12.0          # pixels per point in the output (about 860 dpi)

# Cambridge logo geometry, in points, measured from 9702_s25_qp_42 page 1
CREST_H = 29.4
GAP = 5.0
CAP_H = 11.4       # height of a capital letter
BASE1 = 11.6       # first baseline below the top of the logo
BASE2 = 27.4       # second baseline


def badge(src):
    im = Image.open(src).convert('RGB').filter(ImageFilter.MedianFilter(5))
    a = np.asarray(im).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    # the patch is the bright disc on a dark background
    ys, xs = np.where(lum > 110)
    cx, cy = (xs.min() + xs.max()) / 2, (ys.min() + ys.max()) / 2
    R = max(xs.max() - xs.min(), ys.max() - ys.min()) / 2 - 2
    yy, xx = np.mgrid[:a.shape[0], :a.shape[1]]
    d = np.hypot(xx - cx, yy - cy)
    red = (r > g + 40) & (r > b + 20)
    green = (g > r + 3) & (g > b + 8)
    blue = (b > r + 20) & ~green
    white = np.where(red, lum > 45, np.where(green, lum > 40, np.where(blue, False, lum > 60)))
    ink = (~white) & (d < R)
    ink = np.asarray(Image.fromarray((ink * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(7))) > 127
    rim = R * 0.034
    ink |= (d >= R) & (d < R + rim)
    alpha = d < R + rim
    rgba = np.zeros(a.shape[:2] + (4,), np.uint8)
    rgba[..., :3] = np.where(ink[..., None], 0, 255)
    rgba[..., 3] = np.where(alpha, 255, 0)
    half = R + rim + 1
    return Image.fromarray(rgba).crop((int(cx - half), int(cy - half), int(cx + half), int(cy + half)))


def make(src, line1, line2):
    crest = badge(src)
    size = int(round(CREST_H * PX))
    crest = crest.resize((size, size), Image.LANCZOS)
    semi = ImageFont.truetype(INTER + 'Inter-SemiBold.otf', 100)
    reg = ImageFont.truetype(INTER + 'Inter-Regular.otf', 100)
    cap = semi.getbbox('H')[3] - semi.getbbox('H')[1]
    fs = int(round(100 * CAP_H * PX / cap))
    semi = ImageFont.truetype(INTER + 'Inter-SemiBold.otf', fs)
    reg = ImageFont.truetype(INTER + 'Inter-Regular.otf', fs)
    tx = size + GAP * PX
    w = int(tx + max(semi.getlength(line1), reg.getlength(line2)) + 2)
    out = Image.new('RGBA', (w, size), (255, 255, 255, 0))
    out.alpha_composite(crest, (0, 0))
    draw = ImageDraw.Draw(out)
    draw.text((tx, BASE1 * PX), line1, font=semi, fill=(0, 0, 0, 255), anchor='ls')
    draw.text((tx, BASE2 * PX), line2, font=reg, fill=(0, 0, 0, 255), anchor='ls')
    out.save(OUT)
    print(f'wrote {OUT} ({out.width} x {out.height} px, {out.width / PX:.1f} x {out.height / PX:.1f} pt)')


if __name__ == '__main__':
    args = sys.argv[1:]
    opt = lambda k, d: args[args.index(k) + 1] if k in args else d
    pos = [a for i, a in enumerate(args) if not a.startswith('--') and (i == 0 or not args[i - 1].startswith('--'))]
    make(pos[0] if pos else HERE / 'logo_source.jpg', opt('--line1', 'F3XP'), opt('--line2', 'M.A.R.S.'))
