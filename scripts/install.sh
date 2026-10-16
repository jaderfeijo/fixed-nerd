#!/bin/sh
# Install the built font for the current user (X11 core font, for xterm/uxterm).
# Only NEW terminals pick it up; already-running ones are not touched.
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${1:-$ROOT/dist/fixed-nerd-6x13.bdf}"
DEST="${FIXEDNERD_DIR:-$HOME/.local/share/fonts/X11/fixed-nerd}"
mkdir -p "$DEST"
bdftopcf -t -o "$DEST/fixednerd6x13.pcf" "$SRC"
gzip -9 -f "$DEST/fixednerd6x13.pcf"
mkfontdir "$DEST"
xset +fp "$DEST"
xset fp rehash
echo "Installed to $DEST"
echo "Try it:  uxterm -fn '-jaderfeijo-FixedNerd-medium-r-semicondensed--13-120-75-75-c-60-iso10646-1'"
echo "Make it permanent: add 'xset +fp $DEST' to your X startup (e.g. ~/.xsessionrc) and"
echo "  UXTerm*font: -jaderfeijo-FixedNerd-medium-r-semicondensed--13-120-75-75-c-60-iso10646-1"
echo "to ~/.Xresources."
