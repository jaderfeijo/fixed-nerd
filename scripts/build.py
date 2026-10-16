#!/usr/bin/env python3
"""Build fixed-nerd-6x13.bdf: misc-fixed 6x13 plus Powerline and Nerd Font glyphs.

    scripts/build.py [--symbols PATH] [--out PATH] [--verify]

Upstream glyphs are never modified; only codepoints that upstream lacks are added.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdf
import fallback_glyphs
import powerline
import rasterize_icons

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAMILY = "FixedNerd"
XLFD = "-jaderfeijo-FixedNerd-Medium-R-SemiCondensed--13-120-75-75-C-60-ISO10646-1"
COPYRIGHT = ("Public domain font (misc-fixed 6x13). Added glyphs: see NOTICE.md "
             "(Powerline MIT, Nerd Fonts MIT, Font Awesome CC BY 4.0, Codicons CC BY 4.0, "
             "Octicons MIT, Devicons MIT, Seti-UI MIT).")


def retitle(header):
    out = []
    for line in header:
        if line.startswith("FONT "):
            line = "FONT " + XLFD
        elif line.startswith("FOUNDRY "):
            line = 'FOUNDRY "jaderfeijo"'
        elif line.startswith("FAMILY_NAME "):
            line = 'FAMILY_NAME "%s"' % FAMILY
        elif line.startswith("COPYRIGHT "):
            line = 'COPYRIGHT "%s"' % COPYRIGHT
        elif line.startswith("STARTPROPERTIES "):
            pass
        out.append(line)
    # extra comments right after the first COMMENT line(s)
    extra = [
        "COMMENT Fixed Nerd: misc-fixed 6x13 (public domain) with added Powerline/Nerd Font glyphs.",
        "COMMENT Modified from the upstream X.Org misc-misc 6x13.bdf; see NOTICE.md for sources and licenses.",
    ]
    idx = max(i for i, l in enumerate(out) if l.startswith("COMMENT")) + 1
    return out[:idx] + extra + out[idx:]


def make_glyph(cp, rows):
    return bdf.Glyph("uni%04X" % cp, cp, powerline.W, (powerline.W, powerline.H, 0, -2), rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=os.path.join(ROOT, "build/symbols/SymbolsNerdFontMono-Regular.ttf"))
    ap.add_argument("--text-font", default="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                    help="DejaVu Sans Mono (apt: fonts-dejavu-core), source of TUI symbol fallbacks")
    ap.add_argument("--upstream", default=os.path.join(ROOT, "upstream/6x13.bdf"))
    ap.add_argument("--out", default=os.path.join(ROOT, "build/fixed-nerd-6x13.bdf"))
    ap.add_argument("--verify", action="store_true", help="check upstream glyphs are unchanged")
    args = ap.parse_args()

    font = bdf.parse(args.upstream)
    original = {cp: (g.dwidth, g.bbx, list(g.rows)) for cp, g in font.glyphs.items()}
    added = {}

    for cp, rows in powerline.glyphs().items():
        added[cp] = ("powerline", rows)
    for name, cp, mode in rasterize_icons.codepoints():
        if cp in added:
            continue
        rows = rasterize_icons.rasterize(args.symbols, cp, mode)
        if rows and any("#" in r for r in rows):
            added[cp] = (name, rows)

    for cp, (src, rows) in fallback_glyphs.glyphs(font.glyphs, args.text_font).items():
        if cp not in added:
            added[cp] = ("tui-" + src, rows)

    skipped = [cp for cp in added if cp in font.glyphs]
    for cp, (_, rows) in added.items():
        if cp in font.glyphs:
            continue            # never touch upstream glyphs
        font.glyphs[cp] = make_glyph(cp, rows)
    font.header = retitle(font.header)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    bdf.write(font, args.out)

    counts = {}
    for cp, (name, _) in added.items():
        if cp not in skipped:
            counts[name] = counts.get(name, 0) + 1
    print("upstream glyphs: %d, added: %d, skipped (already in upstream): %d"
          % (len(original), sum(counts.values()), len(skipped)))
    for name, n in sorted(counts.items()):
        print("  %-18s %d" % (name, n))

    if args.verify:
        chk = bdf.parse(args.out)
        bad = [cp for cp, v in original.items()
               if (chk.glyphs[cp].dwidth, chk.glyphs[cp].bbx, chk.glyphs[cp].rows) != v]
        if bad:
            sys.exit("verify FAILED: %d upstream glyphs changed" % len(bad))
        print("verify OK: all %d upstream glyphs identical" % len(original))


if __name__ == "__main__":
    main()
