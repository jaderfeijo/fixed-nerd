#!/bin/sh
# Download the Nerd Fonts "Symbols Only" release at a pinned tag into build/symbols/.
set -eu
TAG=v3.5.1
cd "$(dirname "$0")/.."
mkdir -p build/symbols && cd build/symbols
curl -fsSL -o NerdFontsSymbolsOnly.tar.xz "https://github.com/ryanoasis/nerd-fonts/releases/download/$TAG/NerdFontsSymbolsOnly.tar.xz"
tar -xJf NerdFontsSymbolsOnly.tar.xz LICENSE README.md SymbolsNerdFontMono-Regular.ttf
sha256sum NerdFontsSymbolsOnly.tar.xz SymbolsNerdFontMono-Regular.ttf
