#!/usr/bin/env bash
# Install Fixed Nerd for the current user: the X11 font, its place in the font path at every login, and
# the xterm/uxterm font setting. Nothing of yours is replaced: the two settings are marked blocks
# ("fixed-nerd") in the Window Maker autostart file and in ~/.Xresources, and --uninstall removes exactly those.
# Already-running terminals are never touched.
set -euo pipefail

NAME=fixed-nerd
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
SRC="${FIXEDNERD_BDF:-$HERE/dist/fixed-nerd-6x13.bdf}"
DEST="${FIXEDNERD_DIR:-${XDG_DATA_HOME:-$HOME/.local/share}/fonts/X11/fixed-nerd}"
XRES="${XRESOURCES_FILE:-$HOME/.Xresources}"
AUTOSTART="${AUTOSTART_FILE:-${GNUSTEP_USER_ROOT:-$HOME/GNUstep}/Library/WindowMaker/autostart}"
XLFD='-jaderfeijo-FixedNerd-medium-r-semicondensed--13-120-75-75-c-60-iso10646-1'
DRY=0 UNINSTALL=0 APPLY=1 XRESOURCES=1 STARTUP=1

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --uninstall) UNINSTALL=1 ;;
    --no-apply) APPLY=0 ;;
    --no-xresources) XRESOURCES=0 ;;
    --no-autostart) STARTUP=0 ;;
    -h|--help)
      cat <<USAGE
Usage: ./install.sh [--dry-run] [--uninstall] [--no-apply] [--no-xresources] [--no-autostart]
  --no-apply        do not touch the running X session (the settings then take effect at next login)
  --no-xresources   do not make Fixed Nerd the default font of xterm/uxterm (in ~/.Xresources)
  --no-autostart    do not add the font directory to the font path at login (Window Maker autostart)
  --uninstall       remove the font and both blocks again
Environment: FIXEDNERD_DIR (where the font goes), XRESOURCES_FILE, AUTOSTART_FILE.
USAGE
      exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

have() { command -v "$1" >/dev/null 2>&1; }
run() { if [ "$DRY" = 1 ]; then echo "[dry-run] $*"; else "$@"; fi; }
live() { [ "$APPLY" = 1 ] && [ "$DRY" = 0 ] && [ -n "${DISPLAY:-}" ] && have xset; }

block() {  # block add|remove FILE COMMENT_CHAR [CONTENT]
  [ "$DRY" = 1 ] && { echo "[dry-run] block $1 in $2"; return 0; }
  python3 - "$1" "$2" "$3" "$NAME" "${4:-}" <<'PY'
import os, re, sys
action, path, c, name, content = sys.argv[1:6]
begin, end = f"{c} >>> {name} >>>", f"{c} <<< {name} <<<"
text = open(path).read() if os.path.exists(path) else None
if text is None and action == "remove":
    sys.exit(0)
text = re.sub(r"(?ms)^" + re.escape(begin) + r"\n.*?^" + re.escape(end) + r"\n?", "", text or "")
if action == "remove":
    text = text.rstrip("\n") + "\n" if text.strip() else ""
else:
    blk = f"{begin}\n{content.rstrip()}\n{end}\n"
    last = list(re.finditer(r"(?m)^exit\s+0\s*$", text))
    if last and c == "#":
        i = last[-1].start(); text = text[:i] + blk + text[i:]
    else:
        text = text.rstrip("\n"); text = (text + "\n\n" if text else ("#!/bin/sh\n\n" if c == "#" else "")) + blk
os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
open(path, "w").write(text)
PY
  [ "$3" = "#" ] && [ -f "$2" ] && head -c 2 "$2" | grep -q '^#!' && chmod +x "$2" || true
}

if [ "$UNINSTALL" = 1 ]; then
  live && { xset -fp "$DEST" 2>/dev/null || true; xset fp rehash 2>/dev/null || true; }
  block remove "$AUTOSTART" "#"
  block remove "$XRES" "!"
  run rm -rf -- "$DEST"
  echo "Removed Fixed Nerd. Terminals that are already open keep the font until they are closed;"
  echo "new ones use the default again (xrdb cannot delete keys: log out and in to drop the old setting)."
  exit 0
fi

missing=(); have bdftopcf || missing+=(xfonts-utils); have mkfontdir || missing+=(xfonts-utils); have python3 || missing+=(python3)
if [ "${#missing[@]}" -gt 0 ]; then
  echo "Missing: $(printf '%s\n' "${missing[@]}" | sort -u | tr '\n' ' ') -- install with: sudo apt install $(printf '%s\n' "${missing[@]}" | sort -u | tr '\n' ' ')"
  [ "$DRY" = 1 ] || exit 1
fi
[ -f "$SRC" ] || { echo "font source not found: $SRC" >&2; exit 1; }

run mkdir -p "$DEST"
if [ "$DRY" = 1 ]; then
  echo "[dry-run] bdftopcf $SRC | gzip > $DEST/fixednerd6x13.pcf.gz; mkfontdir $DEST"
else
  bdftopcf -t "$SRC" | gzip -9 -n > "$DEST/fixednerd6x13.pcf.gz"
  mkfontdir "$DEST"
fi
echo "Font installed in $DEST"

if [ "$STARTUP" = 1 ]; then
  d=${DEST/#"$HOME"/\$HOME}      # keep $HOME symbolic in the file
  block add "$AUTOSTART" "#" "# Fixed Nerd: put the font on the X font path (new terminals pick it up)
xset -fp \"$d\" 2>/dev/null; xset +fp \"$d\" && xset fp rehash"
fi
if [ "$XRESOURCES" = 1 ]; then
  block add "$XRES" "!" "UXTerm*font: $XLFD
XTerm*font: $XLFD"
fi
if live; then
  xset -fp "$DEST" 2>/dev/null || true; xset +fp "$DEST"; xset fp rehash
  [ "$XRESOURCES" = 1 ] && have xrdb && [ -f "$XRES" ] && xrdb -merge "$XRES"
  echo "Active in this session: new xterm/uxterm windows use it; windows that are already open do not change."
else
  echo "No running X session touched: the font and settings apply from your next login."
fi
