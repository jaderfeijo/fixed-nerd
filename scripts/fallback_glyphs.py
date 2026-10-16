"""Fill gaps in misc-fixed 6x13 for glyphs that popular terminal UIs emit.

Three sources, in priority order:
  1. HAND   -- drawn here (carets and media symbols where shape/alignment matter)
  2. ALIAS  -- reuse an existing upstream glyph that has the same look
  3. DejaVu Sans Mono, scaled so its advance is 6px, baseline on the font's baseline
Wide (East Asian Wide / emoji-presentation) symbols are skipped: xterm gives them two
cells, which a 6px core-font glyph cannot fill.
"""
from PIL import Image, ImageDraw, ImageFont

import tui_glyphs

W, H, ASCENT = 6, 13, 11
SS = 8
THRESHOLD = 0.40

WIDE = set(map(ord, "⏩⏪⏫⏬⏰⏳⌚⌛✨⚡✅❌❓❔❕❗⭐⭕⬛⬜"))

HAND = {
    0x276F: ["......", "......", "......", "##....", ".##...", "..##..", "...##.", "..##..",
             ".##...", "##....", "......", "......", "......"],          # ❯
    0x276E: ["......", "......", "......", "....##", "...##.", "..##..", ".##...", "..##..",
             "...##.", "....##", "......", "......", "......"],          # ❮
    0x2771: ["......", "......", "......", "#.....", ".#....", "..#...", "...#..", "..#...",
             ".#....", "#.....", "......", "......", "......"],          # ❱ (medium)
    0x2770: ["......", "......", "......", ".....#", "....#.", "...#..", "..#...", "...#..",
             "....#.", ".....#", "......", "......", "......"],          # ❰
    0x26A0: ["......", "......", "..##..", ".#..#.", ".#..#.", "#.##.#", "#.##.#", "#.##.#",
             "#....#", "######", "......", "......", "......"],          # ⚠
    0x23F8: ["......", "......", "......", "......", ".#.#..", ".#.#..", ".#.#..", ".#.#..",
             ".#.#..", ".#.#..", "......", "......", "......"],          # ⏸ (pause)
}
# codepoint -> upstream codepoint whose bitmap it should reuse
ALIAS = {
    0x23FA: 0x25CF,   # ⏺ record      <- ●
    0x23F5: 0x25B8,   # ⏵ play        <- ▸
    0x23F4: 0x25C2,   # ⏴             <- ◂
    0x23F6: 0x25B4,   # ⏶             <- ▴
    0x23F7: 0x25BE,   # ⏷             <- ▾
    0x23F9: 0x25AA,   # ⏹ stop        <- ▪
    0x2B25: 0x25C6,   # ⬥ medium diamond <- ◆
    0x2B26: 0x25C7,   # ⬦             <- ◇
    0x2B27: 0x25C6,   # ⬧ lozenge     <- ◆
    0x2B28: 0x25C7,   # ⬨             <- ◇
    0x2B29: 0x25C6,   # ⬩ small       <- ◆
    0x2B2A: 0x25C6,   # ⬪
    0x2B2B: 0x25C7,   # ⬫
    0x2B1D: 0x2219,   # ⬝ black very small square <- ∙
    0x2B1E: 0x2219,
}


def _rows(img, left=0, top=0):
    px = img.load()
    rows = [["."] * W for _ in range(H)]
    for y in range(img.height):
        for x in range(img.width):
            gx, gy = left + x, top + y
            if 0 <= gx < W and 0 <= gy < H and px[x, y] / 255 >= THRESHOLD:
                rows[gy][gx] = "#"
    return ["".join(r) for r in rows]


def _has_glyph(font, cp):
    """False when the font would draw its .notdef box for cp."""
    def render(c):
        im = Image.new("L", (200, 200), 0)
        ImageDraw.Draw(im).text((20, 150), chr(c), font=font, fill=255, anchor="ls")
        return im.tobytes()
    return render(cp) != render(0x10FFFE)


def _from_text_font(font_path, cp):
    probe = ImageFont.truetype(font_path, 100)
    if not _has_glyph(probe, cp):
        return None
    adv = probe.getlength("M")
    size = 6 / adv * 100                       # advance of the font == 6px
    font = ImageFont.truetype(font_path, size * SS)
    canvas = Image.new("L", (W * SS, H * SS), 0)
    ImageDraw.Draw(canvas).text((0, ASCENT * SS), chr(cp), font=font, fill=255, anchor="ls")
    if canvas.getbbox() is None:
        return None
    return _rows(canvas.resize((W, H), Image.BOX))


def glyphs(upstream, text_font_path):
    """Return {codepoint: (source, rows)} for every curated glyph upstream lacks."""
    out = {}
    for cp in sorted(tui_glyphs.codepoints()):
        if cp in upstream or cp in WIDE:
            continue
        if cp in HAND:
            out[cp] = ("hand", HAND[cp])
        elif cp in ALIAS and ALIAS[cp] in upstream:
            out[cp] = ("alias", list(upstream[ALIAS[cp]].rows))
        else:
            rows = _from_text_font(text_font_path, cp)
            if rows and any("#" in r for r in rows):
                out[cp] = ("dejavu", rows)
    return out
