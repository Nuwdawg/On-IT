"""Logo, barcodes and QR codes for the cover and page furniture.

The barcodes are Code 39 (the * start and stop characters are printed
beside them, as on Cambridge papers) and scan as plain digits:
- top of every page: 19870727 (the release date of Rick Astley's
  "Never Gonna Give You Up") then 000 and the page number;
- down the side of the cover: 299792458, the speed of light in m s–1.
The QR codes open the song on YouTube.
"""
from pathlib import Path

from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.code39 import Standard39
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.utils import ImageReader

HERE = Path(__file__).resolve().parent
RICKROLL = 'https://youtu.be/dQw4w9WgXcQ'
RELEASE_DATE = '19870727'
SPEED_OF_LIGHT = '299792458'


def page_code(pageno):
    return f'{RELEASE_DATE}000{pageno:02d}'


def code39(c, x, y, w, h, value, vertical=False):
    """Code 39 barcode filling w x h points with its bottom-left at (x, y).
    With vertical=True the bars run horizontally and the code reads upwards
    across a box w wide and h tall."""
    length, height = (h, w) if vertical else (w, h)
    probe = Standard39(value, barWidth=1.0, barHeight=height, ratio=2.5, checksum=0, quiet=0, stop=1)
    bc = Standard39(value, barWidth=length / probe.width, barHeight=height, ratio=2.5,
                    checksum=0, quiet=0, stop=1)
    c.saveState()
    c.setFillGray(0)
    if vertical:
        c.translate(x + w, y)
        c.rotate(90)
        bc.drawOn(c, 0, 0)
    else:
        bc.drawOn(c, x, y)
    c.restoreState()


def qr(c, x, y, size, data=RICKROLL):
    """QR code size x size points with its bottom-left at (x, y), no quiet zone."""
    w = QrCodeWidget(data, barLevel='L', barBorder=0)
    x0, y0, x1, y1 = w.getBounds()
    d = Drawing(size, size, transform=[size / (x1 - x0), 0, 0, size / (y1 - y0), 0, 0])
    d.add(w)
    renderPDF.draw(d, c, x, y)


LOGO = HERE / 'logo.png'      # black-and-white logo made by make_logo.py


def logo(c, x, y, w, h, align='left'):
    """Draw the F3XP M.A.R.S. logo fitted inside the w x h box with bottom-left (x, y),
    left-aligned and vertically centred, as the Cambridge logo sits.
    Does nothing if there is no logo file yet."""
    if not LOGO.exists():
        return
    img = ImageReader(str(LOGO))
    iw, ih = img.getSize()
    s = min(w / iw, h / ih)
    dx = (w - iw * s) / 2 if align == 'center' else 0
    c.drawImage(img, x + dx, y + (h - ih * s) / 2, iw * s, ih * s, mask='auto')
