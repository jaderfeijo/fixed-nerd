"""Minimal BDF reader/writer, just enough for fixed-width bitmap fonts.

Glyphs are exposed as lists of pixel-row strings ('#' = ink, '.' = blank) so
that the rest of the pipeline never has to deal with hex bitmaps.
"""
from dataclasses import dataclass, field


@dataclass
class Glyph:
    name: str
    encoding: int
    dwidth: int
    bbx: tuple  # (width, height, xoff, yoff)
    rows: list  # pixel rows, top to bottom, each len == bbx[0]


@dataclass
class Font:
    header: list  # raw lines before the first STARTCHAR (minus CHARS)
    glyphs: dict = field(default_factory=dict)  # encoding -> Glyph
    trailer: list = field(default_factory=list)


def parse(path):
    with open(path, encoding="latin-1") as f:
        lines = f.read().splitlines()
    font = Font(header=[])
    i = 0
    while not lines[i].startswith("STARTCHAR"):
        if not lines[i].startswith("CHARS "):
            font.header.append(lines[i])
        i += 1
    while i < len(lines):
        line = lines[i]
        if line.startswith("STARTCHAR"):
            name = line.split(None, 1)[1]
            enc = dwidth = bbx = None
            i += 1
            while lines[i] != "BITMAP":
                key, *rest = lines[i].split()
                if key == "ENCODING":
                    enc = int(rest[0])
                elif key == "DWIDTH":
                    dwidth = int(rest[0])
                elif key == "BBX":
                    bbx = tuple(int(x) for x in rest)
                i += 1
            i += 1
            w, h = bbx[0], bbx[1]
            rows = []
            for _ in range(h):
                bits = bin(int(lines[i], 16))[2:].zfill(len(lines[i]) * 4)
                rows.append("".join("#" if b == "1" else "." for b in bits[:w]))
                i += 1
            assert lines[i] == "ENDCHAR", (name, lines[i])
            if enc is not None and enc >= 0:
                font.glyphs[enc] = Glyph(name, enc, dwidth, bbx, rows)
        else:
            if line.strip() and line != "ENDFONT":
                font.trailer.append(line)
        i += 1
    return font


def _hex_row(row):
    nbytes = (len(row) + 7) // 8
    value = int(row.replace("#", "1").replace(".", "0").ljust(nbytes * 8, "0"), 2)
    return format(value, "0%dX" % (nbytes * 2))


def write(font, path):
    out = list(font.header)
    out.append("CHARS %d" % len(font.glyphs))
    for enc in sorted(font.glyphs):
        g = font.glyphs[enc]
        out += ["STARTCHAR " + g.name,
                "ENCODING %d" % g.encoding,
                "SWIDTH %d 0" % (g.dwidth * 80),  # 6px cell -> 480, as upstream
                "DWIDTH %d 0" % g.dwidth,
                "BBX %d %d %d %d" % g.bbx,
                "BITMAP"]
        out += [_hex_row(r) for r in g.rows]
        out.append("ENDCHAR")
    out.append("ENDFONT")
    with open(path, "w", encoding="latin-1", newline="\n") as f:
        f.write("\n".join(out) + "\n")
