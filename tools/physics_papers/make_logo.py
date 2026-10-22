#!/usr/bin/env python3
"""Turn an image into the black-and-white logo used on the papers.

    python3 tools/physics_papers/make_logo.py IMAGE [--gray]

The background (taken from the image's corners, or transparency) is
removed, the rest becomes solid black (or grey tones with --gray), the
result is trimmed and saved as tools/physics_papers/logo.png with a
transparent background. The engine fits it into the logo box at the top
of the cover, where Cambridge's logo sits.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

OUT = Path(__file__).resolve().parent / 'logo.png'


def otsu(values):
    hist, _ = np.histogram(values, bins=256, range=(0, 256))
    total, sum_all = values.size, np.dot(np.arange(256), hist)
    best, thr, w0, s0 = 0, 128, 0, 0.0
    for t in range(256):
        w0 += hist[t]
        if w0 == 0 or w0 == total:
            continue
        s0 += t * hist[t]
        m0, m1 = s0 / w0, (sum_all - s0) / (total - w0)
        between = w0 * (total - w0) * (m0 - m1) ** 2
        if between > best:
            best, thr = between, t
    return thr


def make(path, gray=False):
    im = Image.open(path).convert('RGBA')
    # work at a size that prints sharply in a 276 x 29 pt box at 300 dpi
    scale = max(1.0, 1200 / im.width)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    a = np.asarray(im).astype(float)
    alpha = a[..., 3] / 255
    rgb = a[..., :3] * alpha[..., None] + 255 * (1 - alpha[..., None])
    lum = rgb @ np.array([0.299, 0.587, 0.114])
    corners = np.concatenate([lum[:8, :8].ravel(), lum[:8, -8:].ravel(), lum[-8:, :8].ravel(), lum[-8:, -8:].ravel()])
    bg = np.median(corners)
    # distance from the background colour, so dark-on-light and light-on-dark both work
    dist = np.abs(lum - bg)
    if alpha.min() < 0.99:
        dist = np.maximum(dist, 255 * (alpha > 0.5) * (dist < 1))
    t = max(otsu(dist.astype(np.uint8)), 20)
    if gray:
        ink = np.clip((dist - t * 0.5) / (dist.max() - t * 0.5 + 1e-6), 0, 1)
    else:
        ink = (dist > t).astype(float)
    mask = Image.fromarray((ink * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
    box = mask.point(lambda v: 255 if v > 24 else 0).getbbox()
    if box is None:
        raise SystemExit('no logo found in the image')
    mask = mask.crop(box)
    out = Image.new('RGBA', mask.size, (0, 0, 0, 0))
    out.putalpha(mask)
    out.save(OUT)
    print(f'wrote {OUT} ({out.width} x {out.height} px)')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        raise SystemExit(__doc__)
    make(args[0], gray='--gray' in sys.argv)
