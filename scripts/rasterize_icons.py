"""Rasterize Nerd Font symbol glyphs down to the 6x13 cell of misc-fixed 6x13.

Icons keep their aspect ratio (fit into ICON_W x ICON_H and centred vertically);
Powerline Extra shapes (U+E0B4-E0D7) are designed to fill a whole cell, so they
are stretched to 6x13 instead.  Output rows are '#'/'.' strings, 6 wide x 13 tall.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 6, 13
ICON_W, ICON_H = 6, 8      # largest bitmap an icon may occupy
CENTRE_ROW = 6             # vertical centre of icons (cap-height middle)
SS = 8                     # supersampling factor for the source render
THRESHOLD = 0.40           # coverage needed to turn a pixel on

# Ranges taken from the Nerd Fonts glyph sets whose licenses we can honour.
# (Pomicons: OFL RFN, Weather Icons: OFL, Font Logos: unlicensed, Material
# Design: outside the 16-bit range X11 core fonts support -- all excluded.)
RANGES = {
    "powerline-extra": (0xE0C0, 0xE0D7, "fill"),
    "seti":            (0xE5FA, 0xE6B7, "icon"),
    "devicons":        (0xE700, 0xE8EF, "icon"),
    "font-awesome-ext": (0xE200, 0xE2A9, "icon"),
    "codicons":        (0xEA60, 0xEC1E, "icon"),
    "font-awesome":    (0xF000, 0xF2E0, "icon"),
    "octicons":        (0xF400, 0xF533, "icon"),
}


def _render(font, cp, size_px):
    """Render cp at size_px*SS and return a tight-cropped 'L' image or None."""
    canvas = Image.new("L", (size_px * SS * 3, size_px * SS * 3), 0)
    ImageDraw.Draw(canvas).text((size_px * SS, size_px * SS), chr(cp), font=font, fill=255)
    bbox = canvas.getbbox()
    return canvas.crop(bbox) if bbox else None


def _to_rows(img, left, top):
    """Place a coverage image (already at final pixel size) into the 6x13 grid."""
    rows = [["."] * W for _ in range(H)]
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            gx, gy = left + x, top + y
            if 0 <= gx < W and 0 <= gy < H and px[x, y] / 255 >= THRESHOLD:
                rows[gy][gx] = "#"
    return ["".join(r) for r in rows]


def rasterize(font_path, cp, mode):
    font = ImageFont.truetype(font_path, 13 * SS)
    src = _render(font, cp, 13)
    if src is None:
        return None
    if mode == "fill":
        # the shape spans the full cell in the source font: map its cell box
        asc, desc = font.getmetrics()
        cell = Image.new("L", (13 * SS, asc + desc), 0)
        ImageDraw.Draw(cell).text((0, 0), chr(cp), font=font, fill=255)
        small = cell.resize((W, H), Image.BOX)
        return _to_rows(small, 0, 0)
    scale = min(ICON_W / (src.width / SS), ICON_H / (src.height / SS), 1.0)
    w = max(1, round(src.width / SS * scale))
    h = max(1, round(src.height / SS * scale))
    small = src.resize((w, h), Image.BOX)
    left = (W - w) // 2
    top = max(0, min(H - h, CENTRE_ROW - h // 2))
    return _to_rows(small, left, top)


def codepoints():
    for name, (lo, hi, mode) in RANGES.items():
        for cp in range(lo, hi + 1):
            yield name, cp, mode
