# Notices, attribution and changes

`dist/fixed-nerd-6x13.bdf` is a **modified version** of the misc-fixed 6x13 font
combined with glyphs derived from several icon sets. This file lists what is in
it, under which license, and what was changed. Full license texts are in `LICENSES/`.

## Base font: misc-fixed 6x13 (public domain)

Source: https://gitlab.freedesktop.org/xorg/font/misc-misc (commit
`c4e2af05583764fae3d0b2aa20d5c93b031cbcbf`). License: *"Public domain font.  Share and enjoy."*
(`LICENSES/fixed-public-domain.txt`). No attribution is legally required, but credit is due: the
original ASCII/Latin-1 designers are lost to history (likely MIT Project Athena / DEC, mid 1980s);
the Unicode extension was led by Markus Kuhn (University of Cambridge) with major contributions
from Robert Brady, Birger Langkjer, Constantine Stathopoulos, Mark Leisher and others
(see `upstream/AUTHORS`).

**Changes:** none to any existing glyph (checked by `scripts/build.py --verify`). Added glyphs, the font
name (`-jaderfeijo-FixedNerd-...`), the FOUNDRY/FAMILY_NAME/COPYRIGHT properties and two COMMENT
lines were changed.

## Added glyphs

Every added glyph was **converted to a 6x13 one-bit bitmap** (downsampled, thresholded, in
some cases stretched or repositioned to fit the cell) from the vector originals in
*Symbols Nerd Font Mono* (Nerd Fonts v3.5.1), or drawn by hand. These bitmap conversions are the
"changes" required to be indicated by CC BY 4.0 and Apache-2.0 style licenses.

| Codepoints | Glyphs | Set | Upstream | License |
|---|---|---|---|---|
| U+E0A0–E0A3, U+E0B0–E0BF | 20 | Powerline symbols (drawn procedurally / by hand in `scripts/powerline.py`, shapes follow the Powerline originals) | https://github.com/powerline/powerline — Copyright 2013 Kim Silkebækken and contributors | MIT (`LICENSES/powerline-symbols-MIT.txt`) |
| U+E0C0–E0D7 | 18 | Powerline Extra Symbols | https://github.com/ryanoasis/powerline-extra-symbols — Copyright (c) 2016 Ryan L McIntyre | MIT (`LICENSES/powerline-extra-MIT.txt`) |
| U+E200–E2A9 | 169 | Font Awesome Extension | https://github.com/AndreLZGava/font-awesome-extension — Copyright (c) 2017 André Luiz Gava | MIT (`LICENSES/font-awesome-extension-MIT.txt`) |
| U+E5FA–E6B7 | 186 | Seti-UI + Custom | https://github.com/jesseweed/seti-ui — Copyright (c) 2014 Jesse Weed | MIT (`LICENSES/seti-ui-MIT.txt`) |
| U+E700–E8EF | 477 | Devicons | https://github.com/devicons/devicon — Copyright (c) 2015 konpa | MIT (`LICENSES/devicons-MIT.txt`) |
| U+EA60–EC1E | 445 | Codicons | https://github.com/microsoft/vscode-codicons — Copyright (c) Microsoft Corporation | CC BY 4.0 (`LICENSES/codicons-CC-BY-4.0.txt`) |
| U+F000–F2E0 | 736 | Font Awesome (Free) | https://github.com/FortAwesome/Font-Awesome — Copyright Fonticons, Inc. | CC BY 4.0 for icons; SIL OFL 1.1 for the font files (`LICENSES/font-awesome-CC-BY-4.0.txt`, which contains all terms) |
| U+F400–F533 | 307 | Octicons | https://github.com/primer/octicons — Copyright (c) 2023 GitHub Inc. | MIT (`LICENSES/octicons-MIT.txt`) |

The glyph selection and the vector sources come from the Nerd Fonts project
(https://github.com/ryanoasis/nerd-fonts, Copyright (c) 2014 Ryan L McIntyre, MIT —
`LICENSES/nerd-fonts-MIT.txt`).

### TUI symbols (U+23xx, 26xx, 27xx, 29xx, 2Bxx, ...)

About 50 glyphs that popular terminal UIs emit but the base font lacks (`scripts/tui_glyphs.py`):
6 hand-drawn in `scripts/fallback_glyphs.py` (e.g. `❯ ❮ ⚠ ⏸`), 15 reuse existing upstream bitmaps (e.g. `⏺` = `●`),
and the rest are bitmap conversions of **DejaVu Sans Mono** glyphs (scaled to a 6px advance, thresholded).
DejaVu is Copyright (c) 2003 Bitstream, Inc.; DejaVu changes are public domain; Bitstream Vera license in
`LICENSES/dejavu-bitstream-vera.txt`. That license permits modification and addition of glyphs provided the
result is renamed without "Bitstream" or "Vera" (this font is "Fixed Nerd") and that the notice is kept.

### Deliberately excluded
- Pomicons (U+E000–E00A) — OFL 1.1 with a Reserved Font Name; also collides with existing ConScript glyphs.
- Weather Icons (U+E300–E3E3) — OFL 1.1 (a derivative font would have to be OFL).
- Font Logos (U+F300–F381) — no license; these are distro/brand logos.
- Wide/emoji-presentation symbols (e.g. ✨ ⚡ ⏩): xterm gives them two cells, which a 6px glyph cannot fill.
- Material Design Icons (U+F0001+) — outside the 16-bit range that X11 core fonts support.

### A note on Font Awesome
Font Awesome Free licenses its icons under CC BY 4.0 and its *font files* under SIL OFL 1.1 (Reserved Font
Name "Font Awesome"). The glyphs here are bitmap conversions of the icon shapes, credited as
above, and this font does not use the name "Font Awesome". If you need a strictly OFL-clean or
CC BY-free build, remove the `font-awesome` entry from `RANGES` in `scripts/rasterize_icons.py` and rebuild.

## Redistribution checklist
When redistributing `dist/` files, keep this NOTICE.md and the `LICENSES/` directory with them.
